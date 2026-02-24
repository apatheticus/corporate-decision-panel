# Advisory Note Template (Tier 1 -- Hallway Question)

## Purpose

The Advisory Note is the output of a Tier 1 Hallway Question -- a direct consult with a single C-suite agent. No CEO framing, no routing, no team lead delegation. Quick, opinionated, domain-specific.

This is the skill's most lightweight engagement. It should feel like pulling aside a trusted executive in the hallway and asking a focused question. The response is fast, direct, and grounded in domain expertise.

## Production

After the Advisory Note is produced, the orchestrator spawns a Document Agent to produce an Advisory Document DOCX. This is a lightweight memo-format document, not a full board document. See `templates/production/advisory-document.md` for the document specification.

## Agent Execution

- **Agent**: Single C-suite agent operating in **Mode A** (direct consult)
- **Model**: Sonnet (as Agent Team teammate)
- **Process**: The C-suite agent receives the question, runs through their structured internal checklist (considering each team lead perspective briefly), and produces the Advisory Note directly. No subagent delegation.
- **CEO**: Not involved. No framing, no routing.
- **Decision Mode**: Applied as a lens modifier to the response. Defaults to Analyst if no mode specified.

## Tone and Voice

Direct, opinionated, domain-specific. The C-suite agent speaks as a domain expert giving their honest professional assessment -- not as a committee summarizing options. Use first person where natural ("I'd be concerned about...", "The key risk I see..."). Be specific, not hedged.

---

## Template

### Advisory Note

```
ADVISORY NOTE
Domain: [C-Suite Role] -- [Mandate Title]
Date: [YYYY-MM-DD HH:MM UTC]
Mode: [Guardian | Pioneer | Architect | Analyst | Sentinel]
Question: [User's question, reproduced verbatim]

---

[3-5 sentences. Direct, opinionated, domain-specific response.

Sentence 1: The direct answer or recommendation.
Sentence 2-3: The primary reasoning from this domain's perspective.
Sentence 4-5: The key risk, opportunity, or caveat this domain would flag.

The response should reflect the active Decision Mode:
- Guardian: Highlight downside risks, suggest what could go wrong.
- Pioneer: Frame as investment question, suggest acceleration.
- Architect: Include "however, [other role] might see this differently."
- Analyst: Flag confidence level explicitly. Low-confidence = research recommendation.
- Sentinel: Identify the single biggest risk and whether it's survivable.]

---
Confidence: [High | Medium | Low]
[If Low: "I'd recommend deeper analysis on this -- consider /panel or /deliberate."]
```

### Mode-Specific Response Guidance

**Guardian Mode Advisory Note:**
The response should lean toward caution. Lead with what could go wrong. If the answer is "yes, proceed," it should come with explicit conditions. Skeptic posture: "You could do this, but here's what I'd need to see first..."

**Pioneer Mode Advisory Note:**
The response should lean toward action. Frame costs as investments. Frame risks as engineering problems. If the answer involves delay, frame it as strategic timing, not avoidance. Advocate posture: "Here's how to make this work..."

**Architect Mode Advisory Note:**
The response should acknowledge multiple perspectives. Include at least one "however, [other role] might see this differently" observation. Frame recommendations in terms of organizational alignment. Consensus posture: "The strongest path is one that addresses..."

**Analyst Mode Advisory Note (default):**
The response should be evidence-weighted. Flag confidence level prominently. If evidence is thin, say so directly and recommend investigation. Analytical posture: "Based on what we know, [recommendation], but [confidence caveat]..."

**Sentinel Mode Advisory Note:**
The response should focus on the single biggest risk. For every option, ask: "If this is wrong, can we recover?" Frame recommendations in terms of survivable outcomes. Regret-minimizing posture: "The question isn't whether this will succeed, but what happens if it doesn't..."

---

## Escalation Brief

When a C-suite agent determines during Tier 1 analysis that the issue has **significant cross-domain implications**, they produce the Advisory Note as normal AND append a structured Escalation Brief. The Escalation Brief preserves the Tier 1 analysis as input for a higher-tier invocation.

**Trigger criteria for appending an Escalation Brief:**
- The question touches domains outside this C-suite agent's scope
- The answer depends on information this agent cannot assess
- The risk or opportunity scale suggests multi-perspective analysis is warranted
- The agent's confidence is Low due to cross-domain dependencies

The C-suite agent makes this determination as part of their Mode A internal checklist. When considering each team lead perspective, if multiple perspectives from OTHER C-suite domains surface as relevant, that signals cross-domain implications.

### Escalation Brief Format

```
--- ESCALATION BRIEF ---

Initial Domain: [C-suite role that produced the Advisory Note]

Initial Finding:
[1-2 sentence summary of the Advisory Note's core recommendation and reasoning]

Cross-Domain Implications:
[Which other C-suite domains are affected and why. Be specific about what
each domain would need to evaluate.]
- [Domain 1]: [Why this domain is implicated and what they would examine]
- [Domain 2]: [Why this domain is implicated and what they would examine]

Recommended Escalation: [Tier 2 (/panel) | Tier 3 (/deliberate)]
[One sentence explaining why this tier is appropriate. Tier 2 for
2-4 domains with moderate complexity. Tier 3 for cross-cutting,
high-stakes, or irreversible decisions.]

Recommended Routing:
[Which C-suite roles should be activated in the escalated analysis]
- [Role 1]: [Why]
- [Role 2]: [Why]

Recommended Mode: [mode suggestion for escalated analysis, if different from current]
[One sentence if the escalated analysis would benefit from a different mode.
Omit if the current mode is appropriate.]

Key Context for Escalated Analysis:
[Findings from this Tier 1 analysis that the higher tier should build on,
not re-derive. This is the context carry -- the value of not starting from
scratch.]
- [Finding 1 that should inform the escalated analysis]
- [Finding 2 that should inform the escalated analysis]

---
```

### Example: Advisory Note with Escalation Brief

```
ADVISORY NOTE
Domain: CFO -- Financial Skeptic
Date: 2026-02-22 14:30 UTC
Mode: Analyst
Question: Can we afford to hire 15 engineers this quarter?

---

Based on current cash position and burn rate, you can absorb 15 engineering
hires this quarter without triggering a runway concern -- your 18-month
runway compresses to approximately 14 months, which remains within
acceptable bounds for a Series B company. However, I'm at medium confidence
because the real question isn't whether you can afford the salaries -- it's
whether your delivery infrastructure can absorb 15 simultaneous onboards
without degrading current project velocity. The FP&A projection shows the
financial headroom exists, but the working capital timing is tight: you'll
need to front-load recruiting costs against Q3 revenue recognition.

---
Confidence: Medium
The financial analysis is straightforward, but the operational and delivery
implications need deeper examination.

--- ESCALATION BRIEF ---

Initial Domain: CFO -- Financial Skeptic

Initial Finding:
Financial headroom exists for 15 engineering hires but working capital
timing is tight and operational absorption capacity is unknown.

Cross-Domain Implications:
- COO: Operational workflow capacity for 15 simultaneous onboards.
  Existing processes may not scale.
- VP Delivery: Impact on current project commitments during onboarding
  period. Resource allocation disruption risk.
- CTO: Technical team structure and architecture implications of rapid
  scaling. Technical debt risk from fast ramp.

Recommended Escalation: Tier 2 (/panel)

Recommended Routing:
- CFO: Financial modeling (already begun)
- COO: Operational capacity assessment
- VP Delivery: Current commitment impact analysis
- CTO: Technical team structure planning

Key Context for Escalated Analysis:
- Cash position supports the hire: 14-month runway post-hire is acceptable
- Working capital timing requires Q3 revenue recognition to align
- The binding constraint is not financial -- it is operational absorption

---
```

---

## Internal Checklist Reference

Each C-suite agent's Mode A prompt includes a domain-specific internal checklist. Before producing the Advisory Note, the agent briefly considers each team lead perspective using that perspective's core analytical question. This adds approximately 50-100 tokens to each Tier 1 response while preventing shallow, single-dimensional analysis.

The checklists are defined in each C-suite agent's prompt file. The agent notes which team lead perspectives are relevant and which are not, and includes only relevant perspectives in the Advisory Note. The checklist also serves as the trigger for Escalation Brief generation -- if multiple perspectives from OTHER C-suite domains surface as relevant during the checklist pass, that signals cross-domain implications.
