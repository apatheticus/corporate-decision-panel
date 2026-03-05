# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — MVP

**Shipped:** 2026-03-04
**Phases:** 4 | **Plans:** 11 | **Sessions:** ~10

### What Was Built
- Config parser and 4-step pre-flight API validator
- Template-to-prompt serializer converting JSON templates to natural language
- End-to-end Gemini API image generation for all 6 infographic types
- Error handling with exponential backoff, content block detection, placeholder PNG fallback
- AI vision quality validation with corrective retry loop
- Session orchestrator with adaptive rate limiting and summary reporting
- Complete documentation rewrite removing browser automation

### What Worked
- TDD approach (red-green-refactor) caught design issues early — dataclass contracts were solid by Phase 3
- Phase dependency chain was clean: config → generation → reliability → docs
- Gap closure plan (03-03) caught OK+WARN propagation before it became tech debt
- Live integration tests with real API calls validated the full pipeline
- 37 minutes total execution time across 11 plans — fast iteration

### What Was Inefficient
- ROADMAP.md plan checkboxes got out of sync with execution — required tech debt cleanup
- session.py CLI entry point was documented but never implemented — caught only in audit
- Nyquist validation defined but Wave 0 not executed during phases — compliance gap

### Patterns Established
- `GenerationResult` dataclass as universal return type with boolean flags (`had_rate_limit`, `warning_only`)
- Non-blocking quality gates — validation errors produce warnings, not failures
- Factory fixture pattern (`make_config` callable) for parameterized test data
- Placeholder regex with `(default: X)` extraction for config parsing

### Key Lessons
1. Audit before milestone completion catches stale documentation and missing CLI entry points
2. SDK retry must be disabled when implementing custom retry — prevents double-retry explosion
3. AI vision validation is a pragmatic quality gate — catches data label errors without OCR complexity
4. Inter-call delays with adaptive doubling handle rate limiting better than fixed delays

### Cost Observations
- Model mix: ~90% sonnet (execution), ~10% opus (research, planning, audit)
- Sessions: ~10 across 10 days
- Notable: 37min total execution for 11 plans — highly efficient for API migration

---

## Milestone: v1.1 — Initial Design Concerns

**Shipped:** 2026-03-05
**Phases:** 5 | **Plans:** 11 | **Tasks:** 19

### What Was Built
- CEO agent refactored from 682-line monolith to 348-line focused agent + 307-line orchestration protocol
- Executive summary blocks added to all 8 C-suite agents with summary-first synthesis and conflict-triggered deep-dive
- Pre-flight dependency validation for production pipeline (required fail, optional warn)
- CSO timeout protection (maxTurns: 25) with RESEARCH STATUS flag propagation to all C-suite agents
- Session cleanup command (/cdp:cleanup) with age-based filtering and confirmation
- Routing threshold decision trees with diagnostic questions and calibration exemplars
- Directional weighting tables for all 5 decision modes
- Multi-mode cost formula with generic variables and 4 worked examples
- Test scenarios: Tier 2 partial activation, pre-mortem degraded input, mode sensitivity consistency
- Integration polish closing 2 audit-identified gaps (threshold template field, cleanup discoverability)

### What Worked
- Codebase audit approach identified 11 concrete concerns → mapped cleanly to 4 requirements categories and 5 phases
- Phase dependency chain ensured no duplication: CEO extraction first → hardening and specs go to right documents → tests validate formalized specs
- All work was markdown edits — no architecture changes, enabling very fast execution (~10 hours total)
- Milestone audit after Phase 8 caught 2 integration gaps (INT-01, INT-02) → Phase 9 closed both
- 3-source cross-reference for requirements (VERIFICATION + SUMMARY + traceability) eliminated false positives
- Integration checker agent caught label inconsistency and spec gap that phase-level verifiers missed

### What Was Inefficient
- ROADMAP.md progress table plan counts got stale (showed 1/3 and 0/3 for completed phases) — same issue as v1.0
- SUMMARY.md format lacks `one_liner` and `tasks_completed` frontmatter fields — forced manual extraction during milestone completion
- Initial milestone audit was run mid-milestone (before Phase 9), requiring a re-audit after gap closure
- Nyquist validation was largely skipped — 4/5 phases PARTIAL compliance, only Phase 7 fully compliant

### Patterns Established
- Config extraction pattern: monolithic agent → focused agent + referenced config document
- RESEARCH STATUS flag as standalone pattern-matchable line in broadcast (not embedded in prose)
- Conditional field pattern: C-suite agents conditionally include Research Basis/RESEARCH CAVEAT based on broadcast flag
- Countable dimension pattern: quantitative criteria using CONVERGE/PARTIAL/DIVERGE instead of numeric ratios
- Escalation recommendation pattern: thresholds at Tier 2 surface as Escalation Note, not as routing override

### Key Lessons
1. Run milestone audit only after ALL phases complete — avoids re-audit overhead
2. Integration checker catches cross-phase wiring issues that individual phase verifiers miss — worth the cost
3. Markdown-only milestones execute very fast (~10h for 11 plans) but ROADMAP sync still needs attention
4. User-specified roles should always override system recommendations — preserves user intent
5. Test scenarios should validate formalized specs, not prose — Phase 7→8 ordering was correct
6. LLM-appropriate quantification (directional indicators, countable dimensions) avoids false precision

### Cost Observations
- Model mix: ~80% sonnet (execution, verification), ~20% opus (audit, planning, research)
- Total execution: ~10 hours across ~8 sessions
- Notable: 19 tasks across 11 plans in 5 phases — very high throughput for specification work

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | ~10 | 4 | Initial project — established TDD + gap closure patterns |
| v1.1 | ~8 | 5 | Specification work — established config extraction + integration audit patterns |

### Cumulative Quality

| Milestone | Tests | Coverage | Key Additions |
|-----------|-------|----------|---------------|
| v1.0 | 188 | n/a | 5 Python modules (config, preflight, generate, validation, session) |
| v1.1 | 188 | n/a | 38 markdown files (agents, config, templates, test scenarios) |

### Top Lessons (Verified Across Milestones)

1. Audit milestone before completion — catches documentation drift, missing interfaces, and integration gaps (v1.0: session.py CLI, v1.1: INT-01/INT-02)
2. Non-blocking quality gates are more robust than hard failures for AI-generated content
3. ROADMAP.md plan completion counts drift during execution — needs automation or post-phase sync
4. Integration checker catches cross-phase issues that individual verifiers miss — run at milestone level
