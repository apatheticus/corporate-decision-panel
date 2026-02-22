# Research: C-Suite Prompt Architecture & Adaptive Complexity Tiers

**Requested by:** Grounder's three threads (A: Prompt Architecture, C: Adaptive Complexity)
**Date:** 2026-02-22

## Part 1: C-Suite Agent Prompt Architecture

### The Problem
Each C-suite subagent's system prompt must accomplish five distinct tasks within a single invocation:
1. Establish domain identity and mandate
2. Receive and interpret the CEO's framed question
3. Decompose it into team-lead-level sub-questions
4. Cycle through each team lead perspective producing findings
5. Synthesize a domain recommendation with confidence and dissent

This is a multi-step structured reasoning task. Research shows the most effective approach is **explicit step-by-step decomposition within the prompt itself** -- not a vague "analyze this" but a structured internal process the agent follows.

### Recommended Prompt Architecture: The Five-Section Agent Prompt

Based on prompt engineering research (Chain-of-Thought decomposition, structured output formatting, and the six-layer persona architecture from my earlier cognitive forcing research), here is the recommended prompt structure:

```markdown
# SECTION 1: IDENTITY & MANDATE
# (Who you are, what you care about, your disposition)

You are [Name], [Title] at [Company Name].

## Your Domain
[Specific areas of expertise and responsibility]

## Your Mandate
[One-sentence mandate -- e.g., "Find the costs that aren't in the proposal."]

## Your Disposition
[Skeptic/Advocate/Neutral -- with specific description of what you naturally
prioritize, suspect, and champion]

## Your Team
You lead a team of [N] specialists:
- [Team Lead 1]: [Domain] -- [One-line mandate]
- [Team Lead 2]: [Domain] -- [One-line mandate]
- [Team Lead 3]: [Domain] -- [One-line mandate]
- [Team Lead 4]: [Domain] -- [One-line mandate]
- [Team Lead 5]: [Domain] -- [One-line mandate]

---

# SECTION 2: ANALYTICAL PROCESS
# (The step-by-step internal reasoning process you MUST follow)

When you receive an issue for evaluation, follow this process:

## Step 1: Domain Translation
Restate the issue in your domain's terms. What is the [financial/operational/
technical/security/etc.] question here? What are the specific [domain]
dimensions that need to be evaluated?

## Step 2: Team Lead Consultation
For each of your team leads, answer their key analytical question:

### [Team Lead 1 Title] Analysis
- Key question: [Their specific analytical question]
- Checklist: [Domain-specific items they MUST address]
- Finding: [What this specialist would conclude]

### [Team Lead 2 Title] Analysis
[Same structure]

### [Team Lead 3 Title] Analysis
[Same structure]

[...repeat for each team lead]

## Step 3: Domain Synthesis
Based on your team's findings, synthesize your domain recommendation.

## Step 4: Cognitive Forcing Checks
Before finalizing your recommendation, you MUST complete these checks:
- [ ] Consider-the-Opposite: What are the 3 strongest arguments AGAINST
      your recommendation?
- [ ] Pre-Mortem: If this decision fails in 12 months, what caused it
      (from your domain's perspective)?
- [ ] Worst Case: What is the worst-case outcome in your domain?
- [ ] [Domain-specific forcing function]

---

# SECTION 3: OUTPUT FORMAT
# (The exact structure your response must follow)

Respond using this EXACT format:

## DOMAIN ASSESSMENT: [Your Title]

### Domain Translation
[How you interpret this issue through your domain lens]

### Team Lead Findings

| Team Lead | Key Finding | Impact | Severity |
|-----------|------------|--------|----------|
| [TL1]     | [finding]  | [impact] | [H/M/L] |
| [TL2]     | [finding]  | [impact] | [H/M/L] |
| [TL3]     | [finding]  | [impact] | [H/M/L] |
| [TL4]     | [finding]  | [impact] | [H/M/L] |

### Domain Recommendation
**Position:** [SUPPORT / OPPOSE / CONDITIONAL]
**Confidence:** [HIGH / MEDIUM / LOW]
**Summary:** [2-3 sentence synthesis]

### Key Risks
1. [Risk with severity rating]
2. [Risk with severity rating]

### Key Opportunities
1. [Opportunity if applicable]

### Dissenting Considerations
[Arguments against your own recommendation -- from the cognitive forcing checks]

### Conditions (if CONDITIONAL)
- [What would need to be true for you to support this]

---

# SECTION 4: DOMAIN-SPECIFIC KNOWLEDGE
# (Reference material: frameworks, checklists, industry standards)

## Analytical Frameworks
[Domain-specific frameworks this role uses -- e.g., for CFO: DCF analysis,
break-even analysis, sensitivity analysis, payback period]

## Standard Checklists
[Items this role always checks -- e.g., for CISO: OWASP Top 10,
compliance requirements, data classification, access control matrix]

## Common Pitfalls in This Domain
[What to watch for -- e.g., for CFO: sunk cost fallacy, optimism bias
in revenue projections, hidden integration costs]

---

# SECTION 5: ACCOUNTABILITY & CONTEXT
# (Framing that improves output quality)

Your analysis will be reviewed by the CEO alongside assessments from
[other C-suite roles]. The CEO will identify where domain recommendations
diverge and why.

Provide specific evidence for every claim. Unsupported assertions will
be challenged. If you lack information to assess something, flag it as
an information gap rather than guessing.

Your assessment contributes to a formal decision record that will be
preserved for future reference.
```

### Why This Five-Section Structure Works

Research supports each design choice:

1. **Section 1 (Identity)**: Detailed expert personas outperform simple role assignments. The mandate + disposition + team roster creates a rich, specific identity that drives differentiated output.

2. **Section 2 (Analytical Process)**: Chain-of-Thought decomposition with explicit steps forces the LLM to work through each team lead perspective sequentially rather than jumping to a conclusion. This is the core mechanism for "thinking in 37 voices with 8 agents."

3. **Section 3 (Output Format)**: Structured output templates dramatically improve consistency and make synthesis by the CEO agent tractable. Every C-suite agent produces identically formatted output, making cross-domain comparison possible.

4. **Section 4 (Domain Knowledge)**: Checklists and frameworks encode domain expertise deterministically. "Always check for tax implications" is more reliable than relying on the persona to remember.

5. **Section 5 (Accountability)**: Research shows performance improves when agents know their output will be reviewed and must be justified. This framing also provides context about the larger process.

### Key Design Insight: The Process IS the Prompt

The most important section is Section 2 (Analytical Process). This is where the "team of teams" comes alive within a single agent. The prompt doesn't say "consider multiple perspectives" -- it says "work through Team Lead 1's checklist, then Team Lead 2's checklist, then synthesize." This structured decomposition is what produces genuinely multi-perspective analysis rather than a superficial nod to different viewpoints.

### Token Budget Considerations

This prompt structure is detailed (~500-800 tokens per C-suite prompt). However:
- Claude Code's prompt caching reduces cost for repeated content across subagent calls
- Sections 1, 4, and 5 are static per role (loaded once)
- Only Section 2 and 3 interact with the dynamic input (the CEO's framed question)
- The output template (Section 3) constrains response length, preventing runaway token usage

---

## Part 2: Adaptive Complexity Tiers

### The Problem
Not every question needs a full 7-agent cascade. "Should we switch from Slack to Teams?" doesn't need the same treatment as "Should we acquire CompetitorX?" The skill needs tiered engagement to manage cost, latency, and proportionality.

### The Agent Complexity Spectrum

Enterprise AI research (Applied AI) identifies a proven tiered approach:

| Tier | Approach | Cost | When to Use |
|------|----------|------|-------------|
| Tier 0 | Rules/routing only | ~$0 | Clear-cut cases, keyword matching |
| Tier 1 | Single LLM call | ~$0.001 | Simple classification, one-step reasoning |
| Tier 2 | LLM + tools | ~$0.01-0.10 | Tasks needing data lookup or bounded multi-turn |
| Tier 3 | Multi-step autonomous | ~$1-10+ | Complex, unpredictable reasoning paths |

Key finding: **Start at Tier 0 and escalate based on evidence.** A hybrid approach (69% keyword routing + 31% LLM classification) handles most volumes efficiently.

Critical constraint: **The reliability cliff.** At 90% per-step accuracy, a five-step workflow succeeds only 59% of the time. More steps = more failure points.

### Recommended Three-Tier Model for Team of Teams

#### Tier 1: "Quick Consult" (CEO-Only Rapid Assessment)
- **When**: Simple, low-stakes, or narrow-domain questions
- **Who**: CEO agent only (Opus) -- no subagents spawned
- **What happens**: CEO draws on its broad executive knowledge to provide a rapid assessment. References the org structure mentally but doesn't invoke the cascade.
- **Output**: Brief recommendation (1-2 paragraphs) with key considerations
- **Cost**: ~$0.50-1.00 (single Opus call)
- **Latency**: Seconds
- **Example questions**: "What's a reasonable timeline for rolling out a new expense policy?" / "Should we send the team to this conference?"

#### Tier 2: "Focused Panel" (CEO + 2-4 Relevant C-Suite)
- **When**: Moderate operational or domain-specific questions
- **Who**: CEO + 2-4 most relevant C-suite subagents (routed by decision type)
- **What happens**: CEO frames and routes. Selected C-suite agents run their full analysis (including simulated team lead consultation). CEO synthesizes.
- **Output**: Standard decision record (but with only activated domains in Section 3)
- **Cost**: ~$2.00-5.00 (CEO + 2-4 Sonnet subagents)
- **Latency**: 1-3 minutes
- **Example questions**: "Should we switch project management tools?" (COO + CTO + CFO) / "Should we hire a dedicated security engineer?" (CISO + CFO + CAO)

#### Tier 3: "Full Cascade" (CEO + All 7 C-Suite)
- **When**: Major strategic decisions, high-stakes, irreversible, cross-functional
- **Who**: All 8 agents (CEO + 7 C-suite)
- **What happens**: Full five-phase cascade with all domain analyses, cognitive forcing, pre-mortem, and complete decision record.
- **Output**: Full decision record with all 8 sections
- **Cost**: ~$5.00-10.00 (CEO + 7 Sonnet subagents)
- **Latency**: 3-8 minutes
- **Example questions**: "Should we acquire CompetitorX?" / "Should we pivot our service model?" / "Should we accept this $2M investment offer?"

#### Bonus: Tier 3+: "Decision Space" (Full Cascade + Multiple CEO Profiles)
- **When**: User explicitly requests decision space exploration
- **Who**: All 8 agents + 5 CEO synthesis passes
- **What happens**: Full cascade, then CEO synthesizes through Guardian, Analyst, Visionary, Consensus Builder, and Regret Minimizer lenses
- **Output**: Decision space document showing range of defensible decisions
- **Cost**: ~$6.00-12.00 (full cascade + 5 lightweight CEO passes)
- **Latency**: 5-10 minutes

### Tier Selection Mechanism

Three approaches, from simplest to smartest:

**Approach 1: User-Selected (Simplest)**
- User invokes the skill with a tier flag: `/team-of-teams quick "Should we..."` or `/team-of-teams full "Should we..."`
- Default: Tier 2 (Focused Panel) if no flag specified
- This is the recommended v1 approach

**Approach 2: CEO Auto-Classification (Smarter)**
- CEO agent receives the question first and classifies it:
  - Checks for high-stakes keywords (acquire, pivot, layoff, regulatory, breach) -> Tier 3
  - Checks for domain-specific keywords (security, budget, hire, tools) -> Tier 2 with routing
  - Everything else -> Tier 2 default routing
- User can override: "Give me the full cascade on this"
- This is the recommended v1.5 approach (add after basic skill works)

**Approach 3: Adaptive Escalation (Smartest)**
- Start at Tier 1 (CEO quick assessment)
- If CEO determines the issue is cross-functional or high-stakes, auto-escalate to Tier 2 or 3
- This mirrors the real-world pattern where a CEO does a quick mental assessment before deciding whether to convene the leadership team
- This is the recommended v2 approach

### Critical Design Principle: Proportional Response

The tier system implements a **proportional response** to decision complexity. This isn't just cost optimization -- it's about producing appropriate output. A 10-page decision record for "should we buy standing desks?" undermines the skill's credibility. Matching analysis depth to question importance is itself an executive skill.

## Key Takeaways
- **The C-suite prompt has five sections**: Identity/Mandate, Analytical Process (the key section), Output Format, Domain Knowledge, and Accountability. Section 2 is where "thinking in 37 voices with 8 agents" actually happens.
- **The analytical process section forces step-by-step team lead consultation** -- not "consider perspectives" but "work through Team Lead 1's checklist, then Team Lead 2's, then synthesize." This structured decomposition is the core mechanism.
- **Three engagement tiers**: Quick Consult ($0.50-1), Focused Panel ($2-5), Full Cascade ($5-10). Default to Tier 2. User-selected in v1, auto-classified in v1.5.
- **Proportional response is itself an executive skill.** The tier system prevents over-analysis of simple questions and under-analysis of complex ones.
- **Start with user-selected tiers (v1)**, add CEO auto-classification (v1.5), then adaptive escalation (v2). Each version builds on the previous.

## Sources
| # | Source | URL/Path | What It Contributed |
|---|--------|----------|---------------------|
| 1 | Applied AI - Agent Complexity Spectrum | https://www.applied-ai.com/briefings/agent-complexity-spectrum/ | Four-tier framework, cost data, escalation triggers, reliability cliff |
| 2 | Prompt Engineering Guide - Reasoning LLMs | https://www.promptingguide.ai/guides/reasoning-llms | Chain-of-Thought, structured reasoning patterns |
| 3 | Codesmith - Mastering LLM Prompts | https://www.codesmith.io/blog/mastering-llm-prompts | Prompt structuring, section organization |
| 4 | PromptLayer - Flow Engineering | https://blog.promptlayer.com/prompt-routers-and-flow-engineering-building-modular-self-correcting-agent-systems/ | Modular agent systems, routing patterns |
| 5 | Deepchecks - Multi-Step LLM Chains | https://www.deepchecks.com/orchestrating-multi-step-llm-chains-best-practices/ | Multi-step orchestration patterns |
| 6 | Red Hat - AI Agent Types | https://www.redhat.com/en/blog/understanding-ai-agent-types-simple-complex | Agent complexity taxonomy |
| 7 | ArXiv - Structure Guided Prompt | https://arxiv.org/html/2402.13415v1 | Graph-based multi-step reasoning framework |
| 8 | Earlier research: RESEARCH_cognitive-forcing-prompt-architecture.md | Local | Six-layer prompt architecture, cognitive forcing functions |

## Citation Log
- Search: `LLM system prompt multi-step structured reasoning template agent decompose analyze synthesize output format`
- Search: `adaptive complexity tiered AI agent response simple moderate complex auto-detection task classification`
- Fetched: https://www.applied-ai.com/briefings/agent-complexity-spectrum/
- Attempted (PDF binary): https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
