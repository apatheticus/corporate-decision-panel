# Technology Stack

**Analysis Date:** 2026-03-04

## Languages

**Primary:**
- Python 3 - Installation and setup automation (`install.py`)
- Markdown - Skill definition, agent definitions, command definitions, templates
- JSON - Configuration files for infographic prompts (`templates/infographic-prompts/*.json`)

**Secondary:**
- JavaScript/Node.js - Referenced in production pipeline for PPTX/DOCX generation (`pptxgenjs`, `docx` npm packages)
- Python - Fallback PDF generation (`weasyprint`, `pdfkit`, `wkhtmltopdf`)
- YAML - Frontmatter in markdown files for agent metadata and RECORD.md

## Runtime

**Environment:**
- Claude Code (Anthropic Claude Code Agent SDK) - Primary runtime environment for the entire skill
- Python 3 - Standalone installer execution environment

**Package Manager:**
- pip (implied by Python dependencies in production agents)
- npm (implied by Node.js dependencies for PDF/PPTX generation)

## Frameworks

**Core:**
- Claude Code Skill System - The foundational framework for CDP (version 1.0 as of Feb 2026)
- Agent Team (Claude Code) - Multi-agent orchestration for parallel execution

**Document Generation:**
- pptxgenjs - PPTX presentation generation (`templates/production/board-presentation.md`)
- docx (docx-js) - DOCX document generation (`templates/production/board-document.md`)

**PDF Generation:**
- weasyprint (primary) - HTML to PDF conversion for Results PDF and Capsule PDF
- pdfkit/wkhtmltopdf (fallback) - Alternative PDF generation if weasyprint unavailable

**Infographic Generation:**
- Browser automation (Claude Code native) - Interact with Gemini and ChatGPT for image generation via JSON prompts

## Key Dependencies

**Critical:**
- Claude Opus 4.6 model - CEO synthesis and cross-domain judgment (layer 1 orchestrator)
- Claude Sonnet - C-suite agents for domain decomposition and synthesis (8 agents, layer 2)
- Claude Haiku - Team lead specialist analysis (34 agents, layer 3)

**External AI Platforms:**
- Google Gemini Pro (image generation, default) - Infographic generation via browser automation
- ChatGPT (GPT-4o or latest) - Alternative infographic generation platform, user-configurable

**Infrastructure:**
- pptxgenjs - PowerPoint presentation generation library
- docx (docx-js npm package) - DOCX document creation with styling
- weasyprint - CSS-based HTML to PDF rendering

## Configuration

**Environment:**
- `.cdp-context/` - Project-level configuration directory (gitignored)
  - `company.md` - Real company data (financials, headcount, tech stack, constraints)
  - `style.md` - Visual style overrides for infographics (colors, rendering quality, composition)
  - `config.md` - Platform selection for image generation (Gemini or ChatGPT, defaults to Gemini)

**Skill Configuration:**
- `.claude/agents/` - Agent definitions (CEO, C-suite, team leads)
- `.claude/commands/cdp/` - Slash command definitions (consult, panel, deliberate, evaluate, production)
- `config/company-profile.md` - Company archetype presets (Tech/SaaS, Professional Services, Regulated, Manufacturing)
- `config/routing-table.md` - Default C-suite activation rules by decision type
- `config/decision-modes.md` - Five CEO synthesis modes (Guardian, Pioneer, Architect, Analyst, Sentinel)

**Build Artifacts:**
- `.cdp-output/YYYY-MM-DD_<issue-slug>/` - Per-session output directory
  - `RECORD.md` - Persisted session record with YAML frontmatter
  - `build/` - Rerunnable build scripts for production artifacts
  - `images/` - Generated infographic PNGs

## Platform Requirements

**Development:**
- Claude Code (any recent version)
- Python 3.6+ (for installer)
- macOS, Linux, or Windows (installer uses `pathlib` and `shutil` for cross-platform compatibility)

**Production:**
- Claude Code environment with access to:
  - Claude Opus 4.6 API (CEO)
  - Claude Sonnet API (C-suite agents)
  - Claude Haiku API (team leads)
  - Google Gemini Pro API OR OpenAI ChatGPT API (infographic generation)

**Deployment:**
- `.claude/` directory in project root (for agent and command definitions)
- `.cdp-context/` directory in project root (for configuration and company data)
- `.cdp-output/` directory in project root (for session outputs, gitignored by default)

## Optional Dependencies

**Infographic Generation:**
- Browser automation for web UI interaction (Gemini or ChatGPT)
- JavaScript/Node.js runtime (if using pptxgenjs and docx packages locally)
- weasyprint with Python runtime (for PDF generation)

**File Formats:**
- PPTX (Office Open XML) - PowerPoint presentations
- DOCX (Office Open XML) - Word documents
- PDF (PDF/A or standard PDF) - Portable results and capsule archives
- HTML5 + CSS3 - Interactive briefing pages (self-contained, no CDN)
- PNG - Analytical infographics (generated via Gemini or ChatGPT)

---

*Stack analysis: 2026-03-04*
