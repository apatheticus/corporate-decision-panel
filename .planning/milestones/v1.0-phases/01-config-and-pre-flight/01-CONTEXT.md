# Phase 1: Config and Pre-flight - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Parse API key, model ID, and retry limit from `.cdp-context/config.md`; validate them against the Gemini API before any infographic generation starts. Update `templates/config-context.md` with the new fields. This phase does NOT generate infographics — it establishes the configuration foundation every other phase needs.

</domain>

<decisions>
## Implementation Decisions

### Config field format
- Use placeholder-with-instructions format: `- **Gemini API Key:** (paste your key here)` with a comment explaining where to get a key and that the file is gitignored
- Default model ID: `gemini-2.0-flash-exp`
- Include retry limit field now with default value (e.g., `- **Retry Limit:** (default: 2)`) — Phase 3 reads it when built
- Remove the Platform field entirely — Gemini-only means no platform choice needed

### Pre-flight behavior
- Pre-flight runs BOTH standalone (`python preflight.py` or equivalent) AND automatically before generation
- Validates four things in order: (1) config file parseable and required fields present, (2) API key validity, (3) billing / image generation enabled, (4) configured model ID accessible
- Hard stop with specific error on failure — no infographics attempted, operator must fix config
- Pre-flight check during auto-run prevents any generation from starting if validation fails

### Script architecture
- Python implementation (matches roadmap's `scripts/generate_infographic.py` naming)

### Error messaging
- Dual audience: messages must be readable by human operators AND parseable by AI agents (CEO agent)
- Each error should clearly state what failed and what to fix

### Claude's Discretion
- Module structure (flat scripts/ vs package with modules) — pick what scales cleanly through all 4 phases
- Config parsing approach (regex vs markdown parser) — pick simplest reliable approach
- Probe method for pre-flight validation (text-only call vs tiny image generation) — pick most reliable approach that validates billing/image gen
- Exit code strategy (distinct per error type vs simple 0/1)
- Success message format (minimal single-line vs detailed multi-line report)
- Remediation detail level in error messages (include URLs or just describe the problem)
- Python dependency management format (requirements.txt vs pyproject.toml)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `templates/config-context.md`: Current config template with Platform field — will be updated with API key, model ID, retry limit fields
- `templates/infographic-prompts/*.json`: 6 JSON prompt templates with `{{PLACEHOLDER}}` syntax — config parser must align with how these are consumed in Phase 2

### Established Patterns
- Config lives in `.cdp-context/config.md` (gitignored), template lives in `templates/config-context.md` — user copies template to `.cdp-context/` and customizes
- Markdown field format: `- **Field Name:** (value -- default: x)` with parenthetical defaults/options
- Agent system reads `.cdp-context/` files at runtime — config parser must work in this context

### Integration Points
- `templates/production/infographics.md` Task A spec currently references Platform field and browser automation — Phase 4 updates this, but Phase 1's config changes must be forward-compatible
- `agents/ceo.md` spawns the Image Agent with task description — pre-flight results may need to be reportable to the CEO agent
- No `scripts/` directory exists yet — Phase 1 creates this foundation

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-config-and-pre-flight*
*Context gathered: 2026-03-04*
