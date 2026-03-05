---
phase: 06-orchestration-hardening
plan: 02
subsystem: orchestration
tags: [cso, timeout, graceful-degradation, research-gaps, maxTurns, agent-protocol]

# Dependency graph
requires:
  - phase: 05-ceo-architecture
    provides: Executive summary blocks with Confidence and Key Risks fields in all 8 C-suite agents
provides:
  - CSO maxTurns-based timeout with graceful degradation to partial Research Dossier
  - RESEARCH STATUS flag in Phase 0 broadcast for pattern matching by downstream agents
  - Conditional Research Basis field and RESEARCH CAVEAT paragraph in all 8 C-suite Mode B templates
affects: [06-orchestration-hardening, ceo-synthesis]

# Tech tracking
tech-stack:
  added: []
  patterns: [conditional-field-insertion, flag-based-behavioral-branching, graceful-degradation]

key-files:
  created: []
  modified:
    - agents/c-suite/cso.md
    - config/orchestration-protocol.md
    - agents/c-suite/cfo.md
    - agents/c-suite/cto.md
    - agents/c-suite/coo.md
    - agents/c-suite/ciso.md
    - agents/c-suite/cao.md
    - agents/c-suite/vp-sales.md
    - agents/c-suite/vp-delivery.md

key-decisions:
  - "maxTurns: 25 chosen as CSO ceiling -- generous for normal operation (5 team leads with their own maxTurns: 5) but catches runaway execution"
  - "RESEARCH STATUS flag is a standalone pattern-matchable line in Phase 0 broadcast, not buried in prose"
  - "Research Basis: Partial field only appears when research is incomplete -- absence means complete, avoiding noise"
  - "RESEARCH CAVEAT instructs agents to assess domain-specific impact rather than mechanically lowering confidence"

patterns-established:
  - "Conditional field insertion: fields that only appear in output templates when a specific flag is present in the broadcast"
  - "Flag-based behavioral branching: standalone pattern-matchable flags in broadcasts that trigger conditional behavior in downstream agents"
  - "Graceful degradation: behavioral priority instructions for agents approaching turn limits rather than programmatic turn counting"

requirements-completed: [ORCH-03, ORCH-04]

# Metrics
duration: 3min
completed: 2026-03-05
---

# Phase 6 Plan 2: CSO Timeout Handling and Research Caveats Summary

**CSO maxTurns timeout with RESEARCH GAPS reporting, RESEARCH STATUS broadcast flag, and conditional Research Basis/RESEARCH CAVEAT annotations across all 8 C-suite Mode B templates**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-05T10:09:50Z
- **Completed:** 2026-03-05T10:12:55Z
- **Tasks:** 2
- **Files modified:** 9

## Accomplishments
- Added maxTurns: 25 to CSO with behavioral timeout/graceful degradation section including RESEARCH GAPS template
- Added timeout policy to orchestration protocol Phase 1.5 and RESEARCH STATUS: INCOMPLETE flag to Phase 0 broadcast
- Added conditional "Research Basis: Partial" field to all 8 C-suite Mode B executive summary templates (after Confidence, before Key Risks)
- Added conditional RESEARCH CAVEAT paragraph to all 8 C-suite Mode B Domain Recommendation bodies (after executive summary, before analysis)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add CSO timeout handling and RESEARCH STATUS flag to protocol** - `603529b` (feat)
2. **Task 2: Add conditional Research Basis field and RESEARCH CAVEAT to all 8 C-suite agents** - `e3684a1` (feat)

## Files Created/Modified
- `agents/c-suite/cso.md` - Added maxTurns: 25, Timeout and Graceful Degradation section, Research Basis and RESEARCH CAVEAT in Mode B
- `config/orchestration-protocol.md` - Added timeout policy paragraph in Phase 1.5, RESEARCH STATUS flag in Phase 0 broadcast
- `agents/c-suite/cfo.md` - Added conditional Research Basis field and RESEARCH CAVEAT in Mode B template
- `agents/c-suite/cto.md` - Added conditional Research Basis field and RESEARCH CAVEAT in Mode B template
- `agents/c-suite/coo.md` - Added conditional Research Basis field and RESEARCH CAVEAT in Mode B template
- `agents/c-suite/ciso.md` - Added conditional Research Basis field and RESEARCH CAVEAT in Mode B template
- `agents/c-suite/cao.md` - Added conditional Research Basis field and RESEARCH CAVEAT in Mode B template
- `agents/c-suite/vp-sales.md` - Added conditional Research Basis field and RESEARCH CAVEAT in Mode B template
- `agents/c-suite/vp-delivery.md` - Added conditional Research Basis field and RESEARCH CAVEAT in Mode B template

## Decisions Made
- maxTurns: 25 chosen as CSO ceiling -- generous for normal operation but catches runaway execution
- RESEARCH STATUS flag is a standalone pattern-matchable line in Phase 0 broadcast, not buried in prose
- Research Basis: Partial field only appears when research is incomplete -- absence means complete, avoiding noise in normal operation
- RESEARCH CAVEAT instructs agents to assess domain-specific impact rather than mechanically lowering confidence
- Behavioral timeout instructions (prioritize output completeness) rather than programmatic turn counting, since agents cannot detect remaining turns

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- CSO timeout and gap reporting mechanism complete -- ready for integration testing
- All 8 C-suite agents now handle incomplete research gracefully via conditional annotations
- Phase 6 Plan 3 (remaining orchestration hardening tasks) can proceed

## Self-Check: PASSED

All 9 modified files verified on disk. Both task commits (603529b, e3684a1) verified in git log.

---
*Phase: 06-orchestration-hardening*
*Completed: 2026-03-05*
