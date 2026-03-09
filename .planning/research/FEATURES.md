# Feature Landscape: v1.4 Team Refactor

**Domain:** Multi-agent dispatch architecture, slug resolution, validation leniency, production fixes
**Researched:** 2026-03-08
**Confidence:** HIGH (features derived from production error logs, architecture confirmed against Claude Code official docs, codebase audit complete)

## Context

CDP v1.3 shipped 48 agents across a three-tier hierarchy (CEO > C-suite > team leads) with the assumption that C-suite agents could use TeamCreate and Agent tools to dispatch their own team leads. The 2026-03-08 production session revealed this is impossible: Claude Code enforces a strict "no nested teams" constraint -- only the main session (the lead) can use TeamCreate and Agent tools. Teammates and subagents cannot spawn further agents. This is a documented, by-design limitation confirmed in official Claude Code docs (code.claude.com/docs/en/agent-teams: "teammates cannot spawn their own teams or teammates. Only the lead can manage the team.") and GitHub issue #4182.

Additionally, 5 production bugs surfaced: infographic slug mismatches, PDF module path failures, logging protocol path resolution, validation over-strictness, and large file read truncation.

This feature landscape covers the 8 active features in the v1.4 milestone, categorized by their criticality to a working system.

## Table Stakes

Features that must work for the system to function. Missing = production failures or architectural deadlock.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Division team dispatch (Fix 4) | Current architecture is non-functional. C-suite agents cannot dispatch team leads at all. 3 of 4 error-producing agents hit this wall. System falls back to inline analysis, defeating the entire design purpose. | HIGH | Complete rewrite of dispatch-protocol.md, cco-dispatch-protocol.md, orchestration-protocol.md Phases 2-4, ceo.md, and all 9 C-suite agent Mode B sections. ~15 files modified. |
| Sub-question file protocol (Fix 4 sub-feature) | CEO cannot formulate domain-specific sub-questions -- that requires C-suite domain expertise. Files bridge the gap: C-suite writes sub-questions, CEO reads and dispatches team leads with those sub-questions. | MEDIUM | New convention: `{session}/sub-questions/{role}/{team-lead-name}.md`. Directory creation in Session Output Setup. Format spec in dispatch-protocol.md. |
| CEO-managed CCO wave sequencing (Fix 4 sub-feature) | CCO production pipeline is strictly sequential (GD > Writer > Editor > Publisher). Someone must manage wave gating. If CEO does not manage it, nobody can -- CCO cannot use Agent tool. | MEDIUM | Rewrite of cco-dispatch-protocol.md. CEO monitors for report files between waves. CCO becomes Creative Brief author + editorial coordinator via SendMessage, not a production team manager. |
| Infographic slug alias resolution (Fix 1) | Production session hit `ConfigError: No template found for type 'fault-lines'` for 3 of 6 infographic types. Graphic designer agent definition uses shorthand slugs that do not match template file names. | LOW | Add `SLUG_ALIASES` dict in generate_infographic.py, apply in `generate_with_retry()` and `load_template()`. Also fix agent definition and session.py. |
| PDF module path fix (Fix 2) | `python3 -m scripts.build_results_pdf` fails when working directory is not the skill root. Publisher agent hits ModuleNotFoundError every time. | LOW | Add `cd <skill-directory> &&` prefix to invocation in publisher.md. One-line fix. |

## Differentiators

Features that improve reliability, DX, or resilience. System works without them but is measurably better with them.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Inline logging protocol (Fix 3) | Eliminates a wasted tool call per agent. All 48 agents reference `config/logging-protocol.md` as a file to read, but the path does not resolve when agents run from a consuming project. The protocol is already broadcast in prompts -- the file reference is redundant. | MEDIUM (bulk) | 48-file update. Each file gets the same ~4-line inline replacement. Low per-file risk, high aggregate effort. The canonical `config/logging-protocol.md` file remains for maintainers. |
| Validation leniency for routing diagrams (Fix 5) | 8-role routing diagram fails vision validation on all 3 attempts. PARTIAL labels are correct for high-density infographics but treated as failures. Real images are fine; validation is the problem. | MEDIUM | Add `type_slug` parameter to `validate_infographic()`. Create `LENIENT_TYPES` set. Modify validation prompt for lenient types to accept PARTIAL labels. Pass `type_slug` through from `generate_with_retry()`. |
| Large file read guidance (Fix 6) | CEO truncates 54.6KB recommendation files via Read tool's 2000-line default. Impact was minimal (executive summaries at top) but could cause data loss on larger sessions. | LOW | Documentation addition to orchestration-protocol.md Phase 4 and ceo.md. Add `Read` with `offset`/`limit` guidance. |

## Anti-Features

Features to explicitly NOT build in v1.4.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Nested team support workaround (claude -p hack) | GitHub issue #4182 documents a `claude -p` Bash workaround for nested spawning. It loses visibility, context sharing, error propagation, and structured output. Creates opaque, unmanageable subprocess chains. | Use the CEO-as-universal-dispatcher pattern. Work within the platform constraint, not around it. |
| C-suite direct team lead dispatch (current design) | The original three-tier dispatch (CEO > C-suite > team leads) is architecturally impossible in Claude Code. Continuing to document it creates confusion and guaranteed production failures. | Remove all TeamCreate/Agent references from C-suite agents. Replace with sub-question file writing. |
| CEO inline sub-question formulation | CEO formulating domain-specific sub-questions for team leads bypasses C-suite domain expertise. CEO asking a Controller about "GAAP implications" is generic; CFO asking about "deferred revenue recognition for asset purchases" is domain-translated. | Preserve C-suite domain translation via sub-question files. The two-step (C-suite writes, CEO dispatches) flow is the minimum viable design that preserves domain expertise. |
| Dynamic slug normalization (fuzzy matching) | Going beyond a static alias map to fuzzy string matching or Levenshtein distance adds complexity for marginal benefit. Only 3 slugs are mismatched, and they are known. | Use a hardcoded `SLUG_ALIASES` dict. Add new aliases when new mismatches are discovered. Explicit is better than implicit. |
| Per-infographic validation profiles | Building a full validation configuration system (per-type prompts, per-type pass/fail criteria, per-type label requirements) is overengineered for the current 6-type system. | Use a simple `LENIENT_TYPES` set. Types in the set get a modified validation prompt. All others use the strict default. Add types to the set as production data justifies. |
| Event-driven sub-question notification | Adds infrastructure complexity (file watchers, event loops) for a system where agents use tool-based file I/O. Over-engineering for the polling model that already works. | CEO polls `{session}/sub-questions/{role}/` directories. Simple, reliable, matches the agent execution model. |
| Schema validation for sub-question files | Sub-question files are markdown written by LLM agents and read by LLM agents. Schema validation of LLM output is a category error -- the consumer (CEO) reads natural language, not parsed structure. | Convention-based format: Context Brief + Sub-Question + Output Instruction. Documented in `dispatch-protocol.md`. |
| Agent-to-agent cross-division messaging | Enabling team leads in different divisions to SendMessage each other violates engineered dissent. If the CTO engineering lead talks to the CFO controller, their analyses contaminate each other. | Keep divisions isolated. CEO bridges divisions by reading recommendation files. Cross-domain awareness comes from Phase 4.5 pre-mortem, not runtime communication. |
| Automated retry of entire failed divisions | Over-engineering for a system where individual agent failures are noted as gaps and the cascade continues. Retry logic risks infinite loops and complexity explosion. | Existing failure handling: note gaps, proceed with available findings. A partial analysis with explicit gap notes is more valuable than blocking on retries. |
| Separate validation models for quality checking | Adding model selection for validation complicates config without proven benefit. The problem is prompt strictness, not model capability. | Fix the prompt: lenient verdict rules for high-density types. Same model, different instructions. |
| Programmatic validation of dispatch protocol correctness | Writing a parser to verify agent definitions correctly follow sub-question file conventions. | Use grep-based verification in the implementation checklist. Check for stale `TeamCreate` references, `Agent.*team_name` patterns, and `SendMessage.*shutdown_request` in C-suite agents. |

## Feature Dependencies

```
Division Team Dispatch (Fix 4)
  |
  +---> Sub-Question File Protocol
  |       (C-suite must write sub-Qs before CEO can dispatch team leads)
  |
  +---> CEO-Managed CCO Wave Sequencing
  |       (CCO production pipeline is a special case of division dispatch)
  |
  +---> Session Output Setup update
          (must create {session}/sub-questions/ directory tree)

Slug Alias Resolution (Fix 1) --> independent, no upstream dependency
PDF Module Path Fix (Fix 2) --> independent, no upstream dependency
Inline Logging Protocol (Fix 3) --> independent, no upstream dependency
Validation Leniency (Fix 5) --> independent, no upstream dependency
Large File Read Guidance (Fix 6) --> independent, no upstream dependency

Fix 1 (Slug Aliases) touches same files as Fix 5 (Validation Leniency):
  generate_infographic.py and validation.py. No semantic conflict but
  review together to avoid merge issues.

Fix 3 (Logging Inline) should precede Fix 4 (Dispatch) because Fix 4
  rewrites C-suite agent Mode B sections. If Fix 3 is done first, the
  C-suite rewrites use the new inline protocol. If Fix 4 is done first,
  the C-suite agents must be re-edited for Fix 3.
```

## Detailed Feature Analysis

### 1. Division Team Dispatch Architecture

**What it is:** Restructure the entire dispatch pattern so the CEO (main session) creates all division teams and dispatches all agents. C-suite agents become teammates who formulate domain-specific sub-questions and receive team lead findings via SendMessage.

**Why this specific pattern:**
- Official Claude Code docs confirm: "teammates cannot spawn their own teams or teammates. Only the lead can manage the team." (HIGH confidence, verified against code.claude.com/docs/en/agent-teams)
- The team-based architecture (vs. standalone subagents) is essential because team leads need SendMessage to communicate findings back to their C-suite parent. Standalone subagents can only return results to their spawner.
- The sub-question file convention preserves the most critical design property: C-suite domain translation. Without it, team leads receive the CEO's generic framing instead of domain-specific questions.

**Architecture before (broken):**
```
CEO (main session)
  Agent(CFO, standalone) --> CFO uses TeamCreate + Agent --> FAILS
```

**Architecture after (working):**
```
CEO (main session)
  TeamCreate("cdp-cfo-{slug}")
    Agent(CFO, team_name)        -- formulates sub-Qs, writes to files
    Agent(controller, team_name) -- CEO dispatches with sub-Q from file
    Agent(fpa-analyst, team_name)
    ...
```

**Two-wave dispatch flow:**
1. CEO creates all division teams (one TeamCreate per activated role)
2. CEO dispatches all C-suite agents as teammates (first wave, parallel)
3. C-suite agents write sub-question files to `{session}/sub-questions/{role}/`
4. CEO polls for sub-question files per division
5. CEO dispatches team leads with sub-questions in prompts (second wave, per-division)
6. Team leads SendMessage findings to their C-suite parent
7. C-suite agents synthesize into `_RECOMMENDATION_{role}.md`
8. CEO reads recommendation files (same as current Phase 4)

**Files modified:** ~15 (config/dispatch-protocol.md, config/cco-dispatch-protocol.md, config/orchestration-protocol.md, agents/ceo.md, 9 C-suite agents, Session Output Setup)

**Risk:** HIGH -- this is a protocol rewrite touching the core dispatch mechanism. Every agent's Mode B behavior changes. Regression risk is the CEO dispatch loop becoming incoherent (missing team leads, wrong sub-questions, broken monitoring).

**Mitigation:** Apply the CFO transformation as a template and replicate across all 9 C-suite agents. Verify with grep for stale patterns (TeamCreate, Agent.*team_name, shutdown_request in C-suite agents should return 0 matches post-implementation).

### 2. Sub-Question File Protocol

**What it is:** A file-based communication channel between C-suite agents and the CEO. C-suite agents write domain-translated sub-questions to `{session}/sub-questions/{role}/{team-lead-name}.md`. CEO polls for these files and uses their content to dispatch team leads.

**Why files, not SendMessage:**
- C-suite agents CAN SendMessage to the CEO (they are in a team). But file-based coordination is more debuggable: files persist in the session directory, can be inspected post-run, and create an audit trail.
- SendMessage is asynchronous and transient. The CEO might miss a message while processing another division. Files are durable state.
- Files allow the CEO to batch-dispatch team leads per division as a complete set, rather than reacting to individual messages.

**File format:** Each sub-question file contains the three-section prompt structure from the existing dispatch-protocol.md: Context Brief + Sub-Question + Output Instruction (+ optional Logging Context + File-Path Preamble).

**Directory creation:** Must be added to Session Output Setup in orchestration-protocol.md:
```bash
mkdir -p .cdp-output/YYYY-MM-DD_<issue-slug>/sub-questions
```

### 3. CEO-Managed CCO Production Wave Sequencing

**What it is:** The CEO takes over wave management for the CCO production pipeline. Currently the CCO is responsible for dispatching Graphic Designer, Writer, Editor, Publisher in sequence. Since CCO cannot use Agent/TeamCreate, the CEO must manage the sequential wave dispatch.

**Key difference from analytical dispatch:** Analytical divisions run in parallel (all C-suite agents dispatched simultaneously). CCO production is strictly sequential (Wave 1 must complete before Wave 2 starts). The CEO must monitor for wave completion report files (`_REPORT_graphic-designer.md`, `_REPORT_writer.md`, etc.) between dispatches.

**CCO's new role:** Creative Brief author + editorial coordinator. CCO stays alive in the team, receives team lead messages via SendMessage, provides editorial direction, and makes quality gate decisions. The CEO handles the mechanical dispatch.

### 4. Infographic Slug Alias Resolution

**What it is:** A defensive `SLUG_ALIASES` dictionary that maps common shorthand slugs to their canonical template file names.

**Known mismatches (from production error logs):**
- `fault-lines` --> `fault-line-map`
- `risk-matrix` --> `risk-opportunity-matrix`
- `action-plan` --> `action-plan-timeline`

**Implementation points:**
1. `scripts/generate_infographic.py` (~line 64): Add `SLUG_ALIASES` dict after `ASPECT_RATIOS`
2. `generate_with_retry()` (line 743): Apply alias before `type_slug` is used
3. `load_template()`: Apply alias before template file lookup
4. `scripts/session.py` `run_session()`: Apply alias before passing to `generate_with_retry()`
5. `agents/team-leads/cco/graphic-designer.md` (lines 54-60): Fix the example code to use correct slugs

**Two-layer defense:** Fix the agent definition (source of the mismatch) AND add defensive alias resolution in code (prevents future mismatches from causing production failures).

### 5. Validation Leniency

**What it is:** Parameterized strictness for vision-based validation. High-density infographic types (like the 8-role routing diagram) legitimately have text that appears PARTIAL to vision models but is actually correct. The current validation treats PARTIAL as a failure, causing 3 consecutive validation failures on a correct image.

**Implementation:**
1. Add `type_slug: str | None = None` parameter to `validate_infographic()` in `scripts/validation.py`
2. Add `LENIENT_TYPES: set[str] = {"routing-diagram"}` constant
3. For lenient types, modify the validation prompt: "PARTIAL labels are acceptable for this high-density infographic. Only MISSING labels or garbled text trigger a FAIL."
4. Pass `type_slug` from `generate_with_retry()` (line 823) to `validate_infographic()`

**Why not auto-detect density:** The list of high-density types is small and known. Auto-detecting density from image content adds an API call and complexity. A static set is the right abstraction level for 6 infographic types.

### 6. Inline Logging Protocol

**What it is:** Replace file-path references to `config/logging-protocol.md` in all 48 agent files with an inline 4-line summary of the protocol. The file reference does not resolve when agents run from a consuming project directory.

**Inline replacement:**
```
Follow the error logging protocol: if LOGGING: ON and SESSION PATH: appear
in your prompt, write {session-path}/logs/errors-{YYYYMMDD-HHmm}-{agent-name}.md
as your last action before SendMessage/TaskUpdate. Log only tool failures,
workarounds, data quality issues, or instruction ambiguity. If no issues,
do not create a log file.
```

**Why inline instead of fixing the path:** The path cannot be fixed portably. The skill directory is not at a predictable location relative to the consuming project. The protocol is already broadcast via `LOGGING: ON` in prompts -- the file reference is redundant. Inlining eliminates the dependency while preserving the protocol behavior.

**Canonical file retention:** `config/logging-protocol.md` remains in the repo as the maintainer reference. It is no longer referenced by agents at runtime.

### 7. PDF Module Path Fix

**What it is:** Add `cd <skill-directory> &&` prefix to the `python3 -m scripts.build_results_pdf` invocation in the publisher agent definition.

**Root cause:** Python's `-m` flag requires the `scripts` package to be importable, which requires the working directory to contain the `scripts/` directory. When the publisher runs from a consuming project's directory, the module import fails.

**One file change:** `agents/team-leads/cco/publisher.md` line 41.

### 8. Large File Read Guidance

**What it is:** Documentation addition noting that recommendation files exceeding 2000 lines should be read with `offset`/`limit` parameters. Executive summaries are always in the first 50 lines.

**Two files:** `config/orchestration-protocol.md` Phase 4 section, `agents/ceo.md` Phase 4 section.

## MVP Recommendation

All 8 features are needed. Prioritization is by implementation order (dependencies + risk management), not "what to cut."

**Implementation order (recommended):**

1. **Fix 1: Slug alias resolution** -- Quick win (30 min). Prevents production failures on next run. Unblocks CCO pipeline testing.
2. **Fix 2: PDF module path** -- Quick win (10 min). One-line fix. Unblocks publisher testing.
3. **Fix 5: Validation leniency** -- Code change (1 hr). Improves routing diagram reliability. Touches same files as Fix 1, so do them close together.
4. **Fix 3: Inline logging protocol** -- Bulk update (2 hr). 48 files, identical pattern. Low per-file risk. Do before Fix 4 so the C-suite agent rewrites in Fix 4 use the new inline protocol.
5. **Fix 4: Division team dispatch** -- Architecture rewrite (4-6 hr). Largest change. Sub-order:
   a. `config/dispatch-protocol.md` -- sets the new pattern
   b. `config/cco-dispatch-protocol.md` -- CCO-specific wave pattern
   c. `config/orchestration-protocol.md` -- Phases 2/3/4 + Production Spawn Sequence + Session Output Setup
   d. `agents/ceo.md` -- CEO dispatch instructions + team lead mapping references
   e. `agents/c-suite/*.md` -- all 9 Mode B sections (use CFO as template)
   f. Verification grep pass
6. **Fix 6: Large file read guidance** -- Documentation only (15 min). Add after orchestration protocol is finalized.

**Defer nothing.** All features address production failures or architectural impossibilities discovered in a real session. The only question is ordering, not scoping.

## Complexity Summary

| Feature | Complexity | Files Modified | Risk | Depends On |
|---------|-----------|----------------|------|------------|
| Slug alias resolution | LOW | 3 (generate_infographic.py, session.py, graphic-designer.md) | LOW -- additive, backward compatible | None |
| PDF module path | LOW | 1 (publisher.md) | LOW -- one-line fix | None |
| Validation leniency | MEDIUM | 2 (validation.py, generate_infographic.py) | LOW -- additive parameter, existing behavior unchanged for non-lenient types | None |
| Inline logging protocol | MEDIUM (bulk) | 48 agent files | LOW per file, MEDIUM aggregate (48 files to verify) | None |
| Division team dispatch | HIGH | ~15 (2 config protocols, 1 orchestration protocol, CEO, 9 C-suite, Session Output Setup) | HIGH -- protocol rewrite, regression risk on entire dispatch mechanism | None (but Fix 3 should precede to avoid double-editing C-suite agents) |
| Sub-question file protocol | MEDIUM | Included in Fix 4 file count | MEDIUM -- new convention, must be coherent with dispatch flow | Fix 4 dispatch rewrite |
| CCO wave sequencing | MEDIUM | Included in Fix 4 file count | MEDIUM -- sequential dispatch is more complex than parallel | Fix 4 dispatch rewrite |
| Large file read guidance | LOW | 2 (orchestration-protocol.md, ceo.md) | LOW -- documentation only | None (but write after Fix 4 to avoid double-editing) |

## Sources

- Claude Code official docs: [Subagents](https://code.claude.com/docs/en/sub-agents) -- confirms "Subagents cannot spawn other subagents"
- Claude Code official docs: [Agent Teams](https://code.claude.com/docs/en/agent-teams) -- confirms "No nested teams: teammates cannot spawn their own teams or teammates. Only the lead can manage the team."
- GitHub Issue [#4182](https://github.com/anthropics/claude-code/issues/4182) -- "Sub-Agent Task Tool Not Exposed When Launching Nested Agents" (closed as duplicate, confirmed by-design)
- [Multi-Agent AI Architecture Patterns](https://www.sitepoint.com/multi-agent-ai-development-architecture/) -- coordinator/dispatcher patterns
- [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) -- file-based coordination, hierarchical dispatch
- [Azure AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) -- orchestration patterns
- [Auto-adaptive thresholds for AI-driven quality gating](https://www.dynatrace.com/news/blog/auto-adaptive-thresholds-for-ai-driven-quality-gating/) -- configurable validation strictness patterns
- Project error logs: `ref/team-refactor-context-260308.md`, `ref/team-refactor-plan-260308.md`
- Codebase audit: `scripts/generate_infographic.py`, `scripts/validation.py`, `scripts/session.py`, all 48 agent definitions
