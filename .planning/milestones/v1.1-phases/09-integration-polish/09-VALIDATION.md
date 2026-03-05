---
phase: 9
slug: integration-polish
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-03-05
---

# Phase 9 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual verification (markdown inspection) |
| **Config file** | none |
| **Quick run command** | Visual inspection of modified files |
| **Full suite command** | Cross-reference panel-assessment.md with orchestration-protocol.md Step 5 and test-scenarios/tier2-partial-activation.md Expected Output Excerpt; verify SKILL.md frontmatter YAML parses correctly |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Visual diff review of modified files
- **After every plan wave:** Cross-reference all three wiring points (template field, protocol format, test scenario expected output)
- **Before `/gsd:verify-work`:** Full cross-reference verification must pass
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 09-01-01 | 01 | 1 | TEST-01, SPEC-03 | manual-only | Verify `templates/panel-assessment.md` contains `Triggered Thresholds:` field in Escalation Note section | N/A | ⬜ pending |
| 09-01-02 | 01 | 1 | ORCH-05 | manual-only | Verify `SKILL.md` frontmatter contains `/cdp:cleanup` and body contains Session Cleanup subsection | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements — no test infrastructure needed for markdown template edits.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| panel-assessment.md Escalation Note includes triggered-threshold enumeration field | TEST-01, SPEC-03 | Markdown template edit — no automated test infra for markdown content validation (explicitly out of scope) | Verify `templates/panel-assessment.md` Escalation Note section contains `Triggered Thresholds:` field; cross-reference format against `config/orchestration-protocol.md` Step 5 |
| /cdp:cleanup discoverable in SKILL.md | ORCH-05 | Markdown skill file edit — structural verification only | Verify `SKILL.md` frontmatter `invocation:` list includes `/cdp:cleanup`; verify Invocation Grammar section contains Session Cleanup subsection |

---

## Validation Sign-Off

- [ ] All tasks have manual verification instructions
- [ ] Sampling continuity: visual diff after every commit
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
