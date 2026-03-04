---
phase: 02-api-integration
plan: 01
subsystem: api
tags: [gemini, prompt-engineering, json, template-serialization, regex]

# Dependency graph
requires:
  - phase: 01-config-preflight
    provides: ConfigError class for structured error handling
provides:
  - load_template function for JSON template loading by type slug
  - substitute_placeholders function for {{TOKEN}} regex replacement
  - serialize_template function flattening JSON + data to natural language prompt
  - save_prompt function for writing prompt files to disk
  - PLACEHOLDER_RE compiled regex pattern
affects: [02-api-integration, 03-orchestration, 04-integration]

# Tech tracking
tech-stack:
  added: []
  patterns: [template-to-prompt serialization, placeholder regex substitution, natural language prompt assembly]

key-files:
  created:
    - scripts/generate_infographic.py
    - tests/test_generate_infographic.py
  modified:
    - tests/conftest.py

key-decisions:
  - "Descriptive paragraphs over keyword lists for prompt structure (per Google guidance and CONTEXT.md)"
  - "Inline data substitution within template sections rather than a separate data block"
  - "Unknown placeholders resolve to [TOKEN] bracketed form for visibility without breaking prompts"
  - "load_template accepts template_dir kwarg for test isolation"

patterns-established:
  - "Template loading with slug normalization (underscores to hyphens, lowercase, strip)"
  - "Regex-based placeholder substitution with fallback for missing keys"
  - "Section-based prompt assembly: subject, objects, notes, constraints, style, colors, extras data, quality, style override"

requirements-completed: [GEN-02]

# Metrics
duration: 3min
completed: 2026-03-04
---

# Phase 2 Plan 1: Prompt Serialization Summary

**JSON template to natural language prompt pipeline with regex placeholder substitution, hex color inclusion, and style override support**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-04T14:39:15Z
- **Completed:** 2026-03-04T14:42:15Z
- **Tasks:** 1 (TDD: RED + GREEN)
- **Files modified:** 3

## Accomplishments
- Built complete prompt serialization pipeline: load JSON templates by slug, substitute {{TOKEN}} placeholders with data values, flatten to natural language paragraphs
- Hex color codes from extras.color_mapping included in serialized prompts for brand consistency
- Style override support: .cdp-context/style.md content can be appended as additional guidance
- save_prompt writes INFOGRAPHIC_{slug}_PROMPT.txt alongside generation output for debugging

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Prompt serialization tests** - `cecf4e2` (test)
2. **Task 1 GREEN: Prompt serialization implementation** - `cdb7902` (feat)

_TDD task: RED wrote 22 failing tests, GREEN implemented passing code._

## Files Created/Modified
- `scripts/generate_infographic.py` - Core prompt serialization module: load_template, substitute_placeholders, serialize_template, save_prompt
- `tests/test_generate_infographic.py` - 22 tests in TestPromptSerialization covering all serialization behaviors
- `tests/conftest.py` - Added fixtures: sample_template, sample_data, sample_template_path

## Decisions Made
- Structured prompt as descriptive paragraphs: subject line, data elements, context notes, constraints, style, color coding, supplementary data, quality cues -- following Google's recommendation that descriptive paragraphs produce better Gemini images than keyword lists
- Inline data substitution within template sections rather than a separate data block -- keeps context close to where data appears
- Unknown placeholders resolve to [TOKEN] in brackets rather than raising errors -- makes missing data visible without breaking the prompt
- load_template accepts an optional template_dir keyword argument for test isolation without monkeypatching

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Prompt serialization pipeline ready for Phase 2 Plans 2-3 (API call integration and CLI wrapper)
- load_template, substitute_placeholders, serialize_template are all importable for use in generate_infographic() function
- save_prompt ready for use in the generation flow to save prompts alongside PNGs
- Full test suite (42 tests) remains green with no regressions

## Self-Check: PASSED

- [x] scripts/generate_infographic.py exists
- [x] tests/test_generate_infographic.py exists
- [x] tests/conftest.py exists
- [x] Commit cecf4e2 (RED) exists
- [x] Commit cdb7902 (GREEN) exists
- [x] All 5 exports importable (load_template, substitute_placeholders, serialize_template, save_prompt, PLACEHOLDER_RE)

---
*Phase: 02-api-integration*
*Completed: 2026-03-04*
