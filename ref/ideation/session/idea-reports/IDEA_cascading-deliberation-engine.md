# Idea Report: The Cascading Deliberation Engine

**Direction explored by:** Free Thinker + Grounder
**Report number:** 1
**Related threads:** Cascade architecture, engineered dissent, org roster design, decision record format

---

## The Idea

The "Team of Teams" Agent Skill should be architected as a **Cascading Deliberation Engine** — a five-phase process that transforms any business issue into a rich, multi-perspective analysis and a structured decision. The architecture emulates the top two layers of an SMB org chart (CEO + C-suite + team leads) but implements it as a two-tier agent system: 8 real Agent Team instances (CEO + 7 C-suite officers), where each C-suite agent internally simulates their team leads by performing sequential analytical passes through each specialist's lens.

The engine works through cascading decomposition: the CEO frames the issue and routes it to relevant C-suite members, each C-suite member translates the framing into domain-specific questions for their team leads, the team lead perspectives produce focused findings, the C-suite member synthesizes upward, and the CEO deliberates across all domain recommendations to produce a final decision. The output is a comprehensive Decision Record — a self-contained document that captures not just the decision, but the full reasoning chain, fault lines, dissenting views, and assumptions behind it.

What makes this more than "ask a panel of experts" is **engineered dissent**. Disagreement is produced through two mechanisms: organic dissent (different domain lenses naturally produce different conclusions) and mandated dissent (specific roles carry explicit skeptic or advocate dispositions baked into their prompts). The CISO is the "Constitutional Skeptic" — their default is that change introduces risk. The CFO is the "Cost Archaeologist" — they find the costs that aren't in the proposal. The VP of Sales is the "Revenue Optimist" — they find the growth opportunity. These structural tensions produce analysis that's richer than consensus.

## The Key Insight

Organizational decision-making quality comes not from collecting opinions but from **structurally engineering productive conflict** across domain perspectives, then synthesizing through fault-line analysis rather than majority vote.

## How We Got Here

The Free Thinker's opening identified five potential directions. The Grounder selected the cascading delegation pattern (#3) and the dissent problem (#2) as the load-bearing ideas, and asked the Free Thinker to fuse them into mechanics. The resulting five-phase cascade model emerged with adversarial vs. advocacy mandates for each role. The Grounder then pushed for concrete deliverables: the full org roster with mandates and the decision record format. When the 37-role roster materialized, the Grounder proposed the two-tier agent architecture (8 real agents, 37 conceptual roles) as the pragmatic implementation model, and identified routing as a core feature rather than an optimization.

## The Grounder's Take

- **Does this connect to what was asked for?** Directly. The concept seed asks for a skill that "realistically emulates a SMB's org structure to make decisions and answer questions on issues." This architecture does exactly that — with the added benefit that it produces better decisions than a real org because it strips out politics and information asymmetry while preserving productive structural tensions.
- **Would the audience care?** Yes. The user wants a spec for a builder agent. This gives them the core architecture — the thing the builder agent needs to understand first before building anything. The five-phase process, the role roster, and the decision record are all directly spec-able.
- **Is this one of the good ones?** This is THE one. Everything else we discuss will be features, refinements, or extensions of this core architecture.

## The Free Thinker's Vision

At its most ambitious, this is a **boardroom in a box** — a system where a solo founder or small leadership team can pressure-test any decision against the collective analytical power of a full executive team. Not just "what should I do?" but "show me how a CFO, CISO, CTO, COO, CAO, VP of Sales, and VP of Delivery would each analyze this, where they'd disagree, and why." Every decision gets the rigor of a well-run executive committee, with the structural integrity of mandated dissent ensuring that risk, cost, opportunity, and execution reality are all represented — even when the human user might prefer to hear only good news.

The Decision Record becomes an institutional artifact — something you refer back to, challenge when conditions change, and use to build organizational memory over time. Future extensions include: **CEO personality profiles** (running the same issue through different synthesis styles — risk-averse, growth-oriented, consensus-builder — to see how different leadership dispositions produce different decisions from identical analysis), cross-functional C-suite deliberation (Phase 4.5), persistent institutional memory across sessions, and the ability for roles to request additional research mid-analysis.

## Architecture Summary

### Five-Phase Process
1. **CEO Frames** — Decomposes the issue into evaluation dimensions, classifies decision type, routes to relevant C-suite members
2. **C-Suite Dispatches Downward** — Each C-level translates the framing into domain-specific questions for their team leads (an analytical act, not just forwarding)
3. **Team Leads Produce Findings** — Narrow, focused analysis through specialist lenses (simulated within each C-suite agent)
4. **C-Suite Synthesizes Upward** — Each C-level collects team findings and produces a domain recommendation with confidence level
5. **CEO Deliberates** — Identifies fault lines, weights perspectives by decision type, synthesizes a decision that addresses the strongest objections

### Two-Tier Agent Architecture
- **Tier 1 (8 real agents):** CEO, COO, CFO, CTO, CISO, CAO, VP of Sales, VP of Delivery
- **Tier 2 (29 simulated perspectives):** Team leads represented as sequential analytical passes within each C-suite agent's processing

### Engineered Dissent Model

| Role | Disposition | Mandate |
|------|------------|---------|
| CEO | Synthesizer | "You frame, listen, weigh, and decide. Your value is judgment, not expertise." |
| COO | Execution Realist (Skeptic) | "Can we actually do this with the people and processes we have?" |
| CFO | Cost Archaeologist (Skeptic) | "Find the costs that aren't in the proposal." |
| CTO | Capability Expander (Advocate) | "What does this make possible that wasn't possible before?" |
| CISO | Constitutional Skeptic (Skeptic) | "Your default is that change introduces risk. You are the org's immune system." |
| VP of Sales | Revenue Optimist (Advocate) | "How does this help us sell more, faster, or to new markets?" |
| VP of Delivery | Promise Keeper (Skeptic) | "What do we sacrifice from existing commitments to do this?" |
| CAO | Org Gravity Sensor (Neutral) | "Can the organization — people, policies, culture — absorb this?" |

### Full Organizational Roster (29 Team Leads)

**COO Team Leads:**
- Operations Manager — day-to-day workflow and capacity impact
- Process/Quality Lead — standards, efficiency, and operational compliance
- Vendor/Procurement Manager — external dependencies and supply chain
- Facilities/Office Manager — physical/logistical infrastructure (conditional on company type)

**CFO Team Leads:**
- Controller — accounting accuracy, GAAP implications, audit risk
- Head of FP&A — financial modeling and scenario planning
- Treasury/Cash Manager — liquidity, funding, and cash flow impact
- AP/AR Manager — payables/receivables cycle implications
- Tax Lead — tax structure and external counsel needs

**CTO Team Leads:**
- Engineering Lead — development effort, architecture, technical debt
- Infrastructure/DevOps Lead — platform, scaling, deployment, reliability
- Data/Analytics Lead — data architecture, integration, reporting
- Product/UX Lead — product roadmap and user experience (may reassign per company profile)

**CISO Team Leads:**
- Security Operations Lead — threat landscape and incident response
- Compliance/GRC Lead — regulatory compliance and governance
- Identity & Access Lead — authentication, authorization, data access
- Security Architecture Lead — security by design, encryption, data protection

**VP of Sales Team Leads:**
- Sales Operations Lead — pipeline, forecasting, deal velocity
- Account Management Lead — retention, expansion, client satisfaction
- Business Development Lead — new markets, partnerships, channels
- Sales Enablement Lead — tools, training, and execution readiness

**VP of Delivery Team Leads:**
- Project/Program Manager — portfolio scheduling, resourcing, timelines
- Resource Manager — talent allocation and hiring needs
- Client Success Lead — service quality, SLAs, client experience
- QA/Delivery Standards Lead — quality standards and delivery methodology

**CAO Team Leads:**
- HR/People Ops Lead — hiring, morale, skills gaps, change management
- Legal/Contracts Lead — legal exposure, IP, regulatory obligations
- Admin/Policy Lead — internal policies and procedures
- Corporate Communications Lead — internal/external messaging

### Routing Mechanism
- Decision-type classification (Strategic, Operational, Financial, Technical, Personnel, Compliance/Risk)
- Default routing table mapping decision types to C-suite roles
- CEO override capability
- Full-activation triggers for major decisions (acquisition, pivot, layoff)

### Decision Record Output

```
EXECUTIVE SUMMARY
[3-5 sentences: the decision, key reasoning, primary dissent]

DECISION RECORD: [Issue Title]
Decision ID: [auto-generated]
Date: [timestamp]
Submitted by: [user]
Decision Type: [Strategic / Operational / Financial / Technical / Personnel]

1. ISSUE STATEMENT
   [The question as originally posed]

2. CEO FRAMING
   [Decomposition into evaluation dimensions]
   Activated Teams: [roles engaged + rationale for inclusion]
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
   Unresolved Tensions: [surfaced but unresolvable with current info]

5. CEO DECISION
   Decision: [clear statement]
   Most Determinative Perspective: [which domain was weighted highest and why]
   Decision Weight Rationale: [why certain perspectives carried more weight
                               for this type of decision]
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

## Open Threads

- **Company Profile Configuration:** How is the skill parameterized for different company types (B2B SaaS vs. professional services vs. manufacturing)? The roster and role mandates may shift based on company profile.
- **Cross-Functional Deliberation (Phase 4.5):** Should C-suite members be able to challenge each other's recommendations before CEO synthesis? Identified as v2 feature.
- **Institutional Memory:** Can roles maintain persistent knowledge across sessions? Identified as future enhancement due to scope complexity.
- **Prompt Architecture:** How exactly should the C-suite prompts be structured to enable both domain decomposition and team-lead perspective simulation?
- **CEO Personality Profiles:** Can different CEO synthesis styles (risk-averse, growth-oriented, consensus-builder) produce meaningfully different decisions from identical domain analyses?
- **Lightweight Mode:** For simple questions, is there a "quick consult" mode that skips the full cascade?
- **User Interaction Model:** How does the human invoke the skill, provide context, and interact with the output?
- **Implementation Mapping:** How do the 8 agents technically map to Claude Code Agent Teams orchestration patterns?

## Recommendation to Arbiter

**Strongly recommended as the core architecture for the spec.** This isn't one idea among many — it's the foundational design pattern that everything else in the spec will build on. The five-phase cascade, the two-tier agent model, the engineered dissent, the routing mechanism, and the decision record format together form a complete, coherent, and buildable architecture. Flag as "interesting" — or more accurately, flag as "essential."
