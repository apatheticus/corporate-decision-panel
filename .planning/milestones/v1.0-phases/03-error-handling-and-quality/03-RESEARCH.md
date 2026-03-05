# Phase 3: Error Handling and Quality - Research

**Researched:** 2026-03-04
**Domain:** API error handling, retry logic, vision-based quality validation, placeholder generation
**Confidence:** HIGH

## Summary

Phase 3 wraps the existing `generate_infographic()` function with retry logic for transient API errors, content-block detection for safety refusals, placeholder PNG generation on failure, and a Gemini vision-based quality validation pass. The project already uses `google-genai` v1.65.0 which has **built-in retry via tenacity** (exponential backoff + jitter, 5 attempts for 429/5xx errors). This means Phase 3 should NOT hand-roll low-level HTTP retry logic -- instead it should either disable the SDK's built-in retry (set attempts=1) and implement custom retry at the application layer for better control, or configure the SDK's retry options through `HttpOptions(retry_options=...)` and handle content/safety blocks separately. The application-layer approach is recommended because Phase 3 needs a shared retry budget that covers BOTH transient errors AND quality validation retries, which the SDK cannot coordinate.

The existing codebase returns `GenerationResult` dataclasses with `error_code` fields like `API_ERROR_{code}` for `ClientError` exceptions. Phase 3 extends this: classify errors as retryable (429, 503, 500, 502, 504, 408) vs. non-retryable (safety blocks via `finish_reason=SAFETY/IMAGE_SAFETY` or `prompt_feedback.block_reason`), wrap generation in an application-level retry loop, and add a vision validation step after each successful generation. The `google.genai.errors` module has three exception classes: `ClientError` (4xx), `ServerError` (5xx), and base `APIError` -- all with `.code`, `.status`, and `.message` attributes.

**Primary recommendation:** Disable SDK-level retry (set `HttpRetryOptions(attempts=1)`), implement application-level retry with exponential backoff + jitter (base 2s, max 30s), share the config `retry_limit` budget between transient errors and quality validation retries, and use `time.sleep()` for inter-call delay between sequential infographics.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- White PNG with centered error text identifying which infographic failed (e.g., "INFOGRAPHIC_domain-scorecard -- Generation Failed")
- Content/safety blocks use same placeholder but with different error text (e.g., "BLOCKED: content policy") to distinguish from transient failures
- Save prompt as both PROMPT.txt (human-readable) and PROMPT.json (machine-readable with metadata: error code, timestamp, type) for manual retry capability
- Session continues past individual failures -- one failure does not block remaining infographics
- Vision quality pass runs on all 6 infographic types (consistent quality gate)
- Validation checks: send generated image + list of expected data labels (extracted from data JSON) to Gemini vision model; verify labels are present and readable
- Does NOT verify structural correctness (grid layout, timeline ordering) -- only data label presence and readability
- Marginal readability (partially truncated labels) passes with warning, does not trigger retry
- On validation failure: re-generate with original prompt PLUS vision model's corrective feedback appended
- Shared budget: one configurable retry limit (from config.md `Retry Limit` field) covers both transient API errors (429/503) and quality validation retries
- Default 2 retries = 3 total attempts max per infographic
- Content/safety blocks do NOT retry -- immediate placeholder, no budget consumed
- Exponential backoff with jitter on 429/503 errors (base delay at Claude's discretion)
- Inter-call delay between sequential infographics in a session (configurable vs hardcoded at Claude's discretion)
- Adaptive inter-call delay: if a 429 occurs, double the inter-call delay for remaining images in the session
- Per-image structured status lines during generation (extending existing GENERATING/PROMPT/IMAGE/SAVED pattern)
- Final summary table after all 6 infographics: type, status (OK/FAILED/BLOCKED), attempts used, output path
- Summary shows overall validation result per image (OK with optional WARN flag, FAILED, BLOCKED) -- no per-label details in summary
- Exit code 0 if any infographic succeeded; exit 1 only on total session failure (all 6 failed)
- Warnings count as succeeded -- clean reporting model where only hard failures affect status

### Claude's Discretion
- Exponential backoff base delay (research Gemini's typical rate limit windows)
- Inter-call delay: whether hardcoded 3-5s or configurable in config.md
- Vision validation prompt construction (how to format the expected labels for the vision check)
- Where retry logic lives architecturally (wrapper around generate_infographic vs internal)
- Placeholder PNG dimensions and text styling
- Summary table formatting

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ERR-01 | Exponential backoff with jitter on 429/timeout errors | SDK has built-in retry via tenacity; disable it and implement app-level retry for budget control. Base delay 2s, exp_base 2, jitter via `random.uniform(0, 1)`. |
| ERR-02 | Distinguish content/safety blocks (no retry) from transient errors (retry) | Check `response.prompt_feedback.block_reason` for SAFETY/OTHER/IMAGE_SAFETY. Check `candidate.finish_reason` for SAFETY/IMAGE_SAFETY. `ClientError` with code 429 = retryable; `ServerError` (5xx) = retryable; content blocks = immediate placeholder. |
| ERR-03 | Placeholder PNG + saved prompt JSON on total failure | Use Pillow `Image.new("RGB", (1920, 1080), "white")` + `ImageDraw.text()` with `anchor="mm"`. Save PROMPT.json with `{error_code, timestamp, type, prompt_text}` alongside existing PROMPT.txt. |
| ERR-04 | Inter-call delay (3-5s) between sequential infographic generations | Hardcode 4s default with adaptive doubling on 429. Implemented at the session orchestration level (not inside generate_infographic). |
| QUAL-01 | After generation, send image back to Gemini vision with expected data labels | Use `client.models.generate_content()` with `[types.Part.from_bytes(png_bytes, "image/png"), validation_prompt]`. Use a text-only model (same model, text-only config) to verify labels. |
| QUAL-02 | If validation fails, retry generation with corrective feedback | Append vision model's feedback text to original prompt. Consumes from shared retry budget. |
| QUAL-03 | Configurable retry limit stored in config.md | Already implemented: `load_config()` returns `retry_limit` (default 2). Phase 3 consumes this value. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| google-genai | >=1.65.0 | Gemini API client (generation + vision validation) | Already installed; provides `ClientError`, `ServerError`, `HttpRetryOptions` |
| Pillow | >=10.0.0 | Placeholder PNG creation with text | Already installed; `Image`, `ImageDraw`, `ImageFont` |
| tenacity | (bundled) | Exponential backoff engine | Bundled inside google-genai; NOT used directly by our code |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| time | stdlib | `time.sleep()` for inter-call delay | Between sequential infographic generations |
| random | stdlib | Jitter calculation via `random.uniform()` | Added to backoff delay |
| json | stdlib | PROMPT.json serialization | Saving machine-readable prompt metadata |
| datetime | stdlib | Timestamp for PROMPT.json metadata | ISO 8601 timestamp on failure |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Custom retry loop | SDK built-in retry (HttpRetryOptions) | SDK retry handles transient HTTP errors but cannot coordinate shared budget with vision validation retries; custom loop needed |
| Custom retry loop | tenacity directly | Would add a new dependency; overkill for a simple counted loop with sleep |

**Installation:**
```bash
# No new packages needed -- all dependencies already installed
pip install google-genai>=1.65.0 Pillow>=10.0.0
```

## Architecture Patterns

### Recommended Project Structure
```
scripts/
    generate_infographic.py     # Existing -- extended with error classification
    session.py                  # NEW -- session orchestrator (6-image loop, inter-call delay, summary)
    validation.py               # NEW -- vision quality validation
    config.py                   # Existing -- already returns retry_limit
    preflight.py                # Existing -- unchanged
tests/
    test_generate_infographic.py  # Existing -- extended with retry/placeholder tests
    test_session.py               # NEW -- session orchestration tests
    test_validation.py            # NEW -- vision validation tests
    conftest.py                   # Existing -- extended with new fixtures
```

### Pattern 1: Application-Level Retry with Shared Budget
**What:** A retry loop OUTSIDE the SDK that tracks attempts across both transient errors and quality validation failures, sharing a single budget.
**When to use:** Always for this phase -- the user explicitly decided on shared budget.
**Example:**
```python
# Source: Project convention (GenerationResult pattern) + SDK error hierarchy
from google.genai.errors import ClientError, ServerError

def generate_with_retry(
    infographic_type: str,
    data_path: Path,
    output_path: Path,
    retry_limit: int = 2,
    config_dir: Path = Path(".cdp-context"),
) -> GenerationResult:
    """Generate with shared retry budget for transient errors + quality validation."""
    max_attempts = retry_limit + 1  # retry_limit=2 means 3 total attempts
    corrective_feedback: str | None = None

    for attempt in range(max_attempts):
        result = generate_infographic(
            infographic_type, data_path, output_path,
            skip_preflight=(attempt > 0),  # Only preflight on first attempt
            config_dir=config_dir,
            style_override_extra=corrective_feedback,
        )

        if not result.success:
            error_code = result.error_code or ""
            # Content/safety block -- do NOT retry
            if _is_content_block(error_code):
                return _handle_content_block(result, infographic_type, output_path)
            # Transient error -- retry with backoff
            if attempt < max_attempts - 1:
                _backoff(attempt)
                continue
            # Budget exhausted
            return _handle_total_failure(result, infographic_type, output_path)

        # Success -- run vision validation
        validation = validate_infographic(result.output_path, data_path, config_dir)
        if validation.passed or validation.warning_only:
            return result  # OK or OK+WARN
        # Validation failed -- retry with corrective feedback
        if attempt < max_attempts - 1:
            corrective_feedback = validation.feedback
            continue
        return result  # Budget exhausted but image exists

    return result  # Should not reach here
```

### Pattern 2: Error Classification
**What:** Classify API errors into retryable vs. non-retryable categories.
**When to use:** Inside the retry loop to decide whether to retry or produce placeholder.
**Example:**
```python
# Source: google.genai.errors module + types.py FinishReason/BlockedReason enums

RETRYABLE_CODES = {408, 429, 500, 502, 503, 504}
CONTENT_BLOCK_REASONS = {"SAFETY", "IMAGE_SAFETY", "OTHER", "PROHIBITED_CONTENT"}

def _is_retryable_error(error_code: str) -> bool:
    """Check if an API_ERROR_{code} is retryable."""
    if error_code.startswith("API_ERROR_"):
        try:
            code = int(error_code.split("_")[-1])
            return code in RETRYABLE_CODES
        except ValueError:
            pass
    return False

def _is_content_block(error_code: str) -> bool:
    """Check if the error represents a content/safety block."""
    return error_code in ("CONTENT_BLOCKED", "SAFETY_BLOCKED", "IMAGE_SAFETY_BLOCKED")
```

### Pattern 3: SDK Retry Disabled + App-Level Control
**What:** Disable the SDK's built-in retry by passing `HttpRetryOptions(attempts=1)` so the app fully controls retry timing and budget.
**When to use:** When creating the `genai.Client` for generation calls.
**Example:**
```python
# Source: google.genai types.py HttpRetryOptions, _api_client.py retry_args()
from google.genai import types

client = genai.Client(
    api_key=config["api_key"],
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(attempts=1),  # Disable SDK retry
    ),
)
```

### Pattern 4: Placeholder PNG Generation
**What:** Create a white PNG with centered error text using Pillow.
**When to use:** On total failure or content block.
**Example:**
```python
# Source: Pillow docs ImageDraw.text() with anchor="mm"
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_png(
    output_path: Path,
    error_text: str,
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """Create a white placeholder PNG with centered error text."""
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    # Use default font (no external font files needed)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except (OSError, IOError):
        font = ImageFont.load_default(size=36)
    draw.text(
        (width // 2, height // 2),
        error_text,
        fill=(128, 128, 128),  # Gray text on white
        font=font,
        anchor="mm",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path))
    return output_path
```

### Pattern 5: Vision Quality Validation
**What:** Send a generated PNG back to Gemini vision to verify expected data labels are present and readable.
**When to use:** After every successful image generation.
**Example:**
```python
# Source: ai.google.dev/gemini-api/docs/image-understanding
from google import genai
from google.genai import types

def validate_infographic(
    image_path: Path,
    data_path: Path,
    config_dir: Path,
) -> ValidationResult:
    """Validate that expected data labels are present in the generated infographic."""
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

    prompt = (
        "You are a quality checker for data infographics. "
        "Examine this infographic and verify that the following data labels "
        "are present and clearly readable:\n\n"
        + "\n".join(f"- {label}" for label in expected_labels)
        + "\n\nFor each label, report: FOUND (clearly readable), "
        "PARTIAL (present but truncated/hard to read), or MISSING.\n\n"
        "Then provide an overall verdict: PASS if all labels are FOUND or PARTIAL, "
        "FAIL if any label is MISSING.\n\n"
        "Format your response as:\n"
        "VERDICT: PASS|FAIL\n"
        "WARNINGS: [any PARTIAL labels, or 'none']\n"
        "MISSING: [any MISSING labels, or 'none']\n"
        "FEEDBACK: [if FAIL, specific guidance for regeneration]"
    )

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

    return _parse_validation_response(response.text)
```

### Anti-Patterns to Avoid
- **Relying on SDK built-in retry for budget control:** The SDK retries transient errors automatically but cannot track a shared budget with quality validation retries. Disable SDK retry and manage at app level.
- **Retrying content/safety blocks:** These are deterministic -- the same prompt will always be blocked. Immediate placeholder, no budget consumed.
- **Creating the genai.Client inside the retry loop:** Expensive and unnecessary. Create once, reuse across attempts.
- **Using os.system or subprocess for Pillow:** Pillow is already a dependency; use it directly.
- **Hardcoding font paths:** Use `ImageFont.load_default(size=N)` as fallback for cross-platform compatibility.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTTP retry with backoff | Custom urllib retry logic | Simple `time.sleep()` with calculated delay | SDK already handles HTTP transport; we just need application-level delay |
| PNG generation | Raw PNG byte manipulation | `Pillow Image.new() + ImageDraw` | Pillow handles format, compression, text rendering |
| JSON serialization | Manual string formatting | `json.dumps()` with indent | Handles escaping, encoding, formatting |
| Timestamp generation | Manual date formatting | `datetime.now(timezone.utc).isoformat()` | ISO 8601 standard |
| Vision model prompting | OCR library (Tesseract, etc.) | Gemini vision multimodal input | Already have the API key and client; no additional dependency needed |

**Key insight:** The SDK's built-in retry handles the HTTP-level concerns (connection errors, transport issues). Phase 3's retry operates at the APPLICATION level -- coordinating a shared budget between generation retries and validation retries, which no HTTP library can manage.

## Common Pitfalls

### Pitfall 1: SDK Double-Retry
**What goes wrong:** The SDK retries 429 errors automatically (up to 4 times). If the application ALSO retries, you get exponential explosion: 5 SDK attempts x 3 app attempts = 15 actual API calls when budget says 3.
**Why it happens:** Not realizing the SDK has built-in retry via tenacity.
**How to avoid:** Disable SDK retry with `HttpRetryOptions(attempts=1)` when creating the client.
**Warning signs:** API calls take much longer than expected; rate limit errors cascade.

### Pitfall 2: Content Block Misidentification
**What goes wrong:** A safety-blocked response does NOT raise a `ClientError`. Instead, the API returns a 200 OK with `prompt_feedback.block_reason = SAFETY` or a candidate with `finish_reason = SAFETY`. The current code catches `ClientError` but not content blocks.
**Why it happens:** Content filtering happens at the model level, not the HTTP level. The HTTP request succeeds; the model refuses to generate.
**How to avoid:** After a successful API call, check `response.prompt_feedback.block_reason` and `response.candidates[0].finish_reason` before looking for image data.
**Warning signs:** `NO_IMAGE_IN_RESPONSE` error code when the real cause is a safety block.

### Pitfall 3: Vision Validation Consuming Rate Limit
**What goes wrong:** Each validation call is another API request. For 6 infographics with validation, that is 12+ API calls (6 generate + 6 validate + retries). Rate limits apply to ALL calls combined.
**Why it happens:** Not accounting for validation calls in rate limit arithmetic.
**How to avoid:** Include inter-call delay before validation calls too, not just between generation calls. The 4s delay between infographics should apply between ALL API calls.

### Pitfall 4: Placeholder Overwriting Successful Output
**What goes wrong:** If validation fails after generation succeeded, the PNG exists but needs to be regenerated. The retry loop must re-generate, which means the original (bad) PNG gets overwritten.
**Why it happens:** The output_path is the same across retry attempts.
**How to avoid:** This is actually correct behavior -- overwriting the bad PNG with the retry attempt is desired.

### Pitfall 5: Adaptive Delay Not Persisting Across Images
**What goes wrong:** A 429 error on image 2 should double the inter-call delay for images 3-6, but if delay state is local to each image's retry loop, it resets.
**Why it happens:** Inter-call delay state must live at the SESSION level, not the per-image level.
**How to avoid:** Pass a mutable delay state object through the session loop, or use a session-level variable that gets doubled on 429.

### Pitfall 6: Font Not Available on All Platforms
**What goes wrong:** `ImageFont.truetype("Helvetica.ttc", 36)` fails on Linux/CI where Helvetica is not installed.
**Why it happens:** System fonts differ by OS.
**How to avoid:** Always fallback to `ImageFont.load_default(size=36)` which requires Pillow >= 10.4. Since we require Pillow >= 10.0.0, check availability and use load_default as primary strategy.

## Code Examples

Verified patterns from SDK source code and official documentation:

### Disabling SDK Retry
```python
# Source: .venv/.../google/genai/types.py HttpRetryOptions class
# Source: .venv/.../google/genai/_api_client.py retry_args() function
from google import genai
from google.genai import types

client = genai.Client(
    api_key="your-key",
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=1,  # 1 attempt = no retry
        ),
    ),
)
```

### Detecting Content Blocks in Response
```python
# Source: .venv/.../google/genai/types.py BlockedReason, FinishReason enums
# Must check AFTER a successful API call (200 OK)
response = client.models.generate_content(model=model_id, contents=prompt, config=gen_config)

# Check 1: Prompt-level block
if response.prompt_feedback and response.prompt_feedback.block_reason:
    reason = response.prompt_feedback.block_reason  # e.g., SAFETY, OTHER, IMAGE_SAFETY
    # This is a content block -- do NOT retry

# Check 2: Candidate-level finish reason
if response.candidates:
    finish = response.candidates[0].finish_reason
    if finish in ("SAFETY", "IMAGE_SAFETY", "PROHIBITED_CONTENT"):
        # Content blocked at generation level -- do NOT retry
```

### Exponential Backoff with Jitter
```python
# Source: Google Cloud retry strategy docs
import random
import time

def _backoff(attempt: int, base_delay: float = 2.0, max_delay: float = 30.0) -> float:
    """Sleep with exponential backoff + jitter. Returns actual delay."""
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0, delay * 0.5)  # Up to 50% jitter
    actual_delay = delay + jitter
    time.sleep(actual_delay)
    return actual_delay
```

### Sending Image to Gemini Vision for Validation
```python
# Source: ai.google.dev/gemini-api/docs/image-understanding
from google import genai
from google.genai import types

image_bytes = Path("infographic.png").read_bytes()
response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # Same model works for vision
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        "List all text labels visible in this infographic.",
    ],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT"],  # Text-only response for validation
    ),
)
print(response.text)
```

### Saving PROMPT.json with Metadata
```python
# Source: Project convention (extending existing save_prompt pattern)
import json
from datetime import datetime, timezone

def save_prompt_json(
    prompt: str,
    output_dir: Path,
    type_slug: str,
    error_code: str | None = None,
) -> Path:
    """Save machine-readable prompt with metadata for manual retry."""
    metadata = {
        "type": type_slug,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error_code": error_code,
        "prompt": prompt,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"INFOGRAPHIC_{type_slug}_PROMPT.json"
    path.write_text(json.dumps(metadata, indent=2))
    return path
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual HTTP retry with urllib | SDK built-in tenacity retry | google-genai 1.x (2025) | SDK auto-retries 429/5xx; app must disable to control budget |
| google.generativeai (old SDK) | google.genai (new SDK) | 2025 | Different error classes, Client pattern, types module |
| Separate vision model | Same model for generation + vision | Gemini 2.x+ (2025) | All Gemini models are multimodal; no separate vision model needed |
| `ImageFont.load_default()` (no size param) | `ImageFont.load_default(size=N)` | Pillow 10.4 (2024) | Can now create readable placeholder text without system fonts |

**Deprecated/outdated:**
- `google.generativeai` SDK: Replaced by `google.genai`; this project already uses the new SDK
- `genai.configure(api_key=...)` global pattern: Replaced by `genai.Client(api_key=...)`
- SDK retry respecting `retryDelay` header: [Open issue #1875](https://github.com/googleapis/python-genai/issues/1875), not yet fixed

## Discretion Recommendations

### Exponential Backoff Base Delay: 2 seconds
**Rationale:** Gemini rate limit windows for image generation vary by tier. Tier 1 allows ~10 IPM (images per minute), meaning one image every 6 seconds. A 2-second base with doubling (2s, 4s, 8s) provides reasonable spacing. The SDK's default is 1s base but that is for general API calls; image generation is heavier.

### Inter-Call Delay: Hardcoded 4 seconds, not configurable
**Rationale:** Making it configurable adds complexity to config.md for minimal user value. The 4s delay fits comfortably within the 6s/image budget at Tier 1 (10 IPM) and is well under the 3s/image budget at Tier 2 (20 IPM). The adaptive doubling on 429 provides dynamic adjustment. A hardcoded constant is simpler and sufficient.

### Vision Validation Prompt: Structured output format
**Rationale:** Use a structured prompt that requests VERDICT/WARNINGS/MISSING/FEEDBACK format (see Pattern 5 above). This makes parsing deterministic and provides the corrective feedback text that gets appended to the original prompt on retry.

### Retry Logic Architecture: Wrapper function around generate_infographic
**Rationale:** Keep `generate_infographic()` as-is (it is the unit of work). Create `generate_with_retry()` as a wrapper that manages the retry loop, and `run_session()` that orchestrates all 6 types with inter-call delays. This preserves the existing API contract and testability.

### Placeholder PNG Dimensions: 1920x1080 (16:9) or type-specific
**Rationale:** Use the same aspect ratio as the infographic type would have. For 4:3 types (domain-scorecard, risk-opportunity-matrix), use 1440x1080. For 16:9 types, use 1920x1080. This prevents layout breaks in downstream PPTX/HTML embedding.

### Summary Table Format: Tabular status lines
**Rationale:** Extend the existing `_status()` pattern with a SUMMARY stage:
```
SUMMARY -------
SUMMARY domain-scorecard          OK       1/3  images/INFOGRAPHIC_domain-scorecard.png
SUMMARY risk-opportunity-matrix   FAILED   3/3  images/INFOGRAPHIC_risk-opportunity-matrix.png
SUMMARY routing-diagram           BLOCKED  0/3  images/INFOGRAPHIC_routing-diagram.png
SUMMARY fault-line-map            OK+WARN  2/3  images/INFOGRAPHIC_fault-line-map.png
SUMMARY -------
```

## Open Questions

1. **Vision validation model choice**
   - What we know: All Gemini models are multimodal and can do vision analysis. The config already has `model_id`.
   - What's unclear: Whether the image generation model (e.g., `gemini-2.5-flash-image`) is also optimal for vision analysis, or whether a cheaper/faster model should be used for validation.
   - Recommendation: Use the same `model_id` from config for both generation and validation. This avoids introducing a second model config field. If the model cannot do text-only responses, fall back gracefully.

2. **Pillow load_default(size=N) availability**
   - What we know: `ImageFont.load_default(size=N)` was added in Pillow 10.4. The project requires Pillow >= 10.0.0.
   - What's unclear: Whether the installed Pillow version supports `size` parameter.
   - Recommendation: Bump minimum to Pillow >= 10.4.0 in requirements.txt, or use a try/except fallback.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest >= 8.0.0 |
| Config file | `pytest.ini` (defines `live` marker) |
| Quick run command | `python -m pytest tests/ -x -m "not live" -q` |
| Full suite command | `python -m pytest tests/ -x -m "not live" -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ERR-01 | 429/503 triggers exponential backoff, eventually succeeds or falls back | unit | `python -m pytest tests/test_generate_infographic.py::TestRetry -x` | Wave 0 |
| ERR-02 | SAFETY/OTHER content block produces immediate placeholder, no retry | unit | `python -m pytest tests/test_generate_infographic.py::TestContentBlock -x` | Wave 0 |
| ERR-03 | Total failure produces white placeholder PNG + PROMPT.json | unit | `python -m pytest tests/test_generate_infographic.py::TestPlaceholder -x` | Wave 0 |
| ERR-04 | Inter-call delay of 3-5s between sequential generations | unit | `python -m pytest tests/test_session.py::TestInterCallDelay -x` | Wave 0 |
| QUAL-01 | Vision pass verifies expected data labels are present | unit | `python -m pytest tests/test_validation.py::TestVisionValidation -x` | Wave 0 |
| QUAL-02 | Validation failure retries with corrective feedback | unit | `python -m pytest tests/test_generate_infographic.py::TestRetryWithFeedback -x` | Wave 0 |
| QUAL-03 | Retry limit read from config.md | unit | `python -m pytest tests/test_config.py -x` (already passes) | Exists |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/ -x -m "not live" -q`
- **Per wave merge:** `python -m pytest tests/ -x -m "not live" -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_session.py` -- covers ERR-04 (inter-call delay, adaptive delay, session summary)
- [ ] `tests/test_validation.py` -- covers QUAL-01 (vision validation parsing, expected label extraction)
- [ ] Extend `tests/conftest.py` -- fixtures for mock content-blocked responses, mock validation responses
- [ ] Extend `tests/test_generate_infographic.py` -- new test classes for retry, placeholder, content block scenarios

## Sources

### Primary (HIGH confidence)
- `google.genai.errors` module (v1.65.0) -- `ClientError`, `ServerError`, `APIError` class hierarchy with `.code`, `.status`, `.message` attributes
- `google.genai._api_client` (v1.65.0) -- Built-in retry via tenacity: 5 attempts, exp_base=2, initial_delay=1s, jitter=1, codes=(408, 429, 500, 502, 503, 504)
- `google.genai.types` (v1.65.0) -- `HttpRetryOptions(attempts=1)` to disable SDK retry; `BlockedReason` enum (SAFETY, OTHER, IMAGE_SAFETY, PROHIBITED_CONTENT); `FinishReason` enum (SAFETY, IMAGE_SAFETY)
- [Image understanding docs](https://ai.google.dev/gemini-api/docs/image-understanding) -- `types.Part.from_bytes()` for sending PNG to vision model
- [Google Cloud retry strategy](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/retry-strategy) -- Exponential backoff best practices, initial_delay=1.0, exp_base=2, jitter

### Secondary (MEDIUM confidence)
- [Rate limits docs](https://ai.google.dev/gemini-api/docs/rate-limits) -- IPM limits are tier-specific; Tier 1 approximately 10 IPM for image models
- [python-genai issue #1875](https://github.com/googleapis/python-genai/issues/1875) -- SDK does not respect server retryDelay header (still open)
- [Pillow ImageDraw docs](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html) -- `anchor="mm"` for centered text

### Tertiary (LOW confidence)
- Exact IPM values per tier -- Google frequently changes these; verify by checking actual rate limit headers in responses

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries already installed and verified in source
- Architecture: HIGH -- patterns derived from existing codebase conventions (GenerationResult, _status(), save_prompt())
- Pitfalls: HIGH -- SDK retry behavior verified by reading actual source code in .venv
- Error classification: HIGH -- enums and exception classes verified in installed SDK source
- Rate limits: MEDIUM -- exact IPM values are tier-specific and change frequently
- Vision validation: MEDIUM -- prompt construction is untested; structured output parsing needs validation

**Research date:** 2026-03-04
**Valid until:** 2026-03-18 (14 days -- SDK error handling is stable; rate limits may change)
