# Phase 10: Production Quick Wins - Context

**Gathered:** 2026-03-08
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix 4 specific failures from the 2026-03-08 production session: slug alias resolution for shorthand infographic type slugs, validation leniency for high-density infographic types, PDF module path fix for cross-directory execution, and graphic designer slug corrections. These are independent code/config fixes with no architectural changes.

</domain>

<decisions>
## Implementation Decisions

### Slug alias resolution
- Static `SLUG_ALIASES` dict at module level in `generate_infographic.py`, resolved inside `load_template()` only
- Three aliases: `fault-lines` → `fault-line-map`, `risk-matrix` → `risk-opportunity-matrix`, `action-plan` → `action-plan-timeline`
- Alias resolves for template file lookup only — output filenames use the original slug the caller passed
- `ASPECT_RATIOS` dict gets shorthand entries added (e.g., `'fault-lines': '16:9'`) rather than resolving aliases at that layer

### Output filename convention
- Keep shorthand filenames: `INFOGRAPHIC_fault-lines.png`, `INFOGRAPHIC_risk-matrix.png`, `INFOGRAPHIC_action-plan.png`
- No downstream reference changes needed — README, HTML templates, capsule structure, build_results_pdf all stay as-is
- The alias is purely internal for template file resolution

### Graphic designer slugs
- Graphic designer keeps shorthand slugs in `types_list` and `data_paths` — the alias map handles template resolution
- INFRA-02 scope adjusted: "graphic designer uses slugs that the alias map can resolve" rather than "uses canonical slugs directly"
- No changes needed to graphic designer's data JSON filenames (`fault-lines.json`, `risk-matrix.json`, `action-plan.json`)

### Validation leniency
- `validate_infographic()` gains a `type_slug` parameter (optional, default None)
- `LENIENT_TYPES = {'routing-diagram'}` set at module level in `validation.py`
- For lenient types, PARTIAL labels count as pass (no warning, no retry trigger)
- Garbled text detection stays strict for all types — garbled text is a generation quality problem, not a density issue
- Caller (`generate_with_retry`) passes the original slug — no alias resolution at validation layer
- `routing-diagram` has no alias (already canonical), so this works cleanly

### Publisher path fix
- Add `cd <skill-directory> &&` prefix to `python3 -m scripts.build_results_pdf` invocation in publisher.md
- `<skill-directory>` placeholder matches existing pattern in graphic-designer.md (`sys.path.insert(0, '<skill-directory>')`)
- CEO/dispatcher fills in the actual path when dispatching the publisher

### Claude's Discretion
- Whether capsule PDF build script (`python3 {session}/build/build_capsule.py`) also needs the `cd` fix
- Exact placement of SLUG_ALIASES dict relative to other constants
- Test coverage approach for alias resolution and validation leniency

</decisions>

<specifics>
## Specific Ideas

No specific requirements — these are straightforward bug fixes driven by the 2026-03-08 production session error logs. The decisions above fully specify the implementation approach.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `generate_infographic.py:load_template()`: Already normalizes slugs (lowercase, underscore→hyphen) — alias resolution adds one line
- `generate_infographic.py:ASPECT_RATIOS`: Existing dict at module level — add 3 shorthand entries
- `validation.py:validate_infographic()`: Existing function — add optional `type_slug` parameter
- `validation.py:_parse_validation_response()`: Already parses PARTIAL as `warning_only=True` — leniency logic goes after parsing

### Established Patterns
- Module-level constant dicts for configuration (ASPECT_RATIOS, THINKING_TYPES, RETRYABLE_CODES, CONTENT_BLOCK_REASONS)
- Agent files use `<skill-directory>` and `{session}` as dispatcher-filled placeholders
- Validation is non-blocking by design (API error = pass-with-warning)

### Integration Points
- `generate_with_retry()` calls `validate_infographic()` — needs to pass `type_slug` parameter
- `generate_infographic()` calls `load_template()` — alias resolution happens transparently
- Publisher agent definition (`agents/team-leads/cco/publisher.md`) — bash command update
- Graphic designer agent definition (`agents/team-leads/cco/graphic-designer.md`) — no changes needed (keeps shorthand slugs)

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 10-production-quick-wins*
*Context gathered: 2026-03-08*
