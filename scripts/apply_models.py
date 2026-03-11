"""Apply agent model configuration from .cdp-context/config.md.

Reads tier defaults and per-agent overrides from the Agent Models section
of the CDP configuration file, then updates the `model:` field in YAML
frontmatter of agent definitions in `.claude/agents/`.

Exports:
    ModelConfig    -- Parsed model configuration (tier defaults + overrides)
    ApplyResult    -- Summary of changes applied
    load_model_config  -- Parse config.md for model settings
    classify_agent     -- Determine tier from agent file path
    resolve_model      -- Look up effective model for an agent
    apply_models       -- Walk agent files and rewrite model fields

CLI usage:
    python3 -m scripts.apply_models [--config-dir DIR] [--agents-dir DIR]
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Support both `python3 -m scripts.apply_models` (from repo root)
# and direct invocation when installed as a skill
try:
    from scripts.config import FIELD_PATTERN, _extract_value
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts.config import FIELD_PATTERN, _extract_value

# Valid model shortnames
VALID_MODELS = {"opus", "sonnet", "haiku"}

# Built-in tier defaults (used when config has no Agent Models section)
BUILTIN_DEFAULTS = {
    "ceo": "opus",
    "c-suite": "sonnet",
    "team leads": "haiku",
}

# Matches YAML frontmatter model line
MODEL_LINE_RE = re.compile(r"^(model:\s*)(.+)$", re.MULTILINE)


@dataclass
class ModelConfig:
    """Parsed model configuration."""

    tier_defaults: dict[str, str] = field(default_factory=dict)
    overrides: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ApplyResult:
    """Summary of model application run."""

    changed: int = 0
    unchanged: int = 0
    warnings: list[str] = field(default_factory=list)
    tier_defaults: dict[str, str] = field(default_factory=dict)
    overrides: dict[str, str] = field(default_factory=dict)


def load_model_config(config_path: Path) -> ModelConfig:
    """Parse tier defaults and per-agent overrides from config.md.

    Reads only the ``## Agent Models`` section. Within that section:
    - ``### Tier Defaults`` fields set tier-level models
    - ``### Per-Agent Overrides`` fields set individual agent models

    Returns ModelConfig with warnings for invalid model names.
    If config_path doesn't exist or has no Agent Models section,
    returns empty ModelConfig (built-in defaults will apply).
    """
    config = ModelConfig()

    if not config_path.exists():
        return config

    text = config_path.read_text()

    # Find the ## Agent Models section
    agent_models_match = re.search(
        r"^## Agent Models\s*$", text, re.MULTILINE
    )
    if not agent_models_match:
        return config

    # Extract text from ## Agent Models to the next ## heading or end of file
    section_start = agent_models_match.end()
    next_h2 = re.search(r"^## ", text[section_start:], re.MULTILINE)
    section_text = text[section_start : section_start + next_h2.start()] if next_h2 else text[section_start:]

    # Split into subsections by ### headings
    subsections: dict[str, str] = {}
    parts = re.split(r"^(### .+)$", section_text, flags=re.MULTILINE)
    current_heading = None
    for part in parts:
        if part.startswith("### "):
            current_heading = part.strip().lower()
        elif current_heading is not None:
            subsections[current_heading] = part

    # Parse Tier Defaults
    tier_text = subsections.get("### tier defaults", "")
    for match in FIELD_PATTERN.finditer(tier_text):
        tier_name = match.group(1).strip().lower()
        raw_value = _extract_value(match.group(2))
        if not raw_value:
            continue
        model = raw_value.strip().lower()
        if model not in VALID_MODELS:
            config.warnings.append(
                f"Invalid model '{raw_value}' for tier '{tier_name}', skipping"
            )
            continue
        config.tier_defaults[tier_name] = model

    # Parse Per-Agent Overrides
    override_text = subsections.get("### per-agent overrides", "")
    for match in FIELD_PATTERN.finditer(override_text):
        agent_name = match.group(1).strip().lower()
        raw_value = _extract_value(match.group(2))
        if not raw_value:
            continue
        model = raw_value.strip().lower()
        if model not in VALID_MODELS:
            config.warnings.append(
                f"Invalid model '{raw_value}' for agent '{agent_name}', skipping"
            )
            continue
        config.overrides[agent_name] = model

    return config


def classify_agent(rel_path: Path) -> str:
    """Determine tier from an agent's path relative to the agents directory.

    Classification rules:
    - ``ceo.md`` (top-level) → "ceo"
    - ``c-suite/*.md`` → "c-suite"
    - ``team-leads/**/*.md`` → "team leads"

    Returns the tier string matching config field names.
    """
    parts = rel_path.parts

    if len(parts) == 1:
        # Top-level file: ceo.md
        return "ceo"
    elif parts[0] == "c-suite":
        return "c-suite"
    elif parts[0] == "team-leads":
        return "team leads"

    # Fallback for unexpected structure
    return "team leads"


def resolve_model(agent_name: str, tier: str, config: ModelConfig) -> str:
    """Look up effective model for an agent.

    Resolution order:
    1. Per-agent override from config
    2. Tier default from config
    3. Built-in default for the tier
    """
    # 1. Per-agent override
    if agent_name in config.overrides:
        return config.overrides[agent_name]

    # 2. Tier default from config
    if tier in config.tier_defaults:
        return config.tier_defaults[tier]

    # 3. Built-in default
    return BUILTIN_DEFAULTS.get(tier, "haiku")


def apply_models(agents_dir: Path, config: ModelConfig) -> ApplyResult:
    """Walk agent files in agents_dir and update model: frontmatter.

    Only rewrites files where the model value differs from the resolved
    model. Preserves all other file content.

    Args:
        agents_dir: Path to .claude/agents/ directory.
        config: Parsed model configuration.

    Returns:
        ApplyResult with counts of changed/unchanged files and any warnings.
    """
    result = ApplyResult(
        tier_defaults={
            k: config.tier_defaults.get(k, BUILTIN_DEFAULTS[k])
            for k in BUILTIN_DEFAULTS
        },
        overrides=dict(config.overrides),
    )
    result.warnings.extend(config.warnings)

    if not agents_dir.is_dir():
        result.warnings.append(
            f"Agents directory not found: {agents_dir}. "
            "Run install.py first to populate .claude/agents/."
        )
        return result

    # Collect all known agent filenames for override validation
    known_agents: set[str] = set()
    agent_files: list[tuple[Path, Path]] = []  # (full_path, rel_path)

    for md_file in sorted(agents_dir.rglob("*.md")):
        rel = md_file.relative_to(agents_dir)
        agent_name = md_file.stem
        known_agents.add(agent_name)
        agent_files.append((md_file, rel))

    # Warn about unrecognized agent names in overrides
    for override_name in config.overrides:
        if override_name not in known_agents:
            result.warnings.append(
                f"Override agent '{override_name}' not found in {agents_dir}"
            )

    # Process each agent file
    for md_file, rel in agent_files:
        content = md_file.read_text()
        agent_name = md_file.stem
        tier = classify_agent(rel)
        target_model = resolve_model(agent_name, tier, config)

        # Find and potentially update the model: line in frontmatter
        model_match = MODEL_LINE_RE.search(content)
        if not model_match:
            # No model line in frontmatter — skip
            result.unchanged += 1
            continue

        current_model = model_match.group(2).strip()
        if current_model == target_model:
            result.unchanged += 1
            continue

        # Rewrite only the model value
        new_content = MODEL_LINE_RE.sub(
            rf"\g<1>{target_model}", content, count=1
        )
        md_file.write_text(new_content)
        result.changed += 1

    return result


def _detect_project_root() -> Path:
    """Detect project root from script location.

    When installed as a skill, the script lives at:
        <project>/.claude/skills/corporate-decision-panel/scripts/apply_models.py
    So project root is 4 levels up. Falls back to CWD.
    """
    script_dir = Path(__file__).resolve().parent  # scripts/
    skill_dir = script_dir.parent  # corporate-decision-panel/
    claude_dir = skill_dir.parent.parent  # .claude/ (if skills/ is parent)
    if claude_dir.name == ".claude":
        project_root = claude_dir.parent
        if (project_root / ".cdp-context").is_dir() or (claude_dir / "agents").is_dir():
            return project_root
    return Path.cwd()


def main() -> None:
    """CLI entry point."""
    import argparse

    project_root = _detect_project_root()

    parser = argparse.ArgumentParser(
        description="Apply agent model configuration from config.md"
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=project_root / ".cdp-context",
        help="Directory containing config.md (default: .cdp-context)",
    )
    parser.add_argument(
        "--agents-dir",
        type=Path,
        default=project_root / ".claude" / "agents",
        help="Directory containing agent definitions (default: .claude/agents)",
    )
    args = parser.parse_args()

    config_path = args.config_dir / "config.md"
    config = load_model_config(config_path)
    result = apply_models(args.agents_dir, config)

    # Print warnings
    for warning in result.warnings:
        print(f"  WARNING: {warning}", file=sys.stderr)

    # Print structured output
    tier_summary = " | ".join(
        f"{k.title()}: {v}" for k, v in result.tier_defaults.items()
    )
    print("MODELS OK")
    print(f"  {tier_summary}")
    if result.overrides:
        override_str = ", ".join(
            f"{k}={v}" for k, v in result.overrides.items()
        )
        print(f"  Overrides: {override_str}")
    print(f"  Changed: {result.changed} | Unchanged: {result.unchanged}")

    # Exit non-zero only on fatal errors (missing agents dir)
    if not args.agents_dir.is_dir():
        sys.exit(1)


if __name__ == "__main__":
    main()
