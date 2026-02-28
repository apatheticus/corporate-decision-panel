<div align="center">

# Development Guide

### Corporate Decision Panel -- Contributor Reference

*How to set up a development environment and contribute to CDP.*

*Version 1.0 · February 2026*

</div>

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Development Setup](#development-setup)
- [How CDP Works as a Skill](#how-cdp-works-as-a-skill)
- [Making Changes](#making-changes)
- [Testing Changes](#testing-changes)
- [Project Conventions](#project-conventions)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Optional Skills & Dependencies](#optional-skills--dependencies)

---

## Prerequisites

**Required:**

| Dependency | Purpose |
|-----------|---------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Runtime environment -- CDP runs as a Claude Code skill |
| Git | Version control |
| Python 3+ | Installer script ([`install.py`](../install.py)) |

**Optional (for production pipeline):**

| Dependency | Purpose | Install |
|-----------|---------|---------|
| Node.js + npm | PPTX generation (pptxgenjs), DOCX generation (docx) | [nodejs.org](https://nodejs.org) |
| pptxgenjs | Board presentation generation | `npm install pptxgenjs` |
| docx | Board document and advisory document generation | `npm install docx` |
| weasyprint | PDF generation (Results PDF, Capsule PDF) | `pip install weasyprint` |

Without the optional dependencies, the deliberation cascade works fully -- only the production artifact generation is affected.

---

## Repository Structure

```
corporate-decision-panel/
├── SKILL.md                             # Skill entry point + orchestration protocol
├── README.md                            # Project overview and reference
├── install.py                           # Copies agents + commands into .claude/
├── LICENSE
├── CONTRIBUTING.md                      # Contribution standards
├── COLLABORATORS.md
├── .gitignore
│
├── agents/                              # Agent definitions
│   ├── ceo.md                           # CEO orchestrator (Opus)
│   ├── c-suite/                         # C-suite executives (Sonnet × 8)
│   │   ├── coo.md
│   │   ├── cfo.md
│   │   ├── cto.md
│   │   ├── ciso.md
│   │   ├── cao.md
│   │   ├── vp-sales.md
│   │   ├── vp-delivery.md
│   │   └── cso.md
│   └── team-leads/                      # Specialist analysts (Haiku × 34)
│       ├── coo/                         # 4 team leads
│       ├── cfo/                         # 5 team leads
│       ├── cto/                         # 4 team leads
│       ├── ciso/                        # 4 team leads
│       ├── vp-sales/                    # 4 team leads
│       ├── vp-delivery/                 # 4 team leads
│       ├── cao/                         # 4 team leads
│       └── cso/                         # 5 team leads
│
├── commands/                            # Slash command definitions
│   └── cdp/
│       ├── consult.md                   # /cdp:consult (Tier 1)
│       ├── panel.md                     # /cdp:panel (Tier 2)
│       ├── deliberate.md               # /cdp:deliberate (Tier 3)
│       ├── evaluate.md                 # /cdp:evaluate (auto-triage)
│       └── production.md              # /cdp:production (re-run production)
│
├── config/                              # System configuration
│   ├── company-profile.md               # Archetype presets + override mechanism
│   ├── decision-modes.md                # Five mode definitions + prompt modifiers
│   └── routing-table.md                 # Decision-type routing + threshold conditions
│
├── templates/                           # Output format specifications
│   ├── advisory-note.md                 # Tier 1 output format
│   ├── panel-assessment.md              # Tier 2 output format
│   ├── decision-record.md               # Tier 3 output format
│   ├── comparative-decision-record.md   # Multi-mode output format
│   ├── company-context.md               # Template for .cdp-context/company.md
│   ├── style-context.md                 # Template for .cdp-context/style.md
│   ├── config-context.md                # Template for .cdp-context/config.md
│   └── production/                      # Production artifact specifications
│       ├── advisory-document.md         # Tier 1 DOCX spec
│       ├── board-document.md            # DOCX report spec
│       ├── board-presentation.md        # PPTX slide deck spec
│       ├── decision-briefing-page.md    # HTML briefing page spec
│       └── capsule-structure.md         # Archival PDF spec
│
└── docs/                                # Documentation
    ├── README.md                        # User manual
    ├── ARCHITECTURE.md                  # Technical architecture
    ├── DEVELOPMENT.md                   # This file
    └── media/                           # Documentation images
```

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/<your-username>/corporate-decision-panel
cd corporate-decision-panel
```

### 2. Symlink for Local Testing

Create a symlink so Claude Code discovers the skill from your working copy:

```bash
# Project-local install
mkdir -p <your-project>/.claude/skills
ln -s /path/to/corporate-decision-panel <your-project>/.claude/skills/corporate-decision-panel

# Or global install (all projects)
mkdir -p ~/.claude/skills
ln -s /path/to/corporate-decision-panel ~/.claude/skills/corporate-decision-panel
```

### 3. Run the Installer

The installer copies agent definitions and slash commands from the skill directory into `.claude/`:

```bash
python3 install.py
```

This is idempotent -- safe to re-run after every change. It:

- Copies `agents/` to `.claude/agents/` (preserving `c-suite/` and `team-leads/` structure)
- Copies `commands/` to `.claude/commands/` (preserving `cdp/` structure)
- Appends `.cdp-output/` and `.cdp-context/` to `.gitignore` (project-local only)
- Creates `.cdp-context/` directory (project-local only)
- Seeds `.cdp-context/` with `company.md`, `style.md`, and `config.md` templates (skips files already present)

### 4. Verify Installation

```bash
# Agent definitions are in place
ls .claude/agents/ceo.md

# Slash commands are in place
ls .claude/commands/cdp/
```

After running the installer, restart Claude Code so it picks up the new slash commands.

---

## How CDP Works as a Skill

CDP uses the [Claude Code skill system](https://docs.anthropic.com/en/docs/claude-code). The key files:

- **[`SKILL.md`](../SKILL.md)** -- The skill entry point. Contains the full orchestration protocol: setup check, invocation grammar, phase definitions, agent architecture, production pipeline logic, and routing configuration. Claude Code reads this file when the skill is invoked.

- **[`install.py`](../install.py)** -- Pre-session installer. Copies agent and command files into `.claude/` so they're available immediately when Claude Code starts. Without this, CDP falls back to auto-setup on first invocation (defined in SKILL.md's Setup Check section), but slash commands won't be available until the session is restarted.

- **Agent definitions** (`agents/`) -- Markdown files that Claude Code loads as agent teammates (C-suite) or subagents (team leads). The frontmatter specifies model, tools, and max turns.

- **Command definitions** (`commands/cdp/`) -- Markdown files that Claude Code registers as slash commands. Each command parses the user's input and delegates to the orchestration protocol in SKILL.md.

The skill works because Claude Code's agent system treats markdown files with YAML frontmatter as agent specifications. The `model` field controls which Claude model runs the agent, the `tools` field restricts available tools, and the markdown body is the agent's system prompt.

---

## Making Changes

### Agent Definitions (C-Suite or Team Lead)

**Files:** `agents/c-suite/*.md`, `agents/team-leads/{domain}/*.md`

When modifying an agent:

- Preserve the agent's **perspective type** (skeptic, advocate, systemic, investigative). Changing this affects the engineered dissent balance.
- Keep the **analytical framework** focused on the agent's domain. Agents should not evaluate topics outside their mandate.
- Maintain the **output template** structure so the C-suite parent can synthesize across team leads consistently.
- Ensure **forcing questions** are answerable and genuinely adversarial. They should force the agent to challenge its own analysis.
- Update **blind spots** if the domain boundary changes.

When adding a new team lead:

1. Create the file in `agents/team-leads/{c-suite-parent}/`
2. Use `model: haiku` and restrict tools to `Read`, `Grep`, `Glob`, `WebSearch`
3. Set `maxTurns: 5`
4. Follow the structure of existing team leads (identity, framework, template, forcing questions, blind spots)

### Slash Commands

**Files:** `commands/cdp/*.md`

Commands parse user input and delegate to the orchestration logic in SKILL.md. When modifying a command, ensure:

- The invocation grammar documented in SKILL.md matches the parsing logic
- New parameters are documented in both the command file and SKILL.md

### Configuration (Routing, Modes, Archetypes)

**Files:** `config/routing-table.md`, `config/decision-modes.md`, `config/company-profile.md`

- **Routing changes** affect which C-suite agents activate for each decision type. Ensure the rationale is documented.
- **Mode changes** affect how the CEO weighs competing perspectives. Run the calibration protocol after changes.
- **Archetype changes** affect default behavior for different company types.

### Templates (Output Formats, Production Specs)

**Files:** `templates/*.md`, `templates/production/*.md`

- Output templates define the structure of advisory notes, panel assessments, and decision records. Keep section headers consistent with what the CEO and C-suite agents reference.
- Production templates define the specs for generated artifacts (PPTX, DOCX, HTML, PDF). These are read by production agents as their build instructions.

### Installer

**File:** `install.py`

The installer is a simple Python script that copies files. If you add new directories to `agents/` or `commands/`, the existing `shutil.copytree` calls will pick them up automatically. Changes to installer behavior should maintain idempotency.

---

## Testing Changes

CDP is a prompt-and-configuration system, not a traditional application. There is no automated test suite. Testing is manual and scenario-based.

### Manual Testing

Run CDP commands against your changes and verify the output:

```
# Quick test of a single agent
/cdp:consult cfo: Can we afford to hire 15 engineers this quarter?

# Test routing and multi-agent interaction
/cdp:panel finance tech: Should we build this feature in-house?

# Full cascade test
/cdp:deliberate: Should we pivot to a platform model?

# Test auto-triage logic
/cdp:evaluate: Should we acquire CompetitorX?

# Re-run production for most recent session
/cdp:production
```

### Calibration Protocol

For changes to decision modes or the CEO's synthesis logic, run the calibration protocol defined in [`config/company-profile.md`](../config/company-profile.md):

1. Select a contentious test issue where reasonable people would disagree
2. Run a full Tier 3 cascade with `all-modes`
3. Verify that at least 3 of 5 modes produce materially different outcomes
4. If fewer than 3 modes diverge, the prompt modifiers need revision

### What to Verify

| Change Type | What to Test |
|-------------|-------------|
| Agent definition | Run a Tier 1 consult with the agent; verify it stays in domain, follows its template, answers forcing questions |
| Routing rule | Run `/cdp:evaluate` with several issue types; verify the CEO routes correctly |
| Decision mode | Run a multi-mode comparison; verify the mode produces a distinct synthesis |
| Output template | Run the relevant tier; verify the output matches the template structure |
| Production spec | Run with `--produce` (Tier 2) or Tier 3; verify the artifact is generated correctly |

---

## Project Conventions

### Markdown-Only Codebase

CDP has no traditional application code. The entire system is defined in Markdown files with YAML frontmatter. The only executable code is:

- `install.py` -- Python installer script
- Production build scripts generated at runtime (`build/*.js`, `build/*.py`)

### Preserving Engineered Dissent

The 4-2-1-1-1 composition (4 skeptics, 2 advocates, 1 systemic, 1 investigative, 1 synthesizer) is the system's most important design decision. Any change that shifts the balance must be documented and justified. Pull requests that move the system toward uncritical consensus will not be merged.

### Agent Definition Standards

Every agent definition must include:

- **Perspective type** -- Skeptic, advocate, systemic, investigative, or synthesizer
- **Analytical lens** -- What the agent uniquely focuses on
- **Domain expertise boundaries** -- What the agent does and does not evaluate
- **Output template** -- Mandatory structure for findings
- **Forcing questions** -- At least three adversarial self-challenge questions

### Template Conventions

- Use clear section headers that map to the analysis pipeline
- Include placeholder markers (`{{placeholder}}`) for dynamic content
- Keep formatting consistent with existing templates in `templates/`

### Style

- Use `--` for em dashes (not `—`)
- Professional, clear writing -- avoid jargon where a plain word works
- Code examples use fenced code blocks with language identifiers
- Tables for structured comparisons
- Mermaid diagrams where they add clarity

---

## Pull Request Process

Every PR should include:

| Section | Description |
|---------|-------------|
| **What** | A concise description of the change |
| **Why** | The problem it solves or improvement it makes |
| **How tested** | Which CDP command you ran, what scenario you tested |
| **Dissent impact** | Whether the change affects the skeptic/advocate balance, and if so, how |

PRs require one approving review before merge. Keep changes focused -- one logical change per PR.

**Branch naming:** Use descriptive names that indicate the change type:
- `add-cpo-agent` -- Adding a new agent
- `fix-routing-weights` -- Fixing routing logic
- `update-decision-record-template` -- Template changes
- `docs-architecture` -- Documentation changes

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the full contribution guide.

---

## Issue Reporting

Use these category prefixes in issue titles:

| Prefix | Category |
|--------|----------|
| `[Agent]` | Issues with agent behavior or definitions |
| `[Template]` | Template formatting or content issues |
| `[Routing]` | Incorrect panel composition or routing logic |
| `[Docs]` | Documentation gaps or errors |
| `[Feature]` | New capability requests |

---

## Optional Skills & Dependencies

The production pipeline uses these external Claude Code skills for generating artifacts. CDP's deliberation cascade works without them -- only production output is affected.

| Skill | Used For | Install |
|-------|----------|---------|
| [docx](https://github.com/anthropics/skills) | Board document (DOCX) and advisory document generation | `/find-skills docx` |
| [pdf](https://github.com/anthropics/skills) | Results PDF and Capsule PDF generation | `/find-skills pdf` |
| [frontend-design](https://github.com/anthropics/skills) | Decision briefing page (HTML) | `/find-skills frontend-design` |
| [web-design-guidelines](https://github.com/vercel-labs/agent-skills) | UI review for briefing page | `/find-skills web-design-guidelines` |
| [find-skills](https://github.com/vercel-labs/skills) | Skill discovery | `/install find-skills` |
| [skill-creator](https://github.com/anthropics/skills) | Skill authoring (development only) | `/find-skills skill-creator` |

---

<div align="center">

<br>

**[Back to Top](#development-guide)**

Made with 💨 by the Zerø Effort

Copyright 2026

</div>
