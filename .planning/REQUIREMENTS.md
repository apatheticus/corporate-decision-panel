# Requirements: Corporate Decision Panel v1.9

**Defined:** 2026-03-12
**Core Value:** C-suite agents must deliberate with independent perspectives, supported by expert team lead collaboration within their divisions.

## v1.9 Requirements

Requirements for the Chief Legal Officer role addition. Each maps to roadmap phases.

### CLO Agent

- [x] **CLO-01**: CLO C-suite agent definition with Skeptic disposition, legal exposure mandate, and full phase participation (Phase 0–5)
- [x] **CLO-02**: CLO produces domain recommendation synthesizing team lead findings with confidence level, key risks, and flagged internal contradictions
- [x] **CLO-03**: CLO carries reverse-advocate mitigation — when recommending against an action, names the strongest argument for proceeding
- [x] **CLO-04**: CLO participates in Pre-Mortem Challenge (Phase 4.5, Tier 3) from legal failure perspective
- [x] **CLO-05**: CLO activates minimum 2 and maximum 5 team leads based on issue relevance

### Team Leads

- [x] **TEAM-01**: Corporate Governance & Entity Lead with fiduciary obligation lens, 3 forcing questions, cross-domain challenge to CFO Controller
- [x] **TEAM-02**: Contracts & Commercial Lead with liability allocation lens, 3 forcing questions, cross-domain challenge to COO Vendor/Procurement Mgr
- [x] **TEAM-03**: Regulatory & Government Compliance Lead with enforcement consequence lens, 3 forcing questions, cross-domain challenge to CISO Compliance/GRC
- [x] **TEAM-04**: Employment & Labor Law Lead with workforce legal exposure lens, 3 forcing questions, cross-domain challenge to CAO HR/People Ops
- [x] **TEAM-05**: IP & Data Privacy Lead with IP protection and data obligation lens, 3 forcing questions, dual cross-domain challenges to CTO Data/Analytics and CISO Security Architecture

### CAO Adjustment

- [ ] **CAO-01**: Legal/Contracts Lead removed from CAO team lead roster (agent file deleted)
- [ ] **CAO-02**: CAO agent definition updated — no Legal/Contracts references, legal routes to CLO note added
- [ ] **CAO-03**: All references to CAO Legal/Contracts Lead across codebase swept and updated (22 files identified in research)
- [ ] **CAO-04**: VP Sales Business Development Lead cross-domain challenge re-wired from CAO Legal/Contracts to CLO Contracts & Commercial

### Routing & Modes

- [x] **ROUT-01**: CLO added to default activation for Strategic, Personnel, and Compliance/Risk decision types
- [x] **ROUT-02**: CLO included in all 5 full-activation threshold scenarios
- [x] **ROUT-03**: CSO-CLO research interaction documented in routing table
- [x] **MODE-01**: CLO weighting added to all 5 decision modes in config/decision-modes.md (H/L/M/Confidence/H)
- [ ] **MODE-02**: CLO weighting added to all 5 decision mode sections in agents/ceo.md (skeptic group updates)

### Integration

- [x] **INTG-01**: Company profile archetypes updated with CLO-specific behavior (Technology/SaaS, Professional Services, Regulated Industry, Manufacturing)
- [x] **INTG-02**: CLO override mechanism documented in company-profile.md
- [x] **INTG-03**: Phase 0 Shared Consciousness Broadcast updated to include CLO
- [x] **INTG-04**: Engineered dissent balance updated to 5 skeptics / 2 advocates / 1 systemic / 1 investigative / 1 synthesizer

### Documentation

- [ ] **DOCS-01**: SKILL.md updated — CLO in available roles, agent counts (10 C-suite, 38 team leads), engineered dissent description
- [ ] **DOCS-02**: README.md updated — Available Roles, C-Suite Roster table, Team Lead Roster table, architecture diagrams, engineered dissent balance
- [ ] **DOCS-03**: All documentation agent/team lead counts verified against actual directory listing

## v2 Requirements

None — this milestone is self-contained per the FRD.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Production pipeline changes | CLO is automatically available through existing dispatch — no artifact generation changes needed |
| Engagement tier structure changes | CLO slots into existing tier logic |
| Existing decision mode definitions | Only adding CLO weighting rows, not changing mode logic |
| Slash command syntax changes | CLO available through existing `/cdp:panel clo:` and `/cdp:consult clo:` syntax |
| CEO core synthesis logic changes | Only mode weighting updates, not synthesis algorithm |
| Python code changes | Zero code changes — pure content authoring milestone |
| install.py / apply_models.py changes | Both auto-discover new files by directory convention |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLO-01 | Phase 16 | Complete |
| CLO-02 | Phase 16 | Complete |
| CLO-03 | Phase 16 | Complete |
| CLO-04 | Phase 16 | Complete |
| CLO-05 | Phase 16 | Complete |
| TEAM-01 | Phase 16 | Complete |
| TEAM-02 | Phase 16 | Complete |
| TEAM-03 | Phase 16 | Complete |
| TEAM-04 | Phase 16 | Complete |
| TEAM-05 | Phase 16 | Complete |
| ROUT-01 | Phase 17 | Complete |
| ROUT-02 | Phase 17 | Complete |
| ROUT-03 | Phase 17 | Complete |
| MODE-01 | Phase 17 | Complete |
| MODE-02 | Phase 18 | Pending |
| INTG-01 | Phase 17 | Complete |
| INTG-02 | Phase 17 | Complete |
| INTG-03 | Phase 17 | Complete |
| INTG-04 | Phase 17 | Complete |
| CAO-01 | Phase 18 | Pending |
| CAO-02 | Phase 18 | Pending |
| CAO-03 | Phase 18 | Pending |
| CAO-04 | Phase 18 | Pending |
| DOCS-01 | Phase 19 | Pending |
| DOCS-02 | Phase 19 | Pending |
| DOCS-03 | Phase 19 | Pending |

**Coverage:**
- v1.9 requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0

---
*Requirements defined: 2026-03-12*
*Last updated: 2026-03-12 after roadmap creation*
