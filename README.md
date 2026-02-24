# Corporate Decision Panel

**A boardroom in a box.** Present any business issue and receive structured, multi-perspective analysis with engineered dissent -- not consensus from a single voice, but a decision that shows where expert perspectives collide and why.

CDP emulates an SMB executive committee: a CEO frames and routes, C-suite executives analyze through domain lenses, specialist team leads produce findings, and the CEO synthesizes a decision that addresses the strongest objections. Operates at three engagement tiers (hallway question, working session, board meeting) and five synthesis modes (Guardian, Pioneer, Architect, Analyst, Sentinel).

Runs as a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) agent skill.

---

## Install

Clone into your project's `.claude/skills/` directory and run the installer:

```bash
mkdir -p .claude/skills
git clone https://github.com/apatheticus/corporate-decision-panel .claude/skills/corporate-decision-panel
python3 .claude/skills/corporate-decision-panel/install.py
```

The installer copies agent definitions and slash commands into your project's `.claude/` directory so they're available immediately when you start Claude Code. If you skip the installer, CDP will auto-setup on first use -- but slash commands won't be available until you restart the session.

### Update

```bash
cd .claude/skills/corporate-decision-panel && git pull && python3 install.py
```

### Global install (all projects)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/apatheticus/corporate-decision-panel ~/.claude/skills/corporate-decision-panel
python3 ~/.claude/skills/corporate-decision-panel/install.py
```

---

## Quick Start

**Quick consult with one executive** (Tier 1 -- seconds):
```
/cdp:consult cfo: Can we afford to hire 15 engineers this quarter?
```

**Working session with a focused panel** (Tier 2 -- minutes):
```
/cdp:panel finance tech: Should we build this feature in-house or buy?
```

**Full board deliberation** (Tier 3 -- comprehensive analysis):
```
/cdp:deliberate: Should we pivot to a platform model?
```

Not sure which tier? Let the CEO assess:
```
/cdp:evaluate: Should we acquire CompetitorX?
```

---

## Commands

| Command | Tier | Description |
|---------|------|-------------|
| `/cdp:consult [role] [mode?]: [question]` | 1 - Hallway Question | Quick consult with one C-suite agent. Advisory Note (3-5 sentences). |
| `/cdp:panel [roles] [mode?]: [issue]` | 2 - Working Session | CEO + 2-4 C-suite + team leads. Panel Assessment (~1 page). |
| `/cdp:deliberate [mode?]: [issue]` | 3 - Board Meeting | Full five-phase cascade. Decision Record (3-5 pages). |
| `/cdp:evaluate: [issue]` | Auto-Triage | CEO recommends tier, mode, and routing. |

### Decision Modes

| Mode | Disposition | Resolution Pattern |
|------|-------------|-------------------|
| **Guardian** | Risk-averse (MaxiMin) | Weights skeptics. High bar for approval. |
| **Pioneer** | Growth-oriented (MaxiMax) | Weights advocates. Objections are problems to solve. |
| **Architect** | Consensus-building (Behavioral) | Seeks widest organizational support. |
| **Analyst** | Data-driven (Hurwicz) -- **default** | Weights by confidence level. "Defer" is legitimate. |
| **Sentinel** | Regret-minimizing (MiniMax Regret) | Weights strongest single objection. Survivable paths. |

### Multi-Mode Comparison

```
/cdp:deliberate guardian vs pioneer: Should we enter the enterprise market?
/cdp:deliberate all-modes: Should we acquire CompetitorX?
```

Domain analysis runs once. CEO synthesis runs per mode. Cost: ~1.1x for up to 5x the strategic insight.

### Available Roles

`ceo` `coo` `cfo` `cto` `ciso` `cao` `vp-sales` `vp-delivery` `cso`

---

## Architecture

- **9 C-suite agents** with engineered dissent: 4 skeptics, 2 advocates, 1 systemic, 1 investigative, 1 synthesizer
- **34 team lead subagents** across 8 domains with unique analytical frameworks
- **Three-tier model**: CEO (Opus), C-Suite (Sonnet), Team Leads (Haiku)
- **Five-phase cascade**: Frame & Route → Dispatch → Findings → Synthesize → Deliberate
- **Production pipeline**: HTML briefing, PPTX, DOCX, Results PDF, Capsule PDF

See [SKILL.md](SKILL.md) for the complete specification.

---

## Configuration

### Company Context

Ground agent reasoning in your actual company data:

```bash
mkdir -p .cdp-context
cp .claude/skills/corporate-decision-panel/templates/company-context.md .cdp-context/company.md
# Edit with your company's actual data
```

The `.cdp-context/` directory is gitignored by default -- it contains sensitive business data.

### Company Profile

Archetype presets for different industry types (Technology/SaaS, Professional Services, Regulated Industry, Manufacturing). See [config/company-profile.md](config/company-profile.md).

---

## Optional Dependencies

The production pipeline (all tiers) uses these external skills for generating artifacts. Tier 1 requires only the `docx` npm package for the Advisory Document.

| Skill | Used For | Install |
|-------|----------|---------|
| [docx](https://github.com/anthropics/skills) | Board document (DOCX) generation | `/find-skills docx` |
| [pdf](https://github.com/anthropics/skills) | Results PDF and Capsule PDF | `/find-skills pdf` |
| [frontend-design](https://github.com/anthropics/skills) | Decision briefing page (HTML) | `/find-skills frontend-design` |
| [web-design-guidelines](https://github.com/vercel-labs/agent-skills) | UI review for briefing page | `/find-skills web-design-guidelines` |
| [find-skills](https://github.com/vercel-labs/skills) | Skill discovery | `/install find-skills` |
| [skill-creator](https://github.com/anthropics/skills) | Skill authoring (development only) | `/find-skills skill-creator` |

---

## Repository Structure

```
corporate-decision-panel/               # Clone to .claude/skills/corporate-decision-panel
├── SKILL.md                            # Skill definition + auto-setup
├── README.md
├── .gitignore
├── agents/                             # Agent definitions (copied to .claude/agents/ on setup)
│   ├── ceo.md
│   ├── c-suite/
│   │   ├── cao.md, cfo.md, ciso.md, coo.md
│   │   ├── cso.md, cto.md, vp-delivery.md, vp-sales.md
│   └── team-leads/
│       ├── cao/    (4 leads)
│       ├── cfo/    (5 leads)
│       ├── ciso/   (4 leads)
│       ├── coo/    (4 leads)
│       ├── cso/    (5 leads)
│       ├── cto/    (4 leads)
│       ├── vp-delivery/ (4 leads)
│       └── vp-sales/    (4 leads)
├── commands/                           # Slash commands (copied to .claude/commands/ on setup)
│   └── cdp/
│       ├── consult.md, panel.md
│       ├── deliberate.md, evaluate.md
├── config/
│   ├── company-profile.md
│   ├── decision-modes.md
│   └── routing-table.md
└── templates/
    ├── advisory-note.md
    ├── company-context.md
    ├── comparative-decision-record.md
    ├── decision-record.md
    ├── panel-assessment.md
    └── production/
        ├── board-document.md
        ├── board-presentation.md
        ├── capsule-structure.md
        └── decision-briefing-page.md
```
