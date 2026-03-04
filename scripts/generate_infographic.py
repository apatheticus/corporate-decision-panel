"""Infographic generation pipeline for CDP.

Loads JSON prompt templates, substitutes data placeholders, serializes
to natural language prompts, calls the Gemini API with image modalities,
and saves the resulting PNG.  Also provides a CLI wrapper for standalone
invocation.

Exports:
    load_template            -- Load JSON template by infographic type slug
    substitute_placeholders  -- Replace {{TOKEN}} patterns with data values
    serialize_template       -- Flatten template + data to natural language prompt
    save_prompt              -- Write assembled prompt to disk
    generate_infographic     -- End-to-end generation: preflight, prompt, API, save
    GenerationResult         -- Dataclass with success/output_path/prompt_path/error_code
    PLACEHOLDER_RE           -- Compiled regex for {{PLACEHOLDER}} tokens
    ASPECT_RATIOS            -- Per-type aspect ratio mapping
    THINKING_TYPES           -- Set of types that benefit from thinking mode
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from scripts.config import ConfigError, load_config
from scripts.preflight import run_preflight

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TEMPLATE_DIR = Path("templates/infographic-prompts")

PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")

ASPECT_RATIOS: dict[str, str] = {
    "domain-scorecard":        "4:3",
    "risk-opportunity-matrix": "4:3",
    "routing-diagram":         "16:9",
    "fault-line-map":          "16:9",
    "mode-comparison":         "16:9",
    "action-plan-timeline":    "16:9",
}

THINKING_TYPES: set[str] = {"fault-line-map", "mode-comparison"}

# Models whose IDs start with these prefixes support thinking_level for
# image generation.  The default gemini-2.5-flash-image does NOT.
THINKING_MODEL_PREFIXES: tuple[str, ...] = ("gemini-3-", "gemini-3.")


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class GenerationResult:
    """Result of an infographic generation attempt.

    Attributes:
        success:     True if the PNG was saved successfully.
        output_path: Path to the saved PNG (None on failure).
        prompt_path: Path to the saved prompt text file (None on failure).
        error_code:  Machine-readable error identifier (None on success).
    """

    success: bool
    output_path: Path | None = None
    prompt_path: Path | None = None
    error_code: str | None = None


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


# ---------------------------------------------------------------------------
# Status output
# ---------------------------------------------------------------------------


def _status(stage: str, detail: str = "") -> None:
    """Print a structured status line parseable by the CEO agent.

    Args:
        stage: Status keyword (e.g. GENERATING, PROMPT, IMAGE, SAVED).
        detail: Optional extra information.
    """
    if detail:
        print(f"{stage} {detail}")
    else:
        print(stage)


# ---------------------------------------------------------------------------
# Config builder
# ---------------------------------------------------------------------------


def _build_config(
    infographic_type: str,
    aspect_ratio: str,
    model_id: str,
) -> types.GenerateContentConfig:
    """Build a ``GenerateContentConfig`` with conditional thinking support.

    Thinking is applied only when *infographic_type* is in
    :data:`THINKING_TYPES` **and** the *model_id* starts with a known
    thinking-capable prefix (:data:`THINKING_MODEL_PREFIXES`).

    When thinking is requested but the model does not support it, a
    warning is printed and generation proceeds without thinking.

    Args:
        infographic_type: Normalized type slug.
        aspect_ratio: Aspect ratio string (e.g. "4:3", "16:9").
        model_id: Gemini model identifier from config.

    Returns:
        Configured ``GenerateContentConfig``.
    """
    config_kwargs: dict = {
        "response_modalities": ["TEXT", "IMAGE"],
        "image_config": types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size="2K",
        ),
    }

    if infographic_type in THINKING_TYPES:
        if model_id.startswith(THINKING_MODEL_PREFIXES):
            config_kwargs["thinking_config"] = types.ThinkingConfig(
                thinking_level="High",
            )
        else:
            print(
                f"WARNING thinking requested for {infographic_type} "
                f"but model {model_id} does not support thinking mode"
            )

    return types.GenerateContentConfig(**config_kwargs)


# ---------------------------------------------------------------------------
# Generation engine
# ---------------------------------------------------------------------------


def generate_infographic(
    infographic_type: str,
    data_path: Path,
    output_path: Path,
    skip_preflight: bool = False,
    config_dir: Path = Path(".cdp-context"),
) -> GenerationResult:
    """Generate a single infographic PNG via the Gemini API.

    Steps:
        1. Normalize the type slug.
        2. Run preflight validation (unless *skip_preflight*).
        3. Load config, template, and data.
        4. Check for optional style override (``config_dir/style.md``).
        5. Serialize template + data to a natural language prompt.
        6. Save the prompt to disk.
        7. Call ``generate_content`` with image config.
        8. Extract the image from the response and save as PNG.

    Args:
        infographic_type: Type slug (e.g. "domain-scorecard").
        data_path: Path to a JSON file with placeholder data.
        output_path: Destination path for the PNG.
        skip_preflight: If True, skip pre-flight validation.
        config_dir: Directory containing ``config.md`` and optional
                    ``style.md`` (default: ``.cdp-context``).

    Returns:
        :class:`GenerationResult` with success status, paths, and
        error code (if applicable).
    """
    # --- 1. Normalize type slug ---
    type_slug = infographic_type.lower().replace("_", "-").strip()

    # --- 2. Preflight ---
    if not skip_preflight:
        preflight = run_preflight(config_dir)
        if not preflight.success:
            _status("PREFLIGHT FAILED")
            return GenerationResult(
                success=False,
                error_code=preflight.error_code,
            )

    # --- 3. Load config, template, data ---
    config = load_config(config_dir)
    template = load_template(type_slug)
    data = json.loads(data_path.read_text())

    # --- 4. Optional style override ---
    style_path = config_dir / "style.md"
    style_override: str | None = None
    if style_path.exists():
        style_override = style_path.read_text()

    # --- 5. Serialize prompt ---
    prompt = serialize_template(template, data, style_override)

    # --- 6. Save prompt ---
    prompt_path = save_prompt(prompt, output_path.parent, type_slug)

    _status("GENERATING", type_slug)
    _status("PROMPT", "assembled")

    # --- 7. API call ---
    client = genai.Client(api_key=config["api_key"])
    aspect_ratio = ASPECT_RATIOS.get(type_slug, "16:9")
    gen_config = _build_config(type_slug, aspect_ratio, config["model_id"])

    try:
        response = client.models.generate_content(
            model=config["model_id"],
            contents=prompt,
            config=gen_config,
        )
    except ClientError as e:
        return GenerationResult(
            success=False,
            error_code=f"API_ERROR_{e.code}",
            prompt_path=prompt_path,
        )

    # --- 8. Extract and save image ---
    image = None
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            break

    if image is None:
        return GenerationResult(
            success=False,
            error_code="NO_IMAGE_IN_RESPONSE",
            prompt_path=prompt_path,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(output_path))

    _status("IMAGE", "received")
    _status("SAVED", str(output_path))

    return GenerationResult(
        success=True,
        output_path=output_path,
        prompt_path=prompt_path,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for standalone infographic generation."""
    parser = argparse.ArgumentParser(
        description="Generate a CDP infographic via Gemini API",
    )
    parser.add_argument(
        "type",
        help="Infographic type slug (e.g., domain-scorecard)",
    )
    parser.add_argument(
        "data",
        type=Path,
        help="Path to data JSON file",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Output PNG file path",
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip pre-flight validation",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path(".cdp-context"),
        help="Config directory (default: .cdp-context)",
    )
    args = parser.parse_args()

    result = generate_infographic(
        args.type,
        args.data,
        args.output,
        args.skip_preflight,
        args.config_dir,
    )
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
