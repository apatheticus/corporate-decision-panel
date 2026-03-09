"""Vision-based quality validation for generated infographics.

Sends a generated PNG back to Gemini vision along with expected data labels
extracted from the source data JSON.  The vision model checks that labels
are present and readable, returning a structured VERDICT/WARNINGS/MISSING/
FEEDBACK response that drives retry decisions.

Exports:
    validate_infographic      -- Full validation flow: load, send, parse
    ValidationResult          -- Dataclass with passed/warning_only/feedback/warnings/missing
    _extract_expected_labels  -- Extract expected text labels from data dict
    _parse_validation_response -- Parse structured validation response text
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from google import genai
from google.genai import types
from google.genai.errors import APIError

from scripts.config import load_config


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class ValidationResult:
    """Result of a vision quality validation check.

    Attributes:
        passed:       True if all expected labels are present.
        warning_only: True if passed but with warnings (partial labels).
        feedback:     Corrective feedback text for retry (None if passed clean).
        warnings:     List of warning messages (e.g. truncated labels).
        missing:      List of missing labels detected by vision model.
        garbled:      List of garbled/misspelled text detected by vision model.
    """

    passed: bool
    warning_only: bool = False
    feedback: str | None = None
    warnings: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    garbled: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Lenient validation types
# ---------------------------------------------------------------------------

LENIENT_TYPES: set[str] = {"routing-diagram"}
"""Infographic types where PARTIAL labels are acceptable (clean pass).

High-density types like routing diagrams have inherently dense text that
triggers PARTIAL label detection during vision validation.  For these types,
PARTIAL labels are expected and should not waste retry budget.

Garbled text detection remains strict for all types.
"""


# ---------------------------------------------------------------------------
# Label extraction
# ---------------------------------------------------------------------------


def _extract_expected_labels(data: dict) -> list[str]:
    """Extract expected text labels from a data dict.

    Iterates over data dict values, skipping numeric-only values.
    For string values containing commas that indicate multiple items
    (e.g. "Finance: Approve (High), Legal: Oppose (Medium)"), splits
    on ", " and includes sub-items.

    Args:
        data: Data dict mapping placeholder tokens to concrete values.

    Returns:
        Deduplicated list of expected label strings.
    """
    labels: list[str] = []

    for value in data.values():
        text = str(value).strip()

        # Skip numeric-only values
        if re.match(r"^\d+(\.\d+)?$", text):
            continue

        # Split on ", " if the string contains multiple items
        # Heuristic: contains a comma followed by a space and then an
        # uppercase letter or word boundary indicating a new item
        if ", " in text and re.search(r", [A-Z]", text):
            parts = [p.strip() for p in text.split(", ")]
            labels.extend(parts)
        else:
            labels.append(text)

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for label in labels:
        if label not in seen:
            seen.add(label)
            unique.append(label)

    return unique


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------


def _parse_validation_response(text: str) -> ValidationResult:
    """Parse a structured validation response from the vision model.

    Expected format::

        VERDICT: PASS|FAIL
        WARNINGS: [labels or 'none']
        MISSING: [labels or 'none']
        GARBLED: [garbled text or 'none']
        FEEDBACK: [guidance or 'none']

    If the response is unparseable, returns a fail-closed result
    (validation must not silently pass bad images).

    Args:
        text: Raw text response from the vision model.

    Returns:
        Parsed :class:`ValidationResult`.
    """
    lines = text.strip().split("\n")

    verdict = None
    warnings: list[str] = []
    missing: list[str] = []
    garbled: list[str] = []
    feedback: str | None = None

    for line in lines:
        line_lower = line.strip().lower()

        if line_lower.startswith("verdict:"):
            verdict_text = line.split(":", 1)[1].strip().upper()
            if "PASS" in verdict_text:
                verdict = "PASS"
            elif "FAIL" in verdict_text:
                verdict = "FAIL"

        elif line_lower.startswith("warnings:"):
            content = line.split(":", 1)[1].strip()
            if content.lower() != "none" and content:
                warnings = [w.strip() for w in content.split(",") if w.strip()]

        elif line_lower.startswith("missing:"):
            content = line.split(":", 1)[1].strip()
            if content.lower() != "none" and content:
                missing = [m.strip() for m in content.split(",") if m.strip()]

        elif line_lower.startswith("garbled:"):
            content = line.split(":", 1)[1].strip()
            if content.lower() != "none" and content:
                garbled = [g.strip() for g in content.split(",") if g.strip()]

        elif line_lower.startswith("feedback:"):
            content = line.split(":", 1)[1].strip()
            if content.lower() != "none" and content:
                feedback = content

    # Handle unparseable response -- fail closed
    if verdict is None:
        return ValidationResult(
            passed=False,
            warning_only=False,
            feedback="Validation response unparseable -- treating as fail",
        )

    passed = verdict == "PASS"
    warning_only = passed and len(warnings) > 0

    return ValidationResult(
        passed=passed,
        warning_only=warning_only,
        feedback=feedback,
        warnings=warnings,
        missing=missing,
        garbled=garbled,
    )


# ---------------------------------------------------------------------------
# Status output
# ---------------------------------------------------------------------------


def _status(stage: str, detail: str = "") -> None:
    """Print a structured status line parseable by the CEO agent.

    Args:
        stage: Status keyword (e.g. VALIDATING, VALIDATION).
        detail: Optional extra information.
    """
    if detail:
        print(f"{stage} {detail}")
    else:
        print(stage)


# ---------------------------------------------------------------------------
# Vision quality validation
# ---------------------------------------------------------------------------


def validate_infographic(
    image_path: Path,
    data_path: Path,
    config_dir: Path,
    type_slug: str | None = None,
) -> ValidationResult:
    """Validate that expected data labels are present in a generated infographic.

    Sends the PNG image and a structured validation prompt to the Gemini
    vision model.  The prompt includes expected labels extracted from the
    source data JSON.  The model responds with a structured VERDICT that
    is parsed into a :class:`ValidationResult`.

    SDK retry is disabled (``HttpRetryOptions(attempts=1)``) so the
    application layer controls retry budget.

    On API error, returns ``passed=False`` -- validation fails closed
    to prevent bad images from passing silently.

    For types listed in :data:`LENIENT_TYPES`, PARTIAL label warnings
    are promoted to a clean pass (garbled text detection stays strict).

    Args:
        image_path: Path to the generated PNG file.
        data_path: Path to the source data JSON file.
        config_dir: Directory containing ``config.md`` with API key and model.
        type_slug: Optional infographic type slug for leniency lookup.

    Returns:
        :class:`ValidationResult` with verdict, warnings, and feedback.
    """
    config = load_config(config_dir)

    client = genai.Client(
        api_key=config["api_key"],
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )

    image_bytes = image_path.read_bytes()
    data = json.loads(data_path.read_text())
    expected_labels = _extract_expected_labels(data)

    # Derive type label from image filename for status output
    status_label_slug = image_path.stem.replace("INFOGRAPHIC_", "")
    _status("VALIDATING", status_label_slug)

    prompt = (
        "You are a strict quality checker for data infographics.\n\n"
        "TASK 1 — DATA LABELS\n"
        "Verify that the following data labels are present and clearly readable:\n\n"
        + "\n".join(f"- {label}" for label in expected_labels)
        + "\n\nFor each label, report: FOUND (clearly readable), "
        "PARTIAL (present but truncated/hard to read), or MISSING.\n"
        "A PARTIAL label counts as a failure — only FOUND is acceptable.\n\n"
        "TASK 2 — ALL VISIBLE TEXT\n"
        "Scan ALL visible text in the infographic (titles, axis labels, "
        "legends, annotations, captions — everything). Report any text that "
        "is garbled, misspelled, nonsensical, or not a real English word "
        "(e.g. 'Emmerruation' instead of 'Enumeration', 'Recommendians' "
        "instead of 'Recommendations').\n\n"
        "VERDICT RULES:\n"
        "- FAIL if any label is MISSING or PARTIAL\n"
        "- FAIL if any garbled/misspelled text is found\n"
        "- PASS only when all labels are FOUND and no garbled text exists\n\n"
        "Format your response EXACTLY as:\n"
        "VERDICT: PASS|FAIL\n"
        "WARNINGS: [any PARTIAL labels, or 'none']\n"
        "MISSING: [any MISSING labels, or 'none']\n"
        "GARBLED: [any garbled/misspelled text found, or 'none']\n"
        "FEEDBACK: [if FAIL, specific guidance for regeneration, or 'none']"
    )

    try:
        response = client.models.generate_content(
            model=config["model_id"],
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                prompt,
            ],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT"],
            ),
        )

        result = _parse_validation_response(response.text)

        # Apply leniency for high-density types: PARTIAL labels count as clean pass
        # Garbled text detection stays strict for all types
        if (
            type_slug is not None
            and type_slug in LENIENT_TYPES
            and result.warning_only
            and not result.garbled
        ):
            result = ValidationResult(
                passed=True,
                warning_only=False,
                feedback=None,
                warnings=result.warnings,
                missing=result.missing,
                garbled=result.garbled,
            )

    except (APIError, Exception) as e:
        _status("VALIDATION", f"ERROR {e}")
        return ValidationResult(
            passed=False,
            warning_only=False,
            feedback=f"Validation API error: {e}",
        )

    status_label = "PASS" if result.passed else "FAIL"
    if result.warning_only:
        status_label = "WARN"
    _status("VALIDATION", status_label)

    return result
