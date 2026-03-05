# Research Summary: v1.1 Initial Design Concerns

**Domain:** Integrating 11 concern fixes into existing CDP multi-agent orchestration system
**Researched:** 2026-03-04
**Overall confidence:** HIGH

## Executive Summary

The 11 v1.1 concern fixes integrate cleanly into the existing CDP architecture because the system is fundamentally a prompt-and-configuration system -- there is no application code for the deliberation engine. All changes are markdown specification edits, Python script additions, or new test scenario documents. The system's configuration-as-code pattern means "architecture changes" are document edits, not code refactors.

The most critical finding is that the CEO agent (`agents/ceo.md`, 682 lines) is the gravitational center of the system. Six of eleven concerns either modify, extract from, or add to content currently embedded in this file. The CEO extraction (concern #1) is therefore the foundational change -- it separates the orchestration protocol from CEO identity, creating a clean target for subsequent orchestration augmentations (pre-flight, CSO timeout) and eliminating content duplication with config files (routing thresholds, mode weightings).

The remaining concerns split into three independent tracks: C-suite agent augmentation (executive summaries), config formalization (routing trees, mode weightings, cost formula), and test scenario creation. These tracks have minimal dependencies on each other, enabling parallel work or flexible ordering after the CEO extraction is complete.

No existing components need to be deleted or replaced. No data flows change. No interfaces break. This is purely additive or extractive work on an existing, stable architecture.

## Key Findings

**Stack:** No technology changes. Markdown specifications + one new Python cleanup script.
**Architecture:** CEO agent is a monolith containing three distinct concerns (identity, orchestration protocol, triage). Extraction is the foundational fix.
**Critical pitfall:** Extracting the orchestration protocol but leaving "summary" duplicates in the CEO agent creates two sources of truth. Zero duplication is the only safe approach. Additionally, executive summaries must be structured navigation aids, not prose compressions that flatten the analytical nuance CDP depends on.

## Implications for Roadmap

Based on research, suggested phase structure:

1. **Foundation** - CEO extraction + executive summaries
   - Addresses: Concerns #1 (CEO refactor) and #4 (executive summaries)
   - Avoids: Bloating the CEO agent further with orchestration additions
   - Rationale: #1 creates the clean document where subsequent orchestration changes go. #4 is independent and high-value (token cost reduction), touches only C-suite agents so no conflict with CEO extraction.

2. **Orchestration Hardening** - Pre-flight, CSO timeout, session cleanup
   - Addresses: Concerns #2 (pre-flight), #3 (CSO timeout), #8 (cleanup)
   - Avoids: Adding orchestration logic to the wrong document
   - Rationale: #2 and #3 add to the extracted orchestration protocol. #8 is independent but groups naturally with production pipeline work.

3. **Specification Formalization** - Routing trees, mode weightings, cost formula
   - Addresses: Concerns #5 (routing trees), #6 (mode weightings), #7 (cost formula)
   - Avoids: Testing against ambiguous specifications
   - Rationale: #5 removes duplication revealed by CEO extraction. #6 and #7 expand `config/decision-modes.md` and are naturally grouped.

4. **Test Scenarios** - Routing test, pre-mortem test, mode sensitivity test
   - Addresses: Concerns #9 (Tier 2 routing), #10 (pre-mortem), #11 (mode sensitivity)
   - Avoids: Writing tests before specifications are formalized
   - Rationale: Test scenarios validate the specifications from Phases 2-3. Writing them last ensures test criteria match formalized specs.

**Phase ordering rationale:**
- Phase 1 before Phase 2: Extraction creates the target document for orchestration additions
- Phase 1 before Phase 3: Duplication cleanup in routing/modes is cleaner after extraction
- Phase 3 before Phase 4: Tests should validate formalized specs, not ambiguous prose
- Phase 1 items can run in parallel: CEO extraction and executive summaries touch disjoint files

**Research flags for phases:**
- Phase 1: Standard extraction work, unlikely to need deeper research. The key risk is prompt-level regression (agent behavior changes due to document restructuring). Characterization tests before refactoring are essential.
- Phase 2: CSO timeout handling needs clarity on Claude Code agent timeout mechanisms (maxTurns vs wall-clock). Production pre-flight should be warnings-only for optional dependencies, never blocking.
- Phase 3: Standard formalization. Decision trees should be structured judgment with exemplars, not rigid algorithms that kill CEO routing judgment.
- Phase 4: Test scenarios are specification-level (not automated). Behavioral validation requires running actual deliberations.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Architecture | HIGH | Direct reading of all affected source files; no external dependencies |
| Integration points | HIGH | All 11 concerns analyzed against actual file contents, line-level |
| Build order | HIGH | Dependency analysis based on file-level conflicts and content dependencies |
| Scope estimates | MEDIUM | Line count estimates are reasonable but may vary based on desired detail level |
| Pitfall severity | MEDIUM-HIGH | Pitfalls derived from architectural analysis and multi-agent system patterns |

## Gaps to Address

- Claude Code agent timeout mechanisms: How does Claude Code handle agent tasks that run too long? Relevant for CSO timeout handling (concern #3). Likely via maxTurns, but needs verification.
- `/cdp:cleanup` slash command integration: The exact mechanism for adding new slash commands needs verification during implementation.
- Test scenario validation approach: Whether test scenarios should include a semi-automated validation script or remain purely manual evaluation criteria.
- Executive summary impact on fault-line quality: Should be validated empirically -- run a deliberation with and without summaries and compare Decision Record analytical depth.
