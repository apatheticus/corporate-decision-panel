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

## Findings File Convention

### Directory Structure

Each C-suite role has a dedicated findings directory within the session output:

```
{session}/findings/{role}/
```

Example: `{session}/findings/cfo/`

### File Path

Each team lead writes a single findings file upon completing analysis:

```
{session}/findings/{role}/{agent-name}.md
```

Example: `{session}/findings/cfo/controller.md`

### Content

The findings file contains the team lead's complete output -- the same content they SendMessage to their C-suite parent. The file is the durable record; the SendMessage is the fast notification.

### Write Order

Team leads write the findings file FIRST, then SendMessage. This guarantees the file exists when the C-suite agent checks.

### Convention

One findings file per dispatched team lead. File presence = analysis complete. The absence of a findings file means the team lead has not yet completed (or failed).

## Receiving Team Lead Findings

You are a teammate in a CEO-created division team. Team lead findings arrive via SendMessage automatically -- team leads will SendMessage their findings to you by name within the division team. Team leads also write their findings to `{session}/findings/{role}/` as durable files.

**Fallback completion check:** If you have dispatched team leads and are waiting for findings, periodically check `{session}/findings/{role}/` using Glob to see which findings files have been written. Compare against the sub-question files you wrote to `{session}/sub-questions/{role}/` to determine which team leads have completed. If a findings file exists but you have not yet received the corresponding SendMessage, read the file directly — it contains the same output. Proceed on whichever signal arrives first: a SendMessage or the findings file appearing.

If a team lead fails or times out (neither signal arrives), note the gap and proceed with available findings.

## Failure Handling

If a team lead teammate times out or fails to return a response, note the gap in your domain recommendation and proceed with the findings you have. A partial analysis with an explicit gap note is more valuable than blocking the entire cascade waiting for a response that may never arrive.

### Phase 1.5 Exception: CEO-Monitored Findings Collection

For the CSO during Phase 1.5 research, the standard "periodically check
findings" fallback is replaced by a CEO-monitored pattern. The CSO does not
poll for findings files. Instead, the CEO monitors `{session}/findings/cso/`
and sends the CSO a "FINDINGS COMPLETE -- SYNTHESIZE NOW" signal when team
lead findings are ready. The CSO waits for this signal before beginning
synthesis.

This exception exists because the CSO goes idle after writing sub-question
files and cannot autonomously execute Glob checks while idle. Phase 2
C-suite agents still use the standard dual-signal pattern because they
remain active with analytical work while team leads execute.

## Logging Context

If agent logging is active, the CEO will include logging context in your dispatch prompt. Forward logging context to your sub-question files by adding a Logging Context section:

```
## Logging Context
LOGGING: ON
SESSION PATH: {absolute-session-path}
```

Omit this section if logging is not active.
