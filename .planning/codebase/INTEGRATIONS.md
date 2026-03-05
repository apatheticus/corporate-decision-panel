# External Integrations

**Analysis Date:** 2026-03-04

## APIs & External Services

**AI Model APIs:**
- Claude Opus 4.6 - CEO orchestration and cross-domain synthesis
  - SDK: Claude API via Claude Code runtime
  - Auth: Implicit via Claude Code session
  - Usage: Layer 1 agent (1 instance per deliberation)

- Claude Sonnet - C-suite domain executives and synthesis
  - SDK: Claude API via Claude Code runtime
  - Auth: Implicit via Claude Code session
  - Usage: Layer 2 agents (8 instances, parallel dispatch)

- Claude Haiku - Team lead specialist analysts
  - SDK: Claude API via Claude Code runtime
  - Auth: Implicit via Claude Code session
  - Usage: Layer 3 agents (up to 34 instances, hierarchical dispatch)

**Image Generation Platforms:**
- Google Gemini Pro (default) - Analytical infographic generation
  - Platform: `gemini.google.com`
  - Auth: User session required (browser automation)
  - Config: Set via `.cdp-context/config.md` → `Platform: gemini`
  - Model: Gemini Pro (selected via UI mode picker)
  - Usage: Task A -- Image Agent generates 5-6 infographics per session
  - Integration: JSON prompt templates submitted via browser automation

- ChatGPT (GPT-4o or latest) - Alternative image generation platform
  - Platform: `chatgpt.com`
  - Auth: User session required (browser automation)
  - Config: Set via `.cdp-context/config.md` → `Platform: chatgpt`
  - Model: GPT-4o (selected via UI model picker dropdown)
  - Usage: Task A -- Image Agent (configurable alternative to Gemini)
  - Integration: JSON prompt templates submitted via browser automation

## Data Storage

**Databases:**
- Not used - CDP is a pure analysis engine with no persistent state

**File Storage:**
- Local filesystem (project root `.cdp-output/` directory)
  - Session records (Markdown) - Persisted for production re-runs
  - Infographic images (PNG) - Analytical visualizations
  - Build artifacts (JavaScript, Python scripts) - Rerunnable production jobs
  - Session metadata (YAML frontmatter in RECORD.md)

**Caching:**
- Claude Code Agent Team context management (internal) - Conversation caching between phases
- No external caching service required

## Authentication & Identity

**Auth Provider:**
- Implicit via Claude Code session - No separate auth system
- Infographic generation requires active user session with:
  - Google Gemini account (for Gemini mode)
  - OpenAI ChatGPT account (for ChatGPT mode)
  - Browser automation handles interacting with existing sessions

**Configuration:**
- `.cdp-context/config.md` selects platform (Gemini default)
- Platform selection persists per project
- User must be logged into the selected platform to generate infographics

## Monitoring & Observability

**Error Tracking:**
- Not integrated with external service
- Errors logged to Claude Code session transcript
- Infographic generation failures handled gracefully:
  - Up to 3 retry attempts per infographic (full prompt → corrective feedback → simplified prompt)
  - Session-wide cap of 12 submissions across all infographics
  - Fallback: Placeholder PNG generated with saved prompt for manual re-submission

**Logs:**
- Claude Code session console output
- Persisted RECORD.md contains decision metadata and audit trail
- `.cdp-output/build/` contains executable build scripts for artifact regeneration

**Observability Signals:**
- Production pipeline execution state (Task A-E dependency graph)
- `production_runs` counter in RECORD.md frontmatter
- `last_production` timestamp for session history

## CI/CD & Deployment

**Hosting:**
- Claude Code (local to project where the skill is installed)
- No remote server deployment required
- Skill repo can be cloned globally (`~/.claude/skills/`) or per-project (`.claude/skills/`)

**Installation Pipeline:**
- Python installer (`install.py`) copies agent and command definitions to `.claude/`
- Auto-setup fallback if installer is skipped (executed on first command invocation)
- Idempotent design allows safe re-runs after `git pull` to pick up updates

**Artifact Generation:**
- Local file system output to `.cdp-output/YYYY-MM-DD_<issue-slug>/`
- No remote upload or sync (user manages local or cloud storage)
- Session records and artifacts remain in project directory by default

## Environment Configuration

**Required env vars:**
- None explicit - CDP uses Claude Code session implicitly
- Infographic platforms require active browser session:
  - Gemini: User must be logged into `gemini.google.com`
  - ChatGPT: User must be logged into `chatgpt.com`

**Secrets location:**
- No secrets stored in CDP or configuration files
- User's browser cookies/session tokens (implicit, not CDP-managed)
- `.cdp-context/` directory gitignored to protect company data in `company.md`

**Config files:**
- `.cdp-context/company.md` - Optional company profile with financials and constraints
- `.cdp-context/style.md` - Optional visual style overrides for infographics
- `.cdp-context/config.md` - Optional platform selection for image generation

## Webhooks & Callbacks

**Incoming:**
- None - CDP is a CLI-driven analysis tool with no webhook endpoints

**Outgoing:**
- None - CDP does not push data to external services
- Infographic generation is pull-based (user submits JSON prompts to Gemini/ChatGPT)

## Platform Integration Details

### Image Agent Workflow

**Location:** `templates/production/infographics.md`

**Platforms supported:**
- Gemini (default, primary)
- ChatGPT (alternative)

**Prompt format:**
- JSON templates with Pauhu schema hybrid convention
- Six top-level keys: `core`, `style`, `technical`, `composition`, `quality_keywords`, `extras`
- Template directory: `templates/infographic-prompts/`

**Integration pattern:**
1. Image Agent reads platform selection from `.cdp-context/config.md`
2. For each infographic:
   - Load JSON template from `templates/infographic-prompts/<type-slug>.json`
   - Populate placeholders with Decision Record data
   - Apply style overrides from `.cdp-context/style.md` (if present)
   - Submit JSON to configured platform via browser automation
   - Implement 3-attempt escalation per image (within same conversation)
   - Save PNG to `{session-output}/images/INFOGRAPHIC_<type-slug>.png`
   - If all attempts fail: generate placeholder PNG and save prompt as `INFOGRAPHIC_<type-slug>_PROMPT.json`

**Attempt budgets:**
- Per-infographic: 3 attempts maximum
- Session-wide: 12 submissions across all infographics
- Strict limits to prevent runaway submissions

**Infographics generated:**
1. Routing Diagram - C-suite activation visualization
2. Domain Scorecard - Recommendation/confidence matrix
3. Fault Line Map - Agreement/contention analysis
4. Risk-Opportunity Matrix - Impact/likelihood grid
5. Action Plan Timeline - Gantt-style next steps
6. Mode Comparison (multi-mode only) - Divergence tree

### Artifact Generation Pipeline

**Task A -- Image Agent:**
- Infographic PNGs via Gemini/ChatGPT browser automation
- Output: `{session-output}/images/INFOGRAPHIC_*.png`

**Task B -- Presentation Agent:**
- PPTX via pptxgenjs
- Output: `{session-output}/PRESENTATION_<issue-slug>.pptx`

**Task C -- Document Agent:**
- DOCX via docx npm package
- Output: `{session-output}/REPORT_<issue-slug>.docx`
- (Or `ADVISORY_<issue-slug>.docx` for Tier 1)

**Task D -- Web Page Agent:**
- Self-contained HTML briefing page
- Output: `{session-output}/index.html`
- Embeds images from Task A, links to PPTX/DOCX from Tasks B/C

**Task E -- Archivist:**
- Results PDF (print rendering of index.html)
- Deliberation Capsule PDF (5-layer document)
- Output: `{session-output}/RESULTS_<issue-slug>.pdf`, `{session-output}/CAPSULE_<issue-slug>.pdf`

---

*Integration audit: 2026-03-04*
