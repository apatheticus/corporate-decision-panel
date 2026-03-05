---
phase: 07-specification-formalization
plan: 02
subsystem: config
tags: [decision-modes, weighting-tables, cost-formula, specification]

# Dependency graph
requires:
  - phase: 05-ceo-architecture
    provides: "CEO agent structure and decision-modes.md baseline content"
provides:
  - "Directional weighting tables for all 5 decision modes (HIGH/MODERATE/LOW per C-suite role)"
  - "Multi-mode cost formula with generic variables and 4 worked examples"
affects: [agents/ceo.md, config/orchestration-protocol.md]

# Tech tracking
tech-stack:
  added: []
  patterns: [directional-weighting-tables, generic-cost-formula-with-worked-examples]

key-files:
  created: []
  modified: [config/decision-modes.md]

key-decisions:
  - "Architect/Analyst/Sentinel use uniform MODERATE with criteria-based qualifying notes rather than artificial role differentiation"
  - "Cost formula expressed generically (K, L, N variables) so it stays valid if roster changes; worked examples use current numbers"

patterns-established:
  - "Directional weighting table format: C-Suite Role | Disposition | Influence Level | Rationale"
  - "Worked example format: Scenario + domain analysis breakdown + CEO synthesis count + total vs single-mode ratio"

requirements-completed: [SPEC-04, SPEC-05, SPEC-06]

# Metrics
duration: 3min
completed: 2026-03-05
---

# Phase 7 Plan 02: Decision Mode Weighting Tables and Multi-Mode Cost Formula Summary

**Directional weighting tables (HIGH/MODERATE/LOW) for all 5 decision modes plus multi-mode cost formula with generic variables and 4 worked examples in config/decision-modes.md**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-05T10:56:07Z
- **Completed:** 2026-03-05T10:58:41Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Added directional weighting tables mapping all 8 C-suite roles to HIGH/MODERATE/LOW influence levels for each of the 5 decision modes
- Replaced "approximately 1.1x" approximation with actual cost formula, generic cost ratio formula (K + L + N) / (K + L + 1), and "Why the Marginal Cost Is Low" explanation
- Added 4 worked examples covering Tier 2/3 with 2-mode and 5-mode comparison scenarios
- All existing content (Disposition, Decision Theory, Resolution Pattern, CEO Prompt Modifier, Mode/Tier Interaction Matrix, CEO Mode Recommendation) preserved unchanged

## Task Commits

Each task was committed atomically:

1. **Task 1: Add directional weighting tables to all 5 decision modes** - `bf56348` (feat)
2. **Task 2: Expand multi-mode cost formula with calculation and worked examples** - `1c0acea` (feat)

## Files Created/Modified
- `config/decision-modes.md` - Expanded from 107 to 216 lines with weighting tables and cost formula

## Decisions Made
- Architect, Analyst, and Sentinel modes use uniform MODERATE weighting for all roles, with criteria-based qualifying notes explaining that effective influence depends on cross-domain consensus (Architect), evidence confidence (Analyst), or objection severity (Sentinel) rather than static role disposition. This follows the research recommendation and is more honest than artificial differentiation.
- Cost formula expressed generically with K (C-suite count), L (team lead count), N (mode count) variables so the formula remains valid if the organizational roster changes. Worked examples provide current numbers (8 C-suite, 29 team leads) as concrete illustrations.
- Clarifying note placed on first weighting table (Guardian) stating tables describe CEO synthesis behavior, not C-suite agent behavior -- reinforcing the core design principle that domain analysis is mode-independent.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Decision modes now have explicit, auditable weighting tables for CEO synthesis
- Cost formula section provides verifiable math for multi-mode comparison marketing claims
- Ready for Plan 03 (orchestration protocol threshold evaluation format, if applicable)

## Self-Check: PASSED

- FOUND: config/decision-modes.md
- FOUND: 07-02-SUMMARY.md
- FOUND: bf56348 (Task 1 commit)
- FOUND: 1c0acea (Task 2 commit)

---
*Phase: 07-specification-formalization*
*Completed: 2026-03-05*
