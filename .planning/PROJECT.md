# CDP Image Generation: Browser → API Migration

## What This Is

Migrated the Corporate Decision Panel's infographic generation system from browser-based automation to direct Gemini API calls via the `google-generativeai` SDK. All six infographic types now generate via a single Python script with automatic retry, vision-based quality validation, and session orchestration.

## Core Value

Infographic generation must work without browser interaction — a single API call per infographic that returns a PNG, driven by the same Decision Record data.

## Requirements

### Validated

- ✓ Six infographic types with JSON prompt templates — existing
- ✓ Data extraction from Decision Record sections — existing
- ✓ Placeholder token population (`{{PLACEHOLDER}}` syntax) — existing
- ✓ Style override system via `.cdp-context/style.md` — existing
- ✓ Platform configuration via `.cdp-context/config.md` — existing
- ✓ Placeholder PNG + saved prompt on total failure — existing
- ✓ Output to `{session}/images/INFOGRAPHIC_<type-slug>.png` — existing
- ✓ Embedding in HTML, PPTX, DOCX, PDF outputs — existing
- ✓ Quality criteria (legibility, white background, color fidelity, data completeness) — existing
- ✓ Gemini API integration via `google-generativeai` SDK — v1.0
- ✓ API key storage in `.cdp-context/config.md` — v1.0
- ✓ Prompt serialization from JSON templates to natural language — v1.0
- ✓ Exponential backoff with jitter on transient errors — v1.0
- ✓ Content block detection (no retry on safety blocks) — v1.0
- ✓ AI vision quality validation with corrective retry — v1.0
- ✓ Session orchestrator with adaptive rate limiting — v1.0
- ✓ All browser automation references removed — v1.0
- ✓ Documentation updated for API-based workflow — v1.0

### Active

- [ ] Model profile switch — Flash for development, Pro for production
- [ ] Per-infographic model selection — Pro for text-heavy, Flash for simpler
- [ ] Concurrent generation with IPM-aware rate limiting
- [ ] Imagen 4 as alternative model option

### Out of Scope

- ChatGPT/OpenAI API support — Gemini-only for now
- Browser-based fallback — clean break, no dual-path
- Changing infographic types or data flow from Decision Record
- Modifying downstream embedding (PPTX, DOCX, HTML, PDF)
- Pixel-level programmatic validation (OCR, contrast) — AI vision check sufficient
- Environment variable API key storage — config file pattern consistent with .cdp-context/

## Context

Shipped v1.0 with 4,910 LOC Python (188 tests).
Tech stack: Python, google-generativeai SDK, Pillow, pytest.
Key files: `scripts/config.py`, `scripts/preflight.py`, `scripts/generate_infographic.py`, `scripts/validation.py`, `scripts/session.py`.
All six infographic types verified with live API generation.

## Constraints

- **SDK**: `google-generativeai` Python SDK
- **Output format**: PNG, 2000px minimum on longest edge
- **Config location**: API key in `.cdp-context/config.md` (gitignored)
- **Backward compatible output**: Same filenames, same directory structure, same embedding points

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Gemini API only (drop ChatGPT) | Simplify to one platform | ✓ Good — single SDK, simpler codebase |
| API key in config file (not env vars) | Consistent with existing .cdp-context/ pattern | ✓ Good — fits existing workflow |
| Remove browser automation entirely | Clean break, simpler codebase | ✓ Good — eliminated login issues |
| Simplified retry (no hard budgets) | API calls are fast/cheap | ✓ Good — backoff + jitter handles 429s |
| gemini-2.5-flash-image default model | gemini-2.0-flash-exp was shut down Nov 2025 | ✓ Good — future-proof default |
| Descriptive paragraphs over keyword lists | Per Google guidance for image gen prompts | ✓ Good — higher quality output |
| SDK retry disabled (attempts=1) | Prevents double-retry explosion with our own retry | ✓ Good — clean retry control |
| Non-blocking validation (API error = pass-with-warning) | Quality gate shouldn't block generation | ✓ Good — robust in production |
| 4s inter-call delay with adaptive doubling on 429 | Balance throughput and rate limiting | ✓ Good — full sessions complete cleanly |
| warning_only propagation to session summary | OK+WARN distinguishes clean vs validated-with-issues | ✓ Good — useful status granularity |

---
*Last updated: 2026-03-04 after v1.0 milestone*
