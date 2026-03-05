"""Shared test fixtures for CDP testing.

Provides fixtures for config testing, prompt template testing,
and generation pipeline testing (mocked Gemini API).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image


# ---------------------------------------------------------------------------
# Config fixtures
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Prompt template fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_template():
    """A realistic template dict matching the JSON template structure.

    Mirrors domain-scorecard.json with enough fields to exercise
    all serialization paths: objects, notes, constraints, style,
    color_mapping, quality_keywords, extras.data.
    """
    return {
        "core": {
            "subject": "Domain Scorecard -- recommendation and confidence matrix",
            "objects": [
                "{{DOMAIN_RECOMMENDATIONS}} -- per-domain recommendation with confidence level",
                "{{KEY_RISKS}} -- top risk identified per domain",
            ],
            "notes": [
                "{{ACTIVATED_DOMAINS}} -- list of domains that participated",
                "{{DECISION_MODE}} -- the synthesis mode applied",
            ],
            "constraints": [
                "All text must be legible at 6.5 inch print width",
                "No decorative elements -- every visual element conveys data",
                "White or transparent background",
            ],
        },
        "style": {
            "primary_style": "editorial",
            "render_quality": "professional-quality",
            "lighting": "soft-ambient",
            "color_profile": "neutral",
        },
        "technical": {
            "resolution": "4k",
            "anti_aliasing": True,
            "noise": "low",
            "color_depth": "high",
        },
        "composition": {
            "perspective": "natural_human_vision",
            "framing": "centered",
        },
        "quality_keywords": {
            "include": ["studio quality", "photographic quality"],
            "avoid": ["digital artifacts", "blurry", "oversaturated colors"],
        },
        "extras": {
            "color_mapping": {
                "approve": "#2E7D32",
                "oppose": "#C62828",
                "neutral": "#757575",
            },
            "data": {
                "domain_count": "{{DOMAIN_COUNT}} -- number of activated domains",
                "consensus_level": "{{CONSENSUS_LEVEL}} -- overall consensus level",
            },
        },
    }


@pytest.fixture
def sample_data():
    """Data dict mapping placeholder tokens to concrete values."""
    return {
        "DOMAIN_RECOMMENDATIONS": "Finance: Approve (High), Legal: Oppose (Medium)",
        "KEY_RISKS": "Regulatory exposure in Q3",
        "ACTIVATED_DOMAINS": "Finance, Legal, Operations",
        "DECISION_MODE": "Guardian",
        "DOMAIN_COUNT": "3",
        "CONSENSUS_LEVEL": "mild dissent",
    }


@pytest.fixture
def sample_template_path(tmp_path, sample_template):
    """Writes sample_template to a temp directory as domain-scorecard.json.

    Returns the directory path (to pass as template_dir).
    """
    template_file = tmp_path / "domain-scorecard.json"
    template_file.write_text(json.dumps(sample_template, indent=2))
    return tmp_path


# ---------------------------------------------------------------------------
# Generation pipeline fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_genai_image_response():
    """A mock Gemini API response containing a 1x1 white PNG image.

    The mock response has one part with ``inline_data`` that returns
    a PIL Image from ``part.as_image()``.
    """
    img = Image.new("RGB", (1, 1), color=(255, 255, 255))
    part = MagicMock()
    part.inline_data = True  # truthy to pass ``is not None`` check
    part.as_image.return_value = img
    response = MagicMock()
    response.parts = [part]
    return response


@pytest.fixture
def mock_genai_text_only_response():
    """A mock Gemini API response containing only text (no image).

    Used to test the NO_IMAGE_IN_RESPONSE error path.
    """
    part = MagicMock()
    part.inline_data = None
    part.text = "Here is a description of the infographic."
    response = MagicMock()
    response.parts = [part]
    return response


@pytest.fixture
def sample_data_file(tmp_path, sample_data):
    """Writes sample_data to a JSON file in tmp_path and returns the path."""
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps(sample_data))
    return data_file


# ---------------------------------------------------------------------------
# Content block fixtures (Phase 3)
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_content_blocked_response():
    """A mock Gemini API response with prompt-level content block.

    Simulates a 200 OK response where prompt_feedback.block_reason = "SAFETY".
    No image data is present.
    """
    response = MagicMock()
    response.prompt_feedback = MagicMock()
    response.prompt_feedback.block_reason = "SAFETY"
    response.candidates = []
    response.parts = []
    return response


@pytest.fixture
def mock_candidate_blocked_response():
    """A mock Gemini API response with candidate-level content block.

    Simulates a 200 OK response where candidates[0].finish_reason = "IMAGE_SAFETY".
    No image data is present, but prompt_feedback has no block_reason.
    """
    candidate = MagicMock()
    candidate.finish_reason = "IMAGE_SAFETY"
    response = MagicMock()
    response.prompt_feedback = MagicMock()
    response.prompt_feedback.block_reason = None
    response.candidates = [candidate]
    # Parts exist but have no inline_data
    part = MagicMock()
    part.inline_data = None
    response.parts = [part]
    return response


# ---------------------------------------------------------------------------
# Validation fixtures (Phase 3)
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_validation_pass_response():
    """A mock Gemini vision response indicating validation passed.

    Returns structured text with VERDICT: PASS.
    """
    response = MagicMock()
    response.text = (
        "VERDICT: PASS\n"
        "WARNINGS: none\n"
        "MISSING: none\n"
        "GARBLED: none\n"
        "FEEDBACK: none"
    )
    return response


@pytest.fixture
def mock_validation_fail_response():
    """A mock Gemini vision response indicating validation failed.

    Returns structured text with VERDICT: FAIL and specific missing labels.
    """
    response = MagicMock()
    response.text = (
        "VERDICT: FAIL\n"
        "WARNINGS: none\n"
        "MISSING: Revenue label\n"
        "GARBLED: none\n"
        "FEEDBACK: Ensure Revenue label appears clearly"
    )
    return response


@pytest.fixture
def mock_validation_garbled_response():
    """A mock Gemini vision response indicating garbled text detected.

    Returns structured text with VERDICT: FAIL and garbled text items.
    """
    response = MagicMock()
    response.text = (
        "VERDICT: FAIL\n"
        "WARNINGS: none\n"
        "MISSING: none\n"
        "GARBLED: Emmerruation, Recommendians\n"
        "FEEDBACK: Fix garbled text: 'Emmerruation' should be 'Enumeration'"
    )
    return response
