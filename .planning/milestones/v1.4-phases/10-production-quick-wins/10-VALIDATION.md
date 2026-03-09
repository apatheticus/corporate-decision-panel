---
phase: 10
slug: production-quick-wins
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 10 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (latest) |
| **Config file** | `pytest.ini` |
| **Quick run command** | `python3 -m pytest tests/ -m "not live" -q --tb=short` |
| **Full suite command** | `python3 -m pytest tests/ -m "not live" -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python3 -m pytest tests/ -m "not live" -q --tb=short`
- **After every plan wave:** Run `python3 -m pytest tests/ -m "not live" -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 10-01-01 | 01 | 1 | INFRA-01 | unit | `python3 -m pytest tests/test_generate_infographic.py -k "alias" -x` | ❌ W0 | ⬜ pending |
| 10-01-02 | 01 | 1 | INFRA-01 | unit | `python3 -m pytest tests/test_generate_infographic.py -k "aspect_ratio_shorthand" -x` | ❌ W0 | ⬜ pending |
| 10-01-03 | 01 | 1 | INFRA-01 | unit | `python3 -m pytest tests/test_generate_infographic.py -k "output_filename_shorthand" -x` | ❌ W0 | ⬜ pending |
| 10-01-04 | 01 | 1 | INFRA-02 | unit | Covered by INFRA-01 alias test | ❌ W0 | ⬜ pending |
| 10-02-01 | 02 | 1 | INFRA-03 | unit | `python3 -m pytest tests/test_validation.py -k "lenient" -x` | ❌ W0 | ⬜ pending |
| 10-02-02 | 02 | 1 | INFRA-04 | unit | `python3 -m pytest tests/test_validation.py -k "lenient_type" -x` | ❌ W0 | ⬜ pending |
| 10-02-03 | 02 | 1 | INFRA-04 | unit | `python3 -m pytest tests/test_validation.py -k "garbled_strict_lenient" -x` | ❌ W0 | ⬜ pending |
| 10-02-04 | 02 | 1 | INFRA-04 | unit | `python3 -m pytest tests/test_validation.py -k "non_lenient" -x` | ❌ W0 | ⬜ pending |
| 10-03-01 | 03 | 1 | AGINF-01 | manual-only | Visual inspection of `agents/team-leads/cco/publisher.md` | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_generate_infographic.py` — add `TestSlugAliases` class: `test_alias_resolves_fault_lines`, `test_alias_resolves_risk_matrix`, `test_alias_resolves_action_plan`, `test_non_alias_unchanged`, `test_aspect_ratio_shorthand_entries`, `test_output_filename_uses_shorthand`
- [ ] `tests/test_validation.py` — add `TestLenientValidation` class: `test_lenient_type_partial_passes_clean`, `test_lenient_type_garbled_still_fails`, `test_non_lenient_type_partial_still_warns`, `test_no_type_slug_backward_compatible`, `test_lenient_type_clean_pass_unchanged`

*No framework install needed — pytest is already configured and 161 tests pass.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Publisher.md contains `cd <skill-directory> &&` before `build_results_pdf` | AGINF-01 | Agent definition is a markdown file, not executable code | Visually inspect `agents/team-leads/cco/publisher.md` for correct `cd` prefix |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
