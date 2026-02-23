---
name: corporate-decision-panel
description: >
  A complete organizational reasoning engine that emulates SMB executive
  committee decision-making. Presents any business issue through a structured
  cascade: CEO frames and routes, C-suite executives analyze through domain
  lenses with engineered dissent, team leads produce specialist findings,
  and the CEO synthesizes a decision that addresses the strongest objections.
  Operates at three engagement tiers (hallway question, working session,
  board meeting) and five synthesis modes (Guardian, Pioneer, Architect,
  Analyst, Sentinel).
invocation:
  - /cdp:consult
  - /cdp:panel
  - /cdp:deliberate
  - /cdp:evaluate
---

# Corporate Decision Panel

A boardroom in a box. Present any business issue and receive structured,
multi-perspective analysis with engineered dissent -- not consensus from a
single voice, but a decision that shows where expert perspectives collide
and why.

---

## Setup Check

Before executing any command, verify that CDP agent definitions and slash
commands are installed in the project's `.claude/` directory.

**Check:** Does `.claude/agents/ceo.md` exist in the project root?

**If NO (first run):**
1. Copy all files from this skill's `agents/` directory to `.claude/agents/`,
   preserving the directory structure (`c-suite/`, `team-leads/`)
2. Copy all files from this skill's `commands/` directory to `.claude/commands/`,
   preserving the directory structure (`cdp/`)
3. Append these entries to the project root `.gitignore` if not already present:
   - `.cdp-output/`
   - `.cdp-context/`
4. Create `.cdp-context/` directory if it doesn't exist
5. Print setup confirmation:
   ```
   CDP installed successfully.
   - Agent definitions copied to .claude/agents/
   - Slash commands copied to .claude/commands/cdp/

   Quick start:
     /cdp:consult cfo: Can we afford to hire this quarter?
     /cdp:panel finance tech: Should we build or buy?
     /cdp:deliberate: Should we pivot to a platform model?
     /cdp:evaluate: Should we acquire CompetitorX?
   ```
6. If the user provided a command with this invocation, proceed to execute it

**If YES:** Proceed directly to command execution.

---

## Invocation Grammar

### Tier 1 -- Hallway Question
```
/cdp:consult [role] [mode?]: [question]
```
Quick, opinionated consult with one C-suite agent. No CEO, no routing,
no team leads. Produces an **Advisory Note** (3-5 sentences).

- `/cdp:consult cfo: Can we afford to hire 15 engineers this quarter?`
- `/cdp:consult ciso guardian: What are the risks of this vendor integration?`
- `/cdp:consult vp-sales pioneer: How does this feature help us sell more?`

**Roles:** `ceo`, `coo`, `cfo`, `cto`, `ciso`, `cao`, `vp-sales`,
`vp-delivery`, `cso`

### Tier 2 -- Working Session
```
/cdp:panel [roles] [mode?]: [issue]
```
CEO frames and routes to 2-4 C-suite members. Full domain analysis with
team lead delegation. CEO produces lightweight synthesis. Produces a
**Panel Assessment** (~1 page).

- `/cdp:panel finance tech: Should we build this feature in-house?`
- `/cdp:panel pioneer finance tech sales: Should we acquire CompetitorX?`
- `/cdp:panel --produce operations delivery: Should we restructure the PMO?`

The `--produce` flag triggers the production pipeline (HTML, PPTX, DOCX,
Results PDF, Capsule PDF). Without it, only the Panel Assessment text
is produced.

### Tier 3 -- Board Meeting
```
/cdp:deliberate [mode?]: [issue]
```
Full five-phase cascade. All relevant C-suite activated via routing table.
Full team lead analysis. Pre-mortem challenge. Complete CEO deliberation.
Produces a **Decision Record** (3-5 pages). Production always triggered.

- `/cdp:deliberate: Should we pivot to a platform model?`
- `/cdp:deliberate guardian: Should we take on $10M in debt for expansion?`
- `/cdp:deliberate sentinel: Should we acquire CompetitorX?`

### Auto-Triage
```
/cdp:evaluate: [issue]
```
CEO assesses the issue and recommends a tier, mode, and routing. The user
accepts, overrides, or selects a different configuration.

**CEO evaluates:** scope (single/multi/cross-cutting), impact (low through
critical), reversibility (easily reversed through irreversible).

**Output:**
```
ISSUE TRIAGE: [Issue Title]
Scope: [single-domain | multi-domain | cross-cutting]
Impact: [low | medium | high | critical]
Reversibility: [easily reversed | difficult | irreversible]
Recommended Tier: [tier] -- [rationale]
Recommended Mode: [mode] -- [rationale]
Alternative: [mode] -- [what it would reveal]
```

### Multi-Mode Syntax
Domain analysis runs once. CEO synthesis runs per mode. Cost: ~1.1x for
up to 5x the strategic insight.

```
/cdp:deliberate guardian vs pioneer: [issue]       # Two-mode comparison
/cdp:deliberate guardian vs analyst vs sentinel: [issue]  # Three modes
/cdp:deliberate all-modes: [issue]                 # All five modes
/cdp:consult cfo guardian: [question]              # Tier 1 with mode
/cdp:panel pioneer finance tech: [issue]           # Tier 2 with mode
```

Multi-mode produces a **Comparative Decision Record** with shared analysis,
per-mode synthesis, divergence analysis, and Mode Sensitivity rating.

---

## Decision Modes

Five CEO synthesis prompt modifiers. Domain analysis is identical across
modes -- different weighting produces different decisions from the same
inputs. See `config/decision-modes.md` for full specifications.

| Mode | Disposition | Resolves Tensions By |
|------|-----------|---------------------|
| **Guardian** | Risk-averse (MaxiMin) | Weights skeptics. High bar for approval. |
| **Pioneer** | Growth-oriented (MaxiMax) | Weights advocates. Objections are problems to solve. |
| **Architect** | Consensus-building (Behavioral) | Seeks widest organizational support. |
| **Analyst** | Data-driven (Hurwicz) -- **default** | Weights by confidence level. Defer is legitimate. |
| **Sentinel** | Regret-minimizing (MiniMax Regret) | Weights strongest single objection. Survivable paths. |

---

## Orchestration Protocol

### Tier 1: Hallway Question

1. User invokes `/cdp:consult [role] [mode?]: [question]`
2. Spawn the specified C-suite agent as Agent Team teammate (Sonnet)
3. Agent runs **Mode A** (direct consult):
   - Runs internal checklist (considers each team lead perspective)
   - Produces Advisory Note (3-5 sentences)
   - If cross-domain implications detected: appends Escalation Brief
4. Return Advisory Note to user
5. **No CEO. No team leads. No production.**

Output template: `templates/advisory-note.md`

### Tier 2: Working Session

1. User invokes `/cdp:panel [roles] [mode?]: [issue]`
2. Create Agent Team. Spawn CEO (Opus)
3. CEO runs **Phase 1** (frame and route):
   - Decomposes issue into evaluation dimensions
   - Classifies decision type
   - Routes to user-specified roles (or auto-routes)
4. Spawn activated C-suite agents as teammates (Sonnet)
5. Each C-suite agent runs **Mode B** (full analysis):
   - Translates CEO framing into domain sub-questions
   - Dispatches team lead subagents (Haiku) -- **parallel per domain**
   - Collects team lead findings
   - Synthesizes domain recommendation with confidence level
6. CEO runs **Phase 5** (abbreviated synthesis):
   - Collects domain recommendations
   - Applies Decision Mode
   - Produces Panel Assessment
7. If `--produce` flag: trigger production pipeline
8. Return Panel Assessment to user

Output template: `templates/panel-assessment.md`

### Tier 3: Board Meeting

Full five-phase cascade with optional Phase 1.5 (CSO research) and
Phase 4.5 (pre-mortem challenge).

**Phase 0 -- Shared Consciousness Broadcast**
CEO broadcasts issue context to all activated C-suite agents. Everyone
sees the same picture before reasoning independently.

**Phase 1 -- CEO Frames and Routes**
CEO decomposes the issue, classifies decision type, selects routing via
`config/routing-table.md` defaults (with override capability). States
activation AND exclusion reasoning. Evaluates full-activation threshold
conditions. Issues CSO research directive if applicable.

**Phase 1.5 -- Research Investigation** (conditional)
If CEO activates CSO: CSO decomposes research directive into sub-questions,
dispatches 5 research team leads (Market Intelligence, Competitive
Intelligence, Technology Scout, Industry & Regulatory Analyst, Precedent
& Patterns Analyst). CSO synthesizes findings into Research Dossier with
evidence quality grade and Assumption Registry. Dossier broadcast to all
activated C-suite. **Skipped if CSO not activated.**

**Phase 2 -- C-Suite Dispatches Downward**
Each activated C-suite agent translates CEO framing into domain-specific
sub-questions, one per team lead. This translation is analytical -- the
CFO does not forward the question; the CFO asks the Controller "what are
the GAAP implications?"

**Phase 3 -- Team Leads Produce Findings**
Each team lead subagent performs narrow, focused analysis through their
specialist lens using their unique analytical framework and mandatory
output template. Different methods produce structurally different outputs.

**Phase 4 -- C-Suite Synthesizes Upward**
Each C-suite agent collects team lead findings and synthesizes a domain
recommendation with confidence level, key risks, and key opportunities.
Internal contradictions between team leads flagged as analytical signals.

**Phase 4.5 -- Pre-Mortem Challenge** (Tier 3 only)
After producing their own recommendation, each C-suite agent receives
summaries of ALL other C-suite recommendations and answers: "Assume this
decision fails catastrophically in 12 months. What caused the failure?"
One round only. No back-and-forth.

**Phase 5 -- CEO Deliberation**
CEO maps all domain recommendations onto a decision matrix, identifies
fault lines, determines most determinative perspective, applies Decision
Mode, produces the Decision Record.

**Production automatically triggered after Phase 5.**

Output template: `templates/decision-record.md`
Comparative output: `templates/comparative-decision-record.md`

---

## Agent Architecture

### Tier 1 Agents: Agent Team Teammates (Sonnet)

| Role | Disposition | Mandate |
|------|-----------|---------|
| CEO | Synthesizer | Frame, listen, weigh, decide. Value is judgment. |
| COO | Skeptic | "Can we do this with what we have?" |
| CFO | Skeptic | "Find the costs not in the proposal." |
| CTO | Advocate | "What does this make possible?" |
| CISO | Skeptic | "Change introduces risk. You are the immune system." |
| VP Sales | Advocate | "How does this help us sell more?" |
| VP Delivery | Skeptic | "What do we sacrifice from commitments?" |
| CAO | Systemic | "Can the org absorb this?" |
| CSO | Investigative | "What does the evidence say?" |

**Engineered Dissent Balance:** 4 skeptics + 2 advocates + 1 systemic +
1 investigative + 1 synthesizer. Skeptic-heavy to counterbalance human
optimism bias.

### Tier 2 Agents: Team Lead Subagents (Haiku)

34 specialist analysts dispatched by their C-suite parent. Each has a
unique analytical framework, mandatory output template, three forcing
questions (Pre-Mortem, Adversarial Empathy, Domain Devil's Advocate),
and restricted tool access (Read, Grep, Glob, WebSearch only).

| C-Suite | Team Leads (4-5 each) |
|---------|----------------------|
| COO | Operations Mgr, Process/Quality, Vendor/Procurement, Facilities (conditional) |
| CFO | Controller, Head of FP&A, Treasury/Cash, AP/AR Mgr, Tax Lead |
| CTO | Engineering, Infrastructure/DevOps, Data/Analytics, Product/UX |
| CISO | Security Ops, Compliance/GRC, Identity & Access, Security Architecture |
| VP Sales | Sales Ops, Account Mgmt, Business Development, Sales Enablement |
| VP Delivery | Project/Program Mgr, Resource Mgr, Client Success, QA/Delivery Standards |
| CAO | HR/People Ops, Legal/Contracts, Admin/Policy, Corporate Communications |
| CSO | Market Intel, Competitive Intel, Technology Scout, Industry/Regulatory, Precedent/Patterns |

14 of 34 team leads have a fourth forcing question (Cross-Domain Challenge)
targeting high-interaction pairs where cross-domain assumptions create
blind spots.

### Model Tiering

| Layer | Model | Rationale |
|-------|-------|-----------|
| Team Lead Subagents | Haiku | Narrow analysis. Cost-efficient. Model diversity. |
| C-Suite Agents | Sonnet | Domain decomposition and synthesis. |
| CEO | Opus | Cross-domain synthesis. Highest reasoning quality. |

---

## Production Pipeline

### Trigger Logic

| Tier | Production | Notes |
|------|-----------|-------|
| Tier 1 | Never | Advisory Notes are lightweight by design |
| Tier 2 | `--produce` flag | Optional: `/cdp:panel --produce ...` |
| Tier 3 | Always | Automatic after CEO produces Decision Record |

### Session Output Directory

All production artifacts are written to a per-session directory under `.cdp-output/` in the project working directory:

```
.cdp-output/YYYY-MM-DD_<issue-slug>/
```

The **issue slug** is derived from the Issue Title produced in CEO Phase 1: lowercase, replace non-alphanumeric characters (except hyphens) with hyphens, collapse consecutive hyphens, trim to 50 characters, and strip leading/trailing hyphens.

**Directory structure:**

```
.cdp-output/2026-02-22_should-we-acquire-competitor-x/
├── index.html                          # Decision briefing page
├── PRESENTATION_should-we-acquire-competitor-x.pptx
├── REPORT_should-we-acquire-competitor-x.docx
├── RESULTS_should-we-acquire-competitor-x.pdf
├── CAPSULE_should-we-acquire-competitor-x.pdf
├── images/                             # Infographic PNGs
└── build/                              # Rerunnable build scripts
```

The placeholder `{session-output}` used throughout this section and in production templates refers to this resolved path.

### Dependency Pipeline

```
Task A: Image Agent (infographics)          --+
Task B: Presentation Agent (PPTX)           --+-- parallel
Task C: Document Agent (DOCX)              --+
                                              |
Task D: Web Page Agent (HTML)    <-- blocked by A + B + C
                                              |
Task E: Archivist (PDFs)         <-- blocked by D
```

### Production Agents

**Task A -- Image Agent** (parallel, unblocked)
Generates 5-6 analytical infographics via browser automation:
1. Routing Diagram -- which C-suite activated and why
2. Domain Scorecard -- recommendation/confidence matrix
3. Fault Line Map -- agreement/contention visualization
4. Risk-Opportunity Matrix -- impact/likelihood grid
5. Action Plan Timeline -- Gantt-style next steps
6. Mode Comparison (multi-mode only) -- divergence tree

Output: `{session-output}/images/INFOGRAPHIC_*.png`
Spec: See individual infographic descriptions above

**Task B -- Presentation Agent** (parallel, unblocked)
Creates board-ready PPTX via `pptxgenjs`. 11 slides: Title, Executive
Summary, The Question, Analytical Framework, Domain Analysis (1-2 per
domain), Where Perspectives Collide, The Decision, Guardrails, What Could
Go Wrong, Next Steps, Decision Metadata.

Output: `{session-output}/PRESENTATION_<issue-slug>.pptx`
Build: `{session-output}/build/build_presentation.js`
Spec: `templates/production/board-presentation.md`

**Task C -- Document Agent** (parallel, unblocked)
Creates editable DOCX via `docx` npm package (docx-js). Cover Page, TOC,
8 sections, 2 appendices. US Letter, Arial 12pt, heading styles with
outlineLevel, DXA table widths, LevelFormat.BULLET lists, ImageRun with
alt text.

Output: `{session-output}/REPORT_<issue-slug>.docx`
Build: `{session-output}/build/build_report.js`
Spec: `templates/production/board-document.md`

**Task D -- Web Page Agent** (blocked by A + B + C)
Creates self-contained interactive HTML briefing page. Hero, Executive
Summary, Problem Context, Analytical Framework, Domain Analysis cards,
Fault Line Visualization, The Decision, Dissenting Views, Action Plan,
Download Section (PPTX + DOCX links), Metadata, Navigation. Inline CSS/JS,
no CDN, works from `file://`, PDF-compatible.

Output: `{session-output}/index.html`
Spec: `templates/production/decision-briefing-page.md`

**Task E -- Archivist** (blocked by D)
Produces Results PDF (print rendering of index.html) and Deliberation
Capsule PDF (Cover + 5 layers: Overview, Decision, Analysis, Process,
Context). Technology: weasyprint (fallback: pdfkit/wkhtmltopdf).

Output: `{session-output}/RESULTS_<issue-slug>.pdf`
         `{session-output}/CAPSULE_<issue-slug>.pdf`
Build: `{session-output}/build/build_capsule.py`
Spec: `templates/production/capsule-structure.md`

### Orchestrator Spawn Sequence
```
TaskCreate: "Generate analytical infographics"               -> task A
TaskCreate: "Create board presentation (PPTX)"               -> task B
TaskCreate: "Create board document (DOCX)"                   -> task C
TaskCreate: "Create interactive decision briefing page"      -> task D
TaskCreate: "Produce Results PDF and Deliberation Capsule"   -> task E

TaskUpdate: { taskId: D, addBlockedBy: [A, B, C] }
TaskUpdate: { taskId: E, addBlockedBy: [D] }
```

---

## Routing and Configuration

### Decision-Type Routing
Default C-suite activation by decision type. CEO can override.
See `config/routing-table.md` for full table.

| Type | Default Activation |
|------|-------------------|
| Strategic | CEO, CFO, CTO, VP Sales |
| Operational | CEO, COO, VP Delivery |
| Financial | CEO, CFO, COO |
| Technical | CEO, CTO, CISO |
| Personnel | CEO, CAO, COO, VP Delivery |
| Compliance/Risk | CEO, CISO, CAO, CFO |

### Full-Activation Thresholds
All C-suite activate if ANY condition applies:
1. Practically irreversible
2. Affects >30% of headcount
3. Changes market position or business model
4. Existential financial risk
5. CEO uncertain which domains are relevant

### Company Profile
Archetype presets set roster, default mode, escalation behavior, and
compliance frameworks. See `config/company-profile.md`.

Archetypes: Technology/SaaS (default), Professional Services, Regulated
Industry, Manufacturing/Physical.

### Company Context
An optional markdown file containing real company data — financials,
headcount, tech stack, strategic position, constraints — that grounds
agent reasoning in facts rather than generic frameworks.

- **Location:** `.cdp-context/company.md` in the project root
- **Create it:** Copy `templates/company-context.md` to `.cdp-context/company.md` and fill in what you know. All sections are optional.
- **How it flows:** The CEO reads the file at session start and includes it in the Phase 0 Shared Consciousness Broadcast. All activated agents receive the same company data simultaneously.
- **Privacy:** The `.cdp-context/` directory is gitignored by default — it contains sensitive business data and should not be committed.

Without this file, agents reason using general frameworks. With it,
agents ground their analysis in your actual numbers and constraints.

---

## File References

### Configuration
- `config/routing-table.md` -- Decision-type routing defaults and thresholds
- `config/company-profile.md` -- Archetype presets and override mechanism
- `config/decision-modes.md` -- Five mode definitions with prompt modifiers
- `.cdp-context/company.md` -- Company facts for grounded reasoning (user-created, gitignored)

### Output Templates
- `templates/advisory-note.md` -- Tier 1 Advisory Note + Escalation Brief
- `templates/panel-assessment.md` -- Tier 2 Panel Assessment
- `templates/decision-record.md` -- Tier 3 Decision Record (9 sections)
- `templates/comparative-decision-record.md` -- Multi-mode comparison format

### Production Templates
- `templates/production/decision-briefing-page.md` -- HTML page spec
- `templates/production/board-presentation.md` -- PPTX slide structure
- `templates/production/board-document.md` -- DOCX document structure
- `templates/production/capsule-structure.md` -- Capsule PDF layers

### Agent Definitions (installed to `.claude/agents/` by auto-setup)
- `agents/ceo.md` -- CEO with five-phase cascade protocol
- `agents/c-suite/*.md` -- 8 C-suite agent definitions (COO, CFO, CTO, CISO, CAO, VP Sales, VP Delivery, CSO)
- `agents/team-leads/{domain}/*.md` -- 34 team lead subagent definitions across 8 domains

---

## SMB-First Design Bias

The skill defaults to lightweight engagement. Most SMB decisions are fast,
informal, and made by one or two people. The skill matches that tempo:

- `/cdp:evaluate` auto-triage leans toward Tier 1 unless clear multi-domain
  signals are present
- Tier 1 is the daily habit; Tier 3 is the deliberate escalation
- A skill that defaults to the full board meeting for every question will
  not see daily use

**Default cell:** Tier 1 + Analyst -- quick, evidence-weighted, transparent
about uncertainty.
