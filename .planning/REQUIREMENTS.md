# Requirements: CDP v1.1 Initial Design Concerns

**Defined:** 2026-03-04
**Core Value:** Infographic generation must work without browser interaction -- a single API call per infographic that returns a PNG, driven by the same Decision Record data.

## v1.1 Requirements

Requirements for v1.1 milestone. Each maps to roadmap phases.

### CEO Architecture

- [x] **ARCH-01**: CEO orchestration protocol is extracted into a separate referenced document, with CEO agent focused on identity and synthesis
- [x] **ARCH-02**: CEO agent is under 350 lines after extraction, with zero duplication of orchestration logic
- [x] **ARCH-03**: C-suite agents produce structured executive summary fields (role, position, confidence, key-risks) alongside full recommendations
- [x] **ARCH-04**: CEO reads executive summaries first and references full recommendations only when ambiguity requires it

### Orchestration Resilience

- [x] **ORCH-01**: Production pipeline validates required dependencies before artifact generation, failing explicitly with install instructions
- [x] **ORCH-02**: Production pipeline warns (does not block) when optional dependencies are missing, listing which artifacts will be skipped
- [x] **ORCH-03**: CSO Phase 1.5 has a maxTurns-based timeout that broadcasts partial results with explicit gap reporting if research is incomplete
- [x] **ORCH-04**: C-suite agents annotate recommendations with confidence caveats when CSO research is incomplete
- [x] **ORCH-05**: Session cleanup script deletes old session directories with confirmation prompt and age-based filtering

### Specification Clarity

- [x] **SPEC-01**: Each of the 5 routing threshold conditions has structured diagnostic questions with YES/NO evaluation criteria
- [x] **SPEC-02**: Routing thresholds include calibration exemplars (concrete decision examples showing how each threshold evaluates)
- [ ] **SPEC-03**: CEO explicitly evaluates each threshold in Phase 1 framing output, making routing auditable
- [x] **SPEC-04**: Each of the 5 decision modes has an explicit directional weighting table (HIGH/MODERATE/LOW per perspective)
- [x] **SPEC-05**: Multi-mode cost formula is documented with actual calculation: (1 x Domain Analysis) + (N x CEO Synthesis)
- [x] **SPEC-06**: Multi-mode documentation includes example cost calculations for typical panel sizes

### Test Coverage

- [ ] **TEST-01**: Test scenario validates Tier 2 partial activation correctly excludes non-requested C-suite agents even when full-activation thresholds are met
- [ ] **TEST-02**: Test scenario validates Phase 4.5 Pre-Mortem executes correctly when one or more C-suite agents have missing/partial recommendations
- [ ] **TEST-03**: Mode sensitivity criteria defines quantitative thresholds for LOW/MEDIUM/HIGH divergence ratings
- [ ] **TEST-04**: Test scenario validates mode sensitivity ratings are consistent across similar decision types

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Performance Optimization

- **PERF-01**: Synthesis clustering for panels with 9+ C-suite agents (intermediate synthesizers pre-aggregate)
- **PERF-02**: Team lead timeout enforcement with low-confidence fallback marking
- **PERF-03**: Panel size limit enforcement with context window measurement

### Security Hardening

- **SEC-01**: Runtime file permission check before reading company.md
- **SEC-02**: Redact flag for session exports that removes company data
- **SEC-03**: Pre-session warning for sensitive patterns in company context
- **SEC-04**: API key migration from config.md to environment variables or OS credential store

### Additional Concerns

- **DEBT-01**: Image Agent session-level submission counter for budget enforcement
- **DEBT-02**: Company context syntax/schema validation on load
- **DEBT-03**: Model profile switch (Flash for dev, Pro for production)
- **DEBT-04**: Per-infographic model selection
- **DEBT-05**: Concurrent generation with IPM-aware rate limiting

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Automated agent testing framework | LLM outputs are non-deterministic; false precision. Use specification-level test scenarios instead. |
| Numeric mode weights (1.5x, 0.7x) | LLMs cannot reliably apply numeric multipliers. Directional indicators (HIGH/MODERATE/LOW) are appropriate. |
| Session archival with compression | Over-engineered for local dev artifacts. Simple delete-with-confirmation is sufficient. |
| CEO agent full rewrite | Extraction is sufficient. Identity/judgment sections are proven and stable. |
| Mode-specific C-suite behavior | Violates core design principle: domain analysis is mode-independent. Modes affect CEO synthesis only. |
| Dynamic AI-driven routing | Removes auditability. CDP routing transparency is a core design principle. |
| Agent-to-agent direct communication | Breaks two-tier visibility principle. Phase 4.5 Pre-Mortem provides structured cross-agent awareness. |
| Blocking pre-flight for optional dependencies | Converts optional features into hard requirements. Warn-only is the correct pattern. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| ARCH-01 | Phase 5 | Complete |
| ARCH-02 | Phase 5 | Complete |
| ARCH-03 | Phase 5 | Complete |
| ARCH-04 | Phase 5 | Complete |
| ORCH-01 | Phase 6 | Complete |
| ORCH-02 | Phase 6 | Complete |
| ORCH-03 | Phase 6 | Complete |
| ORCH-04 | Phase 6 | Complete |
| ORCH-05 | Phase 6 | Complete |
| SPEC-01 | Phase 7 | Complete |
| SPEC-02 | Phase 7 | Complete |
| SPEC-03 | Phase 7 | Pending |
| SPEC-04 | Phase 7 | Complete |
| SPEC-05 | Phase 7 | Complete |
| SPEC-06 | Phase 7 | Complete |
| TEST-01 | Phase 8 | Pending |
| TEST-02 | Phase 8 | Pending |
| TEST-03 | Phase 8 | Pending |
| TEST-04 | Phase 8 | Pending |

**Coverage:**
- v1.1 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---
*Requirements defined: 2026-03-04*
*Last updated: 2026-03-04 after roadmap creation*
