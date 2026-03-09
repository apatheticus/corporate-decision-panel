---
phase: 11
slug: inline-logging-protocol
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 11 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Bash grep/find (no test framework — text replacement task) |
| **Config file** | none |
| **Quick run command** | `grep -r "logging-protocol.md" agents/` |
| **Full suite command** | `grep -r "logging-protocol.md" agents/; echo "---"; find agents/ -name "*.md" -type f \| wc -l; echo "---"; grep -rl "## Agent Logging" agents/ \| wc -l; echo "---"; grep -rl "No issues = no log file" agents/ \| wc -l` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run `grep -r "logging-protocol.md" agents/`
- **After every plan wave:** Run full suite command
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 2 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 11-01-01 | 01 | 1 | AGINF-02 | smoke | `grep -rl "No issues = no log file" agents/ceo.md` | N/A | ⬜ pending |
| 11-01-02 | 01 | 1 | AGINF-02 | smoke | `grep -r "logging-protocol.md" agents/c-suite/` (expect 0) | N/A | ⬜ pending |
| 11-01-03 | 01 | 1 | AGINF-02 | smoke | `grep -r "logging-protocol.md" agents/team-leads/` (expect 0) | N/A | ⬜ pending |
| 11-01-04 | 01 | 2 | AGINF-02 | smoke | `grep -r "logging-protocol.md" agents/` (expect 0) + `grep -rl "No issues = no log file" agents/ \| wc -l` (expect 48) | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No Wave 0 setup needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| CCO variant uses "production report" not "synthesis" | AGINF-02 | Semantic correctness of variant text | `grep "production report" agents/c-suite/cco.md` should match; `grep "synthesis" agents/c-suite/cco.md` in logging section should NOT match |
| CEO retains broadcaster role | AGINF-02 | Must not lose config-reading instructions | Verify `agents/ceo.md` still references `.cdp-context/config.md` and Phase 0 broadcast |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 2s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
