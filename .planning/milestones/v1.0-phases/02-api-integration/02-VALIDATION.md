---
phase: 2
slug: api-integration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-04
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (stdlib discovery) |
| **Config file** | none — pytest discovers tests/ automatically |
| **Quick run command** | `python -m pytest tests/test_generate_infographic.py -x` |
| **Full suite command** | `python -m pytest tests/ -x` |
| **Estimated runtime** | ~5 seconds (all mocked API calls) |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_generate_infographic.py -x`
- **After every plan wave:** Run `python -m pytest tests/ -x`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 0 | GEN-01..04 | unit stubs | `python -m pytest tests/test_generate_infographic.py -x` | ❌ W0 | ⬜ pending |
| 02-02-01 | 02 | 1 | GEN-02 | unit | `python -m pytest tests/test_generate_infographic.py::TestPromptSerialization -x` | ❌ W0 | ⬜ pending |
| 02-03-01 | 03 | 1 | GEN-01, GEN-03, GEN-04 | unit (mocked) | `python -m pytest tests/test_generate_infographic.py::TestGeneration -x` | ❌ W0 | ⬜ pending |
| 02-04-01 | 04 | 2 | GEN-01..04 | integration | `python -m pytest tests/test_generate_infographic.py -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_generate_infographic.py` — test stubs for GEN-01 through GEN-04
- [ ] Update `tests/conftest.py` — add fixtures for mock genai client with image response, sample template data, sample data JSON

*Existing infrastructure covers framework install (pytest already available).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Generated PNG visually correct (text legible, layout coherent) | GEN-01 | Visual quality requires human judgment | Open output PNG, verify data labels match input, text is readable |
| Domain Scorecard data labels "recognizably correct" | Success Criteria #3 | Subjective accuracy check | Compare generated PNG labels against source Decision Record data |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
