# Codebase Structure

**Analysis Date:** 2026-03-04

## Directory Layout

```
corporate-decision-panel/
├── SKILL.md                           # Skill definition + orchestration protocol + auto-setup
├── README.md                          # User documentation, quick start, command reference
├── CONTRIBUTING.md                    # Contribution guidelines
├── COLLABORATORS.md                   # Project contributors
├── install.py                         # Manual setup script
├── LICENSE                            # License
├── .gitignore                         # Git ignore patterns
├── agents/                            # Agent definitions (copied to .claude/agents/ on install)
│   ├── ceo.md                         # CEO agent (Opus) - orchestration & synthesis
│   ├── c-suite/                       # 8 C-suite agent definitions
│   │   ├── coo.md                     # Chief Operations Officer (Skeptic)
│   │   ├── cfo.md                     # Chief Financial Officer (Skeptic)
│   │   ├── cto.md                     # Chief Technology Officer (Advocate)
│   │   ├── ciso.md                    # Chief Information Security Officer (Skeptic)
│   │   ├── cao.md                     # Chief Administrative Officer (Systemic)
│   │   ├── vp-sales.md                # VP Sales (Advocate)
│   │   ├── vp-delivery.md             # VP Delivery (Skeptic)
│   │   └── cso.md                     # Chief Strategy Officer (Investigative)
│   └── team-leads/                    # 34 team lead definitions across 8 domains
│       ├── coo/                       # 4 team leads reporting to COO
│       │   ├── operations-manager.md
│       │   ├── process-quality-lead.md
│       │   ├── vendor-procurement-manager.md
│       │   └── facilities-office-manager.md
│       ├── cfo/                       # 5 team leads reporting to CFO
│       │   ├── controller.md
│       │   ├── head-fpa.md
│       │   ├── treasury-cash-manager.md
│       │   ├── ap-ar-manager.md
│       │   └── tax-lead.md
│       ├── cto/                       # 4 team leads reporting to CTO
│       │   ├── engineering-lead.md
│       │   ├── infrastructure-devops-lead.md
│       │   ├── data-analytics-lead.md
│       │   └── product-ux-lead.md
│       ├── ciso/                      # 4 team leads reporting to CISO
│       │   ├── security-ops-lead.md
│       │   ├── compliance-grc-lead.md
│       │   ├── identity-access-lead.md
│       │   └── security-architecture-lead.md
│       ├── cao/                       # 4 team leads reporting to CAO
│       │   ├── hr-people-ops-lead.md
│       │   ├── legal-contracts-lead.md
│       │   ├── admin-policy-lead.md
│       │   └── corporate-communications-lead.md
│       ├── vp-sales/                  # 4 team leads reporting to VP Sales
│       │   ├── sales-operations-lead.md
│       │   ├── account-management-lead.md
│       │   ├── business-development-lead.md
│       │   └── sales-enablement-lead.md
│       ├── vp-delivery/               # 4 team leads reporting to VP Delivery
│       │   ├── project-program-manager.md
│       │   ├── resource-manager.md
│       │   ├── client-success-lead.md
│       │   └── qa-delivery-standards-lead.md
│       └── cso/                       # 5 team leads reporting to CSO
│           ├── market-intelligence-lead.md
│           ├── competitive-intelligence-lead.md
│           ├── technology-scout-lead.md
│           ├── industry-regulatory-analyst.md
│           └── precedent-patterns-analyst.md
├── commands/                          # Slash commands (copied to .claude/commands/ on install)
│   └── cdp/
│       ├── consult.md                 # Tier 1 - Hallway Question
│       ├── panel.md                   # Tier 2 - Working Session
│       ├── deliberate.md              # Tier 3 - Board Meeting
│       ├── evaluate.md                # Auto-Triage
│       └── production.md              # Production Pipeline Re-run
├── config/                            # Configuration files
│   ├── routing-table.md               # Default C-suite activation by decision type + thresholds
│   ├── decision-modes.md              # Five decision mode definitions + CEO prompt modifiers
│   └── company-profile.md             # Company archetype presets (default: Technology/SaaS)
├── templates/                         # Output templates + production specs + context templates
│   ├── advisory-note.md               # Tier 1 output format (3-5 sentences + optional Escalation Brief)
│   ├── panel-assessment.md            # Tier 2 output format (~1 page)
│   ├── decision-record.md             # Tier 3 output format (3-5 pages, 9 sections)
│   ├── comparative-decision-record.md # Multi-mode comparison output format
│   ├── company-context.md             # Template for .cdp-context/company.md (gitignored user file)
│   ├── style-context.md               # Template for .cdp-context/style.md (gitignored user file)
│   ├── config-context.md              # Template for .cdp-context/config.md (gitignored user file)
│   ├── infographic-prompts/           # JSON prompt templates for Image Agent
│   │   ├── routing-diagram.json
│   │   ├── domain-scorecard.json
│   │   ├── fault-line-map.json
│   │   ├── risk-opportunity-matrix.json
│   │   ├── action-plan-timeline.json
│   │   └── mode-comparison.json
│   └── production/                    # Production artifact specifications
│       ├── infographics.md            # Image Agent spec + platform config + retry logic
│       ├── advisory-document.md       # Tier 1 DOCX memo format
│       ├── board-document.md          # Tier 2-3 DOCX specification
│       ├── board-presentation.md      # PPTX specification (11 slides)
│       ├── decision-briefing-page.md  # HTML briefing page specification
│       └── capsule-structure.md       # PDF archival capsule structure
├── docs/                              # Documentation (user-facing)
│   ├── ARCHITECTURE.md                # Technical architecture reference
│   ├── DEVELOPMENT.md                 # Development guide
│   └── README.md                      # Docs overview
├── ref/                               # Reference materials
│   └── ideation/                      # Design ideation notes
└── .planning/                         # GSD planning (created during analysis)
    └── codebase/                      # Codebase analysis documents (this output)
```

## Directory Purposes

**agents/:**
- Purpose: Agent definition files (markdown with YAML frontmatter)
- Contains: CEO + 8 C-suite + 34 team leads = 43 agent definitions
- Key files: `ceo.md` (orchestration hub), `c-suite/*.md` (domain leads), `team-leads/*/*.md` (specialists)
- Install behavior: Entire directory copied to `.claude/agents/` on setup, preserving structure

**agents/c-suite/:**
- Purpose: Eight domain executive agents running on Claude Sonnet
- Contains: Skeptics (COO, CFO, CISO, VP Delivery), Advocates (CTO, VP Sales), Systemic (CAO), Investigative (CSO)
- Each agent has: identity/mandate, team lead composition, Mode A (Tier 1 direct consult), Mode B (full analysis dispatch)

**agents/team-leads/{domain}/:**
- Purpose: 34 specialist analysts organized by C-suite parent domain
- Contains: Each team lead has analytical framework, output template, three forcing questions, blind spots
- Pattern: 4-5 team leads per C-suite parent; 14 of 34 have a fourth Cross-Domain Challenge question

**commands/cdp/:**
- Purpose: Slash command entry points
- Contains: Five commands (consult, panel, deliberate, evaluate, production) with argument parsing and protocol invocation
- Install behavior: Entire directory copied to `.claude/commands/` on setup

**config/:**
- Purpose: Configuration files (not gitignored; shipped with repo)
- Contains: routing-table.md (decision type → default C-suite activation), decision-modes.md (five mode definitions), company-profile.md (archetype presets)
- Mutability: Shipped defaults; can be customized per organization but typically not modified after initial setup

**templates/:**
- Purpose: Output formats, production specs, context templates
- Key files:
  - `advisory-note.md` - Tier 1 format (3-5 sentences)
  - `panel-assessment.md` - Tier 2 format (~1 page)
  - `decision-record.md` - Tier 3 format (3-5 pages, 9 sections)
  - `comparative-decision-record.md` - Multi-mode comparison format
  - `company-context.md` - Template copied to `.cdp-context/company.md` (gitignored)
  - `style-context.md` - Template copied to `.cdp-context/style.md` (gitignored)
  - `config-context.md` - Template copied to `.cdp-context/config.md` (gitignored)
- Install behavior: Only `*-context.md` templates are copied to `.cdp-context/` (user-created directory)

**templates/infographic-prompts/:**
- Purpose: JSON prompt templates for Image Agent (Pauhu schema hybrid)
- Contains: 6 infographic prompts (routing-diagram, domain-scorecard, fault-line-map, risk-opportunity-matrix, action-plan-timeline, mode-comparison)
- Pattern: Each JSON encodes image generation instructions for Gemini or ChatGPT

**templates/production/:**
- Purpose: Specifications for production artifact agents
- Contains: Image Agent, DOCX, PPTX, HTML, PDF specifications

**docs/:**
- Purpose: User-facing documentation
- Key files: ARCHITECTURE.md (technical reference), DEVELOPMENT.md (dev guide), README.md (docs index)

**ref/:**
- Purpose: Design ideation and reference materials
- Contains: Ideation notes, precedent research, decision theory references

## Key File Locations

**Entry Points:**
- `SKILL.md`: Primary orchestration protocol; auto-setup fallback logic
- `commands/cdp/consult.md`: Tier 1 entry point
- `commands/cdp/panel.md`: Tier 2 entry point
- `commands/cdp/deliberate.md`: Tier 3 entry point
- `commands/cdp/evaluate.md`: Auto-triage entry point
- `commands/cdp/production.md`: Production re-run entry point

**Configuration:**
- `config/routing-table.md`: Decision type → C-suite activation defaults
- `config/decision-modes.md`: Five decision mode definitions + CEO prompt modifiers
- `config/company-profile.md`: Company archetype presets
- `templates/company-context.md`: Template for `.cdp-context/company.md` (optional, gitignored)
- `templates/style-context.md`: Template for `.cdp-context/style.md` (optional, gitignored)
- `templates/config-context.md`: Template for `.cdp-context/config.md` (optional, gitignored)

**Core Logic:**
- `agents/ceo.md`: Five-phase cascade orchestration, routing logic, decision synthesis
- `agents/c-suite/cfo.md` (example): Domain mandate, team lead composition, Mode A (direct consult), Mode B (full analysis)
- `agents/team-leads/cfo/controller.md` (example): Analytical framework (GAAP Compliance & Financial Controls Assessment), output template, forcing questions

**Testing:**
- No unit tests. System is validated through end-to-end deliberation runs (Tier 1-3).
- Reference implementation: README.md and SKILL.md include example invocations.

**Output Formats:**
- `templates/advisory-note.md`: Tier 1 (3-5 sentences + optional Escalation Brief)
- `templates/panel-assessment.md`: Tier 2 (~1 page with domain recommendations and CEO synthesis)
- `templates/decision-record.md`: Tier 3 (3-5 pages, 9 sections: Executive Summary, Issue Statement, CEO Framing, Domain Analyses, Fault Lines, Decision, Dissenting Views, Next Steps, Metadata)
- `templates/comparative-decision-record.md`: Multi-mode (shared domain analysis + per-mode synthesis + divergence analysis + Mode Sensitivity)

## Naming Conventions

**Files:**
- Agent definitions: lowercase with hyphens (`cfo.md`, `controller.md`, `security-ops-lead.md`)
- Commands: slash-name without prefix (`consult.md`, `panel.md`, not `cdp-consult.md`)
- Config files: lowercase with hyphens (`routing-table.md`, `decision-modes.md`, `company-profile.md`)
- Templates: descriptive lowercase with hyphens (`advisory-note.md`, `decision-record.md`, `board-presentation.md`)
- JSON prompts: lowercase with hyphens (`routing-diagram.json`, `domain-scorecard.json`)

**Directories:**
- C-suite: lowercase role names (`coo/`, `cfo/`, `cto/`, etc.)
- Team leads: lowercase with hyphens, organized by C-suite parent (`agents/team-leads/cfo/`, `agents/team-leads/cso/`)
- Config, templates, commands: lowercase plural or descriptive (`config/`, `templates/`, `commands/`)
- JSON prompts: grouped in `infographic-prompts/` subdirectory within templates

**Agent Names (in frontmatter):**
- Single lowercase words or lowercase-with-hyphens (`ceo`, `cfo`, `controller`, `engineering-lead`)
- Model field: `opus` (CEO), `sonnet` (C-suite), `haiku` (team leads)

## Where to Add New Code

**New Team Lead:**
1. Create `.md` file in `agents/team-leads/{c-suite-parent}/`
2. Include YAML frontmatter: `name`, `description`, `model: haiku`, `tools: [Read, Grep, Glob, WebSearch]`, `maxTurns: 5`
3. Follow structure: Identity & Mandate → Analytical Framework → Output Template → Forcing Questions → Blind Spots
4. Optional: Add fourth Cross-Domain Challenge question (target high-interaction pairs)
5. Example template: `agents/team-leads/cfo/controller.md`
6. No registration needed; C-suite parent discovers via file structure

**New C-Suite Role:**
1. Create `.md` file in `agents/c-suite/`
2. Assign perspective type (skeptic, advocate, systemic, investigative) and verify 4-2-1-1-1 balance remains sound
3. Create corresponding `agents/team-leads/{role}/` subdirectory with 4-5 team leads
4. Update `config/routing-table.md` with default activation by decision type
5. Example: `agents/c-suite/cfo.md` + `agents/team-leads/cfo/`

**New Decision Mode:**
1. Define in `config/decision-modes.md` with decision theory foundation, disposition, resolution pattern, CEO prompt modifier
2. Add to mode/tier interaction matrix in same file
3. Run calibration protocol: run test issue through all five modes, verify ≥3 of 5 produce materially different outcomes
4. Example mode structure: Guardian (MaxiMin) in `config/decision-modes.md`

**New Company Archetype:**
1. Add preset to `config/company-profile.md`
2. Define roster modifications, default mode, compliance focus, escalation bias
3. Document when to use the new archetype
4. Example: "Technology/SaaS" (default), "Professional Services", "Regulated Industry", "Manufacturing/Physical"

**New Output Template:**
1. Create `.md` file in `templates/` with example output structure
2. Reference in SKILL.md (Orchestration Protocol section) for the relevant tier
3. If tier-specific: `advisory-note.md` (Tier 1), `panel-assessment.md` (Tier 2), `decision-record.md` (Tier 3)
4. Example: `templates/decision-record.md` has 9 sections with placeholder content

**New Production Artifact:**
1. Create spec `.md` file in `templates/production/`
2. Define the artifact type (DOCX, PPTX, HTML, PDF), technology (npm packages: docx, pptxgenjs; Python: weasyprint), and structure
3. Define task in production DAG and dependency relationships (Task A-C parallel, D blocks on A+B+C, E blocks on D)
4. Update SKILL.md Production Pipeline section with task definition
5. Example: `templates/production/board-presentation.md` defines 11-slide PPTX structure

**Modify Routing Rules:**
1. Edit `config/routing-table.md` to change default activation by decision type
2. Update full-activation threshold conditions if expanding or narrowing scope
3. Adjust CSO activation patterns if research investigation thresholds change
4. Example: Change Strategic default from "CEO, CFO, CTO, VP Sales" to include CISO for security-heavy decisions

## Special Directories

**`.claude/agents/` (generated on install):**
- Purpose: Agent definitions registered with Claude Code
- Generated: Yes, copied from `agents/` during install
- Committed: No (lives in project root `.claude/` directory, not in skill repo)
- Structure: Mirrors `agents/` directory structure from skill repo

**`.claude/commands/` (generated on install):**
- Purpose: Slash commands registered with Claude Code
- Generated: Yes, copied from `commands/` during install
- Committed: No (lives in project root `.claude/` directory, not in skill repo)
- Structure: Mirrors `commands/` directory structure from skill repo

**`.cdp-context/` (created on install):**
- Purpose: User-created context files (gitignored, sensitive business data)
- Generated: Yes, created by install.py; seeded with template files if not present
- Committed: No (gitignored by default)
- Contents:
  - `company.md` - Optional company facts (financials, headcount, tech stack, constraints)
  - `style.md` - Optional visual style preferences for Image Agent
  - `config.md` - Optional platform configuration (Gemini or ChatGPT) for Image Agent
- Mutability: User-created and user-modified; not overwritten on re-install

**`.cdp-output/` (generated at runtime):**
- Purpose: Session output directory (gitignored)
- Generated: Yes, per session at decision deliberation time
- Committed: No (gitignored by default)
- Structure: `YYYY-MM-DD_<issue-slug>/` containing RECORD.md, artifacts (HTML, PPTX, DOCX, PDFs), images/, build/
- Lifecycle: Persists after session; enables `/cdp:production` re-runs

**`docs/`:**
- Purpose: User-facing documentation
- Generated: No (maintained in repo)
- Committed: Yes (part of skill repo)
- Key files: ARCHITECTURE.md, DEVELOPMENT.md, README.md

---

*Structure analysis: 2026-03-04*
