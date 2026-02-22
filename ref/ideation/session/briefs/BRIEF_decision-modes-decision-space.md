# Idea Brief: Decision Modes and the Decision Space Map

**Session:** Team of Teams Agent Skill
**Report:** #4 (from Idea Report `IDEA_decision-modes-decision-space.md`)
**Status:** INTERESTING (Arbiter-confirmed)
**Spec Pillar:** Strategic Depth

---

## One-Sentence Summary

Five configurable CEO synthesis modes -- each mapping to established decision theory -- transform the skill from a decision engine into a decision exploration tool by showing how the same domain analysis produces different decisions depending on what the user optimizes for.

## What It Is

Decision Modes are swappable prompt modifiers in the CEO agent's synthesis layer that change how competing domain perspectives are weighted and resolved. The underlying domain analysis (team lead findings, C-suite recommendations, fault lines) is identical across modes. Five modes are defined: **Guardian** (protect what we have -- MaxiMin), **Pioneer** (pursue what we could gain -- MaxiMax), **Architect** (build widest alignment -- Behavioral), **Analyst** (follow the evidence -- Hurwicz balanced), and **Sentinel** (minimize worst-case regret -- MiniMax Regret). The power feature is multi-mode comparison, where domain analysis runs once (the expensive part) and the CEO synthesis runs multiple times (cheap), producing a Comparative Decision Record that shows the decision space side by side. A Mode Sensitivity metric signals whether the decision depends on risk appetite or on evidence.

## Why It Matters

The most useful output of multi-perspective analysis is not a single answer -- it is a map showing how the answer changes depending on what you optimize for. Solo founders and small leadership teams constantly face the question "am I being too cautious or too aggressive?" Decision Modes make that question answerable. When all five modes converge on the same decision, the user knows the answer does not depend on their posture. When modes diverge dramatically, the user knows their personal risk appetite is the deciding factor. This transforms a binary recommendation into a nuanced view of the decision landscape.

## Key Components

- **Five Decision Modes:** Guardian (risk-averse), Pioneer (growth-oriented), Architect (consensus-building), Analyst (data-driven, default), Sentinel (regret-minimizing). Each has a complete CEO prompt modifier.
- **Mode/Tier Interaction Matrix:** Each mode produces distinct behavioral patterns at each tier. Default cell: Tier 1 + Analyst (quick, evidence-weighted, transparent about uncertainty).
- **Multi-Mode Comparison:** `/deliberate guardian vs pioneer: [issue]` or `/deliberate all-modes: [issue]`. Domain analysis runs once; CEO synthesis runs per mode. Cost: approximately 1.1x a single deliberation for 4-5x the strategic insight.
- **Comparative Decision Record:** Side-by-side synthesis showing shared analysis, per-mode decisions with most determinative perspective and key factor, divergence analysis, and Mode Sensitivity metric.
- **Mode Sensitivity:** High sensitivity means the decision depends on risk appetite. Low sensitivity means all modes converge -- the evidence speaks for itself.
- **Invocation Grammar Integration:** Modes work with all tiers and invocation commands from Report #2.

## Open Questions for the Spec

- ~~Can users define custom modes (e.g., "growth-oriented but conservative on regulatory risk")?~~ **Deferred to v2.** See VISION "Custom Decision Modes and Decision Pattern Analysis."
- ~~Should the CEO auto-recommend which mode is appropriate for the decision type?~~ **Resolved (Q6):** Mode recommendation added to `/evaluate` auto-triage. CEO assesses decision characteristics (irreversibility, growth opportunity, complexity, data availability) and recommends a mode + one alternative for comparison. See OPEN_QUESTIONS_RESOLUTION.md and VISION "Auto-Triage."
- ~~Can the system surface patterns in mode selection over time (leadership coaching)?~~ **Deferred to v2.** See VISION "Custom Decision Modes and Decision Pattern Analysis."
- ~~How do you ensure modes produce meaningfully different synthesis, not slight variations?~~ **Resolved (Q7):** Multi-mode calibration in onboarding stress test. Deliberately contentious issue run through all 5 modes. 3-of-5 divergence criterion. Calibration results logged in company profile. See OPEN_QUESTIONS_RESOLUTION.md and VISION "Mode Calibration Protocol."

## Relationship to Other Ideas

This report develops the Decision Modes introduced in Report #2 into a full feature design. The cascade architecture (Report #1) produces the analysis that modes synthesize differently. The cognitive forcing framework (Report #3) ensures the domain analysis is high-quality enough that mode differences are substantive, not cosmetic. Together, the four reports form the complete design: Structure (#1), Experience (#2), Quality (#3), Strategic Depth (#4).
