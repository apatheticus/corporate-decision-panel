# Phase 6: Orchestration Hardening - Context

**Gathered:** 2026-03-05
**Status:** Ready for planning

<domain>
## Phase Boundary

Add pre-flight validation to the production pipeline, CSO timeout handling with gap reporting to Phase 1.5, confidence caveats to C-suite agents when research is incomplete, and a session cleanup command. The deliberation cascade itself is not modified — changes go to SKILL.md production section, config/orchestration-protocol.md Phase 1.5, C-suite agent files, and a new cleanup command.

</domain>

<decisions>
## Implementation Decisions

### Pre-flight validation
- Pre-flight check lives in SKILL.md production section, right before the production DAG (Tasks A-E) — not in the orchestration protocol
- All production tasks are optional — the Decision Record (RECORD.md) is always produced regardless of missing deps
- "Required" means required within a specific task: if Task A can't find google-generativeai, Task A fails with explicit install instructions, but Tasks B-E continue
- Pre-flight runs before spawning any tasks and shows a summary table: Task | Status | Missing Deps — green checkmarks for ready tasks, yellow warnings for skipped tasks with install commands
- Only ready tasks are spawned; skipped tasks are listed with what's needed to enable them

### CSO timeout & gap reporting
- MaxTurns-based timeout only — no wall-clock timeout; uses the existing agent turn limit mechanism
- When CSO hits maxTurns, it produces a partial Research Dossier in normal format PLUS an explicit "Research Gaps" section listing each team lead that didn't complete and what intelligence they were investigating
- Split responsibility: orchestration protocol (config/orchestration-protocol.md Phase 1.5) defines the timeout policy; CSO agent (agents/c-suite/cso.md) defines the timeout behavior (how to detect approaching limit, prioritize output, list gaps)
- Phase 0 broadcast (or supplemental broadcast after Phase 1.5) includes an explicit "RESEARCH STATUS: INCOMPLETE — gaps: [list]" flag when research timed out — C-suite agents check this flag

### Confidence caveat format
- Two-layer approach: executive summary gets a "Research Basis: Partial" field (flag); Domain Recommendation body gets a detailed caveat paragraph explaining which gaps affected the analysis
- "Research Basis" field only appears when research is incomplete — not in every summary; absence means research was complete or CSO wasn't activated
- Agent discretion on confidence assessment — no auto-capping of Confidence when research is partial; agents know whether the missing research affects their domain
- Caveats only apply when CSO was activated but timed out — if CSO was never activated, agents produce normal recommendations without caveats

### Session cleanup
- New slash command `/cdp:cleanup` in commands/cdp/ — fits existing command pattern alongside consult, panel, deliberate, evaluate, production
- Default age threshold: 30 days (sessions older than 30 days are candidates)
- Confirmation flow: show table of sessions to be deleted (date, slug, size), then ask for confirmation before proceeding
- Clean deletion — entire session directory removed, no RECORD.md archiving; users who want to preserve records should export or version-control separately

### Claude's Discretion
- Exact dependency detection method for each production task (file checks, import attempts, command existence)
- How to format the pre-flight table for readability
- Exact wording of CSO timeout instructions and Research Gaps section template
- How /cdp:cleanup discovers and calculates session directory sizes
- Whether to support --older-than flag to override the 30-day default

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `config/orchestration-protocol.md`: Phase 1.5 section exists — timeout policy additions go here
- `agents/c-suite/cso.md`: Has Mode B output template (Research Dossier) — timeout behavior instructions go here
- `agents/c-suite/*.md` (8 files): All have executive summary blocks (Role, Position, Confidence, Key Risks) from Phase 5 — Research Basis field extends this format
- `SKILL.md` production section (lines 414-500+): Production DAG and task definitions — pre-flight section goes before Task A-E definitions
- `commands/cdp/`: Five existing commands — cleanup.md follows the same YAML frontmatter + markdown pattern

### Established Patterns
- Agent files use YAML frontmatter (name, description, model, maxTurns) + markdown sections
- C-suite agents have Mode A (Tier 1), Mode B (Tier 2/3), Mode C (Phase 4.5 pre-mortem) — confidence caveats go in Mode B output template
- Executive summary format is identical across all 8 C-suite agents (Phase 5 decision)
- Session output directories at `.cdp-output/YYYY-MM-DD_<issue-slug>/` contain RECORD.md + artifacts (~10-20MB each)
- Slash commands are markdown files in commands/cdp/ with argument-hint in frontmatter

### Integration Points
- SKILL.md production section needs pre-flight validation step before DAG execution
- config/orchestration-protocol.md Phase 1.5 needs timeout policy paragraph
- agents/c-suite/cso.md needs timeout detection and gap reporting instructions
- All 8 C-suite agent Mode B output templates need conditional Research Basis field + caveat paragraph
- Phase 0 broadcast in orchestration protocol needs RESEARCH STATUS flag when applicable
- New commands/cdp/cleanup.md command file

</code_context>

<specifics>
## Specific Ideas

- The pre-flight table should be clear enough that a user can immediately see what's missing and copy-paste the install command — no hunting through docs
- The CSO Research Gaps section should name each team lead that timed out (e.g., "Market Intelligence Lead: market sizing investigation incomplete") so C-suite agents know exactly which intelligence is missing
- The RESEARCH STATUS flag in the broadcast should be unambiguous — a single line that C-suite agents can pattern-match on, not buried in prose

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 06-orchestration-hardening*
*Context gathered: 2026-03-05*
