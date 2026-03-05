# Technology Stack: v1.1 Initial Design Concerns

**Project:** CDP v1.1 Concern Fixes
**Researched:** 2026-03-04
**Confidence:** HIGH (all approaches verified against existing codebase patterns)

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Markdown specifications | N/A | All 11 concern fixes are spec documents or spec modifications | CDP is a prompt-and-configuration system. The deliberation engine has no application code. |
| Claude Code skill framework | Current | Agent definitions, slash commands, orchestration | Existing platform. No changes needed. |

### Scripting (Concern #8 only)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | 3.10+ | Session cleanup script | Consistent with existing v1.0 scripts (config.py, preflight.py, session.py, etc.) |
| pytest | Current | Tests for cleanup script | Consistent with existing test suite (188 tests) |
| pathlib | stdlib | File system operations | Already used throughout existing scripts |
| argparse | stdlib | CLI interface | Already used in preflight.py |
| shutil | stdlib | Directory removal | Standard library, no new dependency |

### Infrastructure

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Git | Current | Version control for spec changes | Existing. All concern fixes tracked as commits. |

## No New Dependencies

v1.1 introduces zero new dependencies. The only code addition (concern #8, session cleanup) uses Python standard library only. All other concerns are markdown specification documents.

This is deliberate. The CDP system's power comes from its specification architecture, not its code. Adding code dependencies to solve specification problems would be an anti-pattern.

## Approach by Concern Category

### Specification Extraction (#1 CEO Refactor)

**Approach:** Progressive disclosure via file references. CEO agent (682 lines) splits into core identity (~330 lines) plus referenced protocol specification (~350 lines). The CEO agent reads the extracted protocol via Claude Code's native file reference mechanism.

**Target structure:**
```
agents/ceo.md                          # ~330 lines: identity, mandate, synthesis, modes
config/orchestration-protocol.md       # ~350 lines: 5-phase cascade, production pipeline, session setup
```

**Why not subdirectory pattern (agents/ceo/*):** The orchestration protocol is configuration-adjacent (it defines procedural rules the CEO follows), making `config/` a natural home alongside `routing-table.md` and `decision-modes.md`.

### Specification Augmentation (#2, #3, #4, #5, #6, #7, #11)

**Approach:** Add sections to existing markdown files. No new tools, frameworks, or patterns needed. Each augmentation follows the existing document style and formatting conventions.

| Concern | Target File | Addition Type |
|---------|-------------|---------------|
| #2 Pre-Flight | Orchestration protocol | New section: "Production Pre-Flight" |
| #3 CSO Timeout | Orchestration protocol + CSO agent | New subsection in Phase 1.5 |
| #4 Executive Summaries | 7 C-suite agents | New output field in Mode B |
| #5 Routing Trees | `config/routing-table.md` | Expanded threshold conditions |
| #6 Mode Weightings | `config/decision-modes.md` | New weighting tables per mode |
| #7 Cost Formula | `config/decision-modes.md` | New "Cost Model" subsection |
| #11 Mode Sensitivity | `config/decision-modes.md` | Formalized criteria |

### New Components (#8 Session Cleanup)

**Approach:** Python script following existing patterns from v1.0 scripts.

| Pattern | Source | Applied to Cleanup |
|---------|--------|-------------------|
| Dataclass results | `GenerationResult`, `SessionResult` | `CleanupResult` |
| Structured status output | `_status()` in session.py | Same pattern for cleanup status |
| CLI with argparse | `preflight.py` | `--older-than`, `--dry-run`, `--confirm` |
| Config directory default | `.cdp-context` | `.cdp-output` |

### Test Scenarios (#9, #10, #11 tests)

**Approach:** Markdown specification documents, not automated tests. These are behavioral contracts with expected outcomes that require running actual deliberations to validate.

**Why not pytest:** LLM agent behavior is non-deterministic. Automated assertions about agent output produce false positives (always pass because structure is correct) or false negatives (fail because LLM phrasing varies). The value is in defining what SHOULD happen, not in asserting what DID happen.

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Cleanup implementation | Python script | Bash script | Python consistent with existing scripts, easier to test with pytest, pathlib for cross-platform |
| Cleanup implementation | Python script | Prompt-based (CEO follows cleanup protocol) | File enumeration, date math, and size calculation are more reliable in code |
| Test scenarios | Markdown spec documents | pytest automated tests | LLM outputs are non-deterministic. Cannot assert on specific agent responses. |
| Test scenarios | Markdown spec documents | DeepEval/LangChain eval framework | CDP does not call LLMs via API. It defines agent prompts. Eval frameworks solve a different problem. |
| Orchestration protocol location | `config/orchestration-protocol.md` | `agents/ceo/` subdirectory | Protocol is procedural configuration, not agent identity. `config/` is its natural home. |
| Orchestration protocol location | `config/orchestration-protocol.md` | Keep in `SKILL.md` | SKILL.md already has some orchestration content but is focused on invocation grammar. Adding 350 lines would exceed the recommended 500-line limit. |
| Mode weightings | Directional indicators (HIGH/MOD/LOW) | Numeric multipliers (1.5x, 0.7x) | LLMs cannot reliably apply numeric weights. False precision. |
| Routing formalization | Structured judgment with exemplars | Rigid decision trees | Over-formalization kills CEO routing judgment, a core design principle. |

## Installation

```bash
# No new dependencies. Existing environment is sufficient.
pip install -r requirements.txt        # google-genai, Pillow (unchanged)
pip install -r requirements-dev.txt    # pytest (unchanged)

# Verify existing setup:
python -m pytest tests/ --tb=short    # Should pass 188 tests

# After concern #8 is implemented:
python -m scripts.cleanup --help      # New cleanup script
python -m pytest tests/test_cleanup.py -v  # New tests
```

## Sources

- `.planning/PROJECT.md` -- v1.0 tech stack: Python, google-generativeai SDK, Pillow, pytest
- `requirements.txt`, `requirements-dev.txt` -- Current dependencies (direct reading)
- `scripts/*.py` -- Existing Python scripts and their patterns (direct reading)
- `agents/ceo.md` -- CEO agent structure for extraction analysis (direct reading)
- `config/*.md` -- Configuration file patterns (direct reading)
