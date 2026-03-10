# CCO Production Wave Dispatch Protocol

This document defines the CEO-managed production wave sequencing with the CCO as Creative Brief author and editorial coordinator.

---

> **Note:** The CEO creates the production team and dispatches all agents (CCO and wave team leads) as teammates. The CCO drives timing and editorial judgment via SendMessage. The CEO executes dispatch mechanically based on CCO direction.

## Overview

After the CEO writes the Decision Record (or Panel Assessment), the CEO creates a production team (`cdp-cco-{slug}`) and dispatches the CCO as a teammate. The CCO reads RECORD.md, writes the Creative Brief, and coordinates four sequential production waves by SendMessaging the CEO with dispatch instructions. The CEO dispatches each wave agent as a teammate in the production team based on CCO direction.

The CCO retains full creative authority and editorial judgment. The CEO's role in production is purely mechanical -- it dispatches wave agents only when the CCO authorizes it.

## Team Lead Parameters

| Team Lead | Agent Name | maxTurns | Wave |
|-----------|-----------|----------|------|
| Graphic Designer | `graphic-designer` | 15 | 1 |
| Writer | `writer` | 15 | 2 |
| Editor | `editor` | 10 | 3 |
| Publisher | `publisher` | 15 | 4 |

**Editor uses Sonnet** (specified in its agent definition frontmatter) because editorial judgment -- comparing drafts against source material for accuracy, consistency, and tone -- requires stronger reasoning than production execution. The Editor is read-only by design for production artifacts (DOCX/PPTX/PNG): it judges and inspects those files, but does not modify them. The Editor does use the Write tool to produce its own report file (`_REPORT_editor.md`).

## Wave Dispatch Pattern (CEO-Managed)

Production proceeds in four sequential waves, coordinated by the CCO via SendMessage.

```
CEO dispatches CCO as teammate
    |
    v
CCO reads RECORD.md, writes Creative Brief
CCO SendMessages CEO: "Creative Brief complete, dispatch Graphic Designer"
    |
    v
CEO dispatches Graphic Designer as teammate (Wave 1)
Graphic Designer writes reports/_REPORT, SendMessages CCO completion + summary
CCO reads full _REPORT_graphic-designer.md, does assessment
CCO SendMessages CEO: "Wave 1 complete, dispatch Writer"
    |
    v
CEO dispatches Writer as teammate (Wave 2)
Writer writes reports/_REPORT, SendMessages CCO completion + summary
CCO reads full _REPORT_writer.md, does assessment
CCO SendMessages CEO: "Wave 2 complete, dispatch Editor"
    |
    v
CEO dispatches Editor as teammate (Wave 3)
Editor writes reports/_REPORT, SendMessages CCO completion + summary
CCO reads full _REPORT_editor.md, does editorial assessment
CCO SendMessages CEO with editorial verdict (see Editorial Review Gate)
    |
    v
CEO dispatches Publisher as teammate (Wave 4)
Publisher writes reports/_REPORT, SendMessages CCO completion + summary
CCO reads full _REPORT_publisher.md
CCO SendMessages CEO: "Production complete"
```

### Wave 1: Graphic Designer

CEO dispatches the Graphic Designer after CCO sends: "Creative Brief complete, dispatch Graphic Designer."

The Graphic Designer receives the Creative Brief, complete RECORD.md content, and session context.

**After Wave 1 completes:** Graphic Designer writes `{session}/reports/_REPORT_graphic-designer.md` and SendMessages the CCO with a completion summary. CCO reads the full report file, verifies expected PNG files exist in `{session}/images/`. If any are missing, CCO notes the gaps. CCO proceeds to request Wave 2 regardless -- the Writer can produce documents without images, and the Editor will flag missing assets.

### Wave 2: Writer

CEO dispatches the Writer after CCO sends: "Wave 1 complete, dispatch Writer."

The Writer receives the Creative Brief, complete RECORD.md content, and session context. Infographic PNGs are now available in `{session}/images/` for embedding in documents.

**After Wave 2 completes:** Writer writes `{session}/reports/_REPORT_writer.md` and SendMessages the CCO with a completion summary. CCO reads the full report file.

### Wave 3: Editor

CEO dispatches the Editor after CCO sends: "Wave 2 complete, dispatch Editor."

The Editor receives the Creative Brief, RECORD.md content, Wave 1 and Wave 2 report contents (which the CEO reads from the report files and includes in the prompt), and session context.

**After Wave 3 completes:** Editor writes `{session}/reports/_REPORT_editor.md` and SendMessages the CCO with a completion summary. CCO reads the full report file and applies the Editorial Review Gate.

### Wave 4: Publisher

CEO dispatches the Publisher after the CCO sends the editorial verdict and authorizes Wave 4 dispatch.

The Publisher receives the Creative Brief, RECORD.md content, the Editorial Review (read from `_REPORT_editor.md`, with any notes), and session context.

**After Wave 4 completes:** Publisher writes `{session}/reports/_REPORT_publisher.md` and SendMessages the CCO with a completion summary. CCO reads the full report file and produces the CCO Production Report.

## Prompt Structure

Each wave prompt is constructed by the CEO using content that the CCO directs. The CCO's Creative Brief and editorial assessments shape the prompts, while the CEO handles the mechanical dispatch.

### Wave 1 Prompt (Graphic Designer)

1. **Creative Brief** (full text): The CCO's creative direction for this session.
2. **Record Content**: The complete RECORD.md body content. Include the full text -- do not summarize.
3. **Session Context**: Session output path (absolute), issue slug, tier, and decision mode.
4. **Specification Pointer**: "Follow the production specification and output template defined in your agent definition at `.claude/agents/team-leads/cco/graphic-designer.md`."
5. **Logging Context (conditional)**: If agent logging is active, include `LOGGING: ON` and `SESSION PATH: <absolute-session-path>`. Omit if not active.

### Wave 2 Prompt (Writer)

1. **Creative Brief** (full text): The CCO's creative direction for this session.
2. **Record Content**: The complete RECORD.md body content. Include the full text -- do not summarize.
3. **Session Context**: Session output path (absolute), issue slug, tier, and decision mode.
4. **Specification Pointer**: "Follow the production specification and output template defined in your agent definition at `.claude/agents/team-leads/cco/writer.md`."
5. **Logging Context (conditional)**: If agent logging is active, include `LOGGING: ON` and `SESSION PATH: <absolute-session-path>`. Omit if not active.

### Wave 3 Prompt (Editor)

1. **Creative Brief** (full text): For tone and key message verification.
2. **Record Content**: The complete RECORD.md body content. This is the source of truth for accuracy checks.
3. **Wave 1 & 2 Reports**: The Graphic Designer's Infographic Production Report and the Writer's Writer Production Report. Include both in full.
4. **Session Context**: Session output path (absolute) for direct artifact inspection.
5. **Specification Pointer**: "Follow the review framework and output template defined in your agent definition at `.claude/agents/team-leads/cco/editor.md`."
6. **Logging Context (conditional)**: If agent logging is active, include `LOGGING: ON` and `SESSION PATH: <absolute-session-path>`. Omit if not active.

### Wave 4 Prompt (Publisher)

1. **Creative Brief** (full text): For visual direction and audience context.
2. **Record Content**: The complete RECORD.md body content.
3. **Editorial Review**: The Editor's full Editorial Review output, including any "Notes for Publisher" section.
4. **Session Context**: Session output path (absolute), issue slug.
5. **Specification Pointer**: "Follow the production specification and output template defined in your agent definition at `.claude/agents/team-leads/cco/publisher.md`."
6. **Logging Context (conditional)**: If agent logging is active, include `LOGGING: ON` and `SESSION PATH: <absolute-session-path>`. Omit if not active.

## Report Files

Each production team lead writes a report file to the session directory after completing their work and SendMessages the CCO with a completion notification and summary. The CCO must read the full report files for detailed assessment.

| Team Lead | Report File |
|-----------|-------------|
| Graphic Designer | `{session}/reports/_REPORT_graphic-designer.md` |
| Writer | `{session}/reports/_REPORT_writer.md` |
| Editor | `{session}/reports/_REPORT_editor.md` |
| Publisher | `{session}/reports/_REPORT_publisher.md` |

The CCO reads the relevant report files after each wave completes:
- **After Wave 1:** Read `_REPORT_graphic-designer.md`, verify PNG assets
- **After Wave 2:** Read `_REPORT_writer.md`
- **After Wave 3:** Read `_REPORT_editor.md`, apply Editorial Review Gate
- **After Wave 4:** Read `_REPORT_publisher.md`, produce CCO Production Report

## Editorial Review Gate

After reading the Editor's report, the CCO applies the editorial review gate:

- **APPROVED:** CCO SendMessages CEO: "Editorial review passed. Dispatch Publisher."
- **APPROVED WITH NOTES:** CCO SendMessages CEO: "Editorial review passed with notes. Dispatch Publisher." (Notes are included in the Publisher's prompt.)
- **REVISION REQUIRED:** CCO SendMessages CEO with revision instructions for the responsible team lead: "REVISION REQUIRED for {agent-name}: {specific revision instructions}." CEO re-dispatches the responsible team lead with the CCO's revision instructions. **Maximum one revision cycle.** If the second attempt still has issues, CCO proceeds to Wave 4 with editorial notes forwarded to the Publisher.

## Failure Handling

- **Team lead timeout or failure:** If the Graphic Designer fails, CCO proceeds to request Wave 2 with partial results. If the Writer fails, CCO proceeds to request Wave 3 with partial results. The Editor will flag missing artifacts. If the Editor fails, CCO proceeds to request Wave 4 with no editorial notes. If the Publisher fails, CCO reports the failure in the CCO Production Report.
- **Degrade gracefully:** Never block the entire pipeline on a single agent failure. Produce whatever artifacts are possible and report gaps explicitly.
- **Revision cycle limit:** Maximum one revision cycle. If the second attempt still has issues, proceed to Wave 4 with editorial notes forwarded to the Publisher.
