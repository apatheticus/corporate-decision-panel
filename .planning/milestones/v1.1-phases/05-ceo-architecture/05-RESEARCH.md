# Phase 5: CEO Architecture - Research

**Researched:** 2026-03-04
**Domain:** Markdown agent architecture refactoring (prompt engineering document structure)
**Confidence:** HIGH

## Summary

Phase 5 is a pure markdown refactoring operation. The CEO agent (`agents/ceo.md`, currently 682 lines) must be split into two documents: a focused identity/synthesis file (under 350 lines) and a new orchestration protocol document (`config/orchestration-protocol.md`). Simultaneously, all 8 C-suite agent files need a structured executive summary block prepended to their Mode B output templates, and the CEO's Phase 5 synthesis logic needs updated to read summaries first with a conflict-triggered deep-dive pattern.

No code changes, no library installations, no test framework modifications. Every change is a markdown edit to agent definition files and config documents. The project's existing patterns (YAML frontmatter, markdown sections, config files in `config/`, agents referencing config via section pointers) provide clear structural precedents.

**Primary recommendation:** Execute in two waves -- Wave 1 extracts orchestration from CEO.md and creates the protocol document; Wave 2 adds executive summaries to C-suite agents and updates CEO synthesis logic. This avoids the risk of editing 10 files simultaneously without validating the extraction first.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**CEO identity boundary:**
- `/evaluate` triage logic STAYS in CEO -- triage is judgment (assessing tier/mode), not orchestration
- Multi-mode comparison protocol STAYS in CEO -- it's the CEO running synthesis N times with different mode modifiers
- Susceptibility mitigation STAYS in CEO -- self-awareness directives are identity
- Tier-specific behavior STAYS in CEO -- defines synthesis style per tier
- Mode/tier interaction matrix STAYS in CEO -- defines CEO's weighting behavior
- Config references section STAYS in CEO -- brief, helpful pointers
- Five-phase cascade (Phases 0-5) EXTRACTED -- core orchestration protocol
- Production pipeline trigger EXTRACTED -- session setup, DAG spawning, artifact dependencies are orchestration
- Organizational roster EXTRACTED -- reference data for routing, CEO doesn't need it for synthesis

**Executive summary design:**
- Executive summary is an ADDITIONAL BLOCK prepended to the existing Domain Recommendation -- not a replacement
- Full recommendation stays intact below the executive summary block
- Format: structured fields only, ~4-6 lines total:
  - Role: [agent role]
  - Position: [Approve / Approve with Conditions / Oppose / Neutral]
  - Confidence: [High / Medium / Low]
  - Key Risks: [2-3 bullet points]
- IDENTICAL format across all 8 C-suite agents (including CSO -- CSO translates its dossier into the same fields)
- Risks only in the summary -- no opportunities field (opportunities are in the full recommendation)

**Deep-dive trigger criteria:**
- CEO reads executive summaries FIRST for all domain recommendations
- Trigger to read full recommendations: CONFLICTING POSITIONS between executive summaries (e.g., CTO Approve vs CISO Oppose on the same risk dimension)
- When deep-diving, CEO reads ONLY the conflicting domains' full recommendations -- not all of them
- CEO explicitly states in the Decision Record which domains were read in full vs summary-only, and why (audit trail -- fits existing "transparency over elegance" principle)
- Summary-first approach applies to ALL tiers (Tier 2 and Tier 3) -- consistent cognitive pattern regardless of panel size

**Extraction destination:**
- Orchestration protocol goes to `config/orchestration-protocol.md` -- alongside routing-table.md, decision-modes.md, company-profile.md
- CEO.md references the protocol with a section pointer + 2-3 sentence summary per phase (CEO knows the flow without embedding the full protocol)
- Orchestration protocol REFERENCES existing config files (routing-table.md, decision-modes.md) -- no duplication
- Routing logic currently inline in CEO.md moves to orchestration-protocol.md, which references config/routing-table.md for actual table data

### Claude's Discretion
- Exact section ordering within the refactored CEO.md
- How to phrase the phase summaries in the CEO's reference section
- Whether config references section needs updating after extraction
- Exact wording of the executive summary block header/template in C-suite agents

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ARCH-01 | CEO orchestration protocol is extracted into a separate referenced document, with CEO agent focused on identity and synthesis | Line-by-line section analysis identifies exactly which CEO.md sections (319 lines) move to `config/orchestration-protocol.md` and which (355 lines pre-refactor) stay. Section mapping provided below. |
| ARCH-02 | CEO agent is under 350 lines after extraction, with zero duplication of orchestration logic | Current 682-line breakdown shows 355 lines of STAY content. After replacing extracted sections with 2-3 sentence phase summaries (~30 lines) and removing redundant transition text, the refactored CEO.md will be approximately 290-330 lines -- under the 350-line cap. |
| ARCH-03 | C-suite agents produce structured executive summary fields (role, position, confidence, key-risks) alongside full recommendations | All 8 C-suite agents analyzed. Six (CFO, CTO, CISO, CAO, VP Sales, CSO) have explicit Mode B code-block output templates. Two (COO, VP Delivery) have synthesis instructions but no code-block template. All 8 need the identical executive summary block prepended. |
| ARCH-04 | CEO reads executive summaries first and references full recommendations only when ambiguity requires it | CEO Phase 5 synthesis section (lines 235-360, 126 lines) needs updated Step 1 to read executive summaries first, plus a new step for deep-dive triggering on conflicting positions. Decision Record template needs a new audit trail field. |
</phase_requirements>

## Standard Stack

This phase involves no software dependencies. All changes are to markdown agent definition files.

### Core
| File Type | Location | Purpose | Why Standard |
|-----------|----------|---------|--------------|
| Agent definitions | `agents/*.md` | LLM agent prompts with YAML frontmatter | Established project pattern |
| Config documents | `config/*.md` | Referenced configuration and protocol specs | Established project pattern -- routing-table.md, decision-modes.md, company-profile.md already exist here |

### Supporting
| File | Purpose | When Modified |
|------|---------|---------------|
| `SKILL.md` | Skill-level documentation referencing CEO orchestration phases | References to "five-phase cascade" and phase descriptions may need updating to point to orchestration-protocol.md |

### Alternatives Considered
None -- the CONTEXT.md decisions lock all structural choices. No alternatives to evaluate.

## Architecture Patterns

### Current CEO.md Section Map (682 lines)

This is the authoritative breakdown of what STAYS vs. what gets EXTRACTED:

```
STAYS in CEO.md (identity, judgment, synthesis):
  Lines   1-  8 (  8 lines): YAML frontmatter + title
  Lines   9- 24 ( 16 lines): ## Your Identity and Mandate
  Lines 235-360 (126 lines): ### Phase 5 -- CEO Deliberation (Synthesis) *
  Lines 361-429 ( 69 lines): ## /evaluate -- Issue Triage Logic (all subsections)
  Lines 430-491 ( 62 lines): ## Multi-Mode Comparison (all subsections)
  Lines 492-521 ( 30 lines): ## Susceptibility Mitigation (all subsections)
  Lines 522-548 ( 27 lines): ## Tier-Specific Behavior (all subsections)
  Lines 658-673 ( 16 lines): ## Mode/Tier Interaction Matrix
  Lines 674-682 (  9 lines): ## Configuration References
                --------
                ~363 lines raw (before refactoring)

EXTRACTED to config/orchestration-protocol.md:
  Lines  25- 28 (  4 lines): ## The Five-Phase Cascade (header)
  Lines  29- 36 (  8 lines): ### Company Context Loading
  Lines  37- 57 ( 21 lines): ### Phase 0 -- Shared Consciousness Broadcast
  Lines  58-135 ( 78 lines): ### Phase 1 -- Frame and Route
  Lines 136-172 ( 37 lines): ### Phase 1.5 -- CSO Research Directive
  Lines 173-185 ( 13 lines): ### Phase 2 -- C-Suite Dispatches Downward
  Lines 186-195 ( 10 lines): ### Phase 3 -- Team Leads Produce Findings
  Lines 196-211 ( 16 lines): ### Phase 4 -- C-Suite Synthesizes Upward
  Lines 212-234 ( 23 lines): ### Phase 4.5 -- Pre-Mortem Dispatch
  Lines 549-622 ( 74 lines): ## Production Pipeline Trigger (all subsections)
  Lines 623-657 ( 35 lines): ## The Organizational Roster (all subsections)
                --------
                ~319 lines move out

* Phase 5 synthesis STAYS because it's the CEO's primary
  analytical contribution -- identity/judgment, not orchestration.
```

### Refactored CEO.md Target Structure

```markdown
---
name: ceo
description: "Chief Executive Officer - Synthesizer perspective..."
model: opus
---

# CEO -- Chief Executive Officer

## Your Identity and Mandate
[16 lines -- unchanged]

## Orchestration Protocol Reference
[NEW SECTION -- ~30 lines]
[2-3 sentence summary per phase, pointing to config/orchestration-protocol.md]
[Replaces the 319 lines of extracted content with brief awareness]

## CEO Deliberation (Synthesis)
[~130 lines -- Phase 5 content, updated with summary-first logic]
[Step 1 updated: read executive summaries → detect conflicts → selective deep-dive]
[Decision Record template updated: new audit trail field]

## /evaluate -- Issue Triage Logic
[69 lines -- unchanged]

## Multi-Mode Comparison
[62 lines -- unchanged]

## Susceptibility Mitigation
[30 lines -- unchanged]

## Tier-Specific Behavior
[27 lines -- unchanged]

## Mode/Tier Interaction Matrix
[16 lines -- unchanged]

## Configuration References
[~10 lines -- updated to include orchestration-protocol.md reference]
```

**Estimated total: ~290-330 lines** (well under 350-line cap)

### New config/orchestration-protocol.md Structure

```markdown
# CDP Orchestration Protocol

## Overview
[Brief description: this is the authoritative phase sequencing document]
[References: config/routing-table.md, config/decision-modes.md, config/company-profile.md]

## Company Context Loading
[Verbatim from CEO.md lines 29-36]

## Phase 0 -- Shared Consciousness Broadcast
[Verbatim from CEO.md lines 37-57]

## Phase 1 -- Frame and Route
[Content from CEO.md lines 58-135]
[REPLACES inline routing table with: "See config/routing-table.md for default activation rules"]

## Phase 1.5 -- CSO Research Directive (Conditional)
[Verbatim from CEO.md lines 136-172]

## Phase 2 -- C-Suite Dispatches Downward
[Verbatim from CEO.md lines 173-185]

## Phase 3 -- Team Leads Produce Findings
[Verbatim from CEO.md lines 186-195]

## Phase 4 -- C-Suite Synthesizes Upward
[Verbatim from CEO.md lines 196-211]

## Phase 4.5 -- Pre-Mortem Dispatch (Tier 3 Only)
[Verbatim from CEO.md lines 212-234]

## Production Pipeline
[Content from CEO.md lines 549-622]

## Organizational Roster
[Content from CEO.md lines 623-657]
```

### Executive Summary Block Pattern

To be prepended to each C-suite agent's Mode B output template:

```
EXECUTIVE SUMMARY
Role: [Agent Role]
Position: [Approve / Approve with Conditions / Oppose / Neutral]
Confidence: [High / Medium / Low]
Key Risks:
- [Risk 1]
- [Risk 2]
- [Risk 3 if applicable]

---

[EXISTING DOMAIN RECOMMENDATION CONTENT UNCHANGED BELOW]
```

**CSO special case:** The CSO produces a Research Dossier, not a Domain Recommendation. The executive summary block for the CSO translates its dossier findings into the same structured fields. The CSO's "Position" maps to the dossier's directional weight of evidence (e.g., "Evidence Supports" / "Evidence Mixed" / "Evidence Insufficient" / "Evidence Contradicts"), but the CONTEXT.md decision mandates the IDENTICAL format, so the CSO must use the same Position vocabulary (Approve / Approve with Conditions / Oppose / Neutral) interpreted through its investigative lens.

### CEO Synthesis Update Pattern

The CEO's Phase 5 Step 1 needs restructuring from:

```
Current: Read all domain recommendations → Build matrix → Analyze fault lines
```

To:

```
New: Read all executive summaries → Build summary matrix → Detect conflicting
     positions → Deep-dive ONLY conflicting domains' full recommendations →
     Build complete analysis matrix → Analyze fault lines
```

The Decision Record template gains a new field:

```
SYNTHESIS METHODOLOGY
  Domains read in full: [list with rationale per domain]
  Domains read summary-only: [list]
  Deep-dive trigger: [what conflict triggered full reading, or "None -- no conflicts detected"]
```

### Anti-Patterns to Avoid

- **Duplicating content between CEO.md and orchestration-protocol.md.** The CONTEXT.md is explicit: "zero duplicated orchestration content." Phase summaries in CEO.md describe the flow at a high level (2-3 sentences each) but do NOT reproduce the detailed protocol steps.
- **Modifying C-suite agent behavior or analytical logic.** The executive summary is an additional output block, not a change to how agents analyze. Mode B analytical process stays identical.
- **Breaking the CSO's unique role.** The CSO's executive summary uses the same format but must not imply the CSO is producing a recommendation. The CSO's "Position" field reflects the evidence direction, not advocacy.
- **Over-engineering the deep-dive trigger.** The trigger is simple: conflicting positions between executive summaries. Do not add complex scoring or threshold logic -- the CEO model can interpret "CTO Approve vs CISO Oppose on the same risk dimension" naturally.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Routing table duplication | Inline routing tables in orchestration-protocol.md | Reference `config/routing-table.md` | Content already exists; single source of truth |
| Decision mode definitions | Inline mode descriptions in orchestration-protocol.md | Reference `config/decision-modes.md` | Content already exists; will be formalized further in Phase 7 |
| Structured validation of executive summaries | Any programmatic validation of markdown output | Trust the prompt template pattern | This is a prompt engineering project -- agents follow templates because of instructional framing, not code enforcement |

**Key insight:** This project is a markdown-based prompt engineering system. There is no runtime validation, no code parsing, no schema enforcement. Quality comes from clear, unambiguous templates that LLM agents follow. The executive summary block works because the template is precise and the instruction is mandatory.

## Common Pitfalls

### Pitfall 1: Exceeding the 350-Line Cap
**What goes wrong:** After extraction, the CEO.md is still over 350 lines because the phase summary section is too verbose, or transition text from the original wasn't cleaned up.
**Why it happens:** The "2-3 sentence summary per phase" instruction is easy to interpret as "2-3 sentences plus context, examples, and caveats."
**How to avoid:** Each phase summary should be exactly 2-3 sentences -- a brief description of what happens in that phase and nothing more. No examples, no edge cases, no conditional logic. Those belong in the orchestration protocol.
**Warning signs:** Any phase summary exceeding 4 lines. Any section that starts explaining "when" or "how" in detail rather than just "what."

### Pitfall 2: Breaking Cross-References
**What goes wrong:** After extraction, references in SKILL.md, commands/cdp/, or other parts of the project still point to CEO.md for orchestration details that now live in orchestration-protocol.md.
**Why it happens:** The CEO.md has been the single source of truth for the entire cascade protocol. Many documents reference it implicitly.
**How to avoid:** After extraction, grep for references to "ceo.md", "CEO", "five-phase cascade", "Phase 0", "Phase 1", etc. in SKILL.md and commands/. Update references that pointed to CEO.md for orchestration content to point to config/orchestration-protocol.md instead. References that point to CEO.md for synthesis, triage, or multi-mode comparison should remain.
**Warning signs:** SKILL.md describing the phase cascade but not mentioning orchestration-protocol.md.

### Pitfall 3: Inconsistent Executive Summary Across Agents
**What goes wrong:** Agents with different Mode B template structures get slightly different executive summary formatting, breaking the CEO's ability to scan all 8 uniformly.
**Why it happens:** Six C-suite agents (CFO, CTO, CISO, CAO, VP Sales, CSO) have explicit code-block output templates. Two (COO, VP Delivery) have only synthesis instructions without code-block templates. The implementation may apply the summary block differently.
**How to avoid:** The executive summary block text must be identical across all 8 files -- copy-paste, not rewrite. For COO and VP Delivery, the executive summary block should be added as a new code-block template section since they lack one.
**Warning signs:** Diff comparison of the executive summary block across all 8 agents shows any variation.

### Pitfall 4: CSO Executive Summary Confusion
**What goes wrong:** The CSO's executive summary is framed as a recommendation when the CSO's mandate is evidence-only. This undermines the CSO's investigative neutrality.
**Why it happens:** The executive summary format uses "Position" and "Key Risks" -- vocabulary that implies advocacy. The CSO's mandate is explicitly non-positional.
**How to avoid:** Add a brief instruction in the CSO agent file explaining how to interpret the executive summary fields through an investigative lens. Position maps to evidence weight (but uses the same vocabulary per the locked decision). The instruction should clarify that this is a structured summary of findings, not a departure from investigative neutrality.
**Warning signs:** The CSO agent file has the executive summary template but no instruction about how to interpret the fields.

### Pitfall 5: Phase 5 Synthesis Logic Becomes Incoherent
**What goes wrong:** The updated synthesis steps (summary-first, deep-dive on conflict) are added alongside the existing Phase 5 steps without properly integrating, creating contradictory instructions.
**Why it happens:** The existing Phase 5 has 5 steps (Map matrix -> Fault-line analysis -> Most determinative perspective -> Apply mode -> Decision Record). The summary-first logic must modify Step 1 but also connects to Step 2 (fault-line analysis uses deep-dive results). If added as a bolt-on rather than integrated, the steps conflict.
**How to avoid:** Rewrite Step 1 to incorporate summary-first reading. Add the deep-dive logic as part of Step 1, not as a separate step. The rest of the steps (2-5) work on the results of Step 1 regardless of whether full recommendations or summaries were read.
**Warning signs:** The synthesis section has more than 5 steps, or Step 1 has two contradictory instructions about reading recommendations.

## Code Examples

### Executive Summary Block -- Standard C-Suite Agent (e.g., CFO)

The block is prepended to the existing Mode B output template:

```markdown
5. **Synthesize domain recommendation.** Produce your CFO Domain Recommendation:

\```
EXECUTIVE SUMMARY
Role: CFO
Position: [Approve / Approve with Conditions / Oppose / Neutral]
Confidence: [High / Medium / Low]
Key Risks:
- [Risk 1]
- [Risk 2]
- [Risk 3 if applicable]

---

CFO DOMAIN RECOMMENDATION

Domain Recommendation: [Approve / Approve with Conditions / Oppose / Neutral]
Confidence Level: [High / Medium / Low]

SUMMARY:
[2-3 sentence synthesis of the overall financial assessment]
[... rest of existing template unchanged ...]
\```
```

### Executive Summary Block -- CSO Special Case

The CSO's executive summary appears at the top of the Research Dossier:

```markdown
\```
EXECUTIVE SUMMARY
Role: CSO
Position: [Approve / Approve with Conditions / Oppose / Neutral]
Confidence: [High / Medium / Low]
Key Risks:
- [Risk 1 -- evidence gap or contradicted assumption]
- [Risk 2 -- evidence gap or contradicted assumption]
- [Risk 3 if applicable]

---

RESEARCH DOSSIER
================
[... existing Research Dossier format unchanged ...]
\```
```

### CEO Phase Summary Reference Section

```markdown
## Orchestration Protocol Reference

The full orchestration protocol is defined in `config/orchestration-protocol.md`.
This section provides a brief overview so the CEO understands the flow without
embedding the full protocol.

**Company Context Loading:** Check for `.cdp-context/company.md` and include its
contents in the Phase 0 broadcast if present.

**Phase 0 -- Shared Consciousness Broadcast:** Broadcast issue context, framing,
and Research Dossier (if available) to all activated C-suite agents simultaneously.
Implements shared consciousness -- everyone sees the same picture before reasoning
independently.

**Phase 1 -- Frame and Route:** Decompose the issue into evaluation dimensions,
classify decision type, route to C-suite using default activation table
(see `config/routing-table.md`), assess full-activation threshold conditions,
and state activation/exclusion reasoning.

**Phase 1.5 -- CSO Research Directive (Conditional):** When the CSO is activated,
issue a structured research directive. The CSO produces a Research Dossier with
evidence summary, assumption registry, and evidence quality grade.

**Phase 2 -- C-Suite Dispatches Downward:** Each activated C-suite executive
translates the CEO framing into domain-specific sub-questions for their team leads.

**Phase 3 -- Team Leads Produce Findings:** Team leads perform specialist analysis
and report to their C-suite parent. The CEO does not see team lead outputs directly.

**Phase 4 -- C-Suite Synthesizes Upward:** Each C-suite executive synthesizes
team lead findings into a domain recommendation with executive summary, confidence
level, key risks, and internal contradictions.

**Phase 4.5 -- Pre-Mortem Dispatch (Tier 3 Only):** After Phase 4, each agent
receives all peer recommendations and answers: "Assume this decision fails
catastrophically in 12 months. What caused the failure?"

For production pipeline trigger, session setup, spawn sequence, and organizational
roster details, see `config/orchestration-protocol.md`.
```

### Updated CEO Synthesis Step 1

```markdown
#### Step 1: Read Executive Summaries and Detect Conflicts

Read the executive summary block from each activated C-suite agent's domain
recommendation (or Research Dossier, for the CSO). Lay out all executive
summaries in a single matrix:

| C-Suite Role | Position | Confidence | Key Risks |
|-------------|----------|-----------|-----------|
| [role] | [Approve/Oppose/Conditions/Neutral] | [H/M/L] | [risk bullets] |

**Conflict detection:** Scan the Position column for opposing positions between
any two agents on related risk dimensions (e.g., one Approve and one Oppose
where both address the same concern). If conflicting positions are detected,
read the FULL domain recommendations for ONLY the conflicting domains -- not
all domains.

**No conflicts detected:** Proceed to Step 2 using executive summary data only.
The full recommendations remain available but are not read unless summaries
reveal ambiguity.

**Audit trail:** Record which domains were read in full vs. summary-only in the
Decision Record's Synthesis Methodology section, with the triggering conflict
or "None -- no conflicts detected."
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Monolithic CEO agent (682 lines) | Split: identity/synthesis (CEO.md) + orchestration (config/orchestration-protocol.md) | Phase 5 (this phase) | Cleaner separation of concerns; CEO focused on judgment |
| CEO reads all full domain recommendations | CEO reads executive summaries first, deep-dives on conflict only | Phase 5 (this phase) | Reduced CEO synthesis input; faster cognitive path; audit trail |
| C-suite output is full recommendation only | C-suite output is executive summary + full recommendation | Phase 5 (this phase) | Enables summary-first CEO pattern; compact overview |

## Open Questions

1. **SKILL.md update scope**
   - What we know: SKILL.md references "five-phase cascade" and phase descriptions that currently point to CEO.md conceptually. Lines 108, 233-234, 236-281, 665 all describe the cascade.
   - What's unclear: Whether SKILL.md should be updated in this phase or left for a documentation pass. SKILL.md is a user-facing document (~700 lines) and changes could be significant.
   - Recommendation: Update SKILL.md minimally in this phase -- add a reference to `config/orchestration-protocol.md` where it describes the cascade. The SKILL.md already describes the phases at a summary level, so it does not need to change its content, just add a pointer to the new authoritative source.

2. **COO and VP Delivery Mode B template gap**
   - What we know: COO (121 lines) and VP Delivery (121 lines) have synthesis instructions but no explicit code-block output template for their Mode B domain recommendation. The other 6 agents all have explicit ```` ``` ```` templates.
   - What's unclear: Whether to add a full code-block template to COO and VP Delivery (to match the other 6) or just add the executive summary block.
   - Recommendation: Add the full code-block template to COO and VP Delivery, matching the pattern of the other agents. This is a minor improvement and ensures the executive summary block has a consistent anchor point across all 8 agents.

3. **Config references section update**
   - What we know: CEO.md's Configuration References section (lines 674-682) lists routing-table.md, decision-modes.md, and company-profile.md with brief descriptions.
   - What's unclear: Whether to add orchestration-protocol.md to this section (Claude's Discretion per CONTEXT.md).
   - Recommendation: Yes, add orchestration-protocol.md to the Configuration References section. It fits the existing pattern exactly.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x |
| Config file | `pytest.ini` |
| Quick run command | `pytest tests/ -x -m "not live"` |
| Full suite command | `pytest tests/ -m "not live"` |

### Phase Requirements to Test Map

This phase modifies markdown agent definition files, not Python code. The existing test suite (188 tests) covers the Python infographic generation system, not the agent prompt files. There are no automated tests for agent markdown content.

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ARCH-01 | CEO orchestration extracted to separate doc | manual-only | N/A -- verify file structure and content | N/A |
| ARCH-02 | CEO agent under 350 lines, zero duplication | manual-only | `wc -l agents/ceo.md` (verify < 350) | N/A |
| ARCH-03 | C-suite agents produce executive summaries | manual-only | N/A -- verify template block in all 8 agent files | N/A |
| ARCH-04 | CEO reads summaries first, deep-dives on conflict | manual-only | N/A -- verify synthesis logic in CEO.md | N/A |

**Justification for manual-only:** This project explicitly excludes automated agent testing (see REQUIREMENTS.md Out of Scope: "Automated agent testing framework -- LLM outputs are non-deterministic; false precision. Use specification-level test scenarios instead."). All ARCH requirements are about markdown file content and structure, not code behavior.

### Sampling Rate
- **Per task commit:** `wc -l agents/ceo.md` (verify under 350) + visual diff review
- **Per wave merge:** Verify all 8 C-suite agent files contain identical executive summary block; verify config/orchestration-protocol.md exists and contains extracted content; verify zero duplication via content comparison
- **Phase gate:** All 5 success criteria from ROADMAP.md verified manually

### Wave 0 Gaps
None -- no test infrastructure changes needed. Validation is structural (file counts, content comparison) rather than behavioral.

## Sources

### Primary (HIGH confidence)
- `agents/ceo.md` -- Full 682-line source file analyzed line-by-line
- `agents/c-suite/*.md` -- All 8 C-suite agent files examined for Mode B output templates
- `config/routing-table.md` -- Existing config file confirming reference pattern
- `config/decision-modes.md` -- Existing config file confirming reference pattern
- `.planning/phases/05-ceo-architecture/05-CONTEXT.md` -- User decisions constraining all architectural choices
- `.planning/REQUIREMENTS.md` -- ARCH-01 through ARCH-04 requirement definitions
- `SKILL.md` -- Skill-level documentation with cascade references

### Secondary (MEDIUM confidence)
- Line count analysis of STAY vs. EXTRACT sections -- computed from source but assumes clean extraction without significant rewording

### Tertiary (LOW confidence)
- None -- all findings verified against primary sources in the repository

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no software dependencies; all changes are markdown edits to files examined in full
- Architecture: HIGH -- every section of CEO.md analyzed with line counts; STAY/EXTRACT boundaries defined by locked user decisions; target line count computed
- Pitfalls: HIGH -- patterns identified from actual file analysis (e.g., COO/VP Delivery template gap, SKILL.md references, CSO special case)

**Research date:** 2026-03-04
**Valid until:** Indefinite -- this is a one-time refactoring with no external dependency changes
