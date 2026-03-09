# Contributing to the Corporate Decision Panel

Thank you for your interest in contributing. This project is a **Claude Code agent skill** — not a traditional software library. Contributions involve agent definitions, prompt templates, routing configuration, and documentation rather than application code.

## Getting Started

1. **Fork** the repository and clone your fork.
2. **Branch** from `main` with a descriptive name (e.g. `add-cpo-agent`, `fix-routing-weights`).
3. **Install locally** by symlinking the repo into your Claude Code skills directory:
   ```bash
   ln -s /path/to/corporate-decision-panel ~/.claude/skills/corporate-decision-panel
   ```
4. Test your changes by running CDP commands (`/cdp:panel`, `/cdp:consult`, etc.) in Claude Code.

## Project Structure

| Path | Purpose |
|------|---------|
| `agents/ceo.md` | CEO synthesizer agent definition |
| `agents/c-suite/` | C-suite executive agent definitions |
| `agents/team-leads/` | Domain-specialist team lead agents |
| `commands/cdp/` | Slash command definitions (`panel`, `consult`, `evaluate`, `deliberate`, `production`, `resume`, `cleanup`) |
| `config/` | Routing table, decision modes, company profile template |
| `scripts/` | Python scripts (config parser, model applicator, infographic generation, PDF builder) |
| `templates/` | Output templates (decision records, assessments, board documents) |
| `tests/` | Automated tests for Python scripts |
| `SKILL.md` | Skill entry point and orchestration logic |

## Types of Contributions

- **Agent improvements** — Refine an existing agent's perspective, expertise description, or analytical lens.
- **New team leads** — Add specialist agents under an existing C-suite domain.
- **Templates** — Improve output structure or add new document formats.
- **Configuration** — Enhance routing logic, decision modes, or scoring criteria.
- **Documentation** — Clarify setup, usage, or architectural decisions.
- **Bug reports** — File issues for incorrect routing, missing perspectives, or template errors.

## Preserving Engineered Dissent

The panel's value comes from its balance of perspectives. The current composition is intentional:

- **4 Skeptic** — CFO, CISO, COO, VP Delivery
- **2 Advocate** — CTO, VP Sales
- **1 Systemic** — CAO
- **1 Investigative** — CSO
- **1 Synthesizer** — CEO

When proposing changes to agent roles or adding new executives, explain how the change preserves or improves this balance. Pull requests that shift the panel toward uncritical consensus will not be merged.

## Writing Standards

### Agent Definitions

- State the agent's **perspective type** (skeptic, advocate, systemic, investigative, synthesizer).
- Define a clear **analytical lens** — what this agent uniquely focuses on.
- Include **domain expertise** boundaries so the agent stays in character.
- Avoid overlap with existing agents; each should bring a distinct viewpoint.

### Templates

- Use clear section headers that map to the analysis pipeline.
- Include placeholder markers (`{{placeholder}}`) for dynamic content.
- Keep formatting consistent with existing templates in `templates/`.

### Configuration

- Routing changes must include the rationale in the PR description.
- Decision mode changes should document the intended effect on panel composition.

## Pull Request Process

Every PR should include:

- **What** — A concise description of the change.
- **Why** — The problem it solves or improvement it makes.
- **How tested** — How you verified the change works (e.g. which CDP command you ran, what scenario you tested).
- **Dissent impact** — Whether the change affects the skeptic/advocate balance, and if so, how.

PRs require one approving review before merge. Keep changes focused — one logical change per PR.

## Issue Reporting

Use these category prefixes in issue titles:

- `[Agent]` — Issues with agent behavior or definitions
- `[Template]` — Template formatting or content issues
- `[Routing]` — Incorrect panel composition or routing logic
- `[Docs]` — Documentation gaps or errors
- `[Feature]` — New capability requests

## Code of Conduct

Be respectful, constructive, and assume good intent. We're building a tool for better decision-making — let's model that in how we collaborate.
