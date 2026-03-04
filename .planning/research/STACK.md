# Stack Research

**Domain:** Gemini API image generation via Python SDK
**Researched:** 2026-03-04
**Confidence:** HIGH (official docs + PyPI + Google Developers Blog verified)

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| `google-genai` | `>=1.65.0` (current: 1.65.0) | Gemini API client — image generation + auth | Official GA SDK as of May 2025. The old `google-generativeai` package is deprecated as of November 30, 2025. Only `google-genai` supports current image generation models and is actively maintained. |
| `gemini-2.5-flash-image` | Stable (GA: Oct 2, 2025) | Image generation model | The only GA (non-preview) Gemini native image model. Supports `generate_content()` with IMAGE response modality, accepts structured text prompts, outputs at 1K/2K/4K resolution with configurable aspect ratios. Better fit than Imagen 4 for analytical infographics because it integrates reasoning into visual generation. |
| `Pillow` | `>=11.0.0` | Convert raw bytes from API response to PNG file on disk | The `google-genai` SDK returns image data as `inline_data.data` (raw bytes). Pillow's `Image.open(BytesIO(...))` + `.save("file.png")` is the standard pattern for writing PNG files. No alternative for this step. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `io.BytesIO` | stdlib | Wrap raw image bytes for Pillow consumption | Always — Pillow cannot open raw bytes directly, requires a file-like object |
| `pathlib.Path` | stdlib | Build output paths (`{session}/images/INFOGRAPHIC_<slug>.png`) | Always — already used throughout CDP codebase; consistent with `install.py` patterns |
| `re` or string operations | stdlib | Parse API key from `.cdp-context/config.md` Markdown format | When reading the key from the CDP config file rather than an env var |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Google AI Studio | Obtain API key, test prompts interactively | API key is created at `aistudio.google.com/apikey`. Studio also has rate-limit dashboards. |
| Gemini API pricing page | Monitor per-image cost | Image generation requires paid tier (billing enabled). Gemini 2.5 Flash Image: $0.039/image. |

---

## Installation

```bash
# Core SDK (replaces deprecated google-generativeai)
pip install "google-genai>=1.65.0"

# Image processing
pip install "Pillow>=11.0.0"
```

Or with uv (faster):

```bash
uv pip install "google-genai>=1.65.0" "Pillow>=11.0.0"
```

**No requirements.txt changes to the CDP repo itself** — these are runtime dependencies invoked by Claude Code's Python environment, not packaged into CDP.

---

## How the API Actually Works

### Method: `generate_content()` with IMAGE modality

This is the correct method for `gemini-2.5-flash-image`. Do NOT use `generate_images()` for this model — that method is for Imagen 4 only.

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import pathlib

# API key read from .cdp-context/config.md (parse the Markdown field)
client = genai.Client(api_key="YOUR_API_KEY_FROM_CONFIG")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=populated_json_prompt_as_string,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="4:3",   # landscape infographics
            image_size="2K",      # 2000px+ on longest edge, satisfies CDP requirement
        ),
    ),
)

# Extract and save PNG
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        output_path = pathlib.Path(session_output) / "images" / f"INFOGRAPHIC_{slug}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(str(output_path), format="PNG")
```

### Resolution

`image_size="2K"` satisfies CDP's "2000px minimum on longest edge" requirement. Supported sizes: `"1K"` (default), `"2K"`, `"4K"`. Use `"2K"` — `"4K"` increases latency and cost with marginal gain for print/embed use cases.

### Aspect Ratios Available (gemini-2.5-flash-image)

`"1:1"`, `"2:3"`, `"3:2"`, `"3:4"`, `"4:3"`, `"4:5"`, `"5:4"`, `"9:16"`, `"16:9"`, `"21:9"`

For infographics: `"4:3"` suits most matrix/timeline layouts; `"16:9"` suits wide diagrams (routing, fault-line).

---

## Alternatives Considered

| Recommended | Alternative | Why Not |
|-------------|-------------|---------|
| `gemini-2.5-flash-image` | `imagen-4.0-generate-001` (Imagen 4 Standard) | Imagen 4 uses `generate_images()` method (separate API surface), has no reasoning integration, and costs $0.04/image vs $0.039. Imagen 4 Ultra is $0.06/image. For analytical infographics that require understanding structured JSON prompts, Gemini's reasoning-backed image generation is materially better. |
| `gemini-2.5-flash-image` | `gemini-3.1-flash-image-preview` | The 3.1 model is Preview status only (as of March 2026). Not suitable for production. Use stable `gemini-2.5-flash-image` unless the 3.1 model reaches GA before implementation. |
| `gemini-2.5-flash-image` | `gemini-3-pro-image-preview` | Also Preview-only. Higher capability but preview APIs have no stability guarantees. Revisit post-GA. |
| `google-genai` | `google-generativeai` | Deprecated November 30, 2025. Does not support current image generation models. Will receive no updates. **Do not use.** |
| Pillow | OpenCV | OpenCV is overkill for simple byte-to-PNG conversion. Pillow is the standard, zero-configuration option. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `google-generativeai` | Deprecated November 30, 2025. Not actively maintained. Does not support `gemini-2.5-flash-image` or Imagen 4. | `google-genai>=1.65.0` |
| `generate_images()` with `gemini-2.5-flash-image` | `generate_images()` is the Imagen-family method. Calling it with a Gemini model will fail. | `generate_content()` with `response_modalities=["IMAGE"]` |
| `GOOGLE_API_KEY` environment variable | CDP stores config in `.cdp-context/config.md`, not env vars. Forcing env vars breaks CDP's configuration convention. | Read key from config file, pass to `genai.Client(api_key=...)` |
| Free-tier API key for image generation | Image generation is NOT available on the Gemini API free tier. Requests will return quota errors. The user MUST enable billing. | Paid tier (billing enabled in Google AI Studio) |
| `image_size="1K"` for infographics | 1K images will be below CDP's 2000px minimum. | `image_size="2K"` |
| Gemini 2.0 Flash Experimental (`gemini-2.0-flash-exp-image-generation`) | Experimental model, no longer the current recommendation. Docs now point to `gemini-2.5-flash-image`. | `gemini-2.5-flash-image` |

---

## Stack Patterns by Variant

**If infographic is a wide layout (routing diagram, fault-line map):**
- Use `aspect_ratio="16:9"` or `"4:3"` in `ImageConfig`

**If infographic is a tall layout (scorecard, risk matrix):**
- Use `aspect_ratio="3:4"` or `"1:1"` in `ImageConfig`

**If ALL attempts fail (placeholder path):**
- Generate placeholder PNG using only Pillow — no API call needed
- `Image.new("RGB", (2000, 1500), color="white")` + `ImageDraw` for centered text
- This keeps the fallback entirely stdlib + Pillow with no external dependencies

**If API key is missing or blank in config:**
- Skip API call, write placeholder immediately, log the error
- Do not raise exceptions that block Tasks B/C/D

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| `google-genai>=1.65.0` | Python `>=3.10` | Requires Python 3.10+. Claude Code's default Python is 3.10+. |
| `Pillow>=11.0.0` | Python `>=3.9` | No conflict with google-genai. |
| `gemini-2.5-flash-image` model | `google-genai>=1.0.0` | Model became GA in October 2025; use latest SDK to ensure `ImageConfig` parameters are available. |

---

## Billing Requirement (Important)

Image generation via the Gemini API is **not available on the free tier**. The user must:

1. Enable billing in Google Cloud / Google AI Studio
2. Create a paid API key at `aistudio.google.com/apikey`
3. Add the key to `.cdp-context/config.md`

Cost per CDP session: 5-6 infographics × $0.039 = **~$0.20–$0.23 per full session**. Negligible for production use; important to document in user-facing setup instructions.

---

## Sources

- [Gemini API: Generate images (official docs)](https://ai.google.dev/gemini-api/docs/image-generation) — Model IDs, `generate_content()` with IMAGE modality, `ImageConfig` parameters (HIGH confidence)
- [Gemini API: Generate images using Imagen (official docs)](https://ai.google.dev/gemini-api/docs/imagen) — `generate_images()` method, Imagen 4 model IDs, resolution parameters (HIGH confidence)
- [google-genai on PyPI](https://pypi.org/project/google-genai/) — Version 1.65.0 confirmed current as of 2026-02-26 (HIGH confidence)
- [Gemini API Libraries (official)](https://ai.google.dev/gemini-api/docs/libraries) — `google-generativeai` deprecated November 30, 2025; `google-genai` is current GA SDK (HIGH confidence)
- [Gemini 2.5 Flash Image GA announcement](https://developers.googleblog.com/en/gemini-2-5-flash-image-now-ready-for-production-with-new-aspect-ratios/) — GA date October 2, 2025; aspect ratio list; pricing $0.039/image (HIGH confidence)
- [Gemini API Pricing (official)](https://ai.google.dev/gemini-api/docs/pricing) — Image generation requires paid tier, no free tier (HIGH confidence)
- [Google Gen AI SDK docs](https://googleapis.github.io/python-genai/) — `generate_images()` vs `generate_content()` method separation (MEDIUM confidence — site scraped March 2026)
- [Imagen 4 GA announcement](https://developers.googleblog.com/en/imagen-4-now-available-in-the-gemini-api-and-google-ai-studio/) — Imagen 4 model IDs, paid-only (HIGH confidence)

---

*Stack research for: Gemini API image generation (CDP Browser-to-API Migration)*
*Researched: 2026-03-04*
