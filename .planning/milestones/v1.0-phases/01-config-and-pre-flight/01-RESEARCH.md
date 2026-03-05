# Phase 1: Config and Pre-flight - Research

**Researched:** 2026-03-04
**Domain:** Gemini API configuration, key validation, markdown config parsing (Python)
**Confidence:** HIGH

## Summary

Phase 1 establishes the configuration and validation foundation for Gemini API image generation. The core work involves: (1) updating the markdown config template with API key, model ID, and retry limit fields, (2) writing a Python config parser for the existing `- **Field:** value` markdown format, (3) implementing a 4-step pre-flight validator that checks config presence, API key validity, billing/image-generation access, and model availability.

The critical SDK finding is that `google-generativeai` (referenced in PROJECT.md) was deprecated November 30, 2025. The replacement is `google-genai` (package `google-genai`, import as `from google import genai`). The CONTEXT.md default model `gemini-2.0-flash-exp` was shut down November 14, 2025. The current stable image generation model is `gemini-2.5-flash-image`; for preview/cutting-edge, `gemini-3.1-flash-image-preview` (Nano Banana 2, released February 26, 2026).

Pre-flight validation can be structured as: (1) parse config file, (2) instantiate `genai.Client(api_key=...)` and call `client.models.list()` to validate the key, (3) call `client.models.get(model=configured_model)` to verify model access, (4) attempt a minimal `generate_content` with `response_modalities=["IMAGE"]` to confirm billing/image-generation is enabled. The 4th step is essential because listing models succeeds on the free tier, but image generation requires billing.

**Primary recommendation:** Use `google-genai` SDK with `gemini-2.5-flash-image` as the default model. Structure as a `scripts/` package with `config.py` and `preflight.py` modules. Parse config with regex (no external markdown library needed). Pre-flight must attempt a real image generation probe to validate billing.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Config field format: placeholder-with-instructions `- **Gemini API Key:** (paste your key here)` with comment explaining where to get key; file is gitignored
- Default model ID: `gemini-2.0-flash-exp` **[RESEARCHER NOTE: This model was shut down 2025-11-14. Must use `gemini-2.5-flash-image` instead. Planner should flag this to user.]**
- Include retry limit field now with default value `- **Retry Limit:** (default: 2)` -- Phase 3 reads it
- Remove the Platform field entirely -- Gemini-only means no platform choice needed
- Pre-flight runs BOTH standalone (`python preflight.py` or equivalent) AND automatically before generation
- Validates four things in order: (1) config file parseable and required fields present, (2) API key validity, (3) billing / image generation enabled, (4) configured model ID accessible
- Hard stop with specific error on failure -- no infographics attempted, operator must fix config
- Python implementation (matches roadmap's `scripts/generate_infographic.py` naming)
- Dual audience error messages: readable by human operators AND parseable by AI agents (CEO agent)

### Claude's Discretion
- Module structure (flat scripts/ vs package with modules) -- pick what scales cleanly through all 4 phases
- Config parsing approach (regex vs markdown parser) -- pick simplest reliable approach
- Probe method for pre-flight validation (text-only call vs tiny image generation) -- pick most reliable approach that validates billing/image gen
- Exit code strategy (distinct per error type vs simple 0/1)
- Success message format (minimal single-line vs detailed multi-line report)
- Remediation detail level in error messages (include URLs or just describe the problem)
- Python dependency management format (requirements.txt vs pyproject.toml)

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SETUP-01 | API key stored in `.cdp-context/config.md` with clear field format | Config template update pattern documented; regex parsing approach verified against existing `- **Field:** value` format |
| SETUP-02 | Pre-flight validation probes API key and billing status before any generation | 4-step validation chain documented with SDK methods: `models.list()` for key validity, `models.get()` for model access, `generate_content()` probe for billing/image-gen |
| SETUP-03 | Model ID configurable in `.cdp-context/config.md` (not hardcoded) | Config parser extracts model ID; `client.models.get()` validates it exists; default model corrected to `gemini-2.5-flash-image` |
| DOC-02 | Update `templates/config-context.md` template with API key, model ID, and retry limit fields | Current template structure documented; Platform field removal and new field additions specified |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `google-genai` | 1.65.0+ | Gemini API client (unified SDK) | Official Google SDK; replaces deprecated `google-generativeai`; supports image generation, model listing, all Gemini features |
| Python | 3.10+ | Runtime | `google-genai` requires >=3.10; project has 3.14.3 available |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `Pillow` | latest | Image handling (PIL) | Saving generated images from API response `part.as_image()` |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `google-genai` | `google-generativeai` | **Do not use** -- deprecated Nov 30, 2025; EOL; no new features |
| regex config parsing | `python-markdown` / `mistletoe` | Overkill -- config format is 3 simple key-value lines; regex is more reliable for this specific `- **Key:** value` pattern |
| `requirements.txt` | `pyproject.toml` | pyproject.toml is more modern but this project has zero Python packaging; a flat `requirements.txt` in the project root is simpler and sufficient |

**Installation:**
```bash
pip install google-genai Pillow
```

Or with a requirements file:
```
google-genai>=1.65.0
Pillow>=10.0.0
```

## Architecture Patterns

### Recommended Project Structure
```
scripts/
    __init__.py          # Makes scripts/ a package (enables imports across phases)
    config.py            # Config parsing from .cdp-context/config.md
    preflight.py         # Pre-flight validation (standalone + importable)
    generate_infographic.py  # Phase 2 will add this
templates/
    config-context.md    # Updated template (this phase modifies)
requirements.txt         # Python dependencies
```

**Rationale for package structure:** Phase 2 needs `generate_infographic.py` to import `config.py`. Phase 3 adds retry logic that imports from both. A flat `scripts/` package with `__init__.py` enables this cleanly without sys.path hacks.

### Pattern 1: Markdown Config Parsing with Regex
**What:** Parse `- **Field Name:** value` format from markdown files using a single regex pattern
**When to use:** Reading `.cdp-context/config.md` fields
**Example:**
```python
import re
from pathlib import Path

# Pattern matches: - **Field Name:** value
# Captures field name and value, strips whitespace
FIELD_PATTERN = re.compile(
    r'^-\s+\*\*(.+?):\*\*\s*(.*)$',
    re.MULTILINE
)

def parse_config(config_path: Path) -> dict[str, str]:
    """Parse markdown config file into field dict.

    Returns dict mapping lowercase field names to values.
    Parenthetical defaults like '(default: 2)' are parsed
    to extract the default when no user value is provided.
    """
    text = config_path.read_text()
    fields = {}
    for match in FIELD_PATTERN.finditer(text):
        key = match.group(1).strip().lower()
        value = match.group(2).strip()
        fields[key] = value
    return fields
```

### Pattern 2: Pre-flight Validation Chain
**What:** Sequential validation with early exit and specific error messages
**When to use:** Before any API calls in generation pipeline
**Example:**
```python
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

def run_preflight(config: dict) -> None:
    """Run pre-flight checks. Raises SystemExit on failure."""

    # Step 1: Config completeness
    api_key = config.get("gemini api key", "").strip()
    if not api_key or api_key.startswith("("):
        _fail("CONFIG_MISSING_KEY",
              "Gemini API Key not set in .cdp-context/config.md",
              "Get a key from https://aistudio.google.com/apikey")

    model_id = config.get("image model", "gemini-2.5-flash-image").strip()
    if not model_id or model_id.startswith("("):
        model_id = "gemini-2.5-flash-image"

    # Step 2: API key validity
    client = genai.Client(api_key=api_key)
    try:
        list(client.models.list())  # Force evaluation
    except ClientError as e:
        if e.code == 400 or e.code == 403:
            _fail("INVALID_API_KEY",
                  "Gemini API key is invalid or unauthorized",
                  "Verify key at https://aistudio.google.com/apikey")
        raise

    # Step 3: Model accessibility
    try:
        client.models.get(model=model_id)
    except ClientError as e:
        if e.code == 404:
            _fail("MODEL_NOT_FOUND",
                  f"Model '{model_id}' not found or not accessible",
                  "Check available models at https://ai.google.dev/gemini-api/docs/models")
        raise

    # Step 4: Image generation / billing probe
    try:
        response = client.models.generate_content(
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
            _fail("BILLING_NOT_ENABLED",
                  "Image generation requires billing to be enabled",
                  "Enable billing at https://aistudio.google.com/apikey "
                  "(check Quota tier column shows Tier 1+)")
        if e.code == 429:
            _fail("RATE_LIMITED",
                  "API rate limit hit during pre-flight probe",
                  "Wait a moment and try again")
        raise
```

### Pattern 3: Dual-Audience Error Messages
**What:** Error output format readable by both humans and AI agents
**When to use:** All pre-flight failure messages
**Example:**
```python
def _fail(error_code: str, message: str, remediation: str) -> None:
    """Print structured error and exit.

    Format is parseable by AI agents (CEO) via the error_code
    and readable by human operators via the message + fix.
    """
    print(f"PREFLIGHT FAILED [{error_code}]")
    print(f"  Error: {message}")
    print(f"  Fix: {remediation}")
    sys.exit(1)
```

### Anti-Patterns to Avoid
- **Importing `google.generativeai`:** This is the deprecated package. Always use `from google import genai` (the `google-genai` package).
- **Hardcoding the model ID:** The model must come from config. Models get deprecated; `gemini-2.0-flash-exp` was shut down Nov 14, 2025.
- **Validating only the API key:** A valid key does not mean billing is enabled. Image generation requires billing; you must probe with `response_modalities=["IMAGE"]` to confirm.
- **Silent failure on config parse:** If `config.md` is missing or fields cannot be parsed, fail loudly with the specific problem and file path.
- **Using `genai.configure()`:** This is the deprecated API pattern. The new SDK uses `client = genai.Client(api_key=...)`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Gemini API HTTP calls | Raw `requests`/`httpx` calls | `google-genai` SDK | SDK handles auth, retries, response parsing, error types |
| API key validation | Custom HTTP probe to REST endpoint | `client.models.list()` | SDK raises `ClientError` with proper codes for invalid keys |
| Model existence check | String matching against hardcoded list | `client.models.get(model=id)` | Model list changes frequently; runtime check is authoritative |
| Image response decoding | Manual base64 decode of response data | `part.as_image()` (returns PIL Image) | SDK handles encoding, content type detection |

**Key insight:** The `google-genai` SDK provides typed errors (`ClientError` with `.code` and `.message`) that map directly to the error conditions pre-flight needs to detect. Building custom HTTP validation would duplicate this and miss edge cases.

## Common Pitfalls

### Pitfall 1: Using the Deprecated SDK
**What goes wrong:** Import errors, missing features, no image generation support
**Why it happens:** PROJECT.md references `google-generativeai` which was the standard before Nov 2025
**How to avoid:** Install `google-genai`, import as `from google import genai`
**Warning signs:** `import google.generativeai as genai` or `genai.configure()` in code

### Pitfall 2: Default Model is Deprecated
**What goes wrong:** `gemini-2.0-flash-exp` returns 404 or "model not found" errors
**Why it happens:** CONTEXT.md specifies this as the default, but it was shut down Nov 14, 2025
**How to avoid:** Use `gemini-2.5-flash-image` as default. This is the current stable image-generation model.
**Warning signs:** 404 errors when calling `generate_content` or `models.get`

### Pitfall 3: Assuming Valid Key Means Image Generation Works
**What goes wrong:** Key validates fine, but image generation returns 403 PERMISSION_DENIED
**Why it happens:** Free tier may allow text generation but restrict image generation (0 IPM on some models, or free-tier image gen is limited to specific models)
**How to avoid:** Pre-flight step 4 must actually attempt image generation, not just text
**Warning signs:** Pre-flight passes but first real infographic generation fails with 403

### Pitfall 4: Config Regex Doesn't Handle Parenthetical Defaults
**What goes wrong:** Parser returns `"(paste your key here)"` as the API key value
**Why it happens:** Unfilled placeholder fields contain parenthetical instruction text
**How to avoid:** Check if value starts with `(` and treat as empty/default; parse `(default: X)` patterns to extract the default value
**Warning signs:** Pre-flight tries to authenticate with `"(paste your key here)"` as the API key

### Pitfall 5: Probe Image Generation Costs Real Money
**What goes wrong:** Each pre-flight run incurs billing charges
**Why it happens:** Image generation probe creates a real image
**How to avoid:** Use smallest possible probe: `image_size="512px"`, `aspect_ratio="1:1"`, simple prompt. Cost per probe is negligible (~$0.03) but be aware it is non-zero.
**Warning signs:** Unexpected billing if pre-flight runs frequently in automation

### Pitfall 6: Python 3.14 Compatibility
**What goes wrong:** Some packages may not yet fully support Python 3.14.3
**Why it happens:** Python 3.14 is very new (released 2025)
**How to avoid:** google-genai 1.65.0 lists Python 3.10-3.14 support. Verify Pillow compatibility. Consider documenting Python >=3.10 as the requirement.
**Warning signs:** Build/install failures on the host system

## Code Examples

Verified patterns from official sources:

### Client Initialization
```python
# Source: https://googleapis.github.io/python-genai/
from google import genai
from google.genai import types

# Explicit API key (for config-file-based key storage)
client = genai.Client(api_key="YOUR_API_KEY")

# Or via environment variable GEMINI_API_KEY
client = genai.Client()
```

### Listing Models (Key Validation)
```python
# Source: https://ai.google.dev/gemini-api/docs/libraries
# If key is invalid, raises ClientError with code 400 or 403
for model in client.models.list():
    print(model.name)
```

### Getting a Specific Model
```python
# Source: https://googleapis.github.io/python-genai/
# Raises ClientError(404) if model doesn't exist
model_info = client.models.get(model="gemini-2.5-flash-image")
print(model_info.name, model_info.supported_actions)
```

### Image Generation with Config
```python
# Source: https://ai.google.dev/gemini-api/docs/image-generation
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Generate a simple test image",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="2K",
        ),
    ),
)

# Process response
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()  # Returns PIL.Image
        image.save("output.png")
    elif part.text is not None:
        print(part.text)
```

### Error Handling
```python
# Source: https://github.com/googleapis/python-genai/blob/main/google/genai/errors.py
from google.genai.errors import ClientError, ServerError, APIError

try:
    response = client.models.generate_content(...)
except ClientError as e:
    # 4xx errors: invalid key (400/403), not found (404), rate limit (429)
    print(f"Client error {e.code}: {e.message}")
except ServerError as e:
    # 5xx errors: service unavailable (503), internal error (500)
    print(f"Server error {e.code}: {e.message}")
except APIError as e:
    # Catch-all for other API errors
    print(f"API error {e.code}: {e.message}")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `google-generativeai` SDK | `google-genai` SDK | Nov 30, 2025 EOL | Must use new import pattern `from google import genai` |
| `genai.configure(api_key=...)` | `client = genai.Client(api_key=...)` | With new SDK | Client-based, not module-level configuration |
| `gemini-2.0-flash-exp` for images | `gemini-2.5-flash-image` (stable) | Nov 14, 2025 shutdown | Default model in config must change |
| Browser automation for images | `generate_content(response_modalities=["IMAGE"])` | Gemini 2.0+ era | Core migration this project implements |
| `genai.GenerativeModel()` | `client.models.generate_content()` | With new SDK | No model object; call methods directly on `client.models` |

**Deprecated/outdated:**
- `google-generativeai` package: Fully deprecated, EOL Nov 30 2025. Do not install.
- `gemini-2.0-flash-exp`: Shut down Nov 14 2025. Not usable.
- `gemini-2.0-flash-preview-image-generation`: Shut down Nov 14 2025.
- `imagen-3.0-generate-002`: Shut down Nov 10 2025.
- `imagen-4.0-*` variants: Scheduled shutdown June 24 2026; recommended replacement is `gemini-2.5-flash-image` or `gemini-3-pro-image-preview`.

**Current image generation models (as of March 2026):**

| Model ID | Status | Notes |
|----------|--------|-------|
| `gemini-2.5-flash-image` | Stable | Recommended default; best balance of speed/quality/stability |
| `gemini-3.1-flash-image-preview` | Preview | Newest (Feb 2026); faster, cheaper (~50% less); adds 512px resolution |
| `gemini-3-pro-image-preview` | Preview | Highest fidelity; best for text-heavy infographics |

## Open Questions

1. **Default model correction**
   - What we know: CONTEXT.md locked `gemini-2.0-flash-exp` as default, but this model is shut down
   - What's unclear: Whether user is aware of the deprecation
   - Recommendation: Planner should use `gemini-2.5-flash-image` as the default and document the change. The config template comment should note current available models.

2. **Billing probe cost and approach**
   - What we know: Image generation probe at 512px costs ~$0.03. Text-only probe would not validate billing/image-gen access.
   - What's unclear: Whether a `models.get()` check on an image model is sufficient to confirm billing, or whether an actual image generation call is needed
   - Recommendation: Use the image generation probe. The cost is negligible and it is the only way to confirm the full pipeline works (key valid + billing enabled + model accessible + image gen permitted).

3. **Free tier image generation access**
   - What we know: As of Feb 2026, `gemini-2.5-flash-image` has a free tier of ~500 RPD / 2 IPM. Newer models like `gemini-3-pro-image-preview` have no free tier.
   - What's unclear: Whether free-tier access is sufficient for the CDP use case (6 images per session, infrequent use)
   - Recommendation: Pre-flight should detect free-tier usage (may work for `gemini-2.5-flash-image`) vs billing-required models and message accordingly. The pre-flight error for billing should include specific mention of checking the Quota tier column in AI Studio.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (standard Python testing) |
| Config file | none -- see Wave 0 |
| Quick run command | `python -m pytest tests/ -x -q` |
| Full suite command | `python -m pytest tests/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SETUP-01 | Config parser reads API key, model ID, retry limit from `.cdp-context/config.md` | unit | `python -m pytest tests/test_config.py -x` | Wave 0 |
| SETUP-01 | Missing or empty fields produce clear errors | unit | `python -m pytest tests/test_config.py::test_missing_fields -x` | Wave 0 |
| SETUP-02 | Pre-flight validates API key (invalid key produces specific error) | unit (mocked) | `python -m pytest tests/test_preflight.py::test_invalid_key -x` | Wave 0 |
| SETUP-02 | Pre-flight validates billing (403 on image gen produces billing error) | unit (mocked) | `python -m pytest tests/test_preflight.py::test_billing_not_enabled -x` | Wave 0 |
| SETUP-03 | Model ID from config is used in API calls; invalid model produces error | unit (mocked) | `python -m pytest tests/test_preflight.py::test_invalid_model -x` | Wave 0 |
| DOC-02 | Config template has all required fields and correct format | unit | `python -m pytest tests/test_config.py::test_template_fields -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/ -x -q`
- **Per wave merge:** `python -m pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/__init__.py` -- package init
- [ ] `tests/test_config.py` -- covers SETUP-01, SETUP-03, DOC-02
- [ ] `tests/test_preflight.py` -- covers SETUP-02 (with mocked API calls)
- [ ] `tests/conftest.py` -- shared fixtures (temp config files, mock client)
- [ ] Framework install: `pip install pytest` -- no test framework exists yet
- [ ] `requirements.txt` or `requirements-dev.txt` -- pytest dependency

## Sources

### Primary (HIGH confidence)
- [Google Gen AI SDK docs](https://googleapis.github.io/python-genai/) -- client initialization, API patterns
- [Gemini image generation docs](https://ai.google.dev/gemini-api/docs/image-generation) -- response_modalities, image_config, supported models, code examples
- [Gemini models page](https://ai.google.dev/gemini-api/docs/models) -- current model IDs and capabilities
- [Gemini deprecations page](https://ai.google.dev/gemini-api/docs/deprecations) -- model shutdown dates
- [google-genai errors.py](https://github.com/googleapis/python-genai/blob/main/google/genai/errors.py) -- exception hierarchy: APIError > ClientError/ServerError
- [google-genai on PyPI](https://pypi.org/project/google-genai/) -- version 1.65.0, Python >=3.10

### Secondary (MEDIUM confidence)
- [Gemini billing docs](https://ai.google.dev/gemini-api/docs/billing) -- tier system, how to check billing status
- [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) -- IPM concept for image models
- [deprecated-generative-ai-python repo](https://github.com/google-gemini/deprecated-generative-ai-python) -- confirms deprecation status

### Tertiary (LOW confidence)
- [Third-party blog on Nano Banana 2](https://almcorp.com/blog/google-nano-banana-2-gemini-31-flash-image-complete-guide/) -- pricing comparison ($0.067 vs $0.134 per 2K image)
- [Third-party blog on free tier limits](https://blog.laozhang.ai/en/posts/gemini-image-generation-free-limit-2026) -- 500 RPD / 2 IPM free tier for gemini-2.5-flash-image (needs validation)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- official SDK docs, PyPI verified, deprecation confirmed via official repo
- Architecture: HIGH -- patterns follow SDK examples directly; project structure informed by existing codebase
- Pitfalls: HIGH -- deprecated SDK/model confirmed via official sources; billing requirement confirmed via official docs
- Config parsing: HIGH -- existing config format is visible in templates/config-context.md; regex approach is straightforward
- Image generation probe: MEDIUM -- probe approach is logical but exact error codes for billing-not-enabled vs other 403s not documented officially

**Research date:** 2026-03-04
**Valid until:** 2026-04-04 (stable SDK and model landscape; 30-day window appropriate)
