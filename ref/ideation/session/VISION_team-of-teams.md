# Vision Document: The Corporate Decision Panel Agent Skill

**Session:** Corporate Decision Panel Agent Skill Ideation
**Date:** 2026-02-22
**Purpose:** Comprehensive design vision for a builder agent to construct a Claude Code Agent Skill that emulates SMB organizational decision-making.

---

## The Vision

**A Company OS.** Not a chatbot that roleplays executives, but a complete organizational reasoning engine that gives any founder, leader, or team the analytical power of a full executive committee -- with the structural integrity of mandated dissent ensuring that risk, cost, opportunity, and execution reality are all represented, even when the human user might prefer to hear only good news.

The Corporate Decision Panel Agent Skill transforms Claude Code into a boardroom in a box. Present any business issue -- from a quick operational question to a major strategic decision -- and the skill decomposes it through the top two layers of a SMB org structure: a CEO who frames and routes, C-suite executives who decompose and synthesize through their domains, and team leads who produce narrow, focused analysis using domain-specific analytical methods. The output is not a recommendation from a single voice. It is a structured Decision Record that shows how different domain perspectives analyze the same issue, where they agree, where they disagree, and why -- then synthesizes a decision that addresses the strongest objections.

The skill operates at three levels of depth (a quick hallway question, a focused working session, or a full board meeting) and four styles of synthesis (risk-averse, growth-oriented, consensus-building, or data-driven). Users match engagement to decision weight. The CEO who needs a quick gut check from the CFO perspective gets it in seconds. The founder facing a strategic pivot gets a comprehensive multi-perspective analysis with pre-mortem failure mode assessment.

What makes this more than "ask a panel of experts" is that disagreement is engineered, not accidental. The CISO is the Constitutional Skeptic -- their default is that change introduces risk. The VP of Sales is the Revenue Optimist -- they find the growth opportunity. These structural tensions are not bugs to be resolved but features that produce richer analysis than consensus ever could. The Fault Line Analysis section of every Decision Record captures the meta-analysis of where expert perspectives collide -- the single most valuable analytical artifact the system produces.

---

## Architecture: Three Pillars

The skill's design rests on four pillars, each the subject of a dedicated idea report.

### Pillar 1: Structure -- The Cascading Deliberation Engine

**Five-Phase Process:**

1. **Phase 0 -- Shared Consciousness Broadcast.** Before any analysis begins, the CEO broadcasts the issue context and framing to all activated C-suite agents simultaneously. This implements McChrystal's shared consciousness principle: everyone sees the same picture before reasoning independently. Without this, agents optimize for their domain without understanding the full context.

2. **Phase 1 -- CEO Frames and Routes.** The CEO decomposes the issue into evaluation dimensions, classifies the decision type (Strategic, Operational, Financial, Technical, Personnel, Compliance/Risk), and routes to relevant C-suite members using a default routing table with override capability. Routing is an analytical act: the CEO's choice of which domains to activate is itself a judgment about what matters. The framing includes explicit exclusion reasoning -- why certain teams were NOT activated, visible to the user. For research-relevant decisions, the CEO also issues a research directive to the CSO specifying what factual questions need investigation.

3. **Phase 1.5 -- Research Investigation (conditional).** When the CEO activates the CSO, a research phase executes before domain analysis begins. The CSO receives the CEO's research directive, decomposes it into research sub-questions, dispatches research team leads (Market Intelligence, Competitive Intelligence, Technology Scout, Industry & Regulatory Analyst, Precedent & Patterns Analyst) to investigate the factual landscape. Each research lead conducts iterative web search and analysis through their specialist lens. The CSO synthesizes findings into a **Research Dossier** containing: evidence summary, team lead findings with confidence grades, an Assumption Registry (each assumption tagged as Confirmed/Contradicted/Unverified/Partially Supported), key evidence (confirms/contradicts/complicates the proposal), evidence gaps, and an overall evidence quality grade. The Research Dossier is broadcast to all activated domain C-suite members before Phase 2 begins. Phase 1.5 is skipped entirely for decision types where the CEO does not activate the CSO (typically Operational and Personnel decisions).

4. **Phase 2 -- C-Suite Dispatches Downward.** Each activated C-suite executive translates the CEO's framing into domain-specific sub-questions, one per team lead. This translation is itself analytical -- the CFO does not forward the CEO's question to the Controller; the CFO asks the Controller "what are the GAAP implications of this change?" This decomposition separates the skill from "a panel of chatbots." When Phase 1.5 has executed, each C-suite executive receives both the CEO's framing AND the Research Dossier, grounding their domain analysis in investigated evidence rather than user-supplied context alone.

5. **Phase 3 -- Team Leads Produce Findings.** Each team lead subagent performs narrow, focused analysis through their specialist lens using their unique analytical framework and mandatory output template. The Controller produces a GAAP Compliance Assessment. The FP&A analyst produces a Three-Scenario Financial Model. Different methods produce structurally different outputs that cannot collapse into one voice.

6. **Phase 4 -- C-Suite Synthesizes Upward.** Each C-suite executive collects their team lead findings and synthesizes a domain recommendation with a confidence level, key risks, and key opportunities. Internal contradictions between team lead findings are flagged as analytical signals, not averaged away.

7. **Phase 4.5 -- Pre-Mortem Challenge (Tier 3 only).** After producing their own domain recommendation, each C-suite agent (including the CSO) receives summaries of ALL other activated C-suite members' recommendations and answers one structured question: "Assume this decision fails catastrophically in 12 months. Based on what you see across all the domain recommendations, what caused the failure?" One round only. No back-and-forth debate. Research-backed as the highest single-technique value-add for decision quality. The CSO's pre-mortem contribution focuses on evidence gaps that could invalidate assumptions underlying other domains' recommendations. Findings feed into the Fault Line Analysis and Dissenting Views sections of the Decision Record.

8. **Phase 5 -- CEO Deliberation.** The CEO maps all domain recommendations onto a single matrix (with the Research Dossier as evidentiary foundation when available), identifies fault lines (where and why recommendations diverge), determines the most determinative perspective for this decision type, applies the active Decision Mode to resolve tensions, and produces the final Decision Record.

**Hybrid Agent Architecture:**

The skill uses a hybrid model informed by Claude Code Agent Teams constraints:

- **Tier 1 (Agent Team members):** CEO + 8 C-suite officers (COO, CFO, CTO, CISO, CAO, VP of Sales, VP of Delivery, CSO). Real teammates spawned by the skill orchestrator. Can message each other and the CEO directly.
- **Tier 2 (Custom subagents):** 34 team lead specialists defined in `.claude/agents/team-leads/`. Each C-suite agent invokes their team leads as subagents. Subagents get their own context window, use cost-efficient models (Haiku), have restricted tool access, and report structured results back to their parent.

This architecture provides real isolation per perspective (each team lead gets its own context window, not a simulated pass within a longer prompt), cost optimization (Haiku for narrow analysis, Sonnet/Opus for synthesis), and true management simulation (the C-suite agent dispatches, collects, and synthesizes like a real executive).

**Engineered Dissent Model:**

| Role | Disposition | Mandate |
|------|------------|---------|
| CEO | Synthesizer | Frame, listen, weigh, and decide. Value is judgment, not expertise. |
| COO | Skeptic | "Can we actually do this with the people and processes we have?" |
| CFO | Skeptic | "Find the costs that aren't in the proposal." |
| CTO | Advocate | "What does this make possible that wasn't possible before?" |
| CISO | Skeptic | "Your default is that change introduces risk. You are the org's immune system." |
| VP of Sales | Advocate | "How does this help us sell more, faster, or to new markets?" |
| VP of Delivery | Skeptic | "What do we sacrifice from existing commitments to do this?" |
| CAO | Systemic | "Can the organization -- people, policies, culture -- absorb this?" |
| CSO | Investigative | "What does the evidence say? Bring facts where others bring assumptions." |

Balance: 4 skeptics, 2 advocates, 1 systemic, 1 investigative, 1 synthesizer. The skeptic-heavy balance counterbalances human optimism bias. The investigative role produces evidence, not positions -- it establishes the factual substrate on which domain analyses are built.

**Full Organizational Roster (29 Team Leads):**

| C-Suite | Team Leads |
|---------|-----------|
| COO | Operations Manager, Process/Quality Lead, Vendor/Procurement Manager, Facilities/Office Manager (conditional) |
| CFO | Controller, Head of FP&A, Treasury/Cash Manager, AP/AR Manager, Tax Lead |
| CTO | Engineering Lead, Infrastructure/DevOps Lead, Data/Analytics Lead, Product/UX Lead |
| CISO | Security Operations Lead, Compliance/GRC Lead, Identity & Access Lead, Security Architecture Lead |
| VP Sales | Sales Operations Lead, Account Management Lead, Business Development Lead, Sales Enablement Lead |
| VP Delivery | Project/Program Manager, Resource Manager, Client Success Lead, QA/Delivery Standards Lead |
| CAO | HR/People Ops Lead, Legal/Contracts Lead, Admin/Policy Lead, Corporate Communications Lead |

**Decision-Type Routing:**

| Decision Type | Default Activation | Full Activation Triggers |
|--------------|-------------------|------------------------|
| Strategic | CEO, CFO, CTO, VP Sales | Acquisition, pivot, new market entry |
| Operational | CEO, COO, VP Delivery | Major process change, org restructure |
| Financial | CEO, CFO, COO | Funding round, major investment, cost reduction |
| Technical | CEO, CTO, CISO | Platform migration, architecture change |
| Personnel | CEO, CAO, COO, VP Delivery | Layoff, major hiring, reorg |
| Compliance/Risk | CEO, CISO, CAO, CFO | Regulatory change, breach response, audit |

The CEO can always override defaults. Certain triggers activate all C-suite members regardless of decision type.

**Full-Activation Threshold Conditions:**

The CEO's Phase 1 framing prompt includes explicit threshold conditions for full activation. After classifying the decision type and selecting default routing, the CEO assesses whether the issue has cross-cutting implications that warrant full activation. If any of these conditions apply, all C-suite activate:

1. The decision is practically irreversible
2. The decision affects >30% of headcount
3. The decision changes the company's market position or business model
4. The decision involves existential financial risk
5. The CEO is uncertain which domains are relevant

The CEO states activation reasoning in the CEO Framing section of the Decision Record, including which threshold conditions (if any) triggered full activation. This makes routing a transparent, auditable analytical act rather than opaque pattern matching. The five conditions cover the canonical examples (acquisition -> irreversible + market position; layoff -> headcount; pivot -> business model) while catching novel situations via the uncertainty clause.

**Decision Record Output Format:**

```
EXECUTIVE SUMMARY
[3-5 sentences: the decision, key reasoning, primary dissent]

DECISION RECORD: [Issue Title]
Decision ID: [auto-generated]
Date: [timestamp]
Submitted by: [user]
Decision Type: [classification]
Tier: [1/2/3]
Decision Mode: [Guardian/Pioneer/Architect/Analyst]

1. ISSUE STATEMENT
   [The question as originally posed]

2. CEO FRAMING
   [Decomposition into evaluation dimensions]
   Activated Teams: [roles engaged + rationale]
   Excluded Teams: [roles not engaged + rationale for exclusion]

3. DOMAIN ANALYSES
   3.x [C-Suite Role] - [Mandate Title]
       Domain Recommendation: [Approve / Approve with Conditions / Oppose / Neutral]
       Confidence Level: [High / Medium / Low]
       Summary: [2-3 sentence synthesis]
       Team Lead Findings: [per team lead, 1-2 sentences each]
       Key Risks Identified: [list]
       Key Opportunities Identified: [list]

4. FAULT LINE ANALYSIS
   Points of Agreement: [what most domains agree on]
   Points of Contention: [where and why recommendations diverge]
   Pre-Mortem Findings: [failure modes identified in Phase 4.5]
   Unresolved Tensions: [surfaced but unresolvable with current info]

5. CEO DECISION
   Decision: [clear statement]
   Most Determinative Perspective: [which domain was weighted highest and why]
   Decision Weight Rationale: [why certain perspectives carried more weight]
   Conditions & Guardrails: [drawn from skeptic role recommendations]
   Accepted Risks: [consciously accepted, with reasoning]
   Mitigations Directed: [specific team actions ordered]

6. DISSENTING VIEWS
   [Strongest objections from overruled perspectives, preserved for record]

7. NEXT STEPS
   [Specific actions, implied owners, timelines]

8. METADATA
   Total roles consulted: [N]
   Decision complexity: [Low / Medium / High / Critical]
   Primary domain: [most determinative C-suite area]
   Dissent level: [Consensus / Mild Dissent / Strong Dissent / Split Decision]
   Key Assumptions: [assumptions the analysis rests on]
```

> **Production Note:** The Decision Record is the source of truth for the production phase. All five production artifacts (HTML, PPTX, DOCX, Results PDF, Capsule PDF) are derived from this document. The production phase synthesizes Decision Record content into a comprehensive, narrative-form briefing — not a formatted dump of the sections above. See "Content Mapping: Decision Record to Production Artifacts" in the Production Phase specification for the full mapping.

### Pillar 2: Experience -- The Engagement Model

**Three Interaction Tiers:**

| Tier | Name | Invocation | What Happens | Output | Production |
|------|------|-----------|--------------|--------|------------|
| 1 | Hallway Question | `/consult [role]: [question]` | Direct consult with one C-suite agent. No CEO, no routing, no team leads. Quick, opinionated, domain-specific. | Advisory Note (3-5 sentences) | None |
| 2 | Working Session | `/panel [roles]: [issue]` | CEO routes to 2-4 C-suite members. Each does domain analysis with team lead perspectives. CEO produces lightweight synthesis. | Panel Assessment (~1 page) | Optional (`--produce` flag) |
| 3 | Board Meeting | `/deliberate: [issue]` | Full five-phase cascade. All relevant C-suite activated. Full team lead analysis. Full CEO deliberation with optional Phase 4.5 pre-mortem. | Complete Decision Record (3-5 pages) | Always triggered |

**Auto-Triage:** `/evaluate: [issue]` presents the issue to the CEO for triage. The CEO assesses scope (single-domain vs. multi-domain vs. cross-cutting), impact (low/medium/high/critical), and reversibility (easily reversed vs. difficult vs. irreversible), then recommends both a tier and a Decision Mode with justification. The user can accept, escalate, de-escalate, or select a different mode.

The CEO's mode recommendation is based on decision characteristics:
- High irreversibility -> Sentinel or Guardian
- High growth opportunity -> Pioneer
- High organizational complexity -> Architect
- Low data availability -> Analyst (with "investigate further" likely outcome)
- Multiple strong competing priorities -> Architect
- Existential risk -> Sentinel

Enhanced `/evaluate` output format:
```
ISSUE TRIAGE: [Issue Title]

Scope: [single-domain | multi-domain | cross-cutting]
Impact: [low | medium | high | critical]
Reversibility: [easily reversed | difficult | irreversible]

Recommended Tier: [tier name]
Tier Rationale: [one sentence]

Recommended Mode: [mode name]
Mode Rationale: [one sentence explaining why this mode fits the
decision's characteristics]

Alternative: [suggest one alternative mode for comparison,
explaining what it would reveal]
```

The mode recommendation is advisory -- users who invoke `/consult`, `/panel`, or `/deliberate` directly with a mode specified skip this entirely. The "Alternative" line nudges users toward multi-mode comparison for consequential decisions, which is one of the skill's highest-value features.

**SMB-First Default: Bias Toward Tier 1.** The skill's default behavior should bias toward lightweight engagement. Most SMB decisions are fast, informal, and made by one or two people -- the skill should match that tempo. When the CEO auto-triages, the default recommendation should lean toward Tier 1 unless clear multi-domain signals are present. The goal is to make Tier 1 the daily habit and Tier 3 the deliberate escalation, not the other way around. A skill that defaults to the full board meeting for every question will not see daily use.

**Tier Escalation with Context Carry:** Tier selection is final at invocation -- the system does not auto-escalate mid-conversation. However, if a C-suite agent in Tier 1 realizes the issue has significant cross-domain implications, it produces its Advisory Note as normal AND appends a structured **Escalation Brief** that preserves the Tier 1 analysis as input for a higher-tier invocation.

Each C-suite agent's Tier 1 (Mode A) prompt includes: "If you determine this issue has significant cross-domain implications, produce your Advisory Note as normal AND append an Escalation Brief: a structured summary of your initial findings, the cross-domain implications you've identified, and a recommended tier and routing. Format the brief so it can be passed as context to a higher-tier invocation."

Escalation Brief format:
```
--- ESCALATION BRIEF ---
Initial Domain: [C-suite role]
Initial Finding: [1-2 sentence summary]
Cross-Domain Implications: [which other domains are affected and why]
Recommended Escalation: [Tier 2 /panel or Tier 3 /deliberate]
Recommended Routing: [which C-suite roles should be activated]
Key Context for Escalated Analysis: [findings the higher tier should build on]
---
```

This delivers context preservation and clear guidance without cascade interruption logic. The user re-invokes manually but with a structured brief that makes escalation seamless in practice, preserving the principle that "the user matches engagement to decision weight."

### Pillar 4: Strategic Depth -- Decision Modes and the Decision Space Map

The skill should not produce a single recommendation -- it should reveal a **decision space**. The same domain analysis can be synthesized through multiple Decision Modes, each a configurable lens that changes how the CEO agent weighs and resolves competing perspectives without changing the underlying analysis. By running the same inputs through different synthesis styles, the user sees not "what to do" but "what the terrain looks like in every direction." This transforms the skill from a decision engine into a **decision exploration tool**.

**Five CEO Decision Modes:**

Each mode maps to established decision theory (Rowe & Boulgarides Decision Style Theory + classical operations research):

| Mode | Disposition | Decision Theory | How It Resolves Fault Lines |
|------|------------|----------------|---------------------------|
| Guardian | Risk-averse | MaxiMin | Weights skeptic roles (CISO, CFO, COO, VP Delivery) more heavily. Skeptics must be satisfied, not just acknowledged. Decisions tend toward: don't do it, do a smaller version, or do it with extensive guardrails. |
| Pioneer | Growth-oriented | MaxiMax | Weights advocate roles (VP Sales, CTO) more heavily. Skeptic concerns are treated as engineering problems to solve, not reasons to stop. Decisions tend toward: do it, do it bigger, do it faster. |
| Architect | Consensus-building | Behavioral | Weights the fault lines themselves. Seeks the position that satisfies the most domain concerns. Conditions drawn from multiple domains, not just the most determinative one. |
| Analyst | Data-driven (default) | Hurwicz balanced | Weights confidence levels regardless of role disposition. High-confidence findings carry more weight. Low-confidence recommendations flagged as needing more research. "Defer pending better data" is a legitimate outcome. |
| Sentinel | Regret-minimizing | MiniMax Regret | Disproportionately weights the strongest objection from ANY role. Asks: "If this goes wrong, which C-suite member's warning will I wish I'd heeded?" Favors paths where being wrong is survivable. Particularly suited to irreversible decisions. |

Decision Modes are implemented as CEO synthesis prompt modifiers. The underlying domain analysis is identical across modes. The same team lead outputs, the same C-suite recommendations, the same fault lines -- but different weighting produces different decisions.

**CEO Prompt Modifiers (per mode):**

Each mode has a specific prompt modifier injected into the CEO's synthesis layer:

- **Guardian:** "You are cautious by disposition. You'd rather miss an opportunity than take a risk that could damage the business. When skeptic and advocate perspectives conflict, you lean toward the skeptics unless the advocates present overwhelming evidence of low-risk upside."
- **Pioneer:** "You are growth-oriented by disposition. You believe the biggest risk is standing still while competitors move. Frame skeptic concerns as implementation challenges to solve, not objections to honor."
- **Architect:** "You are a consensus-builder by disposition. You believe that decisions succeed or fail based on organizational alignment. Look for the position that satisfies the most domain concerns, even if it means a less aggressive or less cautious path."
- **Analyst:** "You are analytically driven. You distrust both optimism and pessimism -- you trust evidence. Weight domain recommendations by their confidence levels, not their enthusiasm or caution. A decision to defer is not indecision -- it's a rational response to insufficient information."
- **Sentinel:** "You are a regret minimizer. For every option, ask: 'If this decision turns out to be wrong, can we recover?' Disproportionately weight the single strongest objection from any domain. Choose the path where being wrong is survivable, even if being right is less spectacular."

**Mode/Tier Interaction Matrix:**

Each mode produces distinct behavioral patterns at each tier:

|  | Tier 1 (Hallway Question) | Tier 2 (Working Session) | Tier 3 (Board Meeting) |
|--|--------------------------|------------------------|----------------------|
| **Guardian** | Highlights downside risks, suggests what could go wrong | Synthesis biased toward risk mitigation. Extensive guardrails. | CEO weights skeptics heavily. High bar for approval. |
| **Pioneer** | Frames as investment question, suggests acceleration | Synthesis biased toward opportunity capture. "How to" not "whether to." | CEO weights advocates heavily. Low bar unless existential risk. |
| **Architect** | Includes "however, [other role] might see this differently" | Seeks option addressing most concerns across all activated roles. | CEO seeks widest organizational support. Conditions from all domains. |
| **Analyst** | Flags confidence level explicitly. Low-confidence = research recommendation. | Synthesis driven by which domains have highest-confidence findings. | CEO weights by evidence quality. Low-confidence = "investigate further." |
| **Sentinel** | Identifies the single biggest risk and whether it's survivable. | Identifies strongest objection across all activated roles. Tests whether downside is recoverable. | CEO disproportionately weights the strongest single objection. Favors survivable paths. |

Default cell for most users, most of the time: **Tier 1 + Analyst** -- quick, evidence-weighted, transparent about uncertainty.

**Multi-Mode Comparison and the Comparative Decision Record:**

The key efficiency insight: domain analysis is mode-independent. Multi-mode comparison runs domain analysis once (the expensive part) and CEO synthesis multiple times (cheap, single-agent passes). Cost: approximately 1.1x a single deliberation for 5x the strategic insight.

**Invocation:**
- Single mode: `/deliberate guardian: should we acquire CompetitorX?`
- Two-mode comparison: `/deliberate guardian vs pioneer: should we acquire CompetitorX?`
- All modes: `/deliberate all-modes: should we acquire CompetitorX?`
- Tier 1 with mode: `/consult cfo guardian: can we afford this?`
- Tier 2 with mode: `/panel pioneer finance tech: should we build this feature?`

**Comparative Decision Record format:**

```
COMPARATIVE DECISION RECORD: [Issue Title]
Decision ID: [auto-generated]
Modes Compared: [list]

EXECUTIVE SUMMARY
[One paragraph per mode showing how the decision differs]

SHARED ANALYSIS
[Domain analyses -- identical across modes, presented once]
[Fault Line Analysis -- presented once]

MODE COMPARISONS

  GUARDIAN SYNTHESIS:
    Decision: [statement]
    Most Determinative Perspective: [role + why]
    Key Factor: [what tipped this mode's decision]
    Conditions: [guardrails]

  PIONEER SYNTHESIS:
    Decision: [statement]
    Most Determinative Perspective: [role + why]
    Key Factor: [what tipped this mode's decision]
    Conditions: [guardrails]

  [repeat for each requested mode]

DIVERGENCE ANALYSIS
  Where Modes Agree: [decisions all modes reached]
  Where Modes Diverge: [the pivot points]
  The Key Choice: [what the user is actually deciding between -- not the
    business question, but the values/priorities question underneath it]

METADATA
  [standard metadata]
  Mode Sensitivity: [how much does the decision change across modes?
    High sensitivity = the decision depends heavily on risk appetite.
    Low sensitivity = all modes converge on the same answer --
    the evidence speaks for itself.]
```

**Mode Sensitivity** is a novel signal: if all modes produce the same decision, the right answer does not depend on the user's posture. If modes diverge dramatically, the user knows their personal risk appetite is the deciding factor, not the analysis. This transforms a binary recommendation into a nuanced view of the decision landscape.

### Pillar 3: Analytical Quality -- Cognitive Forcing and the Prompt Architecture

**The Voice Collapse Problem:**

Telling one LLM to "think as 5 different people" typically produces 5 paragraphs of the same underlying reasoning with different vocabulary. Simple role assignments ("You are a CFO") show zero measurable improvement in LLM output quality. The solution is not better persona descriptions -- it is forcing each perspective to use different analytical methods that produce structurally different outputs.

**Three-Layer Prompt Architecture:**

**Layer 1 -- Team Lead Subagent Definitions (29 Analytical Framework Packages):**

Each team lead is a custom subagent definition in `.claude/agents/team-leads/[domain]/[role].md` containing:

1. **Analytical Framework:** The specific methodology this role uses (e.g., GAAP Compliance Assessment, Three-Scenario Financial Modeling, Liquidity Stress Test).
2. **Mandatory Output Template:** Structured format forcing specific analytical artifacts, different per role.
3. **Three Forcing Questions:**
   - **Pre-Mortem** (Klein 2007): "Assume this decision fails in 12 months. From your domain perspective, what caused the failure?"
   - **Adversarial Empathy** (McChrystal JSOC): "If you were [domain-relevant external adversary], how would you exploit this?" (Applied where relevant -- auditors for Controller, threat actors for CISO leads, competitors for Sales leads)
   - **Domain Devil's Advocate** (Nemeth 2001): "What would [domain expert critic] find concerning?" Authentic domain-grounded criticism rather than generic contrarianism.
4. **Cross-Domain Challenge (for paired team leads only):** A fourth forcing question that challenges assumptions from a specific other domain. Applied to 14 of 29 team leads in 7 high-interaction pairs where cross-domain assumptions most commonly create blind spots. See "Cross-Domain Forcing Question Pairs" below.
5. **Accountability Framing:** "Your analysis will be reviewed by [C-suite parent] alongside analyses from other specialists. Provide specific evidence for every claim."
6. **Blind Spot Declaration:** Explicit statement of what this role does NOT consider.
7. **Subagent Configuration:** Model (Haiku), tools (Read, Grep, Glob, WebSearch only), max turns (3-5), permission mode (plan -- analysis only, no execution).

**Layer 2 -- C-Suite Agent Prompts (7 Domain Orchestration Templates):**

Each C-suite agent prompt supports three cognitive modes:
- **Mode A (Tier 1 Direct Consult):** Quick, opinionated response drawing on internalized team lead perspectives. No subagent delegation. Includes a **structured internal checklist** that forces explicit consideration of each team lead's core question before producing the Advisory Note, ensuring analytical breadth without subagent cost. The checklist asks the C-suite agent to note which team lead perspectives are relevant and which are not, including only relevant perspectives in the Advisory Note.
- **Mode B (Tier 2/3 Full Analysis):** Explicit delegation to team lead subagents. Receive CEO framing -> translate into domain sub-questions -> dispatch subagents -> collect structured outputs -> synthesize domain recommendation.
- **Mode C (Phase 4.5 Challenge):** Review all peer C-suite recommendations and produce pre-mortem failure mode analysis.

**Mode A Structured Internal Checklists (per C-suite agent):**

Each C-suite agent's Mode A prompt includes a domain-specific checklist. Before producing the Advisory Note, the agent briefly considers each team lead perspective using that perspective's core analytical question. This adds ~50-100 tokens to each Tier 1 response while preventing shallow analysis.

*CFO checklist:*
> - Controller: Any accounting treatment or compliance implications?
> - FP&A: What are the rough financial scenarios (best/worst/likely)?
> - Treasury: Any cash flow timing concerns?
> - AP/AR: Any working capital cycle impact?
> - Tax: Any tax structure implications?

*COO checklist:*
> - Operations Manager: Any operational workflow or capacity implications?
> - Process/Quality Lead: Any process compliance or quality standard concerns?
> - Vendor/Procurement Manager: Any vendor dependency or procurement implications?
> - Facilities/Office Manager: Any physical infrastructure or workspace impact? (if active)

*CTO checklist:*
> - Engineering Lead: Any development effort, technical debt, or architecture implications?
> - Infrastructure/DevOps Lead: Any infrastructure, deployment, or scalability concerns?
> - Data/Analytics Lead: Any data architecture, analytics, or reporting impact?
> - Product/UX Lead: Any product roadmap or user experience implications?

*CISO checklist:*
> - Security Operations Lead: Any threat surface, monitoring, or incident response implications?
> - Compliance/GRC Lead: Any regulatory compliance or governance concerns?
> - Identity & Access Lead: Any access control, authentication, or authorization impact?
> - Security Architecture Lead: Any security architecture or design pattern concerns?

*VP Sales checklist:*
> - Sales Operations Lead: Any sales process, CRM, or pipeline implications?
> - Account Management Lead: Any existing customer relationship or retention concerns?
> - Business Development Lead: Any partnership, channel, or market expansion impact?
> - Sales Enablement Lead: Any sales training, collateral, or tooling implications?

*VP Delivery checklist:*
> - Project/Program Manager: Any project timeline, scope, or resource implications?
> - Resource Manager: Any staffing, allocation, or capacity concerns?
> - Client Success Lead: Any client satisfaction, SLA, or relationship impact?
> - QA/Delivery Standards Lead: Any quality assurance or delivery standard concerns?

*CAO checklist:*
> - HR/People Ops Lead: Any hiring, retention, policy, or culture implications?
> - Legal/Contracts Lead: Any legal exposure, contract, or IP concerns?
> - Admin/Policy Lead: Any administrative policy or procedural impact?
> - Corporate Communications Lead: Any internal/external messaging or reputation concerns?

C-suite prompt structure includes: role identity and mandate, team composition, analytical domain with natural tension partners, operating mode instructions, synthesis instructions, and domain-level forcing questions.

**Layer 3 -- CEO Synthesis (Modular Decision Modes):**

Fixed analytical component (fault line mapping, most determinative perspective identification, cross-domain pre-mortem) plus swappable Decision Mode module that adjusts synthesis weighting.

**Reference Implementation -- CFO Domain (5 Complete Packages):**

The CFO domain serves as the reference implementation with complete analytical framework packages for all five team leads:

| Team Lead | Framework | Output Artifact |
|-----------|-----------|----------------|
| Controller | GAAP Compliance and Financial Controls Assessment | Compliance Impact Assessment with risk rating |
| Head of FP&A | Three-Scenario Financial Modeling | Scenario Analysis with critical variable and decision sensitivity |
| Treasury/Cash Manager | Liquidity Stress Test | Cash Flow Impact Timeline with funding gap analysis |
| AP/AR Manager | Working Capital Cycle Analysis | Payables/Receivables Impact with vendor relationship risk |
| Tax Lead | Tax Structure Optimization Assessment | Tax Implications Memo with external counsel recommendation |

Each package includes complete forcing questions with domain-specific adversarial figures (external auditor, short-seller, bank, IRS, key vendor). This reference implementation should be used as the template for all 29 packages.

**Bias and Role Susceptibility Mapping:**

Research on LLM role-playing identifies specific failure modes where agents drift from their mandated perspective. Each role's prompt should include awareness of its susceptibility patterns:

| Disposition | Susceptibility | Mitigation |
|------------|---------------|------------|
| Skeptic roles (CISO, CFO, COO, VP Delivery) | Risk of softening objections to match perceived user preference. LLMs have a sycophancy bias that undermines skeptic mandates. | Explicit instruction: "Your value is in surfacing concerns, not in being agreeable. A skeptic who hedges is worthless." |
| Advocate roles (CTO, VP Sales) | Risk of under-weighting genuine constraints. Advocacy can become cheerleading. | Require advocates to name the strongest objection to their own position and explain why they still advocate. |
| Synthesizer (CEO) | Risk of false balance -- treating all perspectives as equally weighted regardless of decision type. Also susceptible to anchoring on the first domain recommendation received. | Require explicit weight rationale. Randomize order of domain recommendation presentation. |
| Systemic (CAO) | Risk of vagueness -- "organizational culture" analysis can be unfalsifiable. | Require concrete indicators: specific policies affected, specific teams impacted, specific precedents set. |

The builder agent should incorporate these susceptibility mitigations directly into each role's prompt. The forcing questions partially address this (pre-mortem and devil's advocate counteract sycophancy), but explicit susceptibility awareness adds a second layer of defense.

**Cross-Domain Forcing Question Pairs:**

Seven high-interaction team lead pairs have a fourth forcing question ("Cross-Domain Challenge") that challenges assumptions from a specific other domain. These pairs represent real organizational friction points where one domain's analysis commonly rests on assumptions another domain would challenge.

| Pair | Team Lead A (Domain) | Team Lead B (Domain) | A's Cross-Domain Question | B's Cross-Domain Question |
|------|---------------------|---------------------|--------------------------|--------------------------|
| 1 | Engineering Lead (CTO) | Controller (CFO) | "What does your implementation estimate assume about how this will be capitalized vs. expensed?" | "What does the accounting treatment assume about how Engineering will structure the implementation?" |
| 2 | FP&A Analyst (CFO) | Sales Operations Lead (VP Sales) | "What revenue assumptions does this projection share with -- or diverge from -- the sales pipeline forecast?" | "What does the sales forecast assume about pricing, margins, or financial constraints that FP&A might challenge?" |
| 3 | Security Architecture Lead (CISO) | Infrastructure/DevOps Lead (CTO) | "What security constraints does the proposed architecture assume, and are they realistic given DevOps's operational requirements?" | "What operational assumptions does the infrastructure design make about security controls and their performance impact?" |
| 4 | HR/People Ops Lead (CAO) | Resource Manager (VP Delivery) | "What does the staffing plan assume about hiring timelines, availability, and retention?" | "What does the resource allocation assume about HR's ability to recruit, onboard, or redeploy personnel?" |
| 5 | Legal/Contracts Lead (CAO) | Business Development Lead (VP Sales) | "What contractual terms or legal constraints does the deal structure assume are negotiable or enforceable?" | "What does the business case assume about legal feasibility, contract timelines, or regulatory approval?" |
| 6 | Process/Quality Lead (COO) | QA/Delivery Standards Lead (VP Delivery) | "What quality standards does the process change assume Delivery can maintain during transition?" | "What does the delivery quality framework assume about operational process stability during this change?" |
| 7 | Data/Analytics Lead (CTO) | Compliance/GRC Lead (CISO) | "What does the data architecture assume about data residency, retention, and access compliance requirements?" | "What does the compliance framework assume about the technical feasibility of data controls?" |

14 of 29 team leads receive this fourth question. The remaining 15 team leads retain only the three standard forcing questions (Pre-Mortem, Adversarial Empathy, Domain Devil's Advocate). The builder agent should validate these pairs against the full roster during implementation and adjust if cross-domain assumption gaps are found elsewhere.

---

## Implementation Specification

### File Structure

```
.claude/
  agents/
    ceo.md                           # CEO agent definition
    c-suite/
      coo.md                         # C-suite agent definitions
      cfo.md
      cto.md
      ciso.md
      cao.md
      vp-sales.md
      vp-delivery.md
    team-leads/
      coo/
        operations-manager.md        # Team lead subagent definitions
        process-quality-lead.md
        vendor-procurement-manager.md
      cfo/
        controller.md
        fpa-analyst.md
        treasury-manager.md
        ap-ar-manager.md
        tax-lead.md
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
  skills/
    corporate-decision-panel/
      skill.md                       # Skill front matter and instructions
      templates/
        decision-record.md           # Decision Record template
        advisory-note.md             # Tier 1 output template
        panel-assessment.md          # Tier 2 output template
        decision-space-map.md        # Multi-mode comparison template
        comparative-decision-record.md # Multi-mode Comparative Decision Record
      config/
        routing-table.md             # Decision-type routing defaults
        company-profile.md           # Company parameterization
        decision-modes.md            # CEO Decision Mode prompt modifiers
      templates/production/
        decision-briefing-page.md    # HTML page structure and design spec
        board-presentation.md        # PPTX slide structure and content mapping
        board-document.md            # DOCX document structure and formatting spec
        capsule-structure.md         # Capsule PDF layers and content inventory
```

### Subagent Definition Format

Each team lead subagent file follows this pattern:

```yaml
---
name: [role-slug]
description: "[analytical domain] analyst for [C-suite parent] domain"
model: haiku
tools:
  - Read
  - Grep
  - Glob
  - WebSearch
maxTurns: 5
---

# [Role Title] -- [Analytical Framework Name]

## Your Identity
You are the [Role Title] reporting to the [C-suite Parent]. You own [domain scope].

## Your Analytical Framework
[Framework name and methodology description]

## Your Output Template
[Structured template with specific fields to fill]

## Your Forcing Questions
- Domain Devil's Advocate: "[domain-specific question]"
- Pre-Mortem: "[domain-specific failure scenario question]"
- Adversarial Empathy: "[domain-specific external adversary question]"

## Your Blind Spots
You do NOT evaluate: [explicit scope exclusions]. Leave those to [other roles].

## Instructions
Analyze the issue presented to you ONLY through your specific domain lens.
Do not attempt to evaluate the overall business merit of the proposal.
Your job is narrow, focused, domain-specific analysis. Produce your
findings using the output template above. Be direct and opinionated --
flag concerns clearly, do not hedge.

Your analysis will be reviewed by the [C-suite Parent] alongside analyses
from other specialists. Provide specific evidence for every claim.
Unsupported assertions will be challenged.
```

### Heterogeneous Model Tiering

| Layer | Model | Rationale |
|-------|-------|-----------|
| Team Lead Subagents | Haiku | Narrow, focused analysis. Cost-efficient. Model diversity improves analytical variety. |
| C-Suite Agents | Sonnet | Domain decomposition, delegation, and synthesis. Moderate complexity. |
| CEO Agent | Opus | Cross-domain synthesis, fault-line analysis, and decision-making. Highest reasoning quality. |

Research on multi-agent systems suggests heterogeneous model tiers actually improve output quality beyond cost savings: model diversity produces more varied analytical perspectives than homogeneous agents.

### Company Profile Configuration

The skill supports company profile parameterization through **archetype presets** -- pre-configured profiles that set roster composition, default decision mode, escalation behavior, and industry-specific frameworks. Users select an archetype during onboarding and can override individual settings afterward.

**Four Company Archetype Presets:**

| Archetype | Roster Modifications | Default Mode | Compliance Focus | Notes |
|-----------|---------------------|-------------|-----------------|-------|
| **Technology / SaaS** (default) | Facilities/Office Manager inactive. Product/UX Lead under CTO. | Analyst | SOC 2, GDPR | Pioneer-leaning for growth-stage companies |
| **Professional Services** | All roles active. VP Delivery weighted heavily in routing. | Architect | Client contract compliance | Client-centric framing in COO and VP Sales domains |
| **Regulated Industry** | All roles active. Compliance/GRC Lead expanded scope. | Guardian | HIPAA, SOX, PCI-DSS (industry-specific) | Industry-specific compliance frameworks auto-configured |
| **Manufacturing / Physical** | Facilities/Office Manager active. Supply chain emphasis in COO. | Analyst | Industry safety, environmental | Vendor/Procurement Manager weighted heavily |

**Company Profile Configuration Format:**

```yaml
company_profile:
  archetype: technology_saas  # | professional_services | regulated_industry | manufacturing
  name: "Acme Corp"
  industry: "B2B SaaS"
  headcount: 350

  overrides:
    team_leads:
      facilities-office-manager: { active: false }
      product-ux-lead: { active: true, reports_to: cto }
    default_mode: analyst
    escalation_bias: normal  # conservative | normal | aggressive
```

Archetype presets give the best ratio of configuration simplicity to roster accuracy -- one choice gets 80% configured. The onboarding stress test (below) validates the preset before real use. Users who need fine-grained control override individual settings after selecting a preset. The builder agent should ship with at least the Technology/SaaS default and one additional preset (Professional Services or Regulated Industry) to demonstrate the pattern.

Default profile: mid-market IT/technology services company, 200-500 employees (based on Explorer research).

### Onboarding Stress Test as Initialization

When the skill is first configured for a company, run an organizational stress test as initialization. Present a representative cross-functional issue and run it through the full cascade. This serves four purposes:
1. **Validates the configuration:** Confirms all agents produce coherent, domain-appropriate analysis for this company type.
2. **Calibrates the user:** Shows the user what the skill produces and at what depth.
3. **Surfaces profile issues:** If a team lead produces irrelevant analysis (e.g., Facilities Manager for a fully-remote SaaS company), the user can adjust the profile before real use.
4. **Verifies mode distinctiveness:** Confirms that Decision Modes produce meaningfully different synthesis, not slight variations.

**Mode Calibration Protocol:**

The stress test extends beyond single-mode validation to include a multi-mode calibration step:

1. **Contentious test issue required.** The stress test issue must be deliberately contentious -- an issue where reasonable people would disagree about the right approach. Example: "Should we acquire a competitor that would double our headcount but carries significant regulatory risk and requires taking on substantial debt?" An issue where all modes agree is too easy for calibration.

2. **Run all five modes.** Domain analysis runs once (the expensive part); CEO synthesis runs five times (cheap). Cost: approximately 1.1x the single-mode stress test.

3. **Calibration criteria: 3-of-5 divergence.** At least 3 of 5 modes must produce materially different outcomes. "Materially different" means either a different decision (approve vs. oppose vs. defer) or the same decision with substantially different conditions, guardrails, or accepted risks. If fewer than 3 modes diverge on a deliberately contentious issue, the prompt modifiers need revision before the skill is considered calibrated.

4. **Log calibration results.** Store results in the company profile for reference:

```yaml
calibration:
  stress_test_issue: "[issue description]"
  date: "[timestamp]"
  mode_results:
    guardian: "[decision summary]"
    pioneer: "[decision summary]"
    architect: "[decision summary]"
    analyst: "[decision summary]"
    sentinel: "[decision summary]"
  divergence_score: "[N] of 5 modes produced different decisions"
  calibration_status: pass  # or fail -- requiring prompt modifier revision
```

### Cost and Implementation Viability

Explorer research on implementation viability produced concrete cost estimates and confirmed the recommended architecture patterns.

**Cost Per Decision (v1 Staged Execution):**

| Scenario | C-Suite Agents Activated | Estimated Cost |
|----------|------------------------|----------------|
| Tier 1 (Hallway Question) | 1 Sonnet subagent | ~$0.50-1.00 |
| Tier 2 with routing (3-5 agents) | 3-5 Sonnet subagents + Opus CEO | ~$2.50-5.00 |
| Tier 3 full cascade (all 7) | 7 Sonnet subagents + Opus CEO | ~$4.50-9.00 |
| Multi-mode comparison (5 modes) | Same as Tier 3 + 4 additional CEO synthesis passes | ~$5.00-10.00 |
| Tier 3 + production (5 production agents) | Deliberation + Image, Presentation, Document, Web Page, Archivist | ~$7.50-15.00 total |
| Tier 2 `--produce` (lighter production) | Panel assessment + 5 production agents (less content) | ~$4.50-9.00 total |

Production costs are additive to deliberation costs. The production phase adds approximately $3-6 for a full Tier 3 production run and $2-4 for a lighter Tier 2 `--produce` run. Infographic generation via browser automation (Image Agent) is the most variable cost component.

For comparison, a naive 37-agent flat architecture would cost $18-37 per decision. The hybrid architecture with selective routing achieves 40-60% cost reduction while maintaining analytical quality.

**v1 Architecture: Staged Execution with Subagents**

The recommended v1 implementation uses the CEO as the main session, invoking C-suite members as subagents (which can run in parallel). Team lead analysis is simulated within each C-suite subagent's prompt via the analytical framework packages from Report #3. This pattern:
- Requires only 8 context windows (1 CEO + 7 C-suite)
- Benefits from prompt caching for repeated system prompt content
- Works within all current Claude Code Agent Teams constraints
- Produces 7 independent analytical perspectives (the primary quality driver)

**v2 Architecture: Hybrid Agent Team + Subagents**

When Claude Code supports teammates spawning subagents (not yet confirmed), the architecture evolves to: CEO as team lead of an Agent Team, 7 C-suite as teammates (with inter-agent messaging for Phase 4.5), each spawning team lead subagents on Haiku. This enables true three-tier execution with cross-functional deliberation.

**Key cost design decision:** Routing is a core feature, not a v2 optimization. Without routing, every question triggers 7 subagent calls. With routing, most decisions activate 3-5 C-suite members, reducing cost 40-60% and producing less analytical noise.

---

## Production Phase

The deliberation phase produces Decision Records -- structured text documents designed for analytical completeness. The production phase transforms that content into board-ready artifacts designed for consumption, presentation, editing, and archiving.

### One Content, Five Formats

The production phase produces five artifacts from the Decision Record. These are format variants of the same synthesized content -- not different documents.

- **`index.html`** — Interactive decision briefing page. The designed, definitive rendering. A polished web page presenting the full decision with navigation, infographic visualizations, and download links to the other artifacts. This is the artifact people will actually use day-to-day.
- **`PRESENTATION_<issue-slug>.pptx`** — Board presentation slide deck. The same content structured for presenting to a group -- one concept per slide, visual aids, speaker-note-ready. Built for the meeting room.
- **`REPORT_<issue-slug>.docx`** — Editable board document. The same content in a format designed for executive review workflows: comments, tracked changes, annotation, redlining. Built for collaborative editing and formal approval processes.
- **`RESULTS_<issue-slug>.pdf`** — Print-portable PDF of the distribution page. The "email it, attach it, archive it" artifact -- same design as the HTML page, PDF format.
- **`CAPSULE_<issue-slug>.pdf`** — Comprehensive deliberation archive. Different in kind from the other four. Not a format variant of the decision briefing, but a layered archive of the entire deliberation process: the Decision Record plus all domain analyses, team lead findings, routing rationale, pre-mortem findings, and source materials. Built for institutional memory and decision revisitation.

**Consistency principle:** The information presented in HTML, PPTX, DOCX, and Results PDF must be identical. They serve different consumption contexts (browsing, presenting, editing, sharing/archiving) but present the same decision, the same rationale, the same analysis, and the same action plan. If the content in any of these diverges from the others, something has gone wrong. The Capsule PDF is the exception -- it contains everything the other four contain plus the full deliberation process.

### Synthesized Content, Not Raw Decision Record

The production artifacts do not simply reformat the Decision Record sections with nicer typography. They present the Decision Record content as a **synthesized, comprehensive briefing** -- a narrative document that a board member, advisor, or future decision-maker can read and understand without knowledge of the system that produced it.

The synthesized content includes:

1. **Executive summary** — The decision, why it was chosen, and the primary dissent, in 3-5 sentences
2. **Problem statement and context** — The issue as originally posed, with business context
3. **Analytical framework** — How the issue was decomposed: which domains were consulted, why, and what each was asked to evaluate
4. **Detailed domain analysis** — Per-domain findings with visual aids (infographic scorecards, routing diagrams), structured to show what each perspective revealed
5. **Risk and disagreement analysis** — The fault lines: where perspectives collide, pre-mortem failure modes, unresolved tensions. This is the most valuable analytical section and should be prominently featured in every format.
6. **The decision with full rationale** — The chosen path, which perspective was most determinative and why, the decision mode applied, and how fault lines were resolved
7. **Guardrails and conditions** — Drawn from skeptic role recommendations: what must be true for this decision to succeed
8. **Plan to be executed** — Next steps with implied owners and timelines
9. **Dissenting views** — The strongest objections from overruled perspectives, preserved for the record. Not buried in an appendix -- given visible placement.
10. **Expected benefits and accepted risks** — What the decision is expected to achieve, and what risks were consciously accepted with reasoning
11. **Unknowns and open questions** — What the analysis could not resolve, and what assumptions the decision rests on
12. **Metadata and links** — Decision classification, complexity, dissent level, mode used, roles consulted

This is a narrative document, not a formatted dump of Decision Record sections. The production agents must synthesize, not transcribe.

### When Production is Triggered

- **Tier 3 (Board Meeting):** Always triggered. After the CEO produces the final Decision Record, the orchestrator automatically transitions to the production phase and spawns all five production agents.
- **Tier 2 (Working Session):** Optional. Triggered by the `--produce` flag on invocation (e.g., `/panel --produce finance tech: should we build this feature?`). Without the flag, Tier 2 produces only the Panel Assessment text document.
- **Tier 1 (Hallway Question):** No production. Advisory Notes are lightweight by design -- formatting them as board-ready documents would undermine the Tier 1 value proposition of speed and simplicity.
- **Multi-Mode Comparisons:** A single set of production artifacts that includes all mode comparisons. The domain analysis is presented once (shared across modes), and the synthesis section includes per-mode decisions with divergence analysis. The Comparative Decision Record format maps naturally to the production artifact structure.

### Production Output Directory Structure

```
{session-output}/
  index.html                               # Interactive decision briefing page
  PRESENTATION_<issue-slug>.pptx           # Board presentation slide deck
  REPORT_<issue-slug>.docx                 # Editable board document
  RESULTS_<issue-slug>.pdf                 # Print-portable PDF of distribution page
  CAPSULE_<issue-slug>.pdf                 # Comprehensive deliberation archive
  images/
    INFOGRAPHIC_routing-diagram.png        # Which C-suite activated and why
    INFOGRAPHIC_domain-scorecard.png       # Per-domain recommendation/confidence matrix
    INFOGRAPHIC_fault-lines.png            # Agreement/contention visualization
    INFOGRAPHIC_risk-matrix.png            # Impact/likelihood risk grid
    INFOGRAPHIC_action-plan.png            # Timeline with owners and milestones
    INFOGRAPHIC_mode-comparison.png        # (Multi-mode only) Divergence tree
  build/
    build_presentation.js                  # PPTX build script (pptxgenjs)
    build_report.js                        # DOCX build script (docx-js)
    build_capsule.py                       # Results PDF + Capsule PDF build script (weasyprint)
```

### Production Dependency Pipeline

```
Task A: Image Agent (infographics)          ─┐
Task B: Presentation Agent (PPTX)            ├─ parallel (unblocked immediately)
Task C: Document Agent (DOCX)               ─┘
                                              │
Task D: Web Page Agent (HTML)    ←── blocked by A, B, C
                                              │
Task E: Archivist (Results + Capsule PDF) ←── blocked by D
```

The Image, Presentation, and Document agents work in parallel -- they have no dependencies on each other. The Web Page Agent is blocked until all three complete because it needs to reference the infographic images, link to the PPTX download, and link to the DOCX download. The Archivist is blocked until the Web Page Agent completes because the Results PDF is a direct rendering of the HTML distribution page.

**Communication flow:**

```
                     Orchestrator (Skill Entry Point)
                     ┌────────────┼────────────┐
                     │            │            │
               spawns + assigns   │      spawns + assigns
                     │            │            │
          ┌──────────┼──────┐    │            │
          v          v      v    v            v
    Image Agent  Pres Agent  Doc Agent  Web Page Agent   Archivist
    (parallel)   (parallel)  (parallel) (blocked by      (blocked by
                                         A + B + C)       D)
          │          │          │            │                │
          │          │          │   unblocks │                │
          └──────────┴──────────┴───────────→│                │
                                             │                │
                                       builds designed        │
                                       distribution page      │
                                       with infographics,     │
                                       PPTX + DOCX links      │
                                             │                │
                                             └── unblocks ───→│
                                                              │
                                                        renders Results PDF
                                                        from distribution page
                                                        + builds Capsule PDF
                                                        from all artifacts
                                                              │
                                                        reports complete
```

**Orchestrator spawn sequence:**

```
TaskCreate: "Generate analytical infographics"                → task A
TaskCreate: "Create board presentation (PPTX)"               → task B
TaskCreate: "Create board document (DOCX)"                    → task C
TaskCreate: "Create interactive decision briefing page"       → task D
TaskCreate: "Produce Results PDF and Deliberation Capsule"    → task E

TaskUpdate: { taskId: D, addBlockedBy: [A, B, C] }
TaskUpdate: { taskId: E, addBlockedBy: [D] }
```

### Content Mapping: Decision Record to Production Artifacts

Each Decision Record section maps to specific placement in each output format. The production agents use this mapping to ensure content consistency across formats while adapting presentation to each format's strengths.

**Standard Decision Record Mapping:**

| Decision Record Section | HTML | PPTX | DOCX | Capsule PDF |
|---|---|---|---|---|
| Executive Summary | Hero section with key takeaway callout, decision prominently displayed | Title slide + Executive Summary slide | Document abstract, opening paragraph | Cover page with decision and key infographic |
| Issue Statement | Problem context section with business background | "The Question" slide | Section 1: Problem Statement | Layer 2: Decision |
| CEO Framing | Evaluation dimensions section, routing visualization infographic | "Analytical Framework" slide with routing diagram | Section 2: Analytical Framework, routing rationale table | Layer 2: Decision |
| Domain Analyses (per C-suite) | Card layout per domain, expandable team lead detail sections, scorecard infographic | 1-2 slides per domain (recommendation + key findings) | Section 3: Detailed Analysis, subsection per domain with team lead findings table | Layer 3: Analysis (full detail, every team lead finding) |
| Fault Line Analysis | Interactive/visual fault line section, agreement/contention infographic | "Where Perspectives Collide" slide with fault line map | Section 4: Risk & Disagreement Analysis | Layer 3: Analysis |
| Pre-Mortem Findings | Integrated into fault line section as failure mode callouts | Included in fault line slide or separate "Failure Modes" slide | Section 4 subsection: Pre-Mortem Failure Modes | Layer 3: Analysis |
| CEO Decision | Prominent decision callout with rationale, determinative perspective highlighted | "The Decision" slide + "Guardrails" slide | Section 5: Decision and Rationale | Layer 2: Decision |
| Dissenting Views | Sidebar/callout boxes with visual prominence (not buried) | "What Could Go Wrong" slide | Section 6: Counterarguments and Overruled Perspectives | Layer 2: Decision |
| Next Steps | Action plan section with timeline infographic, implied owners | "Next Steps" slide with action plan visualization | Section 7: Action Plan with owner/timeline table | Layer 2: Decision |
| Metadata | Footer/sidebar with decision classification | Closing slide with key metadata | Appendix A: Decision Metadata | Layer 2: Decision |

**Comparative Decision Record Mapping (Multi-Mode):**

| Comparative Section | HTML | PPTX | DOCX | Capsule PDF |
|---|---|---|---|---|
| Mode Comparison Executive Summary | Hero with per-mode decision summary cards | Title slide listing modes compared + summary slide | Opening paragraph covering all mode outcomes | Cover page with mode sensitivity indicator |
| Shared Analysis | Standard domain analysis section (presented once) | Standard domain slides (presented once) | Sections 1-4 identical to single-mode | Layers 2-3 include shared analysis |
| Per-Mode Synthesis | Tabbed or side-by-side mode panels, each showing decision + determinative perspective + key factor | Per-mode synthesis slides (1 slide each) | Section 5 subsections per mode | Layer 2 includes all mode syntheses |
| Divergence Analysis | Visual divergence section with mode comparison infographic | "The Key Choice" slide with divergence tree | Section 6: Divergence Analysis | Layer 2 |
| Mode Sensitivity | Visual indicator (gauge/spectrum) in executive summary area | Metadata on closing slide | Appendix B: Mode Sensitivity Analysis | Layer 2 metadata |

### Production Agent 1: Image Agent

The Image Agent creates analytical infographic visualizations of key decision dimensions. These are not decorative illustrations -- they are data visualizations that make complex multi-perspective analysis scannable at a glance.

**Five standard infographic types (generated for every production run):**

1. **Routing Diagram** — Which C-suite members were activated, the decision type classification, routing rationale, and which teams were excluded with reasoning. Visual: org chart with activated nodes highlighted, decision type badge, activation/exclusion annotations.

2. **Domain Scorecard** — Per-domain recommendation (Approve / Approve with Conditions / Oppose / Neutral) and confidence level (High / Medium / Low) as a visual matrix. Visual: grid/matrix with color-coded cells, each domain as a row with recommendation and confidence indicators.

3. **Fault Line Map** — Agreement and contention visualization showing where domains align and where they diverge, incorporating pre-mortem findings. Visual: radial or network diagram with domains as nodes, agreement edges (solid) and contention edges (dashed/red), with fault line labels on contention edges.

4. **Risk-Opportunity Matrix** — 2x2 impact/likelihood grid plotting the key risks and opportunities identified across all domain analyses. Visual: quadrant chart with risk items (from skeptic domains) and opportunity items (from advocate domains) plotted by impact and likelihood.

5. **Action Plan Timeline** — Gantt-style visualization of next steps with implied owners and timelines. Visual: horizontal timeline with action items, owner labels, and milestone markers.

6. **(Multi-mode only) Mode Comparison** — Divergence tree showing how different Decision Modes produced different synthesis outcomes from the same underlying analysis. Visual: tree diagram with shared analysis as root, branching into per-mode decisions, with divergence points highlighted.

**Style direction:** Professional, analytical, boardroom-appropriate. Think McKinsey deck graphics, not decorative art or abstract visualization. Clean lines, muted professional colors, clear labels, readable at presentation scale. Every element should convey information, not atmosphere.

**Technology:** Uses `mcp__claude-in-chrome__*` browser automation tools to operate ChatGPT's image generation capabilities. The Image Agent navigates to ChatGPT in Chrome, submits carefully crafted infographic generation prompts, waits for the generated image, and downloads it.

**Infographic generation prompt structure:**

For each infographic, the Image Agent:
1. Reads the Decision Record to extract the relevant data (e.g., domain recommendations and confidence levels for the scorecard)
2. Crafts an image generation prompt that specifies: the data to visualize, the chart/diagram type, the visual style (professional/analytical), the color palette (muted boardroom tones), and the labeling requirements
3. Submits via browser automation and downloads the result

**Output:** `{session-output}/images/INFOGRAPHIC_*.png`

When all images are complete, the Image Agent reports: **"All analytical infographics complete"** with a list of files produced.

### Production Agent 2: Presentation Agent

The Presentation Agent creates a board-ready PowerPoint presentation that structures the decision briefing for live presentation.

**Slide structure:**

| Slide | Content Source | Notes |
|---|---|---|
| Title | Decision Record header | Issue title, decision type, tier, date, mode |
| Executive Summary | Executive Summary section | The decision in 3-5 bullet points |
| The Question | Issue Statement | Problem context, business background |
| Analytical Framework | CEO Framing | Routing diagram infographic, evaluation dimensions, activated/excluded teams |
| Domain Analysis (1-2 per domain) | Domain Analyses | Per-domain: recommendation, confidence, key findings, team lead highlights. Scorecard infographic on first domain slide. |
| Where Perspectives Collide | Fault Line Analysis | Fault line map infographic, agreement/contention points, pre-mortem failure modes |
| The Decision | CEO Decision | Decision statement, most determinative perspective, rationale |
| Guardrails | CEO Decision (conditions) | Conditions drawn from skeptic roles, accepted risks, mitigations |
| What Could Go Wrong | Dissenting Views | Strongest objections from overruled perspectives |
| Next Steps | Next Steps | Action plan timeline infographic, owners, milestones |
| Decision Metadata | Metadata | Classification, complexity, dissent level, mode, key assumptions |

**Multi-mode variant:** Shared analysis slides presented once (The Question through Fault Lines), then per-mode synthesis slides (1 slide each: decision + determinative perspective + key factor), then a "The Key Choice" divergence slide with the mode comparison infographic and Mode Sensitivity indicator.

**Technology:** Uses `pptxgenjs` (Node.js) per the pptx skill's "Creating from Scratch" conventions. The build script is saved to `{session-output}/build/build_presentation.js` and is rerunnable.

**Design principles:**
- Bold, content-informed color palette appropriate to the decision domain (not generic blue)
- Visual element on every slide (infographic, data callout, structured table)
- Title font 36-44pt, body 14-16pt, stat callouts 60-72pt
- Dark background for title + closing, light for content slides
- No accent lines under titles
- Professional typography pairing (e.g., Georgia headers, Calibri body)

**Output:** `{session-output}/PRESENTATION_<issue-slug>.pptx` + build script at `{session-output}/build/build_presentation.js`

### Production Agent 3: Document Agent

The Document Agent creates an editable board document designed for executive review workflows. This is the artifact built for annotation, comments, tracked changes, and formal approval processes -- the document that gets redlined in a review cycle.

**Role:** Where the HTML page is for browsing and the PPTX is for presenting, the DOCX is for **collaborative editing**. Board members, advisors, and executives can add comments, suggest changes, highlight sections for discussion, and track the document through approval workflows. The content is identical to the HTML and PPTX -- the format serves a different consumption context.

**Technology:** `docx-js` (`docx` npm package), following the conventions established in the docx skill. Key implementation details:
- US Letter page size (12,240 x 15,840 DXA) with 1-inch margins
- Arial font family, 12pt default body text
- Override built-in heading styles (Heading1, Heading2, etc.) with `outlineLevel` for TOC support
- Tables with dual widths (`columnWidths` + cell `width`), `WidthType.DXA` only (never percentage), `ShadingType.CLEAR`
- Lists using `LevelFormat.BULLET` numbering config (never unicode bullets)
- Images via `ImageRun` with required `type` parameter and `altText`
- `PageBreak` inside `Paragraph` elements
- Build script validates output with `scripts/office/validate.py`

**Document structure:**

| Section | Content | Notes |
|---|---|---|
| Cover Page | Issue title, decision type, tier, date, mode, executive summary callout | Professional cover with key metadata |
| Table of Contents | Auto-generated from heading styles | `TableOfContents` with `headingStyleRange: "1-3"` |
| Section 1: Executive Summary | 3-5 sentence decision summary | Opening narrative, not bullet points |
| Section 2: Problem Statement | Issue as originally posed, business context | Sets the stage for the analysis |
| Section 3: Analytical Framework | CEO framing, evaluation dimensions, routing rationale | Table of activated/excluded teams with reasoning |
| Section 4: Detailed Analysis | Per-domain subsections with team lead findings | Embedded domain scorecard infographic, structured tables for findings |
| Section 5: Risk & Disagreement Analysis | Fault lines, pre-mortem findings, unresolved tensions | Embedded fault line map infographic, structured disagreement tables |
| Section 6: Decision and Rationale | Decision statement, determinative perspective, weight rationale | Prominent callout formatting for the decision itself |
| Section 7: Counterarguments | Strongest objections from overruled perspectives | Not buried -- given full subsections with reasoning |
| Section 8: Action Plan | Next steps with owners and timelines | Embedded action plan timeline infographic, structured table |
| Appendix A: Decision Metadata | Full metadata block | Classification, complexity, dissent level, mode, assumptions |
| Appendix B: Domain Detail | Expanded team lead findings (optional, for Tier 3) | Full team lead output for deep review |

**Formatting requirements:**
- Professional headers with document title and date
- Footers with page numbers (`PageNumber.CURRENT`)
- Consistent heading hierarchy (H1 for major sections, H2 for subsections, H3 for team lead entries)
- Tables for structured data (domain recommendations, team lead findings, action items)
- Embedded infographic images at readable scale with descriptive alt text
- Page breaks between major sections (cover, each numbered section, each appendix)
- Callout formatting for the decision statement (shaded background, larger font)
- Color-coded recommendation indicators in domain analysis tables (green for Approve, amber for Conditions, red for Oppose, gray for Neutral)

**Multi-mode variant:** Sections 1-5 present the shared analysis. Section 6 has subsections per mode (6.1 Guardian Synthesis, 6.2 Pioneer Synthesis, etc.). Section 7 becomes Divergence Analysis. An additional Appendix C covers Mode Sensitivity.

**Output:** `{session-output}/REPORT_<issue-slug>.docx` + build script at `{session-output}/build/build_report.js`

### Production Agent 4: Web Page Agent

The Web Page Agent creates a polished, self-contained interactive HTML page that serves as the primary distribution artifact -- the designed, definitive rendering of the decision briefing.

**Blocked until Image Agent, Presentation Agent, AND Document Agent complete.** Three predecessors (vs. two in the Ideation skill) because the download section must link to both the PPTX and DOCX files.

**Page structure:**

- **Hero section** — Issue title, decision type badge, tier indicator. Prominent decision callout showing the conclusion upfront. Key takeaway in 1-2 sentences.
- **Executive Summary** — The full 3-5 sentence summary with the decision, reasoning, and primary dissent.
- **Problem Context** — The issue as originally posed, business background, why this decision matters.
- **Analytical Framework** — How the issue was decomposed. Routing diagram infographic showing which domains were activated and why. Evaluation dimensions.
- **Domain Analysis cards** — One visual card per activated C-suite domain, each showing: recommendation badge (Approve/Oppose/Conditions/Neutral), confidence level, synthesis summary, expandable team lead detail sections. Domain scorecard infographic embedded in this section.
- **Fault Line Visualization** — The most valuable analytical section, given visual prominence. Fault line map infographic, agreement/contention points listed, pre-mortem failure modes in callout boxes.
- **The Decision** — Prominent decision callout with full rationale. Most determinative perspective highlighted. Conditions and guardrails. Risk-opportunity matrix infographic.
- **Dissenting Views** — Given visible placement (not hidden). Strongest objections with full reasoning, presented as sidebar/callout elements.
- **Action Plan** — Timeline visualization with action plan infographic. Owners, timelines, milestones.
- **Download Section** — Links to PPTX and DOCX files via relative paths (`PRESENTATION_<issue-slug>.pptx`, `REPORT_<issue-slug>.docx`).
- **Metadata** — Decision classification, complexity, dissent level, mode, key assumptions. Footer/sidebar treatment.
- **Navigation** — Smooth scrolling, table of contents or nav bar for jumping between sections.

**Design principles (same as Ideation skill):**
- Self-contained: everything in one HTML file (CSS and JS inline)
- No external dependencies (no CDN links, no frameworks)
- Works when opened directly from the filesystem (`file://` protocol)
- Accessible and readable on different screen sizes
- Good typography, readable layout, cohesive color scheme, responsive design
- This is the artifact people will actually look at -- it should feel like a designed product, not a document dump

**PDF-compatibility requirements (for Archivist):**
- Scroll-triggered reveal animations use simple, class-name-based patterns (`.reveal` with `opacity: 0`, JS adds `.visible`) so the Archivist's print CSS can override them
- Avoid layout techniques depending on viewport units for critical sizing
- `backdrop-filter` not supported in weasyprint -- use solid fallback backgrounds
- CSS custom properties (`var(--name)`) supported and encouraged
- Fixed-position elements (nav bar) will be hidden in PDF

**Multi-mode variant:** Hero section shows per-mode decision summary cards. Domain analysis section presented once (shared). After "The Decision" section, a tabbed or side-by-side "Mode Comparisons" section shows each mode's synthesis. A "Divergence Analysis" section with the mode comparison infographic follows. Mode Sensitivity indicator in the metadata section.

**Output:** `{session-output}/index.html`

### Production Agent 5: Archivist

The Archivist produces two PDF artifacts: the Results PDF (a print-portable rendering of the distribution page) and the Deliberation Capsule PDF (a comprehensive layered archive of the entire deliberation process).

**Blocked until the Web Page Agent completes.** The Results PDF is a direct rendering of `index.html`, so the finished page must exist before the Archivist can start.

**Technology:** Python build script using `weasyprint` for HTML-to-PDF rendering. Fallback to `pdfkit` with `wkhtmltopdf` if weasyprint is unavailable.

#### Results PDF

**Purpose:** Print-portable version of the distribution page. Same content, same design, PDF format. The "share via email" artifact.

**Filename:** `{session-output}/RESULTS_<issue-slug>.pdf`

**Build process:**
1. Read `{session-output}/index.html`
2. Convert all relative image paths (`images/*.png`) and CSS `url()` references to base64 data URIs for self-containment
3. Inject print-friendly CSS: `@page` rules for A4/Letter sizing, page break hints at section boundaries, remove fixed navigation, disable transitions/animations/hover/`backdrop-filter`, readable font sizes for print, tightened section padding
4. Neutralize scroll-reveal animations: force `.reveal { opacity: 1 !important; transform: none !important; }` and similar overrides for any JS-dependent visibility classes
5. Strip all `<script>` blocks
6. Render to PDF via `weasyprint`

The content is identical to the distribution page. The Archivist converts format, not content.

#### Deliberation Capsule PDF

**Purpose:** Comprehensive, layered archive of the entire deliberation process. Unlike the other four artifacts (which present only the synthesized decision briefing), the Capsule contains the full analytical record: every domain analysis, every team lead finding, the CEO's routing rationale, Phase 4.5 pre-mortem responses, and the original issue submission.

**Filename:** `{session-output}/CAPSULE_<issue-slug>.pdf`

**Structure (Cover + 5 layers):**

| Section | Contents | Source |
|---|---|---|
| **Cover** | Issue title (large), decision statement, decision mode, date, tier, key infographic (routing diagram thumbnail) | Decision Record header |
| **Layer 1: Overview** | Table of contents with page references, content inventory listing every artifact included with type and source. Structured for both human scanning and AI agent parsing. | Generated from all contents |
| **Layer 2: Decision** | Executive summary, issue statement, CEO framing, decision with rationale, conditions and guardrails, dissenting views, next steps, metadata. The synthesized decision briefing in full. | Decision Record |
| **Layer 3: Analysis** | Full domain analyses (every C-suite domain at full detail), every team lead finding (not summarized), all infographic images at readable size, fault line analysis with pre-mortem findings, risk-opportunity matrix. | Domain analysis data, `images/` |
| **Layer 4: Process** | CEO framing rationale and routing decisions, activation/exclusion reasoning, Phase 4.5 pre-mortem challenge responses (each C-suite member's failure mode analysis), decision mode selection rationale. | Process artifacts |
| **Layer 5: Context** | Original issue as submitted by the user, any reference materials provided, company profile configuration used, routing table configuration. | User input, config files |

**Multi-mode Capsule variant:** Layer 2 includes all mode syntheses and the Divergence Analysis. Layer 4 includes mode selection rationale and Mode Sensitivity analysis.

**Design principles:**
- **"The capsule is the frame. The content is the art."** — Deliberately neutral design (consistent typography, clean layout, clear section dividers) while the decision content carries its own analytical voice.
- **Temperature-neutral** — The capsule presents what happened with structural clarity, not interpretive spin.
- **Plain-language layer names** — "Decision", "Analysis", "Process", "Context" -- not jargon.
- **Dual-audience Overview** — Layer 1 readable by a human scanning for content AND parseable by an AI agent looking for structured metadata.
- **Handle variable content gracefully** — Tier 2 `--produce` runs have less content than Tier 3 full cascades. Some runs activate 3 C-suite domains, others activate all 7. The layout accommodates variability without breaking or looking sparse.

**Build script:** `{session-output}/build/build_capsule.py` produces both PDFs in one run and is rerunnable (`python3 build_capsule.py` from the `build/` directory regenerates both from current artifacts).

**Output:** `{session-output}/RESULTS_<issue-slug>.pdf` + `{session-output}/CAPSULE_<issue-slug>.pdf` + build script

### Production Phase Quality Standards

The production artifacts represent the skill's outward face -- the thing users actually share, present, and archive. Quality standards are non-negotiable:

1. **Content consistency across formats.** The same decision, rationale, analysis, and action plan must appear in HTML, PPTX, DOCX, and Results PDF. Spot-check by comparing executive summaries and next steps across formats.

2. **DOCX must be genuinely editable.** Not a static document that happens to be in `.docx` format. Comments must be addable, tracked changes must work, text must be modifiable. The build script validates with `scripts/office/validate.py`.

3. **Infographics must be analytical, not decorative.** Routing diagrams show actual routing decisions. Scorecards show actual recommendation/confidence data. Fault line maps show actual agreement/contention patterns. If an infographic could apply to any decision, it is not analytical enough.

4. **The HTML distribution page must feel like a designed product.** Not a document dump with syntax highlighting. Professional typography, cohesive color scheme, responsive layout, smooth navigation. This is the artifact that determines whether users return to the skill.

5. **The Capsule PDF must be a complete institutional record.** A reader with no prior context should be able to reconstruct the entire deliberation from the Capsule alone -- the issue, the framing, the analyses, the disagreements, the decision, and the reasoning.

---

## Future Directions (v2 and Beyond)

### Decision Revisitation

Revisit decisions when assumptions change. The Metadata section of every Decision Record captures Key Assumptions. When conditions change, the user can invoke a targeted re-analysis that:
- Identifies which assumptions have been invalidated
- Re-runs only the affected domain analyses
- Produces a Decision Amendment rather than a full new record
- Highlights what changed in the recommendation and why

This transforms the skill from a point-in-time decision tool into a decision lifecycle manager.

### Scenario Forking Engine

Parallel cascades with different parameters producing comparative decision landscapes. Not just "what should we do?" but "what happens if we do X vs. Y vs. Z?" The CEO Personality / Decision Mode concept is a special case of this -- same analysis, different synthesis. Full scenario forking extends this to different issue parameters producing different analyses entirely. Output: a Decision Landscape showing how different assumptions and approaches lead to different outcomes.

### Organizational Stress Test Mode

Invert the cascade. Instead of top-down issue resolution, bottom-up threat and opportunity discovery. Each C-suite agent generates issues from their domain perspective: "What keeps you up at night? What opportunity are we missing?" Output: an Organizational Health Report that surfaces risks and opportunities the user has not yet articulated. McChrystal calls this "getting a full physical instead of going to the doctor with a complaint."

### Institutional Memory

Persistent knowledge across sessions. Roles maintain context about previous decisions, the company's history, and evolving constraints. Previous Decision Records inform current analysis. The system learns the company's patterns and can reference them.

### Cross-Functional Deliberation (Full Phase 4.5)

Beyond the one-round pre-mortem, a full cross-functional challenge where C-suite agents debate each other's recommendations. Research cautions about "problem drift" in multi-round debates, so this requires careful scoping -- perhaps structured around specific fault lines rather than open-ended debate.

### Custom Decision Modes and Decision Pattern Analysis

Users define their own synthesis postures beyond the five defaults: "I'm generally growth-oriented but conservative on anything involving regulatory risk." The CEO's synthesis prompt becomes a user-configurable profile representing their actual leadership style. Over time, the system surfaces patterns in mode selection: "You've chosen the growth-oriented path in 8 of the last 10 decisions. Your CFO's concerns were overridden 6 times. Consider whether the conservative perspective is being systematically underweighted." This is not just decision support -- it is leadership coaching.

### Framework Versioning and Community Contribution

Analytical framework packages versioned and improved independently. Industry-specific variants override defaults. Community-contributed domain frameworks. The skill becomes a platform for organizational reasoning patterns, not just a fixed set of 29 perspectives.

---

## Builder Agent Instructions

The builder agent receiving this specification should construct the skill in the following order:

1. **Skill scaffolding:** Create the `.claude/skills/corporate-decision-panel/` directory with `skill.md` front matter, output templates, routing table, and company profile configuration. The company profile must implement archetype presets (Technology/SaaS default + at least one additional) with the configuration format specified in "Company Profile Configuration" above.

2. **CEO agent definition:** Create `ceo.md` with the five-phase cascade protocol, routing logic, fault-line analysis methodology, and modular Decision Mode system. The Phase 1 framing prompt must include the five full-activation threshold conditions specified in "Full-Activation Threshold Conditions" above.

3. **CFO domain (reference implementation):** Create the CFO C-suite agent and all five CFO team lead subagent definitions using the reference implementation from Report #3. This domain is fully specified and serves as the template.

4. **Remaining C-suite agents:** Create the 6 remaining C-suite agent definitions following the CFO pattern: role identity, mandate, disposition, team composition, operating modes, synthesis instructions. Each C-suite agent's Mode A (Tier 1) prompt must include the structured internal checklist specified in "Mode A Structured Internal Checklists" above and the escalation brief capability specified in "Tier Escalation with Context Carry" above.

5. **Remaining team lead subagents (24):** Create the team lead subagent definitions for all remaining domains. Each must have a unique analytical framework, mandatory output template, and three forcing questions. The 14 team leads in the 7 high-interaction pairs must also include a fourth "Cross-Domain Challenge" forcing question as specified in "Cross-Domain Forcing Question Pairs" above. Use the CFO team leads as the quality benchmark. No two team leads should produce the same type of analysis for the same issue.

6. **Invocation commands:** Implement `/consult`, `/panel`, `/deliberate`, and `/evaluate` with tier routing and mode selection. The `/evaluate` command must include both tier and mode recommendations as specified in "Auto-Triage" above.

7. **Decision Mode overlays:** Create all five CEO synthesis prompt modifiers (Guardian, Pioneer, Architect, Analyst, Sentinel) with their complete prompt text. Implement the multi-mode comparison mechanism: single-mode invocation, two-mode comparison, and all-modes invocation.

8. **Comparative Decision Record template:** Create the Comparative Decision Record format with shared analysis section, per-mode synthesis sections, divergence analysis, and Mode Sensitivity metric. Ensure the mode/tier interaction matrix is reflected in how each mode behaves at each tier.

9. **Production pipeline:** Implement the production trigger mechanism (always for Tier 3, `--produce` flag for Tier 2, never for Tier 1). Create spawn prompts for all five production agents (Image Agent, Presentation Agent, Document Agent, Web Page Agent, Archivist) with full dependency pipeline (A/B/C parallel → D blocked by A+B+C → E blocked by D). Implement the content mapping logic that translates Decision Record sections into the synthesized narrative briefing format. The Document Agent uses `docx-js` (`docx` npm package), the Presentation Agent uses `pptxgenjs`, and the Archivist uses `weasyprint`. Create the four production templates in `templates/production/` (decision-briefing-page.md, board-presentation.md, board-document.md, capsule-structure.md).

10. **Production validation:** Run the production pipeline on the stress test Decision Record from step 9. Verify: (a) all five artifacts are generated without errors, (b) content is consistent across HTML, PPTX, DOCX, and Results PDF (spot-check executive summary and next steps), (c) DOCX passes `scripts/office/validate.py` and is genuinely editable (open in a word processor, add a comment, modify text), (d) infographics are analytical (routing diagram shows actual routing, scorecard shows actual recommendations, fault line map shows actual contention), (e) HTML distribution page loads correctly from `file://` protocol with working navigation and infographic images, (f) Results PDF renders all content (no invisible elements from scroll-reveal animations), (g) Capsule PDF contains all five layers with complete content.

11. **Final validation:** Run the onboarding stress test -- a representative cross-functional issue through the full Tier 3 cascade with production -- and verify that all 29 perspectives produce genuinely different analysis. Execute the Mode Calibration Protocol: run the stress test issue (which must be deliberately contentious) through all five modes, verify that at least 3 of 5 modes produce materially different outcomes (different decision, or same decision with substantially different conditions/guardrails), and log calibration results in the company profile. If fewer than 3 modes diverge, revise the prompt modifiers before considering the skill calibrated. Verify that the complete pipeline from issue submission through production artifact delivery works end-to-end.

**Quality criteria for the builder agent:**
- Each team lead's output must be structurally different from every other team lead's output. If two team leads produce similar analysis for the same issue, their frameworks need revision.
- The Fault Line Analysis section should surface genuine disagreements, not manufactured ones. If all domains agree, say so -- do not force conflict.
- Decision Records should be self-contained documents that a reader can understand without context about the system that produced them.
- The skill should feel like consulting with an executive team, not filling out a form. Tone should be professional, direct, and opinionated -- not hedged or bureaucratic.
- Decision Modes must produce meaningfully different synthesis. If Guardian and Pioneer reach the same conclusion for a contentious issue, the prompt modifiers are not distinct enough. Mode Sensitivity should be high for controversial decisions and low for clear-cut ones.
- Production artifacts must present consistent information across all four briefing formats (HTML, PPTX, DOCX, Results PDF). The Capsule PDF is exempt from this requirement as it contains additional process content.
- The DOCX must be genuinely editable -- comments addable, tracked changes functional, text modifiable. A `.docx` file that breaks when opened in Word or Google Docs is a build failure.
- Infographics must be analytical, not decorative. Every visual element should convey decision-specific data. A routing diagram must show the actual routing for this decision. A scorecard must show actual domain recommendations and confidence levels. Generic or abstract infographics are a quality failure.
- The HTML distribution page must feel like a designed product, not a document dump. Professional typography, cohesive color scheme, responsive layout. This is the artifact that determines whether users adopt the skill for daily use.

---

## Source Materials

- Concept seed: `session/sources/team-of-teams.txt`
- Idea Report #1: `session/idea-reports/IDEA_cascading-deliberation-engine.md`
- Idea Report #2: `session/idea-reports/IDEA_engagement-model.md`
- Idea Report #3: `session/idea-reports/IDEA_cognitive-forcing-prompt-architecture.md`
- Idea Report #4: `session/idea-reports/IDEA_decision-modes-decision-space.md`
- Research: `session/research/RESEARCH_team-of-teams-methodology.md`
- Research: `session/research/RESEARCH_multi-agent-orchestration.md`
- Research: `session/research/RESEARCH_claude-agent-teams.md`
- Research: `session/research/RESEARCH_smb-decision-making.md`
- Research: `session/research/RESEARCH_implementation-viability-routing.md`
- Open questions resolution: `session/OPEN_QUESTIONS_RESOLUTION.md`
- Session summary: `session/SESSION_SUMMARY.md`
- Idea briefs: `session/briefs/`
- Ideation graph: `session/ideation-graph.md`
- Version snapshots: `session/snapshots/`
