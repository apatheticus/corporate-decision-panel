# Architecture

**Analysis Date:** 2026-03-04

## Pattern Overview

**Overall:** Multi-agent hierarchical orchestration system with structured dissent

The Corporate Decision Panel is a prompt-and-configuration based reasoning engine that coordinates 43 agents across 3 analytical layers to simulate an SMB executive committee. It implements a strict hierarchy where agents at each layer (CEO, C-Suite, Team Leads) serve specific analytical purposes with engineered perspectives that deliberately counterbalance human optimism bias.

**Key Characteristics:**
- **Three-layer agent hierarchy** with role-based perspectives (skeptics, advocates, systemic, investigative)
- **Skeptic-heavy composition** (4 skeptics, 2 advocates, 1 systemic, 1 investigative, 1 synthesizer) to correct optimism bias
- **Phase-based cascade** that routes decisions through shared consciousness → framing → research (optional) → domain analysis → synthesis → pre-mortem (Tier 3 only) → CEO decision
- **Decision mode independence** where domain analysis runs once and CEO synthesis runs per mode
- **Fault-line preservation** where disagreement is maintained as signal rather than resolved into consensus

## Layers

**CEO Layer (Opus):**
- Purpose: Frame issues, route to appropriate C-suite members, synthesize cross-domain recommendations, produce final decision
- Location: `agents/ceo.md`
- Contains: Orchestration protocol for all five phases; routing logic; decision synthesis
- Depends on: Company context file (`.cdp-context/company.md`), routing table, decision mode definitions
- Used by: All slash commands that invoke deliberation workflows

**C-Suite Layer (Sonnet × 8):**
- Purpose: Domain decomposition and synthesis; translate CEO framing into domain-specific sub-questions; dispatch team leads; synthesize domain recommendations
- Location: `agents/c-suite/*.md` (coo, cfo, cto, ciso, cao, vp-sales, vp-delivery, cso)
- Contains: Each agent has identity, mandate, team lead delegation pattern, output template, escalation capability
- Depends on: Phase 0 broadcast from CEO; domain-specific sub-questions; team lead findings
- Used by: CEO during Phase 1 (receives routing), Phase 2 (dispatches downward), Phase 4 (synthesizes upward), Phase 4.5 (pre-mortem), Phase 5 (brief summary)

**Team Lead Layer (Haiku × 34):**
- Purpose: Narrow specialist analysis within a single domain using unique analytical frameworks
- Location: `agents/team-leads/{domain}/*.md` (organized by C-suite parent: coo, cfo, cto, ciso, cao, vp-sales, vp-delivery, cso)
- Contains: Each team lead has identity, analytical framework, output template, three forcing questions (pre-mortem, adversarial empathy, domain devil's advocate), blind spots list
- Depends on: Domain sub-questions from C-suite parent; Phase 0 shared consciousness broadcast
- Used by: C-suite parent during Phase 3 (receives findings) and Phase 4 (synthesizes into domain recommendation)

## Data Flow

**User Question → Five-Phase Cascade:**

1. **User invokes slash command** (`/cdp:consult`, `/cdp:panel`, `/cdp:deliberate`) with issue text, tier, mode(s), and role selection
2. **Tier 1 path** (`consult`): Direct C-suite agent consultation only. Agent reads internal checklist for relevant team lead perspectives, produces Advisory Note with optional Escalation Brief
3. **Tier 2-3 paths** (`panel`, `deliberate`): Full five-phase cascade
   - **Phase 0 -- Shared Consciousness Broadcast:** CEO reads optional `.cdp-context/company.md`, broadcasts issue context + company context + CEO framing + routing rationale + decision mode to all activated C-suite agents simultaneously
   - **Phase 1 -- CEO Frames & Routes:** CEO decomposes issue into evaluation dimensions, classifies decision type (Strategic/Operational/Financial/Technical/Personnel/Compliance-Risk), selects routing via `config/routing-table.md` defaults (with override capability), evaluates full-activation threshold conditions (irreversibility, headcount >30%, market position change, existential risk, domain uncertainty), optionally activates CSO for research
   - **Phase 1.5 -- Research Investigation (conditional):** If CSO activated: CSO dispatches 5 research team leads (Market Intelligence, Competitive Intelligence, Technology Scout, Industry/Regulatory, Precedent/Patterns), synthesizes Research Dossier with evidence quality grade and Assumption Registry, broadcasts to all C-suite
   - **Phase 2 -- C-Suite Dispatches Downward:** Each C-suite agent translates CEO framing into domain-specific sub-questions (analytical translation, not forwarding) and dispatches to team leads
   - **Phase 3 -- Team Leads Produce Findings:** Each team lead performs focused analysis using unique analytical framework and mandatory output template (parallel per domain)
   - **Phase 4 -- C-Suite Synthesizes Upward:** Each C-suite agent collects team lead findings and produces domain recommendation with confidence level, key risks, opportunities, flagged internal contradictions
   - **Phase 4.5 -- Pre-Mortem (Tier 3 only):** Each C-suite agent receives peer summaries and answers: "Assume failure in 12 months. What caused it?" One round only, no back-and-forth
   - **Phase 5 -- CEO Deliberation:** CEO maps domain recommendations to decision matrix, identifies fault lines, determines determinative perspective, applies decision mode, produces Decision Record (Tier 3) or Panel Assessment (Tier 2) or Advisory Note (Tier 1)
4. **Production pipeline triggered** (always for Tier 2-3; always for Tier 1): Tasks A-E executed as DAG with dependencies

**Two-tier visibility principle:** Team lead findings flow through C-suite parent only, not directly to CEO. Prevents cherry-picking and preserves domain-level synthesis.

**State Management:**
- **In-conversation:** Phase outputs accumulated in conversation context as agents execute sequentially
- **Persisted:** Decision Record (RECORD.md) saved to `.cdp-output/YYYY-MM-DD_<issue-slug>/RECORD.md` before production pipeline spawns, enabling `/cdp:production` re-runs without re-deliberation
- **Configuration:** Routing defaults in `config/routing-table.md`, decision mode definitions in `config/decision-modes.md`, company archetype presets in `config/company-profile.md`
- **Context:** Optional company data in `.cdp-context/company.md` (gitignored), loaded by CEO at session start, broadcast in Phase 0

## Key Abstractions

**Agent Definition (Markdown):**
- Purpose: Encodes agent identity, perspective type, analytical framework, output template, forcing questions
- Examples: `agents/ceo.md`, `agents/c-suite/cfo.md`, `agents/team-leads/cfo/controller.md`
- Pattern: YAML frontmatter (name, description, model, tools, maxTurns) + markdown sections (identity, mandate, analytical framework, output template, forcing questions, blind spots)

**Slash Command (Markdown):**
- Purpose: Entry point that parses user input and invokes orchestration protocol
- Examples: `commands/cdp/consult.md`, `commands/cdp/panel.md`, `commands/cdp/deliberate.md`, `commands/cdp/evaluate.md`, `commands/cdp/production.md`
- Pattern: YAML frontmatter (name, description, argument-hint) + brief execution instructions

**Decision Mode Modifier (Text prompt injection):**
- Purpose: Alters CEO's weighting disposition during Phase 5 without changing domain analysis
- Examples: Guardian (MaxiMin), Pioneer (MaxiMax), Architect (Behavioral), Analyst (Hurwicz), Sentinel (MiniMax Regret)
- Pattern: Modal text modifiers in CEO prompt defining how to resolve tensions between perspectives

**Engagement Tier (Protocol variant):**
- Purpose: Determines which phases execute and what output is produced
- Examples: Tier 1 (hallway question, direct consult), Tier 2 (working session, CEO + 2-4 C-suite), Tier 3 (board meeting, all relevant C-suite + pre-mortem)
- Pattern: Conditional logic in SKILL.md that routes to different agent team configurations and output templates

**Company Archetype Preset (YAML):**
- Purpose: Sets roster modifications, default decision mode, compliance focus, escalation behavior for industry types
- Examples: Technology/SaaS, Professional Services, Regulated Industry, Manufacturing/Physical
- Pattern: In `config/company-profile.md`; specifies conditional role activation (Facilities/Office Manager), default mode, compliance frameworks

## Entry Points

**Slash Commands:**
- Location: `commands/cdp/*.md`
- Triggers: User invokes `/cdp:consult`, `/cdp:panel`, `/cdp:deliberate`, `/cdp:evaluate`, `/cdp:production`
- Responsibilities: Parse arguments, invoke appropriate orchestration protocol (Tier 1-3 or production re-run), validate session directory for production re-runs

**SKILL.md (Auto-Setup):**
- Location: `SKILL.md`
- Triggers: First use in a project (if agents not already installed in `.claude/agents/`)
- Responsibilities: Copy agents to `.claude/agents/`, copy commands to `.claude/commands/cdp/`, create `.cdp-context/`, seed templates, update `.gitignore`

**install.py (Manual Setup):**
- Location: `install.py`
- Triggers: User runs `python3 install.py` in skill directory
- Responsibilities: Copy agents and commands, create `.cdp-context/`, seed templates, update `.gitignore`

## Error Handling

**Strategy:** Explicit, transparent, user-facing

**Patterns:**
- **Missing agent:** Auto-setup triggers; if setup fails, user sees error message with instructions
- **Missing company context:** Graceful fallback; system works without `.cdp-context/company.md`
- **Missing routing table entry:** CEO logs routing assumption; uses general heuristics
- **Invalid session path (production re-run):** Error message with available sessions
- **Team lead tool restrictions:** Team leads access only Read, Grep, Glob, WebSearch (no Write, Bash); agents error if attempting restricted tools
- **Team lead maxTurns exceeded:** Agent terminates with partial findings; C-suite notes incomplete analysis
- **Production artifact generation failure:** Placeholder artifact generated; source data (JSON prompt) saved for manual generation

## Cross-Cutting Concerns

**Logging:** None structured. Agents produce conversational output only. Decision Record persists to `.cdp-output/*/RECORD.md` for audit trail.

**Validation:**
- Issue slug derivation: lowercase, non-alphanumeric → hyphens, consecutive hyphens collapsed, 50 char trim, leading/trailing stripped
- Routing logic: CEO states both activation AND exclusion reasoning
- Confidence assessment: Each C-suite agent includes confidence level in domain recommendation
- Evidence grading: CSO includes evidence quality grade (High/Medium/Low) in Research Dossier

**Authentication:** Not applicable. System is Claude Code agent skill; inherits project authentication.

**Configuration Precedence:**
1. Per-session overrides (user-specified tier, mode, roles)
2. Company archetype preset (`.cdp-context/company.md` if filled; otherwise default to Technology/SaaS)
3. Routing table defaults (applies to decision type classification)
4. General framework (fallback for unprecedented situations)

---

*Architecture analysis: 2026-03-04*
