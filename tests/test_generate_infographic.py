"""Tests for infographic generation pipeline.

Covers: load_template, substitute_placeholders, serialize_template, save_prompt
(from Plan 01), plus generate_infographic, aspect ratios, thinking config,
preflight integration, and CLI wrapper (from Plan 02), live end-to-end
generation with dimension verification (from Plan 03), and retry/backoff/session
orchestration (from Plan 03-02).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from PIL import Image

from scripts.config import ConfigError
from scripts.generate_infographic import GenerationResult, generate_infographic


class TestPromptSerialization:
    """Tests for the prompt serialization pipeline: template loading,
    placeholder substitution, and natural language serialization."""

    # --- load_template ---

    def test_load_template_returns_dict(self, sample_template_path):
        """load_template reads a JSON template and returns a dict."""
        from scripts.generate_infographic import load_template

        result = load_template("domain-scorecard", template_dir=sample_template_path)
        assert isinstance(result, dict)
        assert "core" in result
        assert "style" in result

    def test_load_template_normalizes_underscores(self, sample_template_path):
        """load_template normalizes underscores to hyphens in the type slug."""
        from scripts.generate_infographic import load_template

        result = load_template("domain_scorecard", template_dir=sample_template_path)
        assert result["core"]["subject"] == "Domain Scorecard -- recommendation and confidence matrix"

    def test_load_template_raises_on_missing(self, tmp_path):
        """load_template raises ConfigError with TEMPLATE_NOT_FOUND for nonexistent types."""
        from scripts.generate_infographic import load_template

        with pytest.raises(ConfigError) as exc_info:
            load_template("nonexistent-type", template_dir=tmp_path)
        assert exc_info.value.error_code == "TEMPLATE_NOT_FOUND"

    # --- substitute_placeholders ---

    def test_substitute_replaces_known_tokens(self):
        """substitute_placeholders replaces {{TOKEN}} with data dict values."""
        from scripts.generate_infographic import substitute_placeholders

        text = "Show {{DOMAIN_RECOMMENDATIONS}} for {{ACTIVATED_DOMAINS}}"
        data = {
            "DOMAIN_RECOMMENDATIONS": "Finance: Approve (High)",
            "ACTIVATED_DOMAINS": "Finance, Legal, Operations",
        }
        result = substitute_placeholders(text, data)
        assert result == "Show Finance: Approve (High) for Finance, Legal, Operations"

    def test_substitute_unknown_tokens_become_bracketed(self):
        """substitute_placeholders replaces unknown {{TOKEN}} with [TOKEN]."""
        from scripts.generate_infographic import substitute_placeholders

        text = "Show {{UNKNOWN_FIELD}} here"
        result = substitute_placeholders(text, {})
        assert result == "Show [UNKNOWN_FIELD] here"

    def test_substitute_mixed_known_and_unknown(self):
        """substitute_placeholders handles mix of present and absent keys."""
        from scripts.generate_infographic import substitute_placeholders

        text = "{{KNOWN}} and {{MISSING}}"
        data = {"KNOWN": "value"}
        result = substitute_placeholders(text, data)
        assert result == "value and [MISSING]"

    def test_substitute_no_placeholders(self):
        """substitute_placeholders returns text unchanged when no placeholders."""
        from scripts.generate_infographic import substitute_placeholders

        text = "No placeholders here"
        result = substitute_placeholders(text, {"KEY": "val"})
        assert result == "No placeholders here"

    def test_substitute_strips_description_suffix(self):
        """substitute_placeholders handles template strings with ' -- description' suffixes.

        Template objects are like '{{TOKEN}} -- description text'.
        The placeholder is replaced but the description part remains.
        """
        from scripts.generate_infographic import substitute_placeholders

        text = "{{DOMAIN_RECOMMENDATIONS}} -- per-domain recommendation"
        data = {"DOMAIN_RECOMMENDATIONS": "Finance: Approve (High)"}
        result = substitute_placeholders(text, data)
        assert result == "Finance: Approve (High) -- per-domain recommendation"

    # --- serialize_template ---

    def test_serialize_starts_with_subject(self, sample_template, sample_data):
        """serialize_template prompt starts with 'Create a {subject}'."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        assert result.startswith("Create a ")
        assert "Domain Scorecard" in result

    def test_serialize_includes_populated_objects(self, sample_template, sample_data):
        """serialize_template includes objects with data substituted."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        # Data was substituted into the objects
        assert "Finance: Approve (High)" in result

    def test_serialize_includes_notes(self, sample_template, sample_data):
        """serialize_template includes notes with data substituted."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        assert "Finance, Legal, Operations" in result

    def test_serialize_includes_constraints(self, sample_template, sample_data):
        """serialize_template includes constraints."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        assert "legible at 6.5 inch" in result

    def test_serialize_includes_style_cues(self, sample_template, sample_data):
        """serialize_template includes primary_style and render_quality."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        assert "editorial" in result
        assert "professional-quality" in result

    def test_serialize_includes_hex_colors(self, sample_template, sample_data):
        """serialize_template includes hex color codes from extras.color_mapping."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        assert "#2E7D32" in result
        assert "#C62828" in result
        assert "approve" in result.lower()

    def test_serialize_includes_quality_keywords(self, sample_template, sample_data):
        """serialize_template includes quality keyword include items."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        assert "studio quality" in result

    def test_serialize_includes_extras_data(self, sample_template, sample_data):
        """serialize_template includes extras.data fields with data substituted."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        # DOMAIN_COUNT was in sample_data, should be substituted
        assert "3" in result  # DOMAIN_COUNT value

    def test_serialize_no_raw_json(self, sample_template, sample_data):
        """serialize_template output contains no raw JSON artifacts."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        # Must not contain JSON structural chars in suspicious patterns
        assert '": "' not in result
        assert '": {' not in result
        assert '": [' not in result

    def test_serialize_with_style_override(self, sample_template, sample_data):
        """serialize_template with style_override appends it as additional guidance."""
        from scripts.generate_infographic import serialize_template

        override = "Use the company brand colors. Prefer sans-serif fonts."
        result = serialize_template(sample_template, sample_data, style_override=override)
        assert "Additional style guidance:" in result
        assert "Use the company brand colors" in result
        assert "sans-serif fonts" in result

    def test_serialize_without_style_override(self, sample_template, sample_data):
        """serialize_template without style_override does not include style section."""
        from scripts.generate_infographic import serialize_template

        result = serialize_template(sample_template, sample_data)
        assert "Additional style guidance:" not in result

    # --- save_prompt ---

    def test_save_prompt_writes_file(self, tmp_path):
        """save_prompt writes the prompt to the correct path."""
        from scripts.generate_infographic import save_prompt

        prompt = "Create a Domain Scorecard infographic."
        result = save_prompt(prompt, tmp_path, "domain-scorecard")
        assert result.exists()
        assert result.read_text() == prompt

    def test_save_prompt_filename_pattern(self, tmp_path):
        """save_prompt uses INFOGRAPHIC_{type-slug}_PROMPT.txt pattern."""
        from scripts.generate_infographic import save_prompt

        result = save_prompt("test prompt", tmp_path, "domain-scorecard")
        assert result.name == "INFOGRAPHIC_domain-scorecard_PROMPT.txt"

    def test_save_prompt_creates_parent_dirs(self, tmp_path):
        """save_prompt creates parent directories if they don't exist."""
        from scripts.generate_infographic import save_prompt

        nested = tmp_path / "session" / "images"
        result = save_prompt("test prompt", nested, "routing-diagram")
        assert result.exists()
        assert result.parent == nested


# ---------------------------------------------------------------------------
# Generation pipeline tests (Plan 02)
# ---------------------------------------------------------------------------


class TestGeneration:
    """Tests for the generate_infographic() function: API call configuration,
    PNG output, prompt saving, error handling, and preflight integration."""

    def _setup_env(self, tmp_path, sample_data, sample_template):
        """Helper: create config dir, template dir, and data file for generation tests.

        Returns (data_path, output_path, config_dir, template_dir).
        """
        # Config directory with valid key
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir()
        (config_dir / "config.md").write_text(
            "- **Gemini API Key:** test-key-abc123\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** 2\n"
        )

        # Template directory
        template_dir = tmp_path / "templates" / "infographic-prompts"
        template_dir.mkdir(parents=True)
        (template_dir / "domain-scorecard.json").write_text(
            json.dumps(sample_template, indent=2)
        )
        (template_dir / "fault-line-map.json").write_text(
            json.dumps(sample_template, indent=2)
        )

        # Data file
        data_path = tmp_path / "data.json"
        data_path.write_text(json.dumps(sample_data))

        # Output path
        output_path = tmp_path / "output" / "infographic.png"

        return data_path, output_path, config_dir, template_dir

    def test_api_call_config(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_genai_image_response,
    ):
        """generate_content is called with response_modalities=["TEXT", "IMAGE"] and image_size="2K"."""
        from scripts.generate_infographic import generate_infographic

        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_genai_image_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is True
        # Verify generate_content was called
        call_args = mock_client.models.generate_content.call_args
        assert call_args is not None
        config_arg = call_args.kwargs.get("config") or call_args[1].get("config")
        assert config_arg.response_modalities == ["TEXT", "IMAGE"]
        assert config_arg.image_config.image_size == "2K"

    def test_png_saved(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_genai_image_response,
    ):
        """generate_infographic saves a PNG file at output_path."""
        from scripts.generate_infographic import generate_infographic

        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_genai_image_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is True
        assert result.output_path == output_path
        assert output_path.exists()

    def test_prompt_saved(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_genai_image_response,
    ):
        """generate_infographic saves a PROMPT.txt file alongside the output."""
        from scripts.generate_infographic import generate_infographic

        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_genai_image_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is True
        assert result.prompt_path is not None
        assert result.prompt_path.exists()
        assert "PROMPT.txt" in result.prompt_path.name

    def test_no_image_in_response(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_genai_text_only_response,
    ):
        """If API returns text-only response, result.success is False with NO_IMAGE_IN_RESPONSE."""
        from scripts.generate_infographic import generate_infographic

        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_genai_text_only_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is False
        assert result.error_code == "NO_IMAGE_IN_RESPONSE"

    def test_preflight_failure_stops_generation(
        self,
        tmp_path,
        sample_data,
        sample_template,
    ):
        """When preflight fails, generate_infographic returns failure and never calls genai.Client."""
        from scripts.generate_infographic import generate_infographic
        from scripts.preflight import PreflightResult

        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_preflight_result = PreflightResult(
            success=False, error_code="INVALID_API_KEY"
        )

        with (
            patch("scripts.generate_infographic.run_preflight", return_value=mock_preflight_result),
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=False,
                config_dir=config_dir,
            )

        assert result.success is False
        assert result.error_code == "INVALID_API_KEY"
        mock_genai.Client.assert_not_called()


class TestAspectRatios:
    """Tests for ASPECT_RATIOS mapping: correct ratio per infographic type."""

    def test_scorecard_4_3(self):
        """domain-scorecard maps to 4:3 aspect ratio."""
        from scripts.generate_infographic import ASPECT_RATIOS

        assert ASPECT_RATIOS["domain-scorecard"] == "4:3"

    def test_matrix_4_3(self):
        """risk-opportunity-matrix maps to 4:3 aspect ratio."""
        from scripts.generate_infographic import ASPECT_RATIOS

        assert ASPECT_RATIOS["risk-opportunity-matrix"] == "4:3"

    def test_routing_16_9(self):
        """routing-diagram maps to 16:9 aspect ratio."""
        from scripts.generate_infographic import ASPECT_RATIOS

        assert ASPECT_RATIOS["routing-diagram"] == "16:9"

    def test_all_types_covered(self):
        """All 6 infographic types are present in ASPECT_RATIOS."""
        from scripts.generate_infographic import ASPECT_RATIOS

        expected = {
            "domain-scorecard",
            "risk-opportunity-matrix",
            "routing-diagram",
            "fault-line-map",
            "mode-comparison",
            "action-plan-timeline",
        }
        assert set(ASPECT_RATIOS.keys()) == expected


class TestThinkingConfig:
    """Tests for conditional thinking_config: applied only for supported models
    AND complex infographic types (fault-line-map, mode-comparison)."""

    def test_thinking_applied_for_gemini3_complex_type(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_genai_image_response,
    ):
        """With gemini-3-pro-image-preview + fault-line-map, thinking_config is applied."""
        from scripts.generate_infographic import generate_infographic

        # Config directory with Gemini 3 model
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir()
        (config_dir / "config.md").write_text(
            "- **Gemini API Key:** test-key-abc123\n"
            "- **Image Model:** gemini-3-pro-image-preview\n"
            "- **Retry Limit:** 2\n"
        )

        template_dir = tmp_path / "templates" / "infographic-prompts"
        template_dir.mkdir(parents=True)
        (template_dir / "fault-line-map.json").write_text(
            json.dumps(sample_template, indent=2)
        )

        data_path = tmp_path / "data.json"
        data_path.write_text(json.dumps(sample_data))
        output_path = tmp_path / "output" / "infographic.png"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_genai_image_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "fault-line-map",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is True
        call_args = mock_client.models.generate_content.call_args
        config_arg = call_args.kwargs.get("config") or call_args[1].get("config")
        assert config_arg.thinking_config is not None
        # The SDK coerces "High" to a ThinkingLevel enum; check via .value
        assert config_arg.thinking_config.thinking_level.value == "HIGH"

    def test_no_thinking_for_flash_image(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_genai_image_response,
        capsys,
    ):
        """With gemini-2.5-flash-image + fault-line-map, no thinking_config; warning printed."""
        from scripts.generate_infographic import generate_infographic

        # Config directory with flash model (no thinking support)
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir()
        (config_dir / "config.md").write_text(
            "- **Gemini API Key:** test-key-abc123\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** 2\n"
        )

        template_dir = tmp_path / "templates" / "infographic-prompts"
        template_dir.mkdir(parents=True)
        (template_dir / "fault-line-map.json").write_text(
            json.dumps(sample_template, indent=2)
        )

        data_path = tmp_path / "data.json"
        data_path.write_text(json.dumps(sample_data))
        output_path = tmp_path / "output" / "infographic.png"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_genai_image_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "fault-line-map",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is True
        # Verify no thinking_config applied
        call_args = mock_client.models.generate_content.call_args
        config_arg = call_args.kwargs.get("config") or call_args[1].get("config")
        assert config_arg.thinking_config is None
        # Verify warning printed
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "thinking" in captured.out.lower()
        assert "gemini-2.5-flash-image" in captured.out

    def test_no_thinking_for_simple_type(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_genai_image_response,
    ):
        """With gemini-3-pro-image-preview + domain-scorecard, no thinking_config."""
        from scripts.generate_infographic import generate_infographic

        # Config directory with Gemini 3 model
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir()
        (config_dir / "config.md").write_text(
            "- **Gemini API Key:** test-key-abc123\n"
            "- **Image Model:** gemini-3-pro-image-preview\n"
            "- **Retry Limit:** 2\n"
        )

        template_dir = tmp_path / "templates" / "infographic-prompts"
        template_dir.mkdir(parents=True)
        (template_dir / "domain-scorecard.json").write_text(
            json.dumps(sample_template, indent=2)
        )

        data_path = tmp_path / "data.json"
        data_path.write_text(json.dumps(sample_data))
        output_path = tmp_path / "output" / "infographic.png"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_genai_image_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is True
        call_args = mock_client.models.generate_content.call_args
        config_arg = call_args.kwargs.get("config") or call_args[1].get("config")
        assert config_arg.thinking_config is None


class TestCLI:
    """Tests for the CLI wrapper (python -m scripts.generate_infographic)."""

    def test_cli_help(self):
        """CLI --help exits with code 0."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "scripts.generate_infographic", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        assert result.returncode == 0
        assert "Infographic type slug" in result.stdout or "type" in result.stdout


# ---------------------------------------------------------------------------
# Placeholder, prompt JSON, and error classification tests (Phase 3 Plan 01)
# ---------------------------------------------------------------------------


class TestPlaceholder:
    """Tests for create_placeholder_png: file creation, dimensions, parent dirs."""

    def test_creates_valid_png(self, tmp_path):
        """create_placeholder_png produces a valid PNG file."""
        from scripts.generate_infographic import create_placeholder_png

        output = tmp_path / "error.png"
        result = create_placeholder_png(output, "TEST ERROR")
        assert result == output
        assert output.exists()
        img = Image.open(output)
        assert img.format == "PNG"

    def test_default_dimensions_1920x1080(self, tmp_path):
        """create_placeholder_png defaults to 1920x1080 (16:9)."""
        from scripts.generate_infographic import create_placeholder_png

        output = tmp_path / "error.png"
        create_placeholder_png(output, "TEST ERROR")
        img = Image.open(output)
        assert img.size == (1920, 1080)

    def test_custom_dimensions(self, tmp_path):
        """create_placeholder_png accepts width/height overrides."""
        from scripts.generate_infographic import create_placeholder_png

        output = tmp_path / "error.png"
        create_placeholder_png(output, "TEST ERROR", width=1440, height=1080)
        img = Image.open(output)
        assert img.size == (1440, 1080)

    def test_creates_parent_directories(self, tmp_path):
        """create_placeholder_png creates parent dirs if they don't exist."""
        from scripts.generate_infographic import create_placeholder_png

        output = tmp_path / "nested" / "deep" / "error.png"
        create_placeholder_png(output, "TEST ERROR")
        assert output.exists()

    def test_white_background(self, tmp_path):
        """create_placeholder_png produces a white background image."""
        from scripts.generate_infographic import create_placeholder_png

        output = tmp_path / "error.png"
        create_placeholder_png(output, "TEST ERROR")
        img = Image.open(output)
        # Check a corner pixel is white
        assert img.getpixel((0, 0)) == (255, 255, 255)


class TestPromptJson:
    """Tests for save_prompt_json: file creation, JSON structure, timestamp."""

    def test_creates_json_file(self, tmp_path):
        """save_prompt_json writes a JSON file at the expected path."""
        from scripts.generate_infographic import save_prompt_json

        result = save_prompt_json("test prompt", tmp_path, "domain-scorecard")
        assert result.exists()
        assert result.name == "INFOGRAPHIC_domain-scorecard_PROMPT.json"

    def test_json_structure(self, tmp_path):
        """save_prompt_json writes JSON with type, timestamp, error_code, prompt fields."""
        import json as json_mod
        from scripts.generate_infographic import save_prompt_json

        save_prompt_json("my prompt text", tmp_path, "domain-scorecard", error_code="API_ERROR_429")
        data = json_mod.loads((tmp_path / "INFOGRAPHIC_domain-scorecard_PROMPT.json").read_text())
        assert data["type"] == "domain-scorecard"
        assert data["prompt"] == "my prompt text"
        assert data["error_code"] == "API_ERROR_429"
        assert "timestamp" in data

    def test_timestamp_iso_8601(self, tmp_path):
        """save_prompt_json timestamp is ISO 8601 UTC."""
        import json as json_mod
        from datetime import datetime, timezone
        from scripts.generate_infographic import save_prompt_json

        save_prompt_json("prompt", tmp_path, "test-type")
        data = json_mod.loads((tmp_path / "INFOGRAPHIC_test-type_PROMPT.json").read_text())
        # Should parse as a valid datetime
        ts = datetime.fromisoformat(data["timestamp"])
        assert ts.tzinfo is not None or "+00:00" in data["timestamp"] or "Z" in data["timestamp"]

    def test_error_code_none_by_default(self, tmp_path):
        """save_prompt_json defaults error_code to None."""
        import json as json_mod
        from scripts.generate_infographic import save_prompt_json

        save_prompt_json("prompt", tmp_path, "test-type")
        data = json_mod.loads((tmp_path / "INFOGRAPHIC_test-type_PROMPT.json").read_text())
        assert data["error_code"] is None


class TestErrorClassification:
    """Tests for _is_retryable_error and _is_content_block helpers."""

    def test_retryable_429(self):
        """_is_retryable_error('API_ERROR_429') returns True."""
        from scripts.generate_infographic import _is_retryable_error

        assert _is_retryable_error("API_ERROR_429") is True

    def test_retryable_503(self):
        """_is_retryable_error('API_ERROR_503') returns True."""
        from scripts.generate_infographic import _is_retryable_error

        assert _is_retryable_error("API_ERROR_503") is True

    def test_retryable_500(self):
        """_is_retryable_error('API_ERROR_500') returns True."""
        from scripts.generate_infographic import _is_retryable_error

        assert _is_retryable_error("API_ERROR_500") is True

    def test_not_retryable_400(self):
        """_is_retryable_error('API_ERROR_400') returns False."""
        from scripts.generate_infographic import _is_retryable_error

        assert _is_retryable_error("API_ERROR_400") is False

    def test_not_retryable_403(self):
        """_is_retryable_error('API_ERROR_403') returns False."""
        from scripts.generate_infographic import _is_retryable_error

        assert _is_retryable_error("API_ERROR_403") is False

    def test_not_retryable_content_block(self):
        """_is_retryable_error('CONTENT_BLOCKED_SAFETY') returns False."""
        from scripts.generate_infographic import _is_retryable_error

        assert _is_retryable_error("CONTENT_BLOCKED_SAFETY") is False

    def test_content_block_safety(self):
        """_is_content_block('CONTENT_BLOCKED_SAFETY') returns True."""
        from scripts.generate_infographic import _is_content_block

        assert _is_content_block("CONTENT_BLOCKED_SAFETY") is True

    def test_content_block_image_safety(self):
        """_is_content_block('CONTENT_BLOCKED_IMAGE_SAFETY') returns True."""
        from scripts.generate_infographic import _is_content_block

        assert _is_content_block("CONTENT_BLOCKED_IMAGE_SAFETY") is True

    def test_not_content_block_api_error(self):
        """_is_content_block('API_ERROR_429') returns False."""
        from scripts.generate_infographic import _is_content_block

        assert _is_content_block("API_ERROR_429") is False


class TestContentBlock:
    """Tests for content block detection in generate_infographic()."""

    def _setup_env(self, tmp_path, sample_data, sample_template):
        """Helper: create config dir, template dir, and data file."""
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir()
        (config_dir / "config.md").write_text(
            "- **Gemini API Key:** test-key-abc123\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** 2\n"
        )

        template_dir = tmp_path / "templates" / "infographic-prompts"
        template_dir.mkdir(parents=True)
        (template_dir / "domain-scorecard.json").write_text(
            json.dumps(sample_template, indent=2)
        )

        data_path = tmp_path / "data.json"
        data_path.write_text(json.dumps(sample_data))
        output_path = tmp_path / "output" / "infographic.png"

        return data_path, output_path, config_dir, template_dir

    def test_prompt_level_content_block(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_content_blocked_response,
    ):
        """generate_infographic detects prompt-level content block (block_reason=SAFETY)."""
        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_content_blocked_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is False
        assert result.error_code == "CONTENT_BLOCKED_SAFETY"

    def test_candidate_level_content_block(
        self,
        tmp_path,
        sample_data,
        sample_template,
        mock_candidate_blocked_response,
    ):
        """generate_infographic detects candidate-level content block (finish_reason=IMAGE_SAFETY)."""
        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_candidate_blocked_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is False
        assert result.error_code == "CONTENT_BLOCKED_IMAGE_SAFETY"

    def test_server_error_caught(
        self,
        tmp_path,
        sample_data,
        sample_template,
    ):
        """generate_infographic catches ServerError (5xx) and returns API_ERROR_{code}."""
        from google.genai.errors import ServerError

        data_path, output_path, config_dir, template_dir = self._setup_env(
            tmp_path, sample_data, sample_template
        )

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = ServerError(
            code=503, response_json={"error": {"message": "Service Unavailable"}}
        )

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is False
        assert result.error_code == "API_ERROR_503"


# ---------------------------------------------------------------------------
# Retry, backoff, and generate_with_retry tests (Phase 3 Plan 02)
# ---------------------------------------------------------------------------


class TestBackoff:
    """Tests for _backoff: exponential delay with jitter."""

    def test_attempt_0_base_delay(self):
        """_backoff(0) uses base delay of ~2s (2.0 + up to 50% jitter)."""
        from scripts.generate_infographic import _backoff

        with (
            patch("scripts.generate_infographic.time.sleep") as mock_sleep,
            patch("scripts.generate_infographic.random.uniform", return_value=0.5),
        ):
            actual = _backoff(0)

        # base=2.0, delay=min(2*2^0,30)=2.0, jitter=uniform(0,1.0)=0.5, total=2.5
        assert actual == pytest.approx(2.5)
        mock_sleep.assert_called_once_with(2.5)

    def test_attempt_1_doubled_delay(self):
        """_backoff(1) doubles the base delay: ~4s + jitter."""
        from scripts.generate_infographic import _backoff

        with (
            patch("scripts.generate_infographic.time.sleep") as mock_sleep,
            patch("scripts.generate_infographic.random.uniform", return_value=1.0),
        ):
            actual = _backoff(1)

        # delay=min(2*2^1,30)=4.0, jitter=uniform(0,2.0)=1.0, total=5.0
        assert actual == pytest.approx(5.0)
        mock_sleep.assert_called_once_with(5.0)

    def test_attempt_2_quadrupled_delay(self):
        """_backoff(2) quadruples the base delay: ~8s + jitter."""
        from scripts.generate_infographic import _backoff

        with (
            patch("scripts.generate_infographic.time.sleep") as mock_sleep,
            patch("scripts.generate_infographic.random.uniform", return_value=2.0),
        ):
            actual = _backoff(2)

        # delay=min(2*2^2,30)=8.0, jitter=uniform(0,4.0)=2.0, total=10.0
        assert actual == pytest.approx(10.0)
        mock_sleep.assert_called_once_with(10.0)

    def test_capped_at_max_delay(self):
        """_backoff with high attempt is capped at max_delay (30s)."""
        from scripts.generate_infographic import _backoff

        with (
            patch("scripts.generate_infographic.time.sleep") as mock_sleep,
            patch("scripts.generate_infographic.random.uniform", return_value=5.0),
        ):
            actual = _backoff(10)  # 2 * 2^10 = 2048, capped to 30

        # delay=30.0, jitter=uniform(0,15.0)=5.0, total=35.0
        assert actual == pytest.approx(35.0)
        mock_sleep.assert_called_once_with(35.0)

    def test_returns_actual_delay(self):
        """_backoff returns the actual delay slept (including jitter)."""
        from scripts.generate_infographic import _backoff

        with (
            patch("scripts.generate_infographic.time.sleep"),
            patch("scripts.generate_infographic.random.uniform", return_value=0.0),
        ):
            result = _backoff(0)

        assert result == pytest.approx(2.0)


class TestRetry:
    """Tests for generate_with_retry: transient errors retry with backoff."""

    def test_succeeds_after_two_failures(self, tmp_path):
        """generate_with_retry retries 429 errors and succeeds on 3rd attempt."""
        from scripts.generate_infographic import generate_with_retry

        call_count = 0

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return GenerationResult(
                    success=False,
                    error_code="API_ERROR_429",
                    prompt_path=tmp_path / "prompt.txt",
                )
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff") as mock_backoff,
            patch("scripts.generate_infographic.validate_infographic") as mock_validate,
        ):
            mock_validate.return_value = MagicMock(passed=True, warning_only=False)
            result = generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert result.success is True
        assert call_count == 3
        assert mock_backoff.call_count == 2

    def test_backoff_called_with_attempt_index(self, tmp_path):
        """_backoff is called with the correct attempt index on each retry."""
        from scripts.generate_infographic import generate_with_retry

        call_count = 0

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return GenerationResult(
                    success=False,
                    error_code="API_ERROR_503",
                    prompt_path=tmp_path / "prompt.txt",
                )
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff") as mock_backoff,
            patch("scripts.generate_infographic.validate_infographic") as mock_validate,
        ):
            mock_validate.return_value = MagicMock(passed=True, warning_only=False)
            generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert mock_backoff.call_args_list == [call(0), call(1)]


class TestRetryBudgetExhausted:
    """Tests for generate_with_retry when all attempts are used up."""

    def test_placeholder_created_on_budget_exhaustion(self, tmp_path):
        """When all retry attempts fail, placeholder PNG is created."""
        from scripts.generate_infographic import generate_with_retry

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            return GenerationResult(
                success=False,
                error_code="API_ERROR_429",
                prompt_path=tmp_path / "prompt.txt",
            )

        output_path = tmp_path / "output.png"

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff"),
            patch("scripts.generate_infographic.create_placeholder_png") as mock_placeholder,
            patch("scripts.generate_infographic.save_prompt_json") as mock_save_json,
        ):
            result = generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                output_path,
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert result.success is False
        mock_placeholder.assert_called_once()
        # Check placeholder text contains the type name
        placeholder_args = mock_placeholder.call_args
        assert "domain-scorecard" in placeholder_args[0][1].lower() or "Generation Failed" in placeholder_args[0][1]

    def test_prompt_json_saved_on_budget_exhaustion(self, tmp_path):
        """When all retry attempts fail, PROMPT.json is saved."""
        from scripts.generate_infographic import generate_with_retry

        prompt_path = tmp_path / "prompt.txt"
        prompt_path.write_text("test prompt")

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            return GenerationResult(
                success=False,
                error_code="API_ERROR_429",
                prompt_path=prompt_path,
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff"),
            patch("scripts.generate_infographic.create_placeholder_png"),
            patch("scripts.generate_infographic.save_prompt_json") as mock_save_json,
        ):
            generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        mock_save_json.assert_called_once()


class TestContentBlockNoRetry:
    """Tests for generate_with_retry: content blocks do NOT retry."""

    def test_no_retry_on_content_block(self, tmp_path):
        """Content block returns immediately -- generate_infographic called exactly once."""
        from scripts.generate_infographic import generate_with_retry

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            return GenerationResult(
                success=False,
                error_code="CONTENT_BLOCKED_SAFETY",
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate) as mock_gen,
            patch("scripts.generate_infographic._backoff") as mock_backoff,
            patch("scripts.generate_infographic.create_placeholder_png") as mock_placeholder,
            patch("scripts.generate_infographic.save_prompt_json"),
        ):
            result = generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert result.success is False
        assert mock_gen.call_count == 1
        mock_backoff.assert_not_called()

    def test_placeholder_has_blocked_text(self, tmp_path):
        """Content block placeholder includes 'BLOCKED: content policy' text."""
        from scripts.generate_infographic import generate_with_retry

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            return GenerationResult(
                success=False,
                error_code="CONTENT_BLOCKED_SAFETY",
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic.create_placeholder_png") as mock_placeholder,
            patch("scripts.generate_infographic.save_prompt_json"),
        ):
            generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        mock_placeholder.assert_called_once()
        error_text = mock_placeholder.call_args[0][1]
        assert "BLOCKED" in error_text
        assert "content policy" in error_text


class TestRetryWithFeedback:
    """Tests for generate_with_retry: validation failure triggers corrective feedback."""

    def test_corrective_feedback_passed_to_generate(self, tmp_path):
        """On validation failure, 2nd call to generate_infographic gets corrective feedback."""
        from scripts.generate_infographic import generate_with_retry

        output_path = tmp_path / "output.png"
        call_kwargs = []

        def mock_generate(infographic_type, data_path, out_path, **kwargs):
            call_kwargs.append(kwargs)
            return GenerationResult(
                success=True,
                output_path=out_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        validate_count = 0

        def mock_validate(image_path, data_path, config_dir):
            nonlocal validate_count
            validate_count += 1
            if validate_count == 1:
                return MagicMock(
                    passed=False,
                    warning_only=False,
                    feedback="Ensure Revenue label appears clearly",
                )
            return MagicMock(passed=True, warning_only=False)

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic.validate_infographic", side_effect=mock_validate),
        ):
            result = generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                output_path,
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert result.success is True
        # First call has no feedback
        assert call_kwargs[0].get("style_override_extra") is None
        # Second call has the corrective feedback
        assert "Revenue label" in call_kwargs[1].get("style_override_extra", "")

    def test_warning_only_does_not_retry(self, tmp_path):
        """Validation with warning_only=True does NOT trigger retry."""
        from scripts.generate_infographic import generate_with_retry

        output_path = tmp_path / "output.png"

        def mock_generate(infographic_type, data_path, out_path, **kwargs):
            return GenerationResult(
                success=True,
                output_path=out_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        def mock_validate(image_path, data_path, config_dir):
            return MagicMock(passed=True, warning_only=True)

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate) as mock_gen,
            patch("scripts.generate_infographic.validate_infographic", side_effect=mock_validate),
        ):
            result = generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                output_path,
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert result.success is True
        # Only called once -- no retry for warning_only
        assert mock_gen.call_count == 1


class TestSDKRetryDisabled:
    """Tests for SDK retry being disabled via HttpRetryOptions(attempts=1)."""

    def test_client_created_with_retry_disabled(
        self,
        tmp_path,
        sample_data,
        sample_template,
    ):
        """generate_infographic creates genai.Client with HttpRetryOptions(attempts=1)."""
        from scripts.generate_infographic import generate_infographic

        # Config directory
        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir()
        (config_dir / "config.md").write_text(
            "- **Gemini API Key:** test-key-abc123\n"
            "- **Image Model:** gemini-2.5-flash-image\n"
            "- **Retry Limit:** 2\n"
        )

        template_dir = tmp_path / "templates" / "infographic-prompts"
        template_dir.mkdir(parents=True)
        (template_dir / "domain-scorecard.json").write_text(
            json.dumps(sample_template, indent=2)
        )

        data_path = tmp_path / "data.json"
        data_path.write_text(json.dumps(sample_data))
        output_path = tmp_path / "output" / "infographic.png"

        mock_client = MagicMock()
        mock_image_response = MagicMock()
        img = Image.new("RGB", (1, 1), color=(255, 255, 255))
        part = MagicMock()
        part.inline_data = True
        part.as_image.return_value = img
        mock_image_response.parts = [part]
        mock_image_response.prompt_feedback = MagicMock()
        mock_image_response.prompt_feedback.block_reason = None
        mock_image_response.candidates = []
        mock_client.models.generate_content.return_value = mock_image_response

        with (
            patch("scripts.generate_infographic.genai") as mock_genai,
            patch("scripts.generate_infographic.TEMPLATE_DIR", template_dir),
        ):
            mock_genai.Client.return_value = mock_client
            result = generate_infographic(
                "domain-scorecard",
                data_path,
                output_path,
                skip_preflight=True,
                config_dir=config_dir,
            )

        assert result.success is True
        # Verify Client was called with http_options containing retry_options
        client_call = mock_genai.Client.call_args
        http_options = client_call.kwargs.get("http_options")
        assert http_options is not None
        assert http_options.retry_options.attempts == 1


class TestPlaceholderDimensions:
    """Tests for type-specific placeholder dimensions in generate_with_retry."""

    def test_4_3_type_gets_1440x1080(self, tmp_path):
        """domain-scorecard (4:3) placeholder uses 1440x1080."""
        from scripts.generate_infographic import generate_with_retry

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            return GenerationResult(
                success=False,
                error_code="API_ERROR_429",
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff"),
            patch("scripts.generate_infographic.create_placeholder_png") as mock_placeholder,
            patch("scripts.generate_infographic.save_prompt_json"),
        ):
            generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=0,
                config_dir=tmp_path,
            )

        mock_placeholder.assert_called_once()
        kwargs = mock_placeholder.call_args[1] if mock_placeholder.call_args[1] else {}
        args = mock_placeholder.call_args[0]
        # Check width=1440, height=1080 (passed as kwargs or positional)
        if "width" in kwargs:
            assert kwargs["width"] == 1440
            assert kwargs["height"] == 1080
        else:
            assert args[2] == 1440
            assert args[3] == 1080

    def test_16_9_type_gets_1920x1080(self, tmp_path):
        """routing-diagram (16:9) placeholder uses 1920x1080."""
        from scripts.generate_infographic import generate_with_retry

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            return GenerationResult(
                success=False,
                error_code="API_ERROR_429",
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff"),
            patch("scripts.generate_infographic.create_placeholder_png") as mock_placeholder,
            patch("scripts.generate_infographic.save_prompt_json"),
        ):
            generate_with_retry(
                "routing-diagram",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=0,
                config_dir=tmp_path,
            )

        mock_placeholder.assert_called_once()
        kwargs = mock_placeholder.call_args[1] if mock_placeholder.call_args[1] else {}
        args = mock_placeholder.call_args[0]
        if "width" in kwargs:
            assert kwargs["width"] == 1920
            assert kwargs["height"] == 1080
        else:
            assert args[2] == 1920
            assert args[3] == 1080


class TestGenerateWithRetryHadRateLimit:
    """Tests for had_rate_limit field on GenerationResult."""

    def test_had_rate_limit_true_on_429(self, tmp_path):
        """GenerationResult.had_rate_limit is True when a 429 was encountered during retry."""
        from scripts.generate_infographic import generate_with_retry

        call_count = 0

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return GenerationResult(
                    success=False,
                    error_code="API_ERROR_429",
                    prompt_path=tmp_path / "prompt.txt",
                )
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff"),
            patch("scripts.generate_infographic.validate_infographic") as mock_validate,
        ):
            mock_validate.return_value = MagicMock(passed=True, warning_only=False)
            result = generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert result.success is True
        assert result.had_rate_limit is True

    def test_had_rate_limit_false_when_no_429(self, tmp_path):
        """GenerationResult.had_rate_limit is False when no 429 was encountered."""
        from scripts.generate_infographic import generate_with_retry

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic.validate_infographic") as mock_validate,
        ):
            mock_validate.return_value = MagicMock(passed=True, warning_only=False)
            result = generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        assert result.success is True
        assert result.had_rate_limit is False


class TestSkipPreflightOnRetry:
    """Tests that preflight only runs on first attempt."""

    def test_skip_preflight_true_for_retries(self, tmp_path):
        """Retry attempts pass skip_preflight=True to generate_infographic."""
        from scripts.generate_infographic import generate_with_retry

        call_kwargs = []

        def mock_generate(infographic_type, data_path, output_path, **kwargs):
            call_kwargs.append(kwargs)
            if len(call_kwargs) == 1:
                return GenerationResult(
                    success=False,
                    error_code="API_ERROR_429",
                    prompt_path=tmp_path / "prompt.txt",
                )
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.generate_infographic.generate_infographic", side_effect=mock_generate),
            patch("scripts.generate_infographic._backoff"),
            patch("scripts.generate_infographic.validate_infographic") as mock_validate,
        ):
            mock_validate.return_value = MagicMock(passed=True, warning_only=False)
            generate_with_retry(
                "domain-scorecard",
                tmp_path / "data.json",
                tmp_path / "output.png",
                retry_limit=2,
                config_dir=tmp_path,
            )

        # First call: skip_preflight=False (attempt 0)
        assert call_kwargs[0].get("skip_preflight") is False
        # Second call: skip_preflight=True (retry)
        assert call_kwargs[1].get("skip_preflight") is True


# ---------------------------------------------------------------------------
# Live integration tests (Plan 03) -- require real Gemini API key
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLiveGeneration:
    """Live end-to-end tests that call the real Gemini API.

    Requires a configured .cdp-context/config.md with a valid API key.
    Run with: python -m pytest tests/test_generate_infographic.py -m live -x -v -s
    Skip in CI by default (not collected unless -m live is specified).
    """

    def test_live_domain_scorecard(self, tmp_path):
        """Generate a real Domain Scorecard via Gemini API and check dimensions."""
        data_path = Path("tests/fixtures/sample-domain-scorecard-data.json")
        output_path = tmp_path / "images" / "INFOGRAPHIC_domain-scorecard.png"

        result = generate_infographic(
            infographic_type="domain-scorecard",
            data_path=data_path,
            output_path=output_path,
            skip_preflight=False,
        )

        assert result.success, f"Generation failed: {result.error_code}"
        assert result.output_path.exists(), "PNG not saved"
        assert result.prompt_path.exists(), "Prompt not saved"

        # Check dimensions: at least 2000px on longest edge
        img = Image.open(result.output_path)
        longest_edge = max(img.size)
        assert longest_edge >= 2000, f"Longest edge {longest_edge}px < 2000px"

        # Check aspect ratio is 4:3 (within tolerance)
        width, height = img.size
        ratio = width / height
        assert 1.2 <= ratio <= 1.4, f"Aspect ratio {ratio:.2f} not close to 4:3 (1.33)"
