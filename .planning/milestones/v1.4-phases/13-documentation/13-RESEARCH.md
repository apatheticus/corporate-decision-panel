# Phase 13: Documentation - Research

**Researched:** 2026-03-08
**Domain:** Markdown specification editing -- large file read guidance for Claude Code agents
**Confidence:** HIGH

## Summary

Phase 13 is a documentation-only change. Two markdown files need small, targeted additions: `config/orchestration-protocol.md` (Phase 4 synthesis section) and `agents/ceo.md` (CEO Deliberation Step 1). The guidance addresses a real production issue discovered on 2026-03-08 where the CAO's 54.6KB `_RECOMMENDATION_cao.md` file was truncated by Claude Code's Read tool 2000-line default. Impact was minimal because executive summaries are at the top of recommendation files, but larger sessions could lose data.

Both target files are 453 lines each and were heavily rewritten during Phase 12 (dispatch architecture rewrite). Phase 12 is complete, so these files are now stable and safe to edit.

**Primary recommendation:** Add a short paragraph (3-5 lines) to each file's Phase 4 section documenting the Read tool's `offset`/`limit` parameters for reading large recommendation files. Keep the guidance minimal -- this is a documentation note, not an architectural change.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DOCS-01 | Large file read guidance added to `config/orchestration-protocol.md` Phase 4 synthesis section | Insert guidance paragraph after the Synchronization subsection in Phase 4 (after line 234). The guidance should note the 2000-line Read tool default, recommend `offset`/`limit` for files exceeding that limit, and note that executive summaries are in the first 50 lines. |
| DOCS-02 | Large file read guidance added to `agents/ceo.md` recommendation synthesis section | Insert guidance into CEO Deliberation Step 1 (around line 117), where the CEO reads `_RECOMMENDATION_{role}.md` files. Same content as DOCS-01, adapted for the CEO agent context. |
</phase_requirements>

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Markdown | N/A | Agent specification format | All 48 agent definitions and 4 config protocols are markdown |
| Claude Code Read tool | Built-in | File reading with `offset`/`limit` params | The tool whose behavior the documentation describes |

### Supporting

No supporting libraries. This is a pure documentation change.

### Alternatives Considered

None. The requirements specify exact files and exact sections.

## Architecture Patterns

### Target File Structure

Both target files follow the same pattern -- phased sections with horizontal rule separators:

```
## Phase N -- Phase Name

[Phase description and instructions]

### Subsections

[Details]

---

## Phase N+1 -- Next Phase Name
```

### Insertion Points

**`config/orchestration-protocol.md`** (453 lines):
- Phase 4 section: lines 216-236
- Insert AFTER the Synchronization subsection (line 234) and BEFORE the `---` separator (line 236)
- The Synchronization subsection already discusses reading `_RECOMMENDATION_{role}.md` files, making it the natural location for read guidance

**`agents/ceo.md`** (453 lines):
- CEO Deliberation (Synthesis) section: starts line 111
- Step 1: Read Executive Summaries and Detect Conflicts: starts line 115
- Insert AFTER the existing Step 1 content (around line 127) where the CEO reads recommendation files
- This step already describes reading `_RECOMMENDATION_{role}.md` files, so the guidance is contextually appropriate

### Pattern: Guidance Note Style

Both files use a consistent style for operational guidance. Notes are formatted as:

```markdown
**Label:** Guidance text that explains the what, when, and how.
```

The new guidance should follow this same pattern for consistency.

### Anti-Patterns to Avoid

- **Over-documenting a simple note:** This is a 3-5 line addition, not a new section. Do not create subsection headers or elaborate procedures.
- **Duplicating content verbatim:** The two files serve different audiences (protocol reference vs. agent instructions). Adapt the wording slightly for each context.
- **Adding guidance to additional files:** The requirements specify only 2 files. The earlier research (Pitfall 15) suggested adding guidance to the Editor agent and dispatch protocol, but those are out of scope for DOCS-01/DOCS-02.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| N/A | N/A | N/A | Documentation-only change, no code involved |

## Common Pitfalls

### Pitfall 1: Editing the Wrong Section

**What goes wrong:** The guidance is added to the wrong Phase section (e.g., Phase 2 instead of Phase 4) or to a subsection that doesn't discuss reading recommendation files.
**Why it happens:** Both files have multiple phases and the sections look similar.
**How to avoid:** In `orchestration-protocol.md`, the target is "## Phase 4 -- C-Suite Synthesizes Upward" (line 216), specifically after "### Synchronization" (line 232). In `ceo.md`, the target is "#### Step 1: Read Executive Summaries and Detect Conflicts" (line 115).
**Warning signs:** The guidance paragraph doesn't follow text that discusses reading `_RECOMMENDATION_{role}.md` files.

### Pitfall 2: Conflicting with Phase 12 Edits

**What goes wrong:** Phase 12 rewrote both files extensively. If the phase 13 implementer uses stale line numbers, the edit lands in the wrong place.
**Why it happens:** Line numbers from the reference plan (pre-Phase 12) are stale.
**How to avoid:** Search for the anchor text ("Synchronization" in orchestration-protocol.md, "Read Executive Summaries" in ceo.md) rather than relying on line numbers. Verify the surrounding content matches expected context before editing.
**Warning signs:** The edit tool reports unexpected context around the target lines.

### Pitfall 3: Scope Creep

**What goes wrong:** The implementer adds large file guidance to additional files (Editor agent, dispatch protocol, other agents) beyond the 2 files specified in DOCS-01/DOCS-02.
**Why it happens:** Earlier research (Pitfall 15 in PITFALLS.md) suggested broader guidance distribution.
**How to avoid:** Limit changes to exactly `config/orchestration-protocol.md` and `agents/ceo.md`. Additional file changes are future work, not part of this phase.

## Code Examples

### Recommended Guidance Text for orchestration-protocol.md

Insert after the Synchronization subsection in Phase 4:

```markdown
### Large Recommendation Files

Recommendation files from complex deliberations may exceed the Read tool's 2000-line default. When reading `_RECOMMENDATION_{role}.md` files, if a file appears truncated, re-read with `offset` and `limit` parameters to retrieve remaining sections. Executive summaries are always in the first 50 lines -- the summary-first synthesis approach (Step 1 of CEO Deliberation) naturally handles most cases even if the file is truncated.
```

### Recommended Guidance Text for agents/ceo.md

Insert into Step 1 of CEO Deliberation, after the audit trail paragraph:

```markdown
**Large files:** If a `_RECOMMENDATION_{role}.md` file exceeds the Read tool's 2000-line default, it will be truncated. Executive summaries are in the first 50 lines, so summary-first synthesis works regardless. If you need the full recommendation (conflict-triggered deep-dive), re-read with `offset` and `limit` parameters to retrieve remaining content.
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| No guidance -- CEO reads full files, truncation silent | Documented guidance on Read tool offset/limit | Phase 13 (this phase) | CEO knows to use chunked reads for large files |

**Context:** The 54.6KB CAO recommendation file truncation was discovered in the 2026-03-08 production session. The summary-first synthesis pattern (introduced in v1.1) naturally mitigates the impact -- the CEO reads executive summaries first and only deep-dives on conflicts. This guidance formalizes that resilience and provides the explicit Read tool parameters for when a deep-dive is needed.

## Open Questions

None. This is a well-scoped, well-understood documentation addition with clear insertion points and content.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual verification (grep) |
| Config file | N/A -- documentation-only change |
| Quick run command | `grep -n "offset.*limit\|limit.*offset\|Large.*File\|Large.*Recommendation" config/orchestration-protocol.md agents/ceo.md` |
| Full suite command | Same as quick run |

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DOCS-01 | Large file read guidance in orchestration-protocol.md Phase 4 | manual-only | `grep -c "offset" config/orchestration-protocol.md` | N/A -- grep verification |
| DOCS-02 | Large file read guidance in ceo.md synthesis section | manual-only | `grep -c "offset" agents/ceo.md` | N/A -- grep verification |

**Justification for manual-only:** These are markdown prose additions to agent specification files. There is no executable code to unit test. Verification is confirming the text exists in the correct section of each file.

### Sampling Rate

- **Per task commit:** `grep -n "offset" config/orchestration-protocol.md agents/ceo.md`
- **Per wave merge:** Same
- **Phase gate:** Grep confirms both files contain the guidance text

### Wave 0 Gaps

None -- existing grep-based verification covers all phase requirements.

## Sources

### Primary (HIGH confidence)

- `ref/team-refactor-context-260308.md` -- Original issue description (54.6KB CAO recommendation file truncation)
- `ref/team-refactor-plan-260308.md` -- Fix 6 specification (exact changes and file targets)
- `.planning/research/FEATURES.md` -- Feature analysis with root cause (Read tool 2000-line default)
- `.planning/research/PITFALLS.md` -- Pitfall 15 (guidance not reaching team leads -- noted but out of scope for DOCS-01/DOCS-02)
- `config/orchestration-protocol.md` -- Current file content, Phase 4 section (lines 216-236)
- `agents/ceo.md` -- Current file content, CEO Deliberation Step 1 (lines 115-127)

### Secondary (MEDIUM confidence)

None needed -- all sources are primary project documentation.

### Tertiary (LOW confidence)

None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- documentation-only, no libraries
- Architecture: HIGH -- exact insertion points verified by reading current file content
- Pitfalls: HIGH -- well-documented from prior research phases

**Research date:** 2026-03-08
**Valid until:** Indefinite -- documentation-only change to stable files
