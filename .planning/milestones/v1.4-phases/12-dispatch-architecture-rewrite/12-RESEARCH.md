# Phase 12: Dispatch Architecture Rewrite - Research

**Researched:** 2026-03-08
**Domain:** Multi-agent dispatch architecture -- markdown agent specification rewriting for CEO-as-universal-dispatcher, sub-question file protocol, and CEO-managed production wave sequencing
**Confidence:** HIGH

## Summary

Phase 12 is the core dispatch architecture rewrite for the Corporate Decision Panel (CDP). It rewrites the agent dispatch mechanism so the CEO (main Claude Code session) creates all division teams and dispatches all agents (C-suite and team leads), because nested Claude Code sessions cannot use Agent/TeamCreate tools -- a hard platform constraint confirmed by three independent failures in the 2026-03-08 production session. The rewrite touches 3 config protocol files, the CEO agent, all 9 C-suite agents, and the session output directory setup.

This is a pure markdown specification rewrite -- zero application code changes. All changes are to agent definitions and orchestration protocols. The critical architectural decision from the CONTEXT.md discussion is **notification-triggered dispatch** rather than polling: C-suite agents SendMessage the CEO when sub-questions are ready (with file paths), and the CEO reads the files and dispatches team leads rolling per-division. This eliminates the polling deadlock pitfall identified in earlier research. The CCO production pipeline uses a similar SendMessage-based coordination pattern where the CCO notifies the CEO when ready for each wave.

**Primary recommendation:** Structure implementation as three plans: (1) config protocol rewrites (dispatch-protocol.md, cco-dispatch-protocol.md, orchestration-protocol.md), (2) CEO agent rewrite, (3) all 9 C-suite agent transformations with verification grep. Protocols must be written first because both the CEO and C-suite agents reference them.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Notification-triggered dispatch, not polling: C-suite agents SendMessage the CEO when sub-questions are ready
- Rolling per-division: CEO dispatches team leads for each division as soon as that C-suite agent's notification arrives -- does not wait for all divisions
- C-suite SendMessage contains file list only: "Sub-questions ready: {list of file paths}" -- CEO reads the files to build team lead prompts
- Sub-question files retained for audit trail: C-suite writes files AND sends file list notification (files persist for debugging/session resume)
- No-team-leads path: C-suite sends "No team leads needed -- proceeding with inline analysis" when no sub-questions are warranted. CEO knows not to wait for that division's sub-question files
- CCO is Creative Brief author + editorial coordinator within CEO-managed production team
- CCO does NOT dispatch waves -- CEO handles all Agent tool dispatch
- Wave sequencing: CCO notifies CEO when ready for next wave. After each wave completes, team leads SendMessage CCO completion + summary. CCO reads full report file, does editorial assessment, then SendMessages CEO: "Wave N complete, dispatch {next-agent}"
- Revision cycles: If Editor returns REVISION REQUIRED, CCO SendMessages CEO with revision instructions for the responsible team lead. CEO re-dispatches. Maximum one revision cycle (unchanged)
- Team lead reports: Production team leads SendMessage CCO (all in same CEO-created team). CCO reads full _REPORT_*.md files for detail
- Pre-mortem agents dispatched as standalone subagents (no team_name), same as current architecture
- Division teams dissolve after C-suite writes _RECOMMENDATION_{role}.md -- clean lifecycle boundary before pre-mortem
- Pre-mortem prompts include executive summaries only (extracted from _RECOMMENDATION_*.md), not full recommendations -- lighter context
- Pre-mortem output files unchanged: _PREMORTEM_{role}.md via Write tool, CEO reads after completion
- CSO uses same division team + sub-question file protocol as other C-suite for Phase 1.5 research
- CEO creates cdp-cso-{slug} team, dispatches CSO as teammate, CSO writes sub-question files for 5 research leads, SendMessages CEO file list, CEO dispatches research leads as teammates
- Sequential timing: CSO Phase 1.5 completes fully before Phase 2 begins. CEO reads _DOSSIER_cso.md, incorporates into Phase 0 broadcast, then dispatches Phase 2 C-suite
- CSO Research Dossier output: {session}/_DOSSIER_cso.md (distinct from _RECOMMENDATION_ convention)
- CSO also participates in Phase 2 analytical round (produces _RECOMMENDATION_cso.md)
- CSO Phase 2 dispatch: standalone subagent (no team_name), inline analysis without team leads. CSO receives CEO framing + its own Research Dossier, produces recommendation without re-dispatching research leads
- CSO Phase 2 dispatch happens simultaneously with other C-suite division team dispatch

### Claude's Discretion
- Sub-question file format and structure (markdown template, metadata fields)
- Exact SendMessage wording for notifications
- CEO context management strategy for Tier 3 with many dispatches
- How CEO detects division team completion (background task notifications)
- Division team naming convention details

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DISP-01 | `config/dispatch-protocol.md` rewritten for CEO-as-universal-dispatcher with sub-question file convention | Architecture pattern: notification-triggered dispatch, sub-question file format, no-team-leads path |
| DISP-02 | `config/cco-dispatch-protocol.md` rewritten for CEO-managed production wave sequencing | CCO as Creative Brief author + editorial coordinator, SendMessage-based wave coordination |
| DISP-03 | `config/orchestration-protocol.md` Phases 2/3/4 updated for CEO division team dispatch flow | Phase 2 rewrite (CEO creates teams, dispatches C-suite as teammates), Phase 3 update (team leads SendMessage C-suite), Phase 4 update (synchronization via recommendation files) |
| DISP-04 | `config/orchestration-protocol.md` Production Spawn Sequence updated for CEO-managed CCO wave dispatch | CEO creates production team, dispatches CCO + wave agents, CCO coordinates via SendMessage |
| DISP-05 | CEO agent updated with TeamCreate instructions, team lead dispatch with sub-questions, and CCO wave management | CEO gains: division team creation, notification-triggered team lead dispatch, CSO Phase 1.5 sequencing, production wave management |
| DISP-06 | 8 analytical C-suite agents transformed -- Mode B removes TeamCreate/Agent dispatch, adds sub-question file writing + teammate message receiving | C-suite transformation pattern: remove steps 3-4 (TeamCreate/Agent/shutdown), replace with sub-Q file writing + SendMessage notification + teammate receiving |
| DISP-07 | CCO agent transformed to Creative Brief author + editorial coordinator | CCO removes TeamCreate/Agent/shutdown, adds Creative Brief writing + SendMessage wave coordination + editorial gate communication |
| DISP-08 | CSO Phase 1.5 dispatch integrated with division team pattern | CSO dual dispatch: Phase 1.5 division team for research (same sub-Q pattern), Phase 2 standalone for analytical |
| DISP-09 | Sub-question directory documented in Session Output Setup | Add `mkdir -p {session}/sub-questions` to directory creation |
| DISP-10 | No stale TeamCreate, Agent.*team_name, or SendMessage.*shutdown_request references in C-suite | Verification grep: `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/` returns zero matches |
</phase_requirements>

## Standard Stack

This phase involves zero application code. All changes are markdown specification edits to agent definitions and orchestration protocols.

### Core
| Component | File | Purpose | Why It Matters |
|-----------|------|---------|----------------|
| Dispatch protocol | `config/dispatch-protocol.md` (115 lines) | Defines sub-question file convention and CEO-as-dispatcher flow | Complete rewrite -- template for all agent behavior |
| CCO dispatch protocol | `config/cco-dispatch-protocol.md` (198 lines) | Defines CEO-managed production wave sequencing | Complete rewrite -- production pipeline coordination |
| Orchestration protocol | `config/orchestration-protocol.md` (436 lines) | Phases 2/3/4 + Production Spawn Sequence | Surgical updates to 4 sections, preserve remaining sections |
| CEO agent | `agents/ceo.md` (382 lines) | CEO identity + orchestration reference | Major additions for dispatch mechanics |
| 8 analytical C-suite agents | `agents/c-suite/{cfo,cto,coo,ciso,cao,vp-sales,vp-delivery,cso}.md` | Mode B dispatch transformation | Mechanical transformation per template |
| CCO agent | `agents/c-suite/cco.md` (222 lines) | Creative Brief author + editorial coordinator | Special transformation (different from analytical agents) |

### Supporting
| Component | File | Purpose | When Relevant |
|-----------|------|---------|---------------|
| Reference document | `ref/team-refactor-context-260308.md` | Architecture decision rationale | When verifying design intent |
| Prior research | `.planning/research/ARCHITECTURE.md` | Detailed integration points | When understanding file interactions |
| Prior pitfalls | `.planning/research/PITFALLS.md` | 15 catalogued pitfalls | When writing verification steps |

### Files NOT Changed (Transparent to Dispatch)
| Component | Reason |
|-----------|--------|
| All 34 team lead agents | Team leads are dispatched by CEO instead of C-suite but behave identically -- same prompts, same SendMessage, same output files |
| `config/routing-table.md` | Routing logic unchanged |
| `config/decision-modes.md` | CEO synthesis modes unchanged |
| All Python scripts | Zero code changes in this phase |
| Templates | No template changes |

## Architecture Patterns

### Pattern 1: Notification-Triggered Dispatch (Key Decision)

**What:** C-suite agents write sub-question files, then SendMessage the CEO with the file paths. CEO reads files and dispatches team leads. Rolling per-division -- CEO acts as soon as each notification arrives.

**Why this over polling:** The CONTEXT.md locks in notification-triggered dispatch. This eliminates the polling deadlock pitfall (Pitfall #2 from prior research) where the CEO burns turns checking directories. SendMessage is reliable, immediate, and leverages the team communication mechanism already available.

**Flow:**
```
1. CEO creates division team: TeamCreate("cdp-{role}-{slug}")
2. CEO dispatches C-suite agent as teammate (Agent with team_name)
3. C-suite agent reads CEO framing from prompt
4. C-suite agent formulates sub-questions
5. C-suite agent writes sub-Q files to {session}/sub-questions/{role}/{team-lead}.md
6. C-suite agent SendMessages CEO: "Sub-questions ready: {file paths}"
   OR: "No team leads needed -- proceeding with inline analysis"
7. CEO reads sub-Q files
8. CEO dispatches team leads as teammates in same division team
9. Team leads SendMessage findings to C-suite agent
10. C-suite agent synthesizes -> writes _RECOMMENDATION_{role}.md
```

**No-team-leads path:** When a C-suite agent determines no team leads are needed (e.g., Tier 2 with a narrow question), it sends "No team leads needed -- proceeding with inline analysis" and proceeds to synthesize directly from its own analysis. CEO does not wait for sub-question files from that division.

### Pattern 2: CEO-Managed CCO Production Waves

**What:** CEO creates production team, dispatches CCO and wave agents. CCO coordinates via SendMessage -- drives timing and editorial judgment. CEO executes dispatch mechanically.

**Flow:**
```
1. CEO creates team: TeamCreate("cdp-cco-{slug}")
2. CEO dispatches CCO as teammate
3. CCO reads RECORD.md, writes Creative Brief
4. CCO SendMessages CEO: "Creative Brief complete, dispatch Graphic Designer"
5. CEO dispatches Graphic Designer as teammate (Wave 1)
6. Graphic Designer writes _REPORT_graphic-designer.md, SendMessages CCO completion
7. CCO reads report, does assessment
8. CCO SendMessages CEO: "Wave 1 complete, dispatch Writer"
9. CEO dispatches Writer (Wave 2)
... [continues for Editor (Wave 3) and Publisher (Wave 4)]

Revision cycle:
- Editor returns REVISION REQUIRED in _REPORT_editor.md
- CCO reads report, SendMessages CEO with revision instructions
- CEO re-dispatches responsible team lead with instructions
- Maximum one revision cycle, then proceed
```

### Pattern 3: CSO Dual Dispatch

**What:** CSO has two dispatch modes in the new architecture:
- **Phase 1.5 (Research):** Division team pattern -- CEO creates cdp-cso-{slug}, dispatches CSO as teammate, CSO writes sub-Q files for research leads, CEO dispatches research leads. Produces `_DOSSIER_cso.md`.
- **Phase 2 (Analytical):** Standalone subagent (no team_name) -- CSO receives CEO framing + its own Research Dossier, produces `_RECOMMENDATION_cso.md` without team leads.

**Timing:** Phase 1.5 completes fully before Phase 2 begins. CSO Phase 2 dispatch happens simultaneously with other C-suite division team dispatch.

### Pattern 4: Pre-Mortem as Standalone Subagents

**What:** Pre-mortem (Phase 4.5) agents are dispatched as standalone subagents (no team_name), same as current architecture. Division teams dissolve after _RECOMMENDATION_{role}.md is written. Pre-mortem prompts include executive summaries only (lighter context).

### Recommended File Change Sequence

```
Plan 1: Config Protocol Rewrites
  config/dispatch-protocol.md         -- COMPLETE rewrite
  config/cco-dispatch-protocol.md     -- COMPLETE rewrite
  config/orchestration-protocol.md    -- SURGICAL updates to 4 sections

Plan 2: CEO Agent Rewrite
  agents/ceo.md                       -- MAJOR additions

Plan 3: C-Suite Agent Transformations + Verification
  agents/c-suite/cco.md               -- Special transformation (CCO)
  agents/c-suite/cso.md               -- Special transformation (dual dispatch)
  agents/c-suite/cfo.md               -- Template transformation
  agents/c-suite/cto.md               -- Apply template
  agents/c-suite/coo.md               -- Apply template
  agents/c-suite/ciso.md              -- Apply template
  agents/c-suite/cao.md               -- Apply template
  agents/c-suite/vp-sales.md          -- Apply template
  agents/c-suite/vp-delivery.md       -- Apply template
  Verification grep                   -- DISP-10 compliance
```

### Anti-Patterns to Avoid
- **CEO as decision-maker for team lead composition:** CEO must dispatch exactly the team leads that have sub-question files. No additions, no omissions. The CEO is a messenger for dispatch, not a decision-maker about team composition.
- **CEO re-processing sub-questions:** CEO reads sub-Q files and pastes content into team lead prompts verbatim. No re-summarizing, no analytical overhead. This preserves C-suite domain translation and minimizes CEO context consumption.
- **CCO wave dispatch without CCO direction:** CEO must never dispatch a production wave agent without CCO SendMessage authorization. The CEO's role in production is purely mechanical.
- **Mixing old and new dispatch patterns:** Every reference to "standalone background subagent" for C-suite in Phases 2-4 must be replaced with "teammate in CEO-created division team." Stale references cause contradictory instructions.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Sub-question file format | Complex structured format with validation | Simple markdown with Context Brief + Sub-Question + Output Instruction sections | LLM-to-LLM communication -- convention-based format is appropriate (explicitly out of scope per REQUIREMENTS.md) |
| CEO polling mechanism | Directory polling loops with sleep/retry | Notification-triggered dispatch via SendMessage | Locked decision from CONTEXT.md -- eliminates polling deadlock entirely |
| Wave coordination protocol | Custom file-based directive system | CCO SendMessage to CEO with dispatch instructions | Simpler than file-based directives, uses existing team communication |
| Division team dissolution | Explicit shutdown_request protocol | Teams naturally dissolve when CEO stops dispatching to them; no shutdown_request needed | C-suite agents can't send shutdown_request because they're teammates, not team leaders |

## Common Pitfalls

### Pitfall 1: CEO Context Window Exhaustion (CRITICAL)
**What goes wrong:** CEO absorbs all dispatch responsibilities. Tier 3 with 7 divisions means ~35+ team lead dispatches, reading ~30 sub-Q files, reading recommendations, managing production waves. Could be 80-100+ tool calls in one session.
**Why it happens:** Dispatch load concentrated in one agent instead of distributed across 10.
**How to avoid:** Keep CEO agent lean. Sub-question files should be short (context brief + sub-question, not full CEO framing repeated). CEO pastes sub-Q content into prompts verbatim without re-processing. Consider turn budget guidance in CEO agent.
**Warning signs:** CEO Decision Records become shallow. Auto-compaction messages appear. Late divisions receive inconsistent context.

### Pitfall 2: Inconsistent Removal of Old Dispatch Instructions (CRITICAL)
**What goes wrong:** One or more C-suite agents retain TeamCreate/Agent/shutdown_request instructions. Agent attempts to use unavailable tools, wastes turns, never writes sub-question files.
**Why it happens:** 9 C-suite agents have similar but NOT identical Mode B sections. CSO has research-specific language. CCO has completely different 4-wave pattern. Find-and-replace misses agent-specific variations.
**How to avoid:** Process agents in uniqueness order: CCO first (most different), CSO second (dual dispatch), then template analytical agent (CFO), then apply template to remaining 6. Run verification grep after all updates.
**Warning signs:** `grep -rE "TeamCreate|Agent.*team_name|SendMessage.*shutdown_request" agents/c-suite/` returns any matches.

### Pitfall 3: Orchestration Protocol Internal Contradictions
**What goes wrong:** Surgical updates to Phases 2-4 and Production Spawn Sequence leave stale references in other sections. Phase 4 Synchronization still says "background subagents with run_in_background: true" while Phase 2 says "teammates."
**Why it happens:** 436-line protocol with internal cross-references. Editing parts while preserving others creates seams.
**How to avoid:** After all surgical edits, search entire protocol for: "standalone," "without team_name," "run_in_background," "TeamCreate" (should only appear in CEO actions), "Agent tool" (verify context). Full read-through for coherence.
**Warning signs:** Two sentences describe different dispatch mechanisms for the same action.

### Pitfall 4: CCO Split-Brain (CEO Dispatch vs CCO Direction)
**What goes wrong:** CEO dispatches a wave agent before CCO authorizes it, or proceeds to Wave 4 without editorial verdict.
**Why it happens:** Division of responsibility between "who can dispatch" (CEO) and "who decides what to dispatch" (CCO).
**How to avoid:** Define CEO's production role as PURELY MECHANICAL. CEO never dispatches a production wave agent without CCO SendMessage authorization. CCO's SendMessage contains: whether to proceed, which agent to dispatch, and any special instructions.
**Warning signs:** Production artifacts have quality issues the Editor flagged but Publisher didn't address.

### Pitfall 5: CSO Phase 1.5 Timing Not Enforced
**What goes wrong:** CSO dispatched simultaneously with Phase 2 C-suite agents. Research Dossier not available for Phase 0 broadcast.
**Why it happens:** CEO creates all teams in one batch without sequencing CSO first.
**How to avoid:** Explicit sequencing in CEO agent and orchestration protocol: Phase 1 (frame) -> Phase 1.5 (CSO division team, wait for _DOSSIER_cso.md) -> Phase 0 broadcast (with dossier) -> Phase 2 (all other C-suite in parallel). CSO Phase 2 standalone dispatch happens WITH Phase 2, not Phase 1.5.
**Warning signs:** Phase 0 broadcast missing Research Dossier when CSO was activated.

### Pitfall 6: Session Resume Protocol Not Updated for Sub-Question Files
**What goes wrong:** Resume protocol doesn't account for sub-question files as a state marker. Session crashed after C-suite wrote sub-Qs but before team leads dispatched. Resume re-dispatches C-suite, producing different sub-questions.
**Why it happens:** Resume protocol designed before sub-question convention existed.
**How to avoid:** Add new resume rule: "If `{session}/sub-questions/{role}/` contains files but no `_RECOMMENDATION_{role}.md` exists, resume by dispatching team leads using existing sub-question files."
**Warning signs:** Resumed session re-dispatches C-suite agents when sub-question files already exist.

## Code Examples

### Sub-Question File Format (Claude's Discretion)

Recommended format -- simple, minimal, convention-based:

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
definition at .claude/agents/team-leads/{role}/{agent-name}.md. Answer all
forcing questions integrated into your assessment.

## Reference Files
- Session: {absolute-session-path}
- Record: {absolute-session-path}/RECORD.md (if exists)
```

### C-Suite Mode B Transformation Template (Using CFO as Example)

**REMOVE (current steps 3-4, approximately lines 98-134):**
```markdown
3. **Create your division team and dispatch team leads as teammates.**
   Follow the dispatch protocol in `config/dispatch-protocol.md`.

   a. Create your division team:
      `TeamCreate: team_name "cdp-cfo-{issue-slug}"`

   b. Spawn team leads as teammates -- all in a single response:
      [Agent tool calls with team_name]

   c. Team leads complete analysis and SendMessage findings back to you.

   d. After collecting all findings, shut down division team
      (SendMessage type: "shutdown_request" to each teammate).

4. **Collect findings.** Team lead findings arrive via SendMessage
   automatically. If a team lead fails or times out, note the gap
   and proceed with available findings.
```

**REPLACE WITH (new steps 3-4):**
```markdown
3. **Write sub-question files for team leads.**
   For each relevant team lead, write a sub-question file to
   `{session}/sub-questions/cfo/{agent-name}.md` using the Write tool.
   Each file contains:
   - Context brief (3-5 sentences summarizing CEO framing)
   - Your domain-specific sub-question for that team lead
   - Output instruction referencing the team lead's agent definition
   - Reference file paths (session directory, RECORD.md if exists)

   See `config/dispatch-protocol.md` for the sub-question file format.

   Your team leads and their agent names:
   | Team Lead | Agent Name | File Path |
   |-----------|-----------|-----------|
   | Controller | `controller` | `{session}/sub-questions/cfo/controller.md` |
   | Head of FP&A | `fpa-analyst` | `{session}/sub-questions/cfo/fpa-analyst.md` |
   | Treasury/Cash Manager | `treasury-manager` | `{session}/sub-questions/cfo/treasury-manager.md` |
   | AP/AR Manager | `ap-ar-manager` | `{session}/sub-questions/cfo/ap-ar-manager.md` |
   | Tax Lead | `tax-lead` | `{session}/sub-questions/cfo/tax-lead.md` |

   Write sub-question files ONLY for relevant team leads. Not every question
   requires all five team leads. The absence of a sub-question file means
   that team lead is not relevant to this decision.

   After writing all sub-question files, notify the CEO via SendMessage:
   "Sub-questions ready: {list of file paths written}"

   If no team leads are needed for this decision, SendMessage the CEO:
   "No team leads needed -- proceeding with inline analysis"

4. **Receive team lead findings.** You are a teammate in a CEO-created
   division team. Team lead findings arrive via SendMessage automatically --
   team leads will SendMessage their findings to you by name within the
   division team. If a team lead fails or times out, note the gap and
   proceed with available findings.

   Expected team leads: [names from team lead table above]
```

### CCO Transformation Pattern

The CCO transformation is fundamentally different from analytical agents. The CCO:
- Does NOT write sub-question files
- Does NOT dispatch team leads
- DOES write Creative Brief (unchanged)
- DOES coordinate waves via SendMessage to CEO
- DOES read _REPORT_*.md files and make editorial decisions
- DOES communicate editorial verdicts and revision instructions to CEO via SendMessage

Key sections to rewrite:
- Remove: `TeamCreate`, `Agent tool call`, `SendMessage type: "shutdown_request"`
- Add: SendMessage notification to CEO for each wave transition
- Add: Receiving _REPORT completions via SendMessage from team leads
- Preserve: Creative Brief Protocol (unchanged)
- Preserve: Editorial Review Gate logic (unchanged, but communication changes to SendMessage)
- Preserve: Completion Report (unchanged)

### CSO Dual Dispatch Pattern

**Mode B (Phase 1.5 Research):** Same as analytical C-suite agents -- writes sub-Q files for research team leads, SendMessages CEO with file paths. But:
- Output file is `_DOSSIER_cso.md` (not `_RECOMMENDATION_cso.md`)
- Happens in Phase 1.5, before Phase 2
- Team leads are research-specific (market-intelligence-lead, etc.)

**Mode B2 (Phase 2 Analytical):** NEW mode -- standalone subagent (no team_name), no team leads. CSO receives CEO framing + its own Research Dossier, produces `_RECOMMENDATION_cso.md` inline. Dispatched simultaneously with other C-suite Phase 2 divisions.

### CEO Division Team Dispatch Logic

The CEO needs these new capabilities documented in its agent definition:

```
Phase 1.5 (if CSO activated):
  1. mkdir -p {session}/sub-questions/cso
  2. TeamCreate("cdp-cso-{slug}")
  3. Agent(cso, team_name="cdp-cso-{slug}", prompt=research directive)
  4. Wait for CSO SendMessage with sub-Q file paths
  5. Read sub-Q files, dispatch research team leads as teammates
  6. Wait for CSO to complete (_DOSSIER_cso.md written)
  7. Read _DOSSIER_cso.md

Phase 0 broadcast (include Research Dossier if available)

Phase 2:
  For each activated analytical role:
    1. mkdir -p {session}/sub-questions/{role}
    2. TeamCreate("cdp-{role}-{slug}")
    3. Agent({role}, team_name="cdp-{role}-{slug}", prompt=CEO framing)

  CSO Phase 2 (simultaneous): Agent(cso, no team_name, prompt=framing+dossier)

  Rolling dispatch:
    As each C-suite SendMessage arrives:
      - "Sub-questions ready: {paths}" -> read files, dispatch team leads
      - "No team leads needed" -> note, no further action for that division

Phase 4:
  Wait for all _RECOMMENDATION_{role}.md files

Phase 4.5 (Tier 3):
  Read executive summaries from recommendations
  Dispatch pre-mortem agents as standalone subagents (no team_name)
  Wait for all _PREMORTEM_{role}.md files

Production:
  1. Write RECORD.md
  2. TeamCreate("cdp-cco-{slug}")
  3. Agent(cco, team_name="cdp-cco-{slug}", prompt=RECORD content)
  4. Wait for CCO SendMessage: "Creative Brief complete, dispatch X"
  5. Dispatch wave agents as CCO directs via SendMessage
  6. Continue until CCO reports production complete
```

### Orchestration Protocol Sections to Update

**Phase 2 (lines ~183-195):** Replace "standalone background subagents via Agent tool without team_name" with CEO division team creation and teammate dispatch. Remove "Each C-suite agent is free to create its own division team" language.

**Phase 3 (lines ~198-204):** Minor wording updates. Team leads still SendMessage C-suite parent. Add: "The CEO dispatched these team leads into the division team based on the C-suite agent's sub-question files."

**Phase 4 (lines ~206-226):** Update synchronization section. C-suite agents write _RECOMMENDATION_{role}.md (unchanged). CEO monitoring mechanism may change (teammates vs background tasks). Remove any "shut down division team" references from C-suite descriptions.

**Production Spawn Sequence (lines ~294-332):** Replace "CEO spawns CCO (single Agent, no team_name)" with CEO creates production team and dispatches CCO as teammate. Replace CCO internal wave management with CEO-managed wave dispatch coordinated by CCO SendMessages.

**Session Output Setup (lines ~276-286):** Add `mkdir -p {session}/sub-questions` to directory creation.

**Session Resume Protocol (lines ~360-389):** Add new resume rule for sub-question files state.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| C-suite creates teams + dispatches team leads | CEO creates all teams + dispatches all agents | v1.4 (this phase) | Workaround for nested session tool restriction |
| CEO polls directories for sub-Q files | C-suite SendMessages CEO with file paths (notification-triggered) | CONTEXT.md decision (this phase) | Eliminates polling deadlock, simpler CEO logic |
| CCO owns entire production pipeline | CEO dispatches, CCO directs via SendMessage | v1.4 (this phase) | Split dispatch authority from creative authority |
| CSO writes _RECOMMENDATION_cso.md for dossier | CSO writes _DOSSIER_cso.md for research, _RECOMMENDATION_cso.md for analytical | CONTEXT.md decision (this phase) | Clear separation of research vs recommendation artifacts |
| C-suite shuts down division team (shutdown_request) | Teams dissolve naturally -- no explicit shutdown needed | v1.4 (this phase) | C-suite agents are teammates, can't send shutdown_request |

## Open Questions

1. **CEO context management for Tier 3 (Claude's Discretion)**
   - What we know: Full Tier 3 could be 80-100+ tool calls in CEO session. Context window pressure is real.
   - What's unclear: Exact strategy for managing context -- should CEO discard sub-Q file content after dispatching team leads? Should turn budget guidance be explicit?
   - Recommendation: Include brief guidance in CEO agent: "After dispatching team leads for a division, do not retain sub-question file content. Focus context on monitoring and synthesis." Keep guidance light -- over-specification risks confusing the model.

2. **Division team completion detection (Claude's Discretion)**
   - What we know: C-suite agents are teammates. When all of a division's agents complete (C-suite + team leads), the team naturally becomes inactive.
   - What's unclear: Does the CEO detect completion via background task notifications, or by checking for _RECOMMENDATION_{role}.md files?
   - Recommendation: CEO monitors for _RECOMMENDATION_{role}.md files (file-based state is more reliable and already established). Background task notifications are a secondary signal.

3. **SendMessage notification exact wording (Claude's Discretion)**
   - What we know: C-suite sends file paths. CCO sends wave coordination messages.
   - Recommendation: Keep wording simple and parseable. C-suite: "Sub-questions ready: {session}/sub-questions/{role}/controller.md, {session}/sub-questions/{role}/fpa-analyst.md" or "No team leads needed -- proceeding with inline analysis." CCO: "Wave 1 complete, dispatch Writer" or "REVISION REQUIRED for Writer: {instructions}."

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | grep + manual coherence review (markdown specification files) |
| Config file | N/A -- no application code tests |
| Quick run command | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/` |
| Full suite command | Quick run command + full read-through of all modified files |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DISP-01 | dispatch-protocol.md rewritten | manual | Read and verify coherence | N/A (rewrite) |
| DISP-02 | cco-dispatch-protocol.md rewritten | manual | Read and verify coherence | N/A (rewrite) |
| DISP-03 | orchestration-protocol.md Phases 2/3/4 updated | manual | Read and verify no stale "standalone subagent" refs in Phase 2/3/4 | N/A (update) |
| DISP-04 | Production Spawn Sequence updated | manual | Read and verify CEO-managed wave pattern | N/A (update) |
| DISP-05 | CEO agent has dispatch mechanics | manual | Read and verify TeamCreate, sub-Q reading, wave management | N/A (update) |
| DISP-06 | 8 analytical agents transformed | smoke | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/{cfo,cto,coo,ciso,cao,vp-sales,vp-delivery,cso}.md` | Existing files |
| DISP-07 | CCO transformed | smoke | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/cco.md` | Existing file |
| DISP-08 | CSO Phase 1.5 integrated | manual | Verify dual dispatch pattern (Phase 1.5 team + Phase 2 standalone) | Existing file |
| DISP-09 | Sub-question directory in Session Output Setup | smoke | `grep "sub-questions" config/orchestration-protocol.md` | Existing file |
| DISP-10 | No stale references | smoke | `grep -rE "TeamCreate\|Agent.*team_name\|SendMessage.*shutdown_request" agents/c-suite/` returns 0 | Existing files |

### Sampling Rate
- **Per task commit:** `grep -rE "TeamCreate|Agent.*team_name|SendMessage.*shutdown_request" agents/c-suite/`
- **Per plan merge:** Full grep + coherence read of all modified files
- **Phase gate:** DISP-10 grep returns zero matches + all protocols read coherently end-to-end

### Wave 0 Gaps
None -- this phase modifies existing markdown files only. No test framework, fixtures, or infrastructure needed.

## Sources

### Primary (HIGH confidence)
- `agents/ceo.md` -- Direct reading of current CEO agent (382 lines)
- `config/orchestration-protocol.md` -- Direct reading of full protocol (436 lines)
- `config/dispatch-protocol.md` -- Direct reading of current dispatch protocol (115 lines)
- `config/cco-dispatch-protocol.md` -- Direct reading of CCO dispatch protocol (198 lines)
- `agents/c-suite/cfo.md` -- Direct reading of template C-suite agent (241 lines)
- `agents/c-suite/cco.md` -- Direct reading of CCO agent (222 lines)
- `agents/c-suite/cso.md` -- Direct reading of CSO agent (341 lines)
- `ref/team-refactor-context-260308.md` -- Reference architecture document (343 lines)
- `.planning/research/ARCHITECTURE.md` -- Prior architecture research
- `.planning/research/PITFALLS.md` -- Prior pitfall research (15 catalogued pitfalls)
- `.planning/phases/12-dispatch-architecture-rewrite/12-CONTEXT.md` -- User decisions from discuss session

### Secondary (MEDIUM confidence)
- Grep verification of current TeamCreate/Agent/shutdown_request references across all 9 C-suite files (confirmed present in all 9)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all files directly read and analyzed
- Architecture: HIGH -- locked decisions from CONTEXT.md provide clear direction; no ambiguity in dispatch pattern
- Pitfalls: HIGH -- 15 pitfalls catalogued in prior research, cross-referenced with CONTEXT.md decisions that resolve several (notification-triggered dispatch eliminates polling deadlock)
- Code examples: HIGH -- transformation templates derived from direct reading of CFO Mode B section

**Research date:** 2026-03-08
**Valid until:** Indefinite -- markdown specification patterns do not change with library updates
