"""CDP configuration parser.

Reads API key, model ID, and retry limit from a markdown-formatted
config file at `.cdp-context/config.md`.

Exports:
    parse_config  -- Low-level field extraction from markdown
    load_config   -- High-level: parse, validate, apply defaults, return typed dict
    ConfigError   -- Structured exception with error_code and remediation
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# Matches markdown field lines: `- **Field Name:** value`
FIELD_PATTERN = re.compile(r"^-\s+\*\*(.+?):\*\*\s*(.*)$", re.MULTILINE)

# Matches `(default: <value>)` inside a placeholder
DEFAULT_PATTERN = re.compile(r"^\(default:\s*(.+?)\)$")

# Defaults applied when field is empty or placeholder
DEFAULT_MODEL_ID = "gemini-2.5-flash-image"
DEFAULT_RETRY_LIMIT = 2


class ConfigError(Exception):
    """Structured config error with machine-readable code and human-readable remediation.

    Attributes:
        error_code:   Short identifier (e.g. CONFIG_NOT_FOUND, CONFIG_MISSING_KEY).
        message:      Human-readable description of the problem.
        remediation:  Actionable fix instructions.
    """

    def __init__(self, error_code: str, message: str, remediation: str = "") -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.remediation = remediation


def _extract_value(raw: str) -> str:
    """Resolve a raw field value, handling placeholders and defaults.

    Rules:
        - If value starts with '(' it is a placeholder.
          - If it matches `(default: X)`, return X.
          - Otherwise return empty string (unfilled placeholder).
        - Otherwise return the stripped value as-is.
    """
    raw = raw.strip()
    if not raw:
        return ""
    if raw.startswith("("):
        match = DEFAULT_PATTERN.match(raw)
        if match:
            return match.group(1).strip()
        return ""
    return raw


def parse_config(config_path: Path) -> dict[str, str]:
    """Extract markdown fields from a config file.

    Args:
        config_path: Path to the config.md file.

    Returns:
        Dict mapping lowercase field names to their extracted values.
        Placeholder values are resolved via ``_extract_value``.

    Raises:
        ConfigError: If the file does not exist.
    """
    if not config_path.exists():
        raise ConfigError(
            error_code="CONFIG_NOT_FOUND",
            message=f"Config file not found: {config_path}",
            remediation=(
                "Copy templates/config-context.md to .cdp-context/config.md "
                "and fill in your Gemini API key."
            ),
        )

    text = config_path.read_text()
    fields: dict[str, str] = {}

    for match in FIELD_PATTERN.finditer(text):
        name = match.group(1).strip().lower()
        value = _extract_value(match.group(2))
        fields[name] = value

    return fields


def load_config(config_dir: Path) -> dict[str, Any]:
    """Parse, validate, and return typed configuration.

    This is the high-level entry point. It reads ``config_dir/config.md``,
    validates the API key, applies defaults for model ID and retry limit,
    and converts retry limit to int.

    Args:
        config_dir: Directory containing ``config.md`` (typically ``.cdp-context``).

    Returns:
        Dict with keys ``api_key`` (str), ``model_id`` (str), ``retry_limit`` (int).

    Raises:
        ConfigError: On missing API key, invalid retry limit, or missing file.
    """
    config_path = config_dir / "config.md"
    fields = parse_config(config_path)

    # --- API key (required, no default) ---
    api_key = fields.get("gemini api key", "")
    if not api_key:
        raise ConfigError(
            error_code="CONFIG_MISSING_KEY",
            message="Gemini API key is missing or empty in config.",
            remediation=(
                "Open .cdp-context/config.md and paste your Gemini API key "
                "after '**Gemini API Key:**'. "
                "Get one at https://aistudio.google.com/apikey"
            ),
        )

    # --- Model ID (defaults to gemini-2.5-flash-image) ---
    model_id = fields.get("image model", "")
    if not model_id:
        model_id = DEFAULT_MODEL_ID

    # --- Retry limit (defaults to 2, must be int) ---
    retry_raw = fields.get("retry limit", "")
    if not retry_raw:
        retry_limit = DEFAULT_RETRY_LIMIT
    else:
        try:
            retry_limit = int(retry_raw)
        except ValueError:
            raise ConfigError(
                error_code="CONFIG_INVALID_RETRY",
                message=f"Retry limit must be an integer, got: '{retry_raw}'",
                remediation=(
                    "Set Retry Limit to a whole number (e.g. 2 or 3) "
                    "in .cdp-context/config.md."
                ),
            )

    return {
        "api_key": api_key,
        "model_id": model_id,
        "retry_limit": retry_limit,
    }
