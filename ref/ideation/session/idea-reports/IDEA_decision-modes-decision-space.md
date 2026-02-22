# Idea Report: Decision Modes and the Decision Space Map

**Direction explored by:** Free Thinker + Grounder
**Report number:** 04
**Related threads:** Cascade architecture (Report #1), Engagement Model (Report #2), CEO personality thread, mode/tier matrix exploration

---

## The Idea

The Team of Teams skill should not produce a single recommendation — it should reveal a **decision space**. The same domain analysis (C-suite findings, team lead outputs, fault lines) can be synthesized through multiple **Decision Modes** — configurable lenses that change how the CEO agent weighs and resolves competing perspectives without changing the underlying analysis. By running the same inputs through different synthesis styles, the user sees not "what to do" but "what the terrain looks like in every direction" — and can make an informed choice about which kind of decision-maker they want to be for this particular issue.

The five Decision Modes are: **Guardian** (protect what we have), **Pioneer** (pursue what we could gain), **Architect** (build the widest organizational alignment), **Analyst** (follow the evidence, defer where evidence is weak), and **Sentinel** (minimize regret on irreversible decisions). Each maps to established decision theory frameworks. Each mode is implemented as a swappable prompt modifier in the CEO agent's synthesis layer, leaving the domain analysis pipeline completely unchanged.

The power move is **multi-mode comparison**: the user requests a deliberation that runs domain analysis once (the expensive part), then feeds the same findings through two or more CEO synthesis modes (lightweight passes). The output is a **Comparative Decision Record** — a side-by-side view showing how the same evidence produces different decisions depending on the synthesis lens. This transforms the skill from a decision engine into a **decision exploration tool**.

## The Key Insight

The most useful output of a multi-perspective analysis isn't a single answer — it's a map showing **how the answer changes depending on what you optimize for**. Decision Modes make the user's implicit risk appetite and strategic posture explicit and visible, turning a binary "do this / don't do this" into a nuanced "here's what each path looks like."

## How We Got Here

The Free Thinker proposed "CEO Personalities" in the opening salvo — the idea that different CEO decision-making styles could produce different outcomes from identical analysis. The Grounder elevated this beyond a "fun variant" by identifying the core insight: it solves a real problem. Users often don't know what kind of decision-maker they want to be on a given issue. Showing the conservative path alongside the aggressive path alongside the balanced path gives them the decision space — what they're actually choosing between. The Free Thinker then developed this into four concrete modes with CEO prompt modifiers, mapped the mode/tier interaction matrix, and designed the multi-mode comparison mechanism.

## The Grounder's Take

- **Does this connect to what was asked for?** Yes, with a twist. The concept seed asks for a skill that "makes decisions and answers questions." Decision Modes make the skill's decisions more valuable by showing the user that the "right" answer depends on their strategic posture — and giving them the tools to explore that dependency. It's a direct enhancement to the Decision Record output.
- **Would the audience care?** This is the feature that would make a founder say "this is actually useful, not just impressive." Solo founders and small leadership teams constantly face the question "am I being too cautious or too aggressive?" Decision Modes make that question answerable by showing both paths side by side.
- **Is this one of the good ones?** Yes. It's the feature that differentiates this skill from "ask a panel of AI experts." Panels give you one answer. This gives you the shape of the decision landscape.

## The Free Thinker's Vision

At its most ambitious, Decision Modes become **strategic profiles** that accumulate over time. A user who consistently picks the Growth mode synthesis learns something about their own decision-making tendencies. The system could surface patterns: "You've chosen the growth-oriented path in 8 of the last 10 decisions. Your CFO's concerns were overridden 6 times. Consider whether the conservative perspective is being systematically underweighted." That's not just decision support — it's leadership coaching.

Further out: custom Decision Modes. A user could define their own synthesis posture: "I'm generally growth-oriented but conservative on anything involving regulatory risk." The CEO's synthesis prompt becomes a user-configurable profile that represents their actual leadership style.

## Architecture Detail: The Four Decision Modes

### Mode 1: Guardian (Conservative / Risk-Averse)

**Strategic posture:** Protect what we have. The downside matters more than the upside.

**CEO synthesis behavior:**
- Weights skeptic roles (CISO, CFO, COO, VP Delivery) more heavily
- Threshold for accepting risk is high — skeptics must be satisfied, not just acknowledged
- Dissenting views from advocates are preserved but the bar for overriding skeptics is steep
- Decisions tend toward: don't do it, do a smaller version, do it with extensive guardrails

**CEO prompt modifier:**
```
DECISION MODE: CONSERVATIVE
You are cautious by disposition. You'd rather miss an opportunity than take
a risk that could damage the business. When skeptic and advocate perspectives
conflict, you lean toward the skeptics unless the advocates present
overwhelming evidence of low-risk upside. Your decision should reflect what
a prudent steward of the business would do, prioritizing stability,
predictability, and downside protection.
```

### Mode 2: Pioneer (Growth / Aggressive)

**Strategic posture:** Pursue what we could gain. Standing still is the biggest risk.

**CEO synthesis behavior:**
- Weights advocate roles (VP Sales, CTO) more heavily
- Skeptic concerns are treated as engineering problems to solve, not reasons to stop
- The synthesis looks for "how do we capture this opportunity?" not "should we?"
- Decisions tend toward: do it, do it bigger, do it faster

**CEO prompt modifier:**
```
DECISION MODE: GROWTH
You are growth-oriented by disposition. You believe the biggest risk is
standing still while competitors move. When skeptic and advocate perspectives
conflict, you look for ways to capture the opportunity while mitigating the
risks, rather than letting the risks kill the opportunity. Frame skeptic
concerns as implementation challenges to solve, not objections to honor.
Your decision should reflect what an ambitious, forward-leaning leader would do.
```

### Mode 3: Architect (Consensus / Collaborative)

**Strategic posture:** Find the path with widest organizational alignment. Decisions succeed on buy-in.

**CEO synthesis behavior:**
- Weights the fault lines themselves — looks for positions that address the most objections
- The synthesis seeks the option that satisfies the most domain concerns
- Decisions may be less bold but have broader organizational support
- Conditions drawn from multiple domains, not just the most determinative one

**CEO prompt modifier:**
```
DECISION MODE: CONSENSUS
You are a consensus-builder by disposition. You believe that decisions
succeed or fail based on organizational alignment. When perspectives
conflict, you look for the position that satisfies the most domain
concerns, even if it means a less aggressive or less cautious path than
any single role would recommend. Your decision should reflect what a
collaborative leader would do — finding common ground without sacrificing
strategic intent.
```

### Mode 4: Analyst (Analytical / Data-Driven)

**Strategic posture:** Follow the evidence. Defer where evidence is weak.

**CEO synthesis behavior:**
- Weights confidence levels — high-confidence findings carry more weight regardless of source
- Low-confidence recommendations get flagged as areas needing more research
- The synthesis is driven by "where do we have the best information?" not "what do we want to be true?"
- Decisions may include "defer pending better data on X" as a legitimate outcome

**CEO prompt modifier:**
```
DECISION MODE: ANALYTICAL
You are analytically driven. You distrust both optimism and pessimism —
you trust evidence. Weight domain recommendations by their confidence
levels, not their enthusiasm or caution. Where confidence is low,
recommend further research before committing. A decision to defer is not
indecision — it's a rational response to insufficient information.
The quality of the analysis matters more than the direction of the
recommendation.
```

### Mode 5: Sentinel (Regret Minimizer / MiniMax Regret)

**Strategic posture:** Which decision can I defend regardless of outcome? Minimize the worst possible regret.

**CEO synthesis behavior:**
- Disproportionately weights the strongest objection from ANY role, regardless of that role's disposition
- The synthesis asks: "If this goes wrong, which C-suite member's warning will I wish I'd heeded?"
- Decisions favor paths where the downside of being wrong is survivable, even if the upside of being right is smaller
- Particularly suited to irreversible decisions (acquisitions, layoffs, market exits)

**CEO prompt modifier:**
```
DECISION MODE: SENTINEL
You are a regret minimizer. For every option, ask: "If this decision turns
out to be wrong, can we recover?" Disproportionately weight the single
strongest objection from any domain — that objection represents your worst
case. Choose the path where being wrong is survivable, even if being right
is less spectacular. Your decision should reflect what a leader who must
answer to a board regardless of outcome would do.
```

*Note: The five modes map to established decision theory (Rowe & Boulgarides Decision Style Theory + classical operations research): Guardian = MaxiMin, Pioneer = MaxiMax, Architect = Behavioral, Analyst = Hurwicz balanced, Sentinel = MiniMax Regret.*

## The Mode/Tier Interaction Matrix

Decision Modes interact with the three Interaction Tiers (from Report #2) to produce distinct behavioral patterns:

|  | Tier 1 (Direct Consult) | Tier 2 (Focused Panel) | Tier 3 (Full Deliberation) |
|--|------------------------|----------------------|---------------------------|
| **Guardian** | CFO gives cautious answer, highlights downside risks, suggests what could go wrong | 3-4 C-suite, synthesis biased toward risk mitigation. Extensive guardrails. | Full cascade, CEO weights skeptics heavily. High bar for approval. |
| **Pioneer** | CFO frames it as investment question, identifies how to fund it, suggests acceleration | Same panel, synthesis biased toward opportunity capture. "How to" not "whether to." | Full cascade, CEO weights advocates heavily. Low bar unless existential risk. |
| **Architect** | Single agent response includes "however, [other role] might see this differently — consider escalating" | Panel seeks option addressing most concerns across all activated roles. | Full cascade, CEO seeks widest organizational support. Conditions from all domains. |
| **Analyst** | Agent flags confidence level explicitly. Low-confidence answers come with research recommendations. | Synthesis driven by which domains have highest-confidence findings. | Full cascade, CEO weights by evidence quality. Low-confidence = "investigate further." |
| **Sentinel** | Agent identifies the single biggest risk and whether it's survivable. "You can do this, but if X goes wrong, here's what happens." | Panel identifies the strongest objection across all activated roles and tests whether the downside is recoverable. | Full cascade, CEO disproportionately weights the strongest single objection. Favors survivable paths. |

**The default cell** for most users, most of the time: **Tier 1 + Analyst**. Quick, evidence-weighted, transparent about uncertainty.

## The Multi-Mode Comparison Mechanism

**Invocation:** `/deliberate conservative vs growth: should we acquire CompetitorX?`

**Process:**
1. CEO frames the issue and routes to relevant C-suite members (standard Phase 0-1)
2. Full domain analysis cascade runs once (Phases 2-4) — this is the expensive part
3. CEO receives all domain recommendations, fault lines, and team lead findings
4. CEO runs synthesis **multiple times** — once per requested mode (lightweight, same input)
5. Output: **Comparative Decision Record**

**Comparative Decision Record structure:**
```
COMPARATIVE DECISION RECORD: [Issue Title]
Decision ID: [auto-generated]
Modes Compared: [list]

EXECUTIVE SUMMARY
[One paragraph per mode showing how the decision differs]

SHARED ANALYSIS
[Domain analyses are identical across modes — presented once]
[Fault Line Analysis — presented once]

MODE COMPARISONS

  CONSERVATIVE SYNTHESIS:
    Decision: [statement]
    Most Determinative Perspective: [role + why]
    Key Factor: [what tipped this mode's decision]
    Conditions: [guardrails]

  GROWTH SYNTHESIS:
    Decision: [statement]
    Most Determinative Perspective: [role + why]
    Key Factor: [what tipped this mode's decision]
    Conditions: [guardrails]

  [repeat for each requested mode]

DIVERGENCE ANALYSIS
  Where Modes Agree: [decisions all modes reached]
  Where Modes Diverge: [the pivot points — what makes the difference]
  The Key Choice: [what the user is actually deciding between — not
    the business question, but the values/priorities question underneath it]

METADATA
  [standard metadata]
  Mode Sensitivity: [how much does the decision change across modes?
    High sensitivity = the decision depends heavily on risk appetite.
    Low sensitivity = all modes converge on the same answer.]
```

**Why Mode Sensitivity matters:** If all four modes produce the same decision, that's a strong signal — the right answer doesn't depend on your posture. If the modes diverge dramatically, the user knows this is a decision where their personal risk appetite is the deciding factor, not the analysis.

## The Invocation Grammar for Decision Modes

Modes integrate with the invocation grammar from Report #2:

- **Default (no mode specified):** Analyst mode. `/deliberate: should we acquire CompetitorX?`
- **Single mode:** `/deliberate guardian: should we acquire CompetitorX?`
- **Multi-mode comparison:** `/deliberate guardian vs pioneer: should we acquire CompetitorX?`
- **All modes:** `/deliberate all-modes: should we acquire CompetitorX?`
- **Tier 1 with mode:** `Ask the CFO as guardian — can we afford this?`
- **Tier 2 with mode:** `/panel pioneer finance tech: should we build this feature?`

The CEO agent parses the mode specification from the invocation and applies the appropriate synthesis modifier(s).

## Cost Efficiency of Multi-Mode Comparison

The key efficiency insight: domain analysis is mode-independent. Running a 4-mode comparison costs approximately:
- 1x full cascade (domain analysis) — the expensive part
- 4x CEO synthesis pass (lightweight, single-agent) — cheap
- Total cost: approximately 1.1x a single full deliberation, producing 4x the strategic insight

This makes multi-mode comparison dramatically more valuable per token than running four separate deliberations.

## Open Threads

- **Custom Decision Modes:** Can users define their own synthesis postures beyond the four defaults? "Growth-oriented but conservative on regulatory risk."
- **Mode Recommendation:** Should the CEO auto-suggest which mode is most appropriate for the decision type? "This is a high-stakes irreversible decision — I recommend Conservative or All-Modes."
- **Decision Pattern Analysis:** Over time, can the system surface patterns in which modes the user selects? "You've overridden the CFO in 6 of 8 decisions — consider running the next one in Conservative mode."
- **Mode Calibration:** How do you ensure modes produce meaningfully different outputs rather than slight variations? The prompt modifiers need to be distinct enough to shift synthesis behavior.

## Recommendation to Arbiter

**Recommended as an important enhancement to the core spec.** Decision Modes transform the skill from a decision engine into a decision exploration tool — arguably the more valuable framing. The multi-mode comparison is cost-efficient (1.1x cost for 4x insight) and produces the "decision space map" that no single-mode analysis can offer. The Mode Sensitivity metric in the Comparative Decision Record is a novel signal that tells the user whether their decision depends on strategy or evidence.

This report builds directly on Report #1 (the cascade produces the analysis that modes synthesize differently) and Report #2 (the invocation grammar and tier system integrate with mode selection). Together with Report #3 (cognitive forcing ensures the domain analysis is high-quality), the four reports form a complete design vision: architecture, experience, quality, and strategic depth.
