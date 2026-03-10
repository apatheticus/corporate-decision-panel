# CDP File Index

### Configuration
- `config/routing-table.md` -- Decision-type routing defaults and thresholds
- `config/company-profile.md` -- Archetype presets and override mechanism
- `config/decision-modes.md` -- Five mode definitions with prompt modifiers
- `config/dispatch-protocol.md` -- Sub-question file convention and CEO-as-universal-dispatcher protocol
- `config/cco-dispatch-protocol.md` -- CCO production team dispatch mechanism (wave-based, 4 waves)
- `config/logging-protocol.md` -- Agent logging protocol (structured log output, log directory convention)
- `config/production-pipeline.md` -- Full production pipeline specification (trigger logic, dependencies, wave dispatch, record persistence)
- `.cdp-context/company.md` -- Company facts for grounded reasoning (user-created, gitignored)
- `.cdp-context/style.md` -- Infographic style overrides (user-created, gitignored)
- `.cdp-context/config.md` -- API keys, agent model overrides, and session settings (user-created, gitignored)

### Output Templates
- `templates/advisory-note.md` -- Tier 1 Advisory Note + Escalation Brief
- `templates/panel-assessment.md` -- Tier 2 Panel Assessment
- `templates/decision-record.md` -- Tier 3 Decision Record (9 sections)
- `templates/comparative-decision-record.md` -- Multi-mode comparison format

### Production Templates
- `templates/creative-brief.md` -- Creative Brief reference template (CCO generates dynamically)
- `templates/production/infographics.md` -- Graphic Designer spec (AI platform + JSON prompts)
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

### Scripts
- `scripts/apply_models.py` -- Agent model config applicator (reads config.md, updates .claude/agents/ frontmatter)
- `scripts/build_results_pdf.py` -- Native Results PDF generator (reportlab, from RECORD.md)
- `scripts/session.py` -- Infographic generation session orchestrator
- `scripts/config.py` -- Configuration parser (shared by other scripts)
- `scripts/validation.py` -- Session validation utilities
- `scripts/preflight.py` -- Pre-flight validation (API key, billing status)
- `scripts/generate_infographic.py` -- Single infographic generation via Gemini API

### Session Records
- `.cdp-output/*/RECORD.md` -- Persisted session record enabling `/cdp:production` re-runs

### Context Templates
- `templates/company-context.md` -- Template for `.cdp-context/company.md`
- `templates/style-context.md` -- Template for `.cdp-context/style.md`
- `templates/config-context.md` -- Template for `.cdp-context/config.md`

### Agent Definitions (installed to `.claude/agents/` by auto-setup)
- `agents/ceo.md` -- CEO identity, judgment criteria, and synthesis logic
- `config/orchestration-protocol.md` -- Five-phase cascade protocol, production pipeline, organizational roster
- `agents/c-suite/*.md` -- 9 C-suite agent definitions (COO, CFO, CTO, CISO, CAO, VP Sales, VP Delivery, CSO, CCO)
- `agents/team-leads/{domain}/*.md` -- 38 team lead agent definitions across 9 domains (29 analytical + 5 research + 4 production)
- `agents/team-leads/cco/*.md` -- 4 CCO production team leads (Graphic Designer, Writer, Editor, Publisher)
