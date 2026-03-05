# Phase 7: Specification Formalization - Research

**Researched:** 2026-03-05
**Domain:** Markdown specification design (structured decision trees, weighting tables, cost formulas)
**Confidence:** HIGH

## Summary

Phase 7 is a pure specification-formalization phase. All six requirements (SPEC-01 through SPEC-06) involve converting existing prose descriptions into structured, auditable specification formats within markdown files. No code changes, no library installations, no Python modifications. Every change is a markdown edit to existing config documents (`config/routing-table.md`, `config/decision-modes.md`) and the orchestration protocol (`config/orchestration-protocol.md`).

The current state has three specification gaps: (1) the five routing threshold conditions in `config/routing-table.md` are described as one-sentence prose summaries without diagnostic questions, YES/NO criteria, or calibration exemplars; (2) the five decision modes in `config/decision-modes.md` describe weighting patterns in narrative prose ("Weights skeptic roles more heavily") but lack explicit directional weighting tables mapping each C-suite perspective to a HIGH/MODERATE/LOW influence level; (3) the multi-mode cost formula is described as "approximately 1.1x a single deliberation" without the actual calculation or worked examples. The orchestration protocol's Phase 1 Step 4 instructs the CEO to "state threshold assessment explicitly" but does not require structured per-condition evaluation in a prescribed format.

**Primary recommendation:** Execute as three distinct specification tasks -- (1) routing threshold decision trees with exemplars in routing-table.md, (2) directional weighting tables in decision-modes.md, (3) multi-mode cost formula with worked examples in decision-modes.md -- plus a fourth task updating orchestration-protocol.md Phase 1 output format and the CEO Decision Record template for auditable threshold evaluation.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SPEC-01 | Each of the 5 routing threshold conditions has structured diagnostic questions with YES/NO evaluation criteria | Current `config/routing-table.md` has 5 one-sentence threshold descriptions (lines 20-24). Each needs expansion into a decision tree with 2-3 diagnostic questions, each with YES/NO binary criteria. Section-by-section analysis below identifies the diagnostic dimensions for each threshold. |
| SPEC-02 | Routing thresholds include calibration exemplars (concrete decision examples showing how each threshold evaluates) | No exemplars currently exist. Each threshold needs 2-3 concrete business scenarios (1 YES, 1 NO, optionally 1 borderline) showing how the diagnostic questions evaluate against real decisions. Exemplar design guidance below. |
| SPEC-03 | CEO explicitly evaluates each threshold in Phase 1 framing output, making routing auditable | Current orchestration protocol Step 4 (line 90) says "State threshold assessment explicitly" but the output format in Step 5 (line 98) allows a summary ("which conditions assessed, which triggered"). The Decision Record template in CEO.md (line 120) has the same summary format. Both need structured per-condition evaluation format. **Critical constraint:** CEO.md is at 348/350 lines -- changes to the Decision Record template must be minimal (expand template placeholder, not add new sections). The heavy lifting goes in `config/orchestration-protocol.md` Step 4/5. |
| SPEC-04 | Each of the 5 decision modes has an explicit directional weighting table (HIGH/MODERATE/LOW per perspective) | Current `config/decision-modes.md` uses prose patterns like "Weights skeptic roles (CISO, CFO, COO, VP Delivery) more heavily" and "Weights advocate roles (VP Sales, CTO) more heavily." Needs a structured table per mode mapping all 8 C-suite perspectives to HIGH/MODERATE/LOW directional influence. **Critical constraint:** REQUIREMENTS.md Out of Scope explicitly prohibits numeric weights (1.5x, 0.7x) -- directional indicators only. |
| SPEC-05 | Multi-mode cost formula is documented with actual calculation: (1 x Domain Analysis) + (N x CEO Synthesis) | Current description: "Approximately 1.1x a single deliberation for 5x the strategic insight." Needs the actual formula breaking down which phases run once vs. N times, and what "1.1x" means in terms of agent invocations. |
| SPEC-06 | Multi-mode documentation includes example cost calculations for typical panel sizes | No worked examples currently exist. Needs concrete calculations for common scenarios: 2-mode comparison, 5-mode (all-modes) comparison, with varying panel sizes. |
</phase_requirements>

## Standard Stack

This phase involves no software dependencies. All changes are to markdown specification files.

### Core
| File Type | Location | Purpose | Why Standard |
|-----------|----------|---------|--------------|
| Config documents | `config/*.md` | Referenced configuration and protocol specs | Established project pattern -- routing-table.md, decision-modes.md, orchestration-protocol.md already exist |
| Agent definition | `agents/ceo.md` | CEO Decision Record output template | Minimal template adjustment only (348/350 lines) |

### Supporting
| File | Purpose | When Modified |
|------|---------|---------------|
| `config/orchestration-protocol.md` | Phase 1 framing output format | Updated to require structured per-condition threshold evaluation |
| `agents/ceo.md` | Decision Record template | Minor template expansion for threshold evaluation format |

### Alternatives Considered
None -- all requirements specify exactly what format to use (decision trees, weighting tables, cost formulas). No design alternatives to evaluate.

## Architecture Patterns

### Current File Structure and Change Locations

```
config/
  routing-table.md         # SPEC-01, SPEC-02: Add decision trees + exemplars (currently 41 lines)
  decision-modes.md        # SPEC-04, SPEC-05, SPEC-06: Add weighting tables + cost formula (currently 106 lines)
  orchestration-protocol.md # SPEC-03: Update Phase 1 output format (currently 312 lines)
agents/
  ceo.md                   # SPEC-03: Minor Decision Record template update (currently 348/350 lines)
```

### Pattern 1: Structured Decision Tree for Threshold Conditions

**What:** Each of the 5 routing threshold conditions gets expanded from a one-sentence description into a decision tree with diagnostic questions and YES/NO criteria.

**Current state (example -- Irreversibility threshold):**
```markdown
1. **Irreversibility** -- The decision is practically irreversible (e.g., acquisition, divestiture, platform decommission)
```

**Target state:**
```markdown
### 1. Irreversibility

**Core question:** Can this decision be meaningfully reversed within 12 months at acceptable cost?

| Diagnostic Question | YES triggers full activation | NO does not trigger |
|---------------------|---------------------------|---------------------|
| Does reversal require rebuilding destroyed capabilities (teams, infrastructure, relationships)? | YES -- irreversible | NO -- may be reversible |
| Does reversal require regulatory re-approval or re-licensing? | YES -- irreversible | NO -- may be reversible |
| Would reversal cost more than 50% of the original decision's cost? | YES -- effectively irreversible | NO -- reversible at cost |

**If ANY diagnostic question answers YES:** Threshold triggered -- full activation.

**Calibration Exemplars:**
- **YES (triggers):** "Divest our healthcare division" -- capabilities destroyed, client relationships severed, regulatory licenses surrendered. Cannot rebuild in under 3 years.
- **NO (does not trigger):** "Switch project management tools from Jira to Linear" -- data exportable, workflows adjustable, revert within weeks.
- **Borderline:** "Commit to 3-year cloud vendor contract with early termination fee" -- technically reversible but financially painful. Evaluate via cost-of-reversal diagnostic.
```

**When to use:** All 5 threshold conditions (Irreversibility, Headcount Impact, Market Position Change, Existential Financial Risk, Domain Uncertainty).

### Pattern 2: Directional Weighting Table for Decision Modes

**What:** Each mode gets a structured table mapping all 8 C-suite perspectives to directional influence levels.

**Current state (example -- Guardian mode):**
```markdown
**Resolution Pattern:** Weights skeptic roles (CISO, CFO, COO, VP Delivery) more heavily.
```

**Target state:**
```markdown
### Guardian -- Directional Weighting

| C-Suite Role | Disposition | Influence Level | Rationale |
|-------------|-------------|-----------------|-----------|
| CISO | Skeptic | HIGH | Primary risk identifier; must be satisfied |
| CFO | Skeptic | HIGH | Financial exposure must be addressed |
| COO | Skeptic | HIGH | Operational feasibility is gating |
| VP Delivery | Skeptic | HIGH | Current obligation impact is non-negotiable |
| CAO | Systemic | MODERATE | Organizational absorption matters but does not gate |
| CSO | Investigative | MODERATE | Evidence informs but does not drive Guardian decisions |
| CTO | Advocate | LOW | Technical opportunity is secondary to risk mitigation |
| VP Sales | Advocate | LOW | Revenue opportunity does not override risk concerns |
```

**Critical constraint:** These are directional indicators, NOT numeric multipliers. REQUIREMENTS.md Out of Scope explicitly states: "Numeric mode weights (1.5x, 0.7x) -- LLMs cannot reliably apply numeric multipliers. Directional indicators (HIGH/MODERATE/LOW) are appropriate."

**When to use:** All 5 decision modes (Guardian, Pioneer, Architect, Analyst, Sentinel).

### Pattern 3: Multi-Mode Cost Formula with Worked Examples

**What:** Replace the "approximately 1.1x" claim with the actual formula showing agent invocations.

**Target state:**
```markdown
## Multi-Mode Cost Formula

**Formula:** Total Cost = (1 x Full Domain Analysis) + (N x CEO Synthesis Pass)

Where:
- **Full Domain Analysis** = Phase 0 broadcast + Phase 1 framing + Phase 1.5 research (if CSO activated) + Phase 2 C-suite dispatch + Phase 3 team lead analysis + Phase 4 C-suite synthesis + Phase 4.5 pre-mortem (Tier 3 only)
- **CEO Synthesis Pass** = Phase 5 only (CEO reads recommendations and produces Decision Record with one mode's prompt modifier)
- **N** = number of modes requested (1 for single mode, 2 for comparison, 5 for all-modes)

### Why ~1.1x for 5 Modes

The domain analysis (Phases 0-4/4.5) is the expensive part: it involves spawning and executing K C-suite agents, each spawning 3-5 team lead subagents (up to 29 total for full activation). The CEO synthesis pass (Phase 5) is a single agent producing a single document from already-collected inputs -- no subagent spawning, no new analysis.

For a Tier 3 full-activation panel:
- Domain analysis: 1 CEO + 8 C-suite + up to 29 team leads = ~38 agent invocations
- Each additional CEO synthesis pass: 1 agent invocation

Cost ratio for 5 modes: (38 + 5) / (38 + 1) = 43/39 = ~1.10x

### Worked Examples

**Example 1: Two-mode comparison (Guardian vs Pioneer), Tier 3, full activation**
- Domain analysis (once): 1 + 8 + 29 = 38 agent invocations
- CEO synthesis (2x): 2 invocations
- Total: 40 invocations vs. 39 for single-mode = 1.03x cost
...
```

### Pattern 4: Structured Per-Condition Threshold Evaluation (SPEC-03)

**What:** Update the orchestration protocol's Phase 1 output format to require structured per-condition evaluation, and update the Decision Record template to match.

**Current Phase 1 Step 5 output format:**
```markdown
- **Threshold Conditions:** Which of the five full-activation conditions were assessed and their status (triggered / not triggered)
```

**Target Phase 1 Step 5 output format:**
```markdown
- **Threshold Assessment:**
  1. Irreversibility: [TRIGGERED/NOT TRIGGERED] -- [one-sentence reasoning]
  2. Headcount Impact: [TRIGGERED/NOT TRIGGERED] -- [one-sentence reasoning]
  3. Market Position Change: [TRIGGERED/NOT TRIGGERED] -- [one-sentence reasoning]
  4. Existential Financial Risk: [TRIGGERED/NOT TRIGGERED] -- [one-sentence reasoning]
  5. Domain Uncertainty: [TRIGGERED/NOT TRIGGERED] -- [one-sentence reasoning]
  Full activation: [YES (conditions X,Y triggered) / NO]
```

**CEO Decision Record template change (SPEC-03):** The existing `Threshold Conditions: [which conditions assessed, which triggered]` line in the CEO.md Decision Record template (line 120) should be expanded to reference the structured format. Since CEO.md is at 348/350 lines, this must be a minimal edit -- expanding the placeholder text within the existing template line, not adding new sections.

### Anti-Patterns to Avoid

- **Numeric weights in weighting tables:** OUT OF SCOPE per REQUIREMENTS.md. Do NOT use 1.5x, 0.7x, or any numeric multiplier. Use HIGH/MODERATE/LOW only.
- **Duplicating content between files:** routing-table.md owns threshold decision trees; orchestration-protocol.md references them. decision-modes.md owns weighting tables; CEO.md references decision-modes.md via config references. No content duplication.
- **Adding content to CEO.md:** The agent is at 348/350 lines. Any change to CEO.md must be net-zero or near-zero lines. The Decision Record template placeholder text can be adjusted but no new sections added.
- **Mode-specific C-suite behavior:** OUT OF SCOPE per REQUIREMENTS.md. Weighting tables describe how the CEO synthesizes, not how C-suite agents behave. "Mode-specific C-suite behavior violates core design principle: domain analysis is mode-independent."

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Decision tree format | Custom flowchart notation | Simple table-based YES/NO diagnostic questions | Tables are readable by both humans and LLMs; flowcharts in markdown are awkward |
| Weighting visualization | ASCII art or diagram | Structured table with HIGH/MODERATE/LOW | Tables are the established pattern in this project (Mode/Tier Interaction Matrix, routing table) |
| Cost calculation | Complex formula with variables | Simple arithmetic with concrete numbers | LLMs handle concrete arithmetic better than abstract formula manipulation |

**Key insight:** The project operates entirely through markdown specifications consumed by LLM agents. Structured tables are the most reliable format for LLM consumption -- they are unambiguous, scannable, and pattern-matchable.

## Common Pitfalls

### Pitfall 1: CEO Line Budget Exhaustion
**What goes wrong:** Adding structured threshold evaluation format to CEO.md pushes it over 350 lines.
**Why it happens:** The Decision Record template is in CEO.md, and SPEC-03 requires expanding the threshold assessment output.
**How to avoid:** Keep changes to CEO.md at net-zero lines. Expand the existing placeholder text in the `Threshold Conditions` line to reference the structured format, but do not add new lines. The detailed format specification belongs in `config/orchestration-protocol.md` Phase 1 Step 4/5, not in the CEO agent.
**Warning signs:** Any edit to CEO.md that adds even 3 lines will breach the 350-line cap.

### Pitfall 2: Confusing Directional Weighting with Behavioral Prescription
**What goes wrong:** Weighting tables get interpreted as instructions for C-suite agents to behave differently per mode.
**Why it happens:** Natural tendency to extend "CEO weights CISO as HIGH in Guardian mode" into "CISO should be more thorough in Guardian mode."
**How to avoid:** Weighting tables must explicitly state they describe CEO synthesis behavior, not C-suite agent behavior. Domain analysis is mode-independent (core design principle, stated in REQUIREMENTS.md Out of Scope).
**Warning signs:** Any language in weighting tables that addresses C-suite agent behavior rather than CEO synthesis weighting.

### Pitfall 3: Over-Specifying Calibration Exemplars
**What goes wrong:** Exemplars become so specific they narrow the threshold's applicability, or so generic they add no diagnostic value.
**Why it happens:** Tension between "concrete enough to calibrate" and "abstract enough to generalize."
**How to avoid:** Each exemplar should name a specific decision type (e.g., "Divest our healthcare division") but focus on why the threshold applies or does not apply. Include one clear YES, one clear NO, and optionally one borderline case that illustrates the judgment involved.
**Warning signs:** Exemplars that are all from one industry, all the same scale, or all unambiguous (borderline cases are the most calibrating).

### Pitfall 4: Multi-Mode Cost Formula Becoming Stale
**What goes wrong:** The formula references a specific number of team leads or agent count that could change in future versions.
**Why it happens:** Hard-coding "29 team leads" or "8 C-suite" in the formula.
**How to avoid:** Express the formula generically (K C-suite agents, L team leads total) and then provide worked examples with current numbers. The formula stays correct even if the roster changes; only the examples would need updating.
**Warning signs:** Formula that only works for the current roster size.

### Pitfall 5: Duplicating Threshold Content Across Files
**What goes wrong:** Threshold decision trees appear in both routing-table.md AND orchestration-protocol.md, creating a maintenance burden and risk of drift.
**Why it happens:** Orchestration protocol Phase 1 Step 4 currently lists the 5 thresholds inline.
**How to avoid:** After adding decision trees to routing-table.md (which is the authoritative source), update orchestration-protocol.md Phase 1 Step 4 to reference routing-table.md for the structured decision trees rather than repeating them. The orchestration protocol can keep the list of 5 condition names but should point to routing-table.md for the detailed diagnostic questions and exemplars.
**Warning signs:** The same diagnostic questions appearing in two files.

## Code Examples

All examples are markdown specification patterns, not code.

### Diagnostic Question Table Format
```markdown
| Diagnostic Question | YES (triggers) | NO (does not trigger) |
|---------------------|----------------|----------------------|
| [Concrete, binary question about the decision] | [Why YES means this threshold is met] | [Why NO means threshold is not met] |
```

### Directional Weighting Table Format
```markdown
| C-Suite Role | Disposition | Influence Level | Rationale |
|-------------|-------------|-----------------|-----------|
| [Role] | [Skeptic/Advocate/Systemic/Investigative] | [HIGH/MODERATE/LOW] | [One sentence explaining why this level for this mode] |
```

### Per-Condition Threshold Evaluation Output Format
```markdown
THRESHOLD ASSESSMENT:
  1. Irreversibility: [TRIGGERED/NOT TRIGGERED] -- [reasoning]
  2. Headcount Impact: [TRIGGERED/NOT TRIGGERED] -- [reasoning]
  3. Market Position Change: [TRIGGERED/NOT TRIGGERED] -- [reasoning]
  4. Existential Financial Risk: [TRIGGERED/NOT TRIGGERED] -- [reasoning]
  5. Domain Uncertainty: [TRIGGERED/NOT TRIGGERED] -- [reasoning]
  Full activation triggered: [YES (conditions N triggered) / NO]
```

### Cost Formula Worked Example Format
```markdown
**Scenario:** [description -- tier, mode count, activation level]
- Domain analysis (once): [breakdown] = [N] agent invocations
- CEO synthesis ([M]x): [M] invocations
- Total: [N+M] invocations vs. [N+1] for single-mode = [ratio]x cost
```

## State of the Art

| Current State | Target State | Impact |
|---------------|-------------|--------|
| Threshold conditions as one-sentence prose with parenthetical examples | Structured decision trees with diagnostic YES/NO questions and calibration exemplars | Makes routing auditable; CEO can evaluate each condition systematically |
| Decision mode weighting as narrative description ("Weights skeptics heavily") | Directional weighting tables (HIGH/MODERATE/LOW per perspective) | Makes synthesis weighting explicit and consistent across uses |
| Multi-mode cost as "~1.1x" approximation | Actual formula with agent invocation breakdown and worked examples | Users and developers understand the real cost model |
| CEO Phase 1 output says "state threshold assessment explicitly" without format | Structured per-condition evaluation with TRIGGERED/NOT TRIGGERED per threshold | Threshold evaluation becomes auditable and consistent |

**Key observations:**
- All current content is correct -- it just needs to be restructured from prose into tables/trees
- No content is being changed, only its format and completeness
- The structured formats align with existing project patterns (tables are used extensively in routing-table.md, decision-modes.md Mode/Tier matrix, orchestration protocol)

## Open Questions

1. **Analyst and Architect weighting tables are less role-aligned than other modes**
   - What we know: Guardian clearly weights skeptics HIGH, Pioneer clearly weights advocates HIGH. But Analyst weights by confidence level (any role) and Architect weights by consensus across domains (all roles).
   - What's unclear: How to represent "weights by confidence, not role" in a per-role HIGH/MODERATE/LOW table.
   - Recommendation: For Analyst, all roles should be MODERATE with a note that effective weight is driven by each role's confidence level in their specific recommendation, not their disposition. For Architect, all roles should be MODERATE with a note that weight is driven by which positions command the most cross-domain support.

2. **Should orchestration-protocol.md Phase 1 Step 4 still list the 5 thresholds inline after routing-table.md is expanded?**
   - What we know: Currently the 5 thresholds are listed in both routing-table.md and orchestration-protocol.md (lines 83-89). After expansion, routing-table.md will be the authoritative source with full decision trees.
   - What's unclear: Whether to keep the inline list in orchestration-protocol.md (for quick reference) or replace it with a pointer to routing-table.md.
   - Recommendation: Keep the 5 threshold names inline in orchestration-protocol.md for quick reference (the CEO needs to know which conditions to evaluate) but replace the one-sentence descriptions with a reference to routing-table.md for the structured decision trees. This avoids duplication while keeping the orchestration protocol self-contained enough to follow.

3. **CSO row in weighting tables**
   - What we know: CSO is Investigative disposition, produces evidence not positions. Its weighting varies by mode.
   - What's unclear: Whether CSO's influence level in synthesis is about its evidence weight or its position weight (since it now produces executive summaries with Position field per Phase 5 changes).
   - Recommendation: CSO influence level represents how much the CEO weighs CSO evidence in resolving fault lines, not whether the CSO "votes." This should be noted in the table.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x |
| Config file | `pytest.ini` |
| Quick run command | `pytest tests/ -x -m "not live"` |
| Full suite command | `pytest tests/ -m "not live"` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SPEC-01 | Each threshold has structured diagnostic questions with YES/NO criteria | manual-only | N/A -- verify structured table format in routing-table.md | N/A |
| SPEC-02 | Each threshold has calibration exemplars | manual-only | N/A -- verify exemplars present per threshold in routing-table.md | N/A |
| SPEC-03 | CEO Phase 1 framing evaluates each threshold explicitly | manual-only | N/A -- verify orchestration-protocol.md Step 4/5 format and CEO.md template | N/A |
| SPEC-04 | Each mode has directional weighting table | manual-only | N/A -- verify 5 weighting tables in decision-modes.md | N/A |
| SPEC-05 | Multi-mode cost formula documented with calculation | manual-only | N/A -- verify formula section in decision-modes.md | N/A |
| SPEC-06 | Multi-mode cost includes worked examples | manual-only | N/A -- verify worked examples in decision-modes.md | N/A |

### Sampling Rate
- **Per task commit:** Visual diff review of modified markdown files; verify structure matches prescribed formats
- **Per wave merge:** Verify all 5 threshold decision trees + all 5 weighting tables + cost formula with examples present
- **Phase gate:** All 6 SPEC requirements verified via content inspection before `/gsd:verify-work`

### Wave 0 Gaps
None -- existing test infrastructure covers all phase requirements. This phase modifies markdown specification files, not Python code. Validation is structural (content format, section presence, line counts) rather than behavioral. Project explicitly excludes automated agent testing (REQUIREMENTS.md Out of Scope).

**Justification for manual-only:** All SPEC requirements are about markdown specification content and structure. There is no code behavior to test. The project explicitly excludes automated agent testing ("LLM outputs are non-deterministic; false precision"). Validation consists of reading the modified files and confirming they contain the prescribed structured formats.

## Detailed File Analysis

### config/routing-table.md (41 lines -- SPEC-01, SPEC-02 target)

**Current content:**
- Lines 1-14: Default Activation by Decision Type table (6 decision types)
- Lines 16-26: Full-Activation Threshold Conditions (5 conditions as one-sentence descriptions)
- Lines 28-41: CSO Research Activation table

**What needs to change:**
- Lines 16-26 (threshold conditions section) must be expanded significantly. Each of the 5 conditions needs:
  - A core diagnostic question (one sentence)
  - A diagnostic questions table (2-3 rows with YES/NO evaluation criteria)
  - A "trigger rule" statement (any YES = triggered)
  - 2-3 calibration exemplars (concrete decision examples)
- The default activation table (lines 1-14) and CSO activation table (lines 28-41) stay unchanged.
- Estimated final size: ~180-220 lines (from 41)

### config/decision-modes.md (106 lines -- SPEC-04, SPEC-05, SPEC-06 target)

**Current content:**
- Lines 1-8: Overview
- Lines 9-65: Five modes (each with Disposition, Decision Theory, Resolution Pattern, CEO Prompt Modifier)
- Lines 66-78: Mode/Tier Interaction Matrix
- Lines 80-93: Multi-Mode Comparison overview
- Lines 95-106: CEO Mode Recommendation table

**What needs to change:**
- Each of the 5 mode sections (lines 9-65) gets an additional directional weighting table appended after the existing CEO Prompt Modifier
- The Multi-Mode Comparison section (lines 80-93) gets expanded with:
  - Actual cost formula breakdown
  - "Why ~1.1x" explanation with agent invocation math
  - 3-4 worked examples for different scenarios
- The existing content (Disposition, Decision Theory, Resolution Pattern, CEO Prompt Modifier, Mode/Tier Matrix, Mode Recommendation) stays unchanged.
- Estimated final size: ~250-300 lines (from 106)

### config/orchestration-protocol.md (312 lines -- SPEC-03 target)

**Current content of interest:**
- Lines 80-90: Phase 1 Step 4 (Assess Full-Activation Threshold Conditions) -- lists 5 conditions inline with one-sentence descriptions
- Lines 92-100: Phase 1 Step 5 (State Activation and Exclusion Reasoning) -- output format includes `Threshold Conditions` as a summary line

**What needs to change:**
- Step 4 (lines 80-90): Replace inline one-sentence descriptions with condition names + reference to routing-table.md for structured decision trees. Add instruction to evaluate each condition explicitly using the diagnostic questions.
- Step 5 (lines 92-100): Replace the `Threshold Conditions` summary format with a structured per-condition evaluation format (TRIGGERED/NOT TRIGGERED per condition with one-sentence reasoning).
- Estimated net line change: +10-15 lines (from 312 to ~325)

### agents/ceo.md (348 lines -- minimal SPEC-03 adjustment)

**Current content of interest:**
- Line 120: `Threshold Conditions: [which conditions assessed, which triggered]` in the Decision Record template

**What needs to change:**
- Line 120: Expand the placeholder to reference the structured per-condition format. For example: `Threshold Assessment: [per-condition TRIGGERED/NOT TRIGGERED with reasoning, per config/orchestration-protocol.md Step 5]`
- This is a same-line text replacement -- zero net new lines. The CEO agent stays at 348 lines.

## Weighting Table Design Guidance

This section provides the recommended weighting tables for all 5 modes based on analysis of the existing Resolution Pattern descriptions and CEO Prompt Modifiers.

### Guardian (MaxiMin)
Skeptics HIGH, Systemic/Investigative MODERATE, Advocates LOW. The mode's core principle is "skeptics must be satisfied, not just acknowledged."

### Pioneer (MaxiMax)
Advocates HIGH, Systemic/Investigative MODERATE, Skeptics LOW. The mode's core principle is "skeptic concerns are engineering problems to solve, not reasons to stop."

### Architect (Behavioral)
All roles MODERATE with special note: influence is driven by how many cross-domain concerns each perspective addresses, not by role disposition. The mode's core principle is "the position that satisfies the most domain concerns."

### Analyst (Hurwicz)
All roles MODERATE with special note: effective influence is driven by confidence level in the domain recommendation, not by role disposition. HIGH-confidence findings from any role outweigh LOW-confidence findings from any other role. The mode's core principle is "weight by evidence quality."

### Sentinel (MiniMax Regret)
All roles MODERATE with special note: the single strongest objection from ANY role receives disproportionate weight regardless of that role's disposition. The mode's core principle is "which warning would I most regret ignoring?"

**Design rationale for Architect, Analyst, and Sentinel:** These three modes weight by criteria (consensus support, confidence level, strongest objection) rather than by role disposition. Using a uniform MODERATE base with a qualifying note is more honest than artificially assigning different levels per role, because the actual influence of any given role depends on the specific decision's analysis, not on a static table. The qualifying note is what makes the table useful rather than misleading.

## Sources

### Primary (HIGH confidence)
- `config/routing-table.md` -- Current threshold conditions (41 lines), read in full
- `config/decision-modes.md` -- Current mode descriptions and weighting patterns (106 lines), read in full
- `config/orchestration-protocol.md` -- Current Phase 1 format and threshold assessment instructions (312 lines), read in full
- `agents/ceo.md` -- Current Decision Record template and line count constraint (348/350 lines), read in full
- `.planning/REQUIREMENTS.md` -- Out of Scope items ("Numeric mode weights... Directional indicators are appropriate"), read in full
- `.planning/phases/05-ceo-architecture/05-01-SUMMARY.md` and `05-02-SUMMARY.md` -- Phase 5 outcomes confirming current file state

### Secondary (MEDIUM confidence)
- `.planning/phases/05-ceo-architecture/05-RESEARCH.md` -- Architecture patterns and extraction decisions from Phase 5
- `.planning/phases/06-orchestration-hardening/06-RESEARCH.md` -- Phase 6 patterns for markdown specification editing

### Tertiary (LOW confidence)
None -- all findings are based on direct inspection of the project files.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all files directly inspected, no libraries involved
- Architecture: HIGH -- patterns derived from existing project conventions (table formats, cross-references, file structure)
- Pitfalls: HIGH -- constraints (CEO 350-line cap, no numeric weights, no mode-specific C-suite behavior) are explicitly documented in project requirements and summaries
- Weighting table design: MEDIUM -- the Architect/Analyst/Sentinel "all MODERATE with qualifying note" approach is a design recommendation, not a verified pattern; planner should validate this against the mode descriptions

**Research date:** 2026-03-05
**Valid until:** 2026-04-05 (stable -- markdown specification design, no version sensitivity)
