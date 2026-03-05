"""Pre-flight validation for Gemini API configuration.

Validates API key, billing status, and model accessibility
before any infographic generation starts.

Usage:
    Standalone: python -m scripts.preflight
    Importable: from scripts.preflight import run_preflight, PreflightResult
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from scripts.config import ConfigError, load_config


@dataclass
class PreflightResult:
    """Result of a pre-flight validation run.

    Attributes:
        success:    True if all 4 validation steps passed.
        error_code: Machine-readable error identifier (None on success).
        model_id:   Validated model ID (None on failure).
    """

    success: bool
    error_code: str | None = None
    model_id: str | None = None


def _print_error(error_code: str, message: str, remediation: str) -> None:
    """Print a dual-audience error message.

    Format is parseable by AI agents (CEO) via the bracketed error_code
    and readable by human operators via the message + fix lines.
    """
    print(f"PREFLIGHT FAILED [{error_code}]")
    print(f"  Error: {message}")
    print(f"  Fix: {remediation}")


def _print_success(model_id: str, api_key: str) -> None:
    """Print a structured success message with key preview."""
    key_preview = api_key[:8] + "..."
    print("PREFLIGHT OK")
    print(f"  Model: {model_id}")
    print(f"  Key: {key_preview}")


def run_preflight(config_dir: Path) -> PreflightResult:
    """Run the 4-step pre-flight validation chain.

    Steps:
        1. Parse and validate configuration (config.md)
        2. Validate API key (models.list)
        3. Validate model accessibility (models.get)
        4. Validate billing / image generation (generate_content probe)

    Args:
        config_dir: Path to the directory containing config.md
                    (typically .cdp-context).

    Returns:
        PreflightResult with success status, error code, and model ID.
    """
    # --- Step 1: Config ---
    try:
        config = load_config(config_dir)
    except ConfigError as e:
        _print_error(e.error_code, e.message, e.remediation)
        return PreflightResult(success=False, error_code=e.error_code)

    api_key = config["api_key"]
    model_id = config["model_id"]

    # --- Step 2: API key validity ---
    client = genai.Client(api_key=api_key)
    try:
        list(client.models.list())
    except ClientError as e:
        if e.code in (400, 403):
            _print_error(
                "INVALID_API_KEY",
                "Gemini API key is invalid or unauthorized",
                "Verify your key at https://aistudio.google.com/apikey",
            )
            return PreflightResult(success=False, error_code="INVALID_API_KEY")
        raise

    # --- Step 3: Model accessibility ---
    try:
        client.models.get(model=model_id)
    except ClientError as e:
        if e.code == 404:
            _print_error(
                "MODEL_NOT_FOUND",
                f"Model '{model_id}' not found or not accessible",
                "Check available models at https://ai.google.dev/gemini-api/docs/models",
            )
            return PreflightResult(success=False, error_code="MODEL_NOT_FOUND")
        raise

    # --- Step 4: Billing / image generation probe ---
    try:
        client.models.generate_content(
            model=model_id,
            contents="Generate a 1x1 white square",
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    image_size="512px",
                ),
            ),
        )
    except ClientError as e:
        if e.code == 403:
            _print_error(
                "BILLING_NOT_ENABLED",
                "Image generation requires billing to be enabled",
                "Enable billing at https://aistudio.google.com/apikey "
                "(check Quota tier column shows Tier 1+)",
            )
            return PreflightResult(success=False, error_code="BILLING_NOT_ENABLED")
        if e.code == 429:
            _print_error(
                "RATE_LIMITED",
                "API rate limit hit during pre-flight probe",
                "Wait a moment and try again",
            )
            return PreflightResult(success=False, error_code="RATE_LIMITED")
        raise

    # --- All steps passed ---
    _print_success(model_id, api_key)
    return PreflightResult(success=True, model_id=model_id)


def main() -> None:
    """CLI entry point for standalone pre-flight validation."""
    parser = argparse.ArgumentParser(
        description="Run CDP pre-flight validation checks",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path(".cdp-context"),
        help="Directory containing config.md (default: .cdp-context)",
    )
    args = parser.parse_args()

    result = run_preflight(args.config_dir)
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
