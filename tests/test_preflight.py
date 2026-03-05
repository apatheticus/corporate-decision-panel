"""Tests for scripts.preflight -- pre-flight validation with mocked API calls."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from google.genai.errors import ClientError
from scripts.config import ConfigError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_client_error(code: int, message: str = "", status: str = "") -> ClientError:
    """Create a ClientError with the given HTTP status code."""
    response_json = {"message": message, "status": status}
    return ClientError(code, response_json)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_genai_client():
    """Configurable mock for genai.Client.

    The mock's `models` attribute has .list(), .get(), and .generate_content()
    that all succeed by default.  Override any one to raise ClientError for
    specific failure scenarios.
    """
    client = MagicMock()
    client.models.list.return_value = iter([MagicMock(name="models/gemini-2.5-flash-image")])
    client.models.get.return_value = MagicMock(name="models/gemini-2.5-flash-image")
    client.models.generate_content.return_value = MagicMock()
    return client


@pytest.fixture
def config_dir_with_key(make_config):
    """Returns a config directory with a valid API key filled in."""
    content = (
        "- **Gemini API Key:** AIzaSyA1_test_key_for_preflight\n"
        "- **Image Model:** gemini-2.5-flash-image\n"
        "- **Retry Limit:** 2\n"
    )
    return make_config(content)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestPreflightSuccess:
    """Tests for successful pre-flight validation."""

    def test_preflight_success(self, config_dir_with_key, mock_genai_client):
        """All 4 steps pass, returns PreflightResult(success=True)."""
        from scripts.preflight import run_preflight, PreflightResult

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            result = run_preflight(config_dir_with_key)

        assert isinstance(result, PreflightResult)
        assert result.success is True
        assert result.error_code is None
        assert result.model_id == "gemini-2.5-flash-image"

    def test_preflight_success_message_format(self, config_dir_with_key, mock_genai_client, capsys):
        """Success output contains 'PREFLIGHT OK', 'Model:', and 'Key:'."""
        from scripts.preflight import run_preflight

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            run_preflight(config_dir_with_key)

        captured = capsys.readouterr()
        assert "PREFLIGHT OK" in captured.out
        assert "Model:" in captured.out
        assert "Key:" in captured.out

    def test_preflight_key_preview(self, config_dir_with_key, mock_genai_client, capsys):
        """Success message shows first 8 chars of key + '...', not the full key."""
        from scripts.preflight import run_preflight

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            run_preflight(config_dir_with_key)

        captured = capsys.readouterr()
        # Key is "AIzaSyA1_test_key_for_preflight"; first 8 = "AIzaSyA1"
        assert "AIzaSyA1..." in captured.out
        # Full key must NOT appear
        assert "AIzaSyA1_test_key_for_preflight" not in captured.out


class TestPreflightAPIErrors:
    """Tests for API-level failure conditions (steps 2-4)."""

    def test_preflight_invalid_key(self, config_dir_with_key, mock_genai_client):
        """client.models.list() raises ClientError(403) -> INVALID_API_KEY."""
        from scripts.preflight import run_preflight

        mock_genai_client.models.list.side_effect = _make_client_error(
            403, "API key not valid", "PERMISSION_DENIED"
        )

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            result = run_preflight(config_dir_with_key)

        assert result.success is False
        assert result.error_code == "INVALID_API_KEY"

    def test_preflight_model_not_found(self, config_dir_with_key, mock_genai_client):
        """client.models.get() raises ClientError(404) -> MODEL_NOT_FOUND."""
        from scripts.preflight import run_preflight

        mock_genai_client.models.get.side_effect = _make_client_error(
            404, "Model not found", "NOT_FOUND"
        )

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            result = run_preflight(config_dir_with_key)

        assert result.success is False
        assert result.error_code == "MODEL_NOT_FOUND"

    def test_preflight_billing_not_enabled(self, config_dir_with_key, mock_genai_client):
        """generate_content() raises ClientError(403) -> BILLING_NOT_ENABLED."""
        from scripts.preflight import run_preflight

        mock_genai_client.models.generate_content.side_effect = _make_client_error(
            403, "Billing not enabled", "PERMISSION_DENIED"
        )

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            result = run_preflight(config_dir_with_key)

        assert result.success is False
        assert result.error_code == "BILLING_NOT_ENABLED"

    def test_preflight_rate_limited(self, config_dir_with_key, mock_genai_client):
        """generate_content() raises ClientError(429) -> RATE_LIMITED."""
        from scripts.preflight import run_preflight

        mock_genai_client.models.generate_content.side_effect = _make_client_error(
            429, "Resource exhausted", "RESOURCE_EXHAUSTED"
        )

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            result = run_preflight(config_dir_with_key)

        assert result.success is False
        assert result.error_code == "RATE_LIMITED"


class TestPreflightConfigError:
    """Tests for configuration-level failures (step 1)."""

    def test_preflight_config_error(self, make_config):
        """load_config raises ConfigError -> failure with matching error_code."""
        from scripts.preflight import run_preflight

        # Provide a config with no API key -- triggers CONFIG_MISSING_KEY
        content = (
            "- **Gemini API Key:** (paste your key here)\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** 2\n"
        )
        config_dir = make_config(content)
        result = run_preflight(config_dir)

        assert result.success is False
        assert result.error_code == "CONFIG_MISSING_KEY"


class TestPreflightMessageFormat:
    """Tests for dual-audience error message format."""

    def test_preflight_error_message_format(self, config_dir_with_key, mock_genai_client, capsys):
        """Error output contains 'PREFLIGHT FAILED [CODE]', 'Error:', and 'Fix:'."""
        from scripts.preflight import run_preflight

        mock_genai_client.models.list.side_effect = _make_client_error(
            403, "API key not valid", "PERMISSION_DENIED"
        )

        with patch("scripts.preflight.genai") as mock_genai:
            mock_genai.Client.return_value = mock_genai_client
            run_preflight(config_dir_with_key)

        captured = capsys.readouterr()
        assert "PREFLIGHT FAILED [INVALID_API_KEY]" in captured.out
        assert "Error:" in captured.out
        assert "Fix:" in captured.out
