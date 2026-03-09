---
phase: 12
slug: dispatch-architecture-rewrite
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 12 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | grep + manual coherence review (markdown specification files) |
| **Config file** | N/A — no application code tests |
| **Quick run command** | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/` |
| **Full suite command** | Quick run command + full read-through of all modified files |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/`
- **After every plan wave:** Run full suite command + coherence read of all modified files
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 2 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 12-01-01 | 01 | 1 | DISP-01 | manual | Read and verify coherence | N/A (rewrite) | ⬜ pending |
| 12-01-02 | 01 | 1 | DISP-02 | manual | Read and verify coherence | N/A (rewrite) | ⬜ pending |
| 12-01-03 | 01 | 1 | DISP-03 | manual | Read and verify no stale refs in Phase 2/3/4 | N/A (update) | ⬜ pending |
| 12-01-04 | 01 | 1 | DISP-04 | manual | Read and verify CEO-managed wave pattern | N/A (update) | ⬜ pending |
| 12-01-05 | 01 | 1 | DISP-09 | smoke | `grep "sub-questions" config/orchestration-protocol.md` | Existing file | ⬜ pending |
| 12-02-01 | 02 | 1 | DISP-05 | manual | Read and verify TeamCreate, sub-Q reading, wave mgmt | N/A (update) | ⬜ pending |
| 12-03-01 | 03 | 2 | DISP-06 | smoke | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/{cfo,cto,coo,ciso,cao,vp-sales,vp-delivery,cso}.md` | Existing files | ⬜ pending |
| 12-03-02 | 03 | 2 | DISP-07 | smoke | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/cco.md` | Existing file | ⬜ pending |
| 12-03-03 | 03 | 2 | DISP-08 | manual | Verify dual dispatch pattern (Phase 1.5 team + Phase 2 standalone) | Existing file | ⬜ pending |
| 12-03-04 | 03 | 2 | DISP-10 | smoke | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/` returns 0 | Existing files | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* This phase modifies existing markdown files only. No test framework, fixtures, or infrastructure needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| dispatch-protocol.md coherence | DISP-01 | Markdown specification — no executable tests | Read file end-to-end, verify CEO-as-dispatcher with sub-Q file convention |
| cco-dispatch-protocol.md coherence | DISP-02 | Markdown specification — no executable tests | Read file, verify CEO-managed wave sequencing with CCO as Creative Brief author |
| orchestration-protocol.md Phases 2/3/4 | DISP-03 | Markdown specification — no executable tests | Read Phases 2-4, verify CEO division team dispatch flow |
| Production Spawn Sequence | DISP-04 | Markdown specification — no executable tests | Verify CEO-managed wave pattern in production spawn section |
| CEO agent dispatch mechanics | DISP-05 | Complex behavioral specification | Read CEO agent, verify TeamCreate + sub-Q reading + polling + wave management |
| CSO Phase 1.5 integration | DISP-08 | Complex dispatch pattern | Verify CSO dispatched before other C-suite in Phase 1.5 division team |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 2s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
