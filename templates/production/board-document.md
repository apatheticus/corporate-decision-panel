# Board Document Specification (DOCX)

## Purpose

The board document is the editable artifact designed for executive review workflows: comments, tracked changes, annotation, redlining, and formal approval processes. Where the HTML page is for browsing and the PPTX is for presenting, the DOCX is for **collaborative editing**. The content is identical to the HTML and PPTX -- the format serves the editing and review consumption context.

**Filename:** `{session-output}/REPORT_<issue-slug>.docx`
**Build script:** `{session-output}/build/build_report.js`

> `{session-output}` and `<issue-slug>` are provided by the CEO in your task description. Use them directly.

**Runs in parallel** with Image Agent (Task A) and Presentation Agent (Task B) -- no dependencies on other production agents.

---

## Technology

**Library:** `docx` npm package (docx-js)

The Document Agent writes a build script (`build_report.js`) that uses the `docx` package to generate the DOCX programmatically. The script is saved alongside the output and is rerunnable: `node build_report.js` regenerates the document from current data.

**Validation:** The build script validates output with `scripts/office/validate.py` if available. The DOCX must be genuinely editable -- comments addable, tracked changes functional, text modifiable. A `.docx` file that breaks when opened in Word or Google Docs is a build failure.

---

## Key Implementation Details

### Page Setup
```javascript
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: {
          width: 12240,   // US Letter width in DXA (8.5 inches * 1440)
          height: 15840,  // US Letter height in DXA (11 inches * 1440)
        },
        margin: {
          top: 1440,      // 1 inch
          right: 1440,
          bottom: 1440,
          left: 1440,
        },
      },
    },
    headers: { default: header },
    footers: { default: footer },
    children: [/* document content */],
  }],
});
```

### Font and Typography
- **Primary font**: Arial, 12pt default body text
- **Heading hierarchy**:
  - Heading 1: Arial 18pt bold, `outlineLevel: 0` (for TOC support)
  - Heading 2: Arial 14pt bold, `outlineLevel: 1`
  - Heading 3: Arial 12pt bold, `outlineLevel: 2`
- **Body text**: Arial 12pt, single or 1.15 line spacing
- **Callout text** (decision statement): Arial 14pt bold, shaded background

### Heading Style Overrides
Override built-in heading styles with `outlineLevel` for proper Table of Contents support:
```javascript
new Paragraph({
  text: "Section Title",
  heading: HeadingLevel.HEADING_1,
  style: "Heading1",
  outlineLevel: 0,  // Required for TOC navigation
});
```

### Table Formatting
Tables must use DXA widths exclusively -- never percentage widths:
```javascript
new Table({
  rows: [/* ... */],
  width: { size: 9360, type: WidthType.DXA },  // Full content width
  columnWidths: [2340, 4680, 2340],              // Column widths in DXA
});

// Cell width must also be specified
new TableCell({
  width: { size: 2340, type: WidthType.DXA },
  shading: { type: ShadingType.CLEAR, color: "auto", fill: "F2F2F2" },
  children: [/* ... */],
});
```

### Lists
Use `LevelFormat.BULLET` numbering configuration -- never unicode bullet characters:
```javascript
new Paragraph({
  text: "List item text",
  numbering: { reference: "bullet-list", level: 0 },
});

// Define numbering in document config
const doc = new Document({
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    }],
  },
  // ...
});
```

### Images
Images via `ImageRun` with required `type` parameter and `altText`:
```javascript
new ImageRun({
  data: fs.readFileSync('../images/INFOGRAPHIC_routing-diagram.png'),
  transformation: { width: 600, height: 300 },
  type: 'png',
  altText: {
    title: "Routing Diagram",
    description: "Organizational chart showing which C-suite domains were activated for this decision and why",
    name: "routing-diagram",
  },
});
```

### Page Breaks
`PageBreak` inside `Paragraph` elements:
```javascript
new Paragraph({
  children: [new PageBreak()],
});
```

### Headers and Footers
```javascript
const header = new Header({
  children: [
    new Paragraph({
      children: [
        new TextRun({ text: "Decision Briefing: [Issue Title]", font: "Arial", size: 16, color: "888888" }),
      ],
      alignment: AlignmentType.RIGHT,
    }),
  ],
});

const footer = new Footer({
  children: [
    new Paragraph({
      children: [
        new TextRun({ text: "Page " }),
        new TextRun({ children: [PageNumber.CURRENT] }),
      ],
      alignment: AlignmentType.CENTER,
    }),
  ],
});
```

---

## Document Structure

### Cover Page
**Content source:** Decision Record header + Executive Summary

| Element | Specification |
|---------|--------------|
| Issue title | Arial 28pt bold, centered |
| Decision type | Badge-style text below title |
| Tier indicator | "Tier 3 -- Board Meeting" |
| Decision Mode | Mode name |
| Date | Full date and time |
| Executive summary callout | Shaded box with the decision statement (Arial 14pt) |
| Company name | If configured in company profile |
| Spacing | Vertically centered on page using spacer paragraphs |
| Page break | After cover page |

### Table of Contents
```javascript
new TableOfContents("Table of Contents", {
  hyperlink: true,
  headingStyleRange: "1-3",
});
```
- Auto-generated from heading styles with `outlineLevel`
- Hyperlinked entries for navigation in Word
- Page break after TOC

### Section 1: Executive Summary
**Content source:** Decision Record Executive Summary

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Executive Summary" |
| Content | 3-5 sentence narrative paragraph (not bullet points) |
| Formatting | Opening paragraph style -- slightly larger or bold first sentence to draw the eye |
| Page break | After section |

### Section 2: Problem Statement
**Content source:** Decision Record Section 1 (Issue Statement) + context

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Problem Statement" |
| Issue statement | The question as originally posed, in a styled callout or indented block |
| Business context | 2-3 paragraphs setting the stage for the analysis |
| Page break | After section |

### Section 3: Analytical Framework
**Content source:** Decision Record Section 2 (CEO Framing)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Analytical Framework" |
| Decision type | Classification with rationale |
| Evaluation dimensions | Numbered list |
| Routing rationale table | Table with columns: C-Suite Role, Status (Activated/Excluded), Rationale |
| Routing diagram | `INFOGRAPHIC_routing-diagram.png` embedded via ImageRun |
| Threshold assessment | Full-activation threshold evaluation |
| CSO activation | Research directive if applicable |
| Page break | After section |

### Section 4: Detailed Analysis
**Content source:** Decision Record Section 3 (Domain Analyses)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Detailed Analysis" |
| Domain scorecard | `INFOGRAPHIC_domain-scorecard.png` embedded at section opening |
| Per-domain subsections | Heading 2 for each activated domain |
| Domain recommendation | Color-coded indicator text: green for Approve, amber for Conditions, red for Oppose, gray for Neutral |
| Confidence level | Stated alongside recommendation |
| Summary | 2-3 sentence domain synthesis |
| Team lead findings | Table with columns: Team Lead, Key Finding, Confidence |
| Risks | Bullet list with severity assessments |
| Opportunities | Bullet list with impact assessments |
| Internal contradictions | If present, noted in a distinct paragraph |
| Page break | After section |

### Section 5: Risk & Disagreement Analysis
**Content source:** Decision Record Section 4 (Fault Line Analysis)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Risk & Disagreement Analysis" |
| Fault line map | `INFOGRAPHIC_fault-lines.png` embedded |
| Heading 2 | "Points of Agreement" |
| Agreement bullets | What domains agree on |
| Heading 2 | "Points of Contention" |
| Contention entries | Each contention as a paragraph naming domains and the substance |
| Heading 2 | "Pre-Mortem Failure Modes" |
| Pre-mortem table | Table with columns: C-Suite Role, Predicted Failure Mode, Severity |
| Heading 2 | "Unresolved Tensions" |
| Tension entries | Each tension with what would resolve it |
| Page break | After section |

### Section 6: Decision and Rationale
**Content source:** Decision Record Section 5 (CEO Decision)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Decision and Rationale" |
| Decision callout | Shaded background (light accent color), Arial 14pt bold -- the decision statement prominently displayed |
| Heading 2 | "Most Determinative Perspective" |
| Content | Role identification + rationale for why this perspective was weighted highest |
| Heading 2 | "Decision Weight Rationale" |
| Content | How competing perspectives were weighed -- explicit, not generic |
| Heading 2 | "Conditions & Guardrails" |
| Conditions list | Numbered list, each condition linked to the domain concern it addresses |
| Heading 2 | "Accepted Risks" |
| Risk entries | Each risk with acceptance reasoning |
| Heading 2 | "Mitigations Directed" |
| Mitigation entries | Specific actions with implied owners and timelines |
| Page break | After section |

### Section 7: Counterarguments
**Content source:** Decision Record Section 6 (Dissenting Views)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Counterarguments and Overruled Perspectives" |
| Per-dissent subsections | Heading 2 for each dissenting role |
| Recommendation | What the dissenting role recommended |
| Core objection | The substance of the disagreement -- given full space, not summarized |
| Risk if ignored | What the role believes will happen |
| CEO response | How the objection was weighed and resolved |
| Formatting | Not buried or minimized -- these are full subsections with equal treatment |
| Page break | After section |

### Section 8: Action Plan
**Content source:** Decision Record Section 7 (Next Steps)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Action Plan" |
| Timeline infographic | `INFOGRAPHIC_action-plan.png` embedded |
| Action table | Table with columns: #, Action, Implied Owner, Timeline, Priority |
| Decision review triggers | Bullet list of conditions for revisitation |
| Page break | After section |

### Appendix A: Decision Metadata
**Content source:** Decision Record Section 8 (Metadata)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Appendix A: Decision Metadata" |
| Metadata table | Two-column table: Field, Value |
| Fields | Decision ID, Date, Submitted by, Decision Type, Tier, Decision Mode, Total Roles Consulted, Decision Complexity, Primary Domain, Dissent Level, Company Profile, Routing Override |
| Key assumptions | Listed with confidence levels |
| Research foundation | CSO evidence quality grade if applicable |
| Page break | After appendix |

### Appendix B: Domain Detail
**Content source:** Full team lead outputs (Tier 3 only)

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Appendix B: Domain Detail" |
| Purpose | Expanded team lead findings for deep review -- the full analytical output, not the summarized versions in Section 4 |
| Per-domain subsections | Heading 2 per C-suite domain, Heading 3 per team lead |
| Team lead detail | Full analytical output including framework-specific artifacts (scenario models, compliance assessments, stress tests, etc.) |
| Formatting | Structured tables and lists matching each team lead's output template |
| Note | This appendix is optional for Tier 2 `--produce` runs (less team lead detail available) |

---

## Formatting Requirements Summary

| Element | Specification |
|---------|--------------|
| Page size | US Letter: 12,240 x 15,840 DXA |
| Margins | 1 inch all sides (1,440 DXA) |
| Font family | Arial |
| Body text | 12pt |
| Heading 1 | 18pt bold, outlineLevel 0 |
| Heading 2 | 14pt bold, outlineLevel 1 |
| Heading 3 | 12pt bold, outlineLevel 2 |
| Decision callout | 14pt bold, shaded background (ShadingType.CLEAR with accent fill) |
| Table widths | DXA only (WidthType.DXA), never percentage |
| Table shading | ShadingType.CLEAR |
| Lists | LevelFormat.BULLET, never unicode bullets |
| Images | ImageRun with type parameter and altText |
| Page breaks | PageBreak inside Paragraph elements, between major sections |
| Headers | Document title + date, right-aligned, 8pt gray |
| Footers | Page number centered (PageNumber.CURRENT) |
| TOC | TableOfContents with headingStyleRange "1-3" |
| Color coding | Green (#2d8a4e) Approve, Amber (#d4a017) Conditions, Red (#c0392b) Oppose, Gray (#7f8c8d) Neutral |

---

## Multi-Mode Variant

When the source is a Comparative Decision Record:

### Shared Sections (Sections 1-5)
Sections 1 through 5 present the shared analysis -- identical to single-mode. Domain analyses, fault line analysis, and risk assessment are mode-independent.

### Section 6: Decision and Rationale (Per-Mode Subsections)
Instead of a single decision, Section 6 contains subsections per mode:

- **Heading 1**: "Decision and Rationale"
- **Heading 2**: "6.1 Guardian Synthesis"
  - Decision, determinative perspective, key factor, conditions, accepted risks
- **Heading 2**: "6.2 Pioneer Synthesis"
  - Same structure
- **Heading 2**: "6.3 Architect Synthesis"
  - Same structure
- [Continue for each compared mode]

Each subsection's decision callout uses a slightly different accent color to visually distinguish modes.

### Section 7: Divergence Analysis (Replaces Counterarguments)
In multi-mode, Section 7 becomes the Divergence Analysis:

- **Heading 1**: "Divergence Analysis"
- **Heading 2**: "Where Modes Agree"
  - Robust conclusions that survive all synthesis lenses
- **Heading 2**: "Where Modes Diverge"
  - Pivot points with mode names on each side
- **Heading 2**: "The Key Choice"
  - The underlying values/priorities question -- styled as a prominent callout
- Mode comparison infographic (`INFOGRAPHIC_mode-comparison.png`) embedded

### Appendix C: Mode Sensitivity Analysis (Additional)
- **Heading 1**: "Appendix C: Mode Sensitivity Analysis"
- Mode Sensitivity rating with explanation
- Per-mode decision summary table: Mode, Decision, Determinative Perspective, Key Factor
- Analysis of what the sensitivity level means for the user's decision process

---

## Content Mapping from Decision Record

| Decision Record Section | DOCX Section | Transformation Notes |
|---|---|---|
| Header / ID / Date / Type | Cover Page | Professional cover with key metadata |
| (generated) | Table of Contents | Auto-generated from heading styles |
| Executive Summary | Section 1 | Narrative paragraph, not bullets |
| Section 1: Issue Statement | Section 2: Problem Statement | Framed with business context |
| Section 2: CEO Framing | Section 3: Analytical Framework | Routing table + infographic |
| Section 3: Domain Analyses | Section 4: Detailed Analysis | Per-domain subsections with findings tables |
| Section 4: Fault Line Analysis | Section 5: Risk & Disagreement | Infographic + structured disagreement tables |
| Section 5: CEO Decision | Section 6: Decision and Rationale | Prominent callout + full rationale |
| Section 6: Dissenting Views | Section 7: Counterarguments | Full subsections, not summarized |
| Section 7: Next Steps | Section 8: Action Plan | Infographic + owner/timeline table |
| Section 8: Metadata | Appendix A | Two-column metadata table |
| (expanded team lead data) | Appendix B | Full team lead output for deep review |

The Document Agent synthesizes the Decision Record into a formal document suitable for executive review. The language should be professional and precise -- this document may go through a formal approval workflow with comments, tracked changes, and redlining. Content is identical to the HTML and PPTX; the format serves the editing and annotation consumption context.
