# Research: Cross-Functional Agent Debate -- Quality vs. Cost Tradeoffs

**Requested by:** Free-thinker's Phase 4.5 question (should C-suite agents challenge each other before CEO synthesis?)
**Date:** 2026-02-22

## Question
Should the design include a cross-functional deliberation phase where C-suite agents debate each other's recommendations? What does research say about the quality improvement vs. complexity/cost tradeoff of multi-agent debate rounds?

## Findings

### The Surprising Research Consensus: More Rounds Hurt, More Agents Help

Recent research (2025-2026) on multi-agent debate (MAD) in LLM systems reveals counterintuitive findings that directly affect the Phase 4.5 design question:

**Finding 1: More discussion rounds REDUCE performance.**
Increasing the number of debate rounds between agents does not reliably improve accuracy. Researchers attribute this to "problem drift" -- agents gradually drift from the original task during extended exchanges. This finding contradicts the intuition that more debate = better decisions.

**Finding 2: More agents (horizontal scaling) IMPROVES performance.**
Increasing the number of participating agents shows a consistent upward trend in accuracy. The recommendation: **scale horizontally (add agents) rather than vertically (extend discussions).**

**Finding 3: Token cost scales dramatically with debate rounds.**
- 3 agents, 5 rounds: **101x token cost** for a potential accuracy improvement from 50% to 98% on simple arithmetic
- 4 agents, 5 rounds: **90x token cost** for an improvement from 76% to 88% on GSM8K math
- Most MAD methods fail to outperform simpler single-agent techniques like Self-Consistency (which simply resamples)

**Finding 4: Independent drafting before interaction is critical.**
Two methods that enforce independent initial analysis BEFORE any cross-agent communication significantly improve quality:
- "All-Agents Drafting" (forces independent solutions first): +3.3% improvement
- "Collective Improvement" (restricts communication, shows solutions each round): +7.4% improvement

Both prevent agents from immediately converging on the first proposal they see.

**Finding 5: Heterogeneous agents produce the best results.**
Mixing different model types (e.g., GPT-4o-mini with Llama 3.1-70b) produces significant improvements over homogeneous agents. In the Team of Teams context, this means using different model tiers for different roles could actually improve decision quality.

**Finding 6: Consensus works for knowledge tasks; Voting works for reasoning tasks.**
- Consensus protocols improve knowledge tasks by 2.8% (error-checking, hallucination reduction)
- Voting protocols improve reasoning tasks by 13.2% (exploring multiple reasoning paths)

### What This Means for Phase 4.5

The research strongly suggests the following design:

#### DO: Independent Analysis First (Already in the Cascade)
The existing cascade design (Phases 1-4) already implements the most important pattern: **each C-suite agent produces an independent analysis BEFORE seeing others' work.** This is equivalent to "All-Agents Drafting" and is the single most important factor for decision quality.

#### DO: One Structured Challenge Round (Not Extended Debate)
If there is a cross-functional phase, it should be **exactly one round** -- not an extended back-and-forth debate. Research shows:
- One round of cross-critique captures most of the value
- Additional rounds cause problem drift and reduce quality
- The challenge phase should be structured (specific questions to answer about each other's analysis) not open-ended debate

#### DO: Make the Challenge Phase Targeted, Not Universal
Not every C-suite agent needs to challenge every other agent. Use the natural tension pairings:
- CFO reviews VP Sales' revenue projections (cost reality check)
- CISO reviews CTO's technical proposal (security challenge)
- VP Delivery reviews VP Sales' promises (capacity check)
- COO reviews overall feasibility

This is McChrystal's "fusion cell" -- focused cross-functional interaction, not a free-for-all.

#### DON'T: Allow Extended Multi-Round Debate
Multiple rounds of C-suite agents arguing back and forth will:
- Cost 90-100x more tokens
- Cause problem drift (agents forget the original question)
- Likely underperform the simpler approach of independent analysis + CEO synthesis
- Risk "consensus mush" where agents converge to agreeable positions

#### DON'T: Use Consensus as the Decision Protocol
The CEO should NOT seek consensus among C-suite agents. Research shows:
- For reasoning-heavy decisions (strategy, trade-offs): **Voting/weighting is better** than consensus
- Consensus causes agents to suppress genuine disagreement
- The CEO's job is to synthesize competing perspectives, not find the middle ground

### Recommended Phase 4.5 Design

Based on the research, here is the recommended cross-functional interaction design:

```
Phase 4: C-Suite Upward Synthesis (each agent produces independent recommendation)
    |
Phase 4.5: Targeted Cross-Critique (ONE round, structured)
    |  - Each C-suite agent receives a SUMMARY of other agents' recommendations
    |  - Each agent answers: "What risks or blind spots do you see in the other recommendations?"
    |  - Each agent can REVISE their own recommendation based on what they learned
    |  - NO back-and-forth debate -- one round only
    |
Phase 5: CEO Deliberation (receives original + revised recommendations)
```

Key implementation details:
- C-suite agents see **summaries** of other recommendations, not full analyses (reduces token cost)
- The critique question is **structured**: "What did the other departments miss?" not "do you agree?"
- Agents can **revise** their own recommendation after seeing others' work (captures the value of cross-pollination)
- The CEO receives **both** the original and revised recommendations (can see what changed and why)

### Token Cost Estimate for Phase 4.5

Without Phase 4.5: 7 independent C-suite analyses + CEO synthesis = ~8 agent turns
With Phase 4.5: 7 analyses + 7 cross-critiques + 7 revisions + CEO synthesis = ~22 agent turns

This roughly triples the C-suite layer cost. Whether this is worthwhile depends on whether the user opts for "thorough" vs. "quick" analysis mode. The design should make Phase 4.5 **optional** -- a configuration toggle.

## Key Takeaways
- **The existing cascade design (independent analysis first) is already implementing the highest-value pattern** from multi-agent research. Don't lose this.
- **One structured cross-critique round is valuable; extended debate is harmful.** Problem drift and token cost make multi-round debate counterproductive.
- **Phase 4.5 should be optional** -- a "thorough mode" toggle. Quick mode skips it; thorough mode includes one round of targeted cross-critique.
- **The CEO should use weighted synthesis, not consensus.** Suppress genuine disagreement and you lose the whole point.
- **Heterogeneous model tiers (Haiku for team leads, Sonnet for C-suite, Opus for CEO) could actually improve decision quality**, not just save cost. Research shows model diversity helps.

## Sources
| # | Source | URL/Path | What It Contributed |
|---|--------|----------|---------------------|
| 1 | ICLR 2025 - Multi-LLM-Agent Debate Performance | https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/ | MAD underperforms simpler methods, token cost multiplier, heterogeneous agents |
| 2 | ACL 2025 - Voting or Consensus in MAD | https://arxiv.org/html/2502.19130v4 | More rounds reduce performance, more agents help, AAD/CI methods, task-type protocols |
| 3 | GroupDebate (arXiv 2409.14051) | https://arxiv.org/html/2409.14051 | Efficient debate architecture, forget mechanism for token reduction |
| 4 | Sparse Communication in MAD (arXiv 2406.11776) | https://arxiv.org/html/2406.11776v1 | Sparse communication matches/exceeds full debate at lower cost |
| 5 | Improving Factuality with Multiagent Debate | https://composable-models.github.io/llm_debate/ | Original MAD framework, ensemble effects |
| 6 | EmergentMind - MAD Paradigm | https://www.emergentmind.com/topics/multi-agent-debate-mad-paradigm | MAD overview, strategy comparisons |

## Citation Log
- Search: `multi-agent debate deliberation rounds quality improvement token cost tradeoff LLM AI agents 2025 2026`
- Search: `multi-agent debate consensus AI improve decision quality research rounds of discussion convergence`
- Fetched: https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/
- Fetched: https://arxiv.org/html/2502.19130v4
