# Production Pipeline

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
├── RECORD.md
├── index.html
├── PRESENTATION_should-we-acquire-competitor-x.pptx
├── REPORT_should-we-acquire-competitor-x.docx
├── RESULTS_should-we-acquire-competitor-x.pdf
├── CAPSULE_should-we-acquire-competitor-x.pdf
├── CDP_should-we-acquire-competitor-x.zip
├── images/
├── build/
├── logs/
├── sub-questions/
├── deliberation/
└── reports/
```

**Directory structure (Tier 1):**

```
.cdp-output/2026-02-22_can-we-afford-to-hire-this-quarter/
├── RECORD.md
├── ADVISORY_can-we-afford-to-hire-this-quarter.docx
├── CDP_can-we-afford-to-hire-this-quarter.zip
├── build/
├── logs/
├── sub-questions/
├── deliberation/
└── reports/
```

The placeholder `{session-output}` used throughout this section and in production templates refers to this resolved path.

### Pre-flight Dependency Validation

Before spawning the CCO, the orchestrator validates external dependencies using shell commands and passes the results in the CCO prompt. All production tasks are optional -- the Decision Record (`RECORD.md`) is always produced regardless of task availability. "Required" here means required within a specific task: if a task's dependencies are missing, the CCO's team leads skip that task with explicit install instructions, but all other tasks whose dependencies are satisfied continue normally.

**Dependency table:**

| Agent | Dependencies | Check Command | Install Command |
|-------|-------------|---------------|-----------------|
| Graphic Designer (infographics) | python3, google-genai, Pillow | `python3 -c "from google import genai; from PIL import Image"` | `pip install google-genai>=1.65.0 Pillow>=10.0.0` |
| Writer (PPTX) | node, pptxgenjs | `node -e "require('pptxgenjs')"` | `npm install pptxgenjs` |
| Writer (DOCX) | node, docx | `node -e "require('docx')"` | `npm install docx` |
| Publisher (HTML) | none | -- | -- |
| Publisher (Results PDF) | python3, reportlab, Pillow, pdf2image | `python3 -c "from reportlab.platypus import SimpleDocTemplate; from PIL import Image; from pdf2image import convert_from_path"` | `pip install reportlab Pillow pdf2image` |
| Publisher (Capsule PDF) | python3, weasyprint | `python3 -c "import weasyprint"` | `pip install weasyprint` |

**Execution protocol:**

1. Run each check command from the table above. A non-zero exit code means the dependency is missing.
2. Build a summary table showing task readiness:

   | Agent | Status | Missing Dependencies |
   |-------|--------|---------------------|
   | Graphic Designer (infographics) | READY / SKIP | -- / `pip install google-genai>=1.65.0 Pillow>=10.0.0` |
   | Writer (PPTX) | READY / SKIP | -- / `npm install pptxgenjs` |
   | ... | ... | ... |

   Use a checkmark for ready tasks and a warning marker for skipped tasks, listing the install command so the user can enable them next time.
3. Print the summary table for user visibility before spawning any tasks.
4. Spawn ONLY tasks whose dependencies are satisfied. Do not spawn tasks that failed their check command.
5. List all skipped tasks with their install instructions so the user can install missing dependencies for next time.
6. ALWAYS produce `RECORD.md` regardless of which tasks are skipped -- the Decision Record is the primary output, production artifacts are supplementary.

**Note on Publisher HTML:** The HTML briefing page has no external
dependencies of its own. If some upstream artifacts (infographics, DOCX,
PPTX) failed, the Publisher still runs with whatever artifacts are
available.

### CCO Wave-Based Dispatch (Tier 2/3)

The CCO manages the production pipeline autonomously using a four-wave
dispatch pattern:

```
CEO spawns CCO → CCO reads RECORD.md → CCO creates Creative Brief
→ Wave 1: Graphic Designer           (infographic generation)
→ Wave 2: Writer                     (document production -- PNGs now available)
→ Wave 3: Editor                     (reviews all output)
→ Wave 4: Publisher                  (HTML + PDFs + packaging)
```

See `config/cco-dispatch-protocol.md` for the full dispatch specification.

### Production Team Leads

**Graphic Designer** (Wave 1)
Generates 5-6 analytical infographics via the Gemini API using
`scripts/session.py`. Reads the Decision Record, extracts data per
infographic type, writes data JSON files, and calls the session
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

**Writer** (Wave 2)
Creates board-ready PPTX via `pptxgenjs` and editable DOCX via `docx`
npm package (docx-js). PPTX: 11 slides (Title, Executive Summary, The
Question, Analytical Framework, Domain Analysis, Where Perspectives
Collide, The Decision, Guardrails, What Could Go Wrong, Next Steps,
Decision Metadata). DOCX: Cover Page, TOC, 8 sections, 2 appendices.
US Letter, Arial 12pt, heading styles with outlineLevel.

Output: `{session-output}/PRESENTATION_<issue-slug>.pptx`
         `{session-output}/REPORT_<issue-slug>.docx`
Build: `{session-output}/build/build_presentation.js`
         `{session-output}/build/build_report.js`
Spec: `templates/production/board-presentation.md`,
         `templates/production/board-document.md`

**Editor** (Wave 3, sequential after Waves 1-2)
Reviews all Wave 1 artifacts for accuracy, consistency, tone,
completeness, and infographic quality. Compares artifacts against
RECORD.md (source of truth) and the Creative Brief (tone guidance).
Read-only by design -- the Editor judges, it does not modify.

Verdict: APPROVED | APPROVED WITH NOTES | REVISION REQUIRED
Spec: `agents/team-leads/cco/editor.md`

**Publisher** (Wave 4, sequential after Wave 3)
Creates self-contained interactive HTML briefing page (Hero, Executive
Summary, Problem Context, Analytical Framework, Domain Analysis cards,
Fault Line Visualization, The Decision, Dissenting Views, Action Plan,
Download Section, Metadata, Navigation). Inline CSS/JS, no CDN, works
from `file://`. Also produces Results PDF (generated natively from
RECORD.md via `scripts/build_results_pdf.py` using reportlab — not
rendered from HTML) and Deliberation Capsule PDF (Cover + 5 layers:
Overview, Decision, Analysis, Process, Context via weasyprint).
Incorporates editorial notes from the Editor.

Output: `{session-output}/index.html`
         `{session-output}/RESULTS_<issue-slug>.pdf`
         `{session-output}/CAPSULE_<issue-slug>.pdf`
Build: `scripts/build_results_pdf.py` (Results PDF, permanent),
         `{session-output}/build/build_capsule.py` (Capsule PDF, per-session)
Spec: `templates/production/decision-briefing-page.md`,
         `templates/production/capsule-structure.md`

**Advisory Document Agent** (Tier 1 only, single-task pipeline -- no CCO)
Produces a lightweight Advisory Document DOCX from the Advisory Note. Memo
format (1-2 pages): header block with metadata, the user's question, the
advisory response, and an optional Escalation Brief section if the C-suite
agent appended one. Technology: `docx` npm package (same as board document).

Output: `{session-output}/ADVISORY_<issue-slug>.docx`
Build: `{session-output}/build/build_advisory.js`
Spec: `templates/production/advisory-document.md`

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

### Orchestrator Spawn Sequence (Tier 2/3)

The orchestrator spawns a single CCO agent as a standalone background
subagent, which manages the entire production pipeline internally:

```
Agent tool call:
  subagent_type: "general-purpose"
  name: "cco"
  run_in_background: true
  description: "CCO production pipeline"
  prompt: [RECORD.md content + session context + dependency status]
```

The CCO reads the Decision Record, produces a Creative Brief, creates
its own production team (`TeamCreate: "cdp-cco-{issue-slug}"`), and
dispatches its team leads as teammates in four sequential waves (Graphic Designer
→ Writer → Editor → Publisher). See `config/cco-dispatch-protocol.md`.

**Re-run invocation (`/cdp:production`):** When invoked via production re-run,
the orchestrator reads record content from `RECORD.md` instead of conversation
context and includes it in the CCO Agent prompt. The CCO and its production
team behave identically regardless of original vs. re-run invocation.

**Tier 1 Spawn Sequence:** Single Agent tool call for the Advisory Document DOCX. No CCO, no waves -- one agent, one artifact.
```
Agent tool call:
  subagent_type: "general-purpose"
  name: "advisory-document-agent"
  run_in_background: true
  description: "Advisory Document DOCX"
  prompt: [Advisory Note content + session context]
```
