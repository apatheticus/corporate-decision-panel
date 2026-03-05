---
phase: 1
slug: config-and-pre-flight
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-04
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none — Wave 0 installs |
| **Quick run command** | `python -m pytest tests/ -x -q` |
| **Full suite command** | `python -m pytest tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/ -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | SETUP-01 | unit | `python -m pytest tests/test_config.py -x` | ❌ W0 | ⬜ pending |
| 01-01-02 | 01 | 1 | SETUP-01 | unit | `python -m pytest tests/test_config.py::test_missing_fields -x` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | SETUP-02 | unit (mocked) | `python -m pytest tests/test_preflight.py::test_invalid_key -x` | ❌ W0 | ⬜ pending |
| 01-02-02 | 02 | 1 | SETUP-02 | unit (mocked) | `python -m pytest tests/test_preflight.py::test_billing_not_enabled -x` | ❌ W0 | ⬜ pending |
| 01-03-01 | 03 | 1 | SETUP-03 | unit (mocked) | `python -m pytest tests/test_preflight.py::test_invalid_model -x` | ❌ W0 | ⬜ pending |
| 01-04-01 | 04 | 1 | DOC-02 | unit | `python -m pytest tests/test_config.py::test_template_fields -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/__init__.py` — package init
- [ ] `tests/test_config.py` — covers SETUP-01, SETUP-03, DOC-02
- [ ] `tests/test_preflight.py` — covers SETUP-02 (with mocked API calls)
- [ ] `tests/conftest.py` — shared fixtures (temp config files, mock client)
- [ ] Framework install: `pip install pytest` — no test framework exists yet
- [ ] `requirements-dev.txt` — pytest dependency

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Pre-flight with real valid API key produces success message | SETUP-02 | Requires live API key and billing | Run `python scripts/preflight.py` with valid `.cdp-context/config.md` |
| Pre-flight with real invalid key produces specific error | SETUP-02 | Requires testing against live API | Run with deliberately invalid key, verify error message |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
