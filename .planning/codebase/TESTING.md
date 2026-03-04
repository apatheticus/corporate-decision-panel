# Testing Patterns

**Analysis Date:** 2026-03-04

## Overview

Corporate Decision Panel is a prompt-and-configuration agent system without traditional unit tests, test runners, or code coverage metrics. Testing occurs at the **specification level** and **execution level**:

- **Specification Testing:** Validating agent logic, routing rules, and decision modes through documented protocols
- **Execution Testing:** Running through all three tiers (Tier 1, 2, 3) to verify end-to-end behavior
- **Protocol Testing:** Ensuring the five-phase cascade executes correctly with engineered dissent preserved

There is no test file structure (no `.test.md` or `.spec.md` files). Testing is manual and specification-driven.

## Testing Strategy

CDP's testing relies on:

1. **Specification completeness** - Each agent's modes (A, B, C) are fully specified
2. **Template compliance** - All outputs follow mandatory templates
3. **Manual execution through tiers** - Running `/cdp:consult`, `/cdp:panel`, `/cdp:deliberate` with real business scenarios
4. **Protocol validation** - Verifying five-phase cascade executes correctly
5. **Output validation** - Checking that Decision Records, Panel Assessments, Advisory Notes follow their templates

## Test Dimensions

### 1. Agent Behavior Testing

Each agent is tested across **three modes** to verify correct behavior:

**Mode A (Tier 1 -- Direct Consult):**
- Agent receives a direct question without CEO framing
- Agent runs internal checklist considering all team lead perspectives
- Agent produces Advisory Note (3-5 sentences)
- Optional: Agent appends Escalation Brief if cross-domain implications detected

**Test pattern for Mode A:**
```
Input: /cdp:consult cfo: Can we afford to hire 15 engineers this quarter?

Verify:
- CFO produces Advisory Note in correct format
- Response addresses financial dimensions (FP&A, Treasury, Tax, etc.)
- Confidence level stated explicitly
- If cross-domain, Escalation Brief appended with routing recommendations
- Decision Mode (default: Analyst) applied to tone and framing
```

**Mode B (Tier 2/3 -- Full Analysis):**
- Agent receives CEO framing with evaluation dimensions
- Agent translates CEO question into domain-specific sub-questions
- Agent dispatches relevant team leads (not all five for every question)
- Agent synthesizes team lead findings into domain recommendation

**Test pattern for Mode B:**
```
Input: CEO frames issue; CFO activated

Verify:
- CFO translates CEO framing into financial sub-questions
- CFO dispatches relevant team leads (FP&A, Treasury, etc., not all five)
- CFO collects structured outputs from dispatched team leads
- CFO produces Domain Recommendation with required sections:
  * Domain Recommendation: [Approve/Oppose/Conditions/Neutral]
  * Confidence: [High/Medium/Low]
  * Team Lead Findings (one-liner per relevant lead)
  * Key Risks, Key Opportunities
  * Internal Contradictions (if team leads conflict)
```

**Mode C (Phase 4.5 -- Pre-Mortem, Tier 3 only):**
- Agent receives summaries of ALL other C-suite recommendations
- Agent answers single structured question: "Assume failure in 12 months. What caused it?"
- Agent focuses on cross-domain failure modes (not repeating own risks)

**Test pattern for Mode C:**
```
Input: All activated C-suite recommendations; single pre-mortem question

Verify:
- CFO identifies financial failure modes embedded in other domains' assumptions
- Response is specific: names the assumption, identifies the gap
- Response is NOT a restatement of own domain risks
- One round only, no back-and-forth
- Response informs Fault Line Analysis in Decision Record
```

### 2. Routing and Activation Testing

**Test dimension: Default activation by decision type**

Each decision type has a default routing table (`config/routing-table.md`):

```markdown
| Decision Type | Default Activation |
|---------------|-------------------|
| Strategic | CEO, CFO, CTO, VP Sales |
| Operational | CEO, COO, VP Delivery |
| Financial | CEO, CFO, COO |
| Technical | CEO, CTO, CISO |
| Personnel | CEO, CAO, COO, VP Delivery |
| Compliance/Risk | CEO, CISO, CAO, CFO |
```

**Test pattern:**
```
Scenario: User invokes /cdp:panel with a strategic decision

Verify:
- CEO activates CFO, CTO, VP Sales by default
- CEO can override (add CISO for security angle, add CAO for organizational impact)
- Override rationale is stated explicitly
- CSO activation at CEO discretion, not mandatory
```

**Test dimension: Full-activation threshold conditions**

Five conditions trigger full C-suite activation regardless of decision type:

1. **Irreversibility** - Decision cannot be undone
2. **Headcount Impact** - Affects >30% of headcount
3. **Market Position Change** - Business model or market positioning changes
4. **Existential Financial Risk** - Bet-the-company level financial exposure
5. **Domain Uncertainty** - CEO unsure which domains are relevant

**Test pattern:**
```
Scenario: User presents a decision that triggers one threshold condition

Verify:
- CEO assesses each condition explicitly
- When condition triggered, CEO activates all C-suite
- CEO states which condition(s) triggered full activation
- All 8 C-suite members (COO, CFO, CTO, CISO, CAO, VP Sales, VP Delivery, CSO)
  produce domain recommendations
```

### 3. Disposition Testing (Engineered Dissent)

CDP deliberately engineers dissent by assigning fixed dispositions:

- **4 Skeptics** (COO, CFO, CISO, VP Delivery): Surface concerns, risks, constraints
- **2 Advocates** (CTO, VP Sales): Identify opportunities, possibilities, leverage
- **1 Systemic** (CAO): Organizational absorption and governance
- **1 Investigative** (CSO): Evidence and patterns

**Test pattern for skeptic vs. advocate tension:**
```
Scenario: Proposal to acquire a competitor

Verify (Skeptics):
- CFO surfaces hidden acquisition costs (integration, retention, restructuring)
- COO identifies operational absorption risks
- CISO flags security integration risks
- VP Delivery flags delivery team disruption risks

Verify (Advocates):
- CTO identifies technical integration opportunities and architectural benefits
- VP Sales identifies market position and revenue opportunities

Verify (Synthesizer):
- CEO notes the divergence in fault line analysis
- CEO applies decision mode (Guardian favors skeptics, Pioneer favors advocates)
- CEO does not smooth over disagreement
```

**Susceptibility mitigation testing:**

Each agent's disposition has a natural weakness:

- **Skeptic weakness:** Softening objections (sycophancy bias)
  - Test: Verify skeptic states concerns directly, not hedged
  - Pattern: "Here is the financial risk" not "While this is risky, there might be benefits"

- **Advocate weakness:** Under-weighting genuine constraints
  - Test: Verify advocate names strongest objection to own position
  - Pattern: "The strongest objection is [X], I still advocate because [Y]"

- **Systemic weakness:** Unfalsifiable culture claims
  - Test: Verify systemic claims ground in concrete mechanisms
  - Pattern: "This contradicts policy X, requires contract renegotiation, affects team Y" not "The culture isn't ready"

- **Investigative weakness:** Equidistant from evidence, avoiding judgment
  - Test: Verify investigative role produces evidence summary, not both-sides-ism
  - Pattern: "Evidence confirms/contradicts/partially supports" not "Some evidence suggests"

### 4. Five-Phase Cascade Testing

**Test pattern: Phase progression**

```
Tier 1 (/cdp:consult):
  Phase 0: Skipped
  Phase 1: Skipped
  Phase 2-5: Skipped
  Result: Advisory Note

Tier 2 (/cdp:panel):
  Phase 0: Skipped
  Phase 1: CEO frames and routes to 2-4 C-suite
  Phase 1.5: Conditional (CSO research if CSO activated)
  Phase 2: C-suite dispatch to team leads
  Phase 3: Team lead findings
  Phase 4: C-suite synthesis (no pre-mortem)
  Phase 5: CEO lightweight synthesis
  Result: Panel Assessment

Tier 3 (/cdp:deliberate):
  Phase 0: Shared consciousness broadcast to all activated C-suite
  Phase 1: CEO frames and routes to all relevant C-suite
  Phase 1.5: Conditional (CSO research directive if activated)
  Phase 2: C-suite dispatch to team leads
  Phase 3: Team lead findings
  Phase 4: C-suite synthesis
  Phase 4.5: Pre-mortem challenge (one round)
  Phase 5: CEO full deliberation
  Result: Decision Record (3-5 pages)
```

**Test pattern: Phase 0 broadcast (Tier 2/3 only)**

```
Verify:
- All activated C-suite receive identical context simultaneously
- Broadcast includes: Company context (if .cdp-context/company.md exists),
  issue statement, CEO decomposition, routing rationale, decision type,
  which roles activated/excluded and why, Research Dossier (if Phase 1.5
  executed), active Decision Mode

- No role receives privileged information other roles do not
- Shared consciousness means identical starting point for independent analysis
```

### 5. Output Template Testing

All outputs follow mandatory templates. Templates are tested by verifying structure compliance:

**Advisory Note template compliance:**
```
ADVISORY NOTE
Domain: [Role] -- [Mandate]
Date: [YYYY-MM-DD HH:MM UTC]
Mode: [Guardian | Pioneer | Architect | Analyst | Sentinel]
Question: [User question]

---

[3-5 sentences]

---
Confidence: [High | Medium | Low]
[If Low: explanation of what would increase confidence]

[Optional: ESCALATION BRIEF with cross-domain implications]
```

**Domain Recommendation template compliance:**
```
CFO DOMAIN RECOMMENDATION

Domain Recommendation: [Approve | Oppose | Approve with Conditions | Neutral]
Confidence Level: [High | Medium | Low]

SUMMARY:
[2-3 sentence synthesis]

TEAM LEAD FINDINGS:
- [Lead 1]: [1-2 sentences]
- [Lead 2]: [1-2 sentences]

INTERNAL CONTRADICTIONS:
[Flag tensions between team leads]

KEY RISKS:
[Bulleted list]

KEY OPPORTUNITIES:
[Bulleted list]

CONDITIONS FOR APPROVAL (if Approve with Conditions):
[Bulleted list]
```

**Panel Assessment template compliance:**
```
PANEL ASSESSMENT: [Issue Title]
Assessment ID: PA-[YYYYMMDD]-[number]
Date: [timestamp]
Decision Type: [type]
Tier: 2 (Working Session)
Decision Mode: [mode]

ISSUE SUMMARY
[2-3 sentences]

ACTIVATED DOMAINS
[Table with domain + rationale]

DOMAIN RECOMMENDATIONS
[Per domain: recommendation, confidence, key finding, primary risk, primary opportunity]

KEY AGREEMENTS AND DISAGREEMENTS
[What domains agree on; where they diverge]

CEO SYNTHESIS
[3-5 sentences applying active mode]
Most Determinative Perspective: [role + why]

RECOMMENDED NEXT STEPS
[Bulleted actions with implied owner and timeframe]
```

**Decision Record template compliance (Tier 3):**
```
EXECUTIVE SUMMARY
[3-5 sentences]

DECISION RECORD: [Title]
Decision ID: [auto-generated]
Date: [timestamp]
Submitted by: [user]
Decision Type: [classification]
Tier: [1/2/3]
Decision Mode: [mode]

1. ISSUE STATEMENT
2. CEO FRAMING
3. RESEARCH DOSSIER SUMMARY (if Phase 1.5)
4. DOMAIN ANALYSES (per C-suite role)
5. FAULT LINE ANALYSIS
6. CEO DECISION
7. DISSENTING VIEWS
8. NEXT STEPS
9. METADATA
```

**Test pattern:**
```
For every output, verify:
- All required sections present
- Recommendation enum values used correctly
- Confidence levels stated (High/Medium/Low)
- Date format: YYYY-MM-DD HH:MM UTC
- Decision IDs follow pattern (auto-generated, timestamped)
- Bullet lists and tables properly formatted
- Escal Brief appended only when cross-domain implications detected
```

### 6. Decision Mode Testing

Five decision modes define how CEO synthesizes identical domain analyses into different decisions:

**Mode testing pattern:**
```
Test all modes against the same decision:
Input: Same issue, same domain analyses, same fault lines

For each mode:
- Verify CEO applies mode's disposition modifier
- Verify weighting matches mode theory:
  * Guardian: Weights skeptics more, requires addressing concerns
  * Pioneer: Weights advocates more, frames concerns as engineering problems
  * Architect: Weights consensus potential, seeks position satisfying most concerns
  * Analyst: Weights confidence levels regardless of disposition
  * Sentinel: Weights strongest single objection most heavily

- Verify output differs across modes (mode sensitivity detected)
- Document where modes converge (evidence speaks for itself)
- Document where modes diverge (disposition matters more than analysis)
```

**Mode/Tier interaction testing:**

Each mode produces different behavior at each tier:

```
Guardian mode at Tier 1:
- Highlights downside risks
- Suggests what could go wrong
- Response leans cautious

Guardian mode at Tier 2:
- Synthesis biased toward risk mitigation
- Extensive guardrails on conditions
- Skeptic concerns addressed before approval

Guardian mode at Tier 3:
- CEO weights skeptics heavily
- High bar for approval
- Conditions drawn from all skeptic voices

[Repeat for Pioneer, Architect, Analyst, Sentinel]
```

### 7. Configuration Testing

**Routing table testing:**

```
For each decision type:
- Verify default activation matches documented table
- Verify override mechanism works (user can add/remove roles)
- Verify override rationale stated explicitly
- Verify CSO activation conditional, not mandatory

For full-activation thresholds:
- Create scenario triggering each threshold condition
- Verify all C-suite activates (8 roles)
- Verify CEO assesses each condition explicitly
- Verify CEO states which condition(s) triggered
```

**Decision mode definition testing:**

```
For each mode:
- Verify CEO prompt modifier is present and specific
- Verify mode/tier interaction matrix documented
- Verify mode recommendation criteria explained
- Verify multi-mode comparison cost/benefit documented
- Verify all five modes available for all tiers
```

**Company profile testing:**

```
Verify:
- Archetype presets loadable (.cdp-context/company.md)
- Override mechanism works (can modify defaults per-project)
- Calibration protocol documented (how to adjust for company size/stage)
- Impact on routing/defaults clear (which settings affected by profile)
```

### 8. Cross-Domain Consistency Testing

**Tension pair testing (natural oppositions):**

CDP explicitly documents "natural tension pairs" that should appear in analysis:

```
CFO <-> VP Sales:
- CFO surfaces cost hidden in sales projections
- VP Sales surfaces revenue opportunity CFO's model underestimates
- Tension should be visible in fault line analysis

COO <-> CTO:
- COO surfaces operational constraints on technical ambition
- CTO surfaces architectural leverage operational thinking missed
- Tension should be visible in CEO synthesis

CISO <-> VP Sales:
- CISO surfaces security/regulatory risk in new market
- VP Sales surfaces competitive urgency in delaying
- Tension should be visible in mode-weighted decision
```

## Manual Testing Protocol

Since there are no automated tests, manual testing follows this protocol:

### 1. Specification Review (Monthly)

- Read all agent specifications (`agents/c-suite/*.md`, `agents/team-leads/*/*.md`)
- Verify each agent has complete Mode A, B, C specifications
- Verify susceptibility mitigation is explicit for each agent's disposition
- Verify output templates match documented formats

### 2. Execution Testing (Per significant change)

- Run `/cdp:consult [role]` with a test business scenario
- Run `/cdp:panel [roles]` with a multi-domain scenario
- Run `/cdp:deliberate` with a full-cascade scenario
- Verify output structure matches templates
- Check that engineered dissent is preserved (not averaged away)

### 3. Mode Comparison Testing (Per new decision mode)

- Run same issue through all five decision modes
- Document how synthesis differs by mode
- Verify mode sensitivity is detected/documented
- Verify divergences map to decision theory differences

### 4. Configuration Testing (Per change to routing or modes)

- Update `config/routing-table.md` or `config/decision-modes.md`
- Re-run test scenarios that depend on changed rules
- Verify override mechanism still works
- Verify documentation stays in sync with code

### 5. Output Validation (Every production run)

- After production pipeline completes, verify artifacts exist:
  - Decision Record / Panel Assessment / Advisory Note (RECORD.md)
  - Infographics (PNG files in `/images`)
  - Presentation (PPTX in `.cdp-output/`)
  - Document (DOCX in `.cdp-output/`)
  - Web page (HTML in `.cdp-output/`)
  - PDFs (Results PDF + Deliberation Capsule)
- Check template compliance for each artifact
- Verify cross-references and dependencies correct

## Test Coverage Areas

**Not tested (N/A for prompt system):**
- Unit tests on agent logic (logic is specification-based)
- Code coverage metrics (no traditional code)
- Regression tests (specifications are source of truth)
- Performance benchmarks (decision quality, not execution speed)
- Integration tests against external APIs (no external dependencies)

**Tested:**
- Specification completeness (all agents have all modes)
- Template compliance (all outputs follow mandatory formats)
- Routing correctness (decision type maps to correct C-suite)
- Engineered dissent preservation (perspectives not averaged)
- Decision mode application (mode affects synthesis correctly)
- Phase cascade execution (all phases execute in order)
- Cross-domain tension visibility (natural oppositions emerge)

## Documentation for Testing

- **`agents/c-suite/*.md`** - Agent specifications with Mode A/B/C for testing
- **`config/routing-table.md`** - Routing defaults and threshold conditions
- **`config/decision-modes.md`** - Mode definitions and mode/tier matrix
- **`templates/advisory-note.md`** - Advisory Note format with examples
- **`templates/panel-assessment.md`** - Panel Assessment format
- **`templates/decision-record.md`** - Decision Record format
- **`docs/ARCHITECTURE.md`** - Five-phase cascade and agent hierarchy
- **`SKILL.md`** - Orchestration protocol (full system specification)

---

*Testing analysis: 2026-03-04*
