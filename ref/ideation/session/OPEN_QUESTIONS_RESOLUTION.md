# Open Questions Resolution: Corporate Decision Panel v1

**Session:** Corporate Decision Panel Agent Skill Ideation
**Date:** 2026-02-22
**Purpose:** Resolves the eight genuinely open questions from the ideation session that affect the v1 build. Two questions were already resolved by the Vision document (Phase 0 broadcast mechanism, Phase 4.5 v1 scope). Several are explicitly deferred to v2 (custom blended modes, institutional memory, framework versioning, leadership coaching patterns).

---

## Resolution Summary

| # | Question | Resolution | Implementation | Complexity |
|---|----------|-----------|----------------|------------|
| 1 | Full-activation trigger rules | CEO judgment with threshold conditions in framing prompt | Prompt addition to CEO Phase 1 | Low |
| 2 | Company profile roster modification | Archetype presets with individual overrides | Config design + 2-4 presets | Medium |
| 3 | Mid-conversation tier escalation | Escalation recommendation with structured context brief | Prompt addition to C-suite Tier 1 | Low |
| 4 | Tier 1 internalization quality | Structured internal checklist per C-suite agent | Prompt addition to C-suite Mode A | Low |
| 5 | Cross-domain forcing questions | Selective questions for 5-8 high-interaction team lead pairs | Pair identification + 10-16 questions | Medium |
| 6 | CEO auto-recommending decision mode | Mode recommendation in `/evaluate` auto-triage | Prompt extension to CEO `/evaluate` | Low |
| 7 | Mode distinctiveness verification | Multi-mode calibration in onboarding stress test | Stress test extension | Low |

Five of seven resolutions are prompt-level changes requiring no architectural modifications. Two require medium-effort content design (archetype presets, cross-domain pair mapping). None require changes to the cascade mechanism, agent architecture, or production pipeline.

---

## Question 1: Full-Activation Trigger Rules

**The Problem:** The routing table maps decision types to default C-suite subsets (e.g., Strategic -> CEO, CFO, CTO, VP Sales). The spec mentions "full-activation triggers" for major decisions but only provides three examples (acquisition, pivot, layoff) with no complete rule set or threshold definitions.

**Options Considered:**
- **A: Keyword-Based Trigger List** -- Static list of trigger keywords/phrases. Simple but brittle; misses novel situations.
- **B: CEO Judgment with Override Prompt** -- Add threshold conditions to the CEO's framing phase prompt. Leverages CEO reasoning rather than pattern matching.
- **C: Two-Stage Routing with Escalation** -- Each C-suite agent can flag cross-cutting implications and recommend additional activations mid-cascade. Realistic but adds latency and complexity.

**Resolution: Option B -- CEO Judgment with Threshold Conditions**

The CEO's Phase 1 framing prompt already includes activation reasoning and exclusion rationale. Five threshold conditions are added to that prompt:

> "After classifying the decision type and selecting default routing, assess whether the issue has cross-cutting implications that warrant full activation. If any of these conditions apply, activate all C-suite:
> 1. The decision is practically irreversible
> 2. The decision affects >30% of headcount
> 3. The decision changes the company's market position or business model
> 4. The decision involves existential financial risk
> 5. You are uncertain which domains are relevant
>
> State your activation reasoning in the CEO Framing section."

**Rationale:** The five conditions cover the spec's examples (acquisition -> irreversible + market position; layoff -> headcount; pivot -> business model) while catching novel situations via the uncertainty clause. No additional mechanism needed beyond a prompt addition. The reasoning is visible in the Decision Record (CEO Framing section), maintaining the spec's principle that "routing is an analytical act."

---

## Question 2: Company Profile Roster Modification

**The Problem:** The spec acknowledges different company types need different role structures but provides no concrete rules for conditional activation, role reassignment, or profile configuration format.

**Options Considered:**
- **A: Binary Activation Flags** -- Each team lead has `active: true/false` and optional `reports_to` override. Simple but 29 toggle decisions is heavy onboarding.
- **B: Company Archetype Presets** -- 3-4 presets that configure roster, default mode, and frameworks. Users select one and override as needed.
- **C: Dynamic Roster via CEO Assessment** -- No static config; CEO assesses relevance per-decision. Zero config but inconsistent.

**Resolution: Option B -- Company Archetype Presets with Individual Overrides**

Four company archetype presets:

**1. Technology / SaaS (default)**
- Facilities/Office Manager: inactive
- Product/UX Lead: reports to CTO
- Default decision mode: Analyst
- Compliance focus: SOC 2, GDPR
- Pioneer-leaning defaults for growth-stage companies

**2. Professional Services**
- All roles active
- VP Delivery weighted heavily in routing defaults
- Default decision mode: Architect
- Client-centric framing in COO and VP Sales domains

**3. Regulated Industry (healthcare, finance)**
- All roles active
- Compliance/GRC Lead: expanded scope with industry-specific frameworks
- Default decision mode: Guardian
- Industry-specific compliance: HIPAA (healthcare), SOX (finance), PCI-DSS (payments)

**4. Manufacturing / Physical Operations**
- Facilities/Office Manager: active
- Supply chain emphasis in COO domain
- Vendor/Procurement Manager weighted heavily
- Default decision mode: Analyst

**Configuration format:**

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

**Rationale:** Archetype presets give the best ratio of configuration simplicity to roster accuracy. One choice gets 80% configured. The onboarding stress test validates the preset before real use. The builder agent should ship with at least Technology/SaaS (default) and one additional preset to demonstrate the pattern.

---

## Question 3: Mid-Conversation Tier Escalation

**The Problem:** If a user asks a "hallway question" (Tier 1) and the C-suite agent realizes mid-response that the issue is actually multi-domain or high-stakes, can the system escalate to Tier 2?

**Options Considered:**
- **A: No Mid-Conversation Escalation** -- Tier selection is final. C-suite agent suggests escalation in Advisory Note. User re-invokes.
- **B: Escalation Recommendation with Context Carry** -- Same as A, but the C-suite agent produces a structured Escalation Brief alongside the Advisory Note, preserving Tier 1 analysis for the higher-tier invocation.
- **C: Automatic Escalation with Confirmation** -- C-suite agent triggers escalation; system prompts user for confirmation and spawns higher-tier cascade automatically.

**Resolution: Option B -- Escalation Recommendation with Structured Context Brief**

The C-suite agent's Tier 1 (Mode A) prompt includes:

> "If you determine this issue has significant cross-domain implications, produce your Advisory Note as normal AND append an Escalation Brief: a structured summary of your initial findings, the cross-domain implications you've identified, and a recommended tier and routing. Format the brief so it can be passed as context to a higher-tier invocation."

**Escalation Brief format:**

```
--- ESCALATION BRIEF ---
Initial Domain: [your role]
Initial Finding: [1-2 sentence summary]
Cross-Domain Implications: [which other domains are affected and why]
Recommended Escalation: [Tier 2 /panel or Tier 3 /deliberate]
Recommended Routing: [which C-suite roles should be activated]
Key Context for Escalated Analysis: [findings the higher tier should build on]
---
```

**Rationale:** Delivers 90% of automatic escalation's value (context preservation, clear guidance) with 10% of the implementation complexity (prompt addition only). Preserves the spec's principle that "the user matches engagement to decision weight" -- escalation is a user choice. Option C is a natural v2 evolution if the manual step proves friction-heavy.

---

## Question 4: Tier 1 Internalization Quality

**The Problem:** In Tier 1, the C-suite agent reasons through team lead perspectives internally rather than spawning subagents. The spec specifies the mechanism but not how to ensure quality without subagent isolation.

**Options Considered:**
- **A: Accept the Trade-off** -- Tier 1 is "quick and opinionated." Quality is adequate for hallway questions.
- **B: Structured Internal Checklist** -- Add a brief checklist to each C-suite agent's Mode A prompt forcing explicit consideration of each team lead perspective.
- **C: Lightweight Subagent Delegation** -- Spawn team lead subagents in Tier 1 with reduced scope. Defeats Tier 1's speed/cost advantage.

**Resolution: Option B -- Structured Internal Checklist per C-Suite Agent**

Each C-suite agent's Mode A (Tier 1 Direct Consult) prompt includes a domain-specific internal checklist. Example for CFO:

> "Before producing your Advisory Note, briefly consider each team lead perspective:
> - Controller: Any accounting treatment or compliance implications?
> - FP&A: What are the rough financial scenarios (best/worst/likely)?
> - Treasury: Any cash flow timing concerns?
> - AP/AR: Any working capital cycle impact?
> - Tax: Any tax structure implications?
> Note which perspectives are relevant and which are not. Include only relevant perspectives in your Advisory Note."

**Checklists for all C-suite agents:**

**COO:**
> - Operations Manager: Any operational workflow or capacity implications?
> - Process/Quality Lead: Any process compliance or quality standard concerns?
> - Vendor/Procurement Manager: Any vendor dependency or procurement implications?
> - Facilities/Office Manager: Any physical infrastructure or workspace impact? (if active)

**CTO:**
> - Engineering Lead: Any development effort, technical debt, or architecture implications?
> - Infrastructure/DevOps Lead: Any infrastructure, deployment, or scalability concerns?
> - Data/Analytics Lead: Any data architecture, analytics, or reporting impact?
> - Product/UX Lead: Any product roadmap or user experience implications?

**CISO:**
> - Security Operations Lead: Any threat surface, monitoring, or incident response implications?
> - Compliance/GRC Lead: Any regulatory compliance or governance concerns?
> - Identity & Access Lead: Any access control, authentication, or authorization impact?
> - Security Architecture Lead: Any security architecture or design pattern concerns?

**VP Sales:**
> - Sales Operations Lead: Any sales process, CRM, or pipeline implications?
> - Account Management Lead: Any existing customer relationship or retention concerns?
> - Business Development Lead: Any partnership, channel, or market expansion impact?
> - Sales Enablement Lead: Any sales training, collateral, or tooling implications?

**VP Delivery:**
> - Project/Program Manager: Any project timeline, scope, or resource implications?
> - Resource Manager: Any staffing, allocation, or capacity concerns?
> - Client Success Lead: Any client satisfaction, SLA, or relationship impact?
> - QA/Delivery Standards Lead: Any quality assurance or delivery standard concerns?

**CAO:**
> - HR/People Ops Lead: Any hiring, retention, policy, or culture implications?
> - Legal/Contracts Lead: Any legal exposure, contract, or IP concerns?
> - Admin/Policy Lead: Any administrative policy or procedural impact?
> - Corporate Communications Lead: Any internal/external messaging or reputation concerns?

**Rationale:** Preserves Tier 1's speed and cost advantage (~50-100 extra tokens) while adding analytical scaffolding to prevent shallow responses. Makes internalization visible in output so users can see which perspectives were considered. Low-cost insurance policy that requires no architectural changes.

---

## Question 5: Cross-Domain Forcing Questions

**The Problem:** Each team lead has three forcing questions scoped to their own domain. Should they also have questions that challenge assumptions from other domains?

**Options Considered:**
- **A: No Cross-Domain Forcing** -- Keep domain isolation pure. Cross-domain tension surfaces at Phase 4/4.5.
- **B: Selective Cross-Domain Questions for High-Interaction Pairs** -- Add one cross-domain forcing question to 5-8 team lead pairs where assumptions most commonly cross boundaries.
- **C: Universal Cross-Domain Question** -- Add one generic question to all 29 team leads: "What assumption in your analysis would be most challenged by another domain?" Generic tends to produce generic answers.

**Resolution: Option B -- Selective Cross-Domain Forcing for High-Interaction Pairs**

**Identified high-interaction pairs (7 pairs, 14 team leads affected):**

| Pair | Team Lead A | Team Lead B | Cross-Domain Question (A asks) | Cross-Domain Question (B asks) |
|------|-------------|-------------|-------------------------------|-------------------------------|
| 1 | Engineering Lead (CTO) | Controller (CFO) | "What does your implementation estimate assume about how this will be capitalized vs. expensed?" | "What does the accounting treatment assume about how Engineering will structure the implementation?" |
| 2 | FP&A Analyst (CFO) | Sales Operations Lead (VP Sales) | "What revenue assumptions does this projection share with -- or diverge from -- the sales pipeline forecast?" | "What does the sales forecast assume about pricing, margins, or financial constraints that FP&A might challenge?" |
| 3 | Security Architecture Lead (CISO) | Infrastructure/DevOps Lead (CTO) | "What security constraints does the proposed architecture assume, and are they realistic given DevOps's operational requirements?" | "What operational assumptions does the infrastructure design make about security controls and their performance impact?" |
| 4 | HR/People Ops Lead (CAO) | Resource Manager (VP Delivery) | "What does the staffing plan assume about hiring timelines, availability, and retention?" | "What does the resource allocation assume about HR's ability to recruit, onboard, or redeploy personnel?" |
| 5 | Legal/Contracts Lead (CAO) | Business Development Lead (VP Sales) | "What contractual terms or legal constraints does the deal structure assume are negotiable or enforceable?" | "What does the business case assume about legal feasibility, contract timelines, or regulatory approval?" |
| 6 | Process/Quality Lead (COO) | QA/Delivery Standards Lead (VP Delivery) | "What quality standards does the process change assume Delivery can maintain during transition?" | "What does the delivery quality framework assume about operational process stability during this change?" |
| 7 | Data/Analytics Lead (CTO) | Compliance/GRC Lead (CISO) | "What does the data architecture assume about data residency, retention, and access compliance requirements?" | "What does the compliance framework assume about the technical feasibility of data controls?" |

**Implementation:** Each paired team lead gets a fourth forcing question added to their subagent definition, labeled "Cross-Domain Challenge." The three existing forcing questions (Pre-Mortem, Adversarial Empathy, Domain Devil's Advocate) remain unchanged. Unpaired team leads (15 of 29) keep only the original three.

**Rationale:** Catches the highest-value cross-domain assumption gaps without adding questions to all 29 team leads. The pairs reflect real organizational friction points where one domain's analysis commonly rests on assumptions another domain would challenge. The builder agent should validate these pairs against the full roster and adjust if needed.

---

## Question 6: CEO Auto-Recommending Decision Mode

**The Problem:** Users must currently select a decision mode at invocation or accept the Analyst default. Should the CEO recommend which mode fits best?

**Options Considered:**
- **A: No Mode Recommendation** -- Mode is a user values choice. System shouldn't presume.
- **B: Mode Recommendation in `/evaluate` Auto-Triage** -- Extend the existing triage command to also recommend a mode based on decision characteristics.
- **C: Mandatory Mode Selection Wizard** -- Questionnaire before every Tier 2/3 deliberation. Adds friction.

**Resolution: Option B -- Mode Recommendation in `/evaluate` Auto-Triage**

The `/evaluate` command already assesses decision characteristics for tier selection. Mode recommendation is added as a prompt extension:

> "After recommending a tier, also recommend a Decision Mode based on these characteristics:
> - High irreversibility -> Sentinel or Guardian
> - High growth opportunity -> Pioneer
> - High organizational complexity -> Architect
> - Low data availability -> Analyst (with 'investigate further' likely outcome)
> - Multiple strong competing priorities -> Architect
> - Existential risk -> Sentinel
>
> Provide your mode recommendation with a one-sentence rationale. Also suggest one alternative mode for comparison, explaining what it would reveal."

**Enhanced `/evaluate` output format:**

```
ISSUE TRIAGE: [Issue Title]

Scope: [single-domain | multi-domain | cross-cutting]
Impact: [low | medium | high | critical]
Reversibility: [easily reversed | difficult | irreversible]

Recommended Tier: Board Meeting (Tier 3)
Rationale: [one sentence]

Recommended Mode: Sentinel
Mode Rationale: This decision is practically irreversible and involves
significant downside risk. Sentinel mode will ensure the strongest
objection from any domain is given disproportionate weight.

Alternative: Consider running Guardian vs. Pioneer comparison to see
how risk appetite changes the recommendation.
```

**Rationale:** Extends the natural home for decision assessment. Users who invoke `/consult`, `/panel`, or `/deliberate` directly with a mode skip this entirely. Users who use `/evaluate` get tier and mode guidance. The "Alternative" line nudges users toward multi-mode comparison for consequential decisions.

---

## Question 7: Mode Distinctiveness Verification

**The Problem:** The five decision modes are theoretically distinct but there's no mechanism to verify they actually produce meaningfully different synthesis in practice.

**Options Considered:**
- **A: Mode Sensitivity as Passive Indicator** -- Rely on the existing Mode Sensitivity metric in the Comparative Decision Record. Users become the QA mechanism.
- **B: Onboarding Calibration Test** -- Extend the onboarding stress test to run all five modes and verify divergence. Flag prompt modifiers needing revision if <3 of 5 modes diverge.
- **C: Adversarial Testing Suite** -- 3-5 test issues x 5 modes = 25 CEO synthesis passes. Rigorous but expensive.

**Resolution: Option B -- Multi-Mode Calibration in Onboarding Stress Test**

The onboarding stress test (already specified) is extended with a mode calibration step:

**Calibration protocol:**

1. The stress test issue must be deliberately contentious -- an issue where reasonable people would disagree about the right approach. Example: "Should we acquire a competitor that would double our headcount but carries significant regulatory risk and requires taking on substantial debt?"

2. Run the stress test issue through all five modes. Domain analysis runs once; CEO synthesis runs five times.

3. **Calibration criteria:** At least 3 of 5 modes must produce materially different outcomes.
   - "Materially different" = different decision (approve vs. oppose) OR same decision with substantially different conditions, guardrails, or accepted risks.
   - If fewer than 3 modes diverge on a deliberately contentious issue, the prompt modifiers need revision before the skill is considered calibrated.

4. Log calibration results in the company profile:

```yaml
calibration:
  stress_test_issue: "[issue description]"
  date: "[timestamp]"
  mode_results:
    guardian: "oppose -- regulatory risk too high without proven integration plan"
    pioneer: "approve -- competitive advantage outweighs integration challenges"
    architect: "approve with conditions -- requires all-domain alignment plan"
    analyst: "defer -- insufficient data on regulatory timeline and debt capacity"
    sentinel: "oppose -- downside scenario (failed integration + debt) is not survivable"
  divergence_score: "4 of 5 modes produced different decisions"
  calibration_status: pass
```

**Rationale:** The onboarding stress test is already planned. Extending it to include multi-mode comparison validates the most critical quality dimension of the Decision Modes feature with minimal additional cost (~1.1x the stress test cost). The "3 of 5 must diverge" criterion is a practical minimum bar.

---

## Deferred Questions (v2)

The following questions from the ideation session are explicitly deferred:

- **Custom blended modes** (e.g., "growth-oriented but conservative on regulatory risk") -- Requires user-configurable CEO synthesis profiles. Natural v2 feature after users develop mode preferences.
- **Institutional memory** (C-suite agents remembering previous hallway questions) -- Requires persistent state management across sessions.
- **Framework versioning and community contribution** -- Requires package management infrastructure.
- **Leadership coaching patterns** (surfacing mode selection patterns over time) -- Requires decision history tracking.

---

## Impact on Builder Agent Instructions

These resolutions add the following builder agent tasks:

1. **CEO agent definition** (Step 2): Include the five full-activation threshold conditions in the Phase 1 framing prompt. Include mode recommendation logic in the `/evaluate` triage prompt.

2. **C-suite agent definitions** (Steps 3-4): Include Tier 1 structured internal checklists in each C-suite agent's Mode A prompt. Include escalation brief capability in the Mode A prompt.

3. **Team lead subagent definitions** (Step 5): Add cross-domain forcing questions to the 14 team leads in the 7 identified pairs. Fourth question labeled "Cross-Domain Challenge."

4. **Company profile configuration** (Step 1): Implement archetype presets (Technology/SaaS default + at least one additional). Configuration format with archetype selection and individual overrides.

5. **Onboarding stress test** (Step 11): Extend to include multi-mode calibration. Use a deliberately contentious issue. Verify 3-of-5 mode divergence. Log results in company profile.
