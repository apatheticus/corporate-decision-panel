# Phase 4: Scale and Docs - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

All six infographic types generate successfully via `scripts/generate_infographic.py` and the session orchestrator. Instruction documents (`templates/production/infographics.md` and `agents/ceo.md`) are updated to reflect the API-based workflow. All browser automation references are removed from the image generation workflow. This phase does NOT add new infographic types, modify the generation engine, or change retry/validation logic — those are complete from Phases 2-3.

</domain>

<decisions>
## Implementation Decisions

### Image Agent role
- Image Agent remains a separate spawned agent (Task A), preserving the parallel task architecture (A/B/C run simultaneously)
- Image Agent reads the Decision Record, extracts data per infographic type, and writes a data JSON file to `{session}/images/` per type
- Agent calls the session orchestrator (`scripts/session.py`) to generate all 6 types at once — does not call `generate_infographic` individually
- Agent reports the session summary (OK/FAILED/BLOCKED per type) back to the CEO agent
- Script is a pure generation tool; the agent handles all data extraction from the Decision Record

### Infographics.md rewrite
- Replace these sections: Technology (remove platform profiles, add script invocation), Attempt Budget (simplify to config reference), Browser Automation Workflow (replace with API script workflow), Error Handling (update to match Phase 3 behavior)
- Keep as-is: Purpose, all 6 Infographic Specifications (Routing Diagram through Mode Comparison with layout, data elements, constraints), Output Requirements, Content Mapping from Decision Record, Multi-Mode Variant
- Simplify Attempt Budget to brief "Retry Behavior" section referencing `config.md` `Retry Limit` field — script handles retries internally
- Remove Style Configuration Integration mapping table — replace with brief note that script applies `.cdp-context/style.md` automatically if present
- Audience shift: from "Image Agent doing browser automation" to "Image Agent calling a Python script with data JSON files"

### Verification of all 6 types
- Live test all 6 infographic types with real Decision Record data (Claude finds existing test data or creates representative test data)
- Run automated validation (Phase 3 vision validation) — all types must pass (OK or OK+WARN)
- Manual visual spot-check of all 6 PNG outputs for layout sanity
- If any type fails: debug, fix (prompt template or script), re-verify — all 6 must generate successfully before Phase 4 is complete

### Browser automation cleanup
- Full repo sweep: grep entire codebase for browser automation references (navigate, browser, chatgpt.com, gemini.google.com, platform profiles, conversation, model picker, fast-mode warnings, etc.)
- Remove completely — no ChatGPT references, no platform selection, no dual-platform code, no historical notes
- Platform field in config.md already removed in Phase 1 — verify it's gone during sweep
- No fast-mode considerations needed for API script (API calls work regardless of Claude Code mode)

### Claude's Discretion
- Session orchestrator CLI invocation details (how Image Agent calls session.py)
- Data JSON schema for each infographic type (field names, structure)
- Exact wording of new infographics.md sections (Technology, Workflow, Retry Behavior, Error Handling)
- CEO spawn description wording for Task A
- Test data source (existing session vs synthetic record)
- Order of operations: docs update first vs verification first

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/session.py`: Session orchestrator — runs all infographic types sequentially with inter-call delay, adaptive 429 handling, and summary table
- `scripts/generate_infographic.py`: `generate_infographic()` function with `GenerationResult` dataclass — core generation per type
- `scripts/validation.py`: Vision-based quality validation — runs automatically during generation
- `scripts/config.py`: `load_config()` returns `api_key`, `model_id`, `retry_limit`
- `scripts/preflight.py`: `run_preflight()` with auto-run before generation
- 6 JSON prompt templates in `templates/infographic-prompts/*.json` with core/style/technical/composition/quality_keywords/extras structure

### Established Patterns
- `scripts/` Python package with `__init__.py` — all generation modules live here
- `GenerationResult` dataclass with `success`, `warning_only`, `had_rate_limit` fields
- `_status()` function for structured output lines parseable by CEO agent
- Dual-audience messaging: human-readable + CEO-agent-parseable
- `ConfigError` with `error_code` + `remediation` for dual-audience errors

### Integration Points
- `templates/production/infographics.md` Task A spec — primary doc to rewrite (browser automation → script invocation)
- `agents/ceo.md` Task A spawn instruction — currently says "Generate analytical infographics via browser automation"
- `templates/config-context.md` — Platform field already removed in Phase 1; API key, model ID, retry limit fields present
- Session output convention: `{session}/images/INFOGRAPHIC_<type-slug>.png`

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 04-scale-and-docs*
*Context gathered: 2026-03-04*
