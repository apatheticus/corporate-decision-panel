# Phase 6: Orchestration Hardening - Research

**Researched:** 2026-03-05
**Domain:** Markdown agent specification editing, CLI command creation, session filesystem management
**Confidence:** HIGH

## Summary

Phase 6 is a pure specification-editing and lightweight scripting phase. All five requirements (ORCH-01 through ORCH-05) involve modifications to existing markdown agent definitions, the orchestration protocol, the SKILL.md production section, and the creation of one new slash command file. There are no architecture changes, no new libraries to install, no Python API code to write, and no database migrations. The core technology is markdown prose engineering -- writing precise natural language instructions that AI agents will follow during execution.

The production pre-flight validation (ORCH-01/02) is an orchestrator-level check written as markdown instructions in SKILL.md, not Python code. The existing `scripts/preflight.py` handles Gemini API validation; the new pre-flight covers production task dependencies (pptxgenjs, docx, weasyprint, python3, node). The CSO timeout handling (ORCH-03/04) adds instructions to `cso.md` and `orchestration-protocol.md`, plus a conditional field to all 8 C-suite agent output templates. The cleanup command (ORCH-05) is a new `commands/cdp/cleanup.md` file following the established command pattern.

**Primary recommendation:** Treat this as 5 independent markdown editing tasks, each touching 1-3 files. No file exceeds 350 lines of additions. All changes are verifiable by reading the modified files.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Pre-flight check lives in SKILL.md production section, right before the production DAG (Tasks A-E) -- not in the orchestration protocol
- All production tasks are optional -- the Decision Record (RECORD.md) is always produced regardless of missing deps
- "Required" means required within a specific task: if Task A can't find google-generativeai, Task A fails with explicit install instructions, but Tasks B-E continue
- Pre-flight runs before spawning any tasks and shows a summary table: Task | Status | Missing Deps -- green checkmarks for ready tasks, yellow warnings for skipped tasks with install commands
- Only ready tasks are spawned; skipped tasks are listed with what's needed to enable them
- MaxTurns-based timeout only -- no wall-clock timeout; uses the existing agent turn limit mechanism
- When CSO hits maxTurns, it produces a partial Research Dossier in normal format PLUS an explicit "Research Gaps" section listing each team lead that didn't complete and what intelligence they were investigating
- Split responsibility: orchestration protocol (config/orchestration-protocol.md Phase 1.5) defines the timeout policy; CSO agent (agents/c-suite/cso.md) defines the timeout behavior (how to detect approaching limit, prioritize output, list gaps)
- Phase 0 broadcast (or supplemental broadcast after Phase 1.5) includes an explicit "RESEARCH STATUS: INCOMPLETE -- gaps: [list]" flag when research timed out -- C-suite agents check this flag
- Two-layer approach: executive summary gets a "Research Basis: Partial" field (flag); Domain Recommendation body gets a detailed caveat paragraph explaining which gaps affected the analysis
- "Research Basis" field only appears when research is incomplete -- not in every summary; absence means research was complete or CSO wasn't activated
- Agent discretion on confidence assessment -- no auto-capping of Confidence when research is partial; agents know whether the missing research affects their domain
- Caveats only apply when CSO was activated but timed out -- if CSO was never activated, agents produce normal recommendations without caveats
- New slash command `/cdp:cleanup` in commands/cdp/ -- fits existing command pattern alongside consult, panel, deliberate, evaluate, production
- Default age threshold: 30 days (sessions older than 30 days are candidates)
- Confirmation flow: show table of sessions to be deleted (date, slug, size), then ask for confirmation before proceeding
- Clean deletion -- entire session directory removed, no RECORD.md archiving; users who want to preserve records should export or version-control separately

### Claude's Discretion
- Exact dependency detection method for each production task (file checks, import attempts, command existence)
- How to format the pre-flight table for readability
- Exact wording of CSO timeout instructions and Research Gaps section template
- How /cdp:cleanup discovers and calculates session directory sizes
- Whether to support --older-than flag to override the 30-day default

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ORCH-01 | Production pipeline validates required dependencies before artifact generation, failing explicitly with install instructions | Pre-flight section in SKILL.md with per-task dependency table; detection methods for python3, node, pptxgenjs, docx, google-genai, Pillow, weasyprint |
| ORCH-02 | Production pipeline warns (does not block) when optional dependencies are missing, listing which artifacts will be skipped | Same pre-flight section; all tasks treated as optional per user decision; summary table format with skip/ready status |
| ORCH-03 | CSO Phase 1.5 has a maxTurns-based timeout that broadcasts partial results with explicit gap reporting if research is incomplete | maxTurns addition to CSO frontmatter; timeout detection instructions in cso.md; timeout policy paragraph in orchestration-protocol.md Phase 1.5; RESEARCH STATUS flag in broadcast |
| ORCH-04 | C-suite agents annotate recommendations with confidence caveats when CSO research is incomplete | Conditional "Research Basis: Partial" field in executive summary; caveat paragraph template in Mode B output for all 8 C-suite agents |
| ORCH-05 | Session cleanup script deletes old session directories with confirmation prompt and age-based filtering | New commands/cdp/cleanup.md following established command pattern; directory discovery via .cdp-output/ glob; age calculation from date prefix |
</phase_requirements>

## Standard Stack

### Core
| Library/Tool | Version | Purpose | Why Standard |
|-------------|---------|---------|--------------|
| Markdown | N/A | Agent specification format | All CDP agents, configs, and commands are markdown files |
| YAML frontmatter | N/A | Agent metadata (name, model, maxTurns, tools) | Established pattern across all 42+ agent files |
| Bash/shell commands | N/A | Session cleanup directory operations | Standard filesystem operations (ls, du, rm, find) |

### Supporting (Production Dependencies to Validate)
| Dependency | Required By | Detection Method | Install Command |
|------------|-------------|------------------|-----------------|
| `python3` | Task A (Image Agent), Task E (Archivist) | `which python3` | System package manager |
| `google-genai` (Python) | Task A (Image Agent) | `python3 -c "import google.genai"` | `pip install google-genai>=1.65.0` |
| `Pillow` (Python) | Task A (Image Agent) | `python3 -c "import PIL"` | `pip install Pillow>=10.0.0` |
| `node` | Task B (Presentation), Task C (Document) | `which node` | https://nodejs.org |
| `pptxgenjs` (npm) | Task B (Presentation Agent) | Check in build script context | `npm install pptxgenjs` |
| `docx` (npm) | Task C (Document Agent) | Check in build script context | `npm install docx` |
| `weasyprint` (Python) | Task E (Archivist) | `which weasyprint` or `python3 -c "import weasyprint"` | `pip install weasyprint` |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Per-task dependency check in markdown | Python pre-flight script | Over-engineered: the existing `scripts/preflight.py` handles Gemini API validation; production task deps are best checked by the orchestrator agent at spawn time |
| Wall-clock CSO timeout | maxTurns-based timeout | User locked maxTurns-only; wall-clock requires infrastructure Claude Code doesn't natively support for agent subprocesses |

## Architecture Patterns

### Recommended File Change Structure
```
SKILL.md                                    # Add pre-flight validation section (~40-60 lines)
config/orchestration-protocol.md            # Add timeout policy to Phase 1.5 (~10-15 lines)
                                            # Add RESEARCH STATUS flag to Phase 0 broadcast (~5-10 lines)
agents/c-suite/cso.md                       # Add maxTurns to frontmatter
                                            # Add timeout detection/behavior section (~30-40 lines)
agents/c-suite/cfo.md                       # Add conditional Research Basis field + caveat (~10-15 lines)
agents/c-suite/cto.md                       # Same pattern as cfo.md
agents/c-suite/coo.md                       # Same pattern as cfo.md
agents/c-suite/ciso.md                      # Same pattern as cfo.md
agents/c-suite/cao.md                       # Same pattern as cfo.md
agents/c-suite/vp-sales.md                  # Same pattern as cfo.md
agents/c-suite/vp-delivery.md               # Same pattern as cfo.md
agents/c-suite/cso.md                       # Same pattern (CSO also receives own partial research status)
commands/cdp/cleanup.md                     # New file (~30-50 lines)
```

### Pattern 1: Pre-flight Validation as Orchestrator Instruction
**What:** A markdown section in SKILL.md that instructs the orchestrator (CEO or production trigger agent) to check dependencies before spawning production tasks. Not Python code -- agent-readable instructions.
**When to use:** When the dependency check must happen at the Claude Code agent level (checking for installed npm packages, Python modules, system binaries) before task creation.
**Key insight:** The orchestrator agent can run `which`, `python3 -c "import X"`, and `node -e "require('X')"` commands via its Bash tool. The pre-flight is a set of checks the agent performs, not a standalone script.

**Example:**
```markdown
### Pre-flight Dependency Validation

Before spawning production tasks, validate dependencies for each task:

| Task | Dependencies | Check Command | Install |
|------|-------------|---------------|---------|
| A (Image Agent) | python3, google-genai, Pillow | `python3 -c "from google import genai; from PIL import Image"` | `pip install google-genai>=1.65.0 Pillow>=10.0.0` |
| B (Presentation) | node, pptxgenjs | `node -e "require('pptxgenjs')"` | `npm install pptxgenjs` |
| C (Document) | node, docx | `node -e "require('docx')"` | `npm install docx` |
| D (Web Page) | none | -- | -- |
| E (Archivist) | python3, weasyprint | `python3 -c "import weasyprint"` | `pip install weasyprint` |

**Execution:**
1. Run all check commands
2. Build summary table showing task readiness
3. Print the table for user visibility
4. Spawn ONLY tasks whose dependencies are satisfied
5. List skipped tasks with install instructions
6. ALWAYS produce RECORD.md regardless of task availability
```

### Pattern 2: CSO Timeout via maxTurns with Graceful Degradation
**What:** The CSO agent gets a `maxTurns` value in its YAML frontmatter. The CSO's instructions tell it to monitor its turn count, and when approaching the limit, prioritize producing a partial Research Dossier with explicit gap reporting over completing all team lead dispatches.
**When to use:** Phase 1.5 CSO research where 5 team leads are dispatched and each costs multiple turns.
**Key insight:** Claude Code's `maxTurns` is enforced by the platform. The CSO cannot "detect" its remaining turns programmatically, but it CAN be instructed to prioritize output completeness: "If you have dispatched team leads but not all have returned, produce a partial dossier with what you have and list the gaps." The timeout behavior is an instruction, not code.

**CSO turn budget analysis:**
- CSO has 5 team leads, each dispatched as a subagent
- Each team lead has maxTurns: 5
- CSO needs turns for: receiving directive (1), dispatching leads (1-2), collecting results (1-2), synthesizing dossier (1-2)
- A reasonable maxTurns for CSO: consider that the CSO's turn count does NOT include subagent turns (subagents have their own budgets). The CSO's turns are its own tool calls and responses.
- Recommendation: Set CSO maxTurns to a value that allows completing all 5 dispatches and synthesis under normal conditions but provides a clear ceiling. A value in the range of 15-25 is reasonable -- enough for normal operation, catches runaway loops.

### Pattern 3: Conditional Output Field in Agent Templates
**What:** Adding a field to a template that only appears under specific conditions. The "Research Basis: Partial" field appears in the executive summary ONLY when the RESEARCH STATUS flag indicates incomplete CSO research.
**When to use:** When agents need to conditionally modify their output format based on input signals.

**Example (executive summary modification):**
```markdown
EXECUTIVE SUMMARY
Role: CFO
Position: [Approve / Approve with Conditions / Oppose / Neutral]
Confidence: [High / Medium / Low]
Research Basis: Partial    <-- ONLY include this line when CSO research was incomplete
Key Risks:
- [Risk 1]
- [Risk 2]
```

**Example (caveat paragraph in Domain Recommendation body):**
```markdown
RESEARCH CAVEAT:
[Only include this section when the Phase 0 broadcast contained
"RESEARCH STATUS: INCOMPLETE". Explain which specific research gaps
from the CSO's gap list affect your domain analysis and how they
limit your confidence in specific findings. Do not mechanically
lower your Confidence level -- assess whether the missing research
actually affects your domain.]
```

### Pattern 4: Slash Command File Structure
**What:** New `/cdp:cleanup` command following the established YAML frontmatter + instructions pattern.
**When to use:** Creating new CDP slash commands.

**Example:**
```yaml
---
name: cdp:cleanup
description: Clean up old CDP session directories
argument-hint: "[--older-than days?]"
---

Read the full skill specification at `.claude/skills/corporate-decision-panel/SKILL.md` and follow all instructions there.

The user has invoked the **Session Cleanup** path:

/cdp:cleanup [--older-than days?]

User arguments: $ARGUMENTS

Execute the session cleanup protocol. ...
```

### Anti-Patterns to Avoid
- **Writing Python code for pre-flight dependency checks.** The existing `scripts/preflight.py` handles Gemini API validation. Production task dependencies are checked by the orchestrator agent using simple shell commands. Don't create a separate script for this.
- **Hardcoding turn count detection in CSO instructions.** The CSO cannot read its own turn counter. Instructions should focus on behavioral priorities ("prioritize completing the dossier with available findings") not on counting turns.
- **Adding "Research Basis: Complete" when research was fine.** The user decision is clear: absence of the field means research was complete or CSO wasn't activated. Adding it when everything is fine adds noise.
- **Auto-capping confidence when research is partial.** User explicitly decided against this. Agents assess whether the missing research affects their specific domain.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dependency detection | Custom Python dependency checker | Shell commands (`which`, `python3 -c "import X"`, `node -e "require('X')"`) via agent Bash tool | Simple, cross-platform, no new code to maintain |
| Session age calculation | Date parsing library | Parse YYYY-MM-DD prefix from directory name, compare to current date using shell/agent logic | The date format is already standardized in the session directory naming convention |
| Directory size calculation | Custom file walker | `du -sh` on each session directory | Standard Unix utility, available on all target platforms (macOS/Linux) |
| CSO turn limiting | Custom turn counter | Claude Code's built-in `maxTurns` YAML frontmatter field | Platform-native mechanism, already used by all 34 team lead agents |

**Key insight:** This phase adds no new code -- only markdown instructions and one new command file. The orchestrator agent (Claude Code) already has all the tools needed (Bash, Read, Write) to execute dependency checks and filesystem cleanup.

## Common Pitfalls

### Pitfall 1: Pre-flight Check Placement
**What goes wrong:** Putting the pre-flight in the orchestration protocol instead of SKILL.md, causing it to run during the deliberation cascade rather than only at production time.
**Why it happens:** The orchestration protocol already has the "Production Pipeline Trigger" section, which seems like a natural place.
**How to avoid:** User decision is explicit -- pre-flight goes in SKILL.md production section, right before the production DAG. The orchestration protocol is for the deliberation cascade phases, not production logistics.
**Warning signs:** If the pre-flight instructions appear in `config/orchestration-protocol.md`, they're in the wrong file.

### Pitfall 2: CSO maxTurns Value Too Low
**What goes wrong:** Setting maxTurns too low causes the CSO to routinely hit the limit during normal operation, making "partial research" the default rather than the exception.
**Why it happens:** Underestimating how many turns the CSO needs to dispatch 5 team leads, collect their outputs, and synthesize a dossier.
**How to avoid:** Set maxTurns high enough for normal operation (all 5 leads complete) but low enough to catch genuine runaway execution. The CSO's turns are its own actions, NOT its team leads' turns (they have separate maxTurns: 5 budgets).
**Warning signs:** If CSO research is "incomplete" in most sessions, the maxTurns is too low.

### Pitfall 3: Modifying the Wrong Output Template for Caveats
**What goes wrong:** Adding the Research Basis field to Mode A (Tier 1) or Mode C (Pre-Mortem) output templates instead of Mode B (Tier 2/3 analysis).
**Why it happens:** Each C-suite agent has three modes with separate output templates.
**How to avoid:** CSO research (Phase 1.5) only runs in Tier 2/3 engagements. Caveats only apply in Mode B output. Mode A (Tier 1 hallway question) has no CSO research. Mode C (Pre-Mortem) is a different output entirely.
**Warning signs:** If caveat instructions appear in the Advisory Note format section or the Pre-Mortem section of any agent file.

### Pitfall 4: Breaking Executive Summary Format Consistency
**What goes wrong:** Adding the "Research Basis: Partial" field differently across the 8 C-suite agents, breaking the uniform format that the CEO relies on for matrix scanning.
**Why it happens:** Editing 8 files independently without a consistent template.
**How to avoid:** Define the exact field format once, then apply it identically to all 8 agents. The field goes immediately after the "Confidence" line and before "Key Risks" in every agent.
**Warning signs:** If the Research Basis field appears at different positions in different agent executive summaries.

### Pitfall 5: Cleanup Command Deleting Active Sessions
**What goes wrong:** Deleting a session that is currently being used or was just created.
**Why it happens:** Not filtering by age threshold or miscalculating session age from the directory name.
**How to avoid:** Parse the YYYY-MM-DD prefix from the directory name, calculate days since that date, and only include sessions older than the threshold (default 30 days). Always show the confirmation table before deletion.
**Warning signs:** If the cleanup lists sessions from today or recent days.

### Pitfall 6: RESEARCH STATUS Flag Ambiguity
**What goes wrong:** C-suite agents don't detect incomplete research because the flag is buried in prose or formatted inconsistently.
**Why it happens:** Natural language instructions about "flag" can be interpreted loosely.
**How to avoid:** User decision is explicit: "a single line that C-suite agents can pattern-match on, not buried in prose." Use exactly: `RESEARCH STATUS: INCOMPLETE -- gaps: [list]` as a standalone line in the broadcast.
**Warning signs:** If the flag text is part of a paragraph rather than a standalone, clearly formatted line.

## Code Examples

Verified patterns from the existing codebase:

### Existing Slash Command Pattern (commands/cdp/production.md)
```yaml
---
name: cdp:production
description: Re-run the production pipeline for an existing CDP session
argument-hint: "[session-path?]"
---

Read the full skill specification at `.claude/skills/corporate-decision-panel/SKILL.md` and follow all instructions there.

The user has invoked the **Production Re-run** path:

/cdp:production [session-path?]

User arguments: $ARGUMENTS

Execute the Production Re-run protocol exactly as described in the Orchestration Protocol section.
```

### Existing Agent YAML Frontmatter with maxTurns (team leads)
```yaml
---
name: market-intelligence-lead
description: "Market landscape and demand signal analyst for CSO domain"
model: haiku
tools:
  - Read
  - Grep
  - Glob
  - WebSearch
maxTurns: 5
---
```

### Existing Executive Summary Block (consistent across all 8 agents)
```
EXECUTIVE SUMMARY
Role: CFO
Position: [Approve / Approve with Conditions / Oppose / Neutral]
Confidence: [High / Medium / Low]
Key Risks:
- [Risk 1]
- [Risk 2]
- [Risk 3 if applicable]
```

### Existing Session Directory Naming Convention
```
.cdp-output/YYYY-MM-DD_<issue-slug>/
```
Examples:
- `.cdp-output/2026-02-22_should-we-acquire-competitor-x/`
- `.cdp-output/2026-02-28_can-we-afford-to-hire-this-quarter/`

### Existing Production DAG (SKILL.md lines 414-540)
The pre-flight validation section goes BEFORE the "Dependency Pipeline" subsection (currently at line 414) and AFTER the "Session Output Directory" description.

### CSO Agent Current Frontmatter (no maxTurns)
```yaml
---
name: cso
description: "Chief Strategy Officer - Investigative perspective on evidence-based research and strategic intelligence"
model: sonnet
---
```
Will become:
```yaml
---
name: cso
description: "Chief Strategy Officer - Investigative perspective on evidence-based research and strategic intelligence"
model: sonnet
maxTurns: 25
---
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| No pre-flight validation | Gemini API pre-flight only (`scripts/preflight.py`) | Phase 3 (v1.0) | Only validates API key/billing; production task deps unchecked |
| No CSO turn limit | Team leads have maxTurns: 5 | Phase 2 (v1.0) | CSO itself has no limit; team leads are bounded |
| No executive summary blocks | Standardized blocks across all 8 agents | Phase 5 (v1.1) | Enables CEO summary-first reading; uniform format to extend |
| No cleanup command | 5 slash commands (consult, panel, deliberate, evaluate, production) | Phase 4 (v1.0) | Session directories accumulate without management |

## Open Questions

1. **Exact CSO maxTurns value**
   - What we know: Team leads have maxTurns: 5. CSO dispatches 5 team leads as subagents. Subagent turns don't count against the parent's budget.
   - What's unclear: How many turns the CSO typically uses for dispatch + collection + synthesis in practice. No empirical data exists since CSO has never had a turn limit.
   - Recommendation: Start with maxTurns: 25 (generous for normal operation, catches genuine runaway). The exact value is Claude's discretion per CONTEXT.md. Can be tuned after observing real usage.

2. **Task D and E dependency chains**
   - What we know: Task D (Web Page) depends on Tasks A, B, C completing. Task E (Archivist) depends on Task D. If A, B, or C is skipped, Task D still has something to build (just without those artifacts).
   - What's unclear: Should Task D be skipped if ALL of A, B, C are skipped? Or should it always run with whatever is available?
   - Recommendation: Task D should always run if it has no dependencies of its own. It only needs the Decision Record (always available) and embeds whatever images/links are available. Task E (Archivist) requires weasyprint and should follow standard skip logic.

3. **Cleanup command handling of in-progress sessions**
   - What we know: Sessions have a date prefix. Active sessions are from today's date.
   - What's unclear: Whether a session from today could be "old" (unlikely with 30-day default, but edge case if --older-than 0 is used).
   - Recommendation: The 30-day default makes this a non-issue. If --older-than is supported, document that values below 1 day are not recommended.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (installed, configured) |
| Config file | `pytest.ini` (markers: `live` for Gemini API tests) |
| Quick run command | `python3 -m pytest tests/ -x -m "not live"` |
| Full suite command | `python3 -m pytest tests/ -m "not live"` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ORCH-01 | Pre-flight validates required deps per task, fails with install instructions | manual-only | N/A -- pre-flight is markdown instructions for the orchestrator agent, not Python code | N/A |
| ORCH-02 | Pre-flight warns on missing optional deps, lists skipped artifacts | manual-only | N/A -- same as ORCH-01, agent-level behavior | N/A |
| ORCH-03 | CSO Phase 1.5 timeout broadcasts partial results with gap reporting | manual-only | N/A -- maxTurns is a platform mechanism; timeout behavior is agent instructions | N/A |
| ORCH-04 | C-suite agents annotate with confidence caveats when research incomplete | manual-only | N/A -- conditional output format in markdown agent specs | N/A |
| ORCH-05 | Cleanup command deletes old sessions with confirmation | manual-only | N/A -- slash command is a markdown file; cleanup logic is agent behavior | N/A |

### Sampling Rate
- **Per task commit:** `python3 -m pytest tests/ -x -m "not live"` (verify no regressions in existing Python scripts)
- **Per wave merge:** `python3 -m pytest tests/ -m "not live"` (full existing suite)
- **Phase gate:** Full suite green + manual verification that modified markdown files parse correctly

### Wave 0 Gaps
None -- this phase modifies markdown specification files and creates one new markdown command file. All requirements are agent-behavior specifications, not testable Python code. The existing test suite covers the Python scripts that are NOT being modified in this phase. Running the existing tests confirms no regressions were introduced.

**Manual verification protocol for markdown changes:**
- [ ] SKILL.md pre-flight section is syntactically valid markdown with correct table formatting
- [ ] CSO maxTurns appears in YAML frontmatter and file still parses as valid agent definition
- [ ] All 8 C-suite agent executive summary blocks have identical Research Basis field placement
- [ ] RESEARCH STATUS flag format is consistent between orchestration-protocol.md and C-suite agent instructions
- [ ] `commands/cdp/cleanup.md` follows the exact YAML frontmatter pattern of existing commands
- [ ] No existing functionality is broken (run a `/cdp:consult cfo: test question` to verify)

## Sources

### Primary (HIGH confidence)
- Project codebase direct inspection -- all files read and analyzed:
  - `SKILL.md` (686 lines) -- full production pipeline specification
  - `config/orchestration-protocol.md` (308 lines) -- full cascade protocol
  - `agents/c-suite/cso.md` (240 lines) -- full CSO agent definition
  - `agents/c-suite/cfo.md` (171 lines) -- representative C-suite agent pattern
  - `agents/c-suite/coo.md` (167 lines) -- second representative for pattern confirmation
  - `agents/ceo.md` (349 lines) -- CEO synthesis and orchestration reference
  - `commands/cdp/*.md` (5 files) -- established slash command pattern
  - `scripts/preflight.py` (167 lines) -- existing Gemini pre-flight
  - `scripts/session.py` (208 lines) -- session orchestration
  - `scripts/config.py` (133 lines) -- config parsing
  - `tests/` (5 test files + conftest.py) -- existing test infrastructure
  - `pytest.ini` -- test configuration
  - `requirements.txt` -- Python dependencies (google-genai, Pillow)
  - All 34 team lead agent files -- maxTurns: 5 pattern confirmed
  - All 8 C-suite agent files -- executive summary block pattern confirmed

### Secondary (MEDIUM confidence)
- Claude Code agent `maxTurns` behavior -- based on documented YAML frontmatter semantics observed across all team lead files. The field is platform-enforced.

### Tertiary (LOW confidence)
- Optimal CSO maxTurns value (25) -- no empirical data on typical CSO turn counts. Value is a reasonable estimate based on workflow analysis. Should be validated through actual usage.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries; all changes are markdown edits to existing files
- Architecture: HIGH -- patterns directly observed in codebase (command format, agent frontmatter, executive summary blocks)
- Pitfalls: HIGH -- derived from reading actual file structure, understanding where each change goes, and identifying the exact lines affected
- CSO maxTurns value: LOW -- needs empirical validation

**Research date:** 2026-03-05
**Valid until:** Indefinite for architecture patterns (stable project structure). CSO maxTurns value should be revisited after first real usage.
