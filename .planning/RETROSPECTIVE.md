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

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | ~10 | 4 | Initial project — established TDD + gap closure patterns |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.0 | 188 | n/a | 5 modules (config, preflight, generate, validation, session) |

### Top Lessons (Verified Across Milestones)

1. Audit milestone before completion — catches documentation drift and missing interfaces
2. Non-blocking quality gates are more robust than hard failures for AI-generated content
