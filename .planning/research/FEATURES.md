# Feature Landscape: v1.1 Initial Design Concerns

**Domain:** CDP architectural improvements and specification hardening
**Researched:** 2026-03-04
**Confidence:** HIGH (concerns are well-documented in codebase audit; integration points verified against source files)

## Context

CDP v1.0 shipped a complete 5-phase deliberation cascade with 43 agents, 5 decision modes, 3-tier routing, production pipeline, and session orchestration. The v1.0 milestone audit identified 11 codebase concerns across architectural, specification, resilience, and testing dimensions. This feature landscape maps each concern fix into table-stakes, differentiators, and anti-features, with integration points against the existing CEO/C-suite/team-lead architecture.

## Table Stakes

Features users expect. Missing = product has known failure modes or unclear specifications.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| CEO orchestration extraction (#1) | 682-line monolith with 3 mixed concerns. Unsustainable as system grows. Modification isolation impossible. | Medium | Extraction, not rewrite. ~350 lines move to new file. CEO retains identity + synthesis. |
| Production pre-flight (#2) | Production spawns without validating prerequisites. Silent failures when dependencies missing. | Low | Checklist addition to orchestration protocol. Warn, do not block. |
| CSO Phase 1.5 timeout (#3) | No fallback if CSO research stalls. System hangs with no recovery path. | Medium | Add timeout/fallback + partial dossier handling. Touches CEO + CSO + decision record template. |
| Session cleanup (#8) | Session dirs accumulate indefinitely. No lifecycle management. | Low | Python script + slash command. ~150 lines of code. |
| Routing threshold formalization (#5) | 5 threshold conditions defined in prose. CEO interprets subjectively. Same issue may route differently across runs. | Low-Medium | Structured diagnostic questions with exemplars. Not rigid decision trees. |
| Mode weighting formalization (#6) | Implicit "weight skeptics more" lacks auditability. Mode behavior may drift from specification. | Low | Directional weighting tables (HIGH/MODERATE/LOW) per mode. Not numeric multipliers. |
| Cost formula documentation (#7) | "~1.1x" claim is unsubstantiated. Users cannot predict multi-mode costs. | Low | Documentation only. Formula + example calculations. |

## Differentiators

Features that set product apart. Not strictly required but significantly improve quality.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Executive summaries (#4) | Reduces CEO Opus token ingestion by ~30-50%. Makes synthesis more focused. | Low | ~10 lines added to each of 7 C-suite agents. Must be structured fields, not prose compression. |
| Mode sensitivity criteria (#11) | Formalizes LOW/MEDIUM/HIGH sensitivity into testable criteria. Currently subjective. | Low | Criteria definition in decision-modes.md + test scenario document. |
| Tier 2 routing test (#9) | Validates partial activation exclusion behavior. Currently untested. | Low | Test scenario document with expected outcomes. Not automated. |
| Pre-Mortem test (#10) | Validates Phase 4.5 with partial/missing responses. Currently untested. | Low | Test scenario document with degraded-case expectations. |

## Anti-Features

Features to explicitly NOT build in v1.1.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Automated agent testing framework | LLM agents following prompts cannot be deterministically tested. False precision. | Write specification-level test scenarios with expected-behavior criteria for manual validation. |
| Numeric mode weights (1.5x, 0.7x) | LLMs cannot reliably apply numeric multipliers. Creates false precision that users may trust. | Use directional indicators (HIGH/MODERATE/LOW) for mode weighting guidance. |
| Session archival with compression | Overengineered for local development artifacts. Adds complexity for marginal benefit. | Simple delete-with-confirmation. No archive, no compression, no cloud backup. |
| CEO agent full rewrite | Extraction is sufficient. The CEO identity/judgment sections are well-written and proven. | Extract the orchestration protocol; leave identity, mandate, and susceptibility mitigations intact. |
| Mode-specific C-suite behavior | Making C-suite agents behave differently per mode violates a core design principle. | Keep domain analysis mode-independent. Modes affect CEO synthesis only. |
| Dynamic AI-driven routing | Removes auditability. CDP routing transparency is a core design principle. | Formalize existing routing table with structured criteria. CEO retains override authority. |
| Agent-to-agent direct communication | Breaks two-tier visibility principle. Undermines independent analysis. | Phase 4.5 Pre-Mortem already provides structured cross-agent awareness. |
| Blocking pre-flight for optional dependencies | Converts optional features into hard requirements. Worse UX than silent failure. | Warn-only for production dependencies. Never block deliberation on missing optional skills. |

## Feature Dependencies

```
#1 CEO Extraction --> #2 Production Pre-Flight (adds to extracted protocol)
#1 CEO Extraction --> #3 CSO Timeout (adds to extracted protocol Phase 1.5)
#1 CEO Extraction --> #5 Routing Trees (cleans duplication revealed by extraction)
#5 Routing Trees --> #9 Tier 2 Routing Test (tests formalized routing criteria)
#6 Mode Weightings --> #11 Mode Sensitivity Test (tests formalized mode behavior)

Independent (no upstream dependencies):
  #4 Executive Summaries (touches only C-suite agents)
  #7 Cost Formula (documentation only)
  #8 Session Cleanup (new Python script)
  #10 Pre-Mortem Test (new test scenario)
```

## MVP Recommendation

Prioritize:
1. **#1 CEO Extraction** -- foundational, enables 4 other concerns, addresses primary maintenance bottleneck
2. **#4 Executive Summaries** -- independent, immediate token cost savings, no conflict with other work
3. **#3 CSO Timeout** -- addresses actual failure mode (system hangs with no recovery)
4. **#2 Production Pre-Flight** -- addresses actual failure mode (silent production failures)

Defer if time-constrained:
- **#7 Cost Formula** -- documentation-only, low urgency
- **#9/#10/#11 Test Scenarios** -- validate existing behavior rather than adding new capability. Most valuable AFTER specifications are formalized.

## Feature-to-File Mapping

| Concern | Files Modified | Files Created |
|---------|----------------|---------------|
| #1 CEO Extraction | `agents/ceo.md` (major reduction), `SKILL.md` (minor) | `config/orchestration-protocol.md` |
| #2 Production Pre-Flight | Orchestration protocol (wherever it lives) | None |
| #3 CSO Timeout | Orchestration protocol, `agents/c-suite/cso.md`, `templates/decision-record.md` | None |
| #4 Executive Summaries | 7 C-suite agents (all except CSO), orchestration protocol Phase 4 | None |
| #5 Routing Trees | `config/routing-table.md`, `agents/ceo.md` or orchestration protocol | None |
| #6 Mode Weightings | `config/decision-modes.md` | None |
| #7 Cost Formula | `config/decision-modes.md` | None |
| #8 Session Cleanup | `SKILL.md` | `scripts/cleanup.py`, `tests/test_cleanup.py` |
| #9 Tier 2 Routing Test | None | `tests/scenarios/tier-2-routing.md` |
| #10 Pre-Mortem Test | None | `tests/scenarios/pre-mortem-phase-4-5.md` |
| #11 Mode Sensitivity | `config/decision-modes.md` | `tests/scenarios/mode-sensitivity.md` |

## Complexity Summary

| Feature | Complexity | Plans Estimate | Risk |
|---------|-----------|----------------|------|
| #1 CEO Extraction | MEDIUM | 1-2 | Prompt regression: refactored CEO must produce identical cascade behavior |
| #2 Production Pre-Flight | LOW | 1 | Minimal: additive gate. Risk: over-blocking if optional deps treated as required |
| #3 CSO Timeout | MEDIUM | 1 | Must design for partial results, not binary success/failure |
| #4 Executive Summaries | LOW | 1 | Risk: summaries flatten analytical nuance. Must be structured fields, not prose |
| #5 Routing Trees | LOW-MEDIUM | 1 | Risk: over-formalization kills CEO judgment. Use exemplars, not algorithms |
| #6 Mode Weightings | LOW | 1 | Risk: tables contradict prose modifiers. Derive FROM existing prose |
| #7 Cost Formula | LOW | 0.5 (combine) | Minimal: documentation addition |
| #8 Session Cleanup | LOW | 1 | Minimal: standard file system operations |
| #9 Tier 2 Routing Test | LOW | 0.5 (combine) | Test scenarios, not automated tests |
| #10 Pre-Mortem Test | LOW | 0.5 (combine) | Test scenarios, not automated tests |
| #11 Mode Sensitivity | LOW | 0.5 (combine) | Criteria definition + test scenario |

**Total estimated plans:** 8-10 across 4 phases
