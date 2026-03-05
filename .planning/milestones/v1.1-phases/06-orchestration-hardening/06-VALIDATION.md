---
phase: 6
slug: orchestration-hardening
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-05
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (installed, configured) |
| **Config file** | `pytest.ini` (markers: `live` for Gemini API tests) |
| **Quick run command** | `python3 -m pytest tests/ -x -m "not live"` |
| **Full suite command** | `python3 -m pytest tests/ -m "not live"` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python3 -m pytest tests/ -x -m "not live"`
- **After every plan wave:** Run `python3 -m pytest tests/ -m "not live"`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 06-01-XX | 01 | 1 | ORCH-01 | manual-only | N/A — pre-flight is markdown instructions for the orchestrator agent | N/A | ⬜ pending |
| 06-01-XX | 01 | 1 | ORCH-02 | manual-only | N/A — same as ORCH-01, agent-level behavior | N/A | ⬜ pending |
| 06-02-XX | 02 | 1 | ORCH-03 | manual-only | N/A — maxTurns is platform mechanism; timeout behavior is agent instructions | N/A | ⬜ pending |
| 06-02-XX | 02 | 1 | ORCH-04 | manual-only | N/A — conditional output format in markdown agent specs | N/A | ⬜ pending |
| 06-03-XX | 03 | 2 | ORCH-05 | manual-only | N/A — slash command is markdown file; cleanup logic is agent behavior | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. This phase modifies markdown specification files and creates one new markdown command file. All requirements are agent-behavior specifications, not testable Python code. The existing test suite covers the Python scripts that are NOT being modified in this phase. Running the existing tests confirms no regressions were introduced.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Pre-flight validates required deps, fails with install instructions | ORCH-01 | Agent-level markdown instructions, not code | Run pipeline with a known missing dep; verify error message names dep and install command |
| Pre-flight warns on missing optional deps, lists skipped artifacts | ORCH-02 | Agent-level markdown instructions, not code | Run pipeline without optional dep; verify warning lists skipped artifacts and continues |
| CSO timeout broadcasts partial results with gap reporting | ORCH-03 | Platform maxTurns mechanism, not testable code | Simulate CSO exceeding maxTurns; verify partial results broadcast with gap list |
| C-suite annotates with confidence caveats on incomplete research | ORCH-04 | Conditional output format in markdown specs | Feed incomplete CSO research to C-suite agent; verify "Research Basis: Partial" annotation |
| Cleanup command deletes old sessions with confirmation | ORCH-05 | Slash command is markdown file | Run `/cdp:cleanup`; verify age filter, confirmation prompt, and deletion |
| SKILL.md pre-flight section is valid markdown | ORCH-01/02 | Syntax validation | Visually inspect SKILL.md pre-flight section for correct table formatting |
| All 8 C-suite agents have identical Research Basis field placement | ORCH-04 | Pattern consistency | Compare executive summary blocks across all 8 agents |
| `commands/cdp/cleanup.md` follows existing command YAML pattern | ORCH-05 | Format consistency | Compare cleanup.md frontmatter with existing commands |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
