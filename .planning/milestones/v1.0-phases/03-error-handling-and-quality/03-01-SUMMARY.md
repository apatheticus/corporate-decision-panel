---
phase: 03-error-handling-and-quality
plan: 01
subsystem: api
tags: [pillow, gemini-vision, error-handling, validation, png-placeholder, content-safety]

# Dependency graph
requires:
  - phase: 02-api-integration
    provides: generate_infographic function, GenerationResult dataclass, ClientError handling
provides:
  - create_placeholder_png for white PNG error placeholders with type-specific dimensions
  - save_prompt_json for machine-readable prompt metadata (JSON with error_code, timestamp)
  - Error classification helpers (_is_retryable_error, _is_content_block)
  - Content block detection in generate_infographic (prompt-level and candidate-level)
  - ServerError (5xx) handling in generate_infographic
  - Vision quality validation module (validate_infographic, ValidationResult)
  - Expected label extraction from data dicts (_extract_expected_labels)
  - Structured validation response parsing (_parse_validation_response)
affects: [03-02-retry-loop-and-session]

# Tech tracking
tech-stack:
  added: [Pillow ImageDraw/ImageFont for placeholder generation, google.genai vision multimodal input]
  patterns: [content block detection via prompt_feedback.block_reason and candidate finish_reason, non-blocking validation (API error returns pass-with-warning), structured VERDICT/WARNINGS/MISSING/FEEDBACK parsing]

key-files:
  created: [scripts/validation.py, tests/test_validation.py]
  modified: [scripts/generate_infographic.py, tests/test_generate_infographic.py, tests/conftest.py]

key-decisions:
  - "ImageFont.load_default(size=36) as primary font strategy with try/except fallback for Pillow < 10.4"
  - "Validation API errors return pass-with-warning (non-blocking) to avoid blocking generation"
  - "Content block detection checks both prompt_feedback.block_reason and candidates[0].finish_reason"
  - "Label extraction splits comma-separated items using heuristic (comma + uppercase letter)"

patterns-established:
  - "ValidationResult dataclass follows same pattern as GenerationResult and PreflightResult"
  - "Error codes: CONTENT_BLOCKED_{reason} for safety blocks, API_ERROR_{code} for HTTP errors"
  - "Non-blocking validation: API failures during quality check return pass-with-warning"

requirements-completed: [ERR-02, ERR-03, QUAL-01, QUAL-03]

# Metrics
duration: 6min
completed: 2026-03-04
---

# Phase 3 Plan 1: Error Handling Foundation Summary

**Placeholder PNG generation, PROMPT.json metadata, error classification (retryable vs content-block), content block detection in API responses, and Gemini vision quality validation module**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-04T17:49:14Z
- **Completed:** 2026-03-04T17:55:46Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Placeholder PNG generation with type-specific dimensions (1440x1080 for 4:3, 1920x1080 for 16:9) using Pillow
- Machine-readable PROMPT.json with type, ISO 8601 UTC timestamp, error_code, and prompt text
- Error classification separating retryable HTTP errors (429/503/500) from content safety blocks
- Content block detection in generate_infographic for both prompt-level and candidate-level blocks
- Vision quality validation module that sends PNG + expected labels to Gemini and parses structured response
- Test count increased from 55 to 93 (38 new tests)

## Task Commits

Each task was committed atomically (TDD: RED then GREEN):

1. **Task 1: Placeholder PNG, PROMPT.json, and error classification helpers**
   - `cf1d816` (test: failing tests for placeholder, prompt JSON, error classification, content block)
   - `0641d82` (feat: implementation of all Task 1 functions + generate_infographic updates)
2. **Task 2: Vision quality validation module**
   - `8eff981` (test: failing tests for validation module)
   - `223414e` (feat: implementation of scripts/validation.py)

_TDD tasks had two commits each (test then feat)_

## Files Created/Modified
- `scripts/generate_infographic.py` - Added create_placeholder_png, save_prompt_json, RETRYABLE_CODES, CONTENT_BLOCK_REASONS, _is_retryable_error, _is_content_block, _detect_content_block; updated generate_infographic to catch ServerError and detect content blocks
- `scripts/validation.py` - New module with ValidationResult, _extract_expected_labels, _parse_validation_response, validate_infographic
- `tests/test_generate_infographic.py` - Added TestPlaceholder, TestPromptJson, TestErrorClassification, TestContentBlock classes (21 new tests)
- `tests/test_validation.py` - New test file with TestLabelExtraction, TestResponseParsing, TestValidateInfographic classes (17 new tests)
- `tests/conftest.py` - Added mock_content_blocked_response, mock_candidate_blocked_response, mock_validation_pass_response, mock_validation_fail_response fixtures

## Decisions Made
- Used `ImageFont.load_default(size=36)` as primary font strategy with `try/except TypeError` fallback for older Pillow versions that lack the `size` parameter -- avoids hard dependency on Pillow >= 10.4
- Validation API errors return `passed=True, warning_only=True` -- validation failure should never block generation (non-blocking quality gate)
- Content block detection checks both `response.prompt_feedback.block_reason` (prompt-level) and `response.candidates[0].finish_reason` (candidate-level) against CONTENT_BLOCK_REASONS set
- Label extraction uses heuristic: splits on ", " only when followed by an uppercase letter, preventing false splits on values like "mild dissent"
- ServerError constructor takes `response_json` dict, not `message` string (verified from SDK source)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] ServerError constructor signature mismatch**
- **Found during:** Task 1 (writing test for ServerError handling)
- **Issue:** Plan's test example used `ServerError(code=503, message="...")` but actual SDK constructor requires `response_json` parameter
- **Fix:** Updated test to use `ServerError(code=503, response_json={"error": {"message": "Service Unavailable"}})`
- **Files modified:** tests/test_generate_infographic.py
- **Verification:** Test passes with correct constructor
- **Committed in:** cf1d816 (Task 1 RED commit)

---

**Total deviations:** 1 auto-fixed (1 bug fix)
**Impact on plan:** Minor correction to match actual SDK API. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All building blocks ready for Plan 02's retry loop and session orchestrator
- create_placeholder_png available for total failure and content block placeholders
- save_prompt_json available for error metadata preservation
- Error classification helpers (_is_retryable_error, _is_content_block) ready for retry decisions
- validate_infographic ready for post-generation quality checks
- Content block detection integrated into generate_infographic response flow

## Self-Check: PASSED

- All 5 files exist (2 created, 3 modified)
- All 4 task commits verified (cf1d816, 0641d82, 8eff981, 223414e)
- All exports importable from both modules
- 93 tests pass (38 new, 55 existing unaffected)

---
*Phase: 03-error-handling-and-quality*
*Completed: 2026-03-04*
