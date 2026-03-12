# Test Scenario: Tier 2 Partial Activation with Triggered Thresholds

**Requirement:** TEST-01
**Validates:** Tier 2 partial activation correctly excludes non-requested C-suite agents even when full-activation thresholds are met
**Specification References:**
- `config/orchestration-protocol.md` Step 4 (Tier 2 scoping note)
- `templates/panel-assessment.md` (Activated Domains, Escalation Note sections)
- `config/routing-table.md` (threshold diagnostic questions)

---

## Decision Scenario

**Issue:** "Should we acquire CompetitorX, a competitor in the AI infrastructure space, for $45M?"

**Invocation:** `/cdp:panel finance tech: Should we acquire CompetitorX, a competitor in the AI infrastructure space, for $45M?`

**Decision Type:** Strategic

**Context:** The user explicitly specifies only CFO and CTO. This is an acquisition decision that triggers multiple full-activation thresholds:
- **Irreversibility** -- acquisition cannot be undone; capabilities merge, contracts transfer, regulatory approvals are consumed
- **Market Position Change** -- alters competitive positioning in the AI infrastructure space
- **Existential Financial Risk** -- $45M is a significant capital commitment against company reserves

---

## Pre-Conditions

- Tier 2 invocation with user-specified roles (CFO and CTO)
- Decision characteristics that would trigger 3 of 5 full-activation thresholds
- No `.cdp-context/company.md` required -- scenario is self-contained

---

## Expected Behavior

### Phase 1: Frame and Route

- CEO decomposes the acquisition into evaluation dimensions (financial viability, technical integration, market position impact, talent retention, regulatory exposure, operational absorption)
- CEO classifies as Strategic decision type
- CEO evaluates all 5 threshold conditions per `config/routing-table.md` diagnostic questions:
  - **Irreversibility: TRIGGERED** -- acquisition is practically irreversible. Reversal would require divesting acquired assets, re-establishing competitor as independent entity, unwinding integrated capabilities. Reversal cost exceeds 50% of the original decision cost.
  - **Headcount Impact: NOT TRIGGERED** -- acquisition does not directly restructure >30% of workforce. CompetitorX team integration affects a bounded portion of headcount without eliminating entire role categories.
  - **Market Position Change: TRIGGERED** -- acquiring a competitor alters competitive positioning in AI infrastructure. The company would serve CompetitorX's customer segments and eliminate a direct competitor, changing the competitive landscape.
  - **Existential Financial Risk: TRIGGERED** -- $45M capital commitment. Depending on company reserves, this may commit capital exceeding the 6-month operating expense runway threshold. The acquisition creates single-source dependency on successful integration.
  - **Domain Uncertainty: NOT TRIGGERED** -- CEO can identify relevant domains. Acquisition analysis has clear precedent and known domain relevance (finance for valuation, technology for integration assessment).
- CEO finds 3 of 5 threshold conditions TRIGGERED
- CEO activates ONLY CFO and CTO per user specification -- does NOT override with full activation
- CEO includes structured threshold assessment in framing output showing all 5 conditions evaluated with per-condition TRIGGERED/NOT TRIGGERED status

### Phase 2-4: C-Suite Analysis

- Only CFO and CTO are spawned as Agent Team teammates
- No other C-suite agents (COO, CISO, VP Sales, VP Delivery, CAO, CSO) are spawned
- CFO and CTO each run Mode B with team lead delegation
- CFO evaluates: financial viability, valuation, funding structure, integration costs
- CTO evaluates: technical integration complexity, platform compatibility, engineering talent assessment

### Phase 5: CEO Synthesis

- CEO produces Panel Assessment with only CFO and CTO domain recommendations
- Panel Assessment includes an Escalation Note recommending Tier 3
- Escalation rationale explicitly cites the 3 triggered threshold conditions as reason for full activation
- Escalation Note recommends: `/cdp:deliberate: Should we acquire CompetitorX, a competitor in the AI infrastructure space, for $45M?`
- Escalation Note lists additional domains for Tier 3: COO, CISO, VP Sales, VP Delivery, CAO, CSO

---

## Behavioral Assertions

| # | Assertion | Why It Matters | Specification Reference |
|---|-----------|----------------|------------------------|
| 1 | Only CFO and CTO are activated as C-suite agents | Validates user-specified Tier 2 routing takes precedence over full-activation thresholds | orchestration-protocol.md Step 4 Tier 2 scoping note |
| 2 | CEO evaluates all 5 threshold conditions and finds 3 TRIGGERED | Validates threshold evaluation still occurs at Tier 2 even when thresholds do not override user selection | orchestration-protocol.md Steps 4-5 |
| 3 | Structured threshold assessment appears in CEO framing output with per-condition TRIGGERED/NOT TRIGGERED status | Validates routing decision is auditable regardless of tier | orchestration-protocol.md Step 5 |
| 4 | COO, CISO, VP Sales, VP Delivery, CAO, and CSO are NOT spawned and produce NO analysis | Validates that non-requested agents are fully excluded, not silently activated | orchestration-protocol.md Step 4 Tier 2 scoping note |
| 5 | Panel Assessment includes Escalation Note recommending Tier 3 with full activation | Validates that triggered thresholds are surfaced as escalation recommendation rather than silent override | panel-assessment.md Escalation Note section |
| 6 | Escalation rationale explicitly names the 3 triggered conditions (Irreversibility, Market Position Change, Existential Financial Risk) | Validates that the CEO provides actionable reasoning for why escalation is warranted | panel-assessment.md Escalation Note section |

---

## Failure Modes

| Violation | What Would Happen | How to Detect |
|-----------|-------------------|---------------|
| Full-activation overrides user's Tier 2 role selection | All 9 C-suite agents activate for a decision the user wanted analyzed by only 2 domains. User's explicit intent is ignored. Costs ~4x more in agent turns. | More than 2 C-suite agent spawns in Agent Team. Panel Assessment shows domains the user did not request. |
| Threshold evaluation skipped at Tier 2 | CEO does not assess thresholds because "they don't apply at Tier 2." User never learns that the decision warrants broader analysis. The escalation safety net is lost. | No threshold assessment section in CEO framing output. No Escalation Note in Panel Assessment despite clearly triggerable thresholds. |
| Escalation Note omits threshold rationale | CEO recommends escalation but without citing specific triggered thresholds. User cannot evaluate whether escalation is warranted or routine. | Escalation Note present but rationale is generic ("this issue is complex") rather than citing specific threshold conditions. |

---

## Expected Output Excerpt

The following shows the expected Escalation Note section of the Panel Assessment for this scenario:

```
ESCALATION NOTE

Recommended Escalation: /cdp:deliberate: Should we acquire CompetitorX, a competitor in the AI infrastructure space, for $45M?

Escalation Rationale: This Tier 2 working session activated only CFO and CTO per
the user's specification. However, threshold evaluation identified 3 of 5
full-activation conditions as TRIGGERED:

  1. Irreversibility -- TRIGGERED: Acquisition cannot be meaningfully reversed.
     Divesting acquired assets, re-establishing CompetitorX as an independent entity,
     and unwinding integrated capabilities would cost more than the original acquisition.

  2. Market Position Change -- TRIGGERED: Acquiring a direct competitor in AI
     infrastructure fundamentally alters the company's competitive positioning,
     changes which customer segments are served, and eliminates a market participant.

  3. Existential Financial Risk -- TRIGGERED: $45M capital commitment represents
     a significant portion of available reserves. Integration failure could exhaust
     financial runway before recovery.

Under Tier 3 deliberation, all C-suite perspectives would activate, Phase 0 shared
consciousness broadcast would ensure cross-domain context, and Phase 4.5 pre-mortem
would stress-test the acquisition decision against catastrophic failure scenarios.

Additional Domains for Tier 3: COO (operational capacity to absorb acquired
entity), CISO (security and compliance exposure from integration), VP Sales
(revenue synergies and market channel impact), VP Delivery (existing commitment
disruption from integration workload), CAO (organizational absorption, cultural
integration, legal/contractual implications), CSO (evidence-based research on
comparable acquisitions, market conditions, competitive landscape)
```
