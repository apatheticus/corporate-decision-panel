# Team Lead Dispatch Protocol

This document defines the team-based dispatch pattern used by C-suite agents to invoke team leads during Tier 2 and Tier 3 engagements.

---

> **Note:** C-suite agents are dispatched by the CEO as standalone background subagents (not teammates). Each C-suite agent is therefore free to create its own division team via TeamCreate and spawn team leads as teammates. This dispatch protocol governs the team lead dispatch pattern used *within* each C-suite agent's division team.

## Team Lifecycle

Each C-suite agent creates a **division team** for the duration of their analysis, spawns team leads as **teammates** in that team, collects findings, and shuts down the team when synthesis is complete.

### 1. Create Division Team

Before dispatching any team leads, create your division team:

```
TeamCreate: team_name "cdp-{role}-{issue-slug}"
```

Where `{role}` is your C-suite role (e.g., `cfo`, `cto`, `coo`) and `{issue-slug}` is the issue slug from the CEO's framing.

### 2. Dispatch Team Leads as Teammates

**Tool:** Use the **Agent tool** with `team_name` to invoke each team lead as a **teammate** (separate tmux window).

**Parameters for each Agent tool call:**
- `subagent_type`: `"general-purpose"`
- `name`: The agent name from your team lead mapping table (e.g., `"controller"`, `"engineering-lead"`)
- `team_name`: `"cdp-{role}-{issue-slug}"` (the team you just created)
- `prompt`: See Prompt Structure below
- `description`: Short description of the team lead's task (e.g., `"Controller financial analysis"`)

### 3. Collect Findings

Team leads complete their analysis and SendMessage their findings back to you. Findings arrive automatically as messages in your conversation. If a team lead fails or times out, note the gap and proceed with available findings.

### 4. Shut Down Division Team

After collecting all findings and completing your synthesis, send a shutdown request to each teammate:

```
SendMessage type: "shutdown_request" to each teammate
```

## Parallel Execution

**Critical instruction:** Make ALL Agent tool calls in a single response. Do not dispatch team leads sequentially -- invoke all relevant team leads simultaneously by including multiple Agent tool calls (each with `team_name`) in one message. This is essential for execution speed and ensures team leads work in parallel across separate tmux windows.

## Prompt Structure

Each team lead prompt must contain three sections:

1. **Context Brief** (3-5 sentences): Summarize the CEO's framing, the decision under consideration, and any relevant Research Dossier findings. Give the team lead enough context to understand why they are being consulted without forwarding the entire CEO broadcast.

2. **Sub-Question**: Your domain-specific translated question for this team lead. This is NOT the CEO's original question forwarded verbatim -- it is your translation of the issue into the team lead's specific analytical domain.

3. **Output Instruction**: "Follow the analytical framework and output template defined in your agent definition at `.claude/agents/team-leads/{domain}/{agent-name}.md`. Answer all forcing questions integrated into your assessment."

4. **Logging Context (conditional)**: If agent logging is active, include:
   ```
   LOGGING: ON
   SESSION PATH: <absolute-session-path>
   ```
   Omit entirely if logging is not active.

5. **File-Path Preamble**: Include explicit paths to key reference files
   so the team lead does not waste turns on file discovery:
   - Session output directory (absolute path)
   - RECORD.md path (if it exists at dispatch time)
   - Any domain-specific reference files relevant to the sub-question

   Example:
   ```
   REFERENCE FILES:
   Session: /path/to/.cdp-output/2026-03-06_issue-slug/
   Record: /path/to/.cdp-output/2026-03-06_issue-slug/RECORD.md
   ```

## Example Invocation

CFO dispatching the Controller:

```
TeamCreate: team_name "cdp-cfo-acquire-competitor-x"

Agent tool call:
  subagent_type: "general-purpose"
  name: "controller"
  team_name: "cdp-cfo-acquire-competitor-x"
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

If a team lead teammate times out or fails to return a response, note the gap in your domain recommendation and proceed with the findings you have. A partial analysis with an explicit gap note is more valuable than blocking the entire cascade waiting for a response that may never arrive.

## Relevance Filtering

Not every question requires all team leads. Use judgment about which sub-domains are relevant to the specific decision, but err on the side of inclusion for Tier 3 engagements. When excluding a team lead, do not dispatch them -- simply note in your synthesis that the team lead's domain was assessed as not relevant to this specific decision.
