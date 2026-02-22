# Idea Brief: The Engagement Model

**Session:** Team of Teams Agent Skill
**Report:** #2 (from Idea Report `IDEA_engagement-model.md`)
**Status:** INTERESTING (Arbiter-confirmed)
**Spec Pillar:** Experience

---

## One-Sentence Summary

A two-dimensional control surface -- depth (three interaction tiers) and width (four CEO decision modes) -- that lets users match the skill's engagement level to each decision's weight, transforming it from an event they invoke for major decisions into a daily tool.

## What It Is

The user interface layer for the cascading deliberation engine. Depth is controlled through three tiers: **Tier 1 (Hallway Question)** is a direct consult with a single C-suite agent producing a 3-5 sentence Advisory Note; **Tier 2 (Working Session)** routes to 2-4 relevant C-suite members for a one-page Panel Assessment; **Tier 3 (Board Meeting)** runs the full five-phase cascade producing a complete Decision Record. Width is controlled through four CEO Decision Modes that change how the CEO weighs domain recommendations: **Guardian** (risk-averse), **Pioneer** (growth-oriented), **Architect** (consensus-building), and **Analyst** (data-driven, default). Multi-mode comparison shows the "decision space" -- how different risk appetites shape the same analysis into different outcomes.

## Why It Matters

Most organizational questions do not need a full board meeting. If the skill only operates at maximum depth, users will invoke it rarely and it becomes a quarterly novelty. The three tiers ensure daily adoption by offering a lightweight entry point (Tier 1 costs seconds, not minutes). The four decision modes solve the "whose judgment?" problem -- they reveal that the choice of decision-making style matters as much as the analysis itself. Together, the tiers and modes make the skill feel like having an executive team on retainer rather than a bureaucratic decision machine.

## Key Components

- **Four Invocation Commands:** `/consult [role]: [question]` (Tier 1), `/panel [roles]: [issue]` (Tier 2), `/deliberate: [issue]` (Tier 3), `/evaluate: [issue]` (auto-triage)
- **CEO Triage Logic:** Assesses scope (single vs. multi-domain), impact (low to critical), reversibility (easy to irreversible). Recommends tier with one-sentence justification. User can accept, escalate, or de-escalate.
- **Decision Modes as Prompt Modifiers:** Modes change CEO synthesis weighting, not underlying domain analysis. Identical team lead outputs produce different CEO decisions under different modes.
- **Multi-Mode Comparison:** `--compare-modes` flag runs CEO synthesis four times, producing a Decision Space Map that shows Guardian, Pioneer, Architect, and Analyst outcomes side by side.
- **Tiered Output Formats:** Advisory Note (3-5 sentences), Panel Assessment (~1 page), Full Decision Record (3-5 pages)

## Open Questions for the Spec

- ~~Can a Tier 1 consult escalate to Tier 2 mid-conversation if the C-suite agent realizes the question is bigger than it seemed?~~ **Resolved (Q3):** No auto-escalation. C-suite agent produces Advisory Note + structured Escalation Brief with context carry. User re-invokes manually at higher tier with preserved context. See OPEN_QUESTIONS_RESOLUTION.md and VISION "Tier Escalation with Context Carry."
- ~~Should tier escalation thresholds and default decision mode be configurable per company profile?~~ **Resolved (Q2):** Yes -- archetype presets configure default mode and escalation_bias (conservative/normal/aggressive). See VISION "Company Profile Configuration."
- ~~Could users create custom blended modes (e.g., "growth-oriented but weight security concerns heavily")?~~ **Deferred to v2.** See VISION "Custom Decision Modes and Decision Pattern Analysis."
- ~~Does the C-suite agent in Tier 1 mode remember previous hallway questions?~~ **Deferred to v2.** Connects to institutional memory thread. See VISION "Institutional Memory."

## Relationship to Other Ideas

The cascade architecture (Report #1) is the engine. This report is the steering wheel. Without it, there is a powerful machine with no practical way for users to interact at the right level of depth. Report #3 (Cognitive Forcing) ensures the analysis at every tier is genuinely multi-perspective, not cosmetically varied.
