---
phase: 08-test-scenarios
plan: 01
subsystem: testing
tags: [test-scenarios, routing, pre-mortem, tier-2, degraded-input, orchestration]

# Dependency graph
requires:
  - phase: 07-specification-formalization
    provides: "Structured threshold decision trees, diagnostic questions, per-condition evaluation format"
provides:
  - "Tier 2 scoping clarification in orchestration-protocol.md resolving full-activation ambiguity"
  - "TEST-01 scenario: Tier 2 partial activation with triggered thresholds"
  - "TEST-02 scenario: Pre-mortem degraded input with missing and partial recommendations"
  - "Operational definitions for Missing Recommendation and Partial Recommendation"
affects: [08-02-PLAN, orchestration-protocol, test-scenarios]

# Tech tracking
tech-stack:
  added: []
  patterns: [behavioral-test-scenario-document, specification-level-testing]

key-files:
  created:
    - test-scenarios/tier2-partial-activation.md
    - test-scenarios/premortem-degraded-input.md
  modified:
    - config/orchestration-protocol.md

key-decisions:
  - "Added 'user-specified roles take precedence' language to orchestration-protocol.md Tier 2 scoping note"
  - "Missing confidence field defaults to LOW confidence for synthesis weighting (conservative default)"
  - "Missing agents excluded from pre-mortem broadcast summaries but noted in preamble"

patterns-established:
  - "Behavioral test scenario structure: Requirement, Validates, Spec References, Decision Scenario, Pre-Conditions, Expected Behavior, Behavioral Assertions, Failure Modes, Expected Output Excerpt"
  - "Degraded input definitions as prerequisite section before scenario: operationalize ambiguous terms before using them"
  - "Assertions reference specification file locations, not literal LLM output text"

requirements-completed: [TEST-01, TEST-02]

# Metrics
duration: 3min
completed: 2026-03-05
---

# Phase 8 Plan 1: Tier 2 Routing and Pre-Mortem Test Scenarios Summary

**Tier 2 scoping clarification resolving full-activation ambiguity, plus two behavioral test scenarios validating routing precedence (TEST-01) and pre-mortem resilience under degraded input (TEST-02)**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-05T11:27:57Z
- **Completed:** 2026-03-05T11:31:50Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Resolved specification ambiguity between "all C-suite activate" threshold override and Tier 2 user-specified role constraints by adding Tier 2 scoping note to orchestration-protocol.md Step 4
- Created tier2-partial-activation.md (TEST-01): acquisition scenario with 3 triggered thresholds, 6 behavioral assertions, 3 failure modes, and sample Escalation Note output
- Created premortem-degraded-input.md (TEST-02): B2B-to-B2C pivot scenario with COO missing and VP Delivery partial, 7 behavioral assertions, 4 failure modes, operational definitions for "missing" and "partial" recommendations, and sample Fault Line Analysis output

## Task Commits

Each task was committed atomically:

1. **Task 1: Clarify Tier 2 threshold scoping and create Tier 2 partial activation test scenario** - `78eb291` (feat)
2. **Task 2: Create pre-mortem degraded input test scenario** - `1b31c48` (feat)

## Files Created/Modified

- `config/orchestration-protocol.md` - Added Tier 2 scoping note to Step 4 resolving full-activation threshold ambiguity for user-specified Tier 2 engagements
- `test-scenarios/tier2-partial-activation.md` - TEST-01: Acquisition scenario where user specifies CFO+CTO but 3/5 thresholds trigger; validates routing precedence and escalation recommendation
- `test-scenarios/premortem-degraded-input.md` - TEST-02: B2B-to-B2C pivot scenario with COO missing (timeout) and VP Delivery partial (no confidence/risks); validates pre-mortem resilience and gap acknowledgment

## Decisions Made

- Added "user-specified roles take precedence" as explicit language in the Tier 2 scoping note rather than relying on implicit interpretation of panel-assessment.md constraints
- Defined Missing Recommendation as "activated but no output" and Partial Recommendation as "output with incomplete required fields" -- these operational definitions did not exist in the protocol before
- VP Delivery with partial recommendation still participates in pre-mortem (partial information > exclusion), while COO with no recommendation is excluded entirely (cannot fabricate perspective)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added "user-specified roles take precedence" phrase to orchestration-protocol.md**
- **Found during:** Task 1 verification
- **Issue:** The plan's must_haves artifact check expects the phrase "user-specified roles take precedence" in orchestration-protocol.md, but the initial note insertion used different phrasing ("does not override the user's role selection")
- **Fix:** Prepended "user-specified roles take precedence" to the existing sentence to satisfy the must_haves check while preserving the full clarification
- **Files modified:** config/orchestration-protocol.md
- **Verification:** `grep -c "user-specified roles take precedence" config/orchestration-protocol.md` returns 1
- **Committed in:** 78eb291 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor phrasing adjustment to match must_haves. No scope creep.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- test-scenarios/ directory established with consistent structure pattern for 08-02 to follow
- Behavioral test scenario pattern is documented (Requirement, Validates, Spec References, Decision Scenario, Pre-Conditions, Expected Behavior, Assertions, Failure Modes, Expected Output)
- TEST-01 and TEST-02 complete; TEST-03 (mode sensitivity criteria) and TEST-04 (consistency scenarios) remain for 08-02

## Self-Check: PASSED

All files verified present. All commits verified in git log.

---
*Phase: 08-test-scenarios*
*Completed: 2026-03-05*
