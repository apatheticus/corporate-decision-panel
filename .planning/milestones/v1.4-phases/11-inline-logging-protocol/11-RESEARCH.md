# Phase 11: Inline Logging Protocol - Research

**Researched:** 2026-03-08
**Domain:** Markdown agent definition bulk editing -- text replacement across 48 files
**Confidence:** HIGH

## Summary

Phase 11 is a mechanical bulk-edit operation: replace the file-path reference to `config/logging-protocol.md` in all 48 agent markdown files with an inline summary of the logging protocol. The logging protocol source document is 123 lines and contains activation rules, trigger conditions, file naming, log format, writing mechanics, timing, failure handling, and constraints. The inline replacement must be a condensed summary that makes each agent self-sufficient -- no file reads needed at runtime.

There are exactly three distinct reference patterns across the 48 files: (1) CEO pattern -- reads config, broadcasts logging status, references protocol for own error capture; (2) C-suite pattern -- checks broadcast for logging signals, references protocol after synthesis, passes context to team leads; (3) Team lead pattern -- checks prompt for logging signals, references protocol before final SendMessage/TaskUpdate. The CCO has a slight variant of the C-suite pattern (production report instead of synthesis, production team leads instead of team leads). Each pattern needs a tailored inline replacement.

**Primary recommendation:** Create one plan with two waves -- Wave 1 handles the three replacement templates (CEO, C-suite, team leads), Wave 2 runs the bulk find-and-replace across all 48 files with grep verification.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| AGINF-02 | All 48 agent files use inline logging protocol summary instead of `config/logging-protocol.md` file path reference | Full analysis of all 48 files, three reference pattern variants identified, condensed inline protocol text designed, verification commands defined |
</phase_requirements>

## Standard Stack

Not applicable -- this phase involves only markdown file editing. No libraries, no code. The "stack" is:

| Tool | Purpose | Why |
|------|---------|-----|
| Bash `grep -r` | Verification | Success criteria explicitly requires `grep -r "logging-protocol.md" agents/` returns zero matches |
| Read/Write tools | File editing | Each of 48 agent .md files gets its logging section replaced |

## Architecture Patterns

### File Organization

```
agents/
  ceo.md                          # 1 file  -- CEO pattern
  c-suite/
    cao.md, cco.md, cfo.md,       # 9 files -- C-suite pattern (CCO has minor variant)
    ciso.md, coo.md, cso.md,
    cto.md, vp-delivery.md,
    vp-sales.md
  team-leads/
    cao/    (4 files)             # 38 files -- Team lead pattern
    cco/    (4 files)             #   (CCO team leads have minor variant:
    cfo/    (5 files)             #    "production team" context vs "division team")
    ciso/   (4 files)
    coo/    (4 files)
    cso/    (5 files)
    cto/    (4 files)
    vp-delivery/ (4 files)
    vp-sales/    (4 files)
```

### Pattern 1: CEO Logging Reference (1 file)

**Current text (lines 343-349 of `agents/ceo.md`):**
```markdown
## Agent Logging

At the start of each session, read `.cdp-context/config.md` and check the
"Agent Logging" field. If the value is "on", include `LOGGING: ON` and
`SESSION PATH: <absolute-path>` in the Phase 0 broadcast and all downstream
agent prompts. Follow the logging protocol at `config/logging-protocol.md`
for your own error capture.
```

**Unique aspects:** CEO is the logging broadcaster. Reads config, propagates signals. Also logs its own errors. Uses Write tool for log files.

### Pattern 2: C-suite Logging Reference (9 files)

**Current text (example from `agents/c-suite/cfo.md` lines 204-209):**
```markdown
## Agent Logging

If agent logging is active for this session (the Phase 0 broadcast or your prompt
contains `LOGGING: ON` and `SESSION PATH:`), follow the error logging protocol at
`config/logging-protocol.md` after completing your synthesis. Pass the logging context
(`LOGGING: ON` and `SESSION PATH:`) to all team lead dispatch prompts.
```

**Variant -- CCO (lines 194-200):** Same structure but says "production report" instead of "synthesis" and "production team lead dispatch prompts" instead of "team lead dispatch prompts". The CCO also checks `your prompt` not `the Phase 0 broadcast or your prompt`.

### Pattern 3: Team Lead Logging Reference (38 files)

**Current text (example from `agents/team-leads/cfo/controller.md` lines 133-135):**
```markdown
If agent logging is active for this session (your prompt contains `LOGGING: ON`
and `SESSION PATH:`), follow the error logging protocol at `config/logging-protocol.md`
before your final SendMessage and TaskUpdate.
```

**Variant -- CCO team leads:** Same text but context is "CCO's production team" rather than "C-suite parent's division team". The logging reference itself is identical.

### Inline Replacement Design

The 123-line `config/logging-protocol.md` must be condensed into an inline summary. Key information to preserve:

1. **Activation** -- `LOGGING: ON` + `SESSION PATH:` in prompt (already stated in current references)
2. **When to log** -- Tool failures, workarounds, data quality issues, instruction ambiguity, timeout/capacity issues. No issues = no log file.
3. **File naming** -- `errors-{YYYYMMDD-HHmm}-{agent-name}.md` in `{session-path}/logs/`
4. **Log format** -- Issue blocks with What happened / Expected / Workaround / Impact
5. **Write method** -- C-suite/CEO/CCO production leads: Write tool. Analytical team leads: Bash heredoc with single-quoted delimiter.
6. **Timing** -- Last action before SendMessage/TaskUpdate
7. **Failure handling** -- Abandon logging on write failure, complete task normally
8. **Constraints** -- No effect on analysis/output, no mentions in output, one tool call max

**Recommended inline summary (~30 lines per agent):**

For team leads (most common, 38 files):
```markdown
## Agent Logging

If your prompt contains `LOGGING: ON` and `SESSION PATH: <path>`, error logging is active.

**When to log:** Only when you encounter tool failures, workarounds applied, data quality issues, instruction ambiguity, or timeout/capacity issues. No issues = no log file.

**File:** `{session-path}/logs/errors-{YYYYMMDD-HHmm}-{agent-name}.md`

**Format:**
\```markdown
# Agent Error Log: {Role Title}
**Agent:** {name}  |  **Session:** {session-path}  |  **Date:** {date}
---
## Issue 1: {Brief title}
**What happened:** ...
**Expected:** ...
**Workaround:** ...
**Impact:** ...
\```

**Write method:** Use Bash heredoc with single-quoted delimiter (`'LOGEOF'`).

**Rules:** Log as your last action before SendMessage/TaskUpdate. If the log write fails, abandon logging and complete your task normally. Logging does not change your analysis or output. Do not mention logging in your output or SendMessage. One tool call max for logging.
```

For C-suite (9 files) -- same core but:
- Write method is Write tool (not Bash heredoc)
- Additional instruction: "Pass the logging context (`LOGGING: ON` and `SESSION PATH:`) to all team lead dispatch prompts"
- Timing: "after completing your synthesis" (or "production report" for CCO)

For CEO (1 file) -- same core but:
- Retains the config-reading/broadcasting role
- Write method is Write tool
- No "pass to team leads" instruction (CEO already handles broadcasting)

### Anti-Patterns to Avoid

- **Embedding the full 123-line protocol:** Bloats agent files unnecessarily. A 30-line summary captures all actionable information.
- **Different content across agents for the same role type:** All analytical team leads should have identical logging text. All C-suite should have identical logging text (with CCO variant). Consistency prevents drift.
- **Removing the `## Agent Logging` header:** Keep the section header for discoverability and grep-ability.
- **Leaving partial references:** Ensure `logging-protocol.md` string is completely absent from every file -- partial edits are worse than no edit.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Bulk file editing | Manual per-file edits in 48 files | Structured batch approach: define template, apply systematically | Consistency -- hand-editing 48 files invites typos and drift |

## Common Pitfalls

### Pitfall 1: Missing files in the count
**What goes wrong:** Editing 47 of 48 files and declaring success.
**Why it happens:** Agent file tree has subdirectories; easy to miss one.
**How to avoid:** Start with `find agents/ -name "*.md" -type f | wc -l` to confirm 48 files. End with `grep -r "logging-protocol.md" agents/` to confirm zero matches.
**Warning signs:** Final grep returns any matches.

### Pitfall 2: Inconsistent inline text across same-type agents
**What goes wrong:** Slightly different logging instructions in different team lead files.
**Why it happens:** Copy-paste drift when editing many files.
**How to avoid:** Define the replacement text ONCE per agent type, then apply identically.
**Warning signs:** Diff across same-type agents shows unexpected variations.

### Pitfall 3: Breaking surrounding markdown structure
**What goes wrong:** Deleting too much or too little, corrupting adjacent sections.
**Why it happens:** The logging section boundaries vary slightly (some end at EOF, some have sections after).
**How to avoid:** Identify exact line ranges per file. The logging section always starts with `## Agent Logging` and ends at the next `##` heading or EOF.
**Warning signs:** Agent files have malformed markdown after edit.

### Pitfall 4: Forgetting the CCO variant
**What goes wrong:** CCO and CCO team leads get the standard C-suite/team-lead text instead of their production-specific variant.
**Why it happens:** CCO pattern is structurally identical but has different terminology ("production report" vs "synthesis", "production team leads" vs "team lead dispatch prompts").
**How to avoid:** Treat CCO as an explicit variant. Verify CCO and CCO team leads separately.
**Warning signs:** CCO file says "synthesis" instead of "production report".

### Pitfall 5: CEO losing its broadcaster role
**What goes wrong:** CEO gets the C-suite template and loses the config-reading/broadcasting instructions.
**Why it happens:** CEO is treated as "just another C-suite agent" during bulk edit.
**How to avoid:** CEO has its own template. The config-reading and broadcasting instructions are NOT part of the logging protocol -- they stay in the CEO file. Only the `Follow the logging protocol at config/logging-protocol.md for your own error capture` reference gets replaced with inline protocol text.
**Warning signs:** CEO file no longer mentions `.cdp-context/config.md` reading or Phase 0 broadcast.

## Code Examples

### Verification commands (from success criteria)

```bash
# Must return 48
find agents/ -name "*.md" -type f | wc -l

# Must return 0 matches
grep -r "logging-protocol.md" agents/

# Confirm every agent file has inline logging section
grep -rl "## Agent Logging" agents/ | wc -l  # Should return 48

# Spot-check: inline protocol text present (check for a distinctive phrase)
grep -rl "No issues = no log file" agents/ | wc -l  # Should return 48
```

### File counts by type

| Agent Type | Count | Files |
|------------|-------|-------|
| CEO | 1 | `agents/ceo.md` |
| C-suite (standard) | 8 | `agents/c-suite/{cao,cfo,ciso,coo,cso,cto,vp-delivery,vp-sales}.md` |
| C-suite (CCO variant) | 1 | `agents/c-suite/cco.md` |
| Team leads (analytical) | 34 | All `agents/team-leads/{cao,cfo,ciso,coo,cso,cto,vp-delivery,vp-sales}/*.md` |
| Team leads (CCO production) | 4 | `agents/team-leads/cco/{editor,graphic-designer,publisher,writer}.md` |
| **Total** | **48** | |

### Write method per agent type

| Agent Type | Log Write Method | Reason (from protocol) |
|------------|-----------------|------------------------|
| CEO | Write tool | "C-suite agents, CEO, and CCO production team leads: Use the Write tool" |
| C-suite (all 9) | Write tool | Same as above |
| CCO production team leads (4) | Write tool | "CCO production team leads: Use the Write tool" |
| Analytical team leads (34) | Bash heredoc | "Analytical team leads: Use Bash with a heredoc" |

## State of the Art

Not applicable -- this is a markdown file editing task, not a technology domain.

## Open Questions

None. The scope is fully defined:
- Source content: `config/logging-protocol.md` (123 lines, read and analyzed)
- Target files: 48 agent .md files (all identified with exact paths)
- Reference patterns: 3 types identified (CEO, C-suite, team lead) with 2 minor variants (CCO)
- Success criteria: 3 specific grep/count checks from ROADMAP.md
- No ambiguity in what needs to change

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Bash grep/find (no test framework -- this is a text replacement task) |
| Config file | none |
| Quick run command | `grep -r "logging-protocol.md" agents/` |
| Full suite command | `grep -r "logging-protocol.md" agents/ && find agents/ -name "*.md" -type f \| wc -l && grep -rl "## Agent Logging" agents/ \| wc -l` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AGINF-02a | Every agent file contains inline logging protocol summary | smoke | `grep -rl "No issues = no log file" agents/ \| wc -l` (expect 48) | N/A -- shell command |
| AGINF-02b | No agent file references `config/logging-protocol.md` | smoke | `grep -r "logging-protocol.md" agents/` (expect 0 matches) | N/A -- shell command |
| AGINF-02c | Agent file count unchanged | smoke | `find agents/ -name "*.md" -type f \| wc -l` (expect 48) | N/A -- shell command |

### Sampling Rate
- **Per task commit:** `grep -r "logging-protocol.md" agents/`
- **Per wave merge:** Full verification suite (all 3 commands above)
- **Phase gate:** All 3 verification checks pass

### Wave 0 Gaps
None -- existing test infrastructure (shell commands) covers all phase requirements.

## Sources

### Primary (HIGH confidence)
- Direct file reads of all 48 agent .md files via grep and Read tool
- `config/logging-protocol.md` -- full source protocol (123 lines)
- `.planning/REQUIREMENTS.md` -- AGINF-02 requirement definition
- `.planning/ROADMAP.md` -- Phase 11 success criteria

### Secondary (MEDIUM confidence)
- None needed -- this phase is entirely self-contained within the repository

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no stack, just markdown editing
- Architecture: HIGH - all 48 files examined, all 3 patterns identified, exact line numbers verified
- Pitfalls: HIGH - patterns fully analyzed, variants catalogued, verification commands tested

**Research date:** 2026-03-08
**Valid until:** indefinite (content is repository-internal, not dependent on external libraries)
