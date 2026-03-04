# Project Research Summary

**Project:** Corporate Decision Panel — Gemini API Image Agent Migration
**Domain:** Gemini API image generation integration (browser automation to direct API migration)
**Researched:** 2026-03-04
**Confidence:** HIGH (stack and architecture verified from official docs; features MEDIUM due to fast-moving model landscape; pitfalls MEDIUM-HIGH from official docs + confirmed community issues)

## Executive Summary

The CDP Image Agent currently generates infographics by submitting JSON prompts to the Gemini web UI through browser automation. This approach breaks in Claude Code fast-mode, requires session login state, and cannot be reliably automated. The migration path is well-understood: replace browser steps with direct calls to `google-genai>=1.65.0` SDK using `client.models.generate_content()` with `response_modalities=["IMAGE"]`, save the resulting PNG via Pillow, and keep the existing Pauhu-schema JSON templates as-is by serializing them to text strings before submission. The total dependency footprint is minimal: two packages (`google-genai`, `Pillow`), one new script (`scripts/generate_infographic.py`), and a config field addition to `.cdp-context/config.md`.

The recommended model is `gemini-2.5-flash-image` (GA since October 2025) at `image_size="2K"` with a `4:3` or `16:9` aspect ratio depending on infographic type. This satisfies CDP's 2000px minimum requirement and costs approximately $0.039 per image (~$0.20-$0.23 per full session). Image generation is unavailable on the free Gemini API tier — a paid API key is non-negotiable. The old `google-generativeai` package was deprecated November 30, 2025 and must not be used; only `google-genai` supports current image generation models.

The primary risks are not architectural but operational: billing not enabled produces confusing silent failures; model names change with as little as two weeks' notice; text rendering accuracy is approximately 75-94% depending on model choice, which means data-critical labels (scores, role names, percentages) may be approximate rather than exact. These risks are manageable with a pre-flight API probe, configurable model ID, and a placeholder fallback path — all of which the existing codebase partially implements. The migration is low-risk if built in the correct order: config schema first, script skeleton second, API wiring third, error handling fourth, instruction document update last.

## Key Findings

### Recommended Stack

The migration requires exactly two new runtime dependencies. `google-genai>=1.65.0` is the only current GA SDK for Gemini API image generation; the older `google-generativeai` was sunset November 30, 2025. `Pillow>=11.0.0` is required to convert the raw bytes returned by the API into a PNG file on disk. Both are pure-Python, widely available, and conflict-free with the existing CDP environment. All other required utilities (`io.BytesIO`, `pathlib.Path`, `re`) are Python stdlib — no additional packages needed.

The API call pattern is `client.models.generate_content()` with `response_modalities=["IMAGE"]` in the config — NOT `generate_images()`, which is the Imagen-family method only. The `image_size` parameter must be uppercase `"2K"` (not `"2k"` or `2048`). The model string should be stored in config, not hardcoded, because Google rotates image model names every few months.

**Core technologies:**
- `google-genai>=1.65.0`: Gemini API client — only GA SDK supporting current image generation models; replaces deprecated `google-generativeai`
- `gemini-2.5-flash-image`: Image generation model — GA since October 2025, integrates reasoning with generation, $0.039/image
- `Pillow>=11.0.0`: PNG file output — converts raw API response bytes to PNG via `Image.open(BytesIO(...))`

### Expected Features

The migration is fundamentally a capability substitution, not a feature expansion. Every P1 feature maps to something the browser workflow already did; the API enables cleaner, more reliable execution of the same outputs.

**Must have (table stakes — migration fails without these):**
- API key auth from `.cdp-context/config.md` — `genai.Client(api_key=KEY)` replaces browser session login
- `response_modalities=["IMAGE"]` in generation config — without this, the API returns text only (most common implementation mistake)
- JSON template serialization to text string — existing Pauhu-schema JSON must be `json.dumps()`-converted before submission; the API does not parse JSON natively
- `image_size="2K"` with aspect ratio — meets 2000px minimum; requires paid tier; `4:3` for matrix/scorecard, `16:9` for routing/fault-line layouts
- Base64-to-PNG extraction and file save — `Image.open(BytesIO(part.inline_data.data)).save(path)` pattern; output path must match existing contract
- Exponential backoff retry on 429/503 — replaces the browser's hard budget counter with a simpler transient-error-only retry model
- Placeholder PNG + saved prompt JSON on total failure — existing behavior that must be preserved for downstream task compatibility

**Should have (add after basic pipeline is validated):**
- Aspect ratio optimization per infographic type — test whether `4:3` vs `16:9` materially improves each of the 6 types
- Thinking mode (`thinking_level="High"`) for Fault-Line Map and Mode Comparison — may improve accuracy on densest infographics; adds latency
- Interleaved text response capture — log the text portion of the API response for debugging prompt adherence

**Defer (v2+):**
- Imagen 4 as an alternative model — different quality characteristics worth exploring once v1 quality is characterized
- Concurrent generation with IPM-aware rate limiting — out of scope per PROJECT.md; sequential is correct for now
- Per-infographic model selection (Pro for text-heavy, Flash for others) — cost optimization, not MVP

### Architecture Approach

The architecture is a thin Python script layer between the Image Agent's markdown instructions and the Gemini API. The Image Agent invokes `scripts/generate_infographic.py` via the Bash tool, passing a template type, Decision Record data, and output path. The script handles everything: config parsing, template loading, placeholder replacement, API call with retry, response extraction, and PNG write. The existing JSON templates (`templates/infographic-prompts/*.json`) are unchanged in structure; they are loaded, tokens replaced, and serialized to a string for API submission. The client is instantiated once and reused across all 5-6 infographic calls per session.

**Major components:**
1. **Config Reader** — Parses `Gemini API Key:` field from `.cdp-context/config.md` using regex; also reads `Image Model:` field for model ID configurability
2. **Prompt Builder** — Loads JSON template, replaces `{{PLACEHOLDER}}` tokens with Decision Record data, validates JSON integrity, serializes to string
3. **API Call Layer** — `client.models.generate_content()` with retry logic; distinguishes transient errors (429, 503 — retry) from content blocks (SAFETY, OTHER — skip to placeholder) from auth failures (403 — abort all)
4. **Response Handler** — Guards `finish_reason` before accessing `content.parts`; extracts `inline_data.data` bytes; writes PNG via Pillow
5. **Placeholder Generator** — On exhausted retries: writes white PNG with failure text via Pillow; saves prompt JSON as `INFOGRAPHIC_<type>_PROMPT.json`

### Critical Pitfalls

1. **Billing not enabled produces confusing 403/429 errors** — Add a pre-flight API probe before starting the infographic loop; emit a specific human-readable message if billing is not enabled; do not retry billing errors
2. **Model names rotate every few months with little notice** — Store the model ID in `.cdp-context/config.md` as a configurable field; never hardcode it in the script; verify model existence via `client.models.list()` in the pre-flight check
3. **`response_modalities=["IMAGE"]` is required and commonly omitted** — Without this parameter the API returns text only with no image; it must be explicit in every `GenerateContentConfig`; this is the single most common implementation error (confirmed GitHub issue #568)
4. **JSON prompt must be serialized to a string, not passed as a Python dict** — The API accepts text, not structured JSON objects; `json.dumps(populated_template)` is required; omitting this produces generic images that ignore the template data
5. **Text rendering accuracy is 75-94% — data labels may be wrong** — Use `gemini-2.5-flash-image` for initial testing; validate that scores, role names, and percentages render correctly; the existing placeholder fallback is the correct safety net when text accuracy is unacceptable

## Implications for Roadmap

The research identifies a clear five-phase build order, driven by component dependencies. Each phase builds on the previous and can be independently tested before the next begins.

### Phase 1: Foundation — Config Schema and Pre-flight Validation

**Rationale:** Every other component depends on the API key being correctly read from config. Establishing the config field syntax and a working pre-flight probe first eliminates the most common silent failure mode (billing errors) and makes all subsequent testing deterministic.

**Delivers:** Working API key parsing from `.cdp-context/config.md`; pre-flight probe that validates billing status and model availability before any infographic generation; clear error messages for auth and billing failures; updated `config-context.md` template with `Gemini API Key:` and `Image Model:` fields.

**Addresses:** API key auth (P1), billing-error distinction (Pitfall 1), model ID configurability (Pitfall 2)

**Avoids:** Hours of debugging SDK or prompt format when the real issue is billing; silent 403 failures mid-session

**Research flags:** Standard patterns — no additional research needed. Config file parsing, regex extraction, and `client.models.list()` discovery are well-documented.

### Phase 2: Script Skeleton — Template Loading and PNG Output

**Rationale:** Build and test the non-API parts of `scripts/generate_infographic.py` in isolation: config reading, JSON template loading, `{{PLACEHOLDER}}` replacement, JSON serialization to string, and Pillow PNG writing. This lets the image save path be validated before any API costs are incurred.

**Delivers:** A working script that reads a template, applies substitutions, and writes a placeholder PNG — with no live API call. Validates the output path contract (`{session}/images/INFOGRAPHIC_<slug>.png`) against what Tasks B, C, and D expect. Also validates the JSON-to-string serialization approach.

**Addresses:** JSON prompt as text (Pitfall 4), base64-to-PNG save pattern (P1 feature), output path contract stability

**Avoids:** Discovering path or format errors after spending API budget on test calls

**Research flags:** Standard patterns — Pillow byte-to-PNG conversion, `pathlib.Path.mkdir(parents=True)`, and `json.dumps()` are trivial and well-documented.

### Phase 3: API Integration — Single Infographic Type End-to-End

**Rationale:** Wire the live API call for one infographic type (Domain Scorecard is best — it is the most text-dense and will surface text rendering accuracy issues immediately). Test `response_modalities=["IMAGE"]`, `image_size="2K"`, aspect ratio, and `finish_reason` guard in isolation before scaling to all six types.

**Delivers:** A working end-to-end generation for one infographic type: real API call, real PNG written to disk at the correct path, verified dimensions (≥2000px), verified PNG validity (open in image viewer). Confirms the JSON-as-text approach produces correct visual output.

**Addresses:** `response_modalities` requirement (P1, Pitfall — omission is the most common mistake), `image_size="2K"` encoding (Pitfall 3), `finish_reason` guard (Architecture Pattern 3), JSON prompt format (Pitfall 4)

**Avoids:** Discovering format or config issues after wiring all six types; spending full session API budget during debugging

**Research flags:** Needs focused testing — text rendering accuracy for Domain Scorecard is the highest-risk unknown. Verify label precision on the first real output before proceeding. May need to evaluate Flash vs Pro model quality tradeoff here.

### Phase 4: Error Handling and Retry Logic

**Rationale:** Production reliability requires distinguishing transient errors (429, 503 — retry) from content blocks (SAFETY, OTHER — skip) from auth failures (403 — abort). The retry logic must include inter-call delays to avoid IPM rate limit storms across a full 6-infographic session.

**Delivers:** Retry loop with exponential backoff and jitter; inter-call delay (3-5 seconds minimum between images); error classification logic; placeholder PNG + saved PROMPT.json on all failure paths; session completion report with per-infographic status.

**Addresses:** Rate limit handling (Pitfall 6, P1 feature), content block vs transient error distinction (Architecture Anti-pattern 2), placeholder fallback preservation (P1), security — API key never in logs or prompt files

**Avoids:** 429 rate limit storms on the 2nd-3rd infographic; infinite retry loops on content blocks; corrupted session output

**Research flags:** Standard patterns — exponential backoff with jitter is well-documented. The specific IPM limit values are MEDIUM confidence (tier-dependent, changes frequently); test with a full 6-infographic session to confirm the 3-5 second inter-call delay is sufficient.

### Phase 5: Scale to All Six Types and Update Instruction Documents

**Rationale:** Once the single-type pipeline is proven reliable, extend to all six infographic types and update `templates/production/infographics.md` to replace browser automation steps with the script invocation pattern.

**Delivers:** All six infographic types generating via API (`scripts/generate_infographic.py` with type-slug argument routing); type-specific aspect ratio assignments; updated Image Agent task spec in `infographics.md` with browser automation references removed; updated `agents/ceo.md` to remove browser-dependent Task A spawning instructions.

**Addresses:** All remaining P1 features; aspect ratio optimization per type (P2); browser automation code removal (Pitfall checklist item)

**Avoids:** Leaving browser automation code paths that confuse the agent; old config options (`Platform: chatgpt`) remaining in templates

**Research flags:** Aspect ratio selection per infographic type is empirical — needs brief testing to confirm `4:3` vs `16:9` for each of the six types. No additional API research needed; the patterns are established by Phase 3.

### Phase Ordering Rationale

- **Config before script:** The regex parsing pattern for `.cdp-context/config.md` is the foundation; every other component passes through it
- **Script before API:** Isolating template loading and PNG write logic allows fast, cost-free iteration on the non-API components
- **Single type before all six:** Validates the complete API pattern at minimal cost before scaling; surfaces text rendering accuracy issues on the hardest type first
- **Errors after API wiring:** Error handling requires a working API call to test; the error paths can be simulated (force a bad key, force a 503) once the success path is stable
- **Instruction docs last:** The script must be proven before the agent instruction document depends on it; updating docs first would cause the agent to fail until the script catches up

### Research Flags

Phases needing validation during implementation:

- **Phase 3 (API Integration):** Text rendering accuracy on Domain Scorecard is the highest-risk unknown. Flash vs Pro model quality tradeoff must be evaluated empirically on real Decision Record data before committing to a model choice for production.
- **Phase 4 (Rate Limits):** IPM limit values are tier-specific and change frequently; verify inter-call delay is sufficient by running a full 6-infographic session end-to-end.

Phases with standard patterns (additional research not needed):

- **Phase 1 (Config Schema):** Regex parsing, `client.models.list()`, error message design — all well-documented
- **Phase 2 (Script Skeleton):** Pillow, `pathlib`, `json.dumps()` — trivial stdlib patterns
- **Phase 5 (Scale + Docs):** Extending the Phase 3 pattern to additional infographic types is mechanical; aspect ratio selection is empirical (brief test, not research)

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | `google-genai`, `gemini-2.5-flash-image`, `Pillow` all verified from official docs and PyPI. The deprecated `google-generativeai` risk is confirmed from official deprecation notice. |
| Features | MEDIUM | P1 features are verified from official docs. Model landscape is fast-moving — `gemini-3.1-flash-image-preview` was referenced as MEDIUM confidence since it is still Preview status. Rate limit numbers are tier-specific and change without notice. |
| Architecture | HIGH | Component boundaries, data flow, config parsing pattern, retry logic, and `finish_reason` guard are all verified from official SDK docs and confirmed community issues. The `generate_content()` vs `generate_images()` method distinction is documented. |
| Pitfalls | MEDIUM-HIGH | Critical pitfalls verified from official docs (billing, model churn, `image_size` enum, `response_modalities`). Text rendering accuracy estimates (75-94%) from multiple sources including official Vertex AI limitation docs. Rate limit multi-dimension behavior from official Google Cloud blog + community corroboration. |

**Overall confidence:** HIGH for implementation decisions; MEDIUM for model quality and rate limit specifics that require empirical validation.

### Gaps to Address

- **Text rendering accuracy thresholds:** The 75-94% accuracy range is too wide to inform a clear Flash vs Pro model decision. Phase 3 must include a quality benchmark on the Domain Scorecard (most text-dense) before committing to a model for production.
- **IPM limits by paid tier:** The exact IPM quota for the user's API tier is not knowable without checking their AI Studio dashboard. The 3-5 second inter-call delay is a conservative default; Phase 4 testing will confirm whether it is sufficient.
- **Aspect ratio per infographic type:** No definitive mapping was found in documentation. Research recommends `4:3` for matrix/scorecard layouts and `16:9` for routing/fault-line diagrams, but this is a reasoned inference, not a tested result. Validate in Phase 5.
- **`gemini-3.1-flash-image-preview` readiness:** If this model reaches GA before Phase 3 implementation, it may offer meaningfully better text rendering than `gemini-2.5-flash-image`. Check model status at implementation time before locking in the default.

## Sources

### Primary (HIGH confidence)
- [Gemini API: Generate images — Official Docs](https://ai.google.dev/gemini-api/docs/image-generation) — model IDs, `generate_content()` with IMAGE modality, `ImageConfig` parameters
- [Gemini API Libraries — Official](https://ai.google.dev/gemini-api/docs/libraries) — `google-generativeai` deprecated November 30, 2025; `google-genai` is current GA SDK
- [Gemini 2.5 Flash Image GA Announcement — Google Developers Blog](https://developers.googleblog.com/en/gemini-2-5-flash-image-now-ready-for-production-with-new-aspect-ratios/) — GA date, aspect ratio list, $0.039/image pricing
- [google-genai on PyPI](https://pypi.org/project/google-genai/) — version 1.65.0 current as of 2026-02-26
- [Gemini API Deprecations — Official](https://ai.google.dev/gemini-api/docs/deprecations) — model retirement timeline, deprecation notice process
- [Google Gen AI Python SDK — GitHub](https://github.com/googleapis/python-genai) — official SDK source, retry patterns
- [GitHub Issue #568 — response_modalities requirement](https://github.com/google-gemini/cookbook/issues/568) — confirms `response_modalities=["IMAGE"]` omission as most common mistake
- [Gemini Image Generation Limitations — Vertex AI Docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/gemini-image-generation-limitations) — text rendering accuracy, known weak points

### Secondary (MEDIUM confidence)
- [Gemini API Rate Limits — Official Docs](https://ai.google.dev/gemini-api/docs/rate-limits) — numerical limits are tier-specific and change; use AI Studio dashboard for current values
- [Google Gen AI SDK Docs](https://googleapis.github.io/python-genai/) — `generate_images()` vs `generate_content()` method separation (scraped March 2026)
- [Gemini API Error 429 — Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/learn-how-to-handle-429-resource-exhaustion-errors-in-your-llms) — exponential backoff patterns, 429 handling
- [finishReason blocking behavior — API Help](https://help.apiyi.com/en/gemini-api-image-blocked-finishreason-other-solution-en.html) — `finish_reason` guard pattern
- [Pauhu Gemini Image Prompting Handbook — GitHub](https://github.com/pauhu/gemini-image-prompting-handbook) — JSON prompt schema CDP already uses; API text-submission compatibility

### Tertiary (LOW confidence — orientation only, not relied upon for implementation decisions)
- [Gemini Image Rate Limit 2026 — LaoZhang AI Blog](https://blog.laozhang.ai/en/posts/gemini-image-generation-free-limit-2026) — billing change context, free tier IPM removal
- [Gemini 3 Pro Image Reliability Analysis — LaoZhang AI Blog](https://blog.laozhang.ai/en/posts/gemini-3-pro-image-api-unreliable) — community analysis of model reliability patterns
- [Fix Nano Banana 2 Errors — aifreeapi.com](https://www.aifreeapi.com/en/posts/nano-banana-2-error-429-502-rate-limit) — community rate limit workarounds

---
*Research completed: 2026-03-04*
*Ready for roadmap: yes*
