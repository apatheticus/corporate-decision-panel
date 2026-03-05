---
phase: 7
slug: specification-formalization
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-05
---

# Phase 7 — Validation Strategy

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

- **After every task commit:** Visual diff review of modified markdown files; verify structure matches prescribed formats
- **After every plan wave:** Verify all 5 threshold decision trees + all 5 weighting tables + cost formula with examples present
- **Before `/gsd:verify-work`:** Full suite must be green; all 6 SPEC requirements verified via content inspection
- **Max feedback latency:** ~5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 07-01-* | 01 | 1 | SPEC-01 | manual-only | N/A — verify structured decision tree format in routing-table.md | N/A | ⬜ pending |
| 07-01-* | 01 | 1 | SPEC-02 | manual-only | N/A — verify calibration exemplars per threshold in routing-table.md | N/A | ⬜ pending |
| 07-02-* | 02 | 1 | SPEC-04 | manual-only | N/A — verify 5 weighting tables in decision-modes.md | N/A | ⬜ pending |
| 07-02-* | 02 | 1 | SPEC-05 | manual-only | N/A — verify formula section in decision-modes.md | N/A | ⬜ pending |
| 07-02-* | 02 | 1 | SPEC-06 | manual-only | N/A — verify worked examples in decision-modes.md | N/A | ⬜ pending |
| 07-03-* | 03 | 2 | SPEC-03 | manual-only | N/A — verify orchestration-protocol.md evaluation format and CEO.md template | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. This phase modifies markdown specification files, not Python code. No new test stubs or fixtures needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Each threshold has structured diagnostic questions with YES/NO criteria | SPEC-01 | Markdown content structure, not code behavior | Inspect routing-table.md for 5 decision trees with diagnostic question tables |
| Each threshold has calibration exemplars | SPEC-02 | Markdown content, project excludes automated agent testing | Inspect routing-table.md for 2-3 exemplars per threshold condition |
| CEO Phase 1 framing evaluates each threshold explicitly | SPEC-03 | Template format in markdown, non-deterministic output | Verify orchestration-protocol.md Step 4/5 format and CEO.md Decision Record template |
| Each mode has directional weighting table | SPEC-04 | Markdown table structure | Verify 5 weighting tables in decision-modes.md with HIGH/MODERATE/LOW values |
| Multi-mode cost formula documented with calculation | SPEC-05 | Specification prose, not executable code | Verify formula section exists in decision-modes.md |
| Multi-mode cost includes worked examples | SPEC-06 | Worked example prose | Verify worked examples with typical panel sizes in decision-modes.md |

**Justification for all-manual:** All SPEC requirements specify markdown content and structure. No code behavior to test. Project explicitly excludes automated agent testing (REQUIREMENTS.md Out of Scope: "LLM outputs are non-deterministic; false precision").

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — manual-only justified above
- [x] Sampling continuity: structural review after each commit
- [x] Wave 0 covers all MISSING references — none needed
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
