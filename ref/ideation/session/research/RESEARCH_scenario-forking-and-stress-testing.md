# Research: Scenario Forking & Organizational Stress Testing

**Requested by:** Proactive research in support of Free Thinker's second wave (Directions A and B)
**Date:** 2026-02-22

## Questions
1. Is there a formal framework for running parallel "what-if" scenarios and comparing their outcomes systematically?
2. Is there precedent for bottom-up, proactive risk/opportunity discovery (as opposed to top-down issue analysis) in multi-agent or organizational systems?

## Findings

### Part 1: Scenario Forking — Formal Frameworks

#### Scenario-Based Decision Analysis (SBDA)

The Free Thinker's "Scenario Forking Engine" maps directly to an established methodology: **Scenario-Based Decision Analysis (SBDA)**, which integrates two separate disciplines:

1. **Scenario Planning (SP)** — Constructing multiple plausible future narratives to test strategy robustness
2. **Structured Decision Making (SDM)** — Rooted in decision theory, focused on explicit assessment of expected outcomes across a set of decision alternatives

SBDA addresses a known limitation of traditional scenario planning: SP lacks "a defined structure for establishing objectives, quantifying tradeoffs, and evaluating the performance of candidate decisions to meet those objectives." By adding structured evaluation (what the Team of Teams already provides via the cascade), SBDA becomes a complete framework.

**Key methodology from the literature (Think Insights / Scenario Planning):**

Five phases:
1. **Define Scope & Time Horizon** — What are we deciding, and over what timeframe?
2. **Identify Key Drivers** — External factors (market, regulation, technology) and internal variables (capabilities, capital, talent)
3. **Collect & Analyze Data** — Gather information to assess predictability and impact
4. **Develop Scenarios** — Construct alternative futures with distinct assumptions and early warning indicators
5. **Apply & Maintain** — Test strategies under each scenario, develop contingency plans

Organizations typically develop 2-4 scenarios using one of three structures:
- **Spectrum**: Testing sensitivity around one major variable
- **Matrix**: Examining two dimensions of uncertainty simultaneously
- **Binary**: Comparing favorable vs. unfavorable outcomes

**How this maps to the Team of Teams Scenario Forking Engine:**

| SBDA Phase | Team of Teams Implementation |
|---|---|
| Define Scope | CEO frames the issue (Phase 1 — already in cascade) |
| Identify Key Drivers | CEO identifies the decision alternatives (new Phase 0.5) |
| Collect & Analyze Data | C-suite cascade runs once per fork (or once with fork-specific parameters) |
| Develop Scenarios | Each fork IS a scenario — "acquire" vs. "build" vs. "invest elsewhere" |
| Apply & Maintain | Meta-CEO comparison across fork Decision Records |

The critical design insight from SBDA: **the value is not in the individual scenarios but in the comparison.** The "Divergence Analysis" section of the Comparative Decision Record is where the real strategic insight lives — showing where forks agree (robust conclusions) and where they diverge (decisions that depend on assumptions).

#### Simulation Agent Framework (ArXiv 2505.13761)

A 2025 framework called Simulation Agent demonstrates the technical pattern the forking engine would follow:
- Users describe "what-if" scenarios in natural language
- The AI agent dynamically modifies input parameters, reruns analysis, and presents comparative results
- "Rapid scenario exploration capability" — same underlying model, different parameter sets
- Results synthesized via "JSON summaries highlighting key performance indicators"

This validates the Free Thinker's core efficiency insight: **run the expensive domain analysis once per fork, not once per mode.** The forking happens at the issue-framing level (different business alternatives), while the analysis cascade is reused machinery.

#### Cost Implications of Forking

If the standard Full Cascade costs ~$5-10 per decision:
- **3-fork scenario analysis**: ~$15-30 (3x cascade) + ~$2-3 (meta-CEO comparison) = ~$17-33
- **With routing optimization** (not all C-suite activated per fork): ~$8-20
- **With shared context** (forks share the same company profile, only the "action" parameter changes): Some cost savings from prompt caching

This is expensive but proportionate for major strategic decisions (acquisition, market entry, pivot). The key constraint: forking should be a Tier 3+ feature, never the default.

---

### Part 2: Organizational Stress Testing — Bottom-Up Discovery

#### The Concept

The Free Thinker's Direction B inverts the cascade: instead of routing a user-provided issue downward, each C-suite agent proactively identifies issues from their domain. This is an **organizational health assessment** or **proactive risk discovery** pattern.

#### Precedent in AI Agent Systems

Research on AI-augmented organizational assessment shows:

1. **Proactive vs. Reactive Paradigm Shift**: AI agent research consistently emphasizes the transition from reactive analysis (respond to presented issues) to proactive discovery (surface latent risks and opportunities). This is described as AI's "predictive capabilities" that let organizations "anticipate challenges before they happen" (Datagrid, 2025).

2. **Multi-Domain Analysis**: AI excels at "spotting patterns across numerous variables simultaneously" — this multi-dimensional analysis maps directly to having each C-suite domain independently scan for issues, then cross-referencing across domains to identify systemic patterns.

3. **Bottom-Up Pattern**: Risk Management AI Agents are described as systems designed to "identify, assess, and mitigate risks" by "leveraging advanced analytics" to "navigate complex risk landscapes." The key: they don't wait for issues to be presented — they actively scan.

#### How This Maps to Team of Teams

The Stress Test mode would work as follows:

**Input:** Company context document (financials, current projects, market position, recent changes, headcount, tech stack, etc.)

**Process (Inverted Cascade):**
1. **CEO distributes company context** to all C-suite agents (broadcast, not routing — everyone participates)
2. **Each C-suite agent, using their team lead frameworks, scans for issues in their domain:**
   - CFO: Cash flow projections, burn rate concerns, budget gaps, hidden costs
   - CISO: Security posture gaps, compliance deadlines, unaddressed vulnerabilities
   - COO: Capacity constraints, process bottlenecks, vendor dependencies
   - CTO: Technical debt, scaling risks, architecture concerns
   - VP Sales: Pipeline gaps, market shifts, competitive threats
   - VP Delivery: Resource conflicts, SLA risks, quality concerns
   - CAO: Hiring gaps, retention risks, legal exposure, policy gaps
3. **Each C-suite agent outputs a prioritized issue list** with severity ratings
4. **CEO triages and cross-references:** Identifies systemic issues (appearing across multiple domains), prioritizes, and produces the Organizational Health Report

**Output:** Not a Decision Record but an **Organizational Health Report:**
```
ORGANIZATIONAL HEALTH REPORT
Date: [timestamp]
Company Context: [summary of inputs]

CRITICAL ISSUES (Require immediate attention)
1. [Issue] — Identified by: [role(s)] — Severity: CRITICAL
   Preliminary recommendation: [1-2 sentences]
   Cross-domain implications: [which other domains are affected]

HIGH PRIORITY ISSUES
[...]

WATCH LIST (Monitor, not urgent)
[...]

OPPORTUNITIES IDENTIFIED
[...]

SYSTEMIC PATTERNS
- [Pattern spanning multiple domains]

RECOMMENDED NEXT STEPS
- "Feed Issue #1 into /deliberate for full cascade analysis"
- "Schedule CFO deep-dive on Issue #3"
```

#### The "Full Physical vs. Doctor Visit" Insight

The Free Thinker's metaphor is precise. The standard cascade is a doctor visit (you bring a complaint, they diagnose). The stress test is a full physical (the system finds what you didn't know to ask about). Both are valuable; they serve different needs:

- **Standard cascade**: Known issue, need analysis → Decision Record
- **Stress test**: No specific issue, need to discover what to worry about → Health Report → feeds back into standard cascade for specific issues

#### Key Design Consideration: Company Context Quality

The stress test is only as good as the company context input. If the user provides vague context ("we're a SaaS company"), the C-suite agents will produce generic issues. The skill should provide a **Company Context Template** that prompts for specific data points each domain needs:
- Financials: Revenue, burn rate, runway, recent fundraising
- Operations: Headcount, key projects, vendor dependencies
- Technology: Stack, known technical debt, scaling concerns
- Security: Last audit date, compliance frameworks, incident history
- Sales: Pipeline, conversion rates, key accounts, competitive landscape
- Delivery: Active projects, resource utilization, SLA performance
- Admin: Recent hires/departures, pending legal issues, policy changes

The richer the context, the more specific and actionable the stress test output.

#### Cost Implications

A stress test always activates all 7 C-suite agents (no routing optimization — the whole point is broad domain scanning). Cost: ~$5-10 per stress test (same as a Full Cascade). This is appropriate for a periodic organizational review, not a daily tool.

---

## Key Takeaways

- **Scenario Forking maps to the established SBDA framework** (Scenario-Based Decision Analysis), combining scenario planning with structured decision making. The value is in the comparison across forks, not the individual analyses.
- **The forking engine's efficiency depends on reusing the cascade machinery** with different input parameters per fork. Cost: ~$8-33 per multi-fork analysis depending on routing and number of forks.
- **Organizational Stress Testing inverts the cascade** from top-down issue analysis to bottom-up discovery. The output is an Organizational Health Report with a prioritized issue queue, not a Decision Record.
- **Stress testing requires rich company context input** — the skill should provide a Company Context Template to ensure each domain has the data it needs for meaningful scanning.
- **Both features are Tier 3+ capabilities** — they're expensive and should be reserved for strategic planning moments, not daily use. The standard cascade and direct consult tiers handle routine decisions.
- **The stress test feeds back into the standard cascade** — discovered issues can be routed into full deliberation, creating a discovery-to-decision pipeline.

## Sources
| # | Source | URL/Path | What It Contributed |
|---|--------|----------|---------------------|
| 1 | Think Insights - Scenario Planning | https://thinkinsights.net/strategy/scenario-planning | Five-phase scenario planning methodology, 2-4 scenarios, three structural approaches |
| 2 | ScienceDirect - Scenario-Based Decision Analysis | https://www.sciencedirect.com/science/article/pii/S0006320723003762 | SBDA framework integrating SP + SDM, addressing SP's limitation in structured evaluation |
| 3 | ArXiv - Simulation Agent Framework | https://arxiv.org/html/2505.13761v1 | LLM + simulation integration, parallel scenario execution via API, comparative result synthesis |
| 4 | Wikipedia - Scenario Planning | https://en.wikipedia.org/wiki/Scenario_planning | Foundational methodology reference |
| 5 | Datagrid - AI Agent Risk Assessment | https://datagrid.com/blog/ai-agent-risk-assessment | Proactive risk identification patterns, multi-domain analysis capabilities |
| 6 | Rapid Innovation - AI Risk Assessment Agents | https://www.rapidinnovation.io/post/ai-agents-for-risk-assessment | AI agent risk assessment architecture, proactive vs. reactive paradigm |
| 7 | Cambridge Core - Parallel World Framework | https://www.cambridge.org/core/journals/data-centric-engineering/article/parallel-world-framework-for-scenario-analysis-in-knowledge-graphs/ | Parallel scenario analysis in knowledge graphs |
| 8 | ResearchGate - Combining SP and MCDA | https://www.researchgate.net/publication/227499698 | Integration of scenario planning with multi-criteria decision analysis |

## Citation Log
- Search: `multi-agent scenario analysis parallel simulation decision comparison framework AI 2025 2026`
- Search: `scenario planning comparison parallel analysis decision theory multiple alternatives evaluate side by side framework`
- Search: `organizational health assessment proactive risk identification multi-domain business diagnostic AI agent`
- Search: `LLM organizational risk assessment proactive threat discovery bottom-up analysis agent 2025`
- Fetched: https://thinkinsights.net/strategy/scenario-planning
- Fetched: https://arxiv.org/html/2505.13761v1
- Fetched (403 blocked): https://www.sciencedirect.com/science/article/pii/S0006320723003762
