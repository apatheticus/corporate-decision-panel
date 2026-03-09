# Technology Stack: v1.4 Team Refactor

**Project:** CDP v1.4 Team Refactor
**Researched:** 2026-03-08
**Confidence:** HIGH (all changes are to existing codebase patterns; no new dependencies required)

## Executive Summary

The v1.4 milestone addresses 6 fixes from the 2026-03-08 production session error logs plus 2 documentation additions. The critical finding is: **zero new library dependencies are needed**. Every fix operates within the existing technology footprint -- Python stdlib, existing `google-genai` SDK, Pillow, reportlab, and pytest. The changes fall into two categories: (1) Python code modifications to existing scripts (`validation.py`, `generate_infographic.py`, `session.py`), and (2) markdown specification rewrites across 48+ agent/config files.

This is deliberate. CDP's deliberation engine is a prompt-and-configuration system. The Python scripts handle only infographic generation, validation, and PDF building. The team dispatch architecture, slug resolution, logging protocol, and validation leniency are all solvable within existing patterns. Adding dependencies would be an anti-pattern for this system.

## Recommended Stack

### Core Framework (Unchanged)

| Technology | Version | Purpose | Why Unchanged |
|------------|---------|---------|---------------|
| Python | 3.10+ | Scripts: config, preflight, generation, validation, session, PDF | All 6 code-touching fixes modify existing Python files. No new Python features required beyond what 3.10+ provides (union types via `from __future__ import annotations`). |
| Markdown specifications | N/A | 48 agent definitions + 4 config protocols | Division team dispatch, logging protocol, and large file guidance are pure markdown specification changes. |
| Claude Code skill framework | Current | Agent definitions, slash commands, orchestration | TeamCreate, Agent, SendMessage tools are platform-provided. The refactor changes WHO calls them (CEO instead of C-suite), not HOW they work. |

### Image Generation Pipeline (Unchanged)

| Technology | Version | Purpose | Why Unchanged |
|------------|---------|---------|---------------|
| google-genai | >=1.65.0 | Gemini API for infographic generation + vision validation | Validation leniency (Fix 5) changes the prompt text sent to the same API, not the SDK usage pattern. Slug aliases (Fix 1) resolve before any API call. |
| Pillow | >=10.0.0 | Placeholder PNG generation, image manipulation | No changes to Pillow usage. |
| reportlab | (existing) | PDF generation via `build_results_pdf.py` | Fix 2 (PDF module path) changes the invocation command in a markdown agent definition, not the Python code. |
| pytest | >=8.0.0 | Test suite for all scripts | New tests for slug aliases and validation leniency follow existing mock patterns. |

### Infrastructure (Unchanged)

| Technology | Version | Purpose | Why Unchanged |
|------------|---------|---------|---------------|
| Git | Current | Version control | Standard. |
| pathlib | stdlib | File system operations | Already used throughout. Sub-question file I/O uses same patterns. |
| json | stdlib | Data serialization | Template loading, data paths -- unchanged. |
| re | stdlib | Regex for slug normalization | Already used in `load_template()` and `config.py`. |

## What Changes (Code Only)

The v1.4 changes touch Python code in only three files. Here is exactly what changes and why no new dependencies are needed:

### Fix 1: Slug Alias Resolution (`generate_infographic.py`, `session.py`)

**What:** Add a `SLUG_ALIASES` dict mapping shorthand slugs to canonical template names.

**Pattern:** Dict lookup -- the most basic Python pattern. Applied at the entry points of `load_template()`, `generate_with_retry()`, and `run_session()`.

```python
# New constant after ASPECT_RATIOS (line ~64)
SLUG_ALIASES: dict[str, str] = {
    "fault-lines": "fault-line-map",
    "risk-matrix": "risk-opportunity-matrix",
    "action-plan": "action-plan-timeline",
}
```

**Resolution point:** Early in each function, before any template file lookup:
```python
type_slug = SLUG_ALIASES.get(type_slug, type_slug)
```

**Why no library needed:** This is a 4-line constant + 1-line resolution per function. Using a library for string aliasing would be absurd over-engineering. The existing `load_template()` already normalizes underscores to hyphens; aliases extend this pattern.

**Test pattern:** Follows existing `test_load_template_normalizes_underscores` test in `test_generate_infographic.py`. Add parametrized tests for each alias.

### Fix 5: Validation Leniency (`validation.py`, `generate_infographic.py`)

**What:** Add `type_slug` parameter to `validate_infographic()`. For types in a `LENIENT_TYPES` set, modify the validation prompt to accept PARTIAL labels.

**Pattern:** Conditional prompt text based on set membership. Same pattern as `THINKING_TYPES` in `generate_infographic.py`.

```python
# New constant in validation.py
LENIENT_TYPES: set[str] = {"routing-diagram"}

# Modified prompt construction (within validate_infographic)
if type_slug and type_slug in LENIENT_TYPES:
    verdict_rules = (
        "VERDICT RULES (lenient -- high-density infographic):\n"
        "- FAIL if any label is MISSING\n"
        "- FAIL if any garbled/misspelled text is found\n"
        "- PASS if all labels are FOUND or PARTIAL and no garbled text exists\n"
        "- A PARTIAL label is acceptable for this infographic type\n"
    )
else:
    verdict_rules = (
        "VERDICT RULES:\n"
        "- FAIL if any label is MISSING or PARTIAL\n"
        "- FAIL if any garbled/misspelled text is found\n"
        "- PASS only when all labels are FOUND and no garbled text exists\n"
    )
```

**Caller change:** In `generate_with_retry()` (line ~823), pass `type_slug`:
```python
validation = validate_infographic(
    result.output_path, data_path, config_dir, type_slug=type_slug
)
```

**Why no library needed:** This is prompt text variation, not a new capability. The validation infrastructure (API call, response parsing, result dataclass) is unchanged.

**Test pattern:** Follows existing `TestValidateInfographic` class. Add tests verifying lenient prompt text when `type_slug="routing-diagram"` and strict prompt when `type_slug=None` or non-lenient type.

### Fix 2: PDF Module Path (markdown only)

**What:** Change the invocation command in `agents/team-leads/cco/publisher.md` to `cd <skill-directory> && python3 -m scripts.build_results_pdf --session-dir {session}`.

**Why no code change:** The Python script works correctly. The problem was the agent's working directory when invoking it. This is a 1-line markdown edit.

## What Changes (Markdown Specifications)

### Fix 3: Inline Logging Protocol (48 files)

**What:** Replace `config/logging-protocol.md` file-path references in all 48 agent definitions with an inline summary of the logging protocol.

**Current pattern (in each agent file):**
```
follow the error logging protocol at `config/logging-protocol.md`
```

**New pattern (inline in each agent file):**
```
follow the error logging protocol: if `LOGGING: ON` and `SESSION PATH:` appear in
your prompt, write `{session-path}/logs/errors-{YYYYMMDD-HHmm}-{agent-name}.md` as
your last action before SendMessage/TaskUpdate. Log only tool failures, workarounds,
data quality issues, or instruction ambiguity. If no issues, do not create a log file.
```

**Why inline, not fix the path:** The logging protocol was already designed so agents do NOT need to read the file -- the CEO broadcasts `LOGGING: ON` and `SESSION PATH:` in prompts. Agents were reading the file because the reference was ambiguous enough to trigger a file-read attempt. Inlining eliminates the dependency entirely. The `config/logging-protocol.md` file remains as the canonical reference for human maintainers.

**Stack implication:** None. Pure text replacement across 48 files.

### Fix 4: Division Team Dispatch Architecture (12+ files)

**What:** Rewrite dispatch architecture so CEO creates all teams and dispatches all agents. C-suite agents become teammates who write sub-question files instead of using TeamCreate/Agent tools.

**Files affected:**
- `config/dispatch-protocol.md` -- complete rewrite
- `config/cco-dispatch-protocol.md` -- rewrite for CEO-managed waves
- `config/orchestration-protocol.md` -- update Phases 2/3/4 + Production Spawn Sequence
- `agents/ceo.md` -- add TeamCreate, team lead dispatch, CCO wave management
- `agents/c-suite/*.md` (9 files) -- transform Mode B dispatch sections

**New file-based coordination pattern:**
```
{session}/sub-questions/{role}/{team-lead-name}.md
```

C-suite agents write sub-question files. CEO polls for them. CEO dispatches team leads with sub-question content in their prompts. Team leads SendMessage findings to C-suite agents. C-suite agents synthesize into `_RECOMMENDATION_{role}.md`.

**Stack implication:** None. This uses Claude Code's existing Agent, TeamCreate, and SendMessage tools -- just rearranges which agent calls which tool. The file-based coordination pattern uses standard filesystem operations (Write tool for agents, Read tool for CEO polling).

**New directory in session output:**
```bash
mkdir -p .cdp-output/YYYY-MM-DD_<issue-slug>/sub-questions
```

This follows the existing pattern for session directory creation (see `config/orchestration-protocol.md` Session Output Setup section).

### Fix 6: Large File Read Guidance (2 files)

**What:** Add notes in `config/orchestration-protocol.md` and `agents/ceo.md` about using Read tool with `offset`/`limit` parameters for large recommendation files.

**Stack implication:** None. Documents an existing Claude Code tool parameter.

## What NOT to Add

| Rejected Addition | Why Not |
|-------------------|---------|
| File watcher / inotify library for sub-question polling | Claude Code agents use the Read tool for file access. There is no event loop to integrate inotify with. CEO polls directories via `ls` / `Glob`, which is the correct pattern for agent-based file coordination. |
| Message queue (Redis, RabbitMQ) for inter-agent communication | Claude Code provides SendMessage for teammate communication. Adding infrastructure dependencies for what is already a platform feature would be wrong. |
| YAML/TOML for sub-question files | Sub-question files are markdown documents consumed by LLM agents, not structured data consumed by code. Markdown is the correct format. |
| Fuzzy string matching library (fuzzywuzzy, rapidfuzz) for slug aliases | The alias set is fixed and small (3 entries). A dict lookup is sufficient. Fuzzy matching would introduce false positives for unknown slug typos that should fail loudly. |
| Schema validation library (pydantic, marshmallow) for sub-question file format | Sub-question files are free-form markdown written by LLM agents and read by LLM agents. Schema validation of LLM-generated markdown is a solved problem (it is not solvable). The format is a convention, not a schema. |
| Logging framework (structlog, loguru) for inline logging protocol | Agent logging is file-based markdown. The agents use Write/Bash tools, not Python logging. A Python logging framework is irrelevant to agent-side logging. |
| pytest-xdist for parallel test execution | The test suite is fast enough (<5 seconds). Parallelization adds complexity for no measurable benefit. |
| Additional Gemini models for validation | The validation uses the same model configured for generation. Adding model selection for validation would complicate config for no proven benefit -- the leniency fix addresses the actual problem (prompt strictness, not model capability). |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Slug resolution | Dict alias map in `generate_infographic.py` | Fix only the graphic-designer agent definition (correct the slugs) | Belt-and-suspenders: fixing the agent definition prevents the known case, but aliases defend against future shorthand mistakes by any agent. Cost is 4 lines. |
| Slug resolution | Early resolution in `load_template()` + `generate_with_retry()` + `run_session()` | Resolution only in `session.py` | Template loading should also resolve aliases for direct CLI usage. Applying at all entry points is more robust. |
| Validation leniency | `type_slug` parameter + `LENIENT_TYPES` set | Global leniency toggle in config.md | Per-type leniency is correct because only high-density infographics need it. Global leniency would mask real validation failures in simpler types. |
| Validation leniency | Conditional prompt text | Separate lenient validation function | Single function with conditional prompt is simpler and follows the existing pattern (one validate_infographic function, not two). |
| Logging protocol | Inline summary in each agent file | Fix the file path to be absolute/resolvable | Agents do not need the file -- the CEO broadcasts logging status. Fixing the path just makes an unnecessary file read succeed. Inlining eliminates the read entirely. |
| Inter-agent coordination | File-based sub-question convention | Direct SendMessage from C-suite to CEO with sub-questions | CEO would need to parse sub-questions from messages and match them to the correct division. File-based convention gives the CEO explicit paths to poll and read, which is simpler and more reliable. |
| Inter-agent coordination | CEO polls for sub-question files | C-suite agents signal completion via SendMessage | Both can coexist. CEO can watch for both file appearance AND completion messages. But the file is the source of truth because it contains the sub-question content. |
| PDF module path fix | `cd <skill-directory> &&` prefix in agent definition | Add `sys.path` manipulation to `build_results_pdf.py` | Changing the script's working directory in the invocation command is cleaner than hardcoding path manipulation in Python. The script is correct; the invocation context was wrong. |

## Installation

```bash
# No new dependencies. Existing environment is sufficient.
pip install -r requirements.txt        # google-genai>=1.65.0, Pillow>=10.0.0 (unchanged)
pip install -r requirements-dev.txt    # pytest>=8.0.0 (unchanged)

# Verify existing setup:
python -m pytest tests/ --tb=short    # Should pass existing tests

# After v1.4 changes:
python -m pytest tests/ --tb=short    # Should pass existing + new tests for aliases/leniency
```

## Test Strategy

New tests follow existing patterns exactly:

| Fix | Test File | Test Pattern | Mock Strategy |
|-----|-----------|--------------|---------------|
| Slug aliases | `test_generate_infographic.py` | `test_load_template_normalizes_underscores` pattern | No mock needed -- `load_template()` with alias slugs against real template dir |
| Slug aliases | `test_session.py` | New `TestSlugAliasResolution` class | Mock `generate_with_retry` to verify resolved slug is passed |
| Validation leniency | `test_validation.py` | `TestValidateInfographic` pattern | Mock `genai.Client` as existing tests do; verify prompt text contains "lenient" for routing-diagram |
| Validation leniency | `test_validation.py` | New `TestLenientValidation` class | Verify PARTIAL labels pass for lenient types, fail for strict types |

**No new test dependencies.** pytest, unittest.mock, PIL, and pathlib cover everything.

## Integration Points

### Slug Aliases Touch Points

1. `generate_infographic.py` -- `SLUG_ALIASES` constant + resolution in `load_template()`, `generate_with_retry()`
2. `session.py` -- resolution in `run_session()` before passing to downstream
3. `agents/team-leads/cco/graphic-designer.md` -- fix the canonical slugs (prevents the alias from firing)
4. Tests: `test_generate_infographic.py`, `test_session.py`

### Validation Leniency Touch Points

1. `validation.py` -- `LENIENT_TYPES` constant + `type_slug` parameter + conditional prompt
2. `generate_infographic.py` -- pass `type_slug` to `validate_infographic()` call (line ~823)
3. Tests: `test_validation.py`

### Division Team Dispatch Touch Points

1. `config/dispatch-protocol.md` -- complete rewrite (source of truth for sub-question file convention)
2. `config/cco-dispatch-protocol.md` -- rewrite (CEO-managed wave sequencing)
3. `config/orchestration-protocol.md` -- Phases 2/3/4 + Production Spawn Sequence updates
4. `agents/ceo.md` -- TeamCreate instructions, sub-question polling, team lead dispatch
5. `agents/c-suite/*.md` (9 files) -- Mode B step 3/4 transformation
6. `config/orchestration-protocol.md` Session Output Setup -- add `sub-questions/` directory

### Inline Logging Protocol Touch Points

1. All 48 agent files in `agents/` -- replace `config/logging-protocol.md` reference with inline summary
2. `config/logging-protocol.md` -- unchanged (remains as canonical reference for maintainers)

## Dependency Graph

```
Fix 1 (slug aliases) -----> independent, do first
Fix 2 (PDF path) ---------> independent, do first
Fix 5 (validation) -------> independent, do after Fix 1 (same files touched)
Fix 3 (logging inline) ---> independent, bulk operation
Fix 4 (dispatch arch) ----> depends on nothing, but is largest change
Fix 6 (large file) -------> depends on Fix 4 (adds to same files Fix 4 rewrites)
```

Fixes 1, 2, and 5 are code changes (Python). Fixes 3, 4, and 6 are specification changes (markdown). They can proceed in parallel tracks, with Fix 6 applied after Fix 4 to avoid merge conflicts in `orchestration-protocol.md` and `ceo.md`.

## Sources

- `scripts/generate_infographic.py` -- existing slug normalization, ASPECT_RATIOS, THINKING_TYPES patterns (direct reading)
- `scripts/validation.py` -- existing validate_infographic signature, prompt construction (direct reading)
- `scripts/session.py` -- existing run_session flow (direct reading)
- `scripts/config.py` -- existing config loading pattern (direct reading)
- `scripts/build_results_pdf.py` -- PDF generation script (direct reading)
- `config/dispatch-protocol.md` -- current dispatch architecture (direct reading)
- `config/cco-dispatch-protocol.md` -- current CCO dispatch architecture (direct reading)
- `config/orchestration-protocol.md` -- current phase sequencing (direct reading)
- `config/logging-protocol.md` -- current logging protocol (direct reading)
- `agents/ceo.md` -- current CEO agent definition (direct reading)
- `agents/c-suite/cfo.md` -- C-suite Mode B dispatch pattern template (direct reading)
- `ref/team-refactor-context-260308.md` -- error log analysis and architectural options (direct reading)
- `ref/team-refactor-plan-260308.md` -- implementation plan with file-level changes (direct reading)
- `tests/test_validation.py`, `tests/test_session.py`, `tests/test_generate_infographic.py` -- existing test patterns (direct reading)
- `tests/conftest.py` -- shared fixtures (direct reading)
- `requirements.txt`, `requirements-dev.txt` -- current dependencies (direct reading)
