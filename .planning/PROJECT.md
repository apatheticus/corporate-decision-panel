# CDP Image Generation: Browser → API Migration

## What This Is

Migrate the Corporate Decision Panel's infographic generation system from browser-based automation (submitting JSON prompts to Gemini/ChatGPT web UIs) to direct Gemini API calls via the `google-generativeai` SDK. This removes the browser dependency, eliminates login requirements, and makes image generation faster and more reliable.

## Core Value

Infographic generation must work without browser interaction — a single API call per infographic that returns a PNG, driven by the same Decision Record data.

## Requirements

### Validated

<!-- Existing capabilities that already work and must be preserved. -->

- ✓ Six infographic types with JSON prompt templates — existing
- ✓ Data extraction from Decision Record sections — existing
- ✓ Placeholder token population (`{{PLACEHOLDER}}` syntax) — existing
- ✓ Style override system via `.cdp-context/style.md` — existing
- ✓ Platform configuration via `.cdp-context/config.md` — existing
- ✓ Placeholder PNG + saved prompt on total failure — existing
- ✓ Output to `{session}/images/INFOGRAPHIC_<type-slug>.png` — existing
- ✓ Embedding in HTML, PPTX, DOCX, PDF outputs — existing
- ✓ Quality criteria (legibility, white background, color fidelity, data completeness) — existing

### Active

<!-- Current scope. Building toward these. -->

- [ ] Gemini API integration via `google-generativeai` SDK for image generation
- [ ] API key storage in `.cdp-context/config.md`
- [ ] Prompt format optimized for Gemini API (may restructure JSON templates)
- [ ] Simplified retry logic — auto-retry on failure, no hard budget tracking
- [ ] Remove all browser automation code from image generation workflow
- [ ] Update `infographics.md` Task A specification for API-based flow
- [ ] Update platform configuration to reference API key instead of browser login
- [ ] Maintain 2000px minimum resolution and PNG output format

### Out of Scope

- ChatGPT/OpenAI API support — Gemini-only for now
- Browser-based fallback — clean break, no dual-path
- Changing infographic types or data flow from Decision Record
- Modifying downstream embedding (PPTX, DOCX, HTML, PDF)
- Concurrent/parallel image generation (future enhancement)

## Context

The CDP production pipeline generates 5-6 analytical infographics per decision session. These are data visualizations (routing diagrams, scorecards, risk matrices, fault-line maps, action timelines, mode comparisons) — not artistic images.

Current browser automation has known issues:
- Incompatible with Claude Code fast mode
- Requires user to be pre-logged into Gemini/ChatGPT
- Budget tracking (3 per infographic, 12 per session) adds complexity
- Browser session can be unreliable

The Gemini API's native image generation capabilities can accept the same kind of structured prompts and return images directly, removing all browser dependencies.

**Key files to modify:**
- `templates/production/infographics.md` — Task A specification
- `templates/infographic-prompts/*.json` — 6 JSON prompt templates
- `templates/config-context.md` — Platform config template
- `.cdp-context/config.md` — User's platform config (if exists)
- `agents/ceo.md` — Task A spawn instruction

## Constraints

- **SDK**: Must use `google-generativeai` Python SDK (or equivalent JS/Node SDK if preferred)
- **Output format**: PNG, 2000px minimum on longest edge
- **Config location**: API key in `.cdp-context/config.md` (gitignored)
- **Backward compatible output**: Same filenames, same directory structure, same embedding points

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Gemini API only (drop ChatGPT) | Simplify to one platform, user's preference | — Pending |
| API key in config file (not env vars) | Consistent with existing .cdp-context/ pattern | — Pending |
| Remove browser automation entirely | Clean break, simpler codebase | — Pending |
| Simplified retry (no hard budgets) | API calls are fast/cheap, budget tracking was browser workaround | — Pending |

---
*Last updated: 2026-03-04 after initialization*
