# Pitfalls Research

**Domain:** Gemini API image generation — migration from browser automation
**Researched:** 2026-03-04
**Confidence:** MEDIUM-HIGH (official docs verified; some rate limit specifics from community sources)

---

## Critical Pitfalls

### Pitfall 1: Billing Not Enabled — Silent or Confusing API Failures

**What goes wrong:**
The Gemini API image generation models have zero free-tier IPM (Images Per Minute). A free-tier API key silently returns 403 or 429 errors the moment an image generation call is made — not on text calls. The error message does not always make clear that billing activation is the blocker. Developers waste hours debugging SDK configuration, model name, or prompt format when the actual issue is that the account has no billing enabled.

**Why it happens:**
The Gemini API supports text generation on the free tier, so a working API key for text creates the false expectation that image generation will also work. The December 2025 quota reductions removed all free-tier image access without advance notice. CDP users following setup instructions that predate this change will hit this wall immediately.

**How to avoid:**
- Document in the CDP setup guide: image generation requires a paid (Tier 1) Gemini API key with billing enabled.
- Add a pre-flight check in the Image Agent that calls a minimal API probe and explicitly catches the billing-not-enabled error code, then emits a clear human-readable message ("Billing is not enabled on this Gemini API key. Image generation requires a paid account. See: https://ai.google.dev/gemini-api/docs/billing").
- Distinguish billing errors (don't retry) from quota errors (retry with backoff) in the error handler.

**Warning signs:**
- 403 errors on the very first image generation call despite text calls working.
- Error message contains "PERMISSION_DENIED" or "billing not enabled" or a 0-IPM-limit message.
- Browser-based Gemini still works (it uses a different billing path than the API).

**Phase to address:**
Setup/initialization phase — before any image generation code is written. Gate the infographic flow on a validated API key probe that distinguishes billing errors from other failure modes.

---

### Pitfall 2: Model Name Churn — Hardcoded Model IDs Break Without Warning

**What goes wrong:**
Gemini image generation model names change frequently and with short notice. `gemini-2.5-flash-image-preview` was shut down January 15, 2026. `gemini-2.0-flash-exp-image-generation` (the early experimental name) was deprecated months after release. New names follow a different naming convention from models released before September 2025. If CDP hardcodes a model ID like `gemini-2.0-flash-exp-image-generation` in a prompt template or config, it will silently fail with "model not found" errors when Google rotates the stable version.

**Why it happens:**
Image generation models are in Preview status, meaning they ship fast, get renamed, and get deprecated faster than stable text models. Google provides as little as 2 weeks of deprecation notice for Preview models. The rapid iteration cycle (Gemini 2.0 Flash exp → 2.5 Flash Image → 3.1 Flash Image Preview) means any model name baked in today may be invalid within months.

**How to avoid:**
- Store the model ID in `.cdp-context/config.md` as a user-configurable field with a default value, rather than hardcoding it in template logic.
- Document that the default model ID should be updated whenever Google releases a new stable image generation model.
- Include a model discovery step in the pre-flight check: call `client.models.list()` to verify the configured model still exists before generating images.
- Name the config field explicitly (e.g., `Image Model: gemini-2.5-flash-image`) so users can update it independently of the platform field.

**Warning signs:**
- `404 NOT_FOUND` or "model not found" errors from the API.
- Google changelog entries for new image generation model releases.
- Model ID contains `-exp` or `-preview` suffix (high churn risk).

**Phase to address:**
API integration phase — when establishing the SDK call structure. Build model-ID configurability from day one; retrofitting it after hardcoding is error-prone.

---

### Pitfall 3: Resolution Requirements Cannot Be Met with Arbitrary Pixel Values

**What goes wrong:**
CDP requires 2000px minimum on the longest edge. The Gemini API does not accept arbitrary pixel dimensions. It accepts discrete resolution tiers: `512px`, `1K`, `2K`, `4K` — in uppercase. Specifying `2000`, `2048`, `"2k"` (lowercase), or any pixel count not in the enum causes the API to reject the request with a parameter validation error, or silently default to 1K (~1024px on the longest edge). This breaks the CDP output quality guarantee.

**Why it happens:**
Developers familiar with other image APIs (DALL-E, Stable Diffusion) expect pixel-precise resolution control. The Gemini API tier system (`1K`, `2K`) is non-obvious, and the case sensitivity (`2K` not `2k`) is a silent failure mode. The documentation buries the uppercase requirement in a short note.

**How to avoid:**
- Always pass `image_size="2K"` (uppercase) to the API config — this maps to approximately 2048px on the longest edge and satisfies the 2000px minimum.
- Never pass raw pixel counts. Validate the config field against the enum `["512px", "1K", "2K", "4K"]` before calling the API.
- Add a comment in the image generation code: `# Must be uppercase: "2K" not "2k". 1K ~= 1024px, 2K ~= 2048px.`
- For the Imagen path (if used), `imageSize` takes the same `1K`/`2K` values.

**Warning signs:**
- Generated images are smaller than expected (default 1K fallback in play).
- `INVALID_ARGUMENT` errors on the `image_size` parameter.
- Downstream PPTX/DOCX consumers scale up small images, producing blurry output.

**Phase to address:**
API integration phase — encode the resolution specification at the API call layer, not in prompt text. Prompt-level size hints ("2000px wide") are ignored by the API; only the `image_size` parameter matters.

---

### Pitfall 4: JSON Prompt Format Is Not the API Input Format

**What goes wrong:**
The current CDP prompts are structured JSON objects (Pauhu schema: `core`, `style`, `technical`, `composition`, `quality_keywords`, `extras`). In the browser workflow, this JSON is pasted as-is into the Gemini chat UI, which Gemini's web frontend interprets as a structured prompt. The Gemini API `generate_content` call takes a plain text string or typed `Content` parts — not a raw JSON object. If the CDP agent naively passes the JSON object directly without converting it to a text prompt, the API either errors or produces generic output that ignores the JSON structure.

**Why it happens:**
The browser interface treats pasted JSON as a multimodal text prompt; Gemini's model appears to parse it contextually. The API does not have this implicit parsing layer — it requires the contents to be a text string or structured `Part` objects. The migration assumes identical behavior, which is incorrect.

**How to avoid:**
- Convert the populated JSON to a serialized text string (`JSON.stringify(prompt, null, 2)` or `json.dumps(prompt, indent=2)`) and pass that string as the text content of the API call.
- Alternatively, rewrite the prompt templates into structured text prompts, using the JSON keys as section headers, and benchmark whether pure-text prompts produce equivalent or better output.
- Test both approaches on all six infographic types before committing to one format. The API may interpret `extras.data` differently when it arrives as a JSON string in a text message vs. as a structured schema.
- Document which format produces the best infographic quality in a short benchmark session.

**Warning signs:**
- API succeeds but returns a generic or abstract image that ignores `extras.data` content.
- Missing data elements in generated infographics (scores, names, labels not rendered).
- Image quality matches browser output on simple infographics but degrades on data-heavy ones (routing diagram, risk matrix).

**Phase to address:**
Prompt format validation phase — before rolling out to all six infographic types. Run the format comparison on the most data-dense infographic (domain scorecard or risk-opportunity matrix) first.

---

### Pitfall 5: Text Rendering Accuracy Is a Known Weak Point

**What goes wrong:**
CDP infographics require precise text rendering: executive role names, scores, percentages, domain labels, hex color codes, action item descriptions. Gemini's image generation models have approximately 75-94% text rendering accuracy depending on the model, and known weaknesses with small fonts and fine details. Data-critical labels can be misspelled, transposed, or omitted. An infographic that looks visually correct at a glance but has wrong numbers or role labels is worse than a placeholder — it corrupts decision outputs downstream.

**Why it happens:**
Gemini image models are trained for aesthetic image generation, not data-accurate chart rendering. The model does not "understand" that `CFO: Oppose, Confidence: High` must be reproduced verbatim — it treats these as style elements it can approximate. This is fundamentally different from the browser workflow, where Gemini's web interface has stronger grounding in the prompt text due to the conversational context.

**How to avoid:**
- Use `gemini-3-pro-image-preview` (Gemini 3 Pro Image, ~94% text accuracy) rather than the Flash variant for infographics where label precision is critical. Reserve the Flash model for less label-dense infographics.
- Add explicit text-accuracy instructions to every prompt: "Render all text exactly as provided. Do not paraphrase, abbreviate, or reorder labels. Accuracy of text content is mandatory."
- Keep individual text labels short: the Imagen documentation explicitly recommends limiting text to 25 characters or fewer for optimal rendering. Restructure `extras.data` to use abbreviations where possible.
- Implement an output validation step: after receiving the generated image, submit it back to a text-capable Gemini model and ask it to extract all visible text. Compare against expected labels. Flag and retry if critical text is wrong.
- Maintain the existing placeholder fallback: if text accuracy fails after retries, save the prompt and generate a placeholder rather than embedding a corrupted infographic.

**Warning signs:**
- Role names slightly misspelled or truncated.
- Numeric scores that don't match the Decision Record (e.g., `Confidence: Medium` becoming `Confidence: High`).
- Labels missing from crowded infographics (routing diagram with many activated agents).

**Phase to address:**
Quality validation phase — build the output verification loop before deploying to production sessions. The existing 3-attempt retry structure should be reoriented from prompt complexity reduction to text accuracy correction.

---

### Pitfall 6: Rate Limits Operate Across Four Independent Dimensions

**What goes wrong:**
The API enforces rate limits on RPM (Requests Per Minute), RPD (Requests Per Day), TPM (Tokens Per Minute), and IPM (Images Per Minute) independently. A session generating 5-6 infographics in rapid succession can exceed IPM even when well within RPM. The API returns a generic `429 RESOURCE_EXHAUSTED` error for any dimension hit, and the error message does not always indicate which limit was exceeded. Naive retry logic that immediately retries 429s without per-dimension awareness will thrash against IPM limits while staying within RPM.

**Why it happens:**
Developers test with a single image generation call and see it works. When the Image Agent generates all 5-6 infographics sequentially in one session, it pushes against IPM limits that a single-image test never surfaces. The existing browser workflow was naturally rate-limited by the human-pace UI interaction; the API path removes that throttle.

**How to avoid:**
- Add a minimum delay between successive image generation calls (2-5 seconds) regardless of whether the previous call succeeded. This smooths the IPM rate.
- Implement exponential backoff with jitter specifically for 429 errors: start at 5 seconds, double each attempt, cap at 60 seconds, add random jitter (multiply by 0.5-1.0).
- Log which infographic and attempt number triggered a 429 so the session completion report is accurate.
- Do not retry 400 (`INVALID_ARGUMENT`) or 403 (`PERMISSION_DENIED`) errors — these are not transient.
- Check response headers `X-RateLimit-Remaining` and `Retry-After` when available to inform backoff timing.
- The simplified retry logic planned for this milestone (replacing the hard budget counters) should still respect IPM by building in inter-call delays rather than treating the API as instantaneous.

**Warning signs:**
- 429 errors appearing on the 2nd or 3rd infographic in a session but not the 1st.
- Errors resolve with a 30-60 second wait but recur immediately on the next sequential call.
- Session failure patterns cluster around the 3rd-4th image in a batch.

**Phase to address:**
API integration phase — build rate limit handling before wiring the sequential infographic loop. Test with a full 6-infographic session simulation before considering the implementation complete.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcode model ID in template | Simpler initial implementation | Breaks silently when Google deprecates the model (often <6 months) | Never |
| Pass JSON object directly without serializing to string | No conversion code needed | API ignores or misinterprets structured data; silent quality degradation | Never |
| Omit billing-error distinction in error handling | Simpler error path | Users retry forever not knowing they need paid billing | Never |
| Skip inter-call delay between images | Faster generation | IPM rate limits cause 429s on 2nd-3rd infographic; retry storms | Never — add minimum 3s delay |
| Use Flash model for all infographics | Lower cost per image | Unacceptable text rendering accuracy for data-dense infographics | Acceptable for style-heavy infographics (fault line map, routing diagram) if quality holds up |
| Skip output text validation step | Simpler pipeline | Silent data corruption in infographics embedded in board documents | MVP-acceptable if placeholder fallback is reliable; should be added before production use |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Gemini API SDK auth | Passing API key as plain string without sanitization or rotation | Read from `.cdp-context/config.md` at runtime; warn if key is not set; never log the key value |
| `generate_content` response | Accessing `response.text` when IMAGE modality was requested | Check `response.parts` for `inline_data` parts; the image lives in `part.inline_data.data` (base64) not in `response.text` |
| Image response saving | Writing base64 string directly to a `.png` file | Decode base64 first: `Buffer.from(data, 'base64')` (JS) or `base64.b64decode(data)` (Python) before writing |
| `image_size` parameter | Passing `"2k"` (lowercase) or `2048` (integer) | Always pass `"2K"` (uppercase string); only `"512px"`, `"1K"`, `"2K"`, `"4K"` are valid enum values |
| `response_modalities` | Omitting the field or setting `["TEXT"]` only | Must explicitly include `"IMAGE"` in `response_modalities` — the API defaults to text-only output |
| Multi-attempt retry in same session | Opening a new API client session per retry | Reuse the same client instance; multi-turn conversation context via `contents` list if iterative refinement is used |
| Aspect ratio | Sending infographic-style wide prompts without specifying `aspect_ratio` | Specify `aspect_ratio="4:3"` or `"16:9"` explicitly; default `"1:1"` produces square images that may crop data |
| SynthID watermark | Attempting to strip the watermark from generated PNGs | The watermark is invisible and embedded digitally; it does not affect visual output or embedding in PPTX/DOCX/HTML |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Sequential image generation without inter-call delays | 429 IPM errors on 2nd-3rd infographic | Add 3-5 second delay between API calls; implement exponential backoff on 429 | At 2+ images in rapid succession (typical CDP session = 5-6 images) |
| Generating all 6 infographics before checking quality on the first | All 6 complete but several have text rendering failures; no early exit | Check inline_data exists and mime_type is image/png before proceeding to next infographic | First session run — quality issues compound across all 6 images |
| Passing the full untruncated Decision Record section in `extras.data` | Imagen prompt token limit (480 tokens for Imagen) exceeded; text generation timeout | Summarize `extras.data` to essential fields only; the browser workflow tolerated long JSON because the web UI has a higher input limit than the API | Large Decision Records (Tier 3 with full-panel activation) |
| Not caching the API key read from config.md | Config file read 5-6 times per session (once per infographic) | Read and validate the API key once at Image Agent startup; pass to each infographic call | Negligible at 6 images; becomes a concern if parallel generation is added later |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Storing API key in `config.md` in plaintext | Key exposed if `.cdp-context/` is accidentally committed or shared | `.cdp-context/` is already gitignored; add explicit warning in `config-context.md` template that API keys must never be committed; consider reading from environment variable first and falling back to config file |
| Logging the API key in error messages or session transcripts | Key captured in Claude Code session history | Never include the key value in any log, error message, or completion report; log only the last 4 characters as a sanity check |
| Embedding the API key in infographic prompt JSON before sending to the API | Key value included in session output or PROMPT.json fallback files | Extract and handle the API key as a separate credential; it must never appear in prompt data |
| Using a single API key across all users/installations | Single key compromise affects all users | Document that each CDP installation should use its own API key; this is naturally enforced by `.cdp-context/` being per-project |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No setup validation for API key before running a full deliberation | User runs a 20-minute Tier 3 deliberation, image generation fails at the end with a billing error | Add API key validation as a pre-flight step in the Image Agent — probe with a minimal call before starting infographic generation |
| Placeholder PNG identical to current browser-failure placeholder | User cannot tell whether the failure was a browser issue or an API issue | Update placeholder text to clearly indicate the failure mode: "API generation failed — see INFOGRAPHIC_X_PROMPT.json to generate manually using the Gemini web interface" |
| Silent fallback to placeholder with no session-level summary | User receives incomplete session output without knowing why | The existing status report in the task completion message is correct — maintain this pattern; add the specific API error type to each failure log entry |
| Removing browser automation entirely without migration guide | Existing users lose the ability to regenerate old session infographics using the old path | Document the clean break explicitly; provide the JSON prompt files as the manual fallback path (already in the spec) |

---

## "Looks Done But Isn't" Checklist

- [ ] **API key validation:** Image Agent probes the API with a minimal call and fails fast with a clear billing/auth error before starting infographic generation — verify by testing with an invalid key.
- [ ] **Resolution tier:** Generated images are actually 2K (~2048px) on the longest edge — verify by inspecting the PNG dimensions of a generated file, not just trusting the API parameter was accepted.
- [ ] **Base64 decode:** Images saved to disk are valid PNG files (not corrupted base64 strings written as text) — verify by opening the output file with an image viewer.
- [ ] **Model ID configurability:** Changing the model in `.cdp-context/config.md` actually changes which model the API calls — verify by logging the model name at the start of each image generation call.
- [ ] **Rate limit handling:** Running a full 6-infographic session does not produce 429 errors under normal timing — verify by running the full session end-to-end, not just one image.
- [ ] **Placeholder still generated:** When the API call fails (e.g., simulated 503), the placeholder PNG and PROMPT.json are still produced at the expected paths — verify with a forced failure test.
- [ ] **Downstream compatibility:** Generated PNGs embed correctly in PPTX (Task B) and DOCX (Task C) without errors — the filename convention and directory structure must be identical to the current browser output.
- [ ] **JSON prompt to text:** The Pauhu-schema JSON is converted to a text string before being passed to the API, not passed as a raw object — verify by logging the `contents` value of the API call.
- [ ] **Browser automation code removed:** No browser automation calls remain in the Image Agent code path — verify by searching for `computer_use`, `browser`, `navigate`, and `click` in the updated infographics.md specification.
- [ ] **Old config fields cleaned up:** `.cdp-context/config.md` no longer references `Platform: chatgpt` as a valid option (out of scope) — verify by updating the `config-context.md` template.

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Billing not enabled discovered after implementation | LOW | Enable billing on the Google AI Studio account; re-run the Image Agent for the affected session using `/cdp:production` |
| Model ID deprecated mid-deployment | LOW | Update model ID in `.cdp-context/config.md` to the current stable model; no code change required if configurability was built correctly |
| Resolution generating at 1K instead of 2K | MEDIUM | Fix the `image_size` parameter, re-run image generation for affected sessions; downstream PPTX/DOCX may need to be regenerated |
| JSON prompt format produces wrong output | MEDIUM | Test and adopt text-serialized prompt format; update infographic prompt templates; re-run affected infographics |
| Text rendering failures in critical infographics | MEDIUM | Switch to Pro model for affected infographic types; add text accuracy retry loop; regenerate using PROMPT.json files as manual fallback |
| Rate limit storm during 6-image session | LOW | Add inter-call delay and exponential backoff; retry failed infographics individually using the saved PROMPT.json files |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Billing not enabled (silent failure) | API integration setup — before any generation code | Test with an invalid key and confirm the error message is clear and actionable |
| Model ID churn | API integration setup — model configurability | Change the model ID in config.md and confirm the change propagates to the API call |
| Resolution tier confusion | API integration — image_size parameter encoding | Inspect generated PNG file dimensions; must be ≥2000px on longest edge |
| JSON prompt format mismatch | Prompt format validation — before all 6 types | Compare output quality for JSON-as-string vs text-reformatted prompts on the domain scorecard |
| Text rendering accuracy | Quality validation loop — retry structure design | Run all 6 infographic types with a real Decision Record; check that all labels match source data |
| Rate limit multi-dimension hits | API integration — sequential loop with delays | Run full 6-infographic session; confirm no 429 errors; inspect timing between calls |
| Base64 decode error on save | API response handling — image save utility | Open saved PNG in an image viewer; verify it is not corrupted |
| Security — API key in logs/prompts | Error handling and logging design | Grep session output for the API key value; it must not appear anywhere |

---

## Sources

- [Gemini API Image Generation — Official Docs](https://ai.google.dev/gemini-api/docs/image-generation) — MEDIUM confidence (page reflects current state as of fetch date)
- [Gemini API Imagen — Official Docs](https://ai.google.dev/gemini-api/docs/imagen) — MEDIUM confidence
- [Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) — MEDIUM confidence (numerical limits require AI Studio dashboard)
- [Google Gen AI Python SDK — GitHub](https://github.com/googleapis/python-genai) — HIGH confidence
- [Gemini API Deprecations](https://ai.google.dev/gemini-api/docs/deprecations) — HIGH confidence
- [Gemini 3 Pro Image API Reliability Analysis (Dec 2025–Feb 2026)](https://blog.laozhang.ai/en/posts/gemini-3-pro-image-api-unreliable) — LOW confidence (third-party community analysis)
- [Gemini Image Rate Limit Fixes 2026](https://www.aifreeapi.com/en/posts/gemini-image-rate-limit-solution) — LOW confidence (community guide, not official)
- [Fix Every Nano Banana 2 Error (429, 502, Rate Limits)](https://www.aifreeapi.com/en/posts/nano-banana-2-error-429-502-rate-limit) — LOW confidence (community)
- [Gemini API Error 429 — Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/learn-how-to-handle-429-resource-exhaustion-errors-in-your-llms) — MEDIUM confidence (official Google Cloud post)
- [Pauhu Gemini Image Prompting Handbook — GitHub](https://github.com/pauhu/gemini-image-prompting-handbook) — MEDIUM confidence (project the CDP already uses)
- [Gemini Image Generation Free Limits 2026](https://blog.laozhang.ai/en/posts/gemini-image-generation-free-limit-2026) — LOW confidence (community, billing information may drift)
- [Image Generation API Rejects Generic Prompts — GitHub Issue #568](https://github.com/google-gemini/cookbook/issues/568) — MEDIUM confidence (real developer reports)
- [Gemini 2.5 Flash Image Announcement](https://developers.googleblog.com/introducing-gemini-2-5-flash-image/) — HIGH confidence (official Google Developers Blog)

---

*Pitfalls research for: Gemini API image generation — CDP browser-to-API migration*
*Researched: 2026-03-04*
