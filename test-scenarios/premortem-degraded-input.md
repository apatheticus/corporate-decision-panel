# Test Scenario: Pre-Mortem with Degraded Input

**Requirement:** TEST-02
**Validates:** Phase 4.5 Pre-Mortem executes correctly when one or more C-suite agents have missing or partial recommendations
**Specification References:**
- `config/orchestration-protocol.md` Phase 4.5 (Pre-Mortem Dispatch protocol)
- `config/orchestration-protocol.md` Phase 4 (C-Suite Synthesizes Upward -- domain recommendation format)
- `agents/ceo.md` Decision Record template (DISSENTING VIEWS, FAULT LINE ANALYSIS sections)

---

## Degraded Input Definitions

The following operational definitions establish what "missing" and "partial" mean in the context of domain recommendations. These definitions are prerequisites for the behavioral assertions below.

### Missing Recommendation

- **Definition:** A C-suite agent was activated and spawned but produced no domain recommendation output
- **Possible causes:** Agent timeout (exceeded maxTurns), spawn failure, context window exceeded
- **Pre-mortem broadcast treatment:** Excluded from the recommendation summaries distributed to other agents. CEO notes "[Role] did not produce a domain recommendation" in the broadcast preamble.
- **Impact on fault-line analysis:** CEO notes the gap explicitly: "The [Role] perspective was requested but not received. Fault lines involving [Role's domain] cannot be fully assessed."

### Partial Recommendation

- **Definition:** A C-suite agent produced a domain recommendation but with one or more incomplete required fields (e.g., missing Confidence Level, empty Key Risks section, no Team Lead Findings)
- **Pre-mortem broadcast treatment:** Included in the recommendation summaries with available fields. Missing fields are noted as "[not provided]" in the summary distributed to other agents.
- **Impact on fault-line analysis:** CEO uses available information. Recommendations with missing or absent confidence levels are treated as LOW confidence for synthesis weighting purposes.

---

## Decision Scenario

**Issue:** "Should we pivot from B2B SaaS to B2C marketplace model?"

**Invocation:** `/cdp:deliberate: Should we pivot from B2B SaaS to B2C marketplace model?`

**Decision Type:** Strategic (cross-cutting)

**Context:** Tier 3 full deliberation. All C-suite agents activated via routing (cross-cutting strategic decision triggers full activation via Market Position Change threshold -- changes customer segments, revenue model, and competitive positioning simultaneously). This is a Tier 3 engagement so Phase 4.5 pre-mortem executes.

---

## Degraded State Definition

| Agent | Status | Details |
|-------|--------|---------|
| COO | MISSING | Activated but produces NO recommendation. Simulated agent timeout -- exceeded maxTurns. No domain recommendation output exists. |
| VP Delivery | PARTIAL | Produces a recommendation but with missing Confidence Level field and empty Key Risks section. Domain Recommendation is "Approve with Conditions" but confidence and risk assessment are absent. |
| CFO | Complete | Produces complete, well-formed domain recommendation |
| CTO | Complete | Produces complete, well-formed domain recommendation |
| CISO | Complete | Produces complete, well-formed domain recommendation |
| VP Sales | Complete | Produces complete, well-formed domain recommendation |
| CAO | Complete | Produces complete, well-formed domain recommendation |
| CSO | Complete | Produces complete, well-formed domain recommendation |

**Summary:** 6 complete recommendations + 1 partial (VP Delivery) + 1 missing (COO) = 7 available outputs, 8 activated agents.

---

## Pre-Conditions

- Tier 3 invocation with full C-suite activation (8 agents)
- All agents successfully spawned and received Phase 0 broadcast
- COO agent reached maxTurns limit before producing domain recommendation
- VP Delivery agent produced a domain recommendation with incomplete fields
- All other 6 agents produced complete domain recommendations

---

## Expected Behavior

### Phase 4: Collect Recommendations

- CEO collects recommendation outputs from all 8 activated agents
- CEO receives 6 complete domain recommendations (CFO, CTO, CISO, VP Sales, CAO, CSO)
- CEO receives 1 partial domain recommendation from VP Delivery:
  - Domain Recommendation: "Approve with Conditions" (present)
  - Confidence Level: (absent -- field not provided)
  - Summary: (present)
  - Team Lead Findings: (present)
  - Key Risks Identified: (absent -- section empty)
  - Key Opportunities Identified: (present)
  - Internal Contradictions: (present)
- CEO registers COO as "activated but no recommendation received"
- CEO registers VP Delivery recommendation as having incomplete fields (missing Confidence Level, empty Key Risks)

### Phase 4.5: Pre-Mortem Challenge

**Step 1 -- Distribute Recommendations:**
- CEO prepares pre-mortem broadcast with summaries of ALL available recommendations
- Broadcast includes summaries of 7 recommendations (6 complete + 1 partial from VP Delivery)
- COO's absence is noted in the broadcast preamble: "COO: No domain recommendation received (agent timeout)"
- VP Delivery's summary includes available fields with gaps explicitly marked:
  - "VP Delivery -- Delivery & Client Commitments: Recommend Approve with Conditions. Confidence: [not provided]. Key Risks: [not provided]."
- Each agent receiving the broadcast can distinguish between "no risks identified" (a finding) and "risk assessment not performed" (a gap)

**Step 2 -- Challenge Question:**
- The structured pre-mortem question ("Assume this decision fails catastrophically in 12 months...") is sent to all 7 agents that produced ANY output: CFO, CTO, CISO, VP Sales, CAO, CSO, and VP Delivery
- COO does NOT participate in the pre-mortem round because:
  1. The agent is non-responsive (exceeded maxTurns)
  2. The agent produced no recommendation to challenge from
  3. Forcing participation would require fabricating a perspective

**Step 3 -- Collect Pre-Mortem Responses:**
- CEO collects pre-mortem responses from 7 agents (not 8)
- Each responding agent has seen the COO gap and VP Delivery limitations in the broadcast
- Agents may incorporate the gaps into their failure scenarios (e.g., "Failure caused by operational blind spot since COO perspective was missing -- no one assessed operational capacity to execute the pivot")
- VP Delivery participates despite partial recommendation -- having some domain perspective is sufficient for the challenge round

### Phase 5: CEO Deliberation

**Fault Line Analysis:**
- Explicitly acknowledges the COO gap: "The COO (Operations) perspective was requested but not received. Fault lines involving operational feasibility, process capacity, and vendor dependencies cannot be fully assessed."
- Notes VP Delivery limitation: "VP Delivery recommendation received without confidence level or key risks. Treated as LOW confidence for synthesis weighting."
- Fault line analysis proceeds with available information, noting where gaps may hide unidentified fault lines

**Decision Record -- DISSENTING VIEWS:**
- Acknowledges the analytical gaps -- does not pretend complete analysis was achieved
- If pre-mortem responses cited the COO gap as a failure vector, these are preserved verbatim
- The gap is treated as a form of dissent-by-absence: the missing perspective may have contained critical objections

**CEO Synthesis:**
- CEO notes reduced confidence in operational dimensions due to missing COO perspective
- VP Delivery's "Approve with Conditions" recommendation carries reduced weight (LOW confidence default)
- The final decision is still rendered -- the system does not block on missing input
- Decision includes explicit confidence caveats naming the operational assessment gap
- If the decision is approval, conditions should include "validate operational capacity" to compensate for the COO gap

---

## Behavioral Assertions

| # | Assertion | Why It Matters | Specification Reference |
|---|-----------|----------------|------------------------|
| 1 | Pre-mortem broadcast includes summaries of 7 available recommendations, not 8 | Missing recommendation (COO) is excluded from summaries, not represented with empty/placeholder content | orchestration-protocol.md Phase 4.5 Step 1 |
| 2 | COO absence is explicitly noted in pre-mortem broadcast preamble | Other agents need to know a perspective is MISSING, not just absent from the list | orchestration-protocol.md Phase 4.5 Step 1 |
| 3 | VP Delivery summary in broadcast marks missing fields as "[not provided]" | Other agents can distinguish between "no risks identified" and "risk assessment not performed" | orchestration-protocol.md Phase 4 domain recommendation format |
| 4 | COO does NOT participate in the pre-mortem challenge round | A non-responsive agent cannot answer the challenge question. Forcing participation would require fabricating a perspective. | orchestration-protocol.md Phase 4.5 Step 3 |
| 5 | VP Delivery DOES participate in the pre-mortem round despite partial recommendation | Having some recommendation output is sufficient to participate in the challenge round. Partial information is better than exclusion. | orchestration-protocol.md Phase 4.5 Steps 1-3 |
| 6 | CEO Fault Line Analysis explicitly names the COO gap and its impact on operational assessment | The CEO must acknowledge what CANNOT be assessed, not silently produce a decision that appears complete | agents/ceo.md Decision Record FAULT LINE ANALYSIS section |
| 7 | CEO treats VP Delivery recommendation as LOW confidence for synthesis weighting | Missing confidence field defaults to the most conservative assumption, not optimistic interpretation | agents/ceo.md CEO synthesis methodology |

---

## Failure Modes

| Violation | What Would Happen | How to Detect |
|-----------|-------------------|---------------|
| Pre-mortem broadcast includes placeholder for missing agent | Other agents receive fabricated "COO recommends..." content that does not exist. Pre-mortem challenges may be based on false input. | Broadcast summary contains a COO recommendation entry despite COO producing no output. |
| Missing agent still participates in pre-mortem | System attempts to send the challenge question to a non-responsive agent, causing a hang or timeout. Or the system fabricates a pre-mortem response. | Pre-mortem round has 8 responses instead of 7. Or the round hangs waiting for COO. |
| CEO produces decision without acknowledging gaps | Decision Record reads as if all 8 domains provided complete analysis. User assumes full coverage when 1 domain is missing and 1 is degraded. | No mention of COO absence or VP Delivery limitations in Fault Line Analysis or DISSENTING VIEWS. |
| VP Delivery's missing confidence treated as HIGH or MEDIUM | Synthesis gives VP Delivery's recommendation more weight than warranted. Decision anchors on an assessment whose author could not even express their own confidence level. | VP Delivery cited as determinative perspective or high-confidence finding without noting the absent confidence field. |

---

## Expected Output Excerpt

The following shows the expected Fault Line Analysis excerpt from the Decision Record for this scenario:

```
FAULT LINE ANALYSIS

Analytical Coverage Gaps:

  The COO (Operations) perspective was requested but not received. The COO
  agent was activated for this Tier 3 deliberation but exceeded its maxTurns
  limit before producing a domain recommendation. As a result, fault lines
  involving operational feasibility, process capacity to execute the B2B-to-B2C
  pivot, vendor dependency restructuring, and workflow transition planning
  cannot be fully assessed.

  The VP Delivery recommendation was received without a confidence level or
  key risks assessment. This recommendation is treated as LOW confidence for
  synthesis weighting purposes. The VP Delivery's "Approve with Conditions"
  position is noted but carries reduced analytical weight because the domain
  expert could not or did not express their own confidence in the assessment.

Identified Fault Lines:

  1. Revenue Model Transition Risk (CFO vs VP Sales): The CFO identifies
     a 12-18 month revenue trough during the pivot where B2B contracts wind
     down before B2C marketplace revenue reaches break-even. VP Sales sees
     the B2C marketplace TAM as significantly larger but acknowledges the
     go-to-market motion is fundamentally different...

  [Additional fault lines from available domain recommendations]

  N. Operational Execution Gap (unassessed): The COO perspective was not
     available. Pre-mortem responses from CTO and CAO flagged operational
     capacity as a potential failure vector -- specifically, whether existing
     processes and teams can execute a marketplace model while maintaining
     B2B obligations during transition. This fault line is flagged but
     cannot be fully characterized without the COO's domain analysis.
```
