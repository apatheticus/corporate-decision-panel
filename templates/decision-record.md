# Decision Record Template (Tier 3 -- Board Meeting)

## Purpose

The Decision Record is the primary output of a Tier 3 Board Meeting deliberation. It is the **source of truth** for the production phase -- all five production artifacts (HTML, PPTX, DOCX, Results PDF, Capsule PDF) are derived from this document.

The Decision Record presents synthesized, multi-perspective analysis as a self-contained document. A reader with no knowledge of the system that produced it should be able to understand the decision, its rationale, the key disagreements, and the path forward.

## Tone and Voice

Professional, direct, and opinionated. Not hedged or bureaucratic. The CEO speaks as a decision-maker who has weighed competing perspectives and reached a judgment -- not as a moderator summarizing a discussion. Dissenting views are preserved with respect but are clearly identified as overruled.

---

## Template

```
EXECUTIVE SUMMARY
[3-5 sentences. State the decision first, then the key reasoning that drove it,
then the primary dissent. This paragraph should be self-contained -- a reader
who reads nothing else should understand what was decided, why, and what the
strongest objection was.

Example structure:
"[Company] should [decision]. This conclusion is driven primarily by [most
determinative perspective] which found [key finding]. The strongest dissent
comes from [dissenting role], who argues [core objection]. The decision
proceeds with [key guardrail] to address this concern."]


DECISION RECORD: [Issue Title]
Decision ID: DR-[YYYYMMDD]-[sequential-number]
Date: [YYYY-MM-DD HH:MM UTC]
Submitted by: [user identifier]
Decision Type: [Strategic | Operational | Financial | Technical | Personnel | Compliance/Risk]
Tier: 3 (Board Meeting)
Decision Mode: [Guardian | Pioneer | Architect | Analyst | Sentinel]


1. ISSUE STATEMENT

   [The question as originally posed by the user. Reproduce verbatim or with
   minimal editorial clarification. Do not reframe the issue -- that is the
   CEO's job in Section 2. Include any context the user provided.]


2. CEO FRAMING

   [The CEO's decomposition of the issue into evaluation dimensions. This
   section makes routing transparent -- it shows how the CEO interpreted the
   issue and what analytical lens was applied.]

   Decision Type Classification: [type + brief rationale for classification]

   Evaluation Dimensions:
   - [Dimension 1]: [what this dimension examines]
   - [Dimension 2]: [what this dimension examines]
   - [Dimension N]: [what this dimension examines]

   Activated Teams:
   | C-Suite Role | Activation Rationale |
   |-------------|---------------------|
   | [Role] | [Why this domain is relevant to this decision] |
   | [Role] | [Why this domain is relevant to this decision] |

   Excluded Teams:
   | C-Suite Role | Exclusion Rationale |
   |-------------|---------------------|
   | [Role] | [Why this domain was NOT activated for this decision] |

   Full-Activation Threshold Assessment:
   [State which threshold conditions were evaluated and whether any triggered
   full activation:
   - Irreversibility: [assessment]
   - Headcount Impact (>30%): [assessment]
   - Market Position Change: [assessment]
   - Existential Financial Risk: [assessment]
   - Domain Uncertainty: [assessment]
   If full activation was triggered, state which condition(s) triggered it.]

   CSO Research Activation: [Yes/No]
   [If Yes: State the research directive -- what factual questions the CSO
   was directed to investigate. If No: State why research was not needed.]


3. DOMAIN ANALYSES

   [One subsection per activated C-suite domain. Order by relevance to the
   decision, with the most determinative domain first.]

   3.1 [C-Suite Role] -- [Mandate Title]
       (e.g., "CFO -- Financial Skeptic")

       Domain Recommendation: [Approve | Approve with Conditions | Oppose | Neutral]
       Confidence Level: [High | Medium | Low]

       Summary:
       [2-3 sentence synthesis of this domain's analysis. State the
       recommendation and the primary reasoning. Be direct.]

       Team Lead Findings:
       | Team Lead | Key Finding | Confidence |
       |-----------|-------------|------------|
       | [Role] | [1-2 sentence finding from this specialist] | [H/M/L] |
       | [Role] | [1-2 sentence finding from this specialist] | [H/M/L] |

       Key Risks Identified:
       - [Risk 1]: [description + severity assessment]
       - [Risk 2]: [description + severity assessment]

       Key Opportunities Identified:
       - [Opportunity 1]: [description + potential impact]
       - [Opportunity 2]: [description + potential impact]

       Internal Contradictions:
       [If team leads within this domain produced conflicting findings,
       flag them here as analytical signals. Do not average them away.
       If no contradictions, omit this field.]

   3.2 [Next C-Suite Role] -- [Mandate Title]
       [Same structure as 3.1]

   [Continue for all activated domains]

   3.N CSO -- Chief Strategy Officer (Research Domain)
       [Include only if CSO was activated. Present the Research Dossier
       findings in the same structure as other domains.]

       Research Dossier Summary:
       [2-3 sentence synthesis of research findings]

       Evidence Quality Grade: [A (strong) | B (adequate) | C (limited) | D (insufficient)]

       Assumption Registry:
       | Assumption | Status | Evidence |
       |-----------|--------|----------|
       | [Assumption from the proposal] | [Confirmed | Contradicted | Unverified | Partially Supported] | [Brief evidence citation] |

       Key Evidence:
       - Confirms: [evidence supporting the proposal]
       - Contradicts: [evidence challenging the proposal]
       - Complicates: [evidence adding nuance]

       Evidence Gaps:
       - [What could not be determined and why it matters]


4. FAULT LINE ANALYSIS

   [The meta-analysis of where expert perspectives collide. This is the single
   most valuable analytical artifact the system produces. Do not manufacture
   disagreement -- if domains agree, say so. But surface genuine tensions
   with precision.]

   Points of Agreement:
   [What most or all activated domains agree on. These are the stable
   analytical foundations the decision can rest on.]
   - [Agreement 1]: [which domains agree and what they agree on]
   - [Agreement 2]: [which domains agree and what they agree on]

   Points of Contention:
   [Where and why domain recommendations diverge. Name the specific
   domains on each side and the substance of the disagreement.]
   - [Contention 1]: [Domain A] argues [position] while [Domain B]
     argues [counter-position] because [underlying reason for divergence]
   - [Contention 2]: [same structure]

   Pre-Mortem Findings:
   [Failure modes identified during Phase 4.5. Each C-suite member's
   answer to: "Assume this decision fails catastrophically in 12 months.
   What caused the failure?"]
   | C-Suite Role | Predicted Failure Mode | Severity |
   |-------------|----------------------|----------|
   | [Role] | [Their predicted failure scenario] | [Catastrophic | Severe | Moderate] |
   | [Role] | [Their predicted failure scenario] | [Catastrophic | Severe | Moderate] |

   Unresolved Tensions:
   [Tensions that were surfaced but cannot be resolved with current
   information. These are legitimate analytical limits, not failures.]
   - [Tension 1]: [what remains unresolvable and what would resolve it]
   - [Tension 2]: [same structure]


5. CEO DECISION

   Decision:
   [Clear, unambiguous statement of the decision. One to three sentences.
   Start with the verb: "Proceed with...", "Defer...", "Reject...",
   "Approve with conditions..."]

   Most Determinative Perspective: [C-suite role]
   [1-2 sentences explaining why this domain's analysis was weighted
   highest for this particular decision. Not because the role is
   important in general, but because their specific findings were most
   relevant to the core tension.]

   Decision Weight Rationale:
   [How the CEO weighed competing perspectives. Which domains carried
   more weight, which carried less, and why. This must be explicit --
   not "all perspectives were considered" but "the CFO's concerns about
   cash flow timing outweighed the CTO's argument for speed because..."]

   Conditions & Guardrails:
   [Drawn primarily from skeptic role recommendations. These are
   non-negotiable prerequisites for the decision to proceed, not
   optional suggestions.]
   - [Condition 1]: [specific requirement + which domain's concern it addresses]
   - [Condition 2]: [specific requirement + which domain's concern it addresses]

   Accepted Risks:
   [Risks the CEO consciously accepts, with reasoning for acceptance.
   These are not overlooked risks -- they are acknowledged and judged
   acceptable given the decision's potential benefits.]
   - [Risk 1]: [description] -- Accepted because: [reasoning]
   - [Risk 2]: [description] -- Accepted because: [reasoning]

   Mitigations Directed:
   [Specific actions ordered to reduce accepted risks. Each mitigation
   maps to an accepted risk above.]
   - [Mitigation 1]: [action + implied owner + timeline]
   - [Mitigation 2]: [action + implied owner + timeline]


6. DISSENTING VIEWS

   [Strongest objections from perspectives that were overruled in the
   final decision. These are preserved for the record -- not as a
   courtesy but because the decision-maker may need to revisit them
   if conditions change. Present them with full reasoning, not as
   summaries.]

   6.1 [C-Suite Role] -- [Nature of Dissent]
       Recommendation: [what this role recommended]
       Core Objection: [the substance of their disagreement]
       Risk If Ignored: [what this role believes will happen if their
       concern is not adequately addressed]
       CEO Response: [how the CEO weighed and resolved this objection]

   [Repeat for each dissenting perspective]


7. NEXT STEPS

   [Specific actions with implied owners and timelines. These flow
   directly from the CEO Decision and Mitigations Directed. Each
   action should be concrete enough to be assigned.]

   | # | Action | Implied Owner | Timeline | Priority |
   |---|--------|--------------|----------|----------|
   | 1 | [Specific action] | [Role/function] | [Timeframe] | [Critical | High | Medium] |
   | 2 | [Specific action] | [Role/function] | [Timeframe] | [Critical | High | Medium] |

   Decision Review Trigger:
   [Conditions under which this decision should be revisited.
   Tied to the Key Assumptions in Metadata.]
   - Review if: [condition that would invalidate the decision]
   - Review if: [condition that would invalidate the decision]


8. METADATA

   Total Roles Consulted: [N of 9 C-suite + N of 38 team leads activated]
   Decision Complexity: [Low | Medium | High | Critical]
   Primary Domain: [most determinative C-suite area]
   Dissent Level: [Consensus | Mild Dissent | Strong Dissent | Split Decision]

   Key Assumptions:
   [Assumptions the analysis rests on. Each assumption is a potential
   decision review trigger -- if any assumption proves false, the
   decision should be reconsidered.]
   - [Assumption 1]: [statement + current confidence level]
   - [Assumption 2]: [statement + current confidence level]

   Research Foundation: [CSO Research Dossier evidence quality grade, if applicable]
   Company Profile: [archetype used for this analysis]
   Routing Override: [Yes/No -- whether CEO overrode default routing]
```

---

## Field Specifications

### Decision ID
Format: `DR-YYYYMMDD-NNN` where NNN is a sequential number for decisions on that date. Auto-generated by the orchestrator.

### Decision Type Classification
Must be one of: Strategic, Operational, Financial, Technical, Personnel, Compliance/Risk. The CEO may identify a primary type and note secondary types (e.g., "Financial (primary), Strategic (secondary)").

### Domain Recommendation Values
- **Approve**: This domain supports the proposal as presented.
- **Approve with Conditions**: This domain supports the proposal contingent on specific requirements being met.
- **Oppose**: This domain recommends against the proposal.
- **Neutral**: This domain's analysis does not support a clear directional recommendation (insufficient data, out-of-scope impact, or genuinely balanced considerations).

### Confidence Levels
- **High**: Strong evidence base, well-understood domain, clear analytical path.
- **Medium**: Adequate evidence with some gaps, moderate uncertainty in projections.
- **Low**: Limited evidence, high uncertainty, significant assumptions required. In Analyst mode, low-confidence findings are explicitly flagged as needing further investigation.

### Dissent Level Classification
- **Consensus**: All activated domains reach the same directional recommendation.
- **Mild Dissent**: One domain dissents but acknowledges the decision is reasonable.
- **Strong Dissent**: One or more domains strongly oppose the decision with substantive reasoning.
- **Split Decision**: Activated domains are roughly evenly divided.

### Decision Complexity
- **Low**: Single domain, clear evidence, low stakes.
- **Medium**: 2-3 domains, some uncertainty, moderate stakes.
- **High**: Multi-domain, significant uncertainty or contention, high stakes.
- **Critical**: Cross-cutting, high uncertainty, existential or irreversible stakes.

---

## Production Note

This Decision Record is the source of truth for the production phase. All five production artifacts (HTML, PPTX, DOCX, Results PDF, Capsule PDF) are derived from this document. The production phase synthesizes Decision Record content into a comprehensive, narrative-form briefing -- not a formatted dump of the sections above. See `templates/production/` for the full content mapping from Decision Record sections to each production artifact format.
