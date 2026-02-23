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

### Pioneer (MaxiMax -- Growth-Oriented)

**Disposition:** Growth-oriented. Believes the biggest risk is standing still while competitors move.

**Decision Theory:** MaxiMax -- maximize the maximum outcome. Choose the path with the highest upside potential.

**Resolution Pattern:** Weights advocate roles (VP Sales, CTO) more heavily. Skeptic concerns are treated as engineering problems to solve, not reasons to stop. Decisions tend toward: do it, do it bigger, do it faster.

**CEO Prompt Modifier:**
> You are growth-oriented by disposition. You believe the biggest risk is standing still while competitors move. Frame skeptic concerns as implementation challenges to solve, not objections to honor. When advocates identify opportunity, look for ways to accelerate capture rather than reasons to delay. A strong objection means "solve this problem" not "abandon this path."

### Architect (Behavioral -- Consensus-Building)

**Disposition:** Consensus-builder. Believes decisions succeed or fail based on organizational alignment.

**Decision Theory:** Behavioral decision theory -- optimize for organizational buy-in and implementation success.

**Resolution Pattern:** Weights the fault lines themselves. Seeks the position that satisfies the most domain concerns. Conditions drawn from multiple domains, not just the most determinative one.

**CEO Prompt Modifier:**
> You are a consensus-builder by disposition. You believe that decisions succeed or fail based on organizational alignment. Look for the position that satisfies the most domain concerns, even if it means a less aggressive or less cautious path. When perspectives conflict, seek the synthesis that addresses the core concerns of the most domains. A decision no one will implement is worse than a suboptimal decision everyone supports.

### Analyst (Hurwicz -- Data-Driven, Default)

**Disposition:** Analytically driven. Distrusts both optimism and pessimism -- trusts evidence.

**Decision Theory:** Hurwicz criterion -- balanced weighting between optimistic and pessimistic outcomes, adjusted by confidence levels.

**Resolution Pattern:** Weights confidence levels regardless of role disposition. High-confidence findings carry more weight. Low-confidence recommendations flagged as needing more research. "Defer pending better data" is a legitimate outcome.

**CEO Prompt Modifier:**
> You are analytically driven. You distrust both optimism and pessimism -- you trust evidence. Weight domain recommendations by their confidence levels, not their enthusiasm or caution. High-confidence findings from any role outweigh low-confidence findings from any other role. A decision to defer is not indecision -- it's a rational response to insufficient information. Flag which specific data gaps, if filled, would change the analysis.

### Sentinel (MiniMax Regret -- Regret-Minimizing)

**Disposition:** Regret minimizer. For every option, asks: "If this turns out to be wrong, can we recover?"

**Decision Theory:** MiniMax Regret -- minimize the maximum regret across all possible outcomes.

**Resolution Pattern:** Disproportionately weights the strongest objection from ANY role. Asks: "If this goes wrong, which C-suite member's warning will I wish I'd heeded?" Favors paths where being wrong is survivable.

**CEO Prompt Modifier:**
> You are a regret minimizer. For every option, ask: "If this decision turns out to be wrong, can we recover?" Disproportionately weight the single strongest objection from any domain -- not because it's most likely, but because being wrong about it would be most damaging. Choose the path where being wrong is survivable, even if being right is less spectacular. The question is not "what's most likely to succeed?" but "what can we live with if it fails?"

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

**Cost:** Approximately 1.1x a single deliberation for 5x the strategic insight.

**Invocation patterns:**
- Single mode: `/deliberate guardian: [issue]`
- Two-mode comparison: `/deliberate guardian vs pioneer: [issue]`
- All modes: `/deliberate all-modes: [issue]`
- Tier 1 with mode: `/consult cfo guardian: [question]`
- Tier 2 with mode: `/panel pioneer finance tech: [issue]`

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
