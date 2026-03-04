"""Tests for prompt serialization pipeline.

Covers: load_template, substitute_placeholders, serialize_template, save_prompt.
"""

from pathlib import Path

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
