# Domain Pitfalls: v1.1 Concern Fixes

**Domain:** Adding concern fixes to existing CDP markdown-based agent orchestration system
**Researched:** 2026-03-04
**Confidence:** HIGH (derived from direct codebase analysis + multi-agent system failure patterns)

## Critical Pitfalls

Mistakes that cause regressions in the existing working system or silent behavior changes.

### Pitfall 1: Dual Source of Truth After CEO Extraction

**What goes wrong:** The orchestration protocol is extracted from `agents/ceo.md` into a new file, but the CEO agent retains a "summary" or "overview" of the protocol. Over time, edits are made to one document but not the other. The CEO agent follows its own summary (which is stale) instead of the canonical spec.
**Why it happens:** Natural tendency to leave a "helpful overview" in the CEO agent so it has context about what it orchestrates. Prompt refactoring is not code refactoring -- in code, extracting a function preserves behavior. In prompts, moving instructions changes attention distribution and instruction priority.
**Consequences:** CEO agent behavior diverges from canonical protocol. Routing, phase execution, or production triggering becomes inconsistent. Failures are silent -- subtly different decisions, not crashes.
**Prevention:** Zero duplication. The CEO agent references the orchestration protocol by filepath ("Follow the protocol in config/orchestration-protocol.md") without summarizing its contents. After extraction, grep for any phase-specific language ("Phase 0", "Phase 1", "broadcast", "routing table") remaining in the CEO agent. If found, it is residual duplication that must be removed.
**Detection:** Run the same test issue through the system before and after extraction. Compare routing decisions, activated agents, phase sequence, and synthesis structure verbatim.

### Pitfall 2: Executive Summaries That Flatten Analytical Nuance

**What goes wrong:** Executive Summaries are written as prose compressions that strip the specific details CDP depends on. "CFO opposes due to financial concerns" instead of "CFO opposes: Controller flags covenant breach risk at current debt-to-equity; Treasury projects cash runway drops below 18 months post-acquisition." The CEO's synthesis, operating on summaries, cannot identify specific fault lines.
**Why it happens:** LLM summarization inherently compresses toward consensus, flattening disagreement -- the exact signal CDP is designed to preserve. Efficiency pressure ("the summary is good enough") causes the CEO to stop reading full Domain Recommendations.
**Consequences:** Fault-line analysis becomes superficial. Dissenting views are generic. Decision mode application loses precision because the CEO cannot see specific concerns to weight differently.
**Prevention:** Define Executive Summary as a STRUCTURED NAVIGATION AID with mandatory fields, not prose compression: `Recommendation: Oppose | Confidence: Medium | Most Determinative Finding: [specific] | Key Risk: [specific] | Key Opportunity: [specific] | Internal Contradiction: [if any]`. The orchestration protocol must specify that the CEO uses Executive Summaries for orientation, then reads full Domain Recommendations for fault-line analysis and synthesis. Decision Records should cite full recommendations, not summaries.
**Detection:** Compare Decision Records before and after adding executive summaries. If Fault Line Analysis references only summary-level findings and never cites specific team lead findings or internal contradictions, the CEO is working from summaries only.

### Pitfall 3: Pre-Flight That Blocks Deliberation on Optional Dependencies

**What goes wrong:** Pre-flight validation for the production pipeline checks ALL dependencies (including optional production skills like PPTX, DOCX, PDF generation) and blocks the ENTIRE deliberation if any are missing. A user who only needs the Decision Record cannot run because a PDF skill is not installed.
**Why it happens:** Developers conflate "validate and warn" with "validate and block." The engineering instinct to fail fast converts optional features into hard requirements.
**Consequences:** New CDP installations require installing 4+ optional skills before the system works. Users who never needed PPTX/DOCX/PDF output are suddenly unable to run deliberations.
**Prevention:** Separate pre-flight into hard requirements (CEO agent exists, routing table exists) that block, and soft warnings (production skills available) that print a message and continue. The deliberation (Phases 0-5) produces the Decision Record independently of the production pipeline (Tasks A-E). A missing production skill should only affect the production pipeline.
**Detection:** Remove a required production skill, run Tier 3. If the deliberation itself fails or is blocked, the pre-flight is over-scoped.

### Pitfall 4: Routing Decision Trees That Kill CEO Judgment

**What goes wrong:** Decision trees for threshold conditions are formalized with so many criteria, sub-criteria, and edge cases that routing becomes a mechanical checklist. The CEO stops exercising routing judgment -- one of CDP's explicit design principles ("Routing is an analytical act").
**Why it happens:** Formalization pressure. "Make routing auditable" becomes "make routing deterministic." These are different goals. Some analytical dimensions (Irreversibility, Market Position Change, Domain Uncertainty) are genuinely better evaluated as judgment calls than as binary decision trees.
**Consequences:** Novel situations that do not fit the decision tree are misrouted. The CEO's routing reasoning becomes terse ("Irreversibility: YES per decision tree") instead of analytical. Over-activation or under-activation for edge cases.
**Prevention:** Formalize QUANTITATIVE thresholds (headcount >30%) with binary criteria. For QUALITATIVE thresholds (Irreversibility, Market Position Change, Domain Uncertainty), provide exemplars and anchor points rather than decision trees. Include explicit "CEO judgment" escape valves. Limit decision tree depth to 3 levels maximum. If the trees include routing for normal (non-threshold) decisions, they have expanded beyond their scope.
**Detection:** If decision trees have more than 3 levels of nesting, they are overengineered. If the CEO's routing reasoning in Decision Records becomes a checklist instead of analytical prose, formalization has gone too far.

## Moderate Pitfalls

### Pitfall 5: CSO Timeout as Hard Cutoff Instead of Scope Narrowing

**What goes wrong:** Phase 1.5 timeout kills the entire CSO research phase rather than gracefully degrading. If 3 of 5 team leads completed findings but the CSO did not finish synthesis, all research is discarded.
**Prevention:** Design for partial results. If CSO produces a partial dossier (some team leads completed), broadcast what is available with an explicit list of what is missing. C-suite agents should distinguish between "no research" and "partial research" and use available findings at stated confidence. The timeout should narrow scope (CEO directs CSO to focus on highest-priority sub-questions only) rather than kill the phase.

### Pitfall 6: Mode Weighting Tables That Contradict Prompt Modifiers

**What goes wrong:** Formalized weighting tables in `config/decision-modes.md` give explicit direction (e.g., "CISO gets HIGH weight in Guardian mode") that contradicts the nuanced prose CEO Prompt Modifier (which says "lean toward the skeptics unless the advocates present overwhelming evidence").
**Prevention:** Derive weighting tables FROM the existing prose modifiers, not independently. The tables should formalize what the prose already implies. Cross-reference each table entry against the corresponding prompt modifier before finalizing.

### Pitfall 7: Session Cleanup That Deletes Re-Run Data

**What goes wrong:** Cleanup script deletes a session directory containing `RECORD.md` that the user needs for `/cdp:production` re-runs. Or it deletes a session currently being written to by an active production pipeline.
**Prevention:** Check for recently-modified files before deletion. The `--older-than` filter should use directory modification time. Include `--dry-run` as the encouraged default. Never auto-delete without explicit user confirmation.

### Pitfall 8: Test Scenarios That Validate Structure Instead of Behavior

**What goes wrong:** Test scenarios for routing, pre-mortem, and mode sensitivity check output structure ("Does the Panel Assessment have all required sections?") rather than decision quality ("Does the CEO correctly exclude non-requested C-suite members?"). Structural tests always pass because the CEO is designed to produce structurally complete output.
**Prevention:** Write outcome-based test scenarios with expected routing decisions, not template compliance checks. "Expected: Only CFO and CTO activated. If CSO appears in the output, the test fails." Test the negative case explicitly. For mode sensitivity, define divergence criteria quantitatively.

### Pitfall 9: Cost Formula That Assumes Mode Independence

**What goes wrong:** The cost formula documents "domain analysis runs once" for multi-mode comparison. But Phase 0 broadcasts the active Decision Mode to all C-suite agents. If mode name influences domain analysis, the "1x domain analysis" claim is wrong.
**Prevention:** Verify mode independence empirically before documenting. If domain analysis is mode-influenced via Phase 0 broadcast, either document it honestly or consider removing mode from the Phase 0 broadcast for multi-mode comparisons.

## Minor Pitfalls

### Pitfall 10: Orchestration Protocol Placement Creates Category Confusion

**What goes wrong:** The extracted protocol is placed in `config/` alongside routing and mode configs, but it is procedural (do these steps in order) while config files are declarative (here are the rules). This confuses contributors about what belongs where.
**Prevention:** Consider whether `config/orchestration-protocol.md` is the right location vs `docs/orchestration-protocol.md` or an `agents/ceo/` subdirectory. The key criterion: the CEO agent must be able to reference it, and it must be clearly distinct from configuration data.

### Pitfall 11: Specification Changes Without Config Sync

**What goes wrong:** Changes to `config/routing-table.md` or `config/decision-modes.md` do not propagate to the CEO agent, which embeds copies of routing tables and mode definitions. Developer updates config but CEO follows its embedded copy.
**Prevention:** After CEO extraction, the CEO agent should reference config files at runtime rather than embedding copies. If embedding is necessary, version-tag both files and add a sync check to the testing protocol.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| CEO Extraction (Phase 1) | #1: Dual source of truth | Zero duplication. Grep for residual phase-specific language after extraction. |
| Executive Summaries (Phase 1) | #2: Summaries flatten nuance | Structured fields, not prose. CEO reads full recommendations for synthesis. |
| Production Pre-Flight (Phase 2) | #3: Over-blocking | Separate hard requirements (block) from soft warnings (continue). |
| CSO Timeout (Phase 2) | #5: Hard cutoff kills partial results | Scope narrowing, partial dossier broadcast, not binary success/failure. |
| Routing Trees (Phase 3) | #4: Over-formalization kills judgment | Exemplars for qualitative thresholds. Binary criteria only for quantitative. |
| Mode Weightings (Phase 3) | #6: Tables contradict modifiers | Derive tables FROM existing prose. Cross-reference before finalizing. |
| Cost Formula (Phase 3) | #9: Mode independence assumption | Verify empirically before documenting. |
| Session Cleanup (Phase 2) | #7: Delete re-run data | --dry-run default. --older-than filter. Never auto-delete. |
| Test Scenarios (Phase 4) | #8: Testing structure not behavior | Outcome-based expectations. Test negative cases explicitly. |

## Integration Risk Matrix

| If You Fix... | Watch Out For... | Why |
|---------------|------------------|-----|
| CEO refactor (#1) | CSO timeout (#3) | Timeout handling is CEO-owned orchestration logic. Refactoring changes where it lives. |
| CEO refactor (#1) | Mode mapping (#6) | Mode prompt modifiers embedded in CEO.md may move, changing attention distribution. |
| Pre-flight (#2) | Session cleanup (#8) | If pre-flight checks session directory state and cleanup modifies it, re-runs may be blocked. |
| Executive summaries (#4) | Mode sensitivity (#11) | If summaries lose nuance, mode sensitivity tests show false "Low" because modes see flattened input. |
| Routing trees (#5) | Tier 2 routing test (#9) | Over-formalized thresholds cause tests to check tree compliance rather than routing quality. |
| Cost formula (#7) | CEO refactor (#1) | If refactor changes how modes are communicated in Phase 0, mode-independence assumption changes. |

## Sources

- `agents/ceo.md` -- CEO agent structure analysis (682 lines, direct reading)
- `config/routing-table.md` -- Current routing specification (direct reading)
- `config/decision-modes.md` -- Current mode specification (direct reading)
- `agents/c-suite/*.md` -- All 8 C-suite agent output formats (direct reading)
- `.planning/RETROSPECTIVE.md` -- v1.0 lessons learned (direct reading)
- `.planning/milestones/v1.0-MILESTONE-AUDIT.md` -- v1.0 audit findings (direct reading)
