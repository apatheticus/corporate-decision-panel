# Roadmap: Corporate Decision Panel

## Milestones

- ✅ **v1.0 MVP** -- Phases 1-4 (shipped 2026-03-04)
- ✅ **v1.1 Initial Design Concerns** -- Phases 5-9 (shipped 2026-03-05)
- ✅ **v1.4 Team Refactor** -- Phases 10-13 (shipped 2026-03-09)
- ✅ **v1.8 File Organization** -- Phases 14-15 (shipped 2026-03-10)
- **v1.9 Chief Legal Officer** -- Phases 16-19 (in progress)

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

<details>
<summary>v1.4 Team Refactor (Phases 10-13) -- SHIPPED 2026-03-09</summary>

- [x] Phase 10: Production Quick Wins (2/2 plans) -- completed 2026-03-08
- [x] Phase 11: Inline Logging Protocol (2/2 plans) -- completed 2026-03-08
- [x] Phase 12: Dispatch Architecture Rewrite (3/3 plans) -- completed 2026-03-09
- [x] Phase 13: Documentation (1/1 plan) -- completed 2026-03-09

</details>

<details>
<summary>v1.8 File Organization (Phases 14-15) -- SHIPPED 2026-03-10</summary>

- [x] Phase 14: Directory Restructuring (2/2 plans) -- completed 2026-03-10
- [x] Phase 15: Path Resolution and Bundle (2/2 plans) -- completed 2026-03-10

</details>

### v1.9 Chief Legal Officer (In Progress)

**Milestone Goal:** Add a Chief Legal Officer (CLO) C-suite agent with five specialist team leads, expanding the legal-domain analytical layer and rebalancing the engineered dissent roster.

**Phase Numbering:**
- Integer phases (16, 17, 18, 19): Planned milestone work
- Decimal phases (16.1, 16.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 16: CLO Foundation** - Create CLO C-suite agent and 5 specialist team lead definitions (completed 2026-03-12)
- [x] **Phase 17: Configuration** - Wire CLO into routing table, decision modes, company profiles, and orchestration protocol (completed 2026-03-12)
- [x] **Phase 18: Agent Cross-Wiring** - CAO roster reduction, CEO dispatch updates, and 22-file reference sweep (completed 2026-03-12)
- [ ] **Phase 19: Documentation** - Update SKILL.md, README.md, and all documentation counts

## Phase Details

### Phase 16: CLO Foundation
**Goal**: The CLO division exists as a complete, self-contained set of agent definitions ready for integration into the dispatch architecture
**Depends on**: Nothing (first phase of v1.9 -- new files with no modification dependencies)
**Requirements**: CLO-01, CLO-02, CLO-03, CLO-04, CLO-05, TEAM-01, TEAM-02, TEAM-03, TEAM-04, TEAM-05
**Success Criteria** (what must be TRUE):
  1. `agents/c-suite/clo.md` exists with Skeptic disposition, legal exposure mandate, full phase participation (Phase 0-5), reverse-advocate mitigation behavior, and internal contradiction flagging in synthesis
  2. Five team lead files exist under `agents/team-leads/clo/` -- governance, contracts, regulatory, employment, and ip-privacy -- each with analytical framework, forcing questions, output template, and cross-domain challenge wiring
  3. CLO agent specifies minimum 2 / maximum 5 team lead activation based on issue relevance
  4. Each team lead file follows the established structural pattern (matching tool list, maxTurns, model tier, SendMessage protocol) verified against an existing team lead like `agents/team-leads/cfo/controller.md`
  5. IP & Data Privacy Lead has dual cross-domain challenges targeting CTO Data/Analytics and CISO Security Architecture
**Plans**: 2 plans

Plans:
- [x] 16-01-PLAN.md -- CLO C-suite agent definition (Skeptic disposition, 3 modes, reverse-advocate, activation table)
- [x] 16-02-PLAN.md -- 5 CLO team lead definitions (governance, contracts, regulatory, employment, ip-privacy)

### Phase 17: Configuration
**Goal**: The CEO's routing, mode weighting, and company profile logic activates and weights the CLO correctly for all decision types and modes
**Depends on**: Phase 16 (config references CLO agent identifiers that must exist first)
**Requirements**: ROUT-01, ROUT-02, ROUT-03, MODE-01, INTG-01, INTG-02, INTG-03, INTG-04
**Success Criteria** (what must be TRUE):
  1. CLO appears in default activation for Strategic, Personnel, and Compliance/Risk decision types in `config/routing-table.md`, and in all 5 full-activation threshold scenarios
  2. CSO-CLO research interaction is documented in routing table following the format of existing CSO interaction entries
  3. CLO weighting row exists in all 5 decision mode tables in `config/decision-modes.md` with correct Skeptic pattern (HIGH/LOW/MODERATE/Confidence/HIGH)
  4. Company profile archetypes in `config/company-profile.md` include CLO-specific team lead activation (Tech/SaaS: IP/Privacy; Professional Services: Contracts; Regulated: Regulatory; Manufacturing: Employment) with override mechanism documented
  5. Engineered dissent balance updated to 5 skeptics / 2 advocates / 1 systemic / 1 investigative / 1 synthesizer in orchestration protocol, and Phase 0 Shared Consciousness Broadcast includes CLO
**Plans**: 2 plans

Plans:
- [x] 17-01-PLAN.md -- Routing table defaults, full-activation verification, CSO-CLO interaction, and 5 decision mode weighting tables
- [x] 17-02-PLAN.md -- Company profile archetype CLO activation, override mechanism, orchestration roster, and dissent balance

### Phase 18: Agent Cross-Wiring
**Goal**: The CAO no longer references a Legal/Contracts Lead, the CEO dispatches the CLO, and every file in the codebase that referenced the old CAO Legal/Contracts Lead now references the correct CLO equivalent
**Depends on**: Phase 17 (CEO mode weighting in ceo.md must align with config/decision-modes.md; routing must be finalized before CEO dispatch enumeration)
**Requirements**: CAO-01, CAO-02, CAO-03, CAO-04, MODE-02
**Success Criteria** (what must be TRUE):
  1. `agents/team-leads/cao/legal-contracts-lead.md` is deleted and CAO agent definition (`agents/c-suite/cao.md`) contains zero references to Legal/Contracts Lead across all 7 known reference points, with a note routing legal questions to the CLO
  2. `agents/ceo.md` enumerates CLO in Phase 2 dispatch and includes CLO in skeptic group lists for all 5 decision mode sections, matching the weighting in `config/decision-modes.md`
  3. A grep for "legal.contracts", "cao.*legal", and "legal/contracts" across all agent, config, test-scenario, and docs markdown files returns zero stale hits (the 22-file blast radius is fully resolved)
  4. VP Sales Business Development Lead cross-domain challenge is re-wired from CAO Legal/Contracts Lead to CLO Contracts & Commercial Lead
**Plans**: 2 plans

Plans:
- [ ] 18-01-PLAN.md -- Delete CAO Legal/Contracts Lead, update CAO agent (7 refs + identity + count), update CEO dispatch and skeptic count
- [ ] 18-02-PLAN.md -- Codebase-wide reference sweep: VP Sales re-wiring, orchestration protocol, config, test scenarios, CAO sibling peers

### Phase 19: Documentation
**Goal**: All user-facing documentation accurately reflects the 10 C-suite / 38 team lead roster with CLO present and CAO Legal/Contracts absent
**Depends on**: Phase 18 (all functional changes must be finalized before counts can be verified)
**Requirements**: DOCS-01, DOCS-02, DOCS-03
**Success Criteria** (what must be TRUE):
  1. SKILL.md lists CLO in available roles, shows correct agent counts (10 C-suite, 38 team leads), and describes updated engineered dissent balance
  2. README.md (and docs/README.md) shows CLO in Available Roles, C-Suite Roster table, Team Lead Roster table, architecture mermaid diagrams (CLO node added, CAO team lead count updated), and engineered dissent balance
  3. Every documentation file that mentions agent or team lead counts matches the actual directory listing -- verified by comparing stated numbers against `ls agents/c-suite/ | wc -l` and `find agents/team-leads/ -name "*.md" | wc -l`
**Plans**: TBD

Plans:
- [ ] 19-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 16 -> 16.1 (if any) -> 17 -> 18 -> 19

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
| 10. Production Quick Wins | v1.4 | 2/2 | Complete | 2026-03-08 |
| 11. Inline Logging Protocol | v1.4 | 2/2 | Complete | 2026-03-08 |
| 12. Dispatch Architecture Rewrite | v1.4 | 3/3 | Complete | 2026-03-09 |
| 13. Documentation | v1.4 | 1/1 | Complete | 2026-03-09 |
| 14. Directory Restructuring | v1.8 | 2/2 | Complete | 2026-03-10 |
| 15. Path Resolution and Bundle | v1.8 | 2/2 | Complete | 2026-03-10 |
| 16. CLO Foundation | v1.9 | 2/2 | Complete | 2026-03-12 |
| 17. Configuration | v1.9 | Complete    | 2026-03-12 | 2026-03-12 |
| 18. Agent Cross-Wiring | 2/2 | Complete   | 2026-03-12 | - |
| 19. Documentation | v1.9 | 0/? | Not started | - |

---
*Roadmap created: 2026-02-22*
*Last updated: 2026-03-12 -- Phase 18 plans created (2 plans)*
