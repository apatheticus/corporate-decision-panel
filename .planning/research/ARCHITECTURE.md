# Architecture Research

**Domain:** Gemini API image generation integration into multi-agent Claude Code skill
**Researched:** 2026-03-04
**Confidence:** HIGH (official SDK docs + official error docs + verified patterns)

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CEO Agent (Orchestrator)                          │
│  Spawns Task A (Image Agent) in parallel with Tasks B and C         │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ TaskCreate (session-output, issue-slug)
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Image Agent (Task A)                           │
│                                                                      │
│  ┌─────────────────┐   ┌──────────────────┐   ┌─────────────────┐  │
│  │  Config Reader  │   │  Template Engine │   │  Prompt Builder │  │
│  │                 │   │                  │   │                 │  │
│  │ Reads API key   │   │ Loads JSON       │   │ Replaces        │  │
│  │ from            │   │ prompt template  │   │ {{PLACEHOLDER}} │  │
│  │ .cdp-context/   │   │ from templates/  │   │ tokens with     │  │
│  │ config.md       │   │ infographic-     │   │ Decision Record │  │
│  └────────┬────────┘   │ prompts/*.json   │   │ data            │  │
│           │            └────────┬─────────┘   └────────┬────────┘  │
│           │                     │                       │           │
│           └─────────────────────▼───────────────────────┘           │
│                                 │                                    │
│                    ┌────────────▼────────────┐                      │
│                    │    API Call Layer        │                      │
│                    │                         │                      │
│                    │  google-genai SDK        │                      │
│                    │  client.models           │                      │
│                    │  .generate_content()     │                      │
│                    └────────────┬────────────┘                      │
│                                 │                                    │
│                    ┌────────────▼────────────┐                      │
│                    │   Response Handler       │                      │
│                    │                         │                      │
│                    │  Check finish_reason     │                      │
│                    │  Check inline_data       │                      │
│                    │  Write PNG bytes         │                      │
│                    └────────────┬────────────┘                      │
│                                 │                                    │
│           ┌─────────────────────▼───────────────────────┐           │
│           │                                             │           │
│    ┌──────▼──────┐                           ┌──────────▼──────┐   │
│    │  PNG Output │                           │ Placeholder PNG  │   │
│    │             │                           │ + _PROMPT.json   │   │
│    │ {session}/  │                           │ fallback on      │   │
│    │ images/     │                           │ all retries      │   │
│    │ INFOGRAPHIC │                           │ exhausted        │   │
│    │ _<slug>.png │                           └──────────────────┘   │
│    └─────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  External: Gemini API                                │
│                                                                      │
│  Endpoint: generativelanguage.googleapis.com (via SDK)               │
│  Model: gemini-2.0-flash-exp-image-generation (or current)          │
│  Auth: API key passed in client constructor                          │
│  Response: inline_data bytes (PNG) in candidates[0].content.parts   │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Implementation |
|-----------|---------------|----------------|
| Config Reader | Read API key from `.cdp-context/config.md`; parse the `Gemini API Key:` field | Python string parsing (regex or split on `:`) |
| Template Engine | Load the correct JSON template for each infographic type from `templates/infographic-prompts/*.json` | Python `json.load()` |
| Style Applier | If `.cdp-context/style.md` exists, override matching JSON keys per the style mapping table | Python dict mutation |
| Prompt Builder | Replace all `{{PLACEHOLDER}}` tokens with data extracted from the Decision Record | Python `str.replace()` in a loop; serialize back to JSON string |
| API Call Layer | Call `client.models.generate_content()` with populated JSON string as contents; handle retries | `google-genai` SDK, retry loop with exponential backoff |
| Response Handler | Check `finish_reason`; extract `inline_data.data` bytes; write PNG file | Python file I/O, `open(..., "wb")` |
| Placeholder Generator | On exhausted retries, write white PNG with centered failure text; save prompt JSON | Python `Pillow` for PNG generation |

## Recommended Project Structure

The migration replaces browser automation with a Python helper script. The Image Agent instruction document calls this script instead of performing browser steps.

```
templates/
├── infographic-prompts/        # Existing JSON templates (unchanged)
│   ├── routing-diagram.json
│   ├── domain-scorecard.json
│   ├── fault-line-map.json
│   ├── risk-opportunity-matrix.json
│   ├── action-plan-timeline.json
│   └── mode-comparison.json
└── production/
    └── infographics.md         # Update: replace browser steps with API steps

scripts/                        # NEW — helper for infographic generation
└── generate_infographic.py     # Python script: reads key, calls API, saves PNG

.cdp-context/
└── config.md                   # ADD: Gemini API Key field
```

### Structure Rationale

- **`scripts/generate_infographic.py`**: Keeps the API logic out of the markdown instruction file. The Image Agent calls this script with arguments (template path, output path, populated JSON) rather than embedding Python in the markdown prompt. This is the most Claude Code-compatible pattern — agents can call Bash tool to invoke Python scripts.
- **`templates/production/infographics.md`**: Updated to describe the API workflow instead of browser steps. The script invocation replaces the 8-step browser cycle.
- **`templates/infographic-prompts/*.json`**: Unchanged in structure. The JSON prompt format is compatible with direct API submission — the populated JSON becomes the text prompt sent to Gemini.

## Architectural Patterns

### Pattern 1: Config File → API Key Parsing

**What:** Read the API key from `.cdp-context/config.md` at runtime. The file uses markdown with a field like `- **Gemini API Key:** sk-...`. The script must parse the markdown to extract the key.

**When to use:** The CDP pattern stores config in markdown (not env vars, not JSON). This is by design — it keeps user-visible configuration in a readable, gitignored file.

**Trade-offs:** Parsing markdown is fragile if field format drifts. Recommend a strict, documented field syntax and a clear error message when the key is missing or empty.

**Example:**
```python
import re

def read_api_key(config_path: str) -> str:
    """Read Gemini API key from .cdp-context/config.md."""
    with open(config_path, "r") as f:
        content = f.read()
    # Match: - **Gemini API Key:** <value>
    match = re.search(r'\*\*Gemini API Key:\*\*\s*(.+)', content)
    if not match or not match.group(1).strip():
        raise ValueError(
            "Gemini API Key not found in .cdp-context/config.md. "
            "Add: - **Gemini API Key:** YOUR_KEY_HERE"
        )
    return match.group(1).strip()
```

### Pattern 2: JSON Prompt as Text Contents

**What:** The populated JSON prompt object is serialized as a string and sent as the `contents` parameter to `generate_content()`. Gemini image models accept plain text instructions; the JSON structure is the instruction language, not a structured API parameter.

**When to use:** This matches the existing prompt design (Pauhu schema hybrid). The agent already knows how to populate the JSON — nothing changes in the template format.

**Trade-offs:** Gemini treats the JSON as a text description. It is not parsed as structured schema by the model — the model reads it as a highly structured text prompt. This is intentional and is already validated by the existing browser-based workflow.

**Example:**
```python
import json

def build_prompt_string(template_path: str, replacements: dict) -> str:
    """Load JSON template, apply replacements, return as serialized string."""
    with open(template_path, "r") as f:
        raw = f.read()
    for placeholder, value in replacements.items():
        raw = raw.replace(f"{{{{{placeholder}}}}}", value)
    # Validate it's still valid JSON after replacements
    json.loads(raw)
    return raw
```

### Pattern 3: finish_reason Guard Before Accessing Parts

**What:** Always check `candidate.finish_reason` before accessing `candidate.content.parts`. When blocked (`SAFETY`, `OTHER`, `IMAGE_SAFETY`, `NO_IMAGE`), `content.parts` may be `None` or empty, causing an `IndexError` or `AttributeError`.

**When to use:** Every image generation response. This is not optional defensive programming — the SDK has a known issue where accessing `finish_reason` on certain blocked responses can cause an indefinite hang (Issue #2024 in python-genai).

**Trade-offs:** Adds a small check before every response access. Necessary for production reliability.

**Example:**
```python
from google.genai import types

TERMINAL_FINISH_REASONS = {"STOP"}
BLOCKED_FINISH_REASONS = {"SAFETY", "OTHER", "RECITATION", "IMAGE_SAFETY", "NO_IMAGE"}

def extract_image_bytes(response) -> bytes | None:
    """Extract PNG bytes from a Gemini image generation response."""
    if not response.candidates:
        return None

    candidate = response.candidates[0]

    # Check finish reason before accessing content
    finish_reason = str(candidate.finish_reason)
    if any(blocked in finish_reason for blocked in BLOCKED_FINISH_REASONS):
        return None

    if candidate.content is None or not candidate.content.parts:
        return None

    for part in candidate.content.parts:
        if part.inline_data is not None:
            return part.inline_data.data

    return None
```

### Pattern 4: Retry with Exponential Backoff

**What:** Wrap the API call in a retry loop. Retry on `429 RESOURCE_EXHAUSTED` and `503 UNAVAILABLE` with exponential backoff. Do not retry on `SAFETY`/`OTHER` blocks — these are content decisions, not transient errors.

**When to use:** All production Gemini API calls. The simplified retry model (remove hard budget tracking from browser automation) is appropriate here — API calls are fast and cheap.

**Trade-offs:** Too-eager retry on 429 can worsen rate limit exhaustion. Jitter prevents synchronized retry storms when running multiple infographics.

**Example:**
```python
import time
import random
from google.api_core import exceptions as google_exceptions

def generate_with_retry(client, model: str, prompt: str, max_retries: int = 3) -> bytes | None:
    """Call Gemini image generation with exponential backoff on transient errors."""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"]
                )
            )
            image_bytes = extract_image_bytes(response)
            if image_bytes:
                return image_bytes
            # Non-transient failure (content blocked) — do not retry
            return None

        except google_exceptions.ResourceExhausted:
            if attempt == max_retries:
                raise
            wait = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait)

        except google_exceptions.ServiceUnavailable:
            if attempt == max_retries:
                raise
            wait = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait)

        except Exception:
            raise  # Don't retry on unknown errors

    return None
```

## Data Flow

### Infographic Generation Flow

```
Decision Record (RECORD.md)
    │
    │  [Image Agent reads]
    ▼
Section extraction (per infographic type)
    │  e.g., Section 2 for routing-diagram, Section 4 for domain-scorecard
    ▼
.cdp-context/config.md  →  API key extraction
    │
.cdp-context/style.md   →  Style override dict (if present)
    │
templates/infographic-prompts/<type>.json  →  Template load
    │
    ├── Apply {{PLACEHOLDER}} replacements from Decision Record data
    ├── Apply style overrides to JSON dict
    └── Serialize to prompt string (JSON)
    │
    ▼
scripts/generate_infographic.py
    │
    ├── google-genai client.models.generate_content()
    │       model: gemini-2.0-flash-exp-image-generation
    │       contents: populated JSON string
    │       config: response_modalities=["IMAGE"]
    │
    ├── On success: response.candidates[0].content.parts → inline_data.data (PNG bytes)
    │
    └── On failure: retry up to N times (transient) or return None (content block)
    │
    ▼
{session-output}/images/INFOGRAPHIC_<type-slug>.png
    │   (always written — real PNG or placeholder PNG)
    │
    ▼
Task D (Web Page Agent) unblocked
Task B (PPTX Agent) unblocked
Task C (DOCX Agent) unblocked
```

### Error Escalation Flow

```
API Call
    │
    ├── HTTP 429 / 503 → retry with backoff (up to max_retries)
    │
    ├── HTTP 400 INVALID_ARGUMENT → log error, skip retry, write placeholder
    │
    ├── HTTP 403 PERMISSION_DENIED → abort all infographics, report key error
    │
    ├── finish_reason SAFETY / OTHER / IMAGE_SAFETY → write placeholder + prompt JSON
    │
    └── All retries exhausted → write placeholder + prompt JSON
                                 (pipeline continues, Tasks B/C/D not blocked)
```

### Config File Data Flow

```
.cdp-context/config.md
    │
    │  Parsed by: scripts/generate_infographic.py at startup
    │  Fields read:
    │    - "Gemini API Key:" → passed to genai.Client(api_key=...)
    │    - "Platform:" → checked; script only runs if value is "gemini"
    │
    ▼
genai.Client(api_key=KEY)
    │  Client instantiated once, reused for all 5-6 infographic calls
    ▼
Per-infographic generate_content() calls
```

## Scaling Considerations

This is a Claude Code skill running locally — scaling in the traditional sense does not apply. Relevant constraints instead:

| Concern | Reality | Guidance |
|---------|---------|----------|
| Rate limits (RPM) | Free tier: ~10 RPM; paid: varies by tier | Sequential generation (5-6 calls) rarely hits RPM unless retrying aggressively |
| Rate limits (RPD) | Free tier: ~1500 RPD; paid: higher | Not a practical constraint for CDP usage patterns |
| Latency per call | 5-30 seconds per image (model-dependent) | Sequential generation of 6 infographics can take 1-3 minutes total |
| Concurrent calls | Possible in theory | Out of scope per PROJECT.md; sequential is safer for rate limits |
| Key exposure | API key in `.cdp-context/config.md` (gitignored) | Acceptable; consistent with CDP config pattern |

## Anti-Patterns

### Anti-Pattern 1: Accessing response.candidates[0] Without Checking finish_reason

**What people do:** Immediately index into `response.candidates[0].content.parts` assuming success.

**Why it's wrong:** When Gemini blocks a request (SAFETY, OTHER, IMAGE_SAFETY, NO_IMAGE), `content` may be `None` or `parts` may be empty. The SDK has a known hang bug on certain `finish_reason` enum values during image generation (python-genai issue #2024). This causes an `AttributeError`, `IndexError`, or infinite hang.

**Do this instead:** Check `response.candidates` is non-empty, then check `candidate.finish_reason` as a string before accessing `content.parts`. See Pattern 3 above.

### Anti-Pattern 2: Retrying on Content-Policy Blocks

**What people do:** Retry on any non-200 response or any absence of image data, including when Gemini returns `finish_reason: OTHER` due to copyright or content policy.

**Why it's wrong:** Content policy blocks are deterministic. Retrying the same prompt produces the same block. It wastes API quota and causes false delays.

**Do this instead:** Distinguish transient errors (429, 503, 500) from content decisions (SAFETY, OTHER, IMAGE_SAFETY). Only retry transient errors. On a content block, immediately fall through to the simplified prompt or placeholder.

### Anti-Pattern 3: Using the Legacy google-generativeai Package

**What people do:** `pip install google-generativeai` and use `import google.generativeai as genai`.

**Why it's wrong:** `google-generativeai` was deprecated with a sunset deadline of August 31, 2025. The package is no longer updated, and image generation support lags behind the current model lineup.

**Do this instead:** Use `pip install google-genai` and `from google import genai`. This is the unified Gen AI SDK covering all Gemini and Imagen models.

### Anti-Pattern 4: Storing API Key in Environment Variables Only

**What people do:** Rely on `GEMINI_API_KEY` environment variable exclusively, and don't document where the key comes from.

**Why it's wrong:** CDP's configuration model uses `.cdp-context/config.md` as the canonical user-facing config file. Requiring a separate env var breaks the skill's configuration coherence and requires out-of-band setup that isn't in the CDP documentation flow.

**Do this instead:** Read the API key from `.cdp-context/config.md`. The script can fall back to `os.environ.get("GEMINI_API_KEY")` as a secondary option for power users, but the primary path must be the config file.

### Anti-Pattern 5: Hardcoding the Model String

**What people do:** Hardcode `"gemini-2.0-flash-exp-image-generation"` in the script.

**Why it's wrong:** Google's image generation model names have changed multiple times (gemini-2.0-flash-exp → gemini-2.5-flash-image → gemini-3.1-flash-image-preview). The `-exp` suffix indicates experimental and may stop working without warning.

**Do this instead:** Put the model name in `.cdp-context/config.md` with a sensible default. Read it at runtime. The infographics.md Task A spec should document the current recommended model.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Gemini API | `google-genai` SDK; `client.models.generate_content()` | Use `google-genai` (not legacy `google-generativeai`); API key in config file |
| Gemini API auth | `genai.Client(api_key=KEY)` | Key from `.cdp-context/config.md`; do not commit; already gitignored |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Image Agent → Script | Agent calls Bash tool: `python3 scripts/generate_infographic.py <args>` | Script receives template path, Decision Record data, output path as args or stdin |
| Script → Config | Script reads `.cdp-context/config.md` at startup | Must gracefully fail with a clear error if key missing |
| Script → Templates | Script reads `templates/infographic-prompts/<type>.json` | Type slug passed as argument from agent |
| Script → Output | Script writes `{session}/images/INFOGRAPHIC_<type>.png` | Always writes a file (real or placeholder); never leaves path empty |
| Task A → Tasks B/C/D | File system — Task D reads from `{session}/images/` | Output path contract must be stable; placeholder ensures no downstream break |

## Build Order Implications

The migration creates a dependency chain that affects what gets built first:

1. **Config schema first** — Define the `Gemini API Key:` field syntax in `config.md` template and `config-context.md`. All other components depend on this format.

2. **Script skeleton second** — Build `scripts/generate_infographic.py` with config reading, template loading, and PNG writing logic. Test independently before wiring into the agent.

3. **API call integration third** — Wire `google-genai` call into the script. Test with a single infographic type using a real key before handling all six types.

4. **Error and retry handling fourth** — Add retry logic, finish_reason guards, placeholder generation. Test failure paths explicitly (bad key, content block, rate limit simulation).

5. **infographics.md update last** — Replace browser automation steps with the script invocation pattern. Update Task A spawn instruction in `agents/ceo.md` to remove browser references.

6. **Config template update alongside Step 1** — Update `templates/config-context.md` and `config/platform-configuration.md` references to add the API key field.

This order ensures the script works correctly in isolation before the agent instruction document depends on it.

## Sources

- Google Gen AI Python SDK (official): https://googleapis.github.io/python-genai/
- Gemini API image generation docs (official): https://ai.google.dev/gemini-api/docs/image-generation
- Gemini API troubleshooting guide (official): https://ai.google.dev/gemini-api/docs/troubleshooting
- google-generativeai deprecation notice: https://github.com/google-gemini/deprecated-generative-ai-python
- python-genai GitHub (official SDK): https://github.com/googleapis/python-genai
- finishReason blocking behavior: https://help.apiyi.com/en/gemini-api-image-blocked-finishreason-other-solution-en.html
- Image generation examples by example: https://geminibyexample.com/005-image-generation/

---
*Architecture research for: Gemini API image generation integration into Corporate Decision Panel*
*Researched: 2026-03-04*
