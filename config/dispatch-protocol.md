# Team Lead Dispatch Protocol

This document defines the mechanical dispatch pattern used by C-suite agents to invoke team lead subagents during Tier 2 and Tier 3 engagements.

---

## Dispatch Mechanism

**Tool:** Use the **Agent tool** to invoke each team lead as a subagent.

**Parameters for each Agent tool call:**
- `subagent_type`: `"general-purpose"`
- `model`: `"haiku"`
- `name`: The agent name from your team lead mapping table (e.g., `"controller"`, `"engineering-lead"`)
- `prompt`: See Prompt Structure below
- `description`: Short description of the team lead's task (e.g., `"Controller financial analysis"`)

## Parallel Execution

**Critical instruction:** Make ALL Agent tool calls in a single response. Do not dispatch team leads sequentially -- invoke all relevant team leads simultaneously by including multiple Agent tool calls in one message. This is essential for execution speed and ensures team leads work in parallel.

## Prompt Structure

Each team lead prompt must contain three sections:

1. **Context Brief** (3-5 sentences): Summarize the CEO's framing, the decision under consideration, and any relevant Research Dossier findings. Give the team lead enough context to understand why they are being consulted without forwarding the entire CEO broadcast.

2. **Sub-Question**: Your domain-specific translated question for this team lead. This is NOT the CEO's original question forwarded verbatim -- it is your translation of the issue into the team lead's specific analytical domain.

3. **Output Instruction**: "Follow the analytical framework and output template defined in your agent definition at `.claude/agents/team-leads/{domain}/{agent-name}.md`. Answer all forcing questions integrated into your assessment."

## Example Invocation

CFO dispatching the Controller:

```
Agent tool call:
  subagent_type: "general-purpose"
  model: "haiku"
  name: "controller"
  description: "Controller GAAP analysis"
  prompt: |
    CONTEXT: The CEO is evaluating whether to acquire CompetitorX.
    The acquisition would be structured as an asset purchase valued at
    approximately $5M. The Research Dossier indicates the target has
    significant deferred revenue obligations.

    YOUR QUESTION: What are the GAAP accounting treatment implications
    of this asset purchase, including the deferred revenue recognition
    requirements? Are our internal financial controls adequate to absorb
    the target's accounting obligations?

    Follow the analytical framework and output template defined in your
    agent definition at .claude/agents/team-leads/cfo/controller.md.
    Answer all forcing questions integrated into your assessment.
```

## Failure Handling

If a team lead subagent times out or fails to return a response, note the gap in your domain recommendation and proceed with the findings you have. A partial analysis with an explicit gap note is more valuable than blocking the entire cascade waiting for a response that may never arrive.

## Relevance Filtering

Not every question requires all team leads. Use judgment about which sub-domains are relevant to the specific decision, but err on the side of inclusion for Tier 3 engagements. When excluding a team lead, do not dispatch them -- simply note in your synthesis that the team lead's domain was assessed as not relevant to this specific decision.
