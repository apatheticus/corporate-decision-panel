---
name: corporate-decision-panel
version: 1.1.04
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
  - /cdp:production
  - /cdp:cleanup
---

# Corporate Decision Panel

A boardroom in a box. Present any business issue and receive structured,
multi-perspective analysis with engineered dissent -- not consensus from a
single voice, but a decision that shows where expert perspectives collide
and why.

---

## Setup Check

> **Preferred install method:** Run `python3 install.py` from the skill
> directory before starting Claude Code. This ensures slash commands are
> discoverable on first session launch. The auto-setup below is a fallback
> for users who skip the installer.

Before executing any command, verify that CDP agent definitions and slash
commands are installed in the project's `.claude/` directory.

**Check:** Does `.claude/agents/ceo.md` exist in the project root?

**If NO (first run -- auto-setup fallback):**
1. Copy all files from this skill's `agents/` directory to `.claude/agents/`,
   preserving the directory structure (`c-suite/`, `team-leads/`)
2. Copy all files from this skill's `commands/` directory to `.claude/commands/`,
   preserving the directory structure (`cdp/`)
3. Append these entries to the project root `.gitignore` if not already present:
   - `.cdp-output/`
   - `.cdp-context/`
4. Create `.cdp-context/` directory if it doesn't exist
5. Seed `.cdp-context/` with template files (`company.md`, `style.md`, `config.md`) if not already present -- copies from `templates/` directory
6. Print setup confirmation:
   ```
   CDP auto-setup complete.
   - Agent definitions copied to .claude/agents/
   - Slash commands copied to .claude/commands/cdp/

   NOTE: Slash commands (/cdp:consult, /cdp:panel, etc.) require a
   Claude Code restart to become available. Start a new session to use them.

   Quick start (after restart):
     /cdp:consult cfo: Can we afford to hire this quarter?
     /cdp:panel finance tech: Should we build or buy?
     /cdp:deliberate: Should we pivot to a platform model?
     /cdp:evaluate: Should we acquire CompetitorX?
   ```
7. If the user provided a command with this invocation, proceed to execute it

**If YES:** Proceed directly to command execution.

---

## Invocation Grammar

### Tier 1 -- Hallway Question
```
/cdp:consult [role] [mode?]: [question]
```
Quick, opinionated consult with one C-suite agent. No CEO, no routing,
no team leads. Produces an **Advisory Note** (3-5 sentences) and an
**Advisory Document** (DOCX memo).

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

Production always triggers after the Panel Assessment, producing the same
five artifacts as Tier 3 (HTML, PPTX, DOCX, Results PDF, Capsule PDF)
with proportionally lighter content.

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

### Production Re-run
```
/cdp:production [session-path?]
```

Re-runs only the production pipeline for an existing session using the
persisted `RECORD.md`. Does not re-run the deliberation cascade.

Session resolution:
1. Explicit path → validate it contains `RECORD.md`
2. Slug substring match → scan `.cdp-output/*/RECORD.md`, disambiguate if multiple
3. No argument → most recent session (by date prefix)
4. No sessions → error

Examples:
- `/cdp:production` — most recent session
- `/cdp:production .cdp-output/2026-02-28_should-we-acquire-competitor-x/`
- `/cdp:production acquire-competitor` — fuzzy slug match

### Session Cleanup
```
/cdp:cleanup [--older-than days?]
```
Deletes old CDP session directories from `.cdp-output/` with age-based
filtering and a confirmation prompt before deletion. Default threshold
is 30 days.

- `/cdp:cleanup` -- delete sessions older than 30 days
- `/cdp:cleanup --older-than 7` -- delete sessions older than 7 days

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
5. Derive issue slug from the user's question (lowercase, replace non-alphanumeric
   with hyphens, collapse consecutive hyphens, trim to 50 chars, strip leading/trailing hyphens)
6. Create session output directory: `.cdp-output/YYYY-MM-DD_<issue-slug>/build/`
7. Spawn Document Agent to produce Advisory Document DOCX

Output template: `templates/advisory-note.md`
Output spec: `templates/production/advisory-document.md`

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
   - Dispatches team lead subagents via the Agent tool -- **parallel per domain** (all Agent tool calls in a single response per C-suite agent). See `config/dispatch-protocol.md`.
   - Collects team lead findings
   - Synthesizes domain recommendation with confidence level
6. CEO runs **Phase 5** (abbreviated synthesis):
   - Collects domain recommendations
   - Applies Decision Mode
   - Produces Panel Assessment
7. Trigger production pipeline
8. Return Panel Assessment to user

Output template: `templates/panel-assessment.md`

### Tier 3: Board Meeting

Full five-phase cascade with optional Phase 1.5 (CSO research) and
Phase 4.5 (pre-mortem challenge). The authoritative phase protocol is
defined in `config/orchestration-protocol.md`. The overview below
describes the flow at a summary level.

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

### Production Re-run Protocol

When invoked via `/cdp:production`, execute the following steps:

1. **Resolve session directory.** Apply session resolution rules (explicit path,
   slug substring match, or most recent by date prefix). Error if no `.cdp-output/`
   directory exists.
2. **Read and parse `RECORD.md`.** Split YAML frontmatter from body content.
   Extract `type`, `tier`, `issue_title`, `issue_slug`, `activated_roles`, and
   `decision_mode` (or `decision_modes` for multi-mode) from frontmatter.
3. **Error if `RECORD.md` missing.** Display: "This session predates the
   `/cdp:production` feature. Re-run the original deliberation command to
   generate production artifacts and a RECORD.md for future re-runs."
4. **Display session summary.** Show issue title, tier, mode, date, activated
   roles, and number of previous production runs to the user.
5. **Clean stale artifacts.** Remove all files in the session directory except
   `RECORD.md` and the `build/` directory. Recreate `images/` directory.
6. **Route by tier.** Tier 1: spawn Advisory Document Agent only. Tier 2/3:
   spawn the full five-task production DAG (Tasks A-E).
7. **Pass record body content** as input to production agents. Include the full
   record text in each production TaskCreate description. Production agents
   behave identically regardless of original vs. re-run invocation.
8. **Update `RECORD.md` frontmatter.** Increment `production_runs` by 1. Set
   `last_production` to current ISO 8601 timestamp.
9. **Return completion summary.** List all generated artifacts with file paths.

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

| Tier | Production | Artifacts |
|------|-----------|-----------|
| Tier 1 | Always | DOCX |
| Tier 2 | Always | HTML, PPTX, DOCX, Results PDF, Capsule PDF |
| Tier 3 | Always | HTML, PPTX, DOCX, Results PDF, Capsule PDF |

### Session Output Directory

All production artifacts are written to a per-session directory under `.cdp-output/` in the project working directory:

```
.cdp-output/YYYY-MM-DD_<issue-slug>/
```

The **issue slug** is derived from the Issue Title produced in CEO Phase 1: lowercase, replace non-alphanumeric characters (except hyphens) with hyphens, collapse consecutive hyphens, trim to 50 characters, and strip leading/trailing hyphens.

**Directory structure (Tier 2 and Tier 3):**

```
.cdp-output/2026-02-22_should-we-acquire-competitor-x/
├── RECORD.md                              # Persisted session record
├── index.html                          # Decision briefing page
├── PRESENTATION_should-we-acquire-competitor-x.pptx
├── REPORT_should-we-acquire-competitor-x.docx
├── RESULTS_should-we-acquire-competitor-x.pdf
├── CAPSULE_should-we-acquire-competitor-x.pdf
├── images/                             # Infographic PNGs
└── build/                              # Rerunnable build scripts
```

**Directory structure (Tier 1):**

```
.cdp-output/2026-02-22_can-we-afford-to-hire-this-quarter/
├── RECORD.md
├── ADVISORY_can-we-afford-to-hire-this-quarter.docx
└── build/
    └── build_advisory.js
```

The placeholder `{session-output}` used throughout this section and in production templates refers to this resolved path.

### Pre-flight Dependency Validation

Before spawning production tasks, the orchestrator validates external dependencies for each task using shell commands. All production tasks are optional -- the Decision Record (`RECORD.md`) is always produced regardless of task availability. "Required" here means required within a specific task: if a task's dependencies are missing, that task is skipped with explicit install instructions, but all other tasks whose dependencies are satisfied continue normally.

**Dependency table:**

| Task | Dependencies | Check Command | Install Command |
|------|-------------|---------------|-----------------|
| A (Image Agent) | python3, google-genai, Pillow | `python3 -c "from google import genai; from PIL import Image"` | `pip install google-genai>=1.65.0 Pillow>=10.0.0` |
| B (Presentation) | node, pptxgenjs | `node -e "require('pptxgenjs')"` | `npm install pptxgenjs` |
| C (Document) | node, docx | `node -e "require('docx')"` | `npm install docx` |
| D (Web Page) | none | -- | -- |
| E (Archivist) | python3, weasyprint | `python3 -c "import weasyprint"` | `pip install weasyprint` |

**Execution protocol:**

1. Run each check command from the table above. A non-zero exit code means the dependency is missing.
2. Build a summary table showing task readiness:

   | Task | Status | Missing Dependencies |
   |------|--------|---------------------|
   | A (Image Agent) | READY / SKIP | -- / `pip install google-genai>=1.65.0 Pillow>=10.0.0` |
   | B (Presentation) | READY / SKIP | -- / `npm install pptxgenjs` |
   | ... | ... | ... |

   Use a checkmark for ready tasks and a warning marker for skipped tasks, listing the install command so the user can enable them next time.
3. Print the summary table for user visibility before spawning any tasks.
4. Spawn ONLY tasks whose dependencies are satisfied. Do not spawn tasks that failed their check command.
5. List all skipped tasks with their install instructions so the user can install missing dependencies for next time.
6. ALWAYS produce `RECORD.md` regardless of which tasks are skipped -- the Decision Record is the primary output, production artifacts are supplementary.

**Note on Task D:** Task D (Web Page) has no external dependencies of its own. It is blocked by Tasks A, B, and C in the DAG, but if some of those are skipped, Task D still runs with whatever artifacts are available. Task D should always be spawned.

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
Generates 5-6 analytical infographics via the Gemini API using
`scripts/session.py`. The Image Agent reads the Decision Record, extracts
data per infographic type, writes data JSON files, and calls the session
orchestrator. Each infographic is produced by populating a JSON prompt
template (Pauhu schema hybrid) with Decision Record data, applying style
overrides from `.cdp-context/style.md` (if present), and calling the
Gemini API with vision-based quality validation. Retries use corrective
feedback. If all attempts are exhausted, a placeholder PNG is generated
and the populated JSON prompt is saved alongside it for manual retry.

Infographics produced:
1. Routing Diagram -- which C-suite activated and why
2. Domain Scorecard -- recommendation/confidence matrix
3. Fault Line Map -- agreement/contention visualization
4. Risk-Opportunity Matrix -- impact/likelihood grid
5. Action Plan Timeline -- Gantt-style next steps
6. Mode Comparison (multi-mode only) -- divergence tree

Output: `{session-output}/images/INFOGRAPHIC_*.png`
Prompt templates: `templates/infographic-prompts/*.json`
Spec: `templates/production/infographics.md`

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

**Task C' -- Advisory Document Agent** (Tier 1 only, single-task pipeline)
Produces a lightweight Advisory Document DOCX from the Advisory Note. Memo
format (1-2 pages): header block with metadata, the user's question, the
advisory response, and an optional Escalation Brief section if the C-suite
agent appended one. Technology: `docx` npm package (same as board document).

Output: `{session-output}/ADVISORY_<issue-slug>.docx`
Build: `{session-output}/build/build_advisory.js`
Spec: `templates/production/advisory-document.md`

**Task D -- Web Page Agent** (blocked by A + B + C)
Creates self-contained interactive HTML briefing page. Hero, Executive
Summary, Problem Context, Analytical Framework, Domain Analysis cards,
Fault Line Visualization, The Decision, Dissenting Views, Action Plan,
Download Section (PPTX + DOCX links), Metadata, Navigation. Inline CSS/JS,
no CDN, works from `file://`, PDF-compatible.

Output: `{session-output}/index.html`
Spec: `templates/production/decision-briefing-page.md`

**Task E -- Archivist** (blocked by D, maxTurns: 15)
Produces Results PDF (print rendering of index.html) and Deliberation
Capsule PDF (Cover + 5 layers: Overview, Decision, Analysis, Process,
Context). Technology: weasyprint (fallback: pdfkit/wkhtmltopdf).

Output: `{session-output}/RESULTS_<issue-slug>.pdf`
         `{session-output}/CAPSULE_<issue-slug>.pdf`
Build: `{session-output}/build/build_capsule.py`
Spec: `templates/production/capsule-structure.md`

### Record Persistence

Before spawning production agents, the orchestrator writes the complete record
(Decision Record, Panel Assessment, or Advisory Note) to
`{session-output}/RECORD.md`. This persisted copy enables `/cdp:production`
re-runs without re-running the deliberation cascade.

**RECORD.md format:**

```yaml
---
type: decision-record | panel-assessment | advisory-note | comparative-decision-record
tier: 1 | 2 | 3
decision_mode: analyst
decision_modes: []           # multi-mode only
issue_title: "Issue Title"
issue_slug: issue-slug
decision_type: Strategic
date: "YYYY-MM-DDTHH:MM:SSZ"
activated_roles: [cfo, cto]
invocation: "/cdp:deliberate: Issue text"
production_runs: 1
last_production: "YYYY-MM-DDTHH:MM:SSZ"
---
```

Body = complete CEO output (Decision Record / Panel Assessment / Advisory Note)
verbatim. No summarization, no reformatting.

### Orchestrator Spawn Sequence
```
TaskCreate: "Generate analytical infographics via Gemini API script"  -> task A
TaskCreate: "Create board presentation (PPTX)"               -> task B
TaskCreate: "Create board document (DOCX)"                   -> task C
TaskCreate: "Create interactive decision briefing page"      -> task D
TaskCreate: "Produce Results PDF and Deliberation Capsule"   -> task E

TaskUpdate: { taskId: D, addBlockedBy: [A, B, C] }
TaskUpdate: { taskId: E, addBlockedBy: [D] }
```

**Re-run invocation (`/cdp:production`):** When invoked via production re-run,
the orchestrator reads record content from `RECORD.md` instead of conversation
context and includes it in each production TaskCreate description. Production
agents behave identically regardless of original vs. re-run invocation.

**Tier 1 Spawn Sequence:** Single TaskCreate for the Advisory Document DOCX. No dependencies, no blocking — one agent, one artifact.
```
TaskCreate: "Create advisory document (DOCX)
  Session output: <absolute-path>  Issue slug: <issue-slug>"            -> Task C'
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

### Infographic Style

An optional markdown file containing visual style preferences --
brand colors, typography, composition, quality keywords -- that the
Image Agent uses to override default JSON prompt values.

- **Location:** `.cdp-context/style.md` in the project root
- **Create it:** Copy `templates/style-context.md` to `.cdp-context/style.md` and fill in your preferences. All settings are optional.
- **How it flows:** The Image Agent reads the file before generating each infographic and overrides the corresponding JSON prompt values (style, color mappings, composition, quality keywords) with your preferences.
- **Privacy:** The `.cdp-context/` directory is gitignored by default -- it contains sensitive business data and should not be committed.

Without this file, the Image Agent uses the default values from each
JSON prompt template. With it, all infographics reflect your brand
palette and visual preferences.

### API Configuration

A markdown file that configures the Gemini API for infographic generation.

- **Location:** `.cdp-context/config.md` in the project root
- **Create it:** Copy `templates/config-context.md` to `.cdp-context/config.md` and set your API key.
- **How it flows:** The generation script reads the API key, model ID, and retry limit before generating infographics. Pre-flight validation verifies the key and billing status.
- **Privacy:** The `.cdp-context/` directory is gitignored by default -- it contains sensitive business data and should not be committed.

Without this file, the generation script cannot run -- a valid API key is required.

---

## File References

### Configuration
- `config/routing-table.md` -- Decision-type routing defaults and thresholds
- `config/company-profile.md` -- Archetype presets and override mechanism
- `config/decision-modes.md` -- Five mode definitions with prompt modifiers
- `config/dispatch-protocol.md` -- Team lead dispatch mechanism (Agent tool, parallel execution, prompt structure)
- `.cdp-context/company.md` -- Company facts for grounded reasoning (user-created, gitignored)
- `.cdp-context/style.md` -- Infographic style overrides (user-created, gitignored)
- `.cdp-context/config.md` -- API configuration for Image Agent (user-created, gitignored)

### Output Templates
- `templates/advisory-note.md` -- Tier 1 Advisory Note + Escalation Brief
- `templates/panel-assessment.md` -- Tier 2 Panel Assessment
- `templates/decision-record.md` -- Tier 3 Decision Record (9 sections)
- `templates/comparative-decision-record.md` -- Multi-mode comparison format

### Production Templates
- `templates/production/infographics.md` -- Image Agent spec (AI platform + JSON prompts)
- `templates/production/advisory-document.md` -- Tier 1 Advisory Document DOCX
- `templates/production/decision-briefing-page.md` -- HTML page spec
- `templates/production/board-presentation.md` -- PPTX slide structure
- `templates/production/board-document.md` -- DOCX document structure
- `templates/production/capsule-structure.md` -- Capsule PDF layers

### Infographic Prompt Templates
- `templates/infographic-prompts/routing-diagram.json` -- Routing Diagram prompt
- `templates/infographic-prompts/domain-scorecard.json` -- Domain Scorecard prompt
- `templates/infographic-prompts/fault-line-map.json` -- Fault Line Map prompt
- `templates/infographic-prompts/risk-opportunity-matrix.json` -- Risk-Opportunity Matrix prompt
- `templates/infographic-prompts/action-plan-timeline.json` -- Action Plan Timeline prompt
- `templates/infographic-prompts/mode-comparison.json` -- Mode Comparison prompt

### Session Records
- `.cdp-output/*/RECORD.md` -- Persisted session record enabling `/cdp:production` re-runs

### Context Templates
- `templates/company-context.md` -- Template for `.cdp-context/company.md`
- `templates/style-context.md` -- Template for `.cdp-context/style.md`
- `templates/config-context.md` -- Template for `.cdp-context/config.md`

### Agent Definitions (installed to `.claude/agents/` by auto-setup)
- `agents/ceo.md` -- CEO identity, judgment criteria, and synthesis logic
- `config/orchestration-protocol.md` -- Five-phase cascade protocol, production pipeline, organizational roster
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
