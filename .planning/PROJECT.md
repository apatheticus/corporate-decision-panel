# CDP Image Generation: Browser → API Migration

## What This Is

The Corporate Decision Panel (CDP) is an AI-powered executive decision framework that orchestrates a panel of C-suite agent perspectives (CEO, CFO, CTO, CISO, CAO, COO, VP Sales, VP Delivery, CSO) through a structured deliberation cascade. It includes infographic generation via Gemini API, formalized routing and specification documents, and comprehensive test scenarios for edge-case validation.

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
- ✓ CEO orchestration protocol extracted into standalone config — v1.1
- ✓ CEO agent under 350 lines with zero orchestration duplication — v1.1
- ✓ C-suite executive summaries for efficient synthesis — v1.1
- ✓ CEO summary-first synthesis with conflict-triggered deep-dive — v1.1
- ✓ Pre-flight dependency validation for production pipeline — v1.1
- ✓ CSO timeout protection with gap reporting — v1.1
- ✓ C-suite confidence caveats for incomplete research — v1.1
- ✓ Session cleanup command (/cdp:cleanup) — v1.1
- ✓ Structured routing threshold decision trees with calibration exemplars — v1.1
- ✓ Directional weighting tables for all 5 decision modes — v1.1
- ✓ Multi-mode cost formula with worked examples — v1.1
- ✓ CEO per-condition threshold evaluation for audit trail — v1.1
- ✓ Test scenarios: Tier 2 routing, pre-mortem degraded input, mode sensitivity — v1.1

### Active

<!-- Deferred from v1.0 backlog -->
- [ ] Model profile switch — Flash for development, Pro for production
- [ ] Per-infographic model selection — Pro for text-heavy, Flash for simpler
- [ ] Concurrent generation with IPM-aware rate limiting
- [ ] Imagen 4 as alternative model option

## Current Milestone: Planning next milestone

### Out of Scope

- ChatGPT/OpenAI API support — Gemini-only for now
- Browser-based fallback — clean break, no dual-path
- Changing infographic types or data flow from Decision Record
- Modifying downstream embedding (PPTX, DOCX, HTML, PDF)
- Pixel-level programmatic validation (OCR, contrast) — AI vision check sufficient
- Environment variable API key storage — config file pattern consistent with .cdp-context/

## Context

Shipped v1.1 with 4,910 LOC Python (188 tests) + 15,713 LOC markdown specs/agents.
Tech stack: Python, google-generativeai SDK, Pillow, pytest.
Key files: `scripts/config.py`, `scripts/preflight.py`, `scripts/generate_infographic.py`, `scripts/validation.py`, `scripts/session.py`.
Agent/config files: `agents/ceo.md`, `config/orchestration-protocol.md`, `config/routing-table.md`, `config/decision-modes.md`, `SKILL.md`.
All six infographic types verified with live API generation. 19 v1.1 requirements satisfied across 5 phases.

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
| Extract orchestration from CEO into config/ | CEO monolith → focused agent + referenced protocol | ✓ Good — 348-line CEO, 307-line protocol, zero duplication |
| Directional weighting (HIGH/MOD/LOW) not numeric | LLMs can't reliably apply 1.5x multipliers | ✓ Good — explicit out-of-scope constraint validated |
| maxTurns: 25 as CSO timeout ceiling | Balance research depth with session reliability | ✓ Good — graceful degradation with gap reporting |
| User-specified roles override threshold routing at Tier 2 | Preserve user intent; thresholds surface as escalation | ✓ Good — clear separation of user intent vs system recommendation |
| Countable dimensions for mode sensitivity | 3 dimensions with CONVERGE/PARTIAL/DIVERGE, no computed ratios | ✓ Good — LLM-appropriate quantification |
| Clean session deletion, no archival | Users wanting preservation should version-control | ✓ Good — keeps cleanup simple |

---
*Last updated: 2026-03-05 after v1.1 milestone complete*
