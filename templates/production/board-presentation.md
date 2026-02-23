# Board Presentation Specification (PPTX)

## Purpose

The board presentation structures the decision briefing for live presentation -- one concept per slide, visual aids, speaker-note-ready. Built for the meeting room. The content is identical to the HTML and DOCX artifacts; the format serves the presentation consumption context.

**Filename:** `{session-output}/PRESENTATION_<issue-slug>.pptx`
**Build script:** `{session-output}/build/build_presentation.js`

> `{session-output}` and `<issue-slug>` are provided by the CEO in your task description. Use them directly.

**Runs in parallel** with Image Agent (Task A) and Document Agent (Task C) -- no dependencies on other production agents.

---

## Technology

**Library:** `pptxgenjs` (Node.js)

The Presentation Agent writes a build script (`build_presentation.js`) that uses pptxgenjs to generate the PPTX programmatically. The script is saved alongside the output and is rerunnable: `node build_presentation.js` regenerates the presentation from current data.

**Key pptxgenjs patterns:**
```javascript
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();

// Set layout
pres.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5 inches

// Define slide masters for consistency
pres.defineSlideMaster({
  title: 'TITLE_SLIDE',
  background: { color: '1a1a2e' },
  objects: [/* title text, subtitle, date */]
});

pres.defineSlideMaster({
  title: 'CONTENT_SLIDE',
  background: { color: 'ffffff' },
  objects: [/* header bar, footer, slide number */]
});

// Add slides
let slide = pres.addSlide({ masterName: 'CONTENT_SLIDE' });
slide.addText('Title', { x: 0.5, y: 0.3, w: 12, fontSize: 36, fontFace: 'Georgia', bold: true });
slide.addText('Body content', { x: 0.5, y: 1.5, w: 12, fontSize: 14, fontFace: 'Calibri' });

// Add images (infographics)
slide.addImage({ path: '../images/INFOGRAPHIC_routing-diagram.png', x: 1, y: 2, w: 10, h: 4 });

// Add tables
slide.addTable(tableData, { x: 0.5, y: 2, w: 12, colW: [3, 4, 2, 3], fontSize: 12, fontFace: 'Calibri' });

// Save
pres.writeFile({ fileName: '../PRESENTATION_issue-slug.pptx' });
```

---

## Slide Structure

### Slide 1: Title
**Content source:** Decision Record header

| Element | Specification |
|---------|--------------|
| Background | Dark (`--color-bg-dark`), domain-appropriate palette |
| Issue title | 44pt Georgia, white, centered, bold |
| Subtitle line | Decision type + Tier + Date |
| Decision mode badge | Small indicator showing the synthesis mode |
| Bottom | Company name (from company profile) if configured |

### Slide 2: Executive Summary
**Content source:** Decision Record Executive Summary

| Element | Specification |
|---------|--------------|
| Heading | "Executive Summary" -- 36pt Georgia |
| Decision callout | The decision statement in a visually prominent box (accent color background, 24pt, bold) |
| Summary bullets | 3-5 bullet points distilling the key reasoning and primary dissent -- 14pt Calibri |
| Key metric | One stat callout if applicable (60-72pt, accent color) -- e.g., "14-month runway" or "$2.3M investment" |

### Slide 3: The Question
**Content source:** Decision Record Section 1 (Issue Statement)

| Element | Specification |
|---------|--------------|
| Heading | "The Question" -- 36pt Georgia |
| Issue statement | The question as originally posed -- 16pt Calibri, emphasis formatting |
| Business context | 2-3 sentences of background -- 14pt Calibri |
| Visual | Simple visual element framing the question (e.g., question in a distinct container) |

### Slide 4: Analytical Framework
**Content source:** Decision Record Section 2 (CEO Framing)

| Element | Specification |
|---------|--------------|
| Heading | "Analytical Framework" -- 36pt Georgia |
| Routing diagram | `INFOGRAPHIC_routing-diagram.png` -- primary visual, prominently placed |
| Evaluation dimensions | Listed alongside or below the diagram -- 14pt Calibri |
| Activation summary | "N domains activated, M excluded" -- brief annotation |

### Slides 5-N: Domain Analysis (1-2 slides per domain)
**Content source:** Decision Record Section 3 (Domain Analyses)

Each activated domain gets 1-2 slides depending on content volume.

**Single-slide domain (typical):**

| Element | Specification |
|---------|--------------|
| Heading | "[C-Suite Role] -- [Mandate Title]" -- 36pt Georgia |
| Recommendation badge | Color-coded indicator (Approve/Conditions/Oppose/Neutral) -- prominent |
| Confidence level | Visual indicator alongside recommendation |
| Summary | 2-3 sentence synthesis -- 14pt Calibri |
| Key findings | Team lead highlights in a concise table or bullet list |
| Risk/Opportunity callout | Split layout: risks on left (red accent), opportunities on right (green accent) |

**Two-slide domain (when detailed team lead findings are important):**
- Slide A: Recommendation, summary, key risks and opportunities
- Slide B: Team lead findings detail table, internal contradictions if any

**Domain scorecard infographic** (`INFOGRAPHIC_domain-scorecard.png`): Embedded on the first domain analysis slide as an overview before individual domain slides.

### Slide N+1: Where Perspectives Collide
**Content source:** Decision Record Section 4 (Fault Line Analysis)

| Element | Specification |
|---------|--------------|
| Heading | "Where Perspectives Collide" -- 36pt Georgia |
| Fault line map | `INFOGRAPHIC_fault-lines.png` -- primary visual |
| Agreement points | 2-3 bullets showing consensus areas -- 14pt Calibri |
| Contention points | 2-3 bullets showing divergence with domains named -- 14pt Calibri, bold domain names |
| Pre-mortem callout | Most critical failure mode in a distinct callout box |

### Slide N+2: The Decision
**Content source:** Decision Record Section 5 (CEO Decision)

| Element | Specification |
|---------|--------------|
| Heading | "The Decision" -- 36pt Georgia |
| Decision statement | 24pt, bold, prominent container -- the most important text on this slide |
| Most determinative perspective | Highlighted with brief rationale |
| Decision weight rationale | 2-3 sentences on how perspectives were weighed -- 14pt Calibri |
| Decision mode indicator | Small badge showing which mode produced this synthesis |

### Slide N+3: Guardrails
**Content source:** Decision Record Section 5 (Conditions & Guardrails, Accepted Risks)

| Element | Specification |
|---------|--------------|
| Heading | "Guardrails & Conditions" -- 36pt Georgia |
| Conditions | Numbered list of non-negotiable prerequisites -- 14pt Calibri, each linked to the domain concern it addresses |
| Accepted risks | Brief list with reasoning -- 14pt Calibri |
| Mitigations | Directed actions for risk reduction |

### Slide N+4: What Could Go Wrong
**Content source:** Decision Record Section 6 (Dissenting Views) + Section 4 (Pre-Mortem)

| Element | Specification |
|---------|--------------|
| Heading | "What Could Go Wrong" -- 36pt Georgia |
| Dissenting views | Each dissenting role's core objection -- 14pt Calibri, structured as role + objection pairs |
| Pre-mortem failure modes | Top 2-3 failure scenarios from Phase 4.5 -- styled as warning elements |
| Risk matrix | `INFOGRAPHIC_risk-matrix.png` if space permits (or on a separate slide) |

### Slide N+5: Next Steps
**Content source:** Decision Record Section 7 (Next Steps)

| Element | Specification |
|---------|--------------|
| Heading | "Next Steps" -- 36pt Georgia |
| Action plan | `INFOGRAPHIC_action-plan.png` -- primary visual |
| Action table | Structured: Action / Owner / Timeline / Priority -- 12pt Calibri |
| Review triggers | When to revisit this decision -- brief bullets |

### Slide N+6: Decision Metadata (Closing)
**Content source:** Decision Record Section 8 (Metadata)

| Element | Specification |
|---------|--------------|
| Background | Dark (matching title slide) |
| Heading | "Decision Metadata" -- 36pt Georgia, white |
| Key metadata | Decision ID, date, type, complexity, dissent level, mode -- 14pt Calibri, white |
| Roles consulted | Count and list |
| Key assumptions | Listed as decision review triggers |
| Company profile | Archetype used |

---

## Design Principles

### Color Palette
- **Bold, content-informed**: The palette should reflect the decision domain and tone, not default to generic corporate blue.
- Domain-appropriate primary and accent colors (see decision-briefing-page.md Color Palette section)
- Dark background for title and closing slides
- Light background for content slides
- Recommendation badges: green (Approve), amber (Conditions), red (Oppose), gray (Neutral)

### Typography
- **Titles**: 36-44pt, Georgia or comparable serif
- **Body text**: 14-16pt, Calibri or comparable sans-serif
- **Stat callouts**: 60-72pt for key numbers or metrics, accent color
- **Professional pairing**: Serif headers with sans-serif body creates visual hierarchy
- No accent lines under titles

### Visual Elements
- **Every slide has a visual element**: infographic, data callout, structured table, or styled container. No text-only slides.
- Infographic images embedded at readable scale
- Tables with clean formatting, alternating row shading for readability
- Color-coded badges and indicators for quick scanning

### Layout
- Wide format (13.33 x 7.5 inches) for maximum content area
- Consistent margins and element positioning via slide masters
- Left-aligned text (not centered body text)
- Visual elements right-aligned or bottom-aligned to balance text

---

## Multi-Mode Variant

When the source is a Comparative Decision Record:

### Shared Analysis Slides (Presented Once)
Slides 3-N+1 (The Question through Where Perspectives Collide) are identical to single-mode -- the analysis is shared across modes.

### Per-Mode Synthesis Slides (1 per mode)
Replace the single "The Decision" slide with one slide per compared mode:

| Element | Specification |
|---------|--------------|
| Heading | "[Mode Name] Synthesis" -- 36pt Georgia |
| Mode indicator | Prominent badge/label showing the mode |
| Decision statement | 20pt, bold |
| Most determinative perspective | Role + brief rationale |
| Key factor | What tipped this mode's decision |
| Conditions | Brief list of guardrails under this mode |

### The Key Choice (Divergence Slide)
**Content source:** Comparative Decision Record Divergence Analysis

| Element | Specification |
|---------|--------------|
| Heading | "The Key Choice" -- 36pt Georgia |
| Mode comparison infographic | `INFOGRAPHIC_mode-comparison.png` -- divergence tree |
| Where modes agree | Brief bullets |
| Where modes diverge | Brief bullets with mode names |
| The Key Choice | The underlying values/priorities question -- 20pt, prominent callout |
| Mode Sensitivity | Visual indicator on the slide (e.g., gauge graphic or labeled spectrum) |

### Closing Slide Additions
- Mode Sensitivity rating
- All modes listed with their individual decisions

---

## Content Mapping from Decision Record

| Decision Record Section | Slide(s) | Transformation Notes |
|---|---|---|
| Header / ID / Date / Type | Title slide | Formatted as presentation title layout |
| Executive Summary | Executive Summary slide | Distilled to bullets + stat callout |
| Section 1: Issue Statement | The Question slide | Framed as the central question |
| Section 2: CEO Framing | Analytical Framework slide | Routing diagram infographic as primary visual |
| Section 3: Domain Analyses | Domain Analysis slides (1-2 per domain) | Scorecard infographic + per-domain recommendation cards |
| Section 4: Fault Line Analysis | Where Perspectives Collide slide | Fault line map infographic + key contentions |
| Section 5: CEO Decision | The Decision + Guardrails slides | Decision prominently displayed, conditions listed |
| Section 6: Dissenting Views | What Could Go Wrong slide | Objections + pre-mortem failure modes |
| Section 7: Next Steps | Next Steps slide | Action plan infographic + structured table |
| Section 8: Metadata | Decision Metadata closing slide | Key metadata on dark background |

The Presentation Agent synthesizes the Decision Record into presentation-ready content. Slides should tell a story: Setup (Question) -> Analysis (Domains, Fault Lines) -> Resolution (Decision, Guardrails) -> Action (Next Steps). Each slide should convey one concept with supporting visuals. The audience should be able to follow the narrative without reading the full Decision Record.
