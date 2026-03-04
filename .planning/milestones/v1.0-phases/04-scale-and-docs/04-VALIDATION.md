---
phase: 4
slug: scale-and-docs
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-04
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.2 |
| **Config file** | `pytest.ini` |
| **Quick run command** | `cd /Volumes/Data/dev/corporate-decision-panel && python -m pytest tests/ -x -m "not live"` |
| **Full suite command** | `cd /Volumes/Data/dev/corporate-decision-panel && python -m pytest tests/ -x` |
| **Estimated runtime** | ~5 seconds (unit), ~120 seconds (live) |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/ -x -m "not live"`
- **After every plan wave:** Run grep verification pattern + full test suite
- **Before `/gsd:verify-work`:** Full suite must be green + grep pattern returns 0 matches
- **Max feedback latency:** 5 seconds (unit), 120 seconds (live)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | DOC-01 | manual-only | Visual review of infographics.md | N/A — doc | ⬜ pending |
| 04-01-02 | 01 | 1 | DOC-03 | manual-only | Visual review of ceo.md | N/A — doc | ⬜ pending |
| 04-01-03 | 01 | 1 | DOC-04 | smoke | `grep -rn --include="*.md" -e "browser.automation" -e "Browser Automation" -e "chatgpt\.com" -e "gemini\.google\.com" -e "Platform Profile" -e "platform selection" -e "model picker" -e "fast-mode" -e "fast mode" -e "ChatGPT" --exclude-dir=.planning --exclude-dir=.git . \| wc -l` should equal 0 | N/A — grep | ⬜ pending |
| 04-02-01 | 02 | 2 | DOC-04 | integration (live) | `python -m scripts.session` or manual session run with all 6 types | Partial | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/fixtures/sample-routing-diagram-data.json` — test data for routing-diagram type
- [ ] `tests/fixtures/sample-fault-line-map-data.json` — test data for fault-line-map type
- [ ] `tests/fixtures/sample-risk-opportunity-matrix-data.json` — test data for risk-opportunity-matrix type
- [ ] `tests/fixtures/sample-action-plan-timeline-data.json` — test data for action-plan-timeline type
- [ ] `tests/fixtures/sample-mode-comparison-data.json` — test data for mode-comparison type

*Existing: `tests/fixtures/sample-domain-scorecard-data.json` — already present.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| infographics.md correctly describes API workflow | DOC-01 | Document content review — structural/semantic accuracy not automatable | Read sections: Technology, Generation Workflow, Retry Behavior, Error Handling. Verify no browser automation references. Verify kept sections (Purpose, 6 specs, Output Requirements, Content Mapping, Multi-Mode Variant) are unchanged. |
| ceo.md Task A spawn instruction updated | DOC-03 | Single-line text change — grep can verify absence of old text but not correctness of new | Read line ~595. Verify it references "Gemini API script" not "browser automation". Verify data extraction and session.py workflow described. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
