# Roadmap: CDP Image Generation — Browser to API Migration

## Milestones

- ✅ **v1.0 MVP** — Phases 1-4 (shipped 2026-03-04)
- 🚧 **v1.1 Initial Design Concerns** — Phases 5-8 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4) — SHIPPED 2026-03-04</summary>

- [x] Phase 1: Config and Pre-flight (2/2 plans) — completed 2026-03-04
- [x] Phase 2: API Integration (3/3 plans) — completed 2026-03-04
- [x] Phase 3: Error Handling and Quality (3/3 plans) — completed 2026-03-04
- [x] Phase 4: Scale and Docs (3/3 plans) — completed 2026-03-04

</details>

### 🚧 v1.1 Initial Design Concerns (Phases 5-8)

**Milestone Goal:** Address architectural, specification, and testing concerns identified in the codebase audit to improve reliability, clarity, and maintainability.

- [ ] **Phase 5: CEO Architecture** - Extract orchestration protocol from monolithic CEO agent and add executive summaries to C-suite agents
- [ ] **Phase 6: Orchestration Hardening** - Add pre-flight validation, CSO timeout handling, and session cleanup to the production pipeline
- [ ] **Phase 7: Specification Formalization** - Formalize routing thresholds, decision mode weightings, and multi-mode cost calculations into structured specs
- [ ] **Phase 8: Test Scenarios** - Validate routing, pre-mortem, and mode sensitivity behavior against formalized specifications

## Phase Details

### Phase 5: CEO Architecture
**Goal**: CEO agent is cleanly separated into identity/synthesis and orchestration protocol, and C-suite agents provide structured summaries that reduce CEO synthesis input
**Depends on**: Phase 4 (v1.0 complete)
**Requirements**: ARCH-01, ARCH-02, ARCH-03, ARCH-04
**Success Criteria** (what must be TRUE):
  1. CEO agent file contains only identity, judgment criteria, and synthesis logic -- no orchestration phases, routing, or session protocol
  2. A separate orchestration protocol document exists and is referenced by the CEO agent, containing all phase sequencing and coordination logic
  3. CEO agent is under 350 lines with zero duplicated orchestration content between the two documents
  4. Each C-suite agent produces structured executive summary fields (role, position, confidence, key-risks) alongside their full recommendation
  5. CEO synthesis reads executive summaries first and only references full recommendations when summaries reveal ambiguity
**Plans**: 2 plans

Plans:
- [ ] 05-01-PLAN.md — Extract orchestration protocol from CEO and refactor CEO agent under 350 lines
- [ ] 05-02-PLAN.md — Add executive summary blocks to C-suite agents and update CEO synthesis logic

### Phase 6: Orchestration Hardening
**Goal**: Production pipeline validates dependencies before running, CSO research has timeout protection, and old sessions can be cleaned up
**Depends on**: Phase 5 (orchestration protocol extracted -- additions go to the right document)
**Requirements**: ORCH-01, ORCH-02, ORCH-03, ORCH-04, ORCH-05
**Success Criteria** (what must be TRUE):
  1. Running the production pipeline with a missing required dependency fails immediately with an explicit error message naming the missing dependency and install instructions
  2. Running the production pipeline with a missing optional dependency prints a warning listing which artifacts will be skipped, then continues
  3. CSO Phase 1.5 research that exceeds its maxTurns limit broadcasts partial results with explicit gap reporting identifying what research was not completed
  4. C-suite agents receiving incomplete CSO research annotate their recommendations with confidence caveats explaining what information was unavailable
  5. A cleanup command deletes old session directories with age-based filtering and confirmation prompt before deletion
**Plans**: 3 plans

Plans:
- [ ] 06-01-PLAN.md — Add pre-flight dependency validation to SKILL.md production section
- [ ] 06-02-PLAN.md — Add CSO timeout handling with gap reporting and C-suite confidence caveats
- [ ] 06-03-PLAN.md — Create /cdp:cleanup session cleanup command

### Phase 7: Specification Formalization
**Goal**: Routing thresholds, decision mode weightings, and multi-mode costs are documented as structured specifications rather than embedded prose
**Depends on**: Phase 5 (routing/mode content extracted from CEO, avoiding duplication)
**Requirements**: SPEC-01, SPEC-02, SPEC-03, SPEC-04, SPEC-05, SPEC-06
**Success Criteria** (what must be TRUE):
  1. Each of the 5 routing threshold conditions has a structured decision tree with diagnostic questions, YES/NO criteria, and calibration exemplars showing concrete decisions
  2. CEO Phase 1 framing output explicitly evaluates each threshold condition, making the routing decision auditable
  3. Each of the 5 decision modes has a directional weighting table specifying HIGH/MODERATE/LOW influence per C-suite perspective
  4. Multi-mode cost formula is documented with the actual calculation and includes worked examples for typical panel sizes
**Plans**: TBD

Plans:
- [ ] 07-01: TBD
- [ ] 07-02: TBD

### Phase 8: Test Scenarios
**Goal**: Specification-level test scenarios validate routing, pre-mortem, and mode sensitivity behavior against formalized specs
**Depends on**: Phase 7 (tests validate formalized specifications, not ambiguous prose)
**Requirements**: TEST-01, TEST-02, TEST-03, TEST-04
**Success Criteria** (what must be TRUE):
  1. A test scenario demonstrates that Tier 2 partial activation correctly excludes non-requested C-suite agents even when full-activation thresholds are met
  2. A test scenario demonstrates that Phase 4.5 Pre-Mortem executes correctly when one or more C-suite agents have missing or partial recommendations
  3. Mode sensitivity criteria defines quantitative LOW/MEDIUM/HIGH divergence thresholds with concrete examples
  4. A test scenario demonstrates that mode sensitivity ratings produce consistent results across similar decision types
**Plans**: TBD

Plans:
- [ ] 08-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 5 -> 6 -> 7 -> 8

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Config and Pre-flight | v1.0 | 2/2 | Complete | 2026-03-04 |
| 2. API Integration | v1.0 | 3/3 | Complete | 2026-03-04 |
| 3. Error Handling and Quality | v1.0 | 3/3 | Complete | 2026-03-04 |
| 4. Scale and Docs | v1.0 | 3/3 | Complete | 2026-03-04 |
| 5. CEO Architecture | v1.1 | 2/2 | Complete | 2026-03-04 |
| 6. Orchestration Hardening | v1.1 | 1/3 | In Progress | - |
| 7. Specification Formalization | v1.1 | 0/? | Not started | - |
| 8. Test Scenarios | v1.1 | 0/? | Not started | - |
