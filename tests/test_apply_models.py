"""Tests for scripts.apply_models — agent model configuration."""

from pathlib import Path

import pytest

from scripts.apply_models import (
    ApplyResult,
    ModelConfig,
    apply_models,
    classify_agent,
    load_model_config,
    resolve_model,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def make_agents(tmp_path):
    """Factory fixture: creates agent .md files with YAML frontmatter.

    Usage:
        agents_dir = make_agents({
            "ceo.md": "opus",
            "c-suite/cfo.md": "sonnet",
            "team-leads/cfo/controller.md": "haiku",
        })
    """

    def _make(agents: dict[str, str]) -> Path:
        agents_dir = tmp_path / "agents"
        for rel_path, model in agents.items():
            full_path = agents_dir / rel_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            name = Path(rel_path).stem
            full_path.write_text(
                f"---\n"
                f"name: {name}\n"
                f"description: \"Test agent\"\n"
                f"model: {model}\n"
                f"---\n"
                f"\n"
                f"# {name.title()}\n"
                f"\n"
                f"Content here.\n"
            )
        return agents_dir

    return _make


@pytest.fixture
def make_model_config(tmp_path):
    """Factory fixture: creates a config.md with Agent Models section.

    Usage:
        config_path = make_model_config(
            tier_defaults={"CEO": "opus"},
            overrides={"cfo": "opus"},
        )
    """

    def _make(
        tier_defaults: dict[str, str] | None = None,
        overrides: dict[str, str] | None = None,
        extra_content: str = "",
    ) -> Path:
        lines = [
            "# CDP Configuration\n",
            "\n",
            "## Image Generation\n",
            "\n",
            "- **Gemini API Key:** test-key\n",
            "\n",
            "## Agent Logging\n",
            "\n",
            "- **Agent Logging:** off\n",
            "\n",
        ]

        if tier_defaults is not None or overrides is not None:
            lines.append("## Agent Models\n\n")
            lines.append("### Tier Defaults\n\n")
            if tier_defaults:
                for name, model in tier_defaults.items():
                    lines.append(f"- **{name}:** {model}\n")
            lines.append("\n### Per-Agent Overrides\n\n")
            if overrides:
                for name, model in overrides.items():
                    lines.append(f"- **{name}:** {model}\n")

        if extra_content:
            lines.append(extra_content)

        config_dir = tmp_path / ".cdp-context"
        config_dir.mkdir(exist_ok=True)
        config_path = config_dir / "config.md"
        config_path.write_text("".join(lines))
        return config_path

    return _make


# ---------------------------------------------------------------------------
# TestLoadModelConfig
# ---------------------------------------------------------------------------


class TestLoadModelConfig:
    """Tests for parsing model config from config.md."""

    def test_parse_tier_defaults(self, make_model_config):
        """Tier defaults are extracted correctly."""
        path = make_model_config(
            tier_defaults={"CEO": "opus", "C-Suite": "sonnet", "Team Leads": "haiku"}
        )
        config = load_model_config(path)
        assert config.tier_defaults["ceo"] == "opus"
        assert config.tier_defaults["c-suite"] == "sonnet"
        assert config.tier_defaults["team leads"] == "haiku"

    def test_parse_overrides(self, make_model_config):
        """Per-agent overrides are extracted correctly."""
        path = make_model_config(overrides={"cfo": "opus", "vp-sales": "haiku"})
        config = load_model_config(path)
        assert config.overrides["cfo"] == "opus"
        assert config.overrides["vp-sales"] == "haiku"

    def test_missing_file_returns_empty(self, tmp_path):
        """Missing config file returns empty ModelConfig (no error)."""
        config = load_model_config(tmp_path / "nonexistent.md")
        assert config.tier_defaults == {}
        assert config.overrides == {}
        assert config.warnings == []

    def test_no_agent_models_section(self, make_model_config):
        """Config with no Agent Models section returns empty ModelConfig."""
        # Create config without tier_defaults or overrides (no section added)
        config_dir = make_model_config.__wrapped__(None, None) if hasattr(make_model_config, '__wrapped__') else None
        # Simpler approach: just pass None to skip the section
        path = make_model_config()
        config = load_model_config(path)
        assert config.tier_defaults == {}
        assert config.overrides == {}

    def test_invalid_model_warns(self, make_model_config):
        """Invalid model name generates a warning and is skipped."""
        path = make_model_config(tier_defaults={"CEO": "gpt-4"})
        config = load_model_config(path)
        assert "ceo" not in config.tier_defaults
        assert len(config.warnings) == 1
        assert "gpt-4" in config.warnings[0]

    def test_placeholder_defaults_ignored(self, make_model_config):
        """Placeholder values like '(default: opus)' are resolved correctly."""
        # Create config manually with placeholder syntax
        path = make_model_config(tier_defaults={"CEO": "(default: opus)"})
        # The FIELD_PATTERN + _extract_value should resolve "(default: opus)" → "opus"
        config = load_model_config(path)
        # "(default: opus)" is extracted to "opus" by _extract_value
        assert config.tier_defaults.get("ceo") == "opus"

    def test_empty_override_value_skipped(self, make_model_config):
        """Override with empty value is skipped."""
        path = make_model_config(overrides={"cfo": ""})
        config = load_model_config(path)
        assert "cfo" not in config.overrides

    def test_mixed_case_model_normalized(self, make_model_config):
        """Model names are normalized to lowercase."""
        path = make_model_config(tier_defaults={"CEO": "Opus"})
        config = load_model_config(path)
        assert config.tier_defaults["ceo"] == "opus"


# ---------------------------------------------------------------------------
# TestClassifyAgent
# ---------------------------------------------------------------------------


class TestClassifyAgent:
    """Tests for agent tier classification from file paths."""

    def test_ceo_top_level(self):
        assert classify_agent(Path("ceo.md")) == "ceo"

    def test_c_suite(self):
        assert classify_agent(Path("c-suite/cfo.md")) == "c-suite"
        assert classify_agent(Path("c-suite/cto.md")) == "c-suite"
        assert classify_agent(Path("c-suite/vp-sales.md")) == "c-suite"

    def test_team_leads(self):
        assert classify_agent(Path("team-leads/cfo/controller.md")) == "team leads"
        assert classify_agent(Path("team-leads/cso/market-intelligence-lead.md")) == "team leads"
        assert classify_agent(Path("team-leads/cco/writer.md")) == "team leads"


# ---------------------------------------------------------------------------
# TestResolveModel
# ---------------------------------------------------------------------------


class TestResolveModel:
    """Tests for model resolution with override precedence."""

    def test_builtin_default(self):
        """With empty config, built-in defaults apply."""
        config = ModelConfig()
        assert resolve_model("ceo", "ceo", config) == "opus"
        assert resolve_model("cfo", "c-suite", config) == "sonnet"
        assert resolve_model("controller", "team leads", config) == "haiku"

    def test_tier_default_overrides_builtin(self):
        """Tier default from config overrides built-in default."""
        config = ModelConfig(tier_defaults={"c-suite": "opus"})
        assert resolve_model("cfo", "c-suite", config) == "opus"

    def test_per_agent_overrides_tier(self):
        """Per-agent override takes precedence over tier default."""
        config = ModelConfig(
            tier_defaults={"c-suite": "sonnet"},
            overrides={"cfo": "opus"},
        )
        assert resolve_model("cfo", "c-suite", config) == "opus"

    def test_per_agent_override_leaves_others(self):
        """Per-agent override only affects the named agent."""
        config = ModelConfig(
            tier_defaults={"c-suite": "sonnet"},
            overrides={"cfo": "opus"},
        )
        # CTO still gets tier default
        assert resolve_model("cto", "c-suite", config) == "sonnet"

    def test_override_with_no_tier_default(self):
        """Override works even if no tier default is set."""
        config = ModelConfig(overrides={"controller": "sonnet"})
        assert resolve_model("controller", "team leads", config) == "sonnet"


# ---------------------------------------------------------------------------
# TestApplyModels
# ---------------------------------------------------------------------------


class TestApplyModels:
    """End-to-end tests: config + agent files → correct frontmatter rewrites."""

    def test_default_config_no_changes(self, make_agents):
        """With built-in defaults, agents already matching see no changes."""
        agents_dir = make_agents({
            "ceo.md": "opus",
            "c-suite/cfo.md": "sonnet",
            "team-leads/cfo/controller.md": "haiku",
        })
        config = ModelConfig()
        result = apply_models(agents_dir, config)
        assert result.changed == 0
        assert result.unchanged == 3

    def test_tier_default_changes_agents(self, make_agents):
        """Changing a tier default updates all agents in that tier."""
        agents_dir = make_agents({
            "c-suite/cfo.md": "sonnet",
            "c-suite/cto.md": "sonnet",
            "c-suite/coo.md": "sonnet",
        })
        config = ModelConfig(tier_defaults={"c-suite": "opus"})
        result = apply_models(agents_dir, config)
        assert result.changed == 3
        assert result.unchanged == 0

        # Verify file contents
        cfo_content = (agents_dir / "c-suite/cfo.md").read_text()
        assert "model: opus" in cfo_content

    def test_per_agent_override(self, make_agents):
        """Per-agent override changes only the named agent."""
        agents_dir = make_agents({
            "c-suite/cfo.md": "sonnet",
            "c-suite/cto.md": "sonnet",
        })
        config = ModelConfig(overrides={"cfo": "opus"})
        result = apply_models(agents_dir, config)
        assert result.changed == 1
        assert result.unchanged == 1

        cfo_content = (agents_dir / "c-suite/cfo.md").read_text()
        assert "model: opus" in cfo_content
        cto_content = (agents_dir / "c-suite/cto.md").read_text()
        assert "model: sonnet" in cto_content

    def test_idempotent(self, make_agents):
        """Running twice produces 0 changes on second run."""
        agents_dir = make_agents({
            "c-suite/cfo.md": "sonnet",
        })
        config = ModelConfig(overrides={"cfo": "opus"})

        result1 = apply_models(agents_dir, config)
        assert result1.changed == 1

        result2 = apply_models(agents_dir, config)
        assert result2.changed == 0
        assert result2.unchanged == 1

    def test_preserves_other_content(self, make_agents):
        """Only the model: line changes; all other content is preserved."""
        agents_dir = make_agents({
            "c-suite/cfo.md": "sonnet",
        })
        original = (agents_dir / "c-suite/cfo.md").read_text()
        config = ModelConfig(overrides={"cfo": "opus"})

        apply_models(agents_dir, config)

        updated = (agents_dir / "c-suite/cfo.md").read_text()
        # Only difference should be model value
        assert updated == original.replace("model: sonnet", "model: opus")

    def test_missing_agents_dir_warns(self, tmp_path):
        """Missing agents directory produces warning, not crash."""
        config = ModelConfig()
        result = apply_models(tmp_path / "nonexistent", config)
        assert len(result.warnings) == 1
        assert "not found" in result.warnings[0]

    def test_unknown_override_warns(self, make_agents):
        """Override for nonexistent agent produces warning."""
        agents_dir = make_agents({
            "c-suite/cfo.md": "sonnet",
        })
        config = ModelConfig(overrides={"nonexistent-agent": "opus"})
        result = apply_models(agents_dir, config)
        assert any("nonexistent-agent" in w for w in result.warnings)

    def test_no_model_line_skipped(self, tmp_path):
        """Agent file without model: in frontmatter is skipped."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "mystery.md").write_text(
            "---\nname: mystery\ndescription: test\n---\n\nContent.\n"
        )
        config = ModelConfig()
        result = apply_models(agents_dir, config)
        assert result.unchanged == 1
        assert result.changed == 0


class TestApplyModelsIntegration:
    """Integration test: load_model_config → apply_models pipeline."""

    def test_full_pipeline(self, make_model_config, make_agents):
        """Config file → parsed config → applied to agents."""
        config_path = make_model_config(
            tier_defaults={"C-Suite": "opus"},
            overrides={"cto": "haiku"},
        )
        agents_dir = make_agents({
            "ceo.md": "opus",
            "c-suite/cfo.md": "sonnet",
            "c-suite/cto.md": "sonnet",
            "team-leads/cfo/controller.md": "haiku",
        })

        config = load_model_config(config_path)
        result = apply_models(agents_dir, config)

        # CEO unchanged (built-in default = opus)
        assert (agents_dir / "ceo.md").read_text().count("model: opus") == 1
        # CFO changed to opus (tier default)
        assert (agents_dir / "c-suite/cfo.md").read_text().count("model: opus") == 1
        # CTO changed to haiku (per-agent override)
        assert (agents_dir / "c-suite/cto.md").read_text().count("model: haiku") == 1
        # Controller unchanged (built-in default = haiku)
        assert (agents_dir / "team-leads/cfo/controller.md").read_text().count("model: haiku") == 1

        assert result.changed == 2
        assert result.unchanged == 2
