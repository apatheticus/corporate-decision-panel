# Sub-Question File Dispatch Protocol

This document defines the sub-question file convention used by C-suite agents to communicate team lead dispatch requests to the CEO.

---

> **Note:** C-suite agents are teammates in **CEO-created division teams**. They do not create teams or dispatch agents. Instead, they formulate sub-questions for their team leads, write them as files, and notify the CEO via SendMessage. The CEO reads the files and dispatches team leads as teammates into the same division team.

## Overview

When the CEO activates a C-suite agent for Tier 2 or Tier 3 deliberation, the CEO creates a division team (`cdp-{role}-{slug}`) and dispatches the C-suite agent as a teammate. The C-suite agent receives the CEO's framing (and the Research Dossier, if available), translates it into domain-specific sub-questions for relevant team leads, writes those sub-questions as files, and notifies the CEO with the file paths. The CEO then reads the files and dispatches team leads as teammates into the same division team.

## Sub-Question File Convention

### Directory Structure

Each C-suite role has a dedicated sub-question directory within the session output:

```
{session}/sub-questions/{role}/
```

Example: `{session}/sub-questions/cfo/`

### File Path

Each sub-question file targets a single team lead:

```
{session}/sub-questions/{role}/{team-lead-agent-name}.md
```

Example: `{session}/sub-questions/cfo/controller.md`

### Writing Files

C-suite agents use the **Write tool** to create each sub-question file. Write one file per relevant team lead.

## Sub-Question File Format

Each sub-question file follows this format:

```markdown
# Sub-Question: {Team Lead Display Name}

## Context Brief
[3-5 sentences summarizing CEO framing and any relevant Research Dossier findings.
This is the C-suite agent's contextualization, not the CEO's raw framing forwarded.]

## Sub-Question
[The domain-specific translated question for this team lead. This is the C-suite
agent's analytical translation -- the core value of the two-tier hierarchy.]

## Output Instruction
Follow the analytical framework and output template defined in your agent
definition at .claude/agents/team-leads/{domain}/{agent-name}.md. Answer all
forcing questions integrated into your assessment.

## Reference Files
- Session: {absolute-session-path}
- Record: {absolute-session-path}/RECORD.md (if exists)
```

The Context Brief is NOT the CEO's original framing forwarded verbatim -- it is the C-suite agent's translation of the issue into the team lead's specific analytical context.

## Notification Protocol

After writing all sub-question files, notify the CEO via SendMessage:

```
Sub-questions ready: {session}/sub-questions/{role}/controller.md, {session}/sub-questions/{role}/fpa-analyst.md
```

Include the complete list of file paths written.

**No-team-leads path:** If no team leads are needed for this decision, notify the CEO:

```
No team leads needed -- proceeding with inline analysis
```

The CEO will not wait for sub-question files from that division.

## Relevance Filtering

Not every question requires all team leads. Write sub-question files ONLY for team leads whose domain is relevant to the specific decision. The absence of a sub-question file means that team lead is not relevant -- the CEO will only dispatch team leads that have corresponding sub-question files.

Err on the side of inclusion for Tier 3 engagements.

## Receiving Team Lead Findings

You are a teammate in a CEO-created division team. Team lead findings arrive via SendMessage automatically -- team leads will SendMessage their findings to you by name within the division team. If a team lead fails or times out, note the gap and proceed with available findings.

## Failure Handling

If a team lead teammate times out or fails to return a response, note the gap in your domain recommendation and proceed with the findings you have. A partial analysis with an explicit gap note is more valuable than blocking the entire cascade waiting for a response that may never arrive.

## Logging Context

If agent logging is active, the CEO will include logging context in your dispatch prompt. Forward logging context to your sub-question files by adding a Logging Context section:

```
## Logging Context
LOGGING: ON
SESSION PATH: {absolute-session-path}
```

Omit this section if logging is not active.
