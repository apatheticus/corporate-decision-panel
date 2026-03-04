# Feature Research

**Domain:** Gemini API image generation — data visualization / infographic pipeline
**Researched:** 2026-03-04
**Confidence:** MEDIUM (official docs verified via WebFetch; model landscape is fast-moving and some specifics are preview/subject to change)

---

## Context: What This Research Is For

The CDP project is migrating from browser-based image generation (submitting JSON prompts to Gemini web UI) to direct Gemini API calls. The project generates six specific infographic types per decision session: Routing Diagram, Domain Scorecard, Fault-Line Map, Risk/Opportunity Matrix, Action Plan Timeline, and Mode Comparison. These are data-dense analytical visualizations, not artistic images.

The existing JSON prompt templates encode `{{PLACEHOLDER}}` tokens, color mappings, resolution/style directives, and quality constraints. The migration must preserve output fidelity while eliminating browser dependency.

---

## Feature Landscape

### Table Stakes (Migration Fails Without These)

These are capabilities the API must provide or the browser-to-API migration cannot succeed.

| Feature | Why Required | Complexity | Notes |
|---------|--------------|------------|-------|
| PNG output | Downstream embedding in PPTX/DOCX/HTML/PDF expects PNG | LOW | API returns base64 inline data; `mimeType: image/png` is supported. Extract via `part.inline_data.data`. |
| Minimum 2K resolution output | PROJECT.md requires 2000px minimum on longest edge. JSON templates specify "4k". | MEDIUM | `image_size: "2K"` param available on paid tiers. "4K" is Pro model + paid tier only. Free tier caps at 1024px. Must use paid API key. |
| Text rendering accuracy in images | Scorecards, timelines, fault-line maps all require legible labels, role names, domain names | HIGH | Gemini 3 Pro Image achieves ~94% text accuracy. Flash models lower. Long-form or dense label text is documented as a known weakness. This is the highest-risk capability. |
| Structured prompt acceptance | Existing templates are JSON objects with nested keys (`core`, `style`, `technical`, `extras`) | LOW | Gemini API accepts text prompts — JSON must be serialized to string and included in the text prompt. The API does NOT natively parse JSON as `generation_config`; JSON is just prompt text. |
| Base64 image extraction and file save | Pipeline must write PNG to `{session}/images/INFOGRAPHIC_<type-slug>.png` | LOW | Standard Python: `from io import BytesIO; from PIL import Image; Image.open(BytesIO(part.inline_data.data)).save(path)` |
| Error handling / retry on failure | Generation can fail (safety filter, API timeout, quota 429) | MEDIUM | Must catch `google.api_core.exceptions.ResourceExhausted` (429), implement exponential backoff. `tenacity` library pattern recommended. No complex budget tracking needed — API failures are transient. |
| API key auth (no browser session) | Core migration goal: remove login requirement | LOW | `genai.Client(api_key=KEY)` — key stored in `.cdp-context/config.md` per project convention. |

### Differentiators (Advantages Over Browser Approach)

Capabilities the API provides that the browser approach could not reliably deliver.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Deterministic invocation | No browser session, no login state, no UI changes breaking automation | LOW | Direct SDK call. Eliminates Claude Code fast-mode incompatibility entirely. |
| Aspect ratio control | API supports 14 aspect ratios (1:1 through 21:9) — browser UI did not expose this | LOW | `image_config.aspect_ratio` param. Infographics benefit from 4:3 or 16:9 depending on type. |
| Programmatic retry without budget tracking | API retries are cheap and simple; no need to count "3 per infographic, 12 per session" | LOW | Previous budget tracking was a workaround for browser unreliability. API retries can be unlimited with backoff. |
| Resolution param as a config knob | Can request 1K, 2K, or 4K via `image_size` — browser output was whatever the UI decided | MEDIUM | Must be on paid tier for 2K+. Param uses uppercase K: `"2K"` not `"2k"`. |
| Thinking mode for complex prompts | Pro model has built-in multi-step reasoning before generating | MEDIUM | Relevant for dense infographics like Fault-Line Map or Mode Comparison. Enable via `thinking_config.thinking_level: "High"`. Adds latency. |
| Interleaved text + image response | API can return a caption alongside the image in one call | LOW | Useful for logging generation rationale or debugging prompt adherence. Not used in current pipeline but zero-cost to capture. |
| No per-session login state | API key is static; no Gemini session expiry or forced re-login | LOW | Eliminates entire class of browser automation failure modes. |

### Anti-Features (Things the API Cannot Do That Browser Could, or Traps to Avoid)

| Feature | Why It Seems Useful | Why It Is Problematic / Unavailable | What to Do Instead |
|---------|---------------------|--------------------------------------|--------------------|
| Exact pixel-precise data rendering | Charts with exact numbers, precise bar heights, exact color fills at coordinates | The API is a generative model, not a charting library. It will approximate. Numbers in scorecards may be wrong or misplaced. | Pass data values as explicit labeled text in the prompt. Verify output visually. Accept that pixel-perfect accuracy requires a charting library (out of scope). |
| Requesting exact output dimensions in pixels | Specifying "2048x2048" or "1920x1080" exactly | API only accepts named sizes: `"512px"`, `"1K"`, `"2K"`, `"4K"`. No pixel-exact sizing. Aspect ratio + size tier determines final dimensions. | Use `image_size: "2K"` + `aspect_ratio: "4:3"` for closest match to existing output expectations. |
| Guaranteed exact color hex values | JSON templates specify hex codes (`"skeptic": "#C62828"`) | Generative models interpret color descriptions — hex codes in prompt text are hints, not pixel-level guarantees. Output may drift. | Include hex codes in prompt as explicit instructions. Accept approximate color fidelity. Do not rely on pixel-perfect color for downstream logic. |
| Parallel/concurrent generation | Generating all 6 infographics simultaneously | API enforces IPM (images per minute) limits. Free tier is ~5 RPM; paid tiers are higher but not unlimited. Concurrent calls risk 429 errors. | Serial generation with backoff. 6 sequential images at ~10-30s each is acceptable latency. Concurrent generation is explicitly out of scope per PROJECT.md. |
| Audio/video input for context | Providing session audio/video as additional context | API does not support audio or video inputs for image generation | Not relevant to this project — all context comes from Decision Record text. |
| ChatGPT/DALL-E as fallback | Multi-model fallback if Gemini fails | PROJECT.md explicitly excludes this. Also: adds integration complexity for marginal reliability gain. | Placeholder PNG + saved prompt on total failure (existing behavior, already implemented). |
| Browser UI style controls (negative prompts, sliders) | The Gemini web UI sometimes exposed additional controls | These are UI-only features not exposed in the API | Use `quality_keywords.avoid` list from existing JSON templates, serialized as text in the prompt. |

---

## Feature Dependencies

```
API key in .cdp-context/config.md
    └──required by──> genai.Client(api_key) instantiation
                          └──required by──> All generation calls

response_modalities: ['TEXT', 'IMAGE']
    └──required by──> Any image output (without this, API returns text only)

Paid API tier
    └──required by──> image_size: "2K" or "4K"
                          └──required by──> 2000px minimum output requirement

image_config.aspect_ratio
    └──enhances──> image_config.image_size (controls final pixel dimensions)

Exponential backoff retry
    └──required by──> Rate limit resilience (429 handling)
    └──enhances──> Simplified retry logic (replaces browser budget tracking)

Pillow (PIL) library
    └──required by──> Decoding base64 inline_data to PNG file

JSON prompt serialization
    └──required by──> Passing existing JSON template content as text prompt
    (JSON structure is prompt text, not API config — this is a critical distinction)
```

### Dependency Notes

- **Paid tier requires `image_size: "2K"`**: The PROJECT.md 2000px minimum cannot be met on the free tier. Free tier caps at 1024px. The paid Gemini API key must be confirmed before any resolution testing.
- **`response_modalities` is required**: Omitting this parameter causes the API to return text only with no image. This was confirmed as the most common implementation mistake (GitHub issue #568).
- **JSON prompt is text, not config**: The existing `templates/infographic-prompts/*.json` files must be serialized to a string and injected into the text prompt. They are NOT parsed as generation_config by the API. The prompt engineering effort is in formatting JSON content clearly for model comprehension.
- **Pillow is a new dependency**: The browser approach had no Python image processing. The API approach requires PIL/Pillow for base64-to-PNG conversion. Low risk, widely available.

---

## MVP Definition

### Launch With (v1 — Minimum Viable Migration)

These features are required for the migration to replace browser automation completely.

- [ ] `genai.Client` instantiation from API key in `.cdp-context/config.md` — without this, nothing works
- [ ] `response_modalities: ['TEXT', 'IMAGE']` in generation config — without this, no images are returned
- [ ] JSON template serialization to prompt text — reuses existing 6 JSON template files
- [ ] `image_size: "2K"` + appropriate aspect ratio — meets 2000px minimum requirement (requires paid tier)
- [ ] Base64 inline data extraction and PNG save to `{session}/images/INFOGRAPHIC_<type-slug>.png` — preserves existing output contract
- [ ] Exponential backoff retry on 429/timeout errors — replaces browser budget tracking with simpler pattern
- [ ] Placeholder PNG + saved prompt on total failure — existing behavior, must be preserved

### Add After Validation (v1.x)

- [ ] Thinking mode (`thinking_level: "High"`) for the two most complex infographic types (Fault-Line Map, Mode Comparison) — adds latency but may improve accuracy on dense content; validate that basic generation works first
- [ ] Aspect ratio optimization per infographic type — determine which of the 14 ratios best suits each of the 6 types (currently all templates use unspecified ratio)
- [ ] Capture and log text portion of interleaved response — useful for debugging prompt adherence without extra API calls

### Future Consideration (v2+)

- [ ] Imagen 4 as alternative model — Imagen 4 (`imagen-4.0-generate-001`) supports 1K/2K output and 5 aspect ratios; may produce different quality characteristics for certain infographic types. Defer until v1 quality is characterized.
- [ ] Concurrent generation with rate-limit awareness — IPM tracking to parallelize where quota allows. Out of scope per PROJECT.md.
- [ ] Per-infographic model selection — Pro model for text-heavy types, Flash for simpler ones. Cost optimization, not MVP.

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| API key auth + genai.Client setup | HIGH | LOW | P1 |
| response_modalities IMAGE output | HIGH | LOW | P1 |
| PNG extraction and file save | HIGH | LOW | P1 |
| JSON template as prompt text | HIGH | LOW | P1 |
| 2K resolution (paid tier) | HIGH | LOW (config param) | P1 |
| Exponential backoff retry | HIGH | LOW | P1 |
| Placeholder PNG on total failure | MEDIUM | LOW (existing logic) | P1 |
| Aspect ratio control per type | MEDIUM | LOW | P2 |
| Thinking mode for complex types | MEDIUM | MEDIUM (latency tradeoff) | P2 |
| Interleaved text response logging | LOW | LOW | P3 |
| Imagen 4 model alternative | LOW | MEDIUM | P3 |
| Concurrent generation | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for migration to succeed
- P2: Should have, add once basic pipeline works
- P3: Nice to have, future enhancement

---

## API Capability Summary (Verified)

This section records what was confirmed from official documentation for implementation reference.

### Model IDs (as of 2026-03-04)

| Model | ID | Best For | Resolution Support |
|-------|----|----------|-------------------|
| Nano Banana 2 (Flash) | `gemini-3.1-flash-image-preview` | Speed, volume, lower cost | 512px, 1K, 2K, 4K |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Text accuracy, complex prompts | 1K, 2K, 4K |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | Fast, cost-effective | Up to 1K on free tier |
| Imagen 4 | `imagen-4.0-generate-001` | Photorealistic, simple layout | 1K, 2K |

**Recommendation for CDP:** Start with `gemini-2.5-flash-image` for development/testing (lower cost), switch to `gemini-3-pro-image-preview` for production (superior text rendering accuracy matters for scorecards and fault-line maps).

### Generation Config Parameters (Confirmed)

```python
types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE'],   # REQUIRED for image output
    image_config=types.ImageConfig(
        aspect_ratio="4:3",    # or "16:9", "1:1", etc.
        image_size="2K"        # "512px", "1K", "2K", "4K" — UPPERCASE K required
    ),
    thinking_config=types.ThinkingConfig(   # optional, Pro model only
        thinking_level="High"
    )
)
```

### SDK Installation

```bash
pip install -U google-genai pillow
```

Note: `google-genai` is the new SDK (not the older `google-generativeai`). Official docs reference `from google import genai`. Keep updated — older SDK versions generate request formats the current API rejects.

### Rate Limits (MEDIUM confidence — varies by tier, changes frequently)

| Metric | Free Tier | Paid Tier |
|--------|-----------|-----------|
| RPM | ~5 RPM | Higher, tier-dependent |
| IPM | Separate image quota | Separate image quota |
| Daily limit | Yes (low) | Higher |

For CDP (5-6 images per session, sequential): free tier is adequate for development. Paid tier required for 2K resolution and production reliability.

---

## Known Limitations for Data Visualization

These are verified limitations that affect the CDP infographic types specifically.

| Limitation | Affected Infographic Types | Severity | Mitigation |
|------------|---------------------------|----------|------------|
| Text rendering inaccuracy at high label density | Domain Scorecard, Fault-Line Map | HIGH | Use Pro model. Keep label text short in prompts. Validate output. |
| No pixel-exact data rendering | All chart/matrix types | MEDIUM | Accept approximate. Data values are in the Decision Record; visual is reference aid, not primary source. |
| Color hex approximation | All (color mappings defined in JSON extras) | LOW | Include hex codes explicitly in prompt. Accept minor drift. |
| Long-form text rendering issues | Action Plan Timeline, Mode Comparison | MEDIUM | Break long text into bullet points in prompt. Avoid paragraph-length strings. |
| Free tier caps at 1024px | All — fails 2000px requirement | HIGH | Paid API key is non-optional for production use. |
| Aspect ratio stuck at 1:1 (known user-reported issue) | All | LOW | Explicitly set `aspect_ratio` param. Do not rely on prompt text alone to control ratio. |
| Model may not generate image on ambiguous prompt | All | LOW | Always include clear generation directive. Ensure `response_modalities` includes `'IMAGE'`. |

---

## Sources

- [Gemini API Image Generation — Official Docs](https://ai.google.dev/gemini-api/docs/image-generation) — HIGH confidence
- [Gemini API Models](https://ai.google.dev/gemini-api/docs/models) — HIGH confidence
- [Generate Images using Imagen — Official Docs](https://ai.google.dev/gemini-api/docs/imagen) — HIGH confidence
- [Gemini Image Generation Limitations — Vertex AI Docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/gemini-image-generation-limitations) — HIGH confidence
- [Gemini API Rate Limits — Official Docs](https://ai.google.dev/gemini-api/docs/rate-limits) — MEDIUM confidence (limits are tier-specific and change frequently; check AI Studio for current values)
- [Introducing Gemini 2.5 Flash Image — Google Developers Blog](https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/) — HIGH confidence
- [Generating Images with Gemini 2.0 Flash — DEV Community](https://dev.to/wescpy/generating-images-with-gemini-20-flash-from-google-448e) — MEDIUM confidence (community article, code patterns verified against official docs)
- [GitHub Issue #568 — response_modalities requirement](https://github.com/google-gemini/cookbook/issues/568) — HIGH confidence (confirms most common implementation mistake)
- [Gemini Image Generation Rate Limits 2026 — LaoZhang AI Blog](https://blog.laozhang.ai/en/posts/gemini-api-rate-limits-guide) — LOW confidence (third-party, use for orientation only)

---

*Feature research for: Gemini API image generation — CDP browser-to-API migration*
*Researched: 2026-03-04*
