"""Prompt serialization pipeline for CDP infographic generation.

Loads JSON prompt templates, substitutes data placeholders, and
serializes to natural language prompts suitable for Gemini image
generation.  Also provides prompt saving for debugging/iteration.

Exports:
    load_template            -- Load JSON template by infographic type slug
    substitute_placeholders  -- Replace {{TOKEN}} patterns with data values
    serialize_template       -- Flatten template + data to natural language prompt
    save_prompt              -- Write assembled prompt to disk
    PLACEHOLDER_RE           -- Compiled regex for {{PLACEHOLDER}} tokens
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.config import ConfigError

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TEMPLATE_DIR = Path("templates/infographic-prompts")

PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")


# ---------------------------------------------------------------------------
# Template loading
# ---------------------------------------------------------------------------


def load_template(
    infographic_type: str,
    *,
    template_dir: Path | None = None,
) -> dict:
    """Load a JSON prompt template by infographic type slug.

    The type slug is normalized: lowercased, underscores replaced with
    hyphens, whitespace stripped.

    Args:
        infographic_type: Type slug, e.g. "domain-scorecard" or "domain_scorecard".
        template_dir: Override template directory (used in testing).

    Returns:
        Parsed template dict.

    Raises:
        ConfigError: If the template file does not exist (TEMPLATE_NOT_FOUND).
    """
    base = template_dir if template_dir is not None else TEMPLATE_DIR
    slug = infographic_type.lower().replace("_", "-").strip()
    path = base / f"{slug}.json"

    if not path.exists():
        available = sorted(t.stem for t in base.glob("*.json"))
        raise ConfigError(
            error_code="TEMPLATE_NOT_FOUND",
            message=f"No template found for type '{infographic_type}'",
            remediation=f"Available types: {', '.join(available)}" if available else "No templates found in directory.",
        )

    return json.loads(path.read_text())


# ---------------------------------------------------------------------------
# Placeholder substitution
# ---------------------------------------------------------------------------


def substitute_placeholders(text: str, data: dict) -> str:
    """Replace ``{{TOKEN}}`` patterns with values from *data*.

    Tokens present in *data* are replaced with the corresponding value
    (converted to str).  Tokens absent from *data* are replaced with
    ``[TOKEN]`` to make missing data visible without breaking the prompt.

    Args:
        text: Input string potentially containing ``{{TOKEN}}`` patterns.
        data: Mapping of token names to replacement values.

    Returns:
        String with all ``{{TOKEN}}`` patterns resolved.
    """

    def _replacer(match: re.Match) -> str:
        key = match.group(1)
        return str(data.get(key, f"[{key}]"))

    return PLACEHOLDER_RE.sub(_replacer, text)


# ---------------------------------------------------------------------------
# Template serialization
# ---------------------------------------------------------------------------


def serialize_template(
    template: dict,
    data: dict,
    style_override: str | None = None,
) -> str:
    """Flatten a JSON template + data dict into a natural language prompt.

    Produces descriptive paragraphs (not keyword lists) suitable for
    Gemini image generation.  Hex color codes from ``extras.color_mapping``
    are included for brand consistency.

    Structure of the generated prompt:
        1. Subject line (from core.subject)
        2. Data elements (objects with placeholders substituted)
        3. Context notes (notes with placeholders substituted)
        4. Constraints
        5. Style guidance (primary_style, render_quality)
        6. Color coding (hex codes from extras.color_mapping)
        7. Supplementary data (extras.data with placeholders substituted)
        8. Quality cues (quality_keywords.include)
        9. Optional style override appendix

    Args:
        template: Parsed JSON template dict.
        data: Mapping of placeholder tokens to concrete values.
        style_override: Optional extra style guidance to append.

    Returns:
        Multi-paragraph natural language prompt string.
    """
    sections: list[str] = []

    # --- 1. Subject ---
    core = template.get("core", {})
    subject = core.get("subject", "infographic")
    sections.append(f"Create a {subject}.")

    # --- 2. Objects (data elements) ---
    objects = core.get("objects", [])
    if objects:
        populated = [substitute_placeholders(obj, data) for obj in objects]
        section = "Include the following data elements: " + "; ".join(populated) + "."
        sections.append(section)

    # --- 3. Notes ---
    notes = core.get("notes", [])
    if notes:
        populated = [substitute_placeholders(note, data) for note in notes]
        section = "Context: " + "; ".join(populated) + "."
        sections.append(section)

    # --- 4. Constraints ---
    constraints = core.get("constraints", [])
    if constraints:
        section = "Constraints: " + "; ".join(constraints) + "."
        sections.append(section)

    # --- 5. Style ---
    style = template.get("style", {})
    primary_style = style.get("primary_style", "")
    render_quality = style.get("render_quality", "")
    if primary_style or render_quality:
        parts = [p for p in [primary_style, render_quality] if p]
        section = "Style: " + ", ".join(parts) + "."
        sections.append(section)

    # --- 6. Color mapping ---
    extras = template.get("extras", {})
    color_mapping = extras.get("color_mapping", {})
    if color_mapping:
        color_lines = [
            f"Use {hex_val} for {name.replace('_', ' ')}"
            for name, hex_val in color_mapping.items()
        ]
        section = "Color coding: " + ", ".join(color_lines) + "."
        sections.append(section)

    # --- 7. Extras data ---
    extras_data = extras.get("data", {})
    if extras_data:
        populated = [
            substitute_placeholders(value, data)
            for value in extras_data.values()
        ]
        section = "Supplementary data: " + "; ".join(populated) + "."
        sections.append(section)

    # --- 8. Quality keywords ---
    quality = template.get("quality_keywords", {})
    include_kw = quality.get("include", [])
    if include_kw:
        section = "Quality: " + ", ".join(include_kw) + "."
        sections.append(section)

    # --- 9. Style override ---
    if style_override:
        sections.append(f"Additional style guidance: {style_override}")

    return "\n\n".join(sections)


# ---------------------------------------------------------------------------
# Prompt saving
# ---------------------------------------------------------------------------


def save_prompt(prompt: str, output_dir: Path, type_slug: str) -> Path:
    """Write the assembled prompt to disk for debugging and iteration.

    Creates the output directory if it does not exist.

    Args:
        prompt: The assembled natural language prompt text.
        output_dir: Directory to write the prompt file into.
        type_slug: Infographic type slug (e.g. "domain-scorecard").

    Returns:
        Path to the written prompt file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"INFOGRAPHIC_{type_slug}_PROMPT.txt"
    path = output_dir / filename
    path.write_text(prompt)
    return path
