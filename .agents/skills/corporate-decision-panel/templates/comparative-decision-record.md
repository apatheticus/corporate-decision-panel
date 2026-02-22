# Comparative Decision Record Template (Multi-Mode)

## Purpose

The Comparative Decision Record is produced when multiple Decision Modes are invoked for the same issue. It presents the domain analysis once (shared across modes) and the CEO synthesis multiple times (once per mode), then surfaces where modes agree, where they diverge, and what the divergence reveals about the decision.

The key efficiency insight: domain analysis is mode-independent. Multi-mode comparison runs domain analysis once (the expensive part) and CEO synthesis multiple times (cheap, single-agent passes). Cost: approximately 1.1x a single deliberation for 5x the strategic insight.

## Invocation Patterns

- **Two-mode comparison**: `/deliberate guardian vs pioneer: [issue]`
- **All modes**: `/deliberate all-modes: [issue]`
- **Tier 2 with mode**: `/panel pioneer finance tech: [issue]` (single mode, but the pattern extends to multi-mode)
- **Arbitrary mode sets**: `/deliberate guardian vs analyst vs sentinel: [issue]`

## When to Use

Multi-mode comparison is the skill's highest-value feature for consequential decisions. It transforms the output from "what should we do?" to "what does the decision landscape look like?" The `/evaluate` auto-triage suggests multi-mode comparison via the "Alternative" line for decisions where mode sensitivity is likely high.

Use multi-mode when:
- The decision is consequential and the user's risk appetite should influence the outcome
- Stakeholders with different risk profiles will review the decision
- The user wants to understand not just the recommendation but the decision space
- The issue is genuinely contentious (reasonable people would disagree)

## Mode Sensitivity Signal

**Mode Sensitivity** is the novel analytical signal that multi-mode comparison produces:
- **High sensitivity**: Modes diverge significantly. The decision depends heavily on the user's risk appetite, values, or strategic posture. The analysis is informative but the right answer is a values question.
- **Medium sensitivity**: Some modes converge, others diverge. Specific aspects of the decision are clear while others depend on posture.
- **Low sensitivity**: All or most modes converge on the same answer. The evidence speaks for itself regardless of risk appetite. This is a strong signal that the decision is clear-cut.

---

## Template

```
COMPARATIVE DECISION RECORD: [Issue Title]
Decision ID: CDR-[YYYYMMDD]-[sequential-number]
Date: [YYYY-MM-DD HH:MM UTC]
Submitted by: [user identifier]
Decision Type: [Strategic | Operational | Financial | Technical | Personnel | Compliance/Risk]
Tier: [2 | 3]
Modes Compared: [comma-separated list of modes analyzed]


EXECUTIVE SUMMARY

[One paragraph per mode showing how the decision differs. Each paragraph
should be 2-3 sentences: the decision, the key reasoning, and how it
differs from other modes. The reader should be able to scan this section
and understand the full decision landscape.]

Guardian: [2-3 sentences. The decision under risk-averse synthesis.]

Pioneer: [2-3 sentences. The decision under growth-oriented synthesis.]

Architect: [2-3 sentences. The decision under consensus-building synthesis.]

Analyst: [2-3 sentences. The decision under evidence-driven synthesis.]

Sentinel: [2-3 sentences. The decision under regret-minimizing synthesis.]

[Include only the modes that were compared. For a two-mode comparison,
include only those two paragraphs.]

Mode Sensitivity: [High | Medium | Low]
[One sentence explaining the sensitivity rating. E.g., "High -- Guardian
and Pioneer reach opposite conclusions, indicating this decision depends
primarily on risk appetite rather than evidence."]


SHARED ANALYSIS

[This section is identical across all modes. It is presented once.
The shared analysis follows the same structure as Sections 1-4 of the
standard Decision Record.]

1. ISSUE STATEMENT

   [The question as originally posed, verbatim or with minimal editorial
   clarification.]


2. CEO FRAMING

   Decision Type Classification: [type + rationale]

   Evaluation Dimensions:
   - [Dimension 1]: [what this dimension examines]
   - [Dimension N]: [what this dimension examines]

   Activated Teams:
   | C-Suite Role | Activation Rationale |
   |-------------|---------------------|
   | [Role] | [Rationale] |

   Excluded Teams:
   | C-Suite Role | Exclusion Rationale |
   |-------------|---------------------|
   | [Role] | [Rationale] |

   Full-Activation Threshold Assessment: [assessment]
   CSO Research Activation: [Yes/No + rationale]


3. DOMAIN ANALYSES

   [Same structure as standard Decision Record Section 3. One subsection
   per activated C-suite domain with recommendation, confidence, summary,
   team lead findings, key risks, key opportunities.]

   3.1 [C-Suite Role] -- [Mandate Title]
       Domain Recommendation: [Approve | Approve with Conditions | Oppose | Neutral]
       Confidence Level: [High | Medium | Low]
       Summary: [2-3 sentences]
       Team Lead Findings:
       | Team Lead | Key Finding | Confidence |
       |-----------|-------------|------------|
       | [Role] | [Finding] | [H/M/L] |
       Key Risks Identified: [list]
       Key Opportunities Identified: [list]

   [Repeat for all activated domains]


4. FAULT LINE ANALYSIS

   Points of Agreement: [what most domains agree on]
   Points of Contention: [where and why recommendations diverge]
   Pre-Mortem Findings: [Phase 4.5 failure modes, if Tier 3]
   Unresolved Tensions: [surfaced but unresolvable]


MODE COMPARISONS

[One subsection per mode compared. Each subsection shows how the CEO
synthesized the shared analysis through that mode's lens. These sections
are produced by running the CEO synthesis prompt with each mode's prompt
modifier, one at a time, against the same underlying domain analysis.]

GUARDIAN SYNTHESIS
  Decision: [Clear statement of the decision under Guardian mode]
  Most Determinative Perspective: [C-suite role + why this role was
    weighted highest under Guardian's risk-averse lens]
  Key Factor: [The single analytical element that tipped this mode's
    decision. What specific finding or tension drove the conclusion?]
  Conditions & Guardrails: [What must be true for this decision to
    proceed under Guardian synthesis]
  Accepted Risks: [What risks are accepted, with reasoning]
  Dissenting Views Summary: [Strongest overruled objections under this mode]

PIONEER SYNTHESIS
  Decision: [Clear statement under Pioneer mode]
  Most Determinative Perspective: [role + why under growth-oriented lens]
  Key Factor: [What tipped this mode's decision]
  Conditions & Guardrails: [Conditions under Pioneer synthesis]
  Accepted Risks: [Risks accepted, with reasoning]
  Dissenting Views Summary: [Strongest overruled objections under this mode]

ARCHITECT SYNTHESIS
  Decision: [Clear statement under Architect mode]
  Most Determinative Perspective: [role + why under consensus-building lens]
  Key Factor: [What tipped this mode's decision]
  Conditions & Guardrails: [Conditions under Architect synthesis]
  Accepted Risks: [Risks accepted, with reasoning]
  Dissenting Views Summary: [Strongest overruled objections under this mode]

ANALYST SYNTHESIS
  Decision: [Clear statement under Analyst mode]
  Most Determinative Perspective: [role + why under evidence-driven lens]
  Key Factor: [What tipped this mode's decision]
  Conditions & Guardrails: [Conditions under Analyst synthesis]
  Accepted Risks: [Risks accepted, with reasoning]
  Dissenting Views Summary: [Strongest overruled objections under this mode]

SENTINEL SYNTHESIS
  Decision: [Clear statement under Sentinel mode]
  Most Determinative Perspective: [role + why under regret-minimizing lens]
  Key Factor: [What tipped this mode's decision]
  Conditions & Guardrails: [Conditions under Sentinel synthesis]
  Accepted Risks: [Risks accepted, with reasoning]
  Dissenting Views Summary: [Strongest overruled objections under this mode]

[Include only the modes that were compared.]


DIVERGENCE ANALYSIS

[The meta-analysis of how different synthesis lenses produce different
decisions from the same evidence. This section is unique to the
Comparative Decision Record and is the primary value-add of multi-mode
comparison.]

Where Modes Agree:
[Decisions or conclusions that all (or nearly all) compared modes reached.
These are the analytical bedrock -- conclusions robust enough to survive
any reasonable synthesis lens.]
- [Agreement 1]: [what modes agree on and why it's robust]
- [Agreement 2]: [what modes agree on and why it's robust]

Where Modes Diverge:
[The specific pivot points where modes reach different conclusions.
For each divergence, identify which modes are on which side and what
drives the split.]
- [Divergence 1]: [Mode(s) A] reach [conclusion X] while [Mode(s) B]
  reach [conclusion Y]. The pivot is [what drives the difference --
  typically a difference in how a specific tension or risk is weighted].
- [Divergence 2]: [same structure]

The Key Choice:
[What the user is actually deciding between. Not the business question
(that's in the Issue Statement), but the values/priorities question
underneath it. Multi-mode divergence reveals this underlying choice.

Example: "The business question is whether to acquire CompetitorX.
The underlying choice is between protecting current profitability
(Guardian/Sentinel) and capturing market position before the window
closes (Pioneer). The evidence does not resolve this choice -- it
depends on whether you believe the competitive window is real and
whether you can absorb the integration risk."]


METADATA

Total Roles Consulted: [N]
Decision Complexity: [Low | Medium | High | Critical]
Primary Domain: [most determinative across modes, or "varies by mode"]
Dissent Level: [assessed across the shared analysis, not per-mode]
Modes Compared: [list]

Mode Sensitivity: [High | Medium | Low]
Mode Sensitivity Detail:
[Expanded explanation of how sensitive the decision is to synthesis posture.
Include:
- How many modes converge vs. diverge
- Whether the divergence is directional (approve vs. reject) or conditional
  (same direction, different guardrails)
- What this means for the user's decision process]

Key Assumptions: [assumptions the shared analysis rests on]
Research Foundation: [CSO evidence quality grade, if applicable]
Company Profile: [archetype used]
```

---

## Content Mapping to Production Artifacts

When production is triggered for a multi-mode comparison, the production artifacts adapt:

| Production Artifact | Multi-Mode Adaptation |
|----|-----|
| **HTML (index.html)** | Hero shows per-mode decision summary cards. Domain analysis section presented once. After "The Decision" section, tabbed or side-by-side "Mode Comparisons" panels show each mode's synthesis. "Divergence Analysis" section with mode comparison infographic follows. Mode Sensitivity indicator in metadata. |
| **PPTX** | Shared analysis slides presented once (The Question through Fault Lines). Per-mode synthesis slides (1 per mode: decision + determinative perspective + key factor). "The Key Choice" divergence slide with mode comparison infographic and Mode Sensitivity indicator. |
| **DOCX** | Sections 1-5 present shared analysis. Section 6 has subsections per mode (6.1 Guardian Synthesis, 6.2 Pioneer Synthesis, etc.). Section 7 becomes Divergence Analysis. Appendix C covers Mode Sensitivity. |
| **Results PDF** | Renders the HTML page -- inherits the multi-mode layout. |
| **Capsule PDF** | Layer 2 includes all mode syntheses and Divergence Analysis. Layer 4 includes mode selection rationale and Mode Sensitivity analysis. |

---

## Divergence Classification Guide

### Directional Divergence (High Sensitivity)
Modes reach fundamentally different decisions: some approve, some oppose, some defer. This indicates the decision depends primarily on the user's risk appetite or strategic posture.

Example: Guardian opposes acquisition, Pioneer approves aggressively, Sentinel defers pending risk investigation.

### Conditional Divergence (Medium Sensitivity)
Modes reach the same directional decision but with meaningfully different conditions, guardrails, or timelines. The "what" is the same but the "how" differs significantly.

Example: All modes approve the hire, but Guardian requires 6 months of runway buffer, Pioneer wants to accelerate the timeline, and Architect adds cross-departmental coordination requirements.

### Convergence (Low Sensitivity)
All modes reach essentially the same decision with similar conditions. The evidence is clear enough that synthesis posture does not materially change the outcome.

Example: All modes agree the security vulnerability must be patched immediately. The decision does not depend on risk appetite -- the risk is unambiguous.
