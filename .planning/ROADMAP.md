# Roadmap: Corporate Decision Panel

## Milestones

- ✅ **v1.0 MVP** -- Phases 1-4 (shipped 2026-03-04)
- ✅ **v1.1 Initial Design Concerns** -- Phases 5-9 (shipped 2026-03-05)
- :construction: **v1.4 Team Refactor** -- Phases 10-13 (in progress)

## Phases

<details>
<summary>v1.0 MVP (Phases 1-4) -- SHIPPED 2026-03-04</summary>

- [x] Phase 1: Config and Pre-flight (2/2 plans) -- completed 2026-03-04
- [x] Phase 2: API Integration (3/3 plans) -- completed 2026-03-04
- [x] Phase 3: Error Handling and Quality (3/3 plans) -- completed 2026-03-04
- [x] Phase 4: Scale and Docs (3/3 plans) -- completed 2026-03-04

</details>

<details>
<summary>v1.1 Initial Design Concerns (Phases 5-9) -- SHIPPED 2026-03-05</summary>

- [x] Phase 5: CEO Architecture (2/2 plans) -- completed 2026-03-04
- [x] Phase 6: Orchestration Hardening (3/3 plans) -- completed 2026-03-05
- [x] Phase 7: Specification Formalization (3/3 plans) -- completed 2026-03-05
- [x] Phase 8: Test Scenarios (2/2 plans) -- completed 2026-03-05
- [x] Phase 9: Integration Polish (1/1 plan) -- completed 2026-03-05

</details>

### v1.4 Team Refactor (In Progress)

**Milestone Goal:** Fix the nested session limitation preventing C-suite agents from dispatching team leads by moving all Agent/TeamCreate to the CEO, plus address 5 production issues from the 2026-03-08 error logs.

- [x] **Phase 10: Production Quick Wins** - Fix slug aliases, validation leniency, PDF path, and graphic designer slugs (completed 2026-03-08)
- [ ] **Phase 11: Inline Logging Protocol** - Replace file-path logging references with inline protocol summary across 48 agent files
- [ ] **Phase 12: Dispatch Architecture Rewrite** - CEO becomes universal dispatcher; C-suite agents become teammates with file-based sub-question protocol
- [ ] **Phase 13: Documentation** - Add large file read guidance to orchestration protocol and CEO agent

## Phase Details

### Phase 10: Production Quick Wins
**Goal**: Infographic pipeline and agent infrastructure produce correct results without the specific failures observed in the 2026-03-08 production session
**Depends on**: Nothing (independent code/config fixes)
**Requirements**: INFRA-01, INFRA-02, INFRA-03, INFRA-04, AGINF-01
**Success Criteria** (what must be TRUE):
  1. Running `session.py` with shorthand slugs (`fault-lines`, `risk-matrix`, `action-plan`) resolves to canonical template slugs and generates correct infographics
  2. Graphic designer agent definition references only canonical slugs (`fault-line-map`, `risk-opportunity-matrix`, `action-plan-timeline`)
  3. Validation of a `routing-diagram` infographic with PARTIAL labels passes without triggering failure
  4. Publisher agent successfully runs `build_results_pdf` from any working directory (not just the skill directory)
**Plans**: 2 plans

Plans:
- [x] 10-01-PLAN.md — Validation leniency for high-density types + publisher path fix
- [x] 10-02-PLAN.md — Slug alias resolution + ASPECT_RATIOS shorthand entries + validate_infographic wiring

### Phase 11: Inline Logging Protocol
**Goal**: All 48 agent files contain self-sufficient logging instructions with no dependency on external logging protocol file
**Depends on**: Phase 10 (must complete before dispatch rewrite to avoid double-editing C-suite agents)
**Requirements**: AGINF-02
**Success Criteria** (what must be TRUE):
  1. Every agent file in `agents/` contains the inline logging protocol summary text
  2. No agent file contains a file path reference to `config/logging-protocol.md`
  3. `grep -r "logging-protocol.md" agents/` returns zero matches
**Plans**: 2 plans

Plans:
- [ ] 11-01-PLAN.md — Inline logging protocol for CEO + 9 C-suite agents (10 files)
- [ ] 11-02-PLAN.md — Inline logging protocol for 38 team lead agents (34 analytical + 4 CCO production)

### Phase 12: Dispatch Architecture Rewrite
**Goal**: CEO creates all division teams and dispatches all agents (C-suite and team leads); C-suite agents communicate sub-questions via files; CCO production pipeline runs under CEO wave management
**Depends on**: Phase 11 (C-suite agents must have inline logging before rewrite)
**Requirements**: DISP-01, DISP-02, DISP-03, DISP-04, DISP-05, DISP-06, DISP-07, DISP-08, DISP-09, DISP-10
**Success Criteria** (what must be TRUE):
  1. `config/dispatch-protocol.md` documents CEO-as-universal-dispatcher with sub-question file convention (`{session}/sub-questions/{role}/{team-lead-name}.md`)
  2. `config/cco-dispatch-protocol.md` documents CEO-managed production wave sequencing with CCO as Creative Brief author and editorial coordinator
  3. `config/orchestration-protocol.md` Phases 2, 3, and 4 describe CEO division team dispatch flow including TeamCreate per role, two-wave dispatch, and sub-question file polling
  4. CEO agent contains TeamCreate instructions, team lead dispatch with sub-question file reading, polling logic, and CCO wave management
  5. All 8 analytical C-suite agents use Mode B with sub-question file writing and teammate message receiving (no TeamCreate, no Agent dispatch, no shutdown_request references)
  6. CCO agent operates as Creative Brief author and editorial coordinator within CEO-managed production team
  7. CSO Phase 1.5 dispatch is integrated with division team pattern (dispatched before other C-suite agents)
  8. `grep -rE "TeamCreate|Agent\.\*team_name|SendMessage\.\*shutdown_request" agents/c-suite/` returns zero matches
**Plans**: TBD

Plans:
- [ ] 12-01: TBD
- [ ] 12-02: TBD
- [ ] 12-03: TBD

### Phase 13: Documentation
**Goal**: Orchestration protocol and CEO agent provide guidance for handling large files during recommendation synthesis
**Depends on**: Phase 12 (target files are heavily modified during dispatch rewrite; documentation additions go into stabilized files)
**Requirements**: DOCS-01, DOCS-02
**Success Criteria** (what must be TRUE):
  1. `config/orchestration-protocol.md` Phase 4 synthesis section contains large file read guidance (e.g., reading files in chunks, summarizing incrementally)
  2. `agents/ceo.md` recommendation synthesis section contains large file read guidance
**Plans**: TBD

Plans:
- [ ] 13-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 10 -> 11 -> 12 -> 13

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Config and Pre-flight | v1.0 | 2/2 | Complete | 2026-03-04 |
| 2. API Integration | v1.0 | 3/3 | Complete | 2026-03-04 |
| 3. Error Handling and Quality | v1.0 | 3/3 | Complete | 2026-03-04 |
| 4. Scale and Docs | v1.0 | 3/3 | Complete | 2026-03-04 |
| 5. CEO Architecture | v1.1 | 2/2 | Complete | 2026-03-04 |
| 6. Orchestration Hardening | v1.1 | 3/3 | Complete | 2026-03-05 |
| 7. Specification Formalization | v1.1 | 3/3 | Complete | 2026-03-05 |
| 8. Test Scenarios | v1.1 | 2/2 | Complete | 2026-03-05 |
| 9. Integration Polish | v1.1 | 1/1 | Complete | 2026-03-05 |
| 10. Production Quick Wins | 2/2 | Complete    | 2026-03-08 | - |
| 11. Inline Logging Protocol | v1.4 | 0/2 | Not started | - |
| 12. Dispatch Architecture Rewrite | v1.4 | 0/? | Not started | - |
| 13. Documentation | v1.4 | 0/? | Not started | - |
