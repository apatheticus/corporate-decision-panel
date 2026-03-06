# CCO Production Team Dispatch Protocol

This document defines the dispatch pattern used by the CCO to invoke production team leads during Tier 2 and Tier 3 production.

---

## Dispatch Mechanism

**Tool:** Use the **Agent tool** to invoke each production team lead.

**Parameters for each Agent tool call:**
- `subagent_type`: `"general-purpose"`
- `model`: See team lead parameters table below
- `name`: The agent name from the team lead table
- `prompt`: See Prompt Structure below
- `description`: Short description of the team lead's task (e.g., `"Graphic Designer infographic production"`)

## Team Lead Parameters

| Team Lead | Agent Name | Model | maxTurns | Wave |
|-----------|-----------|-------|----------|------|
| Graphic Designer | `graphic-designer` | `haiku` | 10 | 1 |
| Writer | `writer` | `haiku` | 15 | 1 |
| Editor | `editor` | `sonnet` | 10 | 2 |
| Publisher | `publisher` | `haiku` | 15 | 3 |

**Editor uses `sonnet`** because editorial judgment -- comparing drafts against source material for accuracy, consistency, and tone -- requires stronger reasoning than production execution. The Editor is read-only by design: it judges, it does not modify.

## Wave Dispatch Pattern

Production proceeds in three sequential waves. Within each wave, agents execute in parallel.

```
Wave 1: Graphic Designer + Writer  (parallel)
         |
         v
Wave 2: Editor                     (sequential -- reviews Wave 1 output)
         |
         v
Wave 3: Publisher                  (sequential -- incorporates editorial notes)
```

### Wave 1: Graphic Designer + Writer

Dispatch **both agents simultaneously** in a single response with two Agent tool calls. Both receive the Creative Brief, complete RECORD.md content, and session context.

### Wave 2: Editor

Dispatch **after Wave 1 completes**. The Editor receives everything from Wave 1 plus both production reports (Graphic Designer's and Writer's) for review.

### Wave 3: Publisher

Dispatch **after Wave 2 completes** and the editorial review gate is passed. The Publisher receives the Creative Brief, RECORD.md, the Editorial Review (with any notes), and session context.

## Prompt Structure

Each team lead prompt must contain these sections:

### Wave 1 Prompts (Graphic Designer, Writer)

1. **Creative Brief** (full text): The CCO's creative direction for this session.
2. **Record Content**: The complete RECORD.md body content. Include the full text -- do not summarize.
3. **Session Context**: Session output path (absolute), issue slug, tier, and decision mode.
4. **Specification Pointer**: "Follow the production specification and output template defined in your agent definition at `.claude/agents/team-leads/cco/{agent-name}.md`."

### Wave 2 Prompt (Editor)

1. **Creative Brief** (full text): For tone and key message verification.
2. **Record Content**: The complete RECORD.md body content. This is the source of truth for accuracy checks.
3. **Wave 1 Reports**: The Graphic Designer's Infographic Production Report and the Writer's Writer Production Report. Include both in full.
4. **Session Context**: Session output path (absolute) for direct artifact inspection.
5. **Specification Pointer**: "Follow the review framework and output template defined in your agent definition at `.claude/agents/team-leads/cco/editor.md`."

### Wave 3 Prompt (Publisher)

1. **Creative Brief** (full text): For visual direction and audience context.
2. **Record Content**: The complete RECORD.md body content.
3. **Editorial Review**: The Editor's full Editorial Review output, including any "Notes for Publisher" section.
4. **Session Context**: Session output path (absolute), issue slug.
5. **Specification Pointer**: "Follow the production specification and output template defined in your agent definition at `.claude/agents/team-leads/cco/publisher.md`."

## Example Invocation (Wave 1)

```
Agent tool call #1:
  subagent_type: "general-purpose"
  model: "haiku"
  name: "graphic-designer"
  max_turns: 10
  description: "Graphic Designer infographic production"
  prompt: |
    CREATIVE BRIEF:
    [full creative brief text]

    RECORD CONTENT:
    [full RECORD.md body]

    SESSION CONTEXT:
    Session path: /absolute/path/to/.cdp-output/2026-03-06_issue-slug/
    Issue slug: issue-slug

    Follow the production specification and output template defined
    in your agent definition at .claude/agents/team-leads/cco/graphic-designer.md.

Agent tool call #2:
  subagent_type: "general-purpose"
  model: "haiku"
  name: "writer"
  max_turns: 15
  description: "Writer document production"
  prompt: |
    CREATIVE BRIEF:
    [full creative brief text]

    RECORD CONTENT:
    [full RECORD.md body]

    SESSION CONTEXT:
    Session path: /absolute/path/to/.cdp-output/2026-03-06_issue-slug/
    Issue slug: issue-slug

    Follow the production specification and output template defined
    in your agent definition at .claude/agents/team-leads/cco/writer.md.
```

Both Agent tool calls are made in a **single response** so they execute in parallel.

## Failure Handling

- **Team lead timeout or failure:** If a Wave 1 agent fails, proceed to Wave 2 with partial results. The Editor will flag missing artifacts. If the Editor fails, proceed to Wave 3 with no editorial notes. If the Publisher fails, report the failure in the CCO Production Report.
- **Degrade gracefully:** Never block the entire pipeline on a single agent failure. Produce whatever artifacts are possible and report gaps explicitly.
- **Revision cycle limit:** If the Editor returns REVISION REQUIRED, the CCO redispatches the responsible team lead with revision instructions. **Maximum one revision cycle.** If the second attempt still has issues, proceed to Wave 3 with editorial notes forwarded to the Publisher.
