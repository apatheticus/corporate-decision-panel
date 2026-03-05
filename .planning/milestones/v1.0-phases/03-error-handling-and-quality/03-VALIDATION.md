---
phase: 3
slug: error-handling-and-quality
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-04
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest >= 8.0.0 |
| **Config file** | `pytest.ini` (defines `live` marker) |
| **Quick run command** | `python -m pytest tests/ -x -m "not live" -q` |
| **Full suite command** | `python -m pytest tests/ -x -m "not live" -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/ -x -m "not live" -q`
- **After every plan wave:** Run `python -m pytest tests/ -x -m "not live" -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | ERR-01 | unit | `python -m pytest tests/test_generate_infographic.py::TestRetry -x` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | ERR-02 | unit | `python -m pytest tests/test_generate_infographic.py::TestContentBlock -x` | ❌ W0 | ⬜ pending |
| 03-01-03 | 01 | 1 | ERR-03 | unit | `python -m pytest tests/test_generate_infographic.py::TestPlaceholder -x` | ❌ W0 | ⬜ pending |
| 03-01-04 | 01 | 1 | ERR-04 | unit | `python -m pytest tests/test_session.py::TestInterCallDelay -x` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 1 | QUAL-01 | unit | `python -m pytest tests/test_validation.py::TestVisionValidation -x` | ❌ W0 | ⬜ pending |
| 03-02-02 | 02 | 1 | QUAL-02 | unit | `python -m pytest tests/test_generate_infographic.py::TestRetryWithFeedback -x` | ❌ W0 | ⬜ pending |
| 03-02-03 | 02 | 1 | QUAL-03 | unit | `python -m pytest tests/test_config.py -x` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_session.py` — stubs for ERR-04 (inter-call delay, adaptive delay, session summary)
- [ ] `tests/test_validation.py` — stubs for QUAL-01 (vision validation parsing, expected label extraction)
- [ ] Extend `tests/conftest.py` — fixtures for mock content-blocked responses, mock validation responses
- [ ] Extend `tests/test_generate_infographic.py` — new test classes for retry, placeholder, content block scenarios

*Existing infrastructure covers QUAL-03 (config parsing already tested).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full 6-infographic session without 429 storms | ERR-04 | Requires live API calls with real rate limits | Run `python -m cdp.main --session test-session` with live Gemini API key and verify no 429 storms in logs |
| Vision validation catches actual bad text rendering | QUAL-01 | Requires real Gemini vision model for ground truth | Generate infographic, manually corrupt expected labels, run validation, verify detection |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
