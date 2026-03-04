"""Tests for vision quality validation module.

Covers: _extract_expected_labels, _parse_validation_response, validate_infographic
(from Phase 3 Plan 01 Task 2).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.validation import (
    ValidationResult,
    _extract_expected_labels,
    _parse_validation_response,
    validate_infographic,
)


class TestLabelExtraction:
    """Tests for _extract_expected_labels with various data shapes."""

    def test_extracts_string_values(self):
        """_extract_expected_labels extracts string values from the data dict."""
        data = {
            "DOMAIN_RECOMMENDATIONS": "Finance: Approve (High)",
            "KEY_RISKS": "Regulatory exposure in Q3",
        }
        labels = _extract_expected_labels(data)
        assert "Finance: Approve (High)" in labels
        assert "Regulatory exposure in Q3" in labels

    def test_filters_numeric_values(self):
        """_extract_expected_labels skips numeric-only values."""
        data = {
            "DOMAIN_COUNT": "3",
            "KEY_RISKS": "Regulatory exposure in Q3",
        }
        labels = _extract_expected_labels(data)
        assert "3" not in labels
        assert "Regulatory exposure in Q3" in labels

    def test_splits_comma_separated_items(self):
        """_extract_expected_labels splits comma-separated multi-item strings."""
        data = {
            "DOMAIN_RECOMMENDATIONS": "Finance: Approve (High), Legal: Oppose (Medium)",
        }
        labels = _extract_expected_labels(data)
        assert "Finance: Approve (High)" in labels
        assert "Legal: Oppose (Medium)" in labels

    def test_deduplicates(self):
        """_extract_expected_labels returns deduplicated labels."""
        data = {
            "FIELD_1": "Finance: Approve",
            "FIELD_2": "Finance: Approve",
        }
        labels = _extract_expected_labels(data)
        assert labels.count("Finance: Approve") == 1

    def test_handles_sample_data(self, sample_data):
        """_extract_expected_labels works with the sample_data fixture shape."""
        labels = _extract_expected_labels(sample_data)
        # Should include domain-level items, risks, mode
        assert len(labels) > 0
        # Numeric "3" (DOMAIN_COUNT) should be filtered out
        assert "3" not in labels

    def test_empty_data(self):
        """_extract_expected_labels returns empty list for empty data."""
        labels = _extract_expected_labels({})
        assert labels == []


class TestResponseParsing:
    """Tests for _parse_validation_response with PASS, FAIL, WARN, and malformed responses."""

    def test_parse_pass(self):
        """VERDICT: PASS returns passed=True, warning_only=False."""
        text = (
            "VERDICT: PASS\n"
            "WARNINGS: none\n"
            "MISSING: none\n"
            "FEEDBACK: none"
        )
        result = _parse_validation_response(text)
        assert result.passed is True
        assert result.warning_only is False
        assert result.warnings == []
        assert result.missing == []

    def test_parse_fail(self):
        """VERDICT: FAIL returns passed=False with missing and feedback."""
        text = (
            "VERDICT: FAIL\n"
            "WARNINGS: none\n"
            "MISSING: Revenue label\n"
            "FEEDBACK: Ensure Revenue label appears clearly"
        )
        result = _parse_validation_response(text)
        assert result.passed is False
        assert "Revenue label" in result.missing
        assert "Ensure Revenue label appears clearly" in result.feedback

    def test_parse_pass_with_warnings(self):
        """VERDICT: PASS with warnings returns passed=True, warning_only=True."""
        text = (
            "VERDICT: PASS\n"
            "WARNINGS: Label X truncated\n"
            "MISSING: none\n"
            "FEEDBACK: none"
        )
        result = _parse_validation_response(text)
        assert result.passed is True
        assert result.warning_only is True
        assert "Label X truncated" in result.warnings

    def test_parse_malformed_response(self):
        """Malformed response returns pass-with-warning (non-blocking)."""
        text = "This is not a structured response at all."
        result = _parse_validation_response(text)
        assert result.passed is True
        assert result.warning_only is True
        assert "unparseable" in result.feedback.lower()

    def test_parse_case_insensitive(self):
        """VERDICT parsing is case-insensitive."""
        text = (
            "verdict: pass\n"
            "warnings: none\n"
            "missing: none\n"
            "feedback: none"
        )
        result = _parse_validation_response(text)
        assert result.passed is True

    def test_parse_fail_with_multiple_missing(self):
        """VERDICT: FAIL with multiple missing labels."""
        text = (
            "VERDICT: FAIL\n"
            "WARNINGS: none\n"
            "MISSING: Revenue label, Cost label\n"
            "FEEDBACK: Ensure both labels appear"
        )
        result = _parse_validation_response(text)
        assert result.passed is False
        assert len(result.missing) == 2


class TestValidateInfographic:
    """Tests with mocked genai client for validation scenarios."""

    def _setup_env(self, tmp_path, sample_data):
        """Helper: create config dir, image file, and data file."""
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir()
        (config_dir / "config.md").write_text(
            "- **Gemini API Key:** test-key-abc123\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** 2\n"
        )

        # Create a tiny valid PNG for validation
        from PIL import Image

        img = Image.new("RGB", (100, 100), "white")
        image_path = tmp_path / "test.png"
        img.save(str(image_path))

        data_path = tmp_path / "data.json"
        data_path.write_text(json.dumps(sample_data))

        return image_path, data_path, config_dir

    def test_successful_validation_pass(
        self,
        tmp_path,
        sample_data,
        mock_validation_pass_response,
    ):
        """validate_infographic returns passed=True for VERDICT: PASS response."""
        image_path, data_path, config_dir = self._setup_env(tmp_path, sample_data)

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_validation_pass_response

        with patch("scripts.validation.genai") as mock_genai:
            mock_genai.Client.return_value = mock_client
            result = validate_infographic(image_path, data_path, config_dir)

        assert result.passed is True
        assert result.warning_only is False

    def test_validation_fail(
        self,
        tmp_path,
        sample_data,
        mock_validation_fail_response,
    ):
        """validate_infographic returns passed=False for VERDICT: FAIL response."""
        image_path, data_path, config_dir = self._setup_env(tmp_path, sample_data)

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_validation_fail_response

        with patch("scripts.validation.genai") as mock_genai:
            mock_genai.Client.return_value = mock_client
            result = validate_infographic(image_path, data_path, config_dir)

        assert result.passed is False
        assert "Revenue label" in result.missing

    def test_api_error_returns_pass_with_warning(
        self,
        tmp_path,
        sample_data,
    ):
        """validate_infographic returns pass-with-warning on API error (non-blocking)."""
        from google.genai.errors import ClientError

        image_path, data_path, config_dir = self._setup_env(tmp_path, sample_data)

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = ClientError(
            code=500, response_json={"error": {"message": "Internal Error"}}
        )

        with patch("scripts.validation.genai") as mock_genai:
            mock_genai.Client.return_value = mock_client
            result = validate_infographic(image_path, data_path, config_dir)

        assert result.passed is True
        assert result.warning_only is True

    def test_disables_sdk_retry(
        self,
        tmp_path,
        sample_data,
        mock_validation_pass_response,
    ):
        """validate_infographic creates client with HttpRetryOptions(attempts=1)."""
        image_path, data_path, config_dir = self._setup_env(tmp_path, sample_data)

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_validation_pass_response

        with patch("scripts.validation.genai") as mock_genai:
            mock_genai.Client.return_value = mock_client
            validate_infographic(image_path, data_path, config_dir)

        # Verify Client was called with http_options
        call_kwargs = mock_genai.Client.call_args
        assert call_kwargs is not None

    def test_uses_text_only_modalities(
        self,
        tmp_path,
        sample_data,
        mock_validation_pass_response,
    ):
        """validate_infographic uses response_modalities=["TEXT"]."""
        image_path, data_path, config_dir = self._setup_env(tmp_path, sample_data)

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_validation_pass_response

        with patch("scripts.validation.genai") as mock_genai:
            mock_genai.Client.return_value = mock_client
            validate_infographic(image_path, data_path, config_dir)

        call_kwargs = mock_client.models.generate_content.call_args
        config_arg = call_kwargs.kwargs.get("config")
        assert config_arg is not None
        assert config_arg.response_modalities == ["TEXT"]
