# Roadmap: Corporate Decision Panel

## Milestones

- ✅ **v1.0 MVP** -- Phases 1-4 (shipped 2026-03-04)
- ✅ **v1.1 Initial Design Concerns** -- Phases 5-9 (shipped 2026-03-05)
- ✅ **v1.4 Team Refactor** -- Phases 10-13 (shipped 2026-03-09)
- 🚧 **v1.8 File Organization** -- Phases 14-15 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4) -- SHIPPED 2026-03-04</summary>

- [x] Phase 1: Config and Pre-flight (2/2 plans) -- completed 2026-03-04
- [x] Phase 2: API Integration (3/3 plans) -- completed 2026-03-04
- [x] Phase 3: Error Handling and Quality (3/3 plans) -- completed 2026-03-04
- [x] Phase 4: Scale and Docs (3/3 plans) -- completed 2026-03-04

</details>

<details>
<summary>✅ v1.1 Initial Design Concerns (Phases 5-9) -- SHIPPED 2026-03-05</summary>

- [x] Phase 5: CEO Architecture (2/2 plans) -- completed 2026-03-04
- [x] Phase 6: Orchestration Hardening (3/3 plans) -- completed 2026-03-05
- [x] Phase 7: Specification Formalization (3/3 plans) -- completed 2026-03-05
- [x] Phase 8: Test Scenarios (2/2 plans) -- completed 2026-03-05
- [x] Phase 9: Integration Polish (1/1 plan) -- completed 2026-03-05

</details>

<details>
<summary>✅ v1.4 Team Refactor (Phases 10-13) -- SHIPPED 2026-03-09</summary>

- [x] Phase 10: Production Quick Wins (2/2 plans) -- completed 2026-03-08
- [x] Phase 11: Inline Logging Protocol (2/2 plans) -- completed 2026-03-08
- [x] Phase 12: Dispatch Architecture Rewrite (3/3 plans) -- completed 2026-03-09
- [x] Phase 13: Documentation (1/1 plan) -- completed 2026-03-09

</details>

### v1.8 File Organization (In Progress)

**Milestone Goal:** Organize session output files into functional subdirectories (deliberation artifacts and reports) while keeping production outputs at session root, and provide a zip bundle for easy sharing.

- [x] **Phase 14: Directory Restructuring** - Agents write deliberation artifacts and reports to organized subdirectories instead of session root (completed 2026-03-10)
- [x] **Phase 15: Path Resolution and Bundle** - All readers resolve files at new locations and a zip bundle packages production outputs for sharing (completed 2026-03-10)

## Phase Details

### Phase 14: Directory Restructuring
**Goal**: Deliberation artifacts and reports land in organized subdirectories instead of the flat session root
**Depends on**: Nothing (first phase of v1.8)
**Requirements**: DLIB-01, DLIB-02, DLIB-03, REPT-01, REPT-02, PATH-01
**Success Criteria** (what must be TRUE):
  1. Running a full deliberation produces recommendation files (`_RECOMMENDATION_{role}.md`) inside `{session}/deliberation/`, not the session root
  2. Running a full deliberation produces pre-mortem files (`_PREMORTEM_{role}.md`) and CSO dossier (`_DOSSIER_cso.md`) inside `{session}/deliberation/`, not the session root
  3. Running CCO production produces wave reports (`_REPORT_{agent}.md`) and creative briefs (`_CREATIVE_BRIEF_{slug}.md`) inside `{session}/reports/`, not the session root
  4. All production outputs (DOCX, PPTX, PDFs, HTML) and RECORD.md remain at the session root -- no files moved that should stay
**Plans**: 2 plans

Plans:
- [ ] 14-01-PLAN.md -- Deliberation directory setup and write paths (session mkdir, C-suite agent write paths, orchestration protocol write refs, SKILL.md)
- [ ] 14-02-PLAN.md -- Reports directory write paths (CCO team lead write paths, Creative Brief file output, CCO dispatch protocol write refs)

### Phase 15: Path Resolution and Bundle
**Goal**: All agents and scripts that read reorganized files find them at new locations, and production outputs are bundled into a zip for sharing
**Depends on**: Phase 14
**Requirements**: PATH-02, PATH-03, PATH-04, BNDL-01
**Success Criteria** (what must be TRUE):
  1. CEO synthesis reads recommendations, pre-mortems, and dossier from `deliberation/` without path errors
  2. CCO production pipeline reads wave reports and creative briefs from `reports/` without path errors
  3. No agent or script references old flat session-root paths for any file that was moved to `deliberation/` or `reports/`
  4. A `.zip` file containing all production outputs (DOCX, PPTX, PDFs, HTML, images) is created in the session directory after production completes
**Plans**: 2 plans

Plans:
- [ ] 15-01-PLAN.md -- READ-side path migration for all deliberation and report file references across CEO, CCO, orchestration protocol, dispatch protocol, resume command, and SKILL.md
- [ ] 15-02-PLAN.md -- Zip bundle step for Publisher (Tier 2/3) and SKILL.md (Tier 1), production re-run cleanup update, directory structure documentation

## Progress

**Execution Order:**
Phases execute in numeric order: 14 -> 15

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
| 15. Path Resolution and Bundle | 2/2 | Complete   | 2026-03-10 | - |

---
*Roadmap created: 2026-02-22*
*Last updated: 2026-03-10 -- Phase 15 planned (2 plans, 2 waves: read-path migration + zip bundle)*
