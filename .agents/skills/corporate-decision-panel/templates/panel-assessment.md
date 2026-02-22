# Panel Assessment Template (Tier 2 -- Working Session)

## Purpose

The Panel Assessment is the output of a Tier 2 Working Session -- a focused multi-domain analysis with CEO synthesis. It activates 2-4 C-suite domains, runs full domain analysis with team lead delegation (Mode B), and produces a lightweight CEO synthesis. Approximately one page.

The Panel Assessment sits between the Advisory Note (quick, single-domain) and the Decision Record (comprehensive, all-domain). It provides multi-perspective analysis without the full five-phase cascade: no Phase 0 broadcast, no Phase 4.5 pre-mortem, and the CEO synthesis is abbreviated.

## Production

Optional. Triggered by the `--produce` flag on invocation (e.g., `/panel --produce finance tech: should we build this feature?`). Without the flag, the Panel Assessment text is the only output. When `--produce` is triggered, the same five-artifact production pipeline runs with lighter content.

## Agent Execution

- **CEO**: Spawned as team lead. Frames the issue, selects routing from the user-specified roles (or auto-routes if roles not specified), produces the synthesis. Runs on **Opus**.
- **C-Suite Agents**: 2-4 agents activated as teammates. Each runs **Mode B** (full analysis with team lead subagent delegation). Run on **Sonnet**.
- **Team Leads**: Invoked as custom subagents by their C-suite parent. Run on **Haiku**.
- **Phases executed**: Phase 1 (CEO frames/routes) -> Phase 2 (C-suite dispatch) -> Phase 3 (team lead findings) -> Phase 4 (C-suite synthesis) -> Phase 5 (CEO deliberation, abbreviated).
- **Phases skipped**: Phase 0 (shared consciousness broadcast), Phase 1.5 (CSO research -- unless CSO is explicitly activated), Phase 4.5 (pre-mortem challenge).

## Tone and Voice

Professional and concise. The CEO synthesis should feel like a brief executive summary of a working session, not a formal board resolution. Direct, clear, actionable. Approximately one page total.

---

## Template

```
PANEL ASSESSMENT: [Issue Title]
Assessment ID: PA-[YYYYMMDD]-[sequential-number]
Date: [YYYY-MM-DD HH:MM UTC]
Decision Type: [Strategic | Operational | Financial | Technical | Personnel | Compliance/Risk]
Tier: 2 (Working Session)
Decision Mode: [Guardian | Pioneer | Architect | Analyst | Sentinel]


ISSUE SUMMARY

[2-3 sentences framing the issue. What is being decided, why it matters,
and what the key tension is. Written by the CEO based on the user's input.]


ACTIVATED DOMAINS

| Domain | Rationale |
|--------|-----------|
| [C-Suite Role] | [Why this domain was activated for this issue] |
| [C-Suite Role] | [Why this domain was activated for this issue] |

[If the user specified roles, note that. If the CEO auto-routed,
explain the routing logic briefly.]


DOMAIN RECOMMENDATIONS

[One entry per activated domain. Abbreviated compared to Tier 3 --
focused on the recommendation and key reasoning, not exhaustive
team lead detail.]

[C-Suite Role] -- [Mandate Title]
  Recommendation: [Approve | Approve with Conditions | Oppose | Neutral]
  Confidence: [High | Medium | Low]
  Key Finding: [1-2 sentences: the most important insight from this domain]
  Primary Risk: [The single biggest risk this domain identified]
  Primary Opportunity: [The single biggest opportunity, if applicable]

[C-Suite Role] -- [Mandate Title]
  Recommendation: [Approve | Approve with Conditions | Oppose | Neutral]
  Confidence: [High | Medium | Low]
  Key Finding: [1-2 sentences]
  Primary Risk: [single biggest risk]
  Primary Opportunity: [single biggest opportunity, if applicable]

[Repeat for each activated domain]


KEY AGREEMENTS AND DISAGREEMENTS

Agreements:
- [What the activated domains agree on -- 1-3 bullet points]

Disagreements:
- [Where and why the activated domains diverge -- 1-3 bullet points.
  Name the domains on each side and the substance of the disagreement.]


CEO SYNTHESIS

[3-5 sentences. Lightweight synthesis applying the active Decision Mode.
State the recommended course of action, the reasoning, the key condition
or guardrail, and the primary risk being accepted. This is judgment,
not summary.]

Most Determinative Perspective: [role + one sentence why]


RECOMMENDED NEXT STEPS

- [Action 1]: [implied owner] -- [timeframe]
- [Action 2]: [implied owner] -- [timeframe]
- [Action 3]: [implied owner] -- [timeframe]


ESCALATION NOTE
[Optional. Include only if the CEO determines the issue warrants
Tier 3 analysis. Reasons for escalation recommendation:]

Recommended Escalation: /deliberate [mode]: [issue]
Escalation Rationale: [Why Tier 3 is warranted -- typically because
the disagreements surfaced are deeper than a working session can
resolve, the issue has cross-cutting implications beyond the
activated domains, or the stakes justify the full pre-mortem process.]
Additional Domains for Tier 3: [roles not activated in this Tier 2
that should be included in the escalated analysis]
```

---

## Mode-Specific Synthesis Guidance

The CEO synthesis section reflects the active Decision Mode:

**Guardian Mode:**
Synthesis biased toward risk mitigation. Extensive guardrails. If proceeding, conditions are framed as non-negotiable prerequisites. Skeptic domain findings carry more weight.

**Pioneer Mode:**
Synthesis biased toward opportunity capture. "How to" not "whether to." Skeptic concerns reframed as implementation challenges. Advocate domain findings carry more weight.

**Architect Mode:**
Seeks the option addressing the most concerns across all activated roles. Conditions drawn from multiple domains. Emphasizes organizational alignment and implementability.

**Analyst Mode (default):**
Synthesis driven by which domains have the highest-confidence findings. High-confidence findings carry more weight regardless of the domain's disposition. Low-confidence areas flagged for investigation. "Defer pending better data" is a legitimate outcome.

**Sentinel Mode:**
Identifies the strongest objection across all activated roles. Tests whether the downside is recoverable. Favors survivable paths. The synthesis focuses on what happens if the decision is wrong, not just what happens if it's right.

---

## Escalation Criteria

The CEO should recommend Tier 3 escalation when:

1. **Disagreements are deep**: The activated domains have fundamentally different assessments that cannot be resolved with the available information. A Tier 3 pre-mortem (Phase 4.5) would surface the failure modes more rigorously.

2. **Missing domains matter**: During analysis, it became clear that domains NOT activated have critical perspectives. Tier 3 with broader activation would capture these.

3. **Stakes are higher than expected**: The working session revealed that the issue is more consequential, more irreversible, or more complex than initially assessed.

4. **Confidence is uniformly low**: Multiple domains report low confidence, suggesting the issue needs the CSO's research investigation (Phase 1.5) before meaningful analysis is possible.

5. **Production artifacts needed**: If the decision warrants formal documentation (board presentation, editable document, archival record), Tier 3 triggers the production pipeline automatically.

---

## Production Variant (`--produce` flag)

When invoked with `--produce`, the Panel Assessment serves as the source document for the production pipeline, analogous to how the Decision Record serves Tier 3 production. The production artifacts are lighter:

- **Content scope**: Only the activated domains are covered (not full roster).
- **Capsule PDF**: Layers 3 and 4 have less content (fewer domain analyses, no pre-mortem findings).
- **Infographics**: Routing diagram and domain scorecard are generated. Fault line map may be simpler with fewer domains. Risk-opportunity matrix and action plan timeline are generated as normal.
- **All five artifacts** are still produced -- the format is identical, the content is proportionally lighter.

The `--produce` flag does not change the Panel Assessment itself -- it only triggers the production pipeline after the assessment is complete.

---

## Comparison to Other Tiers

| Aspect | Tier 1 Advisory Note | Tier 2 Panel Assessment | Tier 3 Decision Record |
|--------|---------------------|------------------------|----------------------|
| Domains | 1 | 2-4 | All relevant (up to 8) |
| Team leads | None (internalized) | Yes (Mode B delegation) | Yes (Mode B delegation) |
| CEO involvement | None | Frames + synthesizes | Full 5-phase cascade |
| Pre-mortem | No | No | Yes (Phase 4.5) |
| CSO research | No | Only if CSO activated | Conditional (Phase 1.5) |
| Output length | 3-5 sentences | ~1 page | 3-5 pages |
| Production | Never | Optional (`--produce`) | Always |
