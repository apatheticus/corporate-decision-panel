# Idea Report: Cognitive Forcing and the Prompt Architecture

**Direction explored by:** Free Thinker + Grounder
**Report number:** 03
**Related threads:** Cascade mechanics (Report #1), Engagement Model (Report #2), Explorer research on dissent mechanics and Agent Teams constraints

---

## The Idea

The hardest technical challenge in the Team of Teams skill isn't the cascade architecture or the agent orchestration — it's making 29 team lead perspectives produce **genuinely different analysis** rather than cosmetically varied restatements of the same reasoning. The solution is **Cognitive Forcing** — a prompt architecture pattern where each team lead perspective is defined not by a persona description but by a **unique analytical framework, a mandatory output structure, and a domain-specific forcing question** that compels the LLM to perform structurally different cognitive work for each perspective.

This approach is grounded in research (Nemeth 2001) showing that **authentic dissent from genuine domain perspective is more effective than artificially assigned devil's advocacy**. Rather than telling agents to disagree, you make them work with different analytical tools that naturally produce different conclusions. A compliance checklist and a three-scenario financial model are structurally different artifacts that require different reasoning — the LLM cannot collapse them into one voice because it's doing genuinely different work each time.

The prompt architecture extends across all three tiers of the system: team lead subagent definitions (29 analytical framework packages), C-suite agent prompts (7 domain decomposition and synthesis templates), and the CEO agent's synthesis layer (with modular Decision Mode overlays). Together, these form the complete cognitive architecture that makes the skill produce analysis worth reading.

## The Key Insight

Research confirms that simple role assignments ("You are a CFO") show **zero measurable improvement** in LLM output quality. The difference between "7 agents that all sound like slightly different consultants" and "7 genuinely distinct domain perspectives that produce productive disagreement" is not better persona descriptions — it's **forcing each perspective to use different analytical methods that produce structurally different outputs**. Domain knowledge encoded as checklists and analytical frameworks ("always check for: tax implications, GAAP impact, cash flow effects") is deterministic and reliable; domain knowledge encoded as persona descriptions ("you are an expert who would notice these things") is probabilistic and fragile.

## How We Got Here

The Free Thinker identified the "voice collapse" risk: telling one agent to think as five different people typically produces five paragraphs of the same underlying reasoning with different vocabulary. The solution — structured cognitive forcing with different frameworks, output templates, and devil's advocate prompts per perspective — emerged from pushing the prompt architecture question beyond "how do you write a good persona" to "how do you make the LLM do genuinely different cognitive work."

The Explorer's research on dissent mechanics added three critical techniques: the pre-mortem ("assume this fails — what caused it?"), adversarial empathy ("how would a competitor exploit this?"), and the Nemeth finding that authentic role-inherent dissent outperforms assigned contrarianism. These validated the cognitive forcing approach and added specific forcing question techniques that strengthen the framework.

The Grounder's two-tier agent model (now refined to a three-tier hybrid based on Explorer's Agent Teams research) provided the implementation vehicle: team leads as custom subagent definitions (`.claude/agents/`) with per-agent model selection, tool restrictions, and structured output templates.

## The Grounder's Take

- **Does this connect to what was asked for?** Yes — the user wants a spec comprehensive enough for a builder agent to construct the skill. The builder agent cannot write effective prompts without this framework. "Write a CFO prompt" is underspecified. "Write 5 team lead analytical framework packages for the CFO domain, each with a unique framework, output template, and forcing question" is buildable.
- **Would the audience care?** This is what determines whether the skill's output is genuinely useful or just verbose. The difference between "interesting multi-perspective analysis" and "seven variations of the same take" lives entirely in the prompt architecture.
- **Is this one of the good ones?** This is the hardest part of the spec to write and the most important for output quality. The cascade architecture (Report #1) is the skeleton. This is the muscle that makes it move.

## The Free Thinker's Vision

At its most ambitious, each of the 29 analytical framework packages becomes a **domain-specific reasoning engine** — not just a prompt but a complete analytical methodology encapsulated in a subagent definition. The Controller doesn't just "think about accounting" — it runs a GAAP compliance checklist methodology. The FP&A analyst doesn't just "model scenarios" — it produces a structured three-scenario analysis with explicit key variables and probability assessments. The output quality approaches what a competent human specialist would produce — not because the LLM has the specialist's experience, but because it's been given the specialist's analytical toolkit.

Future extensions: analytical framework packages could be versioned and improved independently. The community could contribute domain-specific frameworks. Industry-specific variants could override defaults (a healthcare company's Compliance/GRC Lead uses HIPAA-specific frameworks rather than generic compliance checklists).

## Architecture Detail: The Three-Layer Prompt Architecture

### Layer 1: Team Lead Subagent Definitions (29 Analytical Framework Packages)

Each team lead is implemented as a custom subagent definition in `.claude/agents/`. The definition contains:

**1. Analytical Framework** — The specific methodology this team lead uses to analyze issues.

**2. Mandatory Output Template** — A structured format that forces the LLM to produce specific analytical artifacts, not free-form opinions. Different templates for different roles prevent voice collapse.

**3. Forcing Questions** — Domain-specific prompts that compel the agent to surface insights that might otherwise be suppressed. Three types:
- **Domain Devil's Advocate**: "What would [domain-specific critic] find concerning about this?" (e.g., "What would an external auditor flag?")
- **Pre-Mortem**: "Assume this decision fails in 12 months. From your domain perspective, what caused the failure?" (research-backed as the highest single-technique value for decision improvement)
- **Adversarial Empathy**: "If you were [external adversary relevant to this domain], how would you exploit this?" (e.g., for CISO team leads: "If you were a threat actor, how would you exploit this change?")

**4. Subagent Configuration** — Technical implementation via YAML frontmatter:
- `model`: "haiku" for team leads, "sonnet" for C-suite, "opus" for CEO. Research on multi-agent systems shows heterogeneous model tiers actually IMPROVE output quality beyond cost savings — model diversity produces more varied analytical perspectives than homogeneous agents.
- `tools`: restricted to analytical tools only (Read, Grep, Glob, WebSearch — no file editing)
- `maxTurns`: capped to prevent runaway analysis (3-5 turns typical for team leads)
- `permissionMode`: "plan" for team leads (analysis only, no execution)

**5. Accountability Framing** — Research shows performance improves when decision-makers must justify conclusions to reviewers. Each team lead prompt includes: "Your analysis will be reviewed by [C-suite parent] alongside analyses from other specialists. Provide specific evidence for every claim. Unsupported assertions will be challenged."

**6. Blind Spot Declaration** — An explicit statement of what this role does NOT consider. Keeps lanes clear and prevents roles from drifting into each other's territory.

**Research validation (six-layer prompt architecture):** Studies on LLM prompt effectiveness identify six layers that reliably improve output quality: (1) Role Identity with specific experience context, (2) Decision Perspective describing priorities and natural biases, (3) Cognitive Forcing Functions as structural must-do requirements, (4) Team Management instructions for C-suite agents, (5) Output Format requirements as mandatory templates, and (6) Accountability framing. Simple role assignments without these layers show zero measurable improvement. The analytical framework package structure above maps directly to this research-backed architecture.

**Additional research finding — the cascade itself IS a cognitive forcing function.** The cascade structure forces "structured data acquisition" — systematic information gathering across all domains before any conclusion is formed. Each team lead's focused analysis prevents premature closure. The cross-functional Phase 4.5 implements "consider-the-opposite." The Decision Record implements accountability. The entire architecture is a nested set of cognitive forcing functions operating at every level.

#### Worked Example: CFO Domain (5 Team Lead Packages)

**Package 1 — Controller**
```
Framework: GAAP Compliance and Financial Controls Assessment
Output Template:
  COMPLIANCE IMPACT ASSESSMENT
  1. Revenue Recognition: [impact on ASC 606 compliance]
  2. Asset Classification: [reclassification requirements]
  3. Liability Exposure: [new or modified obligations]
  4. Audit Risk Flags: [items requiring auditor attention]
  5. Internal Control Modifications: [SOX/control changes needed]
  OVERALL RISK RATING: [Low / Medium / High / Critical]

Forcing Questions:
  - Domain DA: "What would an external auditor flag as concerning?"
  - Pre-mortem: "If this decision creates an accounting restatement in 18 months, what caused it?"
  - Adversarial: "If a short-seller were looking for red flags in our financials, would this decision provide one?"
```

**Package 2 — Head of FP&A**
```
Framework: Three-Scenario Financial Modeling
Output Template:
  SCENARIO ANALYSIS
  Best Case:
    - Revenue impact: [amount, timeline]
    - Cost impact: [amount, timeline]
    - Probability: [%]
    - Key enablers: [what must go right]
  Base Case:
    - Revenue impact: [amount, timeline]
    - Cost impact: [amount, timeline]
    - Probability: [%]
    - Key assumptions: [list]
  Worst Case:
    - Revenue impact: [amount, timeline]
    - Cost impact: [amount, timeline]
    - Probability: [%]
    - Key failure modes: [what goes wrong]
  CRITICAL VARIABLE: [the single factor that most determines which scenario materializes]
  DECISION SENSITIVITY: [how much does the recommendation change if the critical variable shifts by 20%?]

Forcing Questions:
  - Domain DA: "What assumption in the base case is most likely to be wrong?"
  - Pre-mortem: "If this investment shows negative ROI at month 12, what was the first signal we missed?"
  - Adversarial: "If a competitor sees our financial statements reflecting this decision, what do they learn about our strategy?"
```

**Package 3 — Treasury/Cash Manager**
```
Framework: Liquidity Stress Test
Output Template:
  CASH FLOW IMPACT TIMELINE
  Month 1-3:  [outflows | inflows | net position | runway impact]
  Month 4-6:  [outflows | inflows | net position | runway impact]
  Month 7-12: [outflows | inflows | net position | runway impact]
  FUNDING GAP: [yes/no | amount | timing]
  FUNDING OPTIONS: [internal reserves / credit line / external raise / defer]
  STRESS SCENARIO: [impact if biggest client delays payment 60 days during this period]

Forcing Questions:
  - Domain DA: "If our biggest client delayed payment by 60 days during this period, could we still fund this?"
  - Pre-mortem: "If we face a cash crisis within 6 months of this decision, what caused it?"
  - Adversarial: "If our bank reviewed this decision, would they tighten our credit terms?"
```

**Package 4 — AP/AR Manager**
```
Framework: Working Capital Cycle Analysis
Output Template:
  PAYABLES/RECEIVABLES IMPACT
  New Vendor Obligations: [terms, amounts, timing]
  Impact on Existing Payment Cycles: [acceleration/deceleration]
  Collection Risk Changes: [new exposure, concentration risk]
  Cash Conversion Cycle Impact: [days change, working capital delta]
  VENDOR RELATIONSHIP RISK: [impact on key vendor relationships]

Forcing Questions:
  - Domain DA: "What happens to our vendor relationships if this initiative fails midway?"
  - Pre-mortem: "If we have a payables crisis in 6 months, was this decision a contributing factor?"
  - Adversarial: "If a key vendor learned about this decision, would they change our payment terms?"
```

**Package 5 — Tax Lead**
```
Framework: Tax Structure Optimization Assessment
Output Template:
  TAX IMPLICATIONS MEMO
  Federal Impact: [liability change, timing]
  State/Local Impact: [nexus, apportionment changes]
  Structure Recommendation: [asset vs. stock, entity structure, timing optimization]
  Deductibility Schedule: [what's deductible, amortization timeline]
  Credits/Incentives: [applicable credits, incentive programs]
  EXTERNAL COUNSEL NEEDED: [yes/no | reason | urgency]

Forcing Questions:
  - Domain DA: "Is there a tax-advantaged structure that materially changes the financial calculus?"
  - Pre-mortem: "If we receive an adverse tax ruling related to this decision, what did we miss?"
  - Adversarial: "If the IRS audited this transaction, what would they scrutinize most closely?"
```

**CFO Synthesis Prompt**: After receiving all five team lead outputs, the CFO agent synthesizes them into a domain recommendation. The synthesis prompt instructs: "Review all team lead findings. Identify which findings are most material to the specific issue at hand. Your domain recommendation should reflect the weight of evidence across all specialist analyses, not average them. Flag where team lead findings conflict with each other — these internal tensions are themselves analytical signals."

### Layer 2: C-Suite Agent Prompts (7 Domain Orchestration Templates)

Each C-suite agent prompt must support three cognitive modes:

**Mode A — Tier 1 (Direct Consult)**: Quick, opinionated response drawing on internalized team lead perspectives. No explicit subagent delegation. The C-suite agent reasons through team lead lenses internally and produces a concise Advisory Note.

**Mode B — Tier 2/3 (Full Analysis)**: Explicit delegation to team lead subagents via Task tool. The C-suite agent:
1. Receives the CEO's framing
2. Translates it into domain-specific sub-questions (one per team lead)
3. Dispatches team lead subagents with the sub-questions
4. Collects structured outputs
5. Synthesizes into domain recommendation

**Mode C — Pre-Mortem Challenge Phase (Phase 4.5)**: After producing their own domain recommendation, each C-suite agent receives summaries of ALL other activated C-suite members' domain recommendations and answers one structured question: "Assume this decision fails catastrophically in 12 months. Based on what you see across all the domain recommendations, what caused the failure?"

Design parameters for Phase 4.5:
- **One round only.** Research shows multiple debate rounds cause "problem drift" — agents gradually forget the original question. A single structured round captures most cross-critique value.
- **Optional, not default.** Phase 4.5 roughly triples C-suite layer token cost. Recommended for Tier 3 Full Deliberation, optional toggle for Tier 2, never used in Tier 1.
- **No back-and-forth.** C-suite agents see summaries, produce failure mode analysis, and stop. They do not debate each other's critiques.
- **Feeds into Decision Record.** Pre-mortem findings appear in the Fault Line Analysis section and inform the Accepted Risks and Dissenting Views sections.
- **Research backing:** Pre-mortem is the highest single-technique value-add for decision quality (McChrystal Group / JSOC methodology). One structured critique round captures most value while avoiding problem drift (multi-agent debate research 2025-2026).

The C-suite prompt structure:

```
ROLE IDENTITY
  Name: [role title]
  Mandate: [one-line mandate from Report #1]
  Disposition: [Skeptic / Advocate / Neutral]
  Domain: [what you own]

TEAM COMPOSITION
  Your team leads: [list with one-line descriptions]

ANALYTICAL DOMAIN
  You analyze issues through the lens of: [domain description]
  Your domain's natural tension partners: [which C-suite roles you typically disagree with, and why]

OPERATING MODES
  Direct Consult: [how to produce a quick Advisory Note]
  Full Analysis: [how to delegate to team leads and synthesize]
  Challenge: [how to review and challenge peer recommendations]

SYNTHESIS INSTRUCTIONS
  When synthesizing team lead findings:
  - Identify the most material findings for this specific issue
  - Flag internal contradictions between team lead analyses
  - Produce a clear domain recommendation with confidence level
  - Include the single strongest risk and single strongest opportunity from your domain

FORCING QUESTIONS (apply in Full Analysis mode)
  Pre-mortem: "From your entire domain's perspective, if this decision fails, what did your team miss?"
  [domain-specific additional forcing questions]
```

### Layer 3: CEO Synthesis Layer (Modular Decision Modes)

The CEO prompt has a fixed analytical component and a swappable synthesis module:

**Fixed Component — Fault Line Analysis:**
```
SYNTHESIS PROTOCOL
1. Map all domain recommendations onto a single matrix:
   [Role | Recommendation | Confidence | Key Risk | Key Opportunity]
2. Identify FAULT LINES — where do recommendations diverge? WHY?
3. Identify the MOST DETERMINATIVE perspective for this decision type
4. Run PRE-MORTEM across all domains: "If this decision fails, which C-suite
   member's warning was most prophetic?"
5. Apply Decision Mode synthesis [see below]
6. Produce Decision Record
```

**Swappable Module — Decision Mode:**
The CEO's synthesis weighting changes based on the active Decision Mode. The mode is injected as a prompt modifier that adjusts how the CEO resolves fault lines and weights domain perspectives. (Decision Modes detailed in future report or spec section.)

## The Three Forcing Question Types (Research-Backed)

### 1. Pre-Mortem (Highest Value)
**"Assume this decision fails catastrophically in 12 months. From your domain perspective, what caused the failure?"**

Research basis: Pre-mortem technique (Klein 2007, applied at JSOC). Surfaces concerns people might otherwise suppress because it grants permission to imagine failure without being labeled as negative. Devil's advocacy increases consideration of alternatives by 61% (OrgChanger research).

Applied at: Every team lead (domain-specific failure), every C-suite member (department-level failure), and the CEO (organizational-level failure). Three levels of pre-mortem produce a comprehensive failure mode analysis.

### 2. Adversarial Empathy
**"If you were [domain-relevant external adversary], how would you exploit this decision?"**

Research basis: McChrystal's JSOC "Act As If" technique. Forces perspective-taking from outside the organization, surfacing vulnerabilities that internal analysis misses.

Applied at: Selected team leads where external adversaries are relevant:
- CISO team leads: "If you were a threat actor..."
- VP Sales team leads: "If you were our primary competitor..."
- CFO team leads: "If you were a short-seller / our bank / the IRS..."
- CAO Legal lead: "If you were opposing counsel..."
- CAO Compliance lead: "If you were a regulator..."

### 3. Domain Devil's Advocate
**"What would [domain-specific expert critic] find concerning about this?"**

Research basis: Nemeth (2001) — authentic dissent from genuine domain perspective outperforms assigned contrarianism. By asking "what would an auditor think?" rather than "play devil's advocate," you elicit domain-grounded criticism rather than generic contrarianism.

Applied at: Every team lead, with the critic figure matched to their domain:
- Controller: "What would an external auditor flag?"
- Engineering Lead: "What would a senior architect reviewing this code/system design criticize?"
- HR Lead: "What would an employment attorney warn about?"
- Security Ops Lead: "What would a penetration tester target?"

## Implementation: Subagent Definition File Structure

The builder agent would create the following file structure:

```
.claude/agents/
  team-leads/
    cfo/
      controller.md          # YAML frontmatter + analytical framework
      fpa-analyst.md
      treasury-manager.md
      ap-ar-manager.md
      tax-lead.md
    coo/
      operations-manager.md
      process-quality-lead.md
      vendor-procurement-manager.md
    cto/
      engineering-lead.md
      infrastructure-devops-lead.md
      data-analytics-lead.md
      product-ux-lead.md
    ciso/
      security-operations-lead.md
      compliance-grc-lead.md
      identity-access-lead.md
      security-architecture-lead.md
    vp-sales/
      sales-operations-lead.md
      account-management-lead.md
      business-development-lead.md
      sales-enablement-lead.md
    vp-delivery/
      project-program-manager.md
      resource-manager.md
      client-success-lead.md
      qa-delivery-standards-lead.md
    cao/
      hr-people-ops-lead.md
      legal-contracts-lead.md
      admin-policy-lead.md
      corporate-communications-lead.md
```

Each file follows the pattern:
```yaml
---
name: controller
description: "GAAP compliance and financial controls analyst for CFO domain"
model: haiku
tools:
  - Read
  - Grep
  - Glob
  - WebSearch
maxTurns: 5
---

# Controller — GAAP Compliance and Financial Controls

## Your Identity
You are the Controller reporting to the CFO. You own accounting accuracy
and financial controls.

## Your Analytical Framework
GAAP Compliance and Financial Controls Assessment

## Your Output Template
[structured template as above]

## Your Forcing Questions
[three forcing questions as above]

## Instructions
Analyze the issue presented to you ONLY through your specific domain lens.
Do not attempt to evaluate the overall business merit of the proposal.
Your job is narrow, focused, domain-specific analysis. Produce your
findings using the output template above. Be direct and opinionated —
flag concerns clearly, don't hedge.
```

## Open Threads

- **Framework Completeness**: This report provides the full CFO example (5 packages). The spec needs all 29 packages designed with equal specificity. This is the largest content-generation task for the builder agent.
- **Framework Versioning**: Can analytical frameworks be updated independently? Could industry-specific variants override defaults?
- **Output Quality Validation**: How do you test whether the cognitive forcing actually prevents voice collapse? What does a quality benchmark look like?
- **Tier 1 Internalization**: In Direct Consult mode, the C-suite agent doesn't spawn subagents — it reasons internally through team lead lenses. How well does this work without the structural forcing of separate subagent contexts?
- **Cross-Domain Forcing**: Should team leads have forcing questions that reference other domains? ("As Controller, what does the Engineering Lead's estimate assume about accounting treatment?")

## Recommendation to Arbiter

**Strongly recommended as a core component of the spec.** The Cognitive Forcing framework is what determines whether the skill produces genuinely useful multi-perspective analysis or just verbose agreement dressed in different terminology. The three forcing question types (pre-mortem, adversarial empathy, domain devil's advocate) are research-backed and directly implementable. The subagent definition file structure gives the builder agent a concrete deliverable list. This report, combined with Report #1 (cascade architecture) and Report #2 (engagement model), completes the three pillars of the spec: structure, experience, and analytical quality.
