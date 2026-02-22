# Idea Brief: The Cascading Deliberation Engine

**Session:** Team of Teams Agent Skill
**Report:** #1 (from Idea Report `IDEA_cascading-deliberation-engine.md`)
**Status:** INTERESTING (Arbiter-confirmed)
**Spec Pillar:** Structure

---

## One-Sentence Summary

A five-phase cascading deliberation process that decomposes any business issue through a two-tier agent hierarchy (8 C-suite agents + 29 team lead subagents) with engineered dissent, producing a structured Decision Record that captures not just the decision but the full reasoning chain, fault lines, and dissenting views.

## What It Is

The core architecture for the Team of Teams Agent Skill. When a user presents an issue, the CEO agent frames it, routes it to relevant C-suite agents, each C-suite agent dispatches to their team lead subagents for domain-specific analysis, synthesizes findings into a domain recommendation, and the CEO deliberates across all domains to produce a final decision. Disagreement is structural, not artificial: skeptic, advocate, and neutral mandates produce productive conflict that the CEO resolves through fault-line analysis.

## Why It Matters

Without this architecture, the skill is just "ask a panel of chatbots." The cascade ensures that each layer of the hierarchy transforms the question rather than just distributing work. The five phases (CEO Frames, C-Suite Dispatches, Team Leads Produce, C-Suite Synthesizes, CEO Deliberates) create a knowledge generation machine where the analysis itself is more valuable than the final recommendation. Engineered dissent (4 skeptics, 2 advocates, 1 systemic, 1 synthesizer) guarantees that risk, cost, opportunity, and execution reality are all represented, even when the user might prefer to hear only good news.

## Key Components

- **Five-Phase Cascade:** Frame -> Dispatch -> Analyze -> Synthesize -> Deliberate
- **Hybrid Agent Architecture:** 8 Agent Team members (CEO + 7 C-suite) invoke 29 custom subagents (team leads) via `.claude/agents/` definitions
- **Engineered Dissent Model:** Mandated dispositions per role -- CISO as Constitutional Skeptic, CFO as Cost Archaeologist, CTO as Capability Expander, VP Sales as Revenue Optimist, COO as Execution Realist, VP Delivery as Promise Keeper, CAO as Org Gravity Sensor
- **Decision-Type Routing:** CEO classifies issues (Strategic, Operational, Financial, Technical, Personnel, Compliance/Risk) and activates relevant subset of C-suite, not all 7 every time
- **Decision Record Output:** 9-section document (Executive Summary, Issue Statement, CEO Framing, Domain Analyses, Fault Line Analysis, CEO Decision, Dissenting Views, Next Steps, Metadata)

## Open Questions for the Spec

- ~~How does Phase 0 (shared consciousness broadcast) integrate with the cascade?~~ **Resolved in Vision:** Phase 0 broadcasts issue context to all activated C-suite agents simultaneously before analysis begins.
- ~~What are the full-activation trigger rules (acquisition, pivot, layoff)?~~ **Resolved (Q1):** CEO judgment with five threshold conditions (irreversibility, >30% headcount, market position change, existential financial risk, domain uncertainty). See OPEN_QUESTIONS_RESOLUTION.md and VISION "Full-Activation Threshold Conditions."
- ~~How does the company profile modify the roster (conditional roles, role reassignment)?~~ **Resolved (Q2):** Company archetype presets (Technology/SaaS, Professional Services, Regulated Industry, Manufacturing) with individual overrides. See OPEN_QUESTIONS_RESOLUTION.md and VISION "Company Profile Configuration."
- ~~Cross-functional deliberation (Phase 4.5) is parked for v2~~ -- but pre-mortem Phase 4.5 is proposed for v1 via Report #3. **Resolved in Vision:** One-round pre-mortem Phase 4.5 is v1 scope. Full multi-round deliberation deferred to v2.

## Relationship to Other Ideas

This is the foundation. Report #2 (Engagement Model) defines how users interact with this engine at different depths. Report #3 (Cognitive Forcing) defines the prompt architecture that makes each perspective produce genuinely different analysis. Together: Structure, Experience, Quality.
