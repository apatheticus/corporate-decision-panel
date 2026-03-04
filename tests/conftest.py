"""Shared test fixtures for CDP config testing."""

from pathlib import Path

import pytest


@pytest.fixture
def make_config(tmp_path):
    """Factory fixture: returns a callable that creates a temporary config file.

    Usage:
        config_path = make_config("- **Gemini API Key:** my-key-123")
        # config_path points to tmp_path / ".cdp-context" / "config.md"
    """

    def _make(content: str) -> Path:
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "config.md"
        config_file.write_text(content)
        return config_dir

    return _make


@pytest.fixture
def valid_config_content():
    """Returns a config string with all three fields properly filled."""
    return (
        "# CDP Configuration\n"
        "\n"
        "## Image Generation\n"
        "\n"
        "- **Gemini API Key:** test-key-abc123\n"
        "- **Image Model:** gemini-2.5-flash-image\n"
        "- **Retry Limit:** 3\n"
    )


@pytest.fixture
def template_path():
    """Returns path to the config template for validation tests."""
    return Path("templates/config-context.md")
