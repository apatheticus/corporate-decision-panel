# Phase 12: Dispatch Architecture Rewrite - Context

**Gathered:** 2026-03-08
**Status:** Ready for planning

<domain>
## Phase Boundary

CEO becomes universal dispatcher for all agents (C-suite and team leads). C-suite agents become teammates in CEO-created division teams, communicate sub-questions via files, and receive team lead findings via SendMessage. CCO production pipeline runs under CEO wave management with CCO retaining creative direction and editorial coordination. Covers requirements DISP-01 through DISP-10.

</domain>

<decisions>
## Implementation Decisions

### CEO dispatch timing
- Notification-triggered dispatch, not polling: C-suite agents SendMessage the CEO when sub-questions are ready
- Rolling per-division: CEO dispatches team leads for each division as soon as that C-suite agent's notification arrives — does not wait for all divisions
- C-suite SendMessage contains file list only: "Sub-questions ready: {list of file paths}" — CEO reads the files to build team lead prompts
- Sub-question files retained for audit trail: C-suite writes files AND sends file list notification (files persist for debugging/session resume)
- No-team-leads path: C-suite sends "No team leads needed — proceeding with inline analysis" when no sub-questions are warranted. CEO knows not to wait for that division's sub-question files

### CCO retained role
- CCO is Creative Brief author + editorial coordinator within CEO-managed production team
- CCO does NOT dispatch waves — CEO handles all Agent tool dispatch
- Wave sequencing: CCO notifies CEO when ready for next wave. After each wave completes, team leads SendMessage CCO completion + summary. CCO reads full report file, does editorial assessment, then SendMessages CEO: "Wave N complete, dispatch {next-agent}"
- Revision cycles: If Editor returns REVISION REQUIRED, CCO SendMessages CEO with revision instructions for the responsible team lead. CEO re-dispatches. Maximum one revision cycle (unchanged)
- Team lead reports: Production team leads SendMessage CCO (all in same CEO-created team). CCO reads full _REPORT_*.md files for detail

### Pre-mortem mechanics (Phase 4.5)
- Pre-mortem agents dispatched as standalone subagents (no team_name), same as current architecture
- Division teams dissolve after C-suite writes _RECOMMENDATION_{role}.md — clean lifecycle boundary before pre-mortem
- Pre-mortem prompts include executive summaries only (extracted from _RECOMMENDATION_*.md), not full recommendations — lighter context, consistent with CEO summary-first approach
- Pre-mortem output files unchanged: _PREMORTEM_{role}.md via Write tool, CEO reads after completion

### CSO Phase 1.5 flow
- CSO uses same division team + sub-question file protocol as other C-suite for Phase 1.5 research
- CEO creates cdp-cso-{slug} team, dispatches CSO as teammate, CSO writes sub-question files for 5 research leads, SendMessages CEO file list, CEO dispatches research leads as teammates
- Sequential timing: CSO Phase 1.5 completes fully before Phase 2 begins. CEO reads _DOSSIER_cso.md, incorporates into Phase 0 broadcast, then dispatches Phase 2 C-suite
- CSO Research Dossier output: {session}/_DOSSIER_cso.md (distinct from _RECOMMENDATION_ convention) — clear separation of research vs. recommendation artifacts
- CSO also participates in Phase 2 analytical round (produces _RECOMMENDATION_cso.md)
- CSO Phase 2 dispatch: standalone subagent (no team_name), inline analysis without team leads. CSO receives CEO framing + its own Research Dossier, produces recommendation without re-dispatching research leads
- CSO Phase 2 dispatch happens simultaneously with other C-suite division team dispatch

### Claude's Discretion
- Sub-question file format and structure (markdown template, metadata fields)
- Exact SendMessage wording for notifications
- CEO context management strategy for Tier 3 with many dispatches
- How CEO detects division team completion (background task notifications)
- Division team naming convention details

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `config/dispatch-protocol.md` (115 lines): Current C-suite dispatch protocol — complete rewrite needed for CEO-as-dispatcher with sub-question file convention
- `config/cco-dispatch-protocol.md` (198 lines): Current CCO wave protocol — rewrite for CEO-managed waves with CCO as Creative Brief author + editorial coordinator
- `config/orchestration-protocol.md` (436 lines): Phases 2/3/4 and Production Spawn Sequence need updating for new dispatch flow
- `agents/ceo.md` (382 lines): Needs TeamCreate instructions, team lead dispatch, sub-question file reading, CCO wave management
- `agents/c-suite/cfo.md` Mode B (lines 85-134): Template for C-suite transformation — remove TeamCreate/Agent, add sub-question file writing + SendMessage notification
- All 8 analytical C-suite agents follow identical Mode B dispatch pattern (cfo.md is the template)
- `agents/c-suite/cco.md`: Special transformation — becomes Creative Brief author + editorial coordinator
- `agents/c-suite/cso.md`: Special handling — Phase 1.5 research division + Phase 2 standalone analytical

### Established Patterns
- Agent files use YAML frontmatter + markdown sections
- C-suite agents have Mode A (Tier 1), Mode B (Tier 2/3), Mode C (Phase 4.5 pre-mortem)
- File-based output convention: _RECOMMENDATION_{role}.md, _PREMORTEM_{role}.md, _REPORT_*.md
- Team naming: cdp-{role}-{issue-slug}
- Inline logging protocol (just completed in Phase 11)

### Integration Points
- `config/orchestration-protocol.md` Phases 2, 3, 4: Describe CEO division team dispatch flow
- `config/orchestration-protocol.md` Production Spawn Sequence: CEO-managed CCO wave dispatch
- `config/orchestration-protocol.md` Session Output Setup: Add sub-questions directory
- `agents/ceo.md`: Add TeamCreate, team lead dispatch with sub-questions, CCO wave management, CSO Phase 1.5 handling
- 8 analytical C-suite agents: Transform Mode B — remove TeamCreate/Agent/shutdown_request, add sub-question file writing + SendMessage notification + teammate message receiving
- `agents/c-suite/cco.md`: Transform to Creative Brief author + editorial coordinator (no dispatch, SendMessage-based wave coordination with CEO)
- `agents/c-suite/cso.md`: Dual dispatch — Phase 1.5 division team for research, Phase 2 standalone for analytical
- Verification: `grep -rE "TeamCreate|Agent\.\*team_name|SendMessage\.\*shutdown_request" agents/c-suite/` must return zero matches

</code_context>

<specifics>
## Specific Ideas

- The notification-triggered pattern replaces the polling approach from the original ref doc (`ref/team-refactor-context-260308.md` section 5). SendMessage is more reliable than directory polling and leverages the team communication mechanism already available to teammates.
- CSO gets a dedicated output file convention (_DOSSIER_cso.md) to distinguish research artifacts from domain recommendations — all other C-suite write _RECOMMENDATION_{role}.md.
- CCO wave coordination via SendMessage creates a "CCO drives timing, CEO executes dispatch" split — CCO retains creative/editorial judgment while CEO handles the mechanical dispatch that CCO can't do as a teammate.
- Pre-mortem stays standalone (no team_name) because it's a simple one-round dispatch with no team lead involvement — creating teams would be overhead with no benefit.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 12-dispatch-architecture-rewrite*
*Context gathered: 2026-03-08*
