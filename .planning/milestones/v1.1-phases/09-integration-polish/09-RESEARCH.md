# Phase 9: Integration Polish - Research

**Researched:** 2026-03-05
**Domain:** Markdown template editing -- closing 2 non-blocking integration gaps from v1.1 milestone audit
**Confidence:** HIGH

## Summary

Phase 9 closes two integration gaps identified by the v1.1 milestone audit (INT-01 and INT-02). Both are straightforward markdown edits to existing files with well-defined targets, clear expected outcomes, and zero architectural impact.

**INT-01** (Medium severity): The `templates/panel-assessment.md` Escalation Note section lacks a dedicated field for enumerating triggered threshold conditions. The orchestration protocol (Step 4) instructs the CEO to surface triggered thresholds in the Escalation Note, and the TEST-01 test scenario expects specific threshold names to appear in a structured enumeration (see `test-scenarios/tier2-partial-activation.md` Expected Output Excerpt, lines 96-127). The template currently has `Recommended Escalation`, `Escalation Rationale`, and `Additional Domains for Tier 3` but no threshold-specific field. A CEO following the template literally would produce generic escalation rationale instead of structured threshold enumeration.

**INT-02** (Low severity): The `/cdp:cleanup` command exists at `commands/cdp/cleanup.md` and functions independently, but is absent from `SKILL.md`'s `invocation:` frontmatter block (which lists 5 commands) and from the Invocation Grammar body section (which has entries for consult, panel, deliberate, evaluate, and production but not cleanup). This makes the command undiscoverable via the skill's documentation entry point.

**Primary recommendation:** Both changes are pure markdown edits with no code, no dependencies, and no risk of regression. They should be implemented in a single plan with two tasks.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| TEST-01 | Test scenario validates Tier 2 partial activation correctly excludes non-requested C-suite agents even when full-activation thresholds are met | INT-01 fix: adding a `Triggered Thresholds` field to panel-assessment.md Escalation Note section completes the wiring expected by the TEST-01 scenario (Assertion 5 and 6 in `test-scenarios/tier2-partial-activation.md`) |
| SPEC-03 | CEO explicitly evaluates each threshold in Phase 1 framing output, making routing auditable | INT-01 fix: the threshold enumeration field in the template ensures the CEO's structured per-condition evaluation has a designated output slot in the Panel Assessment, closing the auditability loop |
| ORCH-05 | Session cleanup script deletes old session directories with confirmation prompt and age-based filtering | INT-02 fix: adding `/cdp:cleanup` to SKILL.md frontmatter and Invocation Grammar makes the cleanup command discoverable through the skill's primary documentation entry point |
</phase_requirements>

## Standard Stack

Not applicable. This phase involves only markdown file edits. No libraries, frameworks, or dependencies are involved.

## Architecture Patterns

### Files to Modify

```
templates/panel-assessment.md    # INT-01: Add triggered-threshold field to Escalation Note
SKILL.md                         # INT-02: Add /cdp:cleanup to frontmatter + Invocation Grammar
```

### INT-01: Panel Assessment Escalation Note Template Edit

**Current state** (lines 105-116 of `templates/panel-assessment.md`):

```
ESCALATION NOTE
[Optional. Include only if the CEO determines the issue warrants
Tier 3 analysis. Reasons for escalation recommendation:]

Recommended Escalation: /deliberate [mode]: [issue]
Escalation Rationale: [Why Tier 3 is warranted -- typically because
the disagreements surfaced are deeper than a working session can
resolve, the issue has cross-cutting implications beyond the
activated domains, or the stakes justify the full pre-mortem process.]
Additional Domains for Tier 3: [roles not activated in this Tier 2
that should be included in the escalated analysis]
```

**Required change:** Add a `Triggered Thresholds` field between `Escalation Rationale` and `Additional Domains for Tier 3`. This field must provide a structured slot for per-condition threshold enumeration, matching the format expected by the TEST-01 test scenario and the orchestration protocol Step 4/5 output format.

**Target format** (derived from orchestration-protocol.md Step 5 format and the TEST-01 Expected Output Excerpt):

```
Triggered Thresholds: [List each triggered condition with status and reasoning.
  Format per condition:
  N. [Condition Name] -- TRIGGERED: [one-sentence reasoning]
  Include only TRIGGERED conditions. Omit if no thresholds were triggered
  (in which case the Escalation Note itself may not be warranted).]
```

**Justification:** The orchestration protocol Step 4 Tier 2 scoping note explicitly states: "triggered thresholds are surfaced in the Panel Assessment's Escalation Note as a recommendation to escalate to Tier 3 with full activation." The TEST-01 scenario's Behavioral Assertion 6 expects the Escalation Note to "explicitly names the 3 triggered conditions (Irreversibility, Market Position Change, Existential Financial Risk)." Without a named template field, this is left to the CEO's improvisation rather than guaranteed by the template structure.

### INT-02: SKILL.md Cleanup Command Discoverability

**Current state of SKILL.md frontmatter** (lines 13-17):

```yaml
invocation:
  - /cdp:consult
  - /cdp:panel
  - /cdp:deliberate
  - /cdp:evaluate
  - /cdp:production
```

**Required change to frontmatter:** Add `/cdp:cleanup` to the invocation list.

**Current state of SKILL.md body:** The Invocation Grammar section (lines 72-169) has subsections for Tier 1 (consult), Tier 2 (panel), Tier 3 (deliberate), Auto-Triage (evaluate), Multi-Mode Syntax, and Production Re-run. No cleanup entry exists.

**Required change to body:** Add a new subsection for Session Cleanup in the Invocation Grammar section, after Production Re-run. The entry should follow the same structure as existing entries: code block with syntax, 1-2 sentences of description, examples, and a brief note about behavior (confirmation, age filtering, default threshold).

**Source for content:** The `commands/cdp/cleanup.md` file (78 lines) defines the command's syntax (`/cdp:cleanup [--older-than days?]`), default age threshold (30 days), and behavior (discover, filter, confirm, delete). The Invocation Grammar entry should be a concise summary consistent with the level of detail in other entries, not a reproduction of the full command file.

### Anti-Patterns to Avoid

- **Over-documenting in SKILL.md:** The cleanup Invocation Grammar entry should match the conciseness level of other entries (3-8 lines of description plus examples). The full protocol lives in `commands/cdp/cleanup.md` and should not be duplicated.
- **Changing the template semantics:** The Escalation Note section must remain marked as `[Optional]`. The triggered-threshold field adds structure to the optional section; it does not make escalation mandatory.
- **Reordering existing fields:** Insert the new field in the logical position (after rationale, before additional domains) without moving existing content.

## Don't Hand-Roll

Not applicable. No custom solutions needed -- both changes are direct markdown template edits.

## Common Pitfalls

### Pitfall 1: Inconsistent Threshold Format Between Template and Protocol

**What goes wrong:** The threshold enumeration format in the panel-assessment template diverges from the format defined in orchestration-protocol.md Step 5 and expected by the TEST-01 scenario.
**Why it happens:** Writing the template field description without cross-referencing the exact format used in both upstream (protocol) and downstream (test scenario) documents.
**How to avoid:** The template field description must use the same `N. [Condition Name] -- TRIGGERED: [reasoning]` format visible in orchestration-protocol.md Step 5 (lines 103-108) and the TEST-01 Expected Output Excerpt (lines 104-118 of `test-scenarios/tier2-partial-activation.md`).
**Warning signs:** The template says "list thresholds" but does not specify the per-condition format.

### Pitfall 2: SKILL.md Frontmatter Ordering Breaks Parsing

**What goes wrong:** Adding `/cdp:cleanup` to the frontmatter invocation list in a position that breaks the YAML list structure.
**Why it happens:** Careless editing of YAML frontmatter.
**How to avoid:** Add the entry as the last item in the invocation list, maintaining the same indentation and dash-prefix format as existing entries.
**Warning signs:** YAML parse errors or the entry appearing as part of the description field.

### Pitfall 3: Cleanup Entry Placement in Invocation Grammar

**What goes wrong:** Placing the cleanup entry within the Multi-Mode Syntax or Production Re-run section instead of as a standalone subsection.
**Why it happens:** The existing sections flow from Tier 1 through Tier 3, then utilities. Cleanup is a utility command like production, not a deliberation tier.
**How to avoid:** Add the cleanup subsection after the Production Re-run subsection (after line 169), using the same `### Heading` level as other subsections. The cleanup command is a session management utility, logically grouped with production re-run.
**Warning signs:** Cleanup description appearing inside the production re-run code block or under the multi-mode syntax section.

## Code Examples

### INT-01: Escalation Note Template With Threshold Field

```markdown
ESCALATION NOTE
[Optional. Include only if the CEO determines the issue warrants
Tier 3 analysis. Reasons for escalation recommendation:]

Recommended Escalation: /deliberate [mode]: [issue]
Escalation Rationale: [Why Tier 3 is warranted -- typically because
the disagreements surfaced are deeper than a working session can
resolve, the issue has cross-cutting implications beyond the
activated domains, or the stakes justify the full pre-mortem process.]
Triggered Thresholds: [List each triggered full-activation threshold
  condition with its status and reasoning. Format per condition:
  N. [Condition Name] -- TRIGGERED: [one-sentence reasoning]
  Include only TRIGGERED conditions. If no thresholds were triggered,
  omit this field.]
Additional Domains for Tier 3: [roles not activated in this Tier 2
that should be included in the escalated analysis]
```

Source: Derived from orchestration-protocol.md Step 5 format (lines 103-108) and TEST-01 Expected Output Excerpt (test-scenarios/tier2-partial-activation.md lines 96-127).

### INT-02: SKILL.md Frontmatter Addition

```yaml
invocation:
  - /cdp:consult
  - /cdp:panel
  - /cdp:deliberate
  - /cdp:evaluate
  - /cdp:production
  - /cdp:cleanup
```

### INT-02: SKILL.md Invocation Grammar Entry

```markdown
### Session Cleanup
```
/cdp:cleanup [--older-than days?]
```
Deletes old CDP session directories from `.cdp-output/` with age-based
filtering and a confirmation prompt before deletion. Default threshold
is 30 days.

- `/cdp:cleanup` -- delete sessions older than 30 days
- `/cdp:cleanup --older-than 7` -- delete sessions older than 7 days
```

Source: Derived from `commands/cdp/cleanup.md` syntax and behavior description, condensed to match the conciseness level of other Invocation Grammar entries.

## State of the Art

Not applicable. This phase involves template edits, not technology choices.

## Open Questions

None. Both integration gaps are fully specified by the milestone audit, the orchestration protocol, and the TEST-01 test scenario. The target files, exact locations, required formats, and expected outcomes are all documented.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual verification (markdown inspection) |
| Config file | none |
| Quick run command | Visual inspection of modified files |
| Full suite command | Cross-reference panel-assessment.md with orchestration-protocol.md Step 5 and test-scenarios/tier2-partial-activation.md Expected Output Excerpt; verify SKILL.md frontmatter YAML parses correctly |

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TEST-01 | panel-assessment.md Escalation Note includes triggered-threshold enumeration field | manual-only | Verify `templates/panel-assessment.md` contains `Triggered Thresholds:` field in Escalation Note section | N/A |
| SPEC-03 | Threshold evaluation has designated output slot in Panel Assessment template | manual-only | Cross-reference `templates/panel-assessment.md` Triggered Thresholds format against `config/orchestration-protocol.md` Step 5 format | N/A |
| ORCH-05 | /cdp:cleanup discoverable in SKILL.md | manual-only | Verify `SKILL.md` frontmatter contains `/cdp:cleanup` and body contains Session Cleanup subsection in Invocation Grammar | N/A |

**Justification for manual-only:** All changes are markdown template edits. The project has no automated test infrastructure for markdown content validation (see REQUIREMENTS.md Out of Scope: "Automated agent testing framework" is explicitly excluded). Verification is structural inspection: does the field exist, does the format match the protocol, does the frontmatter parse.

### Sampling Rate

- **Per task commit:** Visual diff review of modified files
- **Per wave merge:** Cross-reference all three wiring points (template field, protocol format, test scenario expected output)
- **Phase gate:** Full cross-reference verification before `/gsd:verify-work`

### Wave 0 Gaps

None -- no test infrastructure needed for markdown template edits.

## Sources

### Primary (HIGH confidence)

- `templates/panel-assessment.md` (lines 105-116) -- current Escalation Note template section, verified by direct file read
- `SKILL.md` (lines 13-17, 72-169) -- current frontmatter invocation list and Invocation Grammar section, verified by direct file read
- `config/orchestration-protocol.md` (lines 82-108) -- Step 4 Tier 2 scoping note and Step 5 threshold assessment format, verified by direct file read
- `test-scenarios/tier2-partial-activation.md` (lines 96-127) -- Expected Output Excerpt showing the threshold enumeration format the Escalation Note should produce, verified by direct file read
- `commands/cdp/cleanup.md` (78 lines) -- cleanup command syntax and behavior, verified by direct file read
- `.planning/v1.1-MILESTONE-AUDIT.md` (lines 14-28, 112-118) -- INT-01 and INT-02 gap definitions with affected requirements and prescribed fixes

### Secondary (MEDIUM confidence)

None needed. All findings are from direct file reads of project files.

### Tertiary (LOW confidence)

None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no stack involved, pure markdown edits
- Architecture: HIGH - both target files read and analyzed, exact edit locations identified, upstream/downstream format cross-referenced
- Pitfalls: HIGH - all three pitfalls are format-consistency and placement issues identifiable from existing file structure

**Research date:** 2026-03-05
**Valid until:** Indefinitely -- markdown template structure is stable and changes only when the project's protocol evolves
