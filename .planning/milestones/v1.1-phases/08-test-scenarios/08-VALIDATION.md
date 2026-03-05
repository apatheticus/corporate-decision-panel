---
phase: 8
slug: test-scenarios
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-05
---

# Phase 8 — Validation Strategy

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

- **After every task commit:** Verify new/modified markdown files contain required structural elements (assertions table, quantitative criteria, paired scenarios)
- **After every plan wave:** Cross-reference all test scenario assertions against the specification files they cite — verify cited lines exist and match
- **Before `/gsd:verify-work`:** All 4 TEST requirements verified via content inspection
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 08-01-XX | 01 | 1 | TEST-01 | manual-only | N/A — verify scenario assertions against orchestration-protocol.md and panel-assessment.md | N/A | ⬜ pending |
| 08-01-XX | 01 | 1 | TEST-02 | manual-only | N/A — verify scenario defines degraded input handling and expected pre-mortem behavior | N/A | ⬜ pending |
| 08-02-XX | 02 | 1 | TEST-03 | manual-only | N/A — verify quantitative criteria in comparative-decision-record.md with countable dimensions | N/A | ⬜ pending |
| 08-02-XX | 02 | 1 | TEST-04 | manual-only | N/A — verify paired scenarios produce same sensitivity level for structurally similar decisions | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. This phase creates specification documents and extends existing templates — no test infrastructure or fixtures needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Tier 2 partial activation excludes non-requested agents | TEST-01 | Specification document, not code behavior | Verify scenario document defines correct assertions against orchestration-protocol.md Tier 2 scoping |
| Pre-Mortem with missing/partial recommendations | TEST-02 | Specification document, not code behavior | Verify scenario defines degraded input terms and expected pre-mortem broadcast behavior |
| Quantitative divergence thresholds | TEST-03 | Template extension, not code behavior | Verify criteria use countable dimensions with concrete cutoffs in comparative-decision-record.md |
| Mode sensitivity consistency | TEST-04 | Specification document, not code behavior | Verify paired scenarios with structurally similar decisions produce identical sensitivity levels |

**Justification for all-manual:** All TEST requirements produce markdown specification artifacts. There is no code behavior to test. The project's stated position is that specification-level test scenarios replace automated agent testing. Validation consists of reading scenario documents, verifying assertions reference real specification content, and confirming quantitative criteria are countable and unambiguous.

---

## Validation Sign-Off

- [ ] All tasks have manual verification procedures defined
- [ ] Sampling continuity: every task commit produces verifiable markdown artifacts
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
