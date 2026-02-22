# Idea Brief: Cognitive Forcing and the Prompt Architecture

**Session:** Team of Teams Agent Skill
**Report:** #3 (from Idea Report `IDEA_cognitive-forcing-prompt-architecture.md`)
**Status:** INTERESTING (Arbiter-confirmed)
**Spec Pillar:** Analytical Quality

---

## One-Sentence Summary

A three-layer prompt architecture where each of the 29 team lead perspectives is defined not by a persona description but by a unique analytical framework, mandatory output template, and domain-specific forcing questions -- compelling the LLM to perform structurally different cognitive work for each perspective and preventing "voice collapse."

## What It Is

The prompt engineering framework that makes the skill's output worth reading. Research shows simple role assignments ("You are a CFO") produce zero measurable improvement in LLM output quality. The cognitive forcing approach instead gives each team lead a complete analytical toolkit: a specific methodology (e.g., GAAP Compliance Assessment for the Controller, Three-Scenario Financial Modeling for FP&A), a structured output template that forces specific analytical artifacts, and three types of forcing questions drawn from research -- pre-mortem (Klein 2007), adversarial empathy (McChrystal JSOC), and domain devil's advocate (Nemeth 2001). The architecture extends across three layers: 29 team lead subagent definitions, 7 C-suite orchestration templates, and the CEO synthesis layer with modular decision mode overlays.

## Why It Matters

The difference between "7 agents that all sound like slightly different consultants" and "7 genuinely distinct domain perspectives that produce productive disagreement" is not better persona descriptions -- it is forcing each perspective to use different analytical methods that produce structurally different outputs. A GAAP compliance checklist and a three-scenario financial model are fundamentally different analytical artifacts that cannot collapse into the same voice. This is the hardest part of the spec to write and the most important for output quality. The cascade architecture (Report #1) is the skeleton. This is the muscle that makes it move.

## Key Components

- **Analytical Framework Packages (29):** Each team lead defined by analytical methodology + mandatory output template + three forcing questions + accountability framing + blind spot declaration. Implemented as `.claude/agents/team-leads/[domain]/[role].md` subagent definitions.
- **Three Forcing Question Types:** Pre-mortem ("Assume this fails -- what caused it?"), Adversarial Empathy ("If you were [external adversary], how would you exploit this?"), Domain Devil's Advocate ("What would [domain expert critic] find concerning?"). Applied at all three layers.
- **Heterogeneous Model Tiering:** Haiku for team lead subagents, Sonnet for C-suite agents, Opus for CEO. Research suggests model diversity actually improves analytical variety.
- **C-Suite Multi-Mode Support:** Each C-suite prompt supports three cognitive modes -- direct consult (Tier 1 quick response), full analysis (Tier 2/3 subagent delegation), and challenge phase (Phase 4.5 pre-mortem).
- **Phase 4.5 Pre-Mortem:** After producing domain recommendations, C-suite agents see all peer recommendations and answer: "Assume this decision fails catastrophically in 12 months. What caused the failure?" One round only, no back-and-forth, feeds into Decision Record's Fault Line Analysis.
- **CFO Reference Implementation:** Five complete team lead packages (Controller, FP&A, Treasury, AP/AR, Tax Lead) with full frameworks, templates, and forcing questions. Serves as the model for all 29 packages.

## Open Questions for the Spec

- The CFO domain (5 packages) is fully specified. The remaining 24 packages need equal specificity -- this is the largest content-generation task for the builder agent. **Status: Builder agent task, not a design question.**
- ~~Can analytical frameworks be versioned and updated independently? Could industry-specific variants override defaults?~~ **Deferred to v2.** See VISION "Framework Versioning and Community Contribution."
- ~~How well does Tier 1 internalization work? In direct consult mode, the C-suite agent reasons through team lead lenses internally without subagent isolation.~~ **Resolved (Q4):** Structured internal checklists per C-suite agent force explicit consideration of each team lead perspective. Adds ~50-100 tokens. See OPEN_QUESTIONS_RESOLUTION.md and VISION "Mode A Structured Internal Checklists."
- ~~Should team leads have cross-domain forcing questions that reference other domains' assumptions?~~ **Resolved (Q5):** Selective cross-domain forcing for 7 high-interaction pairs (14 team leads). Fourth "Cross-Domain Challenge" question added to paired leads only. See OPEN_QUESTIONS_RESOLUTION.md and VISION "Cross-Domain Forcing Question Pairs."

## Relationship to Other Ideas

The cascade architecture (Report #1) defines the process. The engagement model (Report #2) defines the interface. This report defines what makes the output genuinely multi-perspective rather than cosmetically varied. Three pillars together: Structure, Experience, Quality.
