# Roadmap: CDP Image Generation — Browser to API Migration

## Overview

Migrate the Corporate Decision Panel's infographic generation from browser automation to direct Gemini API calls. The build order is driven by component dependencies: config parsing is the foundation every other component needs, API wiring comes next, reliability (errors + quality validation) follows, and instruction document updates come last once the script is proven. Four phases deliver a working, reliable, browserless image generation pipeline.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Config and Pre-flight** - API key parsing, model ID configurability, and billing validation before any generation
- [ ] **Phase 2: API Integration** - Script skeleton plus live end-to-end generation for one infographic type
- [ ] **Phase 3: Error Handling and Quality** - Retry logic, rate limiting, content-block classification, and AI vision validation
- [ ] **Phase 4: Scale and Docs** - All six infographic types generating via API; instruction documents updated; browser automation removed

## Phase Details

### Phase 1: Config and Pre-flight
**Goal**: Users can configure a Gemini API key and have it validated before any infographic generation starts
**Depends on**: Nothing (first phase)
**Requirements**: SETUP-01, SETUP-02, SETUP-03, DOC-02
**Success Criteria** (what must be TRUE):
  1. User can add `Gemini API Key:` and `Image Model:` fields to `.cdp-context/config.md` and the system reads them correctly
  2. Running the pre-flight check with a valid key and billing enabled produces a clear success message
  3. Running with an invalid key, disabled billing, or wrong model ID produces a specific human-readable error (not a silent 403)
  4. The `templates/config-context.md` template includes API key, model ID, and retry limit fields with documented format
**Plans:** 2 plans

Plans:
- [ ] 01-01-PLAN.md — Config template, parser, test infrastructure
- [ ] 01-02-PLAN.md — Pre-flight validation with 4-step API check

### Phase 2: API Integration
**Goal**: A single infographic type generates end-to-end via the Gemini API, producing a valid PNG at the correct output path
**Depends on**: Phase 1
**Requirements**: GEN-01, GEN-02, GEN-03, GEN-04
**Success Criteria** (what must be TRUE):
  1. `scripts/generate_infographic.py` accepts a template type, Decision Record data, and output path and writes a PNG at `{session}/images/INFOGRAPHIC_<type-slug>.png`
  2. The generated PNG is at least 2000px on its longest edge and opens correctly as a valid image
  3. The Domain Scorecard type (most text-dense) generates with real Decision Record data and the data labels are recognizably correct
  4. Aspect ratio is set per infographic type (4:3 for matrix/scorecard layouts, 16:9 for routing/fault-line diagrams)
  5. Thinking mode is active for Fault-Line Map and Mode Comparison types (configurable `thinking_level`)
**Plans:** 3 plans

Plans:
- [ ] 02-01-PLAN.md — Prompt serialization TDD (template loading, placeholder substitution, natural language flattening)
- [ ] 02-02-PLAN.md — Generation engine (API call, aspect ratios, thinking config, preflight integration, CLI)
- [ ] 02-03-PLAN.md — Live generation verification (Domain Scorecard end-to-end with human visual check)

### Phase 3: Error Handling and Quality
**Goal**: Infographic generation is reliable across a full 6-infographic session — transient failures retry, content blocks skip cleanly, and quality validation catches bad text rendering
**Depends on**: Phase 2
**Requirements**: ERR-01, ERR-02, ERR-03, ERR-04, QUAL-01, QUAL-02, QUAL-03
**Success Criteria** (what must be TRUE):
  1. A 429 or 503 error triggers exponential backoff with jitter and eventually succeeds or falls back gracefully
  2. A SAFETY or OTHER content block does not retry — it immediately produces a placeholder PNG and saves the prompt JSON
  3. After any total failure, the output directory contains a white placeholder PNG and a `INFOGRAPHIC_<type>_PROMPT.json` file, leaving the session intact for downstream tasks
  4. A full 6-infographic session completes without 429 rate-limit storms (inter-call delay of 3-5 seconds between images)
  5. After generation, a Gemini vision pass verifies that expected data labels are present; if it fails, generation retries with corrective feedback up to the configured maximum
**Plans:** 3 plans (2 executed + 1 gap closure)

Plans:
- [x] 03-01-PLAN.md — Error classification, placeholder PNG, PROMPT.json, vision validation module
- [x] 03-02-PLAN.md — Retry wrapper with backoff, session orchestrator with inter-call delay and summary
- [x] 03-03-PLAN.md — Gap closure: propagate validation warning_only to session summary (OK+WARN status)

### Phase 4: Scale and Docs
**Goal**: All six infographic types generate via API and instruction documents reflect the API-based workflow with no browser automation references remaining
**Depends on**: Phase 3
**Requirements**: DOC-01, DOC-03, DOC-04
**Success Criteria** (what must be TRUE):
  1. All six infographic types (routing diagram, scorecard, risk matrix, fault-line map, action timeline, mode comparison) generate successfully via `scripts/generate_infographic.py`
  2. `templates/production/infographics.md` Task A spec describes the API-based script invocation — no browser automation steps remain
  3. `agents/ceo.md` Task A spawn instruction references the script, not browser-based generation
  4. No browser automation code paths remain in the image generation workflow
**Plans:** 3 plans

Plans:
- [ ] 04-01-PLAN.md — Rewrite infographics.md and ceo.md for API-based workflow
- [ ] 04-02-PLAN.md — Browser automation sweep across SKILL.md, README.md, docs/README.md, docs/ARCHITECTURE.md
- [ ] 04-03-PLAN.md — Live 6-type generation verification with test data fixtures and visual spot-check

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Config and Pre-flight | 2/2 | Complete | 2026-03-04 |
| 2. API Integration | 3/3 | Complete | 2026-03-04 |
| 3. Error Handling and Quality | 3/3 | Complete | 2026-03-04 |
| 4. Scale and Docs | 0/3 | Not started | - |
