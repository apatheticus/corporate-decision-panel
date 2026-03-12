# Phase 19: Documentation - Research

**Researched:** 2026-03-12
**Domain:** Documentation sweep -- update all user-facing docs to reflect CLO addition and CAO Legal/Contracts removal
**Confidence:** HIGH

## Summary

Phase 19 is a pure documentation update phase. All functional changes (agent files, config, routing, dispatch) were completed in Phases 16-18. This phase updates user-facing documentation to reflect the new 10 C-suite / 42 team lead roster, the CLO role, the removal of CAO Legal/Contracts Lead, and the updated engineered dissent balance (5 skeptics).

The primary complexity is not the nature of the changes (they are straightforward text/table/diagram edits) but the **breadth**: stale counts and missing CLO references are scattered across 12+ files spanning SKILL.md, README.md, docs/README.md, docs/ARCHITECTURE.md, docs/DEVELOPMENT.md, config/file-index.md, config/decision-modes.md, templates/decision-record.md, CONTRIBUTING.md, and test-scenario files. A systematic approach with verification is essential to avoid leaving stale numbers behind.

**Primary recommendation:** Organize work into two plans: (1) the three primary user-facing files (SKILL.md, README.md, docs/README.md), and (2) all remaining documentation files (ARCHITECTURE.md, DEVELOPMENT.md, file-index.md, decision-modes.md, templates, CONTRIBUTING.md, test-scenarios). Final verification uses filesystem counts as ground truth.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DOCS-01 | SKILL.md updated -- CLO in available roles, agent counts (10 C-suite, 42 team leads), engineered dissent description | Change inventory Section A covers all 10 SKILL.md edit points |
| DOCS-02 | README.md updated -- Available Roles, C-Suite Roster table, Team Lead Roster table, architecture diagrams, engineered dissent balance | Change inventory Sections B and C cover all README.md and docs/README.md edit points |
| DOCS-03 | All documentation agent/team lead counts verified against actual directory listing | Verified Counts section provides ground-truth numbers; verification commands documented |
</phase_requirements>

## Critical Finding: Count Discrepancy in Requirements

The ROADMAP.md and REQUIREMENTS.md state "38 team leads" as the target count. However, the actual filesystem count is **42 team leads**:

| Count Category | Pre-CLO | Post-CLO | Delta |
|----------------|---------|----------|-------|
| C-suite agents | 9 | 10 | +1 (CLO added) |
| Analytical team leads | 29 | 33 | +4 (5 CLO added, 1 CAO Legal/Contracts removed) |
| Research team leads (CSO) | 5 | 5 | 0 |
| Production team leads (CCO) | 4 | 4 | 0 |
| **Total team lead files** | **38** | **42** | **+4** |
| Total agents (all layers) | 48 (1+9+38) | 53 (1+10+42) | +5 |

The requirements' "38 team leads" is stale -- it was carried from the pre-CLO value without applying the net +4 change. The success criteria #3 ("verified by comparing stated numbers against `find agents/team-leads/ -name "*.md" | wc -l`") will produce 42, confirming 42 is the correct count.

**Ground truth commands:**
```bash
ls agents/c-suite/ | wc -l          # 10
find agents/team-leads/ -name "*.md" | wc -l  # 42
```

## Verified Counts (Ground Truth from Filesystem)

These are the correct numbers to use in all documentation:

| Metric | Value | Breakdown |
|--------|-------|-----------|
| C-suite agents (excl CEO) | 10 | COO, CFO, CTO, CLO, CISO, CAO, VP Sales, VP Delivery, CSO, CCO |
| C-suite analytical (excl CEO, CCO) | 9 | COO, CFO, CTO, CLO, CISO, CAO, VP Sales, VP Delivery, CSO |
| Total team lead files | 42 | 33 analytical + 5 research + 4 production |
| "Domain specialists" | 38 | 33 analytical + 5 research (the number used in SKILL.md narrative) |
| Team leads with cross-domain challenges | 18 | Was 14; -1 CAO Legal/Contracts, +5 CLO team leads |
| Agent invocations (full activation) | 43 | 1 CEO + 9 C-suite + 33 analytical team leads |
| Total agents in system | 53 | 1 CEO + 10 C-suite + 42 team leads |
| Skeptics | 5 | COO, CFO, CLO, CISO, VP Delivery |
| Advocates | 2 | CTO, VP Sales |
| Systemic | 1 | CAO |
| Investigative | 1 | CSO |
| Production | 1 | CCO |
| Synthesizer | 1 | CEO |
| Dissent balance | 5-2-1-1-1-1 | 5 skeptics + 2 advocates + 1 systemic + 1 investigative + 1 production + 1 synthesizer |
| CAO team leads | 3 | HR/People Ops, Admin/Policy, Corporate Communications |
| CLO team leads | 5 | Corporate Governance & Entity, Contracts & Commercial, Regulatory & Government Compliance, Employment & Labor Law, IP & Data Privacy |

**Context-dependent count conventions:**
- "34 domain specialists" (old SKILL.md) -> "38 domain specialists" (29->33 analytical + 5 research)
- "34 analytical + 4 production" (old repo structure) -> "38 + 4 production" = 42 total
- "C-Suite (8 agents)" in model tiering tables -> "C-Suite (9 agents)" (now 9 analytical C-suite excl CEO)
- "Sonnet x 9" -> "Sonnet x 10" (C-suite count including CCO)
- "Haiku x 34" -> "Haiku x 38" (domain specialist count excl production)
- "38 team lead agents" -> "42 team lead agents"
- "8 C-suite + 29 team leads = 38 agent invocations" -> "9 C-suite + 33 team leads = 43 agent invocations"
- "43 agents" total -> "53 agents" total
- "across 9 domains" -> "across 10 domains"
- "14 of 34" cross-domain -> "18 of 38" cross-domain

## Comprehensive Change Inventory

### Section A: SKILL.md (10 edit points)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~58-59 | `**Roles:** ceo, coo, cfo, cto, ciso, cao, vp-sales, vp-delivery, cso` | Add `clo` to list | Insert `clo` after `ciso` (alphabetical by role area) |
| ~340 | C-Suite Roster table: 9 rows, no CLO | Add CLO row: `CLO \| Skeptic \| "What is the legal exposure?"` | Between CFO and CTO (per Phase 17 decision: skeptics grouped) |
| ~354 | `4 skeptics + 2 advocates + 1 systemic + 1 investigative + 1 production + 1 synthesizer` | `5 skeptics + 2 advocates + ...` | CLO is Skeptic |
| ~355-356 | `Skeptic-heavy to counterbalance human optimism bias.` | Update skeptic count ratio description | |
| ~361 | `34 domain specialists` | `38 domain specialists` | 33 analytical + 5 research |
| ~362 | `29 analytical team leads (Phase 2-4) and 5 research` | `33 analytical team leads (Phase 2-4) and 5 research` | |
| ~370-378 | Team Lead table: 8 rows, no CLO | Add CLO row with 5 team leads, remove Legal/Contracts from CAO row | CAO count changes from 4 to 3 |
| ~379 | `14 of 34 team leads have a fourth forcing question` | `18 of 38 team leads have a fourth forcing question` | |
| ~448-453 | Routing table: no CLO in any row | Add CLO to Strategic, Personnel, Compliance/Risk | Match config/routing-table.md |
| ~5 (version?) | version: 1.8 | version: 1.9 | Update frontmatter version |

### Section B: README.md (18 edit points)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~17 | `Version 1.7` | `Version 1.9` | Header version |
| ~211 | `4 Skeptics (COO, CFO, CISO, VP Delivery)` | `5 Skeptics (COO, CFO, CLO, CISO, VP Delivery)` | Engineered dissent section |
| ~738 | Available Roles: no `clo` | Add `clo` to the inline code list | |
| ~744-751 | Domain shorthands table: no `legal` shorthand | Add `legal` -> `CLO` -> `Governance, contracts, regulatory, employment, IP/privacy` | |
| ~940 | C-Suite Sonnet 9 | C-Suite Sonnet 10 | Model tiering table |
| ~941 | Team Leads Haiku 34 | Team Leads Haiku 38 | Model tiering table |
| ~946-988 | Agent hierarchy mermaid diagram: 8 C-suite nodes, no CLO | Add CLO node + CLO_TL team lead box | Red/skeptic style |
| ~965 | CAO_TL: `HR/People Ops\nLegal/Contracts\nAdmin/Policy\nCorporate Comms` | Remove `Legal/Contracts`, now 3 items | |
| ~1010-1023 | C-Suite Roster table: 9 rows, no CLO | Add CLO row | Between CFO and CTO |
| ~1024 | `4 Skeptics + 2 Advocates + 1 Systemic + 1 Investigative + 1 Synthesizer` | `5 Skeptics + ...` | |
| ~1030-1040 | Team Lead Roster table: no CLO, CAO has 4 with Legal/Contracts | Add CLO row (5), fix CAO row (3, no Legal/Contracts) | |
| ~1040 | Total: 34 | Total: 38 | (domain specialist count) |
| ~1044 | `14 of 34 team leads` | `18 of 38 team leads` | Cross-domain challenge note |
| ~1283 | `CISO and CAO Legal are always activated` | Update to reference CLO instead of CAO Legal | Regulated Industry archetype |
| ~1303 | Archetype table: `CISO + CAO Legal always active` | Update to `CISO + CLO always active` | |
| ~1794 | `9 C-suite agents (8 analytical + CCO)` | `10 C-suite agents (9 analytical + CCO)` | Repo structure tree |
| ~1804 | `38 team lead agents (34 analytical + 4 production)` | `42 team lead agents (38 domain + 4 production)` | Repo structure tree |
| ~1805-1813 | No `clo/` directory entry, `cao/` says 4 leads | Add `clo/` entry (5 leads), fix `cao/` (3 leads) | |
| ~1885 | `4 skeptics, 2 advocates, 1 systemic, 1 investigative` | `5 skeptics, ...` | Design Principles |

### Section C: docs/README.md (14 edit points)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~58-59 | Roles: no `clo` | Add `clo` | |
| ~262 | Available Roles list: no `clo` | Add `clo` | |
| ~335-378 | Agent hierarchy mermaid: no CLO node | Add CLO node + team lead box | Match README.md diagram |
| ~355 | CAO_TL: `HR/People Ops\nLegal/Contracts\nAdmin/Policy\nCorporate Comms` | Remove `Legal/Contracts` | |
| ~387-388 | C-Suite (8 agents) Sonnet, Team Leads (34) Haiku | Update counts: 9, 38 | |
| ~392-400 | Engineered dissent: 4 Skeptics | 5 Skeptics, add CLO | |
| ~406-417 | C-Suite Roster table: no CLO | Add CLO row | |
| ~420 | `14 of 34 have a fourth Cross-Domain Challenge` | `18 of 38` | |
| ~422-432 | Team Lead Roster table: no CLO, CAO has Legal/Contracts, total 34 | Add CLO (5), fix CAO (3), total 38 | |
| ~648-653 | Routing table: no CLO | Add CLO to Strategic, Personnel, Compliance/Risk | |
| ~508 | Archetype table: `CISO + CAO Legal always active` | Update | |
| ~800 | `9 agents, including CCO` | `10 agents, including CCO` | Repo structure |
| ~802 | `38 agents across 9 domains: 34 analytical + 4 production` | `42 agents across 10 domains: 38 domain + 4 production` | |
| ~858 | `4 skeptics, 2 advocates, 1 systemic, 1 investigative` | `5 skeptics, ...` | Design principles |

### Section D: docs/ARCHITECTURE.md (11 edit points)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~9 | `Version 1.8` | `Version 1.9` | |
| ~35 | `43 agents with engineered dissent` | `53 agents` | |
| ~55 | `C-Suite Agents\n(Sonnet x 9)` | `(Sonnet x 10)` | System diagram mermaid |
| ~56 | `Team Lead Agents\n(Haiku x 34)` | `(Haiku x 38)` | System diagram mermaid |
| ~90-104 | Layer 2 heading `Sonnet x 9`, roster table: no CLO | `Sonnet x 10`, add CLO row | |
| ~106 | `Layer 3: Team Leads (Haiku x 34)` | `Haiku x 38` | |
| ~117-118 | Model tiering table: C-Suite 9, Team Leads 34 | 10, 38 | |
| ~120 | `all 43 agents` | `all 53 agents` | |
| ~128-137 | Engineered dissent table: Skeptic 4 = COO, CFO, CISO, VP Delivery | Skeptic 5 = +CLO | |
| ~138 | `4-2-1-1-1 composition` | `5-2-1-1-1-1 composition` | |
| ~493 | `14 of 34 team leads` | `18 of 38 team leads` | |
| ~516+ | Extension Points section on adding C-suite roles | May need update to reference CLO as recent example | |
| ~550 | `4 skeptics, 2 advocates, 1 systemic, 1 investigative` | `5 skeptics, ...` | Design principles |

### Section E: docs/DEVELOPMENT.md (3 edit points)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~9 | `Version 1.7` | `Version 1.9` | |
| ~69 | `C-suite executives (Sonnet x 9)` | `(Sonnet x 10)` | Repo structure |
| ~79 | `Specialist agents (Haiku x 38, 34 analytical + 4 production)` | `Haiku x 42, 38 domain + 4 production` | |
| ~352 | `4-2-1-1-1 composition (4 skeptics, ...)` | `5-2-1-1-1-1 composition (5 skeptics, ...)` | |

### Section F: config/file-index.md (2 edit points)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~58 | `9 C-suite agent definitions (COO, CFO, CTO, CISO, CAO, VP Sales, VP Delivery, CSO, CCO)` | Add CLO to list, count 10 | |
| ~59 | `38 team lead agent definitions across 9 domains (29 analytical + 5 research + 4 production)` | `42 team lead agent definitions across 10 domains (33 analytical + 5 research + 4 production)` | |

### Section G: config/decision-modes.md (4 edit points)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~189 | `8 C-suite + 29 team leads = 38 agent invocations` | `9 C-suite + 33 team leads = 43 agent invocations` | Example 1 |
| ~191 | `Total: 40 invocations vs. 39` | Update math | |
| ~194 | `8 C-suite + 29 team leads = 38 agent invocations` | `9 C-suite + 33 team leads = 43` | Example 2 |
| ~196 | `Total: 43 invocations vs. 39 for single-mode = 1.10x cost` | Update math: 48 vs 44 | |

### Section H: templates/decision-record.md (1 edit point)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~262 | `N of 8 C-suite + N of 34 team leads activated` | `N of 9 C-suite + N of 38 team leads activated` | Metadata template |

### Section I: CONTRIBUTING.md (1 edit point)

| Line | Current | Updated | Notes |
|------|---------|---------|-------|
| ~42 | `4 Skeptic -- CFO, CISO, COO, VP Delivery` | `5 Skeptic -- CFO, CLO, CISO, COO, VP Delivery` | |

### Section J: test-scenarios (possible edit points -- scope judgment needed)

| File | Current | Updated | Notes |
|------|---------|---------|-------|
| premortem-degraded-input.md ~62 | `full C-suite activation (8 agents)` | `(9 agents)` | Analytical C-suite count |
| tier2-partial-activation.md ~86 | `All 8 C-suite agents activate` | `All 9 C-suite agents` | |

## Architecture Patterns

### Pattern: Systematic Count Verification

After all edits, verify every count by cross-referencing documentation against filesystem:

```bash
# Ground truth
echo "C-suite: $(ls agents/c-suite/ | wc -l)"           # Expect: 10
echo "Team leads: $(find agents/team-leads/ -name '*.md' | wc -l)"  # Expect: 42
echo "Cross-domain: $(grep -rl 'CROSS-DOMAIN CHALLENGE\|Cross-Domain Challenge' agents/team-leads/ | wc -l)"  # Expect: 18

# Verify no stale counts remain
grep -rn '\b34 domain\|34 team\|34 agent\|34 specialist\b' SKILL.md README.md docs/ config/file-index.md
grep -rn '\b38 team lead agent\b' SKILL.md README.md docs/ config/file-index.md
grep -rn 'Sonnet.*9\|9 C-suite\|8 C-suite\|C-Suite.*8\b' SKILL.md README.md docs/ config/
grep -rn 'Haiku.*34\|34 agent\b' SKILL.md README.md docs/ config/
grep -rn '14 of 34\|14 of 38' SKILL.md README.md docs/
grep -rn '43 agent' docs/ config/
grep -rn 'Legal/Contracts' SKILL.md README.md docs/README.md
grep -rn '4 skeptic\b' SKILL.md README.md docs/ config/ CONTRIBUTING.md
```

### Pattern: CLO Placement Convention

Per Phase 17 decision: CLO is placed between CFO and CTO in roster tables to keep skeptics grouped.

In mermaid diagrams, add CLO as a red/skeptic-styled node with its own team lead box.

In inline role lists: insert `clo` alphabetically or by domain convention.

### Anti-Patterns to Avoid

- **Partial update:** Updating the table but not the accompanying text count. Every count appears in at least 2 forms (table + narrative).
- **Counting convention mismatch:** Different files use different counting conventions (34 = domain specialists, 38 = all team leads including production). Maintain each file's existing convention while updating the number.
- **Missing Legal/Contracts cleanup:** Some docs still reference "CAO Legal" or "Legal/Contracts" in contexts that weren't caught by Phase 18's codebase sweep (documentation was explicitly deferred to Phase 19).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Count verification | Manual inspection of every file | grep-based verification script | 12+ files with 5+ count variations; manual inspection will miss something |

## Common Pitfalls

### Pitfall 1: Counting Convention Confusion
**What goes wrong:** The codebase uses at least 4 different count groupings: "domain specialists" (analytical+research), "team lead agents" (all including production), "analytical team leads" (phase 2-4 only), and "agent invocations" (CEO+C-suite+analytical).
**Why it happens:** Different contexts need different numbers.
**How to avoid:** Use the Verified Counts table in this research as the single source of truth. Match each edit to the correct count category for that context.
**Warning signs:** Any count that doesn't appear in the Verified Counts table.

### Pitfall 2: Stale "CAO Legal" References in Prose
**What goes wrong:** Documentation text like "CISO + CAO Legal always active" in company profile descriptions wasn't part of Phase 18's codebase sweep (which focused on agent/config files).
**Why it happens:** Phase 18 swept functional files; documentation was explicitly deferred.
**How to avoid:** Search for "CAO Legal", "Legal/Contracts" across all doc files.

### Pitfall 3: Mermaid Diagram Syntax Errors
**What goes wrong:** Adding a CLO node to existing mermaid flowcharts can break if the connection syntax, style declarations, or subgraph structure is wrong.
**Why it happens:** Mermaid diagrams are sensitive to indentation and connection syntax.
**How to avoid:** Follow the exact pattern of existing nodes (copy CFO node pattern since CLO is also a Skeptic).

### Pitfall 4: Decision Mode Math Errors
**What goes wrong:** The worked examples in decision-modes.md have specific agent invocation math (e.g., "40 vs 39 = 1.03x cost"). Updating the base numbers without re-computing ratios produces wrong math.
**Why it happens:** Multiple dependent numbers in a single paragraph.
**How to avoid:** Re-derive all computed values from the new base counts.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Manual verification (no automated test framework for documentation) |
| Config file | N/A |
| Quick run command | `grep -rn` verification commands |
| Full suite command | Filesystem count comparison |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DOCS-01 | SKILL.md has correct CLO info and counts | manual+grep | `grep -c 'clo' SKILL.md && grep '38 domain' SKILL.md` | N/A |
| DOCS-02 | README.md has CLO in all required sections | manual+grep | `grep -c 'CLO\|clo' README.md docs/README.md` | N/A |
| DOCS-03 | All doc counts match filesystem | smoke | `ls agents/c-suite/ \| wc -l` + `find agents/team-leads/ -name "*.md" \| wc -l` | N/A |

### Sampling Rate
- **Per task commit:** Run grep verification commands
- **Per wave merge:** Full count verification against filesystem
- **Phase gate:** All stale-count grep patterns return zero results

### Wave 0 Gaps
None -- this phase requires no test infrastructure. Verification is grep-based.

## Sources

### Primary (HIGH confidence)
- Filesystem listing of agents/c-suite/ and agents/team-leads/ -- verified counts
- Current file contents of SKILL.md, README.md, docs/README.md, docs/ARCHITECTURE.md, docs/DEVELOPMENT.md -- identified all stale references
- config/routing-table.md and config/decision-modes.md -- verified CLO already integrated in Phases 17-18
- agents/ceo.md -- verified CLO already in dispatch lists from Phase 18

### Secondary (MEDIUM confidence)
- REQUIREMENTS.md "38 team leads" -- identified as stale (pre-CLO number); filesystem is ground truth

## Metadata

**Confidence breakdown:**
- Change inventory: HIGH -- every stale reference identified via grep across full codebase
- Count correctness: HIGH -- derived from filesystem listing, cross-verified
- Pitfalls: HIGH -- based on direct analysis of file contents and counting conventions

**Research date:** 2026-03-12
**Valid until:** 2026-04-12 (stable -- no external dependencies)
