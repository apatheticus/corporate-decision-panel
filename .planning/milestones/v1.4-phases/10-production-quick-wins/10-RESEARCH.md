# Phase 10: Production Quick Wins - Research

**Researched:** 2026-03-08
**Domain:** Infographic pipeline bug fixes (Python scripts + agent markdown definitions)
**Confidence:** HIGH

## Summary

Phase 10 addresses four specific failures observed in the 2026-03-08 production session. All four are localized code/config fixes with no architectural changes required. The fixes span two Python modules (`generate_infographic.py`, `validation.py`), one orchestration module (`session.py` -- indirectly, through the alias map), and one agent markdown definition (`publisher.md`).

The codebase is well-structured with consistent patterns: module-level constant dicts for configuration, clear function signatures, comprehensive tests (161 passing, 2 live-only deselected). Every change maps cleanly to an existing pattern. The graphic designer agent definition (`graphic-designer.md`) requires no changes -- it already uses shorthand slugs, and the alias map handles resolution transparently.

**Primary recommendation:** Implement all four fixes as independent, testable changes. Add shorthand entries to `ASPECT_RATIOS`, add `SLUG_ALIASES` dict resolved in `load_template()`, add `type_slug` parameter to `validate_infographic()` with `LENIENT_TYPES` set, and prefix the publisher's `build_results_pdf` invocation with `cd <skill-directory> &&`.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions

- **Slug alias resolution**: Static `SLUG_ALIASES` dict at module level in `generate_infographic.py`, resolved inside `load_template()` only. Three aliases: `fault-lines` -> `fault-line-map`, `risk-matrix` -> `risk-opportunity-matrix`, `action-plan` -> `action-plan-timeline`. Alias resolves for template file lookup only -- output filenames use the original slug the caller passed. `ASPECT_RATIOS` dict gets shorthand entries added rather than resolving aliases at that layer.
- **Output filename convention**: Keep shorthand filenames (`INFOGRAPHIC_fault-lines.png`, etc.). No downstream reference changes needed. The alias is purely internal for template file resolution.
- **Graphic designer slugs**: Graphic designer keeps shorthand slugs in `types_list` and `data_paths` -- the alias map handles template resolution. INFRA-02 scope adjusted: "graphic designer uses slugs that the alias map can resolve" rather than "uses canonical slugs directly". No changes needed to graphic designer's data JSON filenames.
- **Validation leniency**: `validate_infographic()` gains a `type_slug` parameter (optional, default None). `LENIENT_TYPES = {'routing-diagram'}` set at module level in `validation.py`. For lenient types, PARTIAL labels count as pass (no warning, no retry trigger). Garbled text detection stays strict for all types. Caller (`generate_with_retry`) passes the original slug -- no alias resolution at validation layer. `routing-diagram` has no alias (already canonical), so this works cleanly.
- **Publisher path fix**: Add `cd <skill-directory> &&` prefix to `python3 -m scripts.build_results_pdf` invocation in publisher.md. `<skill-directory>` placeholder matches existing pattern in graphic-designer.md.

### Claude's Discretion

- Whether capsule PDF build script (`python3 {session}/build/build_capsule.py`) also needs the `cd` fix
- Exact placement of SLUG_ALIASES dict relative to other constants
- Test coverage approach for alias resolution and validation leniency

### Deferred Ideas (OUT OF SCOPE)

None -- discussion stayed within phase scope.

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| INFRA-01 | Slug alias map resolves shorthand slugs to canonical template slugs in `generate_infographic.py` and `session.py` | `SLUG_ALIASES` dict in `generate_infographic.py`, resolved in `load_template()`. `session.py` receives shorthand slugs and passes them through; `generate_infographic()` normalizes via `load_template()`. `ASPECT_RATIOS` gets shorthand entries directly. |
| INFRA-02 | Graphic designer agent definition uses correct canonical slugs | Scope adjusted per CONTEXT.md: graphic designer keeps shorthand slugs. Alias map resolves them. No changes to `graphic-designer.md` needed. |
| INFRA-03 | Validation accepts PARTIAL labels for high-density infographic types without triggering failure | `LENIENT_TYPES` set in `validation.py`. `_parse_validation_response` already parses PARTIAL as `warning_only=True`. Leniency logic overrides `warning_only` to False for lenient types (making PARTIAL count as clean pass). |
| INFRA-04 | `validate_infographic()` accepts `type_slug` parameter and applies lenient validation conditionally | New optional `type_slug` parameter on `validate_infographic()`. When `type_slug in LENIENT_TYPES`, PARTIAL labels and `warning_only=True` are treated as clean pass. Garbled text stays strict. |
| AGINF-01 | Publisher agent uses `cd <skill-directory> &&` prefix for `python3 -m scripts.build_results_pdf` invocation | Single-line edit in `agents/team-leads/cco/publisher.md` step 5. |

</phase_requirements>

## Standard Stack

### Core (no new dependencies)

| Library | Version | Purpose | Status |
|---------|---------|---------|--------|
| Python | 3.14 | Runtime | Already installed |
| pytest | installed | Test framework | 161 tests passing |
| reportlab | installed | PDF generation | Used by `build_results_pdf.py` |
| Pillow | installed | Image manipulation | Used by `generate_infographic.py` |
| google-genai | installed | Gemini API client | Used by pipeline |

No new packages are needed. All changes are to existing files.

### Files to Modify

| File | Change Type | Lines Affected |
|------|-------------|----------------|
| `scripts/generate_infographic.py` | Add `SLUG_ALIASES` dict, resolve in `load_template()`, add shorthand entries to `ASPECT_RATIOS`, pass `type_slug` to `validate_infographic()` | ~10 lines added |
| `scripts/validation.py` | Add `LENIENT_TYPES` set, add `type_slug` parameter to `validate_infographic()`, apply leniency logic after parsing | ~12 lines added |
| `agents/team-leads/cco/publisher.md` | Prefix `build_results_pdf` command with `cd <skill-directory> &&` | 1 line changed |
| `tests/test_generate_infographic.py` | Add tests for alias resolution and aspect ratio lookup | ~30 lines added |
| `tests/test_validation.py` | Add tests for lenient validation behavior | ~40 lines added |

## Architecture Patterns

### Existing Pattern: Module-Level Constant Dicts

The codebase uses module-level constant dicts extensively for configuration. All new constants follow this pattern.

**Current examples (lines 57-76 of `generate_infographic.py`):**
```python
ASPECT_RATIOS: dict[str, str] = {
    "domain-scorecard":        "4:3",
    "risk-opportunity-matrix": "4:3",
    "routing-diagram":         "16:9",
    "fault-line-map":          "16:9",
    "mode-comparison":         "16:9",
    "action-plan-timeline":    "16:9",
}

THINKING_TYPES: set[str] = {"fault-line-map", "mode-comparison"}
```

**New constants follow this exact pattern:**
```python
# Place after TEMPLATE_DIR, before PLACEHOLDER_RE (or after ASPECT_RATIOS)
SLUG_ALIASES: dict[str, str] = {
    "fault-lines": "fault-line-map",
    "risk-matrix": "risk-opportunity-matrix",
    "action-plan": "action-plan-timeline",
}

# Add to existing ASPECT_RATIOS:
ASPECT_RATIOS: dict[str, str] = {
    "domain-scorecard":        "4:3",
    "risk-opportunity-matrix": "4:3",
    "routing-diagram":         "16:9",
    "fault-line-map":          "16:9",
    "mode-comparison":         "16:9",
    "action-plan-timeline":    "16:9",
    # Shorthand aliases (same ratios as their canonical counterparts)
    "fault-lines":             "16:9",
    "risk-matrix":             "4:3",
    "action-plan":             "16:9",
}
```

### Pattern: Slug Normalization in load_template()

`load_template()` already normalizes slugs (line 134):
```python
slug = infographic_type.lower().replace("_", "-").strip()
```

Alias resolution adds one line after normalization:
```python
slug = infographic_type.lower().replace("_", "-").strip()
slug = SLUG_ALIASES.get(slug, slug)  # Resolve shorthand aliases
```

This is the ONLY place alias resolution happens. The function then uses `slug` for template file lookup but does NOT change the caller's `infographic_type`. Output filenames continue to use the original (shorthand) slug because `generate_infographic()` uses `type_slug` (line 603) which is normalized but NOT alias-resolved.

### Pattern: Optional Parameters with Default None

`validate_infographic()` gains an optional parameter:
```python
def validate_infographic(
    image_path: Path,
    data_path: Path,
    config_dir: Path,
    type_slug: str | None = None,  # New optional parameter
) -> ValidationResult:
```

This preserves backward compatibility -- all existing callers pass positional args for the first three parameters.

### Pattern: Agent Placeholder Convention

Agent markdown files use `<skill-directory>` and `{session}` as dispatcher-filled placeholders. The graphic designer already demonstrates this (line 49):
```python
sys.path.insert(0, '<skill-directory>')
```

The publisher fix follows this exact convention:
```bash
cd <skill-directory> && python3 -m scripts.build_results_pdf --session-dir {session}
```

### Anti-Patterns to Avoid

- **Alias resolution in multiple places:** The alias MUST only resolve in `load_template()`. Do NOT add alias resolution to `generate_infographic()`, `generate_with_retry()`, `run_session()`, or `validate_infographic()`. The whole point is that shorthand slugs flow through the system untouched for output filenames.
- **Modifying ASPECT_RATIOS to do alias lookup:** Per CONTEXT.md decision, add shorthand entries directly to `ASPECT_RATIOS` rather than resolving aliases at that layer. Simpler, no dependency between constants.
- **Changing graphic-designer.md:** Per CONTEXT.md decision, graphic designer keeps shorthand slugs. No changes needed.
- **Alias resolution in validation layer:** Per CONTEXT.md decision, `routing-diagram` is already canonical (no alias needed). The `type_slug` parameter receives whatever slug the caller passes.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Slug normalization | Custom fuzzy matching | Static `SLUG_ALIASES` dict | Only 3 known mismatches; explicitly out of scope per REQUIREMENTS.md |
| Per-type validation profiles | Complex profile configuration | `LENIENT_TYPES` set membership check | Only 1 known lenient type; set is extensible if needed later |

## Common Pitfalls

### Pitfall 1: Alias Resolution Leaking Into Output Filenames

**What goes wrong:** If alias resolution happens in `generate_infographic()` or `generate_with_retry()` instead of `load_template()`, output filenames change from `INFOGRAPHIC_fault-lines.png` to `INFOGRAPHIC_fault-line-map.png`, breaking downstream references.
**Why it happens:** Natural instinct is to normalize early.
**How to avoid:** Alias resolution ONLY in `load_template()`. The `type_slug` variable in `generate_infographic()` (line 603) uses the original slug, and `load_template(type_slug)` resolves internally.
**Warning signs:** Output PNG filenames using canonical slugs instead of shorthand slugs.

### Pitfall 2: Validation Leniency Suppressing Garbled Text

**What goes wrong:** If leniency makes ALL validation pass for lenient types, garbled text goes undetected.
**Why it happens:** Over-broad implementation of "lenient = pass everything."
**How to avoid:** Leniency only affects the `warning_only` flag (PARTIAL labels). Garbled text detection remains strict. The logic should be: after `_parse_validation_response()`, if `type_slug in LENIENT_TYPES` and result has `warning_only=True` (meaning PARTIAL labels), convert to clean pass. But if `result.garbled` is non-empty, do NOT apply leniency.
**Warning signs:** Garbled text infographics accepted for routing-diagram.

### Pitfall 3: Breaking the validate_infographic Call in generate_with_retry

**What goes wrong:** The existing call on line 823 is positional: `validate_infographic(result.output_path, data_path, config_dir)`. Adding `type_slug` as a non-optional parameter before `config_dir` would break this.
**Why it happens:** Inserting parameters in the wrong position.
**How to avoid:** Add `type_slug` as the LAST parameter with `None` as default. Update the call in `generate_with_retry` to pass it as a keyword argument: `validate_infographic(result.output_path, data_path, config_dir, type_slug=type_slug)`.
**Warning signs:** Existing tests failing after signature change.

### Pitfall 4: Publisher cd Fix Breaking Capsule Build

**What goes wrong:** The capsule build command `python3 {session}/build/build_capsule.py` uses an absolute path to a per-session script, so it does NOT need the `cd` fix. Applying `cd` there is unnecessary but harmless.
**Why it happens:** Assuming all python commands need the same fix.
**How to avoid:** Only fix the `python3 -m scripts.build_results_pdf` command, which uses `-m` (module import) that requires the correct working directory. The capsule script uses an absolute path and does not depend on cwd for module resolution.
**Recommendation for Claude's Discretion:** The capsule build script does NOT need the cd fix because `python3 {session}/build/build_capsule.py` uses a full path, not `-m` module syntax. However, if the capsule script internally imports from `scripts.*`, it WOULD fail. Since the capsule script is written per-session by the publisher agent (not a permanent script), its imports are self-contained. No cd fix needed for capsule.

## Code Examples

### 1. SLUG_ALIASES Dict and load_template() Resolution

```python
# In generate_infographic.py, after TEMPLATE_DIR constant (line 53):

SLUG_ALIASES: dict[str, str] = {
    "fault-lines": "fault-line-map",
    "risk-matrix": "risk-opportunity-matrix",
    "action-plan": "action-plan-timeline",
}

# In load_template(), after normalization (line 134):
def load_template(
    infographic_type: str,
    *,
    template_dir: Path | None = None,
) -> dict:
    base = template_dir if template_dir is not None else TEMPLATE_DIR
    slug = infographic_type.lower().replace("_", "-").strip()
    slug = SLUG_ALIASES.get(slug, slug)  # <-- NEW: resolve shorthand aliases
    path = base / f"{slug}.json"
    # ... rest unchanged
```

### 2. ASPECT_RATIOS Shorthand Entries

```python
ASPECT_RATIOS: dict[str, str] = {
    "domain-scorecard":        "4:3",
    "risk-opportunity-matrix": "4:3",
    "routing-diagram":         "16:9",
    "fault-line-map":          "16:9",
    "mode-comparison":         "16:9",
    "action-plan-timeline":    "16:9",
    # Shorthand aliases
    "fault-lines":             "16:9",
    "risk-matrix":             "4:3",
    "action-plan":             "16:9",
}
```

### 3. Validation Leniency in validation.py

```python
# Module-level constant after imports:
LENIENT_TYPES: set[str] = {"routing-diagram"}

# Updated function signature:
def validate_infographic(
    image_path: Path,
    data_path: Path,
    config_dir: Path,
    type_slug: str | None = None,
) -> ValidationResult:
    # ... existing code through _parse_validation_response ...

    result = _parse_validation_response(response.text)

    # Apply leniency for high-density types: PARTIAL labels count as clean pass
    # Garbled text detection stays strict for all types
    if (
        type_slug is not None
        and type_slug in LENIENT_TYPES
        and result.warning_only
        and not result.garbled
    ):
        result = ValidationResult(
            passed=True,
            warning_only=False,
            feedback=None,
            warnings=result.warnings,
            missing=result.missing,
            garbled=result.garbled,
        )

    # ... existing status output ...
```

### 4. generate_with_retry Caller Update

```python
# Line 823 in generate_infographic.py, existing:
validation = validate_infographic(
    result.output_path, data_path, config_dir
)

# Updated to:
validation = validate_infographic(
    result.output_path, data_path, config_dir, type_slug=type_slug
)
```

### 5. Publisher Path Fix

```markdown
<!-- In publisher.md, step 5, existing: -->
   ```bash
   python3 -m scripts.build_results_pdf --session-dir {session}
   ```

<!-- Updated to: -->
   ```bash
   cd <skill-directory> && python3 -m scripts.build_results_pdf --session-dir {session}
   ```
```

## State of the Art

No technology changes needed. This phase fixes bugs in existing, stable code.

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Graphic designer uses canonical slugs | Graphic designer uses shorthand slugs + alias map | Phase 10 (this phase) | Simpler agent definition, alias map handles mismatch |
| PARTIAL labels always trigger retry | PARTIAL labels pass for lenient types | Phase 10 (this phase) | Routing diagrams no longer waste retry budget |

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (latest) |
| Config file | `pytest.ini` |
| Quick run command | `python3 -m pytest tests/ -m "not live" -q --tb=short` |
| Full suite command | `python3 -m pytest tests/ -m "not live" -v` |

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INFRA-01 | `load_template('fault-lines')` resolves to `fault-line-map.json` template | unit | `python3 -m pytest tests/test_generate_infographic.py -k "alias" -x` | Wave 0 |
| INFRA-01 | `ASPECT_RATIOS['fault-lines']` returns `'16:9'` | unit | `python3 -m pytest tests/test_generate_infographic.py -k "aspect_ratio_shorthand" -x` | Wave 0 |
| INFRA-01 | Output filename uses shorthand slug, not canonical | unit | `python3 -m pytest tests/test_generate_infographic.py -k "output_filename_shorthand" -x` | Wave 0 |
| INFRA-02 | Graphic designer shorthand slugs work with alias map | unit | Covered by INFRA-01 alias test (same code path) | Wave 0 |
| INFRA-03 | `routing-diagram` with PARTIAL labels passes without failure | unit | `python3 -m pytest tests/test_validation.py -k "lenient" -x` | Wave 0 |
| INFRA-04 | `validate_infographic(type_slug='routing-diagram')` treats PARTIAL as clean pass | unit | `python3 -m pytest tests/test_validation.py -k "lenient_type" -x` | Wave 0 |
| INFRA-04 | Garbled text still fails for lenient types | unit | `python3 -m pytest tests/test_validation.py -k "garbled_strict_lenient" -x` | Wave 0 |
| INFRA-04 | Non-lenient types still fail on PARTIAL | unit | `python3 -m pytest tests/test_validation.py -k "non_lenient" -x` | Wave 0 |
| AGINF-01 | Publisher.md contains `cd <skill-directory> &&` before `build_results_pdf` | manual-only | Visual inspection of `agents/team-leads/cco/publisher.md` | N/A |

### Sampling Rate

- **Per task commit:** `python3 -m pytest tests/ -m "not live" -q --tb=short`
- **Per wave merge:** `python3 -m pytest tests/ -m "not live" -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_generate_infographic.py` -- add `TestSlugAliases` class: `test_alias_resolves_fault_lines`, `test_alias_resolves_risk_matrix`, `test_alias_resolves_action_plan`, `test_non_alias_unchanged`, `test_aspect_ratio_shorthand_entries`, `test_output_filename_uses_shorthand`
- [ ] `tests/test_validation.py` -- add `TestLenientValidation` class: `test_lenient_type_partial_passes_clean`, `test_lenient_type_garbled_still_fails`, `test_non_lenient_type_partial_still_warns`, `test_no_type_slug_backward_compatible`, `test_lenient_type_clean_pass_unchanged`

No framework install needed -- pytest is already configured and 161 tests pass.

## Open Questions

1. **Capsule PDF build script cd fix (Claude's Discretion)**
   - What we know: The capsule build command uses `python3 {session}/build/build_capsule.py` (absolute path), not `-m` module syntax. The capsule script is written per-session by the publisher, and its imports are self-contained (not importing from `scripts.*`).
   - What's unclear: Whether any future capsule scripts might import from `scripts.*`.
   - Recommendation: Do NOT add `cd` fix to capsule build. The command already uses an absolute path, and the script is self-contained. If a future capsule script needs `scripts.*` imports, that is a separate fix.

2. **SLUG_ALIASES placement (Claude's Discretion)**
   - Recommendation: Place `SLUG_ALIASES` immediately after `TEMPLATE_DIR` (line 53) and before `PLACEHOLDER_RE` (line 55). This groups it with template-related constants, since it is only used in `load_template()`.

## Sources

### Primary (HIGH confidence)

- Direct codebase analysis of `scripts/generate_infographic.py` (916 lines), `scripts/validation.py` (307 lines), `scripts/session.py` (208 lines)
- Direct codebase analysis of `agents/team-leads/cco/publisher.md`, `agents/team-leads/cco/graphic-designer.md`
- Template directory listing: 6 canonical JSON templates confirmed (`action-plan-timeline.json`, `domain-scorecard.json`, `fault-line-map.json`, `mode-comparison.json`, `risk-opportunity-matrix.json`, `routing-diagram.json`)
- Test suite: 161 tests passing across 6 test files, pytest.ini configured with `live` marker
- CONTEXT.md decisions from `/gsd:discuss-phase` session

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new dependencies, all existing code
- Architecture: HIGH -- patterns directly observed in codebase, changes follow existing conventions exactly
- Pitfalls: HIGH -- derived from actual code structure and call chains

**Research date:** 2026-03-08
**Valid until:** indefinite (internal codebase analysis, no external dependency concerns)
