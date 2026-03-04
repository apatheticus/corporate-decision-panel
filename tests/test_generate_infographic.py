"""Tests for infographic generation pipeline.

Covers: load_template, substitute_placeholders, serialize_template, save_prompt
(from Plan 01), plus generate_infographic, aspect ratios, thinking config,
preflight integration, and CLI wrapper (from Plan 02).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.config import ConfigError


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
