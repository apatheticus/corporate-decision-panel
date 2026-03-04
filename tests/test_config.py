"""Tests for scripts.config — config template and parser."""

from pathlib import Path

import pytest

from scripts.config import ConfigError, load_config, parse_config


# --- parse_config tests ---


class TestParseConfig:
    """Tests for the low-level parse_config function."""

    def test_parse_valid_config(self, make_config, valid_config_content):
        """All three fields extracted correctly from a valid config."""
        config_dir = make_config(valid_config_content)
        result = parse_config(config_dir / "config.md")

        assert result["gemini api key"] == "test-key-abc123"
        assert result["image model"] == "gemini-2.5-flash-image"
        assert result["retry limit"] == "3"

    def test_parse_placeholder_values(self, make_config):
        """Parenthetical placeholder values are treated as empty string."""
        content = (
            "- **Gemini API Key:** (paste your key here)\n"
            "- **Image Model:** (default: gemini-2.5-flash-image)\n"
            "- **Retry Limit:** (default: 2)\n"
        )
        config_dir = make_config(content)
        result = parse_config(config_dir / "config.md")

        # "(paste your key here)" has no default pattern -- empty
        assert result["gemini api key"] == ""

    def test_parse_default_extraction(self, make_config):
        """'(default: X)' placeholder extracts X as the value."""
        content = (
            "- **Gemini API Key:** my-real-key\n"
            "- **Image Model:** (default: gemini-2.5-flash-image)\n"
            "- **Retry Limit:** (default: 2)\n"
        )
        config_dir = make_config(content)
        result = parse_config(config_dir / "config.md")

        assert result["image model"] == "gemini-2.5-flash-image"
        assert result["retry limit"] == "2"

    def test_parse_missing_file(self, tmp_path):
        """Raises ConfigError when config file does not exist."""
        missing = tmp_path / "nonexistent.md"
        with pytest.raises(ConfigError) as exc_info:
            parse_config(missing)
        assert exc_info.value.error_code == "CONFIG_NOT_FOUND"


# --- load_config tests ---


class TestLoadConfig:
    """Tests for the high-level load_config function."""

    def test_load_config_valid(self, make_config, valid_config_content):
        """Returns typed dict with api_key, model_id, retry_limit."""
        config_dir = make_config(valid_config_content)
        result = load_config(config_dir)

        assert result["api_key"] == "test-key-abc123"
        assert result["model_id"] == "gemini-2.5-flash-image"
        assert result["retry_limit"] == 3
        assert isinstance(result["retry_limit"], int)

    def test_load_config_missing_key(self, make_config):
        """Raises ConfigError with CONFIG_MISSING_KEY when API key is placeholder."""
        content = (
            "- **Gemini API Key:** (paste your key here)\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** 2\n"
        )
        config_dir = make_config(content)
        with pytest.raises(ConfigError) as exc_info:
            load_config(config_dir)
        assert exc_info.value.error_code == "CONFIG_MISSING_KEY"
        assert "api key" in exc_info.value.message.lower()

    def test_load_config_default_model(self, make_config):
        """Defaults model_id to gemini-2.5-flash-image when field is placeholder."""
        content = (
            "- **Gemini API Key:** real-key-xyz\n"
            "- **Image Model:** (default: gemini-2.5-flash-image)\n"
            "- **Retry Limit:** 2\n"
        )
        config_dir = make_config(content)
        result = load_config(config_dir)

        assert result["model_id"] == "gemini-2.5-flash-image"

    def test_load_config_default_retry(self, make_config):
        """Defaults retry_limit to 2 when field is placeholder."""
        content = (
            "- **Gemini API Key:** real-key-xyz\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** (default: 2)\n"
        )
        config_dir = make_config(content)
        result = load_config(config_dir)

        assert result["retry_limit"] == 2

    def test_load_config_invalid_retry(self, make_config):
        """Raises ConfigError for non-integer retry limit."""
        content = (
            "- **Gemini API Key:** real-key-xyz\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** banana\n"
        )
        config_dir = make_config(content)
        with pytest.raises(ConfigError) as exc_info:
            load_config(config_dir)
        assert exc_info.value.error_code == "CONFIG_INVALID_RETRY"


# --- Template validation tests ---


class TestTemplate:
    """Tests that validate the config template file itself."""

    def test_template_has_required_fields(self, template_path):
        """Template contains all three required fields."""
        content = template_path.read_text()
        assert "**Gemini API Key:**" in content
        assert "**Image Model:**" in content
        assert "**Retry Limit:**" in content

    def test_template_no_platform_field(self, template_path):
        """Template does NOT contain the removed Platform field."""
        content = template_path.read_text()
        assert "Platform" not in content
