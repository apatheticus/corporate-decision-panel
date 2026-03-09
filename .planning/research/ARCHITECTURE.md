# Architecture: v1.4 Team Refactor Integration

**Domain:** Division team dispatch, sub-question file protocol, CEO-managed wave sequencing, and file-based inter-agent coordination
**Researched:** 2026-03-08
**Confidence:** HIGH (analysis based on direct reading of all affected source files, reference documents, and error logs from 2026-03-08 production session)

---

## Executive Summary

The v1.4 Team Refactor is an architectural inversion: moving all Agent/TeamCreate calls from C-suite agents to the CEO, while preserving the three-tier deliberation hierarchy (CEO > C-suite > team leads). The refactor is necessary because nested Claude Code sessions cannot use Agent/TeamCreate tools -- a hard platform constraint confirmed by three independent agent failures in the 2026-03-08 session. The solution (Option A -- "Division teams with CEO as universal dispatcher") introduces three new architectural components: division team dispatch from the CEO, a sub-question file protocol for C-suite-to-CEO communication, and CEO-managed wave sequencing for the CCO production pipeline. These integrate with the existing file-based output convention (_RECOMMENDATION_*.md, _REPORT_*.md) and SendMessage-based intra-team communication.

The refactor touches 14 files directly (3 config protocols, 1 CEO agent, 9 C-suite agents, 1 SKILL.md) but changes zero application code for the deliberation engine -- all changes are markdown specification edits. The five supporting fixes (slug aliases, PDF path, logging inline, validation leniency, large file guidance) are independent and can be implemented before or in parallel with the core dispatch rewrite.

---

## Existing Architecture (As-Is, v1.5 Codebase)

### System Overview

The CDP is a prompt-as-code system. The deliberation engine has zero application code -- agent behavior is defined entirely by markdown specifications. Python scripts handle only infographic generation, validation, PDF production, and model configuration. "Architecture" here means the structure of markdown specifications that agents follow.

### Current Component Map

```
ORCHESTRATION LAYER (config/)
  orchestration-protocol.md    Five-phase cascade, production trigger, session setup
  dispatch-protocol.md         C-suite -> team lead dispatch pattern (BROKEN)
  cco-dispatch-protocol.md     CCO -> production team dispatch (BROKEN)
  routing-table.md             Decision-type activation rules, thresholds
  decision-modes.md            Five CEO synthesis modes
  production-pipeline.md       Artifact specs, dependency table
  company-profile.md           Archetype presets
  logging-protocol.md          Agent error logging

AGENTS (agents/)
  ceo.md                       CEO identity + orchestration reference (348 lines)
  c-suite/                     9 C-suite agents (CAO, CCO, CFO, CISO, COO, CSO, CTO, VP-Delivery, VP-Sales)
  team-leads/                  34 team lead agents across 9 divisions

SCRIPTS (scripts/)
  config.py                    API key + model config from .cdp-context/
  preflight.py                 Dependency validation
  generate_infographic.py      Gemini API infographic generation
  validation.py                AI vision quality validation
  session.py                   Batch infographic session runner
  build_results_pdf.py         Results PDF via reportlab
  apply_models.py              Agent model override from config

TEMPLATES (templates/)
  Decision record, panel assessment, advisory note formats
  production/                  Artifact production specs
  infographic-prompts/         JSON prompt templates for 6 infographic types

SKILL (SKILL.md)
  Invocation grammar, orchestration overview, agent roster
```

### Current Data Flow (Documented, Not Working)

```
Phase 0: CEO broadcasts issue context to all activated C-suite
Phase 1: CEO frames, routes, classifies decision type
Phase 1.5: CSO research (conditional) -- CSO dispatches research team leads
Phase 2: CEO dispatches C-suite as standalone subagents (Agent, no team_name)
         C-suite creates division team (TeamCreate) <-- FAILS
         C-suite dispatches team leads (Agent with team_name) <-- FAILS
Phase 3: Team leads SendMessage findings to C-suite parent
Phase 4: C-suite synthesizes -> _RECOMMENDATION_{role}.md
Phase 4.5: Pre-mortem round (Tier 3 only) -> _PREMORTEM_{role}.md
Phase 5: CEO reads recommendations, produces Decision Record
Production: CEO dispatches CCO as standalone subagent
            CCO creates production team (TeamCreate) <-- FAILS
            CCO dispatches waves (Agent with team_name) <-- FAILS
```

### What Actually Happens (Workaround)

Because C-suite agents are standalone subagents and cannot use Agent/TeamCreate:
- C-suite agents perform all team lead analysis inline (defeating expert collaboration)
- CCO performs all wave work inline (defeating sequential pipeline)
- Design goals 2 (expert collaboration) and partially 3 (C-suite independence) are not met

### Communication Patterns (Current)

| Pattern | Mechanism | Status |
|---------|-----------|--------|
| CEO -> C-suite | Agent tool (standalone, run_in_background) | Working |
| C-suite -> team leads | Agent tool (with team_name) | BROKEN |
| Team leads -> C-suite | SendMessage | Never exercised (dispatch fails) |
| C-suite -> CEO | File output (_RECOMMENDATION_*.md) | Working |
| CEO -> CCO | Agent tool (standalone) | Working |
| CCO -> production team | Agent tool (with team_name) | BROKEN |
| Production team -> CCO | File output (_REPORT_*.md) | Never exercised |

---

## New Architecture (To-Be, v1.4)

### Core Inversion

**Before:** C-suite agents create teams and dispatch team leads (two-hop dispatch).
**After:** CEO creates all teams and dispatches all agents (single-hop dispatch). C-suite agents communicate sub-questions via files.

This is an inversion of the dispatch authority, not a change to the deliberation model. The intellectual hierarchy remains: CEO frames -> C-suite translates -> team leads analyze -> C-suite synthesizes -> CEO decides.

### New Component Map (Changes Highlighted)

```
ORCHESTRATION LAYER (config/)
  orchestration-protocol.md    ** REWRITE Phases 2/3/4 + Production Spawn Sequence **
  dispatch-protocol.md         ** COMPLETE REWRITE: sub-question file protocol **
  cco-dispatch-protocol.md     ** COMPLETE REWRITE: CEO-managed wave sequencing **
  routing-table.md             (unchanged)
  decision-modes.md            (unchanged)
  production-pipeline.md       (unchanged)
  company-profile.md           (unchanged)
  logging-protocol.md          (unchanged, but 48 agents get inline summary)

AGENTS (agents/)
  ceo.md                       ** MAJOR UPDATE: TeamCreate + dispatch + polling **
  c-suite/                     ** ALL 9 UPDATED: remove dispatch, add sub-Q file writing **
  team-leads/                  (NO CHANGES -- transparent to dispatch mechanism)

SESSION DIRECTORY (new subdirectory)
  {session}/sub-questions/     ** NEW: sub-question file exchange directory **
    {role}/                    One directory per C-suite role
      {team-lead-name}.md     One file per team lead sub-question
```

### New Data Flow

```
Phase 0: CEO broadcasts issue context (unchanged)
Phase 1: CEO frames, routes (unchanged)
         CEO creates session directory including sub-questions/

Phase 1.5: CSO research (conditional)
         ** NEW: CEO creates CSO division team (TeamCreate)
         ** NEW: CEO dispatches CSO as teammate
         CSO formulates research sub-Qs -> writes to {session}/sub-questions/cso/
         ** NEW: CEO polls for sub-Q files -> dispatches research team leads as teammates
         Research team leads SendMessage findings to CSO
         CSO synthesizes Research Dossier -> {session}/_RECOMMENDATION_cso.md (or dossier file)

Phase 2: ** NEW: CEO creates all division teams (one TeamCreate per activated role)
         ** NEW: CEO dispatches C-suite agents as teammates (first wave)
         C-suite reads CEO framing from prompt
         C-suite formulates domain sub-questions
         ** NEW: C-suite writes sub-Qs to {session}/sub-questions/{role}/{team-lead}.md

Phase 2.5 (new implicit step):
         ** NEW: CEO polls {session}/sub-questions/{role}/ directories
         ** NEW: CEO dispatches team leads as teammates with sub-Qs in prompts
         Team leads are placed in same division team as their C-suite parent

Phase 3: Team leads analyze, SendMessage findings to C-suite parent (unchanged mechanism)
         Team leads can SendMessage peer insights within same division (unchanged)

Phase 4: C-suite receives findings via SendMessage (unchanged mechanism)
         C-suite synthesizes -> _RECOMMENDATION_{role}.md (unchanged output)
         CEO reads recommendation files after all agents complete (unchanged)

Phase 4.5: CEO reads all recommendations (unchanged)
         ** CLARIFY: CEO dispatches second-round C-suite agents as standalone subagents?
         OR: CEO dispatches into existing division teams?
         -> RECOMMENDATION: Standalone subagents (new context, no team state to preserve)
         C-suite writes _PREMORTEM_{role}.md (unchanged output)

Phase 5: CEO synthesis (unchanged)

Production:
         ** NEW: CEO creates CCO production team (TeamCreate)
         ** NEW: CEO dispatches CCO as first teammate
         CCO reads RECORD.md, writes Creative Brief
         ** NEW: CEO dispatches Graphic Designer as teammate (Wave 1)
         ** NEW: CEO polls for _REPORT_graphic-designer.md -> dispatches Writer (Wave 2)
         ** NEW: CEO polls for _REPORT_writer.md -> dispatches Editor (Wave 3)
         ** NEW: CEO polls for _REPORT_editor.md -> dispatches Publisher (Wave 4)
         CCO coordinates via SendMessage throughout
```

---

## Integration Points

### Integration Point 1: Session Directory Setup

**Existing:** `mkdir -p {session}/images {session}/build {session}/logs`
**New:** Add `mkdir -p {session}/sub-questions/{role}` for each activated role

**Location:** `config/orchestration-protocol.md` Session Output Setup section (currently lines 276-286)
**Dependency:** Must happen in Phase 1, after routing determines activated roles
**Risk:** LOW -- additive change to existing directory creation

### Integration Point 2: CEO Division Team Creation

**New component:** CEO calls TeamCreate for each activated C-suite role

**What changes:**
- `config/orchestration-protocol.md` Phase 2 section: CEO creates teams instead of dispatching standalone subagents
- `agents/ceo.md`: Add TeamCreate instructions and team naming convention
- `SKILL.md`: Update Tier 2/3 orchestration overview to reflect team dispatch

**Team naming convention (preserved from existing dispatch-protocol.md):**
```
cdp-{role}-{issue-slug}
```
Examples: `cdp-cfo-acquire-competitor-x`, `cdp-cco-acquire-competitor-x`

**Parallel execution:** CEO creates ALL division teams and dispatches ALL C-suite agents in a single response. This is critical for performance -- dispatching sequentially would serialize the entire cascade.

**Risk:** MEDIUM -- CEO prompt becomes significantly more complex with TeamCreate + dispatch for N roles. Need to ensure CEO instructions are clear enough that the model executes all dispatches in one tool-call batch.

### Integration Point 3: C-Suite Agent Transformation

**What changes:** Mode B (Tier 2/3) dispatch section in all 9 C-suite agents

**Current Mode B flow:**
1. Read CEO framing
2. Formulate sub-questions
3. TeamCreate + Agent dispatch team leads (REMOVE)
4. Collect findings via SendMessage
5. Synthesize -> _RECOMMENDATION_{role}.md

**New Mode B flow:**
1. Read CEO framing (unchanged)
2. Formulate sub-questions (unchanged)
3. Write sub-question files to `{session}/sub-questions/{role}/` (NEW)
4. Receive findings via SendMessage (unchanged mechanism, updated wording)
5. Synthesize -> _RECOMMENDATION_{role}.md (unchanged)

**Transformation scope:** 9 agents, each ~10-50 lines of Mode B dispatch section replaced

**Files affected:**
| Agent File | Current Dispatch Lines | Action |
|------------|----------------------|--------|
| `agents/c-suite/cfo.md` | 98-134 | Replace step 3-4 |
| `agents/c-suite/cto.md` | ~similar range | Replace step 3-4 |
| `agents/c-suite/coo.md` | ~similar range | Replace step 3-4 |
| `agents/c-suite/ciso.md` | ~similar range | Replace step 3-4 |
| `agents/c-suite/cao.md` | ~similar range | Replace step 3-4 |
| `agents/c-suite/cso.md` | ~similar range | Replace step 3-4 |
| `agents/c-suite/vp-delivery.md` | 64-107 | Replace step 3-4 |
| `agents/c-suite/vp-sales.md` | 82-125 | Replace step 3-4 |
| `agents/c-suite/cco.md` | 87-139 | Special: becomes Creative Brief author + coordinator |

**CCO special case:** The CCO transformation is different from analytical C-suite agents. The CCO does not formulate sub-questions for analytical team leads. Instead, the CCO:
- Reads RECORD.md
- Produces Creative Brief
- Provides editorial direction via SendMessage to production team leads
- Receives _REPORT files and manages editorial gate decisions
- But does NOT dispatch production team leads (CEO does)

**Risk:** LOW -- the transformation pattern is mechanical and identical across 8 analytical agents. CCO is the only special case.

### Integration Point 4: Sub-Question File Protocol

**New component:** File-based communication from C-suite to CEO for team lead dispatch

**File convention:**
```
{session}/sub-questions/{role}/{team-lead-name}.md
```

Example: `{session}/sub-questions/cfo/controller.md`

**File format (reuses existing dispatch-protocol.md prompt structure):**
```markdown
# Sub-Question: {Team Lead Name}

## Context Brief
[3-5 sentences summarizing CEO framing and Research Dossier findings]

## Sub-Question
[Domain-specific translated question for this team lead]

## Output Instruction
Follow the analytical framework and output template defined in your
agent definition at .claude/agents/team-leads/{role}/{agent-name}.md.
Answer all forcing questions integrated into your assessment.

## Reference Files
Session: {absolute-session-path}
Record: {absolute-session-path}/RECORD.md (if exists)
```

**Location of protocol definition:** `config/dispatch-protocol.md` (complete rewrite)

**CEO polling mechanism:** The CEO monitors `{session}/sub-questions/{role}/` directories for new files. As files appear for a given role, the CEO reads them and dispatches the corresponding team leads into that role's division team.

**Polling design decision:** The CEO should poll ALL role directories in a single pass rather than polling one role at a time. This enables cross-role parallelism -- as soon as ANY C-suite agent writes sub-questions, its team leads can be dispatched without waiting for other C-suite agents.

**Risk:** MEDIUM -- polling file systems in a loop is inherently racy. The CEO might check a directory before a C-suite agent finishes writing all sub-question files for that role, resulting in partial team lead dispatch. **Mitigation:** C-suite agents should write ALL sub-question files before signaling readiness, or the CEO should wait for a sentinel file (e.g., `{session}/sub-questions/{role}/_READY.md`). The reference plan does not specify a sentinel -- the CEO polls and dispatches as files appear. This is acceptable because dispatching team leads incrementally is fine; the C-suite agent will receive findings from however many team leads the CEO dispatched.

**Alternative considered:** Sentinel file pattern (`_READY.md`). This would be cleaner but adds complexity to both C-suite agents (write sentinel) and CEO (check for sentinel). Given that incremental dispatch works, the simpler polling approach is sufficient for v1.4.

### Integration Point 5: CEO Team Lead Dispatch

**New component:** CEO dispatches team leads as teammates in division teams

**What changes:**
- `config/orchestration-protocol.md` Phase 2: CEO dispatch instructions
- `agents/ceo.md`: Team lead mapping table or reference to find team lead agent names

**Dispatch mechanics:**
- CEO reads sub-question file for team lead X in role Y's directory
- CEO dispatches team lead X with:
  - `team_name`: `"cdp-{role}-{issue-slug}"`
  - `prompt`: Contents of sub-question file + file-path preamble + logging context
  - `name`: Agent name from team lead mapping (e.g., `controller`, `engineering-lead`)

**Team lead mapping source:** Each C-suite agent definition contains a team lead table (e.g., CFO has controller, fpa-analyst, treasury-manager, ap-ar-manager, tax-lead). The CEO needs access to these mappings to dispatch correctly. Two options:

1. **Embed full mapping in CEO agent** -- adds ~30 lines but ensures CEO has all info without reading C-suite agent files
2. **Reference C-suite agent files** -- CEO reads `agents/c-suite/{role}.md` to find team lead table. More maintainable but requires extra Read calls.

**Recommendation:** Embed the mapping in `config/dispatch-protocol.md` as the canonical reference. The CEO reads this file (which it already references). C-suite agent definitions retain their own team lead tables for Mode A (Tier 1) use. This avoids duplication anxiety -- the same table exists in two places but serves different purposes (CEO dispatch vs. C-suite context).

**Risk:** LOW -- team lead dispatch is the same Agent tool call pattern the CEO already uses for C-suite agents. The only difference is adding `team_name` parameter and deriving prompts from sub-question files rather than CEO framing.

### Integration Point 6: CEO-Managed CCO Production Waves

**What changes:** The CCO no longer creates its own production team or dispatches team leads. The CEO manages the four-wave sequential pipeline.

**Current flow (broken):**
```
CEO -> Agent(CCO, standalone) -> CCO creates team -> CCO dispatches waves
```

**New flow:**
```
CEO -> TeamCreate("cdp-cco-{slug}")
CEO -> Agent(CCO, team_name) -> CCO reads RECORD.md, writes Creative Brief
CEO -> Agent(graphic-designer, team_name) -> Wave 1
CEO polls _REPORT_graphic-designer.md
CEO -> Agent(writer, team_name) -> Wave 2
CEO polls _REPORT_writer.md
CEO -> Agent(editor, team_name) -> Wave 3
CEO polls _REPORT_editor.md
CEO -> Agent(publisher, team_name) -> Wave 4
```

**Wave gating:** The CEO reads the `_REPORT_*.md` file after each wave to verify completion before dispatching the next wave. This is the same file-based monitoring used for analytical recommendations -- the `_REPORT` file convention already exists and works.

**CCO coordination role:** The CCO remains alive in the production team and can SendMessage editorial direction, quality notes, and revision requests to production team leads. The CCO does NOT dispatch team leads -- it advises. When the Editor returns REVISION REQUIRED, the CCO can SendMessage revision instructions, but the CEO must re-dispatch the responsible team lead.

**Editorial gate handling:** The reference plan states the CEO monitors for `_REPORT_editor.md`, reads the Editorial Review verdict, and either:
- APPROVED / APPROVED WITH NOTES -> proceed to Wave 4 (Publisher)
- REVISION REQUIRED -> re-dispatch the responsible team lead (maximum one revision cycle)

This means the CEO must understand editorial verdicts. This is new CEO logic that should be documented in `config/orchestration-protocol.md` Production Spawn Sequence.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `config/cco-dispatch-protocol.md` | COMPLETE REWRITE | Remove TeamCreate/Agent from CCO, describe CEO wave management |
| `config/orchestration-protocol.md` | REWRITE Production Spawn Sequence | CEO-managed waves, editorial gate |
| `agents/c-suite/cco.md` | MAJOR UPDATE | Remove dispatch section, become Creative Brief author + SendMessage coordinator |
| `agents/ceo.md` | ADD | CCO wave management protocol |

**Risk:** MEDIUM -- the sequential wave dependency chain is the most complex coordination the CEO manages. Getting the polling and gating right requires clear instructions. The CEO is already managing analytical dispatch (which is parallel and simpler), and now must also manage sequential wave dispatch with editorial gates.

### Integration Point 7: Phase 4.5 Pre-Mortem Dispatch

**Existing mechanism:** CEO dispatches second-round C-suite agents as standalone subagents with peer recommendation summaries. Each writes `_PREMORTEM_{role}.md`.

**Question for v1.4:** Should pre-mortem agents be standalone subagents or teammates in existing division teams?

**Recommendation: Standalone subagents.** Rationale:
- Pre-mortem is a fresh analytical pass with new context (all peer recommendations)
- The division team from Phase 2-4 may still be alive -- C-suite agent is still a teammate
- Adding a second C-suite agent to the same team creates identity confusion
- Standalone subagents are simpler: fire-and-forget, read recommendations, write pre-mortem file
- The existing pre-mortem pattern works (standalone dispatch, file output) -- do not change what works

**Risk:** LOW -- no change needed for pre-mortem dispatch. It already uses standalone subagents and file output, which is not affected by the nested session limitation (CEO is the one dispatching).

---

## New Components Summary

| Component | Type | Location | Purpose |
|-----------|------|----------|---------|
| Sub-question directory | Directory convention | `{session}/sub-questions/{role}/` | File exchange between C-suite and CEO |
| Sub-question files | File convention | `{session}/sub-questions/{role}/{team-lead}.md` | Carries domain-translated sub-questions |
| CEO team creation | Protocol addition | `agents/ceo.md` + `config/orchestration-protocol.md` | TeamCreate for each activated role |
| CEO team lead dispatch | Protocol addition | `agents/ceo.md` + `config/orchestration-protocol.md` | Dispatch team leads with sub-Qs from files |
| CEO polling loop | Protocol addition | `agents/ceo.md` + `config/orchestration-protocol.md` | Monitor sub-question and report file directories |
| CEO wave management | Protocol addition | `agents/ceo.md` + `config/orchestration-protocol.md` | Sequential CCO production wave dispatch |
| Team lead mapping table | Reference table | `config/dispatch-protocol.md` | Maps C-suite roles to team lead agent names |

## Modified Components Summary

| Component | File | Change Type | Scope |
|-----------|------|-------------|-------|
| Dispatch protocol | `config/dispatch-protocol.md` | Complete rewrite | From C-suite dispatch to sub-question protocol |
| CCO dispatch protocol | `config/cco-dispatch-protocol.md` | Complete rewrite | From CCO dispatch to CEO wave management |
| Orchestration protocol | `config/orchestration-protocol.md` | Major rewrite | Phases 2/3/4 + Production Spawn Sequence |
| CEO agent | `agents/ceo.md` | Major update | Add TeamCreate, polling, wave management |
| 8 analytical C-suite agents | `agents/c-suite/{role}.md` | Moderate update | Replace dispatch with sub-Q file writing |
| CCO agent | `agents/c-suite/cco.md` | Major update | Remove dispatch, become coordinator |
| SKILL.md | `SKILL.md` | Minor update | Update orchestration overview text |

## Unchanged Components

| Component | Why Unchanged |
|-----------|---------------|
| 34 team lead agent definitions | Dispatch mechanism is transparent to them |
| Routing table | Routing logic unchanged |
| Decision modes | Mode application unchanged |
| Production pipeline spec | Artifact specs unchanged |
| Company profile | Profile system unchanged |
| All Python scripts | No deliberation code; scripts handle infographics/PDFs |
| Templates | Output formats unchanged |
| Logging protocol | Canonical file unchanged (agents get inline summary) |

---

## Patterns to Follow

### Pattern 1: File-Based State Exchange

**What:** Agents communicate state transitions through files in the session directory.
**When:** Any time agent A needs to signal agent B asynchronously.
**Why:** Agent/TeamCreate tools are only available in the main session. SendMessage is only available within teams. Files are the universal communication channel.

**Existing examples:**
- `_RECOMMENDATION_{role}.md` -- C-suite -> CEO
- `_REPORT_{agent}.md` -- production team lead -> CCO
- `_PREMORTEM_{role}.md` -- C-suite (pre-mortem) -> CEO

**New example:**
- `sub-questions/{role}/{team-lead}.md` -- C-suite -> CEO (for team lead dispatch)

**Convention:** Files use underscore prefix (`_RECOMMENDATION_`, `_REPORT_`, `_PREMORTEM_`) for agent output files that the CEO reads. Sub-question files live in a subdirectory because they serve a different purpose (dispatch input, not analysis output).

### Pattern 2: CEO Polling for File Readiness

**What:** CEO checks for the existence of files to determine when to proceed.
**When:** After dispatching an agent, before dispatching a dependent agent.

**Implementation guidance for CEO instructions:**
```
After dispatching C-suite agents, monitor for sub-question files:
1. List {session}/sub-questions/{role}/ for each activated role
2. For each new sub-question file found, read it and dispatch the corresponding team lead
3. Continue polling until all expected sub-question files have been processed
   OR all C-suite agents have completed (background task notifications)
4. Do not block on any single role -- process sub-questions as they appear
```

**Risk mitigation:** The CEO should track which team leads have been dispatched to avoid double-dispatch. A simple checklist approach: "Dispatched team leads: [list]" maintained in the CEO's conversation context.

### Pattern 3: Division Team as Collaboration Scope

**What:** A TeamCreate call defines the collaboration boundary. All agents within a team can SendMessage to each other. Agents in different teams cannot communicate directly.
**When:** Creating the working context for a C-suite division.
**Why:** Preserves engineered dissent -- divisions cannot influence each other. The CEO bridges divisions by reading files, not by enabling cross-team messaging.

```
Team "cdp-cfo-{slug}":     CFO + Controller + FP&A + Treasury + AP/AR + Tax
Team "cdp-cto-{slug}":     CTO + Engineering + Infrastructure + Data + Product
Team "cdp-cco-{slug}":     CCO + Graphic Designer + Writer + Editor + Publisher
```

These are isolated collaboration zones. The CFO's Controller cannot SendMessage to the CTO's Engineering Lead. This is by design.

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Double Dispatch

**What:** CEO dispatches a team lead twice because the polling loop re-reads a sub-question file.
**Why bad:** Wastes tokens, creates duplicate agents in the team, confuses findings collection.
**Prevention:** CEO must track dispatched team leads and skip files already processed. The CEO's instructions should include: "Maintain a list of dispatched team leads. Before dispatching, check if the team lead has already been dispatched."

### Anti-Pattern 2: CEO Reading Team Lead Output

**What:** CEO reads team lead findings directly instead of through C-suite synthesis.
**Why bad:** Defeats the two-tier analytical hierarchy. CEO should see synthesized domain perspectives, not raw specialist output.
**Prevention:** CEO instructions must explicitly state: "Do not read team lead findings. Wait for C-suite to synthesize into _RECOMMENDATION files."

### Anti-Pattern 3: Sentinel File Over-Engineering

**What:** Adding _READY.md, _COMPLETE.md, _STATUS.md sentinel files for every state transition.
**Why bad:** Increases protocol complexity for agents that are already prompt-limited. More files = more conventions to remember = more failure modes.
**Prevention:** Use file existence as the signal (sub-question file exists = ready to dispatch). Use background task completion notifications as the termination signal (agent completed = check for output files).

### Anti-Pattern 4: CCO Attempting Dispatch

**What:** CCO agent still contains TeamCreate/Agent instructions from old protocol.
**Why bad:** CCO as a teammate cannot use these tools. Will waste turns attempting and failing.
**Prevention:** Complete removal of all dispatch instructions from CCO agent definition. CCO's role is Creative Brief + editorial coordination via SendMessage.

### Anti-Pattern 5: Sequential C-Suite Dispatch

**What:** CEO dispatches C-suite agents one at a time, waiting for each to complete before dispatching the next.
**Why bad:** Serializes the entire analytical cascade. A 7-role Tier 3 engagement would take 7x longer.
**Prevention:** CEO must dispatch ALL C-suite agents in a single response with multiple Agent tool calls. All divisions run in parallel.

---

## Build Order (Suggested Phase Structure)

The build order must respect two dependency chains: (1) the dispatch architecture depends on the protocol specifications being correct before agents reference them, and (2) the five supporting fixes are independent of the dispatch rewrite.

### Build Order Rationale

```
INDEPENDENT FIXES (can be done first, in any order):
  Fix 1: Slug aliases         -- scripts + graphic-designer agent
  Fix 2: PDF module path      -- publisher agent
  Fix 5: Validation leniency  -- scripts/validation.py + generate_infographic.py
  Fix 3: Inline logging       -- 48 agent files (bulk update)
  Fix 6: Large file guidance   -- orchestration-protocol.md + ceo.md

CORE DISPATCH REWRITE (sequential dependencies):
  Step A: config/dispatch-protocol.md     -- sets the sub-question file convention
  Step B: config/cco-dispatch-protocol.md -- sets the CEO wave management convention
  Step C: config/orchestration-protocol.md -- references A+B, rewrites Phases 2/3/4
  Step D: agents/ceo.md                    -- implements A+B+C in CEO instructions
  Step E: agents/c-suite/*.md (all 9)      -- transforms Mode B to use sub-Q files
  Step F: SKILL.md                         -- update orchestration overview text
  Step G: Verification pass                -- grep for stale patterns
```

**Why independent fixes first:** They are quick wins that improve production reliability immediately. The slug fix and PDF path fix prevent the same failures that occurred in the 2026-03-08 session. The logging fix eliminates 48 potential file-read failures. None of these conflict with the dispatch rewrite.

**Why protocol specs before agent definitions:** The dispatch-protocol and cco-dispatch-protocol define the conventions that agents follow. Writing agent instructions that reference undefined conventions creates inconsistency. The orchestration protocol ties A+B together with the phase flow. The CEO agent implements the full flow. C-suite agents are last because they reference the dispatch protocol.

**Why verification last:** Grep-based verification catches stale TeamCreate/Agent references in C-suite agents, ensuring the old dispatch pattern has been fully removed.

---

## Scalability Considerations

| Concern | Current State | After v1.4 |
|---------|---------------|------------|
| CEO prompt complexity | Moderate -- dispatch N standalone subagents | High -- create N teams, dispatch N C-suite + ~4N team leads, poll directories, manage waves |
| CEO turn count | ~10-15 turns for Tier 3 | ~25-40 turns for Tier 3 (more dispatch, more polling) |
| Parallel execution | C-suite parallel, team leads sequential within C-suite | C-suite parallel, team leads parallel per-division (improved) |
| File count per session | ~10-15 files | ~30-50 files (sub-questions + existing files) |
| Total agent count | 8-10 C-suite + 0 team leads (inline) | 8-10 C-suite + 20-30 team leads (dispatched) |
| Context window pressure on CEO | Low -- dispatch and wait | Higher -- dispatch, poll, dispatch more, poll more |

**CEO maxTurns concern:** The CEO currently operates without a maxTurns limit (main session). The added polling and dispatch work significantly increases the number of turns required. A Tier 3 with 7 C-suite agents x 4 team leads each = 28 team lead dispatches + 7 C-suite dispatches + production waves + polling turns. This could approach 50+ turns. The CEO being the main session means no maxTurns constraint, but context window exhaustion is possible for very large sessions.

**Mitigation:** The CEO should be efficient in its polling -- batch-read all sub-question directories in a single pass rather than checking one at a time. Dispatch all team leads for a given role in a single response. Use terse acknowledgments ("Dispatched 4 team leads for CFO division") rather than verbose status updates.

---

## Open Questions

### Question 1: CSO Phase 1.5 Dispatch

The CSO is dispatched before other C-suite agents (Phase 1.5, conditional). Under the new architecture:
- Does the CEO create the CSO division team separately in Phase 1.5?
- Does the CEO dispatch CSO research team leads using the same sub-question file protocol?

**Recommendation:** Yes to both. The CSO follows the same pattern as other C-suite agents: CEO creates `cdp-cso-{slug}`, dispatches CSO as teammate, CSO writes sub-Qs to `{session}/sub-questions/cso/`, CEO dispatches research team leads. The only difference is timing (Phase 1.5, before Phase 2).

### Question 2: C-Suite Agent Lifetime in Division Team

When a C-suite agent finishes writing sub-question files, does it:
a) Block waiting for team lead SendMessage findings?
b) Complete and exit, with findings going to a mailbox?

**Recommendation:** (a) Block waiting. The C-suite agent must remain alive to receive SendMessage findings from team leads, synthesize them, and write the _RECOMMENDATION file. The CEO dispatches the C-suite agent with sufficient maxTurns for the full lifecycle: formulate sub-Qs + wait for findings + synthesize.

### Question 3: How Does the CEO Know Which Team Leads to Expect?

When polling sub-question directories, the CEO knows which team leads to dispatch (from the file names). But how does it know when a C-suite agent is done writing sub-questions? Options:

a) **Poll until C-suite agent's background task completes** -- but C-suite agents don't complete until they've received findings and synthesized, which requires team leads to be dispatched first. This creates a chicken-and-egg problem.

b) **C-suite agent writes all sub-Q files quickly, then waits for findings** -- the CEO polls after a brief delay, finds sub-Q files, dispatches team leads. This works because C-suite sub-question formulation is fast (one turn) while team lead analysis takes many turns.

c) **Sentinel file** -- C-suite writes `_READY.md` after all sub-Q files are written. CEO polls for sentinel.

**Recommendation:** (b) is sufficient. The CEO dispatches C-suite agents and polls after a reasonable interval. Sub-question formulation is a single turn (~30 seconds). Team lead analysis takes 5-10 turns. The timing gap is large enough that the CEO will almost always find all sub-Q files on first poll. If a sub-Q file appears later, the CEO dispatches that team lead on the next poll. No sentinel needed.

### Question 4: Error Handling for Missing Sub-Questions

What if a C-suite agent fails before writing any sub-question files?

**Recommendation:** The CEO should set a timeout. If no sub-question files appear for a role after the C-suite agent's background task completes (or after a reasonable timeout), the CEO notes the gap and proceeds. This is consistent with existing failure handling: "a missing recommendation is not a blocker, it is an acknowledged gap."

---

## Sources

All analysis based on direct file reading:
- `agents/ceo.md` (v1.5, 361 lines)
- `agents/c-suite/cfo.md` (representative C-suite agent, 224 lines)
- `agents/c-suite/cco.md` (CCO agent, 207 lines)
- `agents/team-leads/cfo/controller.md` (representative team lead, 60+ lines)
- `agents/team-leads/cco/graphic-designer.md` (production team lead, 80+ lines)
- `config/orchestration-protocol.md` (436 lines)
- `config/dispatch-protocol.md` (115 lines)
- `config/cco-dispatch-protocol.md` (198 lines)
- `config/production-pipeline.md` (60+ lines)
- `config/logging-protocol.md` (124 lines)
- `SKILL.md` (520 lines)
- `ref/team-refactor-context-260308.md` (error analysis reference)
- `ref/team-refactor-plan-260308.md` (implementation plan reference)
- `.planning/PROJECT.md` (project context)
