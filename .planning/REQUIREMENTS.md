# Requirements: Corporate Decision Panel

**Defined:** 2026-03-10
**Core Value:** C-suite agents must deliberate with independent perspectives, supported by expert team lead collaboration within their divisions.

## v1.8 Requirements

Requirements for v1.8 File Organization milestone. Each maps to roadmap phases.

### Deliberation Directory

- [x] **DLIB-01**: Recommendation files (`_RECOMMENDATION_{role}.md`) are written to `deliberation/` subdirectory
- [x] **DLIB-02**: Pre-mortem files (`_PREMORTEM_{role}.md`) are written to `deliberation/` subdirectory
- [x] **DLIB-03**: CSO dossier (`_DOSSIER_cso.md`) is written to `deliberation/` subdirectory

### Reports Directory

- [x] **REPT-01**: Production wave reports (`_REPORT_{agent}.md`) are written to `reports/` subdirectory
- [x] **REPT-02**: Creative brief (`_CREATIVE_BRIEF_{slug}.md`) is written to `reports/` subdirectory

### Production Bundle

- [ ] **BNDL-01**: A `.zip` file containing all production outputs (DOCX, PPTX, PDFs, HTML, images) is created in the session directory

### Path Updates

- [x] **PATH-01**: All agents that create deliberation/report files update their output paths to use new subdirectories
- [x] **PATH-02**: All agents/scripts that read deliberation/report files update their input paths for new locations
- [x] **PATH-03**: CEO dispatch and synthesis references resolve correctly with new deliberation paths
- [x] **PATH-04**: CCO production pipeline wave references resolve correctly with new report paths

## Future Requirements

Deferred from v1.0 backlog -- not in current roadmap.

- **MODL-01**: Model profile switch -- Flash for development, Pro for production
- **MODL-02**: Per-infographic model selection -- Pro for text-heavy, Flash for simpler
- **MODL-03**: Concurrent generation with IPM-aware rate limiting
- **MODL-04**: Imagen 4 as alternative model option

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Moving production outputs to subdirectory | Breaks `index.html` relative paths to `images/`; zip bundle solves sharing need instead |
| Reorganizing `images/` subdirectory | Already organized, no change needed |
| Reorganizing `build/` subdirectory | Already organized, no change needed |
| Reorganizing `logs/` subdirectory | Already organized, no change needed |
| Reorganizing `sub-questions/` subdirectory | Already organized, no change needed |
| Moving RECORD.md from root | Central artifact, stays at session root for discoverability |
| Backward compatibility with old flat layout | Clean break -- no dual-path support |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DLIB-01 | Phase 14 | Complete |
| DLIB-02 | Phase 14 | Complete |
| DLIB-03 | Phase 14 | Complete |
| REPT-01 | Phase 14 | Complete |
| REPT-02 | Phase 14 | Complete |
| BNDL-01 | Phase 15 | Pending |
| PATH-01 | Phase 14 | Complete |
| PATH-02 | Phase 15 | Complete |
| PATH-03 | Phase 15 | Complete |
| PATH-04 | Phase 15 | Complete |

**Coverage:**
- v1.8 requirements: 10 total
- Mapped to phases: 10
- Unmapped: 0

---
*Requirements defined: 2026-03-10*
*Last updated: 2026-03-10 after roadmap revision (production stays at root, zip bundle added)*
