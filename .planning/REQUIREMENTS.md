# Requirements: Corporate Decision Panel

**Defined:** 2026-03-08
**Core Value:** C-suite agents must deliberate with independent perspectives, supported by expert team lead collaboration within their divisions.

## v1.4 Requirements

Requirements for Team Refactor milestone. Each maps to roadmap phases.

### Infographic Pipeline

- [x] **INFRA-01**: Slug alias map resolves shorthand slugs (`fault-lines`, `risk-matrix`, `action-plan`) to canonical template slugs in `generate_infographic.py` and `session.py`
- [x] **INFRA-02**: Graphic designer agent definition uses correct canonical slugs (`fault-line-map`, `risk-opportunity-matrix`, `action-plan-timeline`)
- [x] **INFRA-03**: Validation accepts PARTIAL labels for high-density infographic types (`routing-diagram`) without triggering failure
- [x] **INFRA-04**: `validate_infographic()` accepts `type_slug` parameter and applies lenient validation prompt conditionally via `LENIENT_TYPES` set

### Agent Infrastructure

- [x] **AGINF-01**: Publisher agent uses `cd <skill-directory> &&` prefix for `python3 -m scripts.build_results_pdf` invocation
- [x] **AGINF-02**: All 48 agent files use inline logging protocol summary instead of `config/logging-protocol.md` file path reference

### Dispatch Architecture

- [ ] **DISP-01**: `config/dispatch-protocol.md` rewritten for CEO-as-universal-dispatcher with sub-question file convention (`{session}/sub-questions/{role}/{team-lead-name}.md`)
- [ ] **DISP-02**: `config/cco-dispatch-protocol.md` rewritten for CEO-managed production wave sequencing with CCO as Creative Brief author + editorial coordinator
- [ ] **DISP-03**: `config/orchestration-protocol.md` Phases 2/3/4 updated for CEO division team dispatch flow (TeamCreate per role, two-wave dispatch, sub-question file polling)
- [ ] **DISP-04**: `config/orchestration-protocol.md` Production Spawn Sequence updated for CEO-managed CCO wave dispatch
- [x] **DISP-05**: CEO agent updated with TeamCreate instructions, team lead dispatch with sub-questions, sub-question file polling, and CCO wave management
- [ ] **DISP-06**: 8 analytical C-suite agents transformed -- Mode B removes TeamCreate/Agent dispatch, adds sub-question file writing + teammate message receiving
- [ ] **DISP-07**: CCO agent transformed to Creative Brief author + editorial coordinator within CEO-managed production team
- [x] **DISP-08**: CSO Phase 1.5 dispatch integrated with division team pattern (special timing: dispatched before other C-suite)
- [ ] **DISP-09**: Sub-question directory (`{session}/sub-questions/`) documented in Session Output Setup
- [ ] **DISP-10**: No stale `TeamCreate`, `Agent.*team_name`, or `SendMessage.*shutdown_request` references remain in C-suite agent definitions

### Documentation

- [ ] **DOCS-01**: Large file read guidance added to `config/orchestration-protocol.md` Phase 4 synthesis section
- [ ] **DOCS-02**: Large file read guidance added to `agents/ceo.md` recommendation synthesis section

## Future Requirements

Deferred from v1.0 backlog. Not in current roadmap.

### Image Generation

- **IMGN-01**: Model profile switch -- Flash for development, Pro for production
- **IMGN-02**: Per-infographic model selection -- Pro for text-heavy, Flash for simpler
- **IMGN-03**: Concurrent generation with IPM-aware rate limiting
- **IMGN-04**: Imagen 4 as alternative model option

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Nested team support workaround (`claude -p` hack) | Loses visibility, context sharing, error propagation. Work within platform constraint. |
| C-suite direct team lead dispatch | Architecturally impossible in Claude Code -- only the lead can use Agent/TeamCreate |
| CEO inline sub-question formulation | Bypasses C-suite domain expertise -- team leads would receive generic framing |
| Dynamic slug normalization (fuzzy matching) | Only 3 known mismatches -- static alias map is sufficient |
| Per-infographic validation profiles | Overengineered for 6-type system -- `LENIENT_TYPES` set is sufficient |
| Event-driven sub-question notification | Over-engineering for polling model -- CEO polls directories |
| Schema validation for sub-question files | LLM-to-LLM communication -- convention-based format is appropriate |
| Agent-to-agent cross-division messaging | Violates engineered dissent -- divisions must remain isolated |
| ChatGPT/OpenAI API support | Gemini-only for now |
| Browser-based fallback | Clean break, no dual-path |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFRA-01 | Phase 10 | Complete |
| INFRA-02 | Phase 10 | Complete |
| INFRA-03 | Phase 10 | Complete |
| INFRA-04 | Phase 10 | Complete |
| AGINF-01 | Phase 10 | Complete |
| AGINF-02 | Phase 11 | Complete |
| DISP-01 | Phase 12 | Pending |
| DISP-02 | Phase 12 | Pending |
| DISP-03 | Phase 12 | Pending |
| DISP-04 | Phase 12 | Pending |
| DISP-05 | Phase 12 | Complete |
| DISP-06 | Phase 12 | Pending |
| DISP-07 | Phase 12 | Pending |
| DISP-08 | Phase 12 | Complete |
| DISP-09 | Phase 12 | Pending |
| DISP-10 | Phase 12 | Pending |
| DOCS-01 | Phase 13 | Pending |
| DOCS-02 | Phase 13 | Pending |

**Coverage:**
- v1.4 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0

---
*Requirements defined: 2026-03-08*
*Last updated: 2026-03-08 after roadmap creation*
