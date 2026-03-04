---
phase: 03-error-handling-and-quality
plan: 02
subsystem: api
tags: [retry, backoff, rate-limiting, session-orchestrator, inter-call-delay, adaptive-delay, corrective-feedback]

# Dependency graph
requires:
  - phase: 03-error-handling-and-quality
    plan: 01
    provides: create_placeholder_png, save_prompt_json, error classification helpers, validate_infographic, GenerationResult
provides:
  - generate_with_retry() wrapper with shared retry budget for transient errors and validation
  - _backoff() helper with exponential delay (base 2s, max 30s) and 50% jitter
  - SessionResult dataclass for session-level orchestration results
  - run_session() orchestrator processing all types with inter-call delay
  - Adaptive delay doubling on 429 rate limit for remaining images
  - Summary table output with per-image status (OK/FAILED/BLOCKED)
  - had_rate_limit field on GenerationResult for session-level signaling
  - style_override_extra parameter on generate_infographic for corrective feedback injection
  - SDK retry disabled via HttpRetryOptions(attempts=1) to prevent double-retry
affects: [04-scale-and-docs]

# Tech tracking
tech-stack:
  added: [time.sleep for inter-call delay, random.uniform for jitter calculation]
  patterns: [shared retry budget across transient + validation retries, adaptive rate limiting, session-level orchestration with per-image status tracking]

key-files:
  created: [scripts/session.py, tests/test_session.py]
  modified: [scripts/generate_infographic.py, tests/test_generate_infographic.py]

key-decisions:
  - "Module-level import of validate_infographic in generate_infographic.py (no circular dependency) for clean mock patching"
  - "had_rate_limit field on GenerationResult signals 429 encounters to session layer for adaptive delay"
  - "Placeholder dimensions derived from ASPECT_RATIOS: 4:3 types get 1440x1080, 16:9 types get 1920x1080"
  - "SDK retry disabled via HttpRetryOptions(attempts=1) to prevent double-retry explosion (SDK 5 x app 3 = 15 calls)"

patterns-established:
  - "Retry wrapper pattern: generate_with_retry wraps generate_infographic, owns retry budget"
  - "Session orchestrator pattern: run_session iterates types, applies delay, prints summary"
  - "Adaptive rate limiting: session doubles inter-call delay on 429 for remaining images"
  - "Corrective feedback injection: style_override_extra appended to prompt on validation failure retry"

requirements-completed: [ERR-01, ERR-04, QUAL-02]

# Metrics
duration: 6min
completed: 2026-03-04
---

# Phase 3 Plan 2: Retry Wrapper and Session Orchestrator Summary

**Retry-aware generate_with_retry() wrapper with exponential backoff, corrective feedback from vision validation, and run_session() orchestrator with 4s inter-call delay, adaptive 429 handling, and per-image summary table**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-04T17:59:27Z
- **Completed:** 2026-03-04T18:05:51Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Retry wrapper with shared budget (default 3 attempts) covering both transient API errors and validation retries
- Exponential backoff with jitter (base 2s, doubling per attempt, capped 30s, +50% random jitter)
- Content blocks produce immediate placeholder with no retry and zero budget consumed
- Validation failure triggers retry with corrective feedback appended via style_override_extra
- Session orchestrator processes all types with 4s inter-call delay, doubling on 429
- SDK retry disabled to prevent double-retry explosion (Pitfall 1 from research)
- Test count increased from 93 to 125 (32 new tests)

## Task Commits

Each task was committed atomically (TDD: RED then GREEN):

1. **Task 1: generate_with_retry wrapper with exponential backoff and corrective feedback**
   - `6f8f09f` (test: failing tests for retry, backoff, feedback, SDK retry)
   - `5011aae` (feat: implementation of _backoff, generate_with_retry, SDK retry disabled)
2. **Task 2: Session orchestrator with inter-call delay, adaptive 429 handling, and summary table**
   - `00ba7b4` (test: failing tests for session orchestrator)
   - `4cf26a0` (feat: implementation of scripts/session.py)

_TDD tasks had two commits each (test then feat)_

## Files Created/Modified
- `scripts/generate_infographic.py` - Added _backoff, generate_with_retry, style_override_extra param, HttpRetryOptions(attempts=1), had_rate_limit on GenerationResult
- `scripts/session.py` - New module with SessionResult, run_session, _format_summary_line, adaptive inter-call delay
- `tests/test_generate_infographic.py` - Added TestBackoff, TestRetry, TestRetryBudgetExhausted, TestContentBlockNoRetry, TestRetryWithFeedback, TestSDKRetryDisabled, TestPlaceholderDimensions, TestGenerateWithRetryHadRateLimit, TestSkipPreflightOnRetry (19 new tests)
- `tests/test_session.py` - New test file with TestInterCallDelay, TestAdaptiveDelay, TestSessionContinuesOnFailure, TestSessionSummary, TestSessionAllFailed, TestSessionExitCode, TestSessionResult (13 new tests)

## Decisions Made
- Used module-level import of `validate_infographic` in generate_infographic.py instead of lazy import -- no circular dependency exists (validation imports from config, not generate_infographic), and module-level import enables clean mock patching in tests
- Added `had_rate_limit: bool = False` field to GenerationResult to signal 429 encounters from the per-image retry loop to the session-level orchestrator for adaptive delay
- Derived placeholder dimensions from ASPECT_RATIOS mapping: 4:3 types (domain-scorecard, risk-opportunity-matrix) get 1440x1080; all others get 1920x1080
- Disabled SDK retry with HttpRetryOptions(attempts=1) per research Pitfall 1 -- prevents double-retry explosion (SDK 5 attempts x app 3 attempts = 15 actual API calls)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Complete reliability layer ready for Phase 4 (Scale and Docs)
- generate_with_retry wraps generate_infographic with full retry/validation/feedback loop
- run_session orchestrates all 6 types with rate-limit-safe delays and summary output
- Exit code 0/1 based on any_succeeded for CEO agent integration
- All 125 tests pass (93 existing + 32 new)

## Self-Check: PASSED

- All 4 files exist (2 created, 2 modified)
- All 4 task commits verified (6f8f09f, 5011aae, 00ba7b4, 4cf26a0)
- All exports importable from both modules
- 125 tests pass (32 new, 93 existing unaffected)

---
*Phase: 03-error-handling-and-quality*
*Completed: 2026-03-04*
