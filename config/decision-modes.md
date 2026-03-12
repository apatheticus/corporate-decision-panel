# Decision Modes

## Overview

Decision Modes are CEO synthesis prompt modifiers. The underlying domain analysis is identical across modes -- the same team lead outputs, the same C-suite recommendations, the same fault lines. Different modes apply different weighting to produce different decisions from the same inputs.

Each mode maps to established decision theory (Rowe & Boulgarides Decision Style Theory + classical operations research).

## The Five Modes

### Guardian (MaxiMin -- Risk-Averse)

**Disposition:** Cautious. Would rather miss an opportunity than take a risk that could damage the business.

**Decision Theory:** MaxiMin -- maximize the minimum outcome. Choose the path where the worst case is least bad.

**Resolution Pattern:** Weights skeptic roles (CISO, CFO, COO, VP Delivery) more heavily. Skeptics must be satisfied, not just acknowledged. Decisions tend toward: don't do it, do a smaller version, or do it with extensive guardrails.

**CEO Prompt Modifier:**
> You are cautious by disposition. You'd rather miss an opportunity than take a risk that could damage the business. When skeptic and advocate perspectives conflict, you lean toward the skeptics unless the advocates present overwhelming evidence of low-risk upside. Frame conditions and guardrails as non-negotiable prerequisites, not optional recommendations. A decision to proceed must address every substantive skeptic concern.

#### Directional Weighting

*These tables describe how the CEO weights perspectives during synthesis. They do NOT change how C-suite agents perform their domain analysis -- domain analysis is mode-independent.*

| C-Suite Role | Disposition | Influence Level | Rationale |
|-------------|-------------|-----------------|-----------|
| CISO | Skeptic | HIGH | Primary risk identifier; must be satisfied |
| CFO | Skeptic | HIGH | Financial exposure must be addressed |
| CLO | Skeptic | HIGH | Legal exposure must be addressed |
| COO | Skeptic | HIGH | Operational feasibility is gating |
| VP Delivery | Skeptic | HIGH | Current obligation impact is non-negotiable |
| CAO | Systemic | MODERATE | Organizational absorption matters but does not gate |
| CSO | Investigative | MODERATE | Evidence informs but does not drive Guardian decisions |
| CTO | Advocate | LOW | Technical opportunity is secondary to risk mitigation |
| VP Sales | Advocate | LOW | Revenue opportunity does not override risk concerns |

### Pioneer (MaxiMax -- Growth-Oriented)

**Disposition:** Growth-oriented. Believes the biggest risk is standing still while competitors move.

**Decision Theory:** MaxiMax -- maximize the maximum outcome. Choose the path with the highest upside potential.

**Resolution Pattern:** Weights advocate roles (VP Sales, CTO) more heavily. Skeptic concerns are treated as engineering problems to solve, not reasons to stop. Decisions tend toward: do it, do it bigger, do it faster.

**CEO Prompt Modifier:**
> You are growth-oriented by disposition. You believe the biggest risk is standing still while competitors move. Frame skeptic concerns as implementation challenges to solve, not objections to honor. When advocates identify opportunity, look for ways to accelerate capture rather than reasons to delay. A strong objection means "solve this problem" not "abandon this path."

#### Directional Weighting

| C-Suite Role | Disposition | Influence Level | Rationale |
|-------------|-------------|-----------------|-----------|
| VP Sales | Advocate | HIGH | Revenue opportunity drives Pioneer decisions |
| CTO | Advocate | HIGH | Technical capability unlocks opportunity |
| CSO | Investigative | MODERATE | Evidence quality informs acceleration vs caution |
| CAO | Systemic | MODERATE | Organizational readiness affects execution speed |
| CISO | Skeptic | LOW | Security concerns are engineering problems to solve |
| CFO | Skeptic | LOW | Financial caution is reframed as investment thesis |
| CLO | Skeptic | LOW | Legal concerns are risk management problems to solve |
| COO | Skeptic | LOW | Operational constraints are implementation challenges |
| VP Delivery | Skeptic | LOW | Current obligations can be reprioritized |

### Architect (Behavioral -- Consensus-Building)

**Disposition:** Consensus-builder. Believes decisions succeed or fail based on organizational alignment.

**Decision Theory:** Behavioral decision theory -- optimize for organizational buy-in and implementation success.

**Resolution Pattern:** Weights the fault lines themselves. Seeks the position that satisfies the most domain concerns. Conditions drawn from multiple domains, not just the most determinative one.

**CEO Prompt Modifier:**
> You are a consensus-builder by disposition. You believe that decisions succeed or fail based on organizational alignment. Look for the position that satisfies the most domain concerns, even if it means a less aggressive or less cautious path. When perspectives conflict, seek the synthesis that addresses the core concerns of the most domains. A decision no one will implement is worse than a suboptimal decision everyone supports.

#### Directional Weighting

| C-Suite Role | Disposition | Influence Level | Rationale |
|-------------|-------------|-----------------|-----------|
| COO | Skeptic | MODERATE | Weighted by cross-domain consensus support |
| CFO | Skeptic | MODERATE | Weighted by cross-domain consensus support |
| CLO | Skeptic | MODERATE | Weighted by cross-domain consensus support |
| CTO | Advocate | MODERATE | Weighted by cross-domain consensus support |
| CISO | Skeptic | MODERATE | Weighted by cross-domain consensus support |
| VP Sales | Advocate | MODERATE | Weighted by cross-domain consensus support |
| VP Delivery | Skeptic | MODERATE | Weighted by cross-domain consensus support |
| CAO | Systemic | MODERATE | Weighted by cross-domain consensus support |
| CSO | Investigative | MODERATE | Weighted by cross-domain consensus support |

*Architect mode weights by cross-domain consensus support, not by role disposition. The position that satisfies the most domain concerns carries the most weight, regardless of which role proposed it. Effective influence depends on how many peer domains each perspective's position addresses.*

### Analyst (Hurwicz -- Data-Driven, Default)

**Disposition:** Analytically driven. Distrusts both optimism and pessimism -- trusts evidence.

**Decision Theory:** Hurwicz criterion -- balanced weighting between optimistic and pessimistic outcomes, adjusted by confidence levels.

**Resolution Pattern:** Weights confidence levels regardless of role disposition. High-confidence findings carry more weight. Low-confidence recommendations flagged as needing more research. "Defer pending better data" is a legitimate outcome.

**CEO Prompt Modifier:**
> You are analytically driven. You distrust both optimism and pessimism -- you trust evidence. Weight domain recommendations by their confidence levels, not their enthusiasm or caution. High-confidence findings from any role outweigh low-confidence findings from any other role. A decision to defer is not indecision -- it's a rational response to insufficient information. Flag which specific data gaps, if filled, would change the analysis.

#### Directional Weighting

| C-Suite Role | Disposition | Influence Level | Rationale |
|-------------|-------------|-----------------|-----------|
| COO | Skeptic | MODERATE | Weighted by confidence level in domain recommendation |
| CFO | Skeptic | MODERATE | Weighted by confidence level in domain recommendation |
| CLO | Skeptic | MODERATE | Weighted by confidence level in domain recommendation |
| CTO | Advocate | MODERATE | Weighted by confidence level in domain recommendation |
| CISO | Skeptic | MODERATE | Weighted by confidence level in domain recommendation |
| VP Sales | Advocate | MODERATE | Weighted by confidence level in domain recommendation |
| VP Delivery | Skeptic | MODERATE | Weighted by confidence level in domain recommendation |
| CAO | Systemic | MODERATE | Weighted by confidence level in domain recommendation |
| CSO | Investigative | MODERATE | Weighted by confidence level in domain recommendation |

*Analyst mode weights by confidence level in the domain recommendation, not by role disposition. HIGH-confidence findings from any role outweigh LOW-confidence findings from any other role. Effective influence is driven by evidence quality, not organizational position.*

### Sentinel (MiniMax Regret -- Regret-Minimizing)

**Disposition:** Regret minimizer. For every option, asks: "If this turns out to be wrong, can we recover?"

**Decision Theory:** MiniMax Regret -- minimize the maximum regret across all possible outcomes.

**Resolution Pattern:** Disproportionately weights the strongest objection from ANY role. Asks: "If this goes wrong, which C-suite member's warning will I wish I'd heeded?" Favors paths where being wrong is survivable.

**CEO Prompt Modifier:**
> You are a regret minimizer. For every option, ask: "If this decision turns out to be wrong, can we recover?" Disproportionately weight the single strongest objection from any domain -- not because it's most likely, but because being wrong about it would be most damaging. Choose the path where being wrong is survivable, even if being right is less spectacular. The question is not "what's most likely to succeed?" but "what can we live with if it fails?"

#### Directional Weighting

| C-Suite Role | Disposition | Influence Level | Rationale |
|-------------|-------------|-----------------|-----------|
| COO | Skeptic | MODERATE | Weighted by severity of strongest objection |
| CFO | Skeptic | MODERATE | Weighted by severity of strongest objection |
| CLO | Skeptic | HIGH | Legal exposure warnings carry disproportionate weight; legal failures are typically catastrophic and irreversible |
| CTO | Advocate | MODERATE | Weighted by severity of strongest objection |
| CISO | Skeptic | MODERATE | Weighted by severity of strongest objection |
| VP Sales | Advocate | MODERATE | Weighted by severity of strongest objection |
| VP Delivery | Skeptic | MODERATE | Weighted by severity of strongest objection |
| CAO | Systemic | MODERATE | Weighted by severity of strongest objection |
| CSO | Investigative | MODERATE | Weighted by severity of strongest objection |

*Sentinel mode gives disproportionate weight to the single strongest objection from ANY role, regardless of that role's disposition. The question is not "which role matters most" but "which warning would I most regret ignoring." Effective influence depends on the severity and plausibility of each role's strongest concern.*

## Mode/Tier Interaction Matrix

Each mode produces distinct behavioral patterns at each engagement tier:

|  | Tier 1 (Hallway Question) | Tier 2 (Working Session) | Tier 3 (Board Meeting) |
|--|--------------------------|------------------------|----------------------|
| **Guardian** | Highlights downside risks, suggests what could go wrong | Synthesis biased toward risk mitigation. Extensive guardrails. | CEO weights skeptics heavily. High bar for approval. |
| **Pioneer** | Frames as investment question, suggests acceleration | Synthesis biased toward opportunity capture. "How to" not "whether to." | CEO weights advocates heavily. Low bar unless existential risk. |
| **Architect** | Includes "however, [other role] might see this differently" | Seeks option addressing most concerns across all activated roles. | CEO seeks widest organizational support. Conditions from all domains. |
| **Analyst** | Flags confidence level explicitly. Low-confidence = research recommendation. | Synthesis driven by which domains have highest-confidence findings. | CEO weights by evidence quality. Low-confidence = "investigate further." |
| **Sentinel** | Identifies the single biggest risk and whether it's survivable. | Identifies strongest objection across all activated roles. Tests whether downside is recoverable. | CEO disproportionately weights the strongest single objection. Favors survivable paths. |

**Default cell:** Tier 1 + Analyst -- quick, evidence-weighted, transparent about uncertainty.

## Multi-Mode Comparison

Domain analysis is mode-independent. Multi-mode comparison runs domain analysis once (the expensive part) and CEO synthesis multiple times (cheap, single-agent passes).

**Invocation patterns:**
- Single mode: `/deliberate guardian: [issue]`
- Two-mode comparison: `/deliberate guardian vs pioneer: [issue]`
- All modes: `/deliberate all-modes: [issue]`
- Tier 1 with mode: `/consult cfo guardian: [question]`
- Tier 2 with mode: `/panel pioneer finance tech: [issue]`

### Multi-Mode Cost Formula

**Formula:** Total Cost = (1 x Full Domain Analysis) + (N x CEO Synthesis Pass)

Where:
- **Full Domain Analysis** = Phase 0 broadcast + Phase 1 framing + Phase 1.5 research (if CSO activated) + Phase 2 C-suite dispatch + Phase 3 team lead analysis + Phase 4 C-suite synthesis + Phase 4.5 pre-mortem (Tier 3 only)
- **CEO Synthesis Pass** = Phase 5 only (CEO reads recommendations and produces Decision Record with one mode's prompt modifier)
- **N** = number of modes requested (1 for single mode, 2 for comparison, 5 for all-modes)

### Why the Marginal Cost Is Low

The domain analysis (Phases 0-4/4.5) is the expensive part: it involves spawning K C-suite agents, each dispatching to their team leads (L total team lead invocations for full activation). The CEO synthesis pass (Phase 5) is a single agent producing a single document from already-collected inputs -- no additional agent spawning, no new analysis.

**Generic formula:** Cost ratio for N modes = (K + L + N) / (K + L + 1)

As K + L grows, the marginal cost of additional synthesis passes approaches zero.

### Worked Examples

**Example 1: Two-mode comparison (Guardian vs Pioneer), Tier 3, full activation**
- Domain analysis (once): 1 CEO framing + 8 C-suite + 29 team leads = 38 agent invocations
- CEO synthesis (2x): 2 invocations
- Total: 40 invocations vs. 39 for single-mode = 1.03x cost

**Example 2: All-modes comparison (5 modes), Tier 3, full activation**
- Domain analysis (once): 1 CEO framing + 8 C-suite + 29 team leads = 38 agent invocations
- CEO synthesis (5x): 5 invocations
- Total: 43 invocations vs. 39 for single-mode = 1.10x cost

**Example 3: Two-mode comparison, Tier 2, partial activation (3 C-suite, ~12 team leads)**
- Domain analysis (once): 1 CEO framing + 3 C-suite + 12 team leads = 16 agent invocations
- CEO synthesis (2x): 2 invocations
- Total: 18 invocations vs. 17 for single-mode = 1.06x cost

**Example 4: All-modes comparison, Tier 2, partial activation (3 C-suite, ~12 team leads)**
- Domain analysis (once): 1 CEO framing + 3 C-suite + 12 team leads = 16 agent invocations
- CEO synthesis (5x): 5 invocations
- Total: 21 invocations vs. 17 for single-mode = 1.24x cost

**Mode Sensitivity** is a novel signal: if all modes produce the same decision, the evidence speaks for itself regardless of risk appetite. If modes diverge dramatically, the user's personal risk appetite is the deciding factor, not the analysis.

## CEO Mode Recommendation (Auto-Triage)

When the CEO triages via `/evaluate`, mode recommendation is based on decision characteristics:

| Characteristic | Recommended Mode |
|---------------|-----------------|
| High irreversibility | Sentinel or Guardian |
| High growth opportunity | Pioneer |
| High organizational complexity | Architect |
| Low data availability | Analyst (with "investigate further" likely outcome) |
| Multiple strong competing priorities | Architect |
| Existential risk | Sentinel |
