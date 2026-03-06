# Creative Brief Template

This template defines the structure for the Creative Brief produced by the CCO before dispatching production team leads. The CCO generates this dynamically from the Decision Record -- this file is a reference for consistency, not read at runtime.

---

```
CREATIVE BRIEF
===============

Session: {session-output-path}
Issue: {issue-title}
Date: {timestamp}

COMMUNICATION STRATEGY:
[2-3 sentences on overall approach. What is the core message? What should the
audience take away? What impression should the artifacts collectively create?]

KEY MESSAGES:
1. Primary: [The single most important takeaway]
2. Supporting: [The key evidence or reasoning that supports the primary message]
3. Nuance: [The important caveat, dissent, or complexity that must not be lost]

TONE: [authoritative | analytical | cautionary | balanced | urgent]
[1 sentence explaining the tone choice based on the decision and its context]

AUDIENCE NOTES:
[Who will receive these artifacts? Board members, executive team, broader
leadership? What is their expected familiarity with the issue?]

VISUAL DIRECTION:
[Guidance for the Graphic Designer. Should infographics emphasize consensus
or contention? Risk or opportunity? Should the visual tone be confident,
measured, or warning?]

CONTENT MAPPING:
| RECORD.md Section | Artifact | Treatment |
|-------------------|----------|-----------|
| Executive Summary | DOCX, PPTX, HTML | Lead with decision statement |
| Domain Analyses | DOCX (full), PPTX (summary), HTML (cards) | Depth varies by format |
| Fault Lines | PPTX (dedicated slide), HTML (visualization) | Highlight contention |
| Dissenting Views | DOCX (section), PPTX (slide), HTML (section) | Preserve faithfully |
| Risk Assessment | Infographic (matrix), DOCX, PPTX | Visual + narrative |
| Action Plan | Infographic (timeline), DOCX, PPTX, HTML | Actionable next steps |

SESSION CONTEXT:
- Session path: {absolute-session-path}
- Issue slug: {issue-slug}
- Tier: {tier}
- Decision mode: {mode}
```

---

## Tone Selection Guide

| Decision Context | Recommended Tone |
|-----------------|-----------------|
| Clear approval with strong consensus | **authoritative** -- confident, decisive |
| Approval with conditions or mixed signals | **analytical** -- evidence-focused, measured |
| Oppose or defer with significant risks | **cautionary** -- risk-aware, prudent |
| Close call with legitimate arguments on both sides | **balanced** -- even-handed, acknowledging complexity |
| Time-sensitive with critical implications | **urgent** -- action-oriented, focused on next steps |

## Content Mapping Principles

- **Depth varies by format:** DOCX gets full domain analyses; PPTX gets one-slide summaries; HTML gets expandable cards.
- **Dissent is sacred:** Every format must faithfully represent dissenting views. Omitting dissent is an editorial failure.
- **Infographics supplement, not replace:** Infographics visualize data; they do not replace narrative explanation in documents.
- **Consistency is non-negotiable:** Every artifact must tell the same story. Different depths, same conclusions.
