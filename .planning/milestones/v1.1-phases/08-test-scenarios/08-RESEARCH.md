# Phase 8: Test Scenarios - Research

**Researched:** 2026-03-05
**Domain:** Specification-level test scenarios for LLM agent orchestration (routing, pre-mortem, mode sensitivity)
**Confidence:** HIGH

## Summary

Phase 8 creates specification-level test scenarios that validate the formalized specifications from Phase 7. These are NOT automated pytest tests -- the project explicitly excludes automated agent testing ("LLM outputs are non-deterministic; false precision. Use specification-level test scenarios instead." -- REQUIREMENTS.md Out of Scope). Instead, these are structured markdown scenario documents that define concrete decision inputs, expected system behavior at each phase, and verifiable behavioral assertions. They serve as specification validation artifacts: a human (or future evaluator) can walk through the scenario and confirm the system specifications produce the correct routing, activation, pre-mortem handling, and mode sensitivity behaviors.

The four TEST requirements address three distinct specification domains: (1) Tier 2 partial activation routing (TEST-01), (2) Pre-Mortem resilience under degraded input (TEST-02), and (3) Mode sensitivity criteria definition and consistency (TEST-03, TEST-04). Each requires a different type of scenario structure. TEST-01 and TEST-02 are behavioral test scenarios with specific inputs and expected outputs. TEST-03 is a specification extension (defining quantitative thresholds that do not yet exist in the comparative-decision-record.md template). TEST-04 uses paired scenarios to demonstrate consistency.

A key discovery during research: there is a specification ambiguity between the orchestration protocol's full-activation threshold override ("if ANY condition applies, ALL C-suite members activate") and Tier 2's explicit constraint to user-specified roles. The TEST-01 scenario must resolve this ambiguity by asserting that user selection takes precedence at Tier 2, with the CEO noting triggered thresholds and recommending escalation rather than silently overriding the user's role selection.

**Primary recommendation:** Create test scenarios as structured markdown documents in a new `test-scenarios/` directory at the project root. Each scenario defines: the decision input, the invocation command, the expected behavior at each relevant orchestration phase, and the behavioral assertions that must hold. TEST-03 extends `templates/comparative-decision-record.md` with quantitative divergence thresholds. All four requirements can be addressed in 2-3 plans.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| TEST-01 | Test scenario validates Tier 2 partial activation correctly excludes non-requested C-suite agents even when full-activation thresholds are met | Specification ambiguity identified between orchestration-protocol.md full-activation override and Tier 2 user-specified role constraint. Scenario must define a decision where thresholds trigger but user selects only 2-3 roles. Expected behavior: user selection honored, CEO notes triggered thresholds, recommends Tier 3 escalation. Requires both scenario document and specification clarification in orchestration-protocol.md or panel-assessment.md. |
| TEST-02 | Test scenario validates Phase 4.5 Pre-Mortem executes correctly when one or more C-suite agents have missing or partial recommendations | Phase 4.5 protocol (orchestration-protocol.md lines 191-211) distributes "summaries of ALL other activated C-suite members' recommendations" and collects pre-mortem responses. Scenario must define: what constitutes "missing" (agent never responded) vs "partial" (incomplete fields) recommendation, how the pre-mortem broadcast handles gaps, and what the CEO's fault-line analysis looks like with incomplete input. |
| TEST-03 | Mode sensitivity criteria defines quantitative thresholds for LOW/MEDIUM/HIGH divergence ratings | Current definition in comparative-decision-record.md (lines 26-31, 262-278) is qualitative only. Divergence Classification Guide defines directional (HIGH), conditional (MEDIUM), and convergence (LOW) but without quantitative measures. Need to define measurable criteria: what specific patterns of mode outputs map to each sensitivity level. Quantitative dimensions include: decision direction divergence count, condition/guardrail variance, and determinative-perspective variance. |
| TEST-04 | Test scenario validates mode sensitivity ratings are consistent across similar decision types | Requires paired scenarios with similar characteristics (e.g., two irreversible strategic decisions) that should produce the same sensitivity level. Demonstrates that sensitivity rating is driven by decision characteristics, not arbitrary per-run variation. |
</phase_requirements>

## Standard Stack

This phase involves no software dependencies. All deliverables are markdown specification and scenario files.

### Core
| File Type | Location | Purpose | Why Standard |
|-----------|----------|---------|--------------|
| Test scenario documents | `test-scenarios/*.md` | Structured validation scenarios with inputs, expected behavior, assertions | New directory -- these are the project's test coverage mechanism for non-deterministic LLM agents |
| Specification extension | `templates/comparative-decision-record.md` | Quantitative mode sensitivity criteria (TEST-03) | Extends existing template with measurable thresholds |

### Supporting
| File | Purpose | When Modified |
|------|---------|---------------|
| `config/orchestration-protocol.md` | Clarify full-activation vs. Tier 2 user-selection precedence (TEST-01) | Only if specification ambiguity needs resolving in the protocol itself |
| `templates/panel-assessment.md` | May need note about threshold-triggered escalation recommendation at Tier 2 | Only if the escalation behavior is formalized here |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Standalone test-scenarios/ directory | Inline scenarios within existing spec files | Separate directory keeps specs clean and makes scenarios independently reviewable; also establishes a pattern for future test scenario additions |
| Quantitative divergence counting | Qualitative-only sensitivity | REQUIREMENTS explicitly asks for "quantitative thresholds" so qualitative alone does not satisfy TEST-03 |

## Architecture Patterns

### Recommended Project Structure
```
test-scenarios/
  tier2-partial-activation.md       # TEST-01: Tier 2 excludes non-requested agents
  premortem-degraded-input.md       # TEST-02: Pre-Mortem with missing/partial recs
  mode-sensitivity-criteria.md      # TEST-03: Quantitative divergence thresholds (or in comparative-decision-record.md)
  mode-sensitivity-consistency.md   # TEST-04: Paired scenarios for consistency validation
```

### Pattern 1: Behavioral Test Scenario Document (TEST-01, TEST-02)

**What:** A structured markdown document that defines: (1) the decision scenario, (2) the exact invocation command, (3) the system state at each relevant orchestration phase, (4) behavioral assertions that must hold, and (5) failure modes (what would happen if the assertion were violated).

**When to use:** For TEST-01 and TEST-02, which validate specific orchestration behaviors.

**Template structure:**
```markdown
# Test Scenario: [Name]

**Requirement:** [TEST-XX]
**Validates:** [what specification behavior this tests]
**Specification References:**
- [file:line references to the specs being validated]

## Decision Scenario

**Issue:** [concrete business decision]
**Invocation:** [exact /cdp command]
**Decision Type:** [classification]
**Context:** [any relevant context that makes the scenario specific]

## Pre-Conditions

[System state that must exist before the test]

## Expected Behavior

### Phase 1: Frame and Route
[What the CEO should do -- step by step with expected outputs]

### Phase N: [Next relevant phase]
[Expected behavior]

## Behavioral Assertions

| # | Assertion | Why It Matters | Specification Reference |
|---|-----------|----------------|------------------------|
| 1 | [concrete, verifiable statement] | [what goes wrong if violated] | [file:line] |
| 2 | [concrete, verifiable statement] | [what goes wrong if violated] | [file:line] |

## Failure Modes

| Violation | What Would Happen | How to Detect |
|-----------|-------------------|---------------|
| [assertion violated] | [consequence] | [observable sign] |

## Expected Output Excerpt

[Relevant section of the expected Panel Assessment / Decision Record / Comparative Decision Record showing the correct behavior]
```

### Pattern 2: Specification Extension with Concrete Examples (TEST-03)

**What:** Extends the existing Divergence Classification Guide in `templates/comparative-decision-record.md` with quantitative criteria and concrete worked examples mapping decision patterns to sensitivity levels.

**When to use:** For TEST-03, which requires defining measurable thresholds rather than testing existing behavior.

**Design approach:**

The current qualitative definitions in comparative-decision-record.md are:
- **Directional Divergence (High):** Modes reach fundamentally different decisions -- some approve, some oppose, some defer.
- **Conditional Divergence (Medium):** Same directional decision but meaningfully different conditions, guardrails, or timelines.
- **Convergence (Low):** All modes reach essentially the same decision with similar conditions.

Quantitative thresholds should measure three dimensions:
1. **Decision Direction Divergence:** Count of distinct Decision values across modes (Approve/Approve with Conditions/Oppose/Defer)
2. **Determinative Perspective Variance:** How many different C-suite roles are cited as "Most Determinative Perspective" across modes
3. **Condition/Guardrail Variance:** Whether conditions are additive (same direction, more guardrails) or contradictory (different directions)

**Proposed quantitative criteria:**

```markdown
### Quantitative Sensitivity Criteria

| Dimension | LOW (Convergence) | MEDIUM (Conditional) | HIGH (Directional) |
|-----------|-------------------|---------------------|-------------------|
| Decision directions | 1 (all modes same) | 1-2 (same direction, ≤1 outlier defer) | 3+ distinct decisions, OR approve vs oppose split |
| Most determinative perspective | ≤2 distinct roles | 2-3 distinct roles | 4+ distinct roles cited |
| Conditions overlap | ≥80% shared conditions | 50-79% shared, remainder additive | <50% shared, OR contradictory conditions |
| Overall rule | ALL three dimensions LOW | ANY dimension MEDIUM, none HIGH | ANY dimension HIGH |
```

**Critical constraint:** These thresholds must be assessable by the CEO (an LLM agent) during synthesis. They cannot require computation the LLM cannot perform. The criteria must be pattern-matchable, not formula-driven. This is why the thresholds use simple counts and percentages rather than statistical measures.

### Pattern 3: Paired Consistency Scenarios (TEST-04)

**What:** Two decision scenarios with similar structural characteristics (same decision type, similar complexity, similar threshold profile) that should produce the same mode sensitivity level. Demonstrates that sensitivity is driven by decision characteristics, not arbitrary variation.

**When to use:** For TEST-04, which validates that sensitivity ratings are consistent across similar decisions.

**Design approach:**
- Pair 1: Two irreversible strategic decisions with strong advocate/skeptic tension (expected: HIGH sensitivity -- modes should diverge because risk appetite is the deciding factor)
- Pair 2: Two clear operational decisions with unambiguous evidence (expected: LOW sensitivity -- modes should converge because evidence speaks for itself)
- The pairs test opposite ends of the spectrum to demonstrate the criteria discriminate correctly

### Anti-Patterns to Avoid

- **Testing LLM output literally:** Test scenarios validate SPECIFICATION BEHAVIOR (routing rules, activation logic, template completeness), not exact LLM text output. The project explicitly excludes automated agent testing. Assertions should be about structural decisions (which agents activate, which phases execute, what sections appear in output), not about specific sentences or reasoning chains.
- **Over-specifying scenario details:** Scenarios should define enough context to unambiguously trigger specific specification behaviors, not so much that they become single-use. A good scenario is reusable for manual validation by anyone reading the spec.
- **Numeric precision in mode sensitivity:** LLMs cannot perform exact percentage calculations. The quantitative thresholds must use easily countable dimensions (number of distinct decisions, number of distinct determinative perspectives) rather than computed ratios. "Are conditions ≥80% shared" is assessable by an LLM through pattern matching; "compute the Jaccard similarity coefficient" is not.
- **Making test scenarios depend on specific company context:** Scenarios should be self-contained with embedded context, not dependent on a .cdp-context/company.md file that may or may not exist.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test scenario format | Custom framework or schema | Structured markdown with assertion tables | Consistent with project's markdown-specification-as-code approach; no tooling dependencies |
| Mode sensitivity measurement | Statistical divergence formulas | Countable pattern dimensions (decision directions, determinative perspectives) | LLMs assess these scenarios -- they cannot compute statistics but can count and compare |
| Consistency testing | Automated repeated-execution testing | Paired-scenario structural analysis | Non-deterministic LLM output makes automated repetition meaningless; structural pairing tests the specification, not the output |

**Key insight:** These test scenarios validate that the SPECIFICATIONS are complete, unambiguous, and internally consistent. They do NOT test that LLM agents produce correct output. The project's position is that "specification-level test scenarios" replace automated agent testing -- the scenarios are the test coverage mechanism.

## Common Pitfalls

### Pitfall 1: Confusing Specification Testing with Agent Testing
**What goes wrong:** Scenarios try to assert exact LLM output text, which is non-deterministic and varies per run.
**Why it happens:** Natural tendency to write "expected output" as literal text rather than structural assertions.
**How to avoid:** Every assertion must be structural: "CEO activates only CFO and CTO" not "CEO says 'I am activating the CFO because...'". Assertions check which phases execute, which agents activate, which template sections appear, and what routing decisions are made.
**Warning signs:** Any assertion that quotes expected natural language text from the LLM.

### Pitfall 2: Not Resolving the Tier 2 / Full-Activation Ambiguity
**What goes wrong:** TEST-01 scenario assumes a behavior that the specs do not clearly define, making the "test" meaningless because there is no authoritative answer.
**Why it happens:** The orchestration protocol says "if ANY condition applies, ALL C-suite activate" without scoping this to Tier 3 only. Tier 2 says "route to 2-4 C-suite members" from user specification. The interaction is undefined.
**How to avoid:** The test scenario MUST be paired with a specification clarification. Either: (a) amend orchestration-protocol.md to scope full-activation thresholds to Tier 3 only, or (b) add explicit Tier 2 precedence language stating that user-specified roles take precedence and the CEO notes triggered thresholds as an escalation recommendation. Option (b) is recommended because it preserves the threshold evaluation (useful diagnostic) while respecting user intent.
**Warning signs:** Writing a test scenario without verifying that the spec it references is unambiguous.

### Pitfall 3: Mode Sensitivity Criteria Too Complex for LLM Assessment
**What goes wrong:** Quantitative thresholds require computation that LLMs perform unreliably (e.g., percentage calculations, weighted scores).
**Why it happens:** Natural tendency to make criteria "more rigorous" by adding mathematical precision.
**How to avoid:** All quantitative criteria must be assessable by counting: "How many distinct decision directions?" (count unique values in the Decision field), "How many different Most Determinative Perspectives?" (count unique roles), "Do all modes share the same conditions?" (yes/no pattern match). No computed ratios, no weighted formulas.
**Warning signs:** Any threshold definition that requires arithmetic beyond counting.

### Pitfall 4: Pre-Mortem Scenario Without Defining "Missing" vs "Partial"
**What goes wrong:** TEST-02 scenario says "missing or partial recommendations" but never defines what constitutes each, making the expected behavior ambiguous.
**Why it happens:** The orchestration protocol defines the pre-mortem input as "summaries of ALL other activated C-suite members' recommendations" but does not address what happens when some recommendations are incomplete.
**How to avoid:** The scenario must explicitly define: (a) "missing" = C-suite agent was activated but produced no domain recommendation (agent failure/timeout), (b) "partial" = C-suite agent produced a recommendation with incomplete fields (e.g., no confidence level, no key risks), and (c) expected pre-mortem behavior for each case.
**Warning signs:** Using "missing/partial" without operationalizing both terms.

### Pitfall 5: Consistency Scenarios That Are Too Similar or Too Different
**What goes wrong:** TEST-04 paired scenarios are either so similar they are trivially the same, or so different that consistency is not a meaningful expectation.
**Why it happens:** Tension between "similar enough to expect the same sensitivity" and "different enough to be meaningfully distinct scenarios."
**How to avoid:** Pairs should share structural characteristics (decision type, threshold profile, advocate/skeptic tension level) but differ in domain (different industry, different specific business decision). The structural similarity is what drives sensitivity level; the domain difference proves it is not just memorization of one scenario.
**Warning signs:** Pairs that share the same specific decision (just rephrased) or pairs that differ in structural characteristics (one irreversible, one easily reversed).

## Code Examples

All examples are markdown specification patterns, not code.

### Test Scenario Assertion Table Format
```markdown
## Behavioral Assertions

| # | Assertion | Why It Matters | Specification Reference |
|---|-----------|----------------|------------------------|
| 1 | Only CFO and CTO are activated as C-suite agents | Validates user-specified Tier 2 routing takes precedence over full-activation thresholds | orchestration-protocol.md Step 3; panel-assessment.md "Activated Domains" |
| 2 | CEO notes 2 threshold conditions as TRIGGERED in framing | Validates that threshold evaluation still occurs even when thresholds do not override Tier 2 selection | orchestration-protocol.md Step 4-5 |
| 3 | Escalation Note recommends Tier 3 with rationale citing triggered thresholds | Validates that the CEO surfaces the full-activation signal via escalation recommendation rather than silently overriding | panel-assessment.md "Escalation Note" section |
```

### Quantitative Mode Sensitivity Threshold Format
```markdown
### Quantitative Sensitivity Criteria

To assign a Mode Sensitivity rating, assess these three dimensions across all compared modes:

**Dimension 1: Decision Direction**
Count the number of distinct decisions across modes:
- All modes: same decision (e.g., all "Approve with Conditions") = CONVERGE
- Same direction with ≤1 outlier deferral (e.g., 4 Approve, 1 Defer) = PARTIAL
- Approve vs Oppose split, or 3+ distinct decisions = DIVERGE

**Dimension 2: Determinative Perspective**
Count how many different C-suite roles are cited as "Most Determinative Perspective":
- ≤2 distinct roles across all modes = CONVERGE
- 3 distinct roles = PARTIAL
- 4+ distinct roles = DIVERGE

**Dimension 3: Condition Overlap**
Compare the conditions/guardrails across modes:
- Conditions are substantively the same across modes = CONVERGE
- Same direction, additional conditions in some modes = PARTIAL
- Contradictory conditions or entirely different condition sets = DIVERGE

**Rating Rule:**
- **LOW:** All three dimensions CONVERGE
- **MEDIUM:** Any dimension PARTIAL, none DIVERGE
- **HIGH:** Any dimension DIVERGE
```

### Pre-Mortem Degraded Input Scenario Format
```markdown
## Degraded Input Definition

### Missing Recommendation
Agent: [role]
Status: Activated but produced no domain recommendation
Cause: [agent timeout / spawn failure / context window exceeded]
Pre-Mortem broadcast treatment: Excluded from the recommendation summaries distributed to other agents. CEO notes "[role] did not produce a domain recommendation" in the broadcast.
Impact on fault-line analysis: CEO notes the gap: "The [role] perspective was requested but not received. Fault lines involving [role's domain] cannot be assessed."

### Partial Recommendation
Agent: [role]
Status: Produced recommendation with incomplete fields
Missing fields: [e.g., "No confidence level provided", "Key Risks section empty"]
Pre-Mortem broadcast treatment: Included with available fields. Missing fields noted as "[not provided]" in the summary.
Impact on fault-line analysis: CEO uses available information. Low-confidence or missing-confidence recommendations are treated as LOW confidence for synthesis weighting.
```

### Paired Consistency Scenario Format
```markdown
## Scenario Pair: [Category]

### Scenario A: [Decision Name]
Issue: [description]
Decision Type: [type]
Threshold Profile: [which thresholds trigger]
Advocate/Skeptic Tension: [HIGH/MEDIUM/LOW]
Expected Sensitivity: [HIGH/MEDIUM/LOW]
Expected Sensitivity Rationale: [why this level, citing quantitative criteria]

### Scenario B: [Decision Name]
Issue: [description]
Decision Type: [type]
Threshold Profile: [which thresholds trigger -- same as A]
Advocate/Skeptic Tension: [same as A]
Expected Sensitivity: [same as A]
Expected Sensitivity Rationale: [why this level -- should mirror A's rationale]

### Consistency Assertion
Both scenarios share [structural characteristics]. Both should produce [sensitivity level] because [quantitative criteria evaluation]. If these scenarios produce different sensitivity levels, it indicates [what went wrong -- typically a flaw in the criteria or an edge case that needs clarification].
```

## State of the Art

| Current State | Target State | Impact |
|---------------|-------------|--------|
| No test scenarios exist | 4+ structured test scenario documents validate routing, pre-mortem, and mode sensitivity | First formal test coverage for the LLM agent orchestration system |
| Mode sensitivity is qualitative only (HIGH/MEDIUM/LOW prose descriptions) | Quantitative criteria with countable dimensions and worked examples | Sensitivity ratings become reproducible and auditable |
| Tier 2 / full-activation threshold interaction is ambiguous | Clear precedence rule: user selection takes precedence, CEO recommends escalation | Eliminates specification gap that could cause inconsistent routing behavior |
| Pre-mortem assumes all recommendations are complete | Defined behavior for missing and partial recommendations | Pre-mortem resilience is specified, not left to LLM improvisation |
| No consistency validation for mode sensitivity | Paired scenarios demonstrate sensitivity criteria produce stable results | Proves the criteria are specification-driven, not arbitrary |

## Open Questions

1. **Where do test scenario documents live?**
   - What we know: The project has no existing test-scenarios directory. Existing Python tests are in `tests/`. These scenarios are markdown specification documents, not pytest tests.
   - What's unclear: Whether `test-scenarios/` at project root is the best location, or whether they should live in `config/test-scenarios/` (alongside other config documents) or `docs/test-scenarios/`.
   - Recommendation: `test-scenarios/` at project root. These are first-class project artifacts (validation coverage), not config files or documentation. Root-level placement signals their importance.

2. **Should orchestration-protocol.md be amended for the Tier 2 / full-activation ambiguity?**
   - What we know: The protocol says "if ANY condition applies, ALL C-suite activate" without scoping to a specific tier. Tier 2 panel-assessment.md says "2-4 C-suite members" from user specification.
   - What's unclear: Whether to amend the orchestration protocol to add Tier 2 scoping, or whether the test scenario document alone is sufficient to establish the precedent.
   - Recommendation: Add a brief clarifying note to orchestration-protocol.md Step 4 stating that full-activation thresholds apply to CEO-routed engagements (Tier 3 and auto-routed Tier 2), not to user-specified Tier 2 role selections. The CEO should still evaluate thresholds at Tier 2 and surface triggered conditions as an escalation recommendation. This makes the spec unambiguous and gives the test scenario something concrete to validate.

3. **How specific should mode sensitivity "quantitative" thresholds be?**
   - What we know: REQUIREMENTS says "quantitative thresholds" but the project's design philosophy explicitly rejects numeric precision that LLMs cannot reliably apply (see Out of Scope: "Numeric mode weights (1.5x, 0.7x) -- LLMs cannot reliably apply numeric multipliers").
   - What's unclear: How "quantitative" the thresholds need to be to satisfy TEST-03 without creating false precision.
   - Recommendation: Use countable dimensions (number of distinct decisions, number of distinct determinative perspectives) with clear cutoffs (1 = LOW, 2-3 = MEDIUM, 4+ = HIGH). These are quantitative (they use numbers) but not computationally complex (they require counting, not calculation). The "concrete examples" requirement in TEST-03 is satisfied by the paired scenarios in TEST-04.

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
| TEST-01 | Tier 2 partial activation excludes non-requested agents even when full-activation thresholds are met | manual-only | N/A -- verify test scenario document defines correct assertions against orchestration-protocol.md and panel-assessment.md | N/A |
| TEST-02 | Phase 4.5 Pre-Mortem executes correctly with missing/partial C-suite recommendations | manual-only | N/A -- verify test scenario document defines degraded input handling and expected pre-mortem behavior | N/A |
| TEST-03 | Mode sensitivity criteria defines quantitative LOW/MEDIUM/HIGH divergence thresholds | manual-only | N/A -- verify quantitative criteria in comparative-decision-record.md with countable dimensions and concrete cutoffs | N/A |
| TEST-04 | Mode sensitivity ratings are consistent across similar decision types | manual-only | N/A -- verify paired scenarios demonstrate criteria produce same sensitivity level for structurally similar decisions | N/A |

### Sampling Rate
- **Per task commit:** Verify new/modified markdown files contain required structural elements (assertions table, quantitative criteria, paired scenarios)
- **Per wave merge:** Cross-reference all test scenario assertions against the specification files they cite -- verify cited lines exist and match
- **Phase gate:** All 4 TEST requirements verified via content inspection before `/gsd:verify-work`

### Wave 0 Gaps
None -- this phase creates specification documents and extends existing templates. No test infrastructure or fixtures needed. All validation is structural content review.

**Justification for all-manual:** All TEST requirements produce markdown specification artifacts (test scenario documents, quantitative criteria, paired scenarios). There is no code behavior to test. The project's stated position is that specification-level test scenarios replace automated agent testing. Validation consists of reading the scenario documents, verifying their assertions reference real specification content, and confirming the quantitative criteria are countable and unambiguous.

## Detailed File Analysis

### templates/comparative-decision-record.md (278 lines -- TEST-03 target)

**Current content:**
- Lines 1-25: Purpose, invocation patterns, when to use
- Lines 26-31: Mode Sensitivity Signal (qualitative HIGH/MEDIUM/LOW definitions)
- Lines 33-244: Template with DIVERGENCE ANALYSIS section
- Lines 246-258: Content mapping to production artifacts
- Lines 262-278: Divergence Classification Guide (qualitative)

**What needs to change (TEST-03):**
- The Divergence Classification Guide (lines 262-278) needs expansion with quantitative criteria. The existing qualitative definitions (Directional, Conditional, Convergence) remain as the conceptual framework. Below them, a new "Quantitative Sensitivity Criteria" section adds countable dimensions and cutoffs.
- The Mode Sensitivity Signal section (lines 26-31) should reference the quantitative criteria section for precise assessment.
- Estimated net line change: +30-40 lines (from 278 to ~310-320)

### config/orchestration-protocol.md (321 lines -- TEST-01 clarification target)

**Current content of interest:**
- Lines 80-106: Phase 1 Step 4 (full-activation threshold conditions) and Step 5 (structured per-condition evaluation output). This section says "if any single condition is met, all C-suite members activate regardless of decision type" without tier-scoping.

**What needs to change (TEST-01):**
- Add a brief clarifying note in Step 4 (after line 82) stating that full-activation threshold override applies to CEO-routed engagements. For Tier 2 with user-specified roles, the CEO still evaluates thresholds but surfaces triggered conditions as an escalation recommendation rather than overriding the user's role selection.
- Estimated net line change: +3-5 lines (from 321 to ~325)

### New: test-scenarios/ directory (TEST-01, TEST-02, TEST-04)

**Files to create:**
- `test-scenarios/tier2-partial-activation.md` -- Defines a concrete Tier 2 scenario where the user specifies 2 C-suite roles for an issue that triggers full-activation thresholds. Asserts: only specified roles activate, CEO notes triggered thresholds, escalation recommendation produced.
- `test-scenarios/premortem-degraded-input.md` -- Defines a Tier 3 scenario where one agent produces no recommendation (missing) and another produces an incomplete recommendation (partial). Asserts: pre-mortem executes with available data, CEO notes gaps in fault-line analysis, missing agent perspective acknowledged.
- `test-scenarios/mode-sensitivity-consistency.md` -- Contains 2 pairs of scenarios (one HIGH-sensitivity pair, one LOW-sensitivity pair). Each pair shares structural characteristics but differs in domain. Asserts: paired scenarios produce the same sensitivity level per the quantitative criteria.

## Scenario Design Guidance

### TEST-01: Tier 2 Partial Activation Scenario

**Decision design:** Use an acquisition decision (Strategic type). "Acquire CompanyX for market expansion." This naturally triggers multiple full-activation thresholds: Irreversibility (acquisition is irreversible), Market Position Change (alters competitive positioning), and likely Existential Financial Risk (significant capital commitment).

**Invocation:** `/cdp:panel finance tech: Should we acquire CompanyX, a competitor in the AI infrastructure space?`

User specifies only CFO and CTO. Full-activation thresholds would normally activate all 8 C-suite agents.

**Expected behavior:**
1. CEO evaluates thresholds per orchestration-protocol.md Step 4 -- evaluates all 5 conditions using diagnostic questions from routing-table.md
2. CEO finds Irreversibility TRIGGERED, Market Position Change TRIGGERED, possibly Existential Financial Risk TRIGGERED
3. CEO activates ONLY CFO and CTO (user-specified), NOT the remaining 6 agents
4. CEO includes structured threshold assessment in framing showing which thresholds triggered
5. Panel Assessment includes an Escalation Note recommending Tier 3 with rationale citing triggered thresholds as reason for full activation
6. Non-requested agents (CISO, COO, VP Sales, VP Delivery, CAO, CSO) are NOT spawned and do NOT produce analysis

### TEST-02: Pre-Mortem Degraded Input Scenario

**Decision design:** Use a cross-cutting decision at Tier 3 with full activation. "Should we pivot from B2B SaaS to B2C marketplace?" This triggers Phase 4.5 (Tier 3 only).

**Degraded state:**
- COO: activated but produces NO recommendation (simulated agent failure/timeout)
- VP Delivery: produces recommendation but with missing Confidence Level and empty Key Risks section (partial)
- All other activated agents: produce complete recommendations

**Expected behavior:**
1. Phase 4 collects 7 complete/partial recommendations (6 complete + 1 partial from VP Delivery) and notes 1 missing (COO)
2. Phase 4.5 pre-mortem broadcast includes summaries of available recommendations only -- COO's absence is noted as "COO: No domain recommendation received" and VP Delivery's is included with "[Confidence: not provided]" and "[Key Risks: not provided]"
3. Each agent answering the pre-mortem question has access to available recommendations but sees the gaps
4. CEO's Fault Line Analysis notes: "COO (Operations) perspective was requested but not received. Fault lines involving operational feasibility cannot be fully assessed." And: "VP Delivery recommendation received without confidence level or key risks; treated as LOW confidence for synthesis weighting."
5. The pre-mortem round executes for all agents that DID produce recommendations (including VP Delivery, whose partial recommendation is sufficient to participate in the challenge round)
6. Decision Record DISSENTING VIEWS section acknowledges the analytical gaps

### TEST-03: Quantitative Mode Sensitivity Criteria

**Design:** Three countable dimensions, each with three-level classification (CONVERGE/PARTIAL/DIVERGE), combined via a simple rule (any DIVERGE = HIGH, any PARTIAL and no DIVERGE = MEDIUM, all CONVERGE = LOW).

**Worked examples to include:**
1. **LOW example:** "Patch a critical security vulnerability" -- all 5 modes produce "Approve immediately" with similar guardrails (security monitoring). LOW because: 1 decision direction, 1-2 determinative perspectives (CISO in all modes), conditions substantively the same.
2. **HIGH example:** "Acquire a competitor for $50M" -- Guardian opposes (too risky), Pioneer approves aggressively (competitive window), Sentinel defers (needs more data on downside), Analyst conditionally approves (evidence supports but confidence is medium), Architect seeks middle ground (approve with extensive conditions). HIGH because: 3+ distinct decisions, 4+ determinative perspectives, contradictory conditions.
3. **MEDIUM example:** "Expand engineering team by 40% to support new product line" -- all modes approve but with meaningfully different conditions (Guardian requires 6 months runway buffer, Pioneer accelerates timeline, Architect adds cross-department coordination). MEDIUM because: 1 decision direction, 2-3 determinative perspectives, conditions additive not contradictory.

### TEST-04: Mode Sensitivity Consistency Pairs

**Pair 1 (expected HIGH):**
- Scenario A: "Divest our healthcare division to fund AI expansion" -- irreversible strategic decision with strong advocate/skeptic tension
- Scenario B: "Acquire competitor in adjacent market using 60% of cash reserves" -- irreversible strategic decision with strong advocate/skeptic tension
- Both trigger Irreversibility and Existential Financial Risk. Both have advocate (CTO/VP Sales see growth) vs skeptic (CFO/CISO see risk) tension. Both should produce HIGH sensitivity because the decision fundamentally depends on risk appetite.

**Pair 2 (expected LOW):**
- Scenario A: "Patch critical zero-day vulnerability in production authentication system" -- clear, urgent, unambiguous
- Scenario B: "Respond to regulatory order requiring data localization within 30 days" -- clear, mandatory, unambiguous
- Both have clear single-direction outcomes where all modes converge. Neither has meaningful advocate/skeptic tension because the action is essentially mandatory. Both should produce LOW sensitivity.

## Sources

### Primary (HIGH confidence)
- `config/routing-table.md` -- Full-activation threshold conditions with diagnostic questions and calibration exemplars (121 lines, read in full)
- `config/decision-modes.md` -- Five decision modes with directional weighting tables, multi-mode cost formula (216 lines, read in full)
- `config/orchestration-protocol.md` -- Five-phase cascade protocol including Phase 4.5 pre-mortem (321 lines, read in full)
- `templates/comparative-decision-record.md` -- Multi-mode comparison template with Divergence Classification Guide (278 lines, read in full)
- `templates/panel-assessment.md` -- Tier 2 Panel Assessment template with escalation criteria (179 lines, read in full)
- `agents/ceo.md` -- CEO agent with tier-specific behavior and Decision Record template (348 lines, read in full)
- `.planning/REQUIREMENTS.md` -- TEST-01 through TEST-04 requirements plus Out of Scope exclusions (read in full)
- `.planning/phases/07-specification-formalization/07-VERIFICATION.md` -- Confirms all SPEC requirements satisfied, specifications are current (read in full)

### Secondary (MEDIUM confidence)
- `.planning/phases/07-specification-formalization/07-RESEARCH.md` -- Phase 7 research documenting specification patterns and file analysis (read in full)
- `.planning/ROADMAP.md` -- Phase 8 success criteria (read in full)
- `SKILL.md` -- Tier 2 execution flow showing user-specified role routing (read in full)

### Tertiary (LOW confidence)
None -- all findings are based on direct inspection of the project files.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all files directly inspected, no libraries involved, markdown-only deliverables
- Architecture: HIGH -- test scenario structure follows established project patterns (structured markdown with tables, assertions, worked examples)
- Pitfalls: HIGH -- specification ambiguity (Tier 2 vs full-activation) identified through direct comparison of orchestration-protocol.md and panel-assessment.md; pre-mortem gap handling identified through orchestration-protocol.md Phase 4.5 analysis; mode sensitivity LLM-assessability constraint derived from REQUIREMENTS.md Out of Scope
- Scenario design: MEDIUM -- the specific decision scenarios (acquisition, pivot, security patch) are recommendations; the planner should validate they trigger the intended specification behaviors

**Research date:** 2026-03-05
**Valid until:** 2026-04-05 (stable -- specification testing patterns, no version sensitivity)
