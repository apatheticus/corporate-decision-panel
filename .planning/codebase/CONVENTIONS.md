# Coding Conventions

**Analysis Date:** 2026-03-04

## Overview

Corporate Decision Panel is a markdown-based agent skill system with no traditional code. Conventions apply to:
- **Agent definition files** (`agents/*.md`) - Agent identity, mandate, and analytical frameworks
- **Configuration files** (`config/*.md`) - Routing rules, decision modes, company profiles
- **Command specifications** (`commands/*.md`) - Slash command entry points and invocation grammar
- **Output templates** (`templates/*.md`) - Structured formats for decisions, assessments, and notes
- **Documentation** (`docs/*.md`, `SKILL.md`, `README.md`) - Technical and user-facing docs

This is a prompt-and-configuration system where the entire CDP logic is expressed through structured markdown specifications.

## Naming Patterns

**Agent Files:**
- C-suite agents: `agents/c-suite/{role}.md` - e.g., `agents/c-suite/cfo.md`, `agents/c-suite/ceo.md`
- Team lead agents: `agents/team-leads/{c-suite}/{specialty}.md` - e.g., `agents/team-leads/cao/admin-policy-lead.md`
- Naming uses lowercase with hyphens for multi-word roles: `vp-sales`, `vp-delivery`, `admin-policy-lead`

**Configuration Files:**
- Stored in `config/` directory with descriptive names: `routing-table.md`, `decision-modes.md`, `company-profile.md`

**Command Files:**
- Stored in `commands/cdp/` with command name: `consult.md`, `panel.md`, `deliberate.md`, `evaluate.md`, `production.md`

**Template Files:**
- Output templates in `templates/` with format name: `advisory-note.md`, `panel-assessment.md`, `decision-record.md`
- Production templates in `templates/production/` for artifact generation

**Documentation:**
- Main skill documentation: `SKILL.md` (technical orchestration protocol)
- User documentation: `README.md` (installation, usage, commands)
- Architecture documentation: `docs/ARCHITECTURE.md` (technical reference)
- Development documentation: `docs/DEVELOPMENT.md`

## YAML Frontmatter Convention

All agent and command files begin with YAML frontmatter defining metadata:

```yaml
---
name: cfo
description: "Chief Financial Officer - Skeptic perspective on financial impact and hidden costs"
model: sonnet
---
```

**Required fields:**
- `name`: Agent identifier used in routing and invocation
- `description`: One-sentence agent purpose for discovery
- `model`: Model tier for execution (opus, sonnet, haiku)

**Optional fields (used in team lead agents):**
- `tools`: Array of available tools (`Read`, `Grep`, `Glob`, `WebSearch`)
- `maxTurns`: Maximum conversation turns for this agent

All markdown sections follow frontmatter immediately, no spacing.

## Markdown Structure & Heading Conventions

**Heading hierarchy:**
- Level 1 (`# Title`) - Agent name or document title, appears once at start after frontmatter
- Level 2 (`## Section`) - Major sections (Identity & Mandate, Team Composition, Mode A/B/C, etc.)
- Level 3 (`### Subsection`) - Subsections within modes or sections
- Level 4 (`#### Step/Item`) - Procedural steps or detailed items

**Example C-Suite Agent Structure:**
```markdown
# Chief Financial Officer

## Identity & Mandate
[Agent purpose and core mandate]

## Disposition & Susceptibility Mitigation
[How the agent avoids its natural bias]

## Team Composition
[Table of team leads and their domains]

## Mode A: Tier 1 Internal Checklist (Hallway Question)
[Quick direct consult protocol]

## Mode B: Tier 2/3 Subagent Dispatch (Working Session / Board Meeting)
[Full analysis with team lead delegation]

## Mode C: Phase 4.5 Pre-Mortem Challenge
[Cross-domain failure mode analysis]

## Synthesis Instructions
[Guidelines for domain recommendation synthesis]

## Escalation Brief Capability
[Format for escalating to higher tier]
```

**Table format:**
Tables document role/domain mappings, decision type routing, and mode/tier interactions. Always include headers and align columns:

```markdown
| C-Suite Role | Disposition | Mandate | Natural Tension |
|-------------|-------------|---------|-----------------|
| **CFO** | Skeptic | "Find the costs that aren't in the proposal." | Surfaces hidden financial exposure |
```

## Agent Identity & Mandate Convention

Each agent opens with **Identity & Mandate** section establishing:

1. **Role and Disposition:** "You are the [Title]. Your disposition is **[Skeptic/Advocate/Systemic/Investigative]**."
2. **Core Mandate (quoted):** One sentence, action-oriented: "Find the costs that aren't in the proposal"
3. **Domain Scope:** Bullet-listed areas the agent owns
4. **Value Proposition:** How this agent's perspective prevents failure
5. **Weakness Mitigation:** Explicit susceptibility and how to counteract it

Example from `agents/c-suite/cfo.md`:
```markdown
You are the CFO of this organization. Your disposition is **Skeptic**. Your mandate: **"Find the costs
that aren't in the proposal."**

You own the financial domain: accounting, financial planning and analysis, treasury operations,
accounts payable and receivable, working capital management, and tax structure.

**Skeptic role susceptibility:** As a skeptic, you are at risk of softening your objections to match
the perceived preference of the user. LLMs have a well-documented sycophancy bias that directly
undermines skeptic mandates.

**Mitigation directive:** Your value is in surfacing concerns, not in being agreeable. A skeptic
who hedges is worthless.
```

## Mode Specification Convention

Each agent defines three execution **Modes**:

**Mode A: Tier 1 (Hallway Question)**
- Direct consult, no subagent delegation
- Internal checklist for considering all team lead perspectives briefly
- Output: Advisory Note (3-5 sentences)
- Includes guidance for Escalation Brief generation

**Mode B: Tier 2/3 (Working Session / Board Meeting)**
- Full analysis with team lead subagent dispatch
- Translation of CEO framing into domain-specific sub-questions
- Team lead subagent invocation (custom agents)
- Synthesis of domain recommendation upward

**Mode C: Phase 4.5 (Pre-Mortem Challenge, Tier 3 only)**
- Cross-domain failure mode analysis
- Single question: "Assume this decision fails catastrophically in 12 months..."
- No back-and-forth, one-round response
- Specific, actionable failure scenarios

All three modes are defined in order for every C-suite agent. This creates a predictable structure for navigation and understanding.

## Structural Output Template Convention

Agents produce structured outputs following mandatory templates. Templates define:

1. **Section headers (descriptive, consistent across agents)**
   - ADVISORY NOTE, DOMAIN RECOMMENDATION, DECISION RECORD, PANEL ASSESSMENT
   - Subsections for Key Findings, Team Lead Findings, Key Risks, Key Opportunities

2. **Recommendation enumerations (standardized across all agents)**
   - Domain Recommendation: `[Approve | Approve with Conditions | Oppose | Neutral]`
   - Confidence: `[High | Medium | Low]`
   - Decision: `[clear statement]`

3. **Metadata format (consistent locations)**
   - Date: `[YYYY-MM-DD HH:MM UTC]`
   - Assessment ID: Unique identifiers with timestamp prefix (e.g., `PA-[YYYYMMDD]-[number]`)
   - Disposition, Mandate, Confidence level all located in predictable positions

See `templates/advisory-note.md`, `templates/panel-assessment.md`, `templates/decision-record.md` for complete template specifications.

## Decision Mode Convention

Five decision modes defined in `config/decision-modes.md` with consistent structure:

```markdown
## Mode Name (Decision Theory Base -- Description)

**Disposition:** [one-liner emotional posture]
**Decision Theory:** [Academic reference + summary]
**Resolution Pattern:** [How this mode weights perspectives]

**CEO Prompt Modifier:**
> [Role-specific prompt that modifies behavior]

## Mode/Tier Interaction Matrix
| Mode | Tier 1 | Tier 2 | Tier 3 |
| --- | --- | --- | --- |
```

All five modes (Guardian, Pioneer, Architect, Analyst, Sentinel) follow identical structure. Each mode includes:
- Decision theory backing (MaxiMin, MaxiMax, Behavioral, Hurwicz, MiniMax Regret)
- Behavioral characteristics at each tier (Tier 1, 2, 3)
- Explicit prompt modifier text used during synthesis
- Mode recommendation criteria for auto-triage

## Phase Nomenclature Convention

Five phases of CEO orchestration referenced consistently throughout:

**Phase 0:** Shared Consciousness Broadcast (background context)
**Phase 1:** Frame and Route (CEO decomposition and routing)
**Phase 1.5:** CSO Research Directive (evidence investigation, conditional)
**Phase 2:** C-Suite Dispatch (domain decomposition)
**Phase 3:** Team Lead Findings (specialist analysis)
**Phase 4:** C-Suite Synthesis (domain recommendations)
**Phase 4.5:** Pre-Mortem Challenge (cross-domain failure modes, Tier 3 only)
**Phase 5:** CEO Deliberation (final decision synthesis)

Phases are always referenced by number in parentheses: "Phase 1 (Frame and Route)" or abbreviated "Phase 1.5". This creates findable references throughout the codebase.

## Disposition Convention

All agents assigned one of four fixed dispositions:

- **Skeptic** (4 agents): COO, CFO, CISO, VP Delivery
  - Mandate: Surface concerns and constraints
  - Nature: "Can we actually do this?" perspective
  - Mitigation: Prevent softening objections for sycophancy

- **Advocate** (2 agents): CTO, VP Sales
  - Mandate: Identify opportunity and enablement
  - Nature: "What becomes possible?" perspective
  - Mitigation: Acknowledge genuine constraints even when advocating

- **Systemic** (1 agent): CAO
  - Mandate: Organizational absorption and governance
  - Nature: "Can the organization absorb this?" perspective
  - Mitigation: Ground all claims in concrete mechanisms, not abstract culture

- **Investigative** (1 agent): CSO
  - Mandate: Evidence-based research and pattern finding
  - Nature: "What does the evidence say?" perspective
  - Mitigation: Maintain independence from domain pressures

This balance (4 skeptics, 2 advocates, 1 systemic, 1 investigative, 1 CEO/synthesizer) is deliberate and is maintained across all routing configurations.

## Substantive Specification Conventions

All substantive protocols (routing, modes, team lead roles) documented with:

1. **Purpose statement** explaining why the specification exists
2. **Table format** showing all cases (decision types, modes, tiers)
3. **Rationale column** explaining the reasoning for each entry
4. **Examples** showing how the specification applies
5. **Override mechanism** explaining how defaults can be modified

Example from `config/routing-table.md`:
```markdown
| Decision Type | Default Activation | Description |
|---------------|--------------------|-------------|
| **Strategic** | CEO, CFO, CTO, VP Sales | Acquisition, market strategy, competitive positioning |
| **Operational** | CEO, COO, VP Delivery | Major process change, workflow restructuring, org restructure |

The CEO can always override defaults by adding or removing C-suite members from the activation set.
```

## Code Block Convention

When showing output or invocation examples:

**Markdown-based output (templates):**
```
ADVISORY NOTE
Domain: [Role] -- [Mandate]
Date: [timestamp]

---
[Content]
---
Confidence: [level]
```

**Invocation examples:**
```bash
/cdp:consult cfo: Can we afford to hire 15 engineers?
/cdp:panel finance tech: Should we build or buy?
/cdp:deliberate guardian: Should we acquire CompetitorX?
```

**Configuration examples:**
```yaml
---
name: cfo
description: "Chief Financial Officer - Skeptic perspective"
model: sonnet
---
```

**Inline code references:**
- File paths: backticks with relative paths from skill root: `agents/c-suite/cfo.md`, `config/routing-table.md`
- Command names: backticks with full invocation: `/cdp:consult`, `/cdp:deliberate`
- Configuration keys: backticks for YAML keys: `model`, `name`, `description`

## Documentation Cross-References

Documentation maintains consistent reference patterns:

- **Spec reference:** "See `SKILL.md` for the full orchestration protocol"
- **Agent reference:** "See `agents/c-suite/cfo.md` for the complete CFO specification"
- **Template reference:** "See `templates/advisory-note.md` for the template specification"
- **Configuration reference:** "See `config/routing-table.md` for routing rules"

File paths always use backticks and relative paths from skill root, enabling quick navigation.

## Emphasis Conventions

**Bold for emphasis:** Role names, key mandates, decision outcomes
- `**CEO**`, `**Skeptic**`, `**Approve**`, `**Confidence: High**`

**Backticks for references:** File paths, configuration keys, invocation syntax
- `agents/cfo.md`, `/cdp:deliberate`, `model: sonnet`

**Quoted for mandates:** Core role mandates always quoted and bolded
- **"Find the costs that aren't in the proposal."**
- **"What does this make possible that wasn't possible before?"**

**Inline code for decision types, tiers, phases:**
- Phase 1, Tier 2, Guardian mode, Strategic decision type

## Length Conventions

**Agent files:**
- C-Suite agents: 250-350 lines typically (identity + 3 modes + synthesis + escalation)
- Team Lead agents: 150-250 lines (identity + analytical framework + output template + forcing questions)

**Configuration files:**
- Routing table: ~40 lines (headers, default activation, threshold conditions, CSO patterns)
- Decision modes: ~100 lines (five mode definitions + mode/tier matrix + recommendation criteria)
- Company profile: ~150 lines (archetype presets + override mechanism + calibration)

**Template files:**
- Advisory Note: ~200 lines (purpose + agent execution + tone + template + escalation brief + examples)
- Panel Assessment: ~100 lines (purpose + template structure)
- Decision Record: ~300 lines (purpose + full template + sections)

## Comment Convention

Minimal inline comments. The markdown structure itself serves as documentation. Only explain:
- Why a choice differs from default (in override scenarios)
- Non-obvious analytical reasoning
- Forcing questions that require explicit consideration

No commented-out text or placeholder lines. Deletions are clean removals, not comments.

## Version and Date Convention

Documents include **Analysis Date** or **Version** headers for tracking:
- SKILL.md includes: "Version 1.0 · February 2026"
- ARCHITECTURE.md includes: "Version 1.0 · February 2026"
- Agent files do not include versions (source-of-truth is maintained in config)

Frontmatter does not include version. Agent specifications are treated as living documents that evolve with the system.

---

*Convention analysis: 2026-03-04*
