"""Session orchestrator for generating all infographic types.

Iterates over infographic types, calls generate_with_retry for each,
applies inter-call delay between API calls, adapts delay on 429 rate
limits, and prints a final summary table.

Exports:
    run_session        -- Orchestrate generation for a list of types
    SessionResult      -- Dataclass with results, summary, success flag
    _format_summary_line -- Format a single summary status line
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from scripts.config import load_config
from scripts.generate_infographic import (
    GenerationResult,
    _is_content_block,
    generate_with_retry,
)


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class SessionResult:
    """Result of a full session generating multiple infographic types.

    Attributes:
        results:       Dict mapping type slug to its GenerationResult.
        summary_lines: Formatted summary status lines for output.
        any_succeeded: True if at least one infographic generated successfully.
        total_types:   Total number of infographic types in the session.
    """

    results: dict[str, GenerationResult]
    summary_lines: list[str] = field(default_factory=list)
    any_succeeded: bool = False
    total_types: int = 0


# ---------------------------------------------------------------------------
# Status output
# ---------------------------------------------------------------------------


def _status(stage: str, detail: str = "") -> None:
    """Print a structured status line parseable by the CEO agent.

    Args:
        stage: Status keyword (e.g. SESSION, SUMMARY, RATE_LIMIT).
        detail: Optional extra information.
    """
    if detail:
        print(f"{stage} {detail}")
    else:
        print(stage)


# ---------------------------------------------------------------------------
# Summary formatting
# ---------------------------------------------------------------------------


def _format_summary_line(
    type_slug: str,
    status: str,
    attempts: int,
    max_attempts: int,
    output_path: Path | None,
) -> str:
    """Format a single summary status line.

    Produces a line like::

        SUMMARY domain-scorecard          OK       1/3  images/INFOGRAPHIC_domain-scorecard.png

    Args:
        type_slug: Infographic type slug.
        status: Status string (OK, OK+WARN, FAILED, BLOCKED).
        attempts: Number of attempts used.
        max_attempts: Maximum attempts allowed.
        output_path: Output file path (or None if no output).

    Returns:
        Formatted summary line string.
    """
    path_str = str(output_path) if output_path else "N/A"
    return f"SUMMARY {type_slug:<30s} {status:<10s} {attempts}/{max_attempts}  {path_str}"


# ---------------------------------------------------------------------------
# Session orchestrator
# ---------------------------------------------------------------------------


def run_session(
    types_list: list[str],
    data_paths: dict[str, Path],
    output_dir: Path,
    config_dir: Path = Path(".cdp-context"),
) -> SessionResult:
    """Run generation for all infographic types with inter-call delay.

    Iterates over *types_list*, calling :func:`generate_with_retry` for
    each.  Applies a 4-second inter-call delay between consecutive API
    calls.  If any result encounters a 429 rate limit, the delay doubles
    for remaining images.

    After all types are processed, prints a summary table showing status,
    attempts, and output path for each type.

    Args:
        types_list: Ordered list of infographic type slugs to generate.
        data_paths: Dict mapping type slug to its data JSON path.
        output_dir: Directory for output PNGs.
        config_dir: Directory containing ``config.md``.

    Returns:
        :class:`SessionResult` with per-type results and summary.
    """
    config = load_config(config_dir)
    retry_limit = config.get("retry_limit", 2)
    max_attempts = retry_limit + 1
    inter_call_delay = 4.0
    results: dict[str, GenerationResult] = {}

    for i, type_slug in enumerate(types_list):
        # Apply inter-call delay BETWEEN images (not before first)
        if i > 0:
            time.sleep(inter_call_delay)

        _status("SESSION", f"generating {type_slug} ({i + 1}/{len(types_list)})")

        data_path = data_paths[type_slug]
        output_path = output_dir / f"INFOGRAPHIC_{type_slug}.png"

        result = generate_with_retry(
            type_slug,
            data_path,
            output_path,
            retry_limit,
            config_dir,
        )
        results[type_slug] = result

        # Adaptive delay: double on 429
        if result.had_rate_limit:
            inter_call_delay *= 2
            _status(
                "RATE_LIMIT",
                f"doubling inter-call delay to {inter_call_delay}s",
            )

    # --- Build summary table ---
    summary_lines: list[str] = []
    _status("SUMMARY", "-------")

    for type_slug in types_list:
        result = results[type_slug]
        error_code = result.error_code or ""

        # Determine status
        if result.success:
            status = "OK"
            # We can't easily detect OK+WARN here without extra info,
            # but we record it if the result has warning metadata.
            # For now, OK covers both OK and OK+WARN at session level.
        elif _is_content_block(error_code):
            status = "BLOCKED"
        else:
            status = "FAILED"

        # Determine attempts used (approximation: 1 for success on first,
        # max for failure; had_rate_limit suggests at least 2)
        if result.success:
            attempts = 1
            if result.had_rate_limit:
                attempts = 2  # At least 2 if rate limited
        elif _is_content_block(error_code):
            attempts = 0  # Content block doesn't consume budget
        else:
            attempts = max_attempts

        line = _format_summary_line(
            type_slug, status, attempts, max_attempts, result.output_path
        )
        summary_lines.append(line)
        _status("SUMMARY", line.replace("SUMMARY ", "", 1))

    _status("SUMMARY", "-------")

    any_succeeded = any(r.success for r in results.values())

    return SessionResult(
        results=results,
        summary_lines=summary_lines,
        any_succeeded=any_succeeded,
        total_types=len(types_list),
    )
