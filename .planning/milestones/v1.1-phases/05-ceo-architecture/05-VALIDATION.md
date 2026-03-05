---
phase: 5
slug: ceo-architecture
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-04
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/ -x -m "not live"` |
| **Full suite command** | `pytest tests/ -m "not live"` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** `wc -l agents/ceo.md` (verify under 350) + visual diff review
- **After every plan wave:** Verify all 8 C-suite agent files contain identical executive summary block; verify `config/orchestration-protocol.md` exists and contains extracted content; verify zero duplication via content comparison
- **Before `/gsd:verify-work`:** All 5 success criteria from ROADMAP.md verified manually
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | ARCH-01 | manual-only | N/A -- verify file structure and content | N/A | ⬜ pending |
| 05-01-02 | 01 | 1 | ARCH-02 | manual-only | `wc -l agents/ceo.md` (verify < 350) | N/A | ⬜ pending |
| 05-02-01 | 02 | 2 | ARCH-03 | manual-only | N/A -- verify template block in all 8 agent files | N/A | ⬜ pending |
| 05-02-02 | 02 | 2 | ARCH-04 | manual-only | N/A -- verify synthesis logic in CEO.md | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.*

No test infrastructure changes needed. This phase modifies markdown agent definition files, not Python code. Validation is structural (line counts, content comparison, template consistency) rather than behavioral.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| CEO orchestration extracted to separate doc | ARCH-01 | Agent markdown content, no code behavior | Verify `config/orchestration-protocol.md` exists with all extracted sections; verify CEO.md no longer contains orchestration phases |
| CEO agent under 350 lines, zero duplication | ARCH-02 | Line count + content comparison | Run `wc -l agents/ceo.md`; grep for duplicated orchestration content between CEO.md and orchestration-protocol.md |
| C-suite agents produce executive summaries | ARCH-03 | Template consistency in markdown | Diff executive summary block across all 8 C-suite agent files; verify identical format |
| CEO reads summaries first, deep-dives on conflict | ARCH-04 | Synthesis logic in markdown prompt | Verify CEO.md Phase 5 Step 1 reads executive summaries first; verify Decision Record has Synthesis Methodology field |

**Justification for manual-only:** Project explicitly excludes automated agent testing (REQUIREMENTS.md Out of Scope). All ARCH requirements are about markdown file content and structure, not code behavior.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
