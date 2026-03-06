# Advisory Document Specification (DOCX) -- Tier 1

## Purpose

The Advisory Document is the production artifact for Tier 1 Hallway Questions. It converts the Advisory Note into a lightweight, editable memo-format DOCX -- professional enough to forward to a colleague or attach to an email, but not a full board document. One to two pages maximum.

**Filename:** `{session-output}/ADVISORY_<issue-slug>.docx`
**Build script:** `{session-output}/build/build_advisory.js`

> `{session-output}` and `<issue-slug>` are provided by the orchestrator in your task description. Use them directly.

**No dependencies.** This is the only production artifact at Tier 1 -- single-task pipeline, no blocking.

---

## Supplemental Skills

Before starting implementation, review available skills for any relevant to this artifact type. Invoke applicable skills using the Skill tool to load additional guidance into your context. If no relevant skills are found, proceed — this template is self-contained and sufficient on its own.

---

## Technology

**Library:** `docx` npm package (docx-js) -- same as the board document (`board-document.md`).

The Document Agent writes a build script (`build_advisory.js`) that uses the `docx` package to generate the DOCX programmatically. The script is saved alongside the output and is rerunnable: `node build_advisory.js` regenerates the document from current data.

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
- **Primary font**: Arial
- **Title**: Arial 20pt bold
- **Heading 1**: Arial 16pt bold
- **Heading 2**: Arial 13pt bold
- **Body text**: Arial 12pt, single or 1.15 line spacing
- **Metadata table text**: Arial 10pt

### Table Formatting
Tables use DXA widths exclusively -- same conventions as `board-document.md`:
```javascript
new Table({
  rows: [/* ... */],
  width: { size: 9360, type: WidthType.DXA },  // Full content width
  columnWidths: [3120, 6240],                    // Label + value columns
});

new TableCell({
  width: { size: 3120, type: WidthType.DXA },
  shading: { type: ShadingType.CLEAR, color: "auto", fill: "F2F2F2" },
  children: [/* ... */],
});
```

### Lists
Use `LevelFormat.BULLET` numbering configuration -- same as board document:
```javascript
new Paragraph({
  text: "List item text",
  numbering: { reference: "bullet-list", level: 0 },
});
```

### Headers and Footers
```javascript
const header = new Header({
  children: [
    new Paragraph({
      children: [
        new TextRun({
          text: "Advisory Note -- [Domain]",
          font: "Arial",
          size: 16,   // 8pt
          color: "888888",
        }),
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

### 1. Header Block

Not a full cover page -- a compact header block at the top of page one.

| Element | Specification |
|---------|--------------|
| Title | "Advisory Note" -- Arial 20pt bold, left-aligned |
| Horizontal rule | Paragraph border (bottom) to separate header from metadata |
| Metadata table | 2-column DXA table (label + value), no outer borders |

**Metadata table contents:**

| Label | Value |
|-------|-------|
| Domain | [C-Suite Role] -- [Mandate Title] |
| Date | [YYYY-MM-DD HH:MM UTC] |
| Mode | [Guardian / Pioneer / Architect / Analyst / Sentinel] |
| Confidence | [High / Medium / Low] |

```javascript
// Metadata table
new Table({
  rows: [
    new TableRow({
      children: [
        new TableCell({
          width: { size: 3120, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, color: "auto", fill: "F2F2F2" },
          children: [new Paragraph({ children: [new TextRun({ text: "Domain", font: "Arial", size: 20, bold: true })] })],
        }),
        new TableCell({
          width: { size: 6240, type: WidthType.DXA },
          children: [new Paragraph({ children: [new TextRun({ text: domainValue, font: "Arial", size: 20 })] })],
        }),
      ],
    }),
    // Repeat for Date, Mode, Confidence
  ],
  width: { size: 9360, type: WidthType.DXA },
});
```

Spacing: One blank paragraph after the metadata table before the first section.

---

### 2. Question Section

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Question" -- Arial 16pt bold |
| Content | User's question reproduced verbatim in a styled indented block |

The question is displayed in an indented paragraph with a left border or light background shading to visually distinguish it from the response:

```javascript
new Paragraph({
  children: [new TextRun({ text: userQuestion, font: "Arial", size: 24, italics: true })],
  indent: { left: 720 },  // 0.5 inch indent
  border: {
    left: { style: BorderStyle.SINGLE, size: 6, color: "CCCCCC" },
  },
});
```

---

### 3. Advisory Response Section

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Advisory Response" -- Arial 16pt bold |
| Content | The 3-5 sentence advisory response as professional memo prose |
| Font | Arial 12pt, single spacing |

The response is the body of the memo -- the C-suite agent's direct, opinionated assessment formatted as one or two paragraphs. No bullet points unless the original Advisory Note used them.

---

### 4. Escalation Brief Section (Conditional)

**Include only if the C-suite agent appended an Escalation Brief to the Advisory Note.** If no Escalation Brief was produced, omit this section entirely.

| Element | Specification |
|---------|--------------|
| Heading | Heading 1: "Escalation Brief" -- Arial 16pt bold |
| Subsections | Heading 2 for each component below |

**Subsection structure:**

| Subsection | Content |
|------------|---------|
| Heading 2: "Initial Finding" | 1-2 sentence summary from the Escalation Brief |
| Heading 2: "Cross-Domain Implications" | Bullet list -- each affected domain with rationale |
| Heading 2: "Recommended Escalation" | Tier recommendation with rationale |
| Heading 2: "Recommended Routing" | Bullet list of roles to activate |
| Heading 2: "Key Context" | Bullet list of findings for the escalated analysis |

All bullet lists use `LevelFormat.BULLET` numbering configuration.

---

## Design Principles

- **Memo format, not report format** -- 1-2 pages maximum. This is a hallway answer committed to paper, not a board presentation.
- **No Table of Contents** -- the document is too short to warrant one.
- **No infographics** -- no Graphic Designer runs at Tier 1.
- **No cover page** -- the header block serves as the document identifier.
- **Same `docx` library patterns** as `board-document.md`: DXA widths, `LevelFormat.BULLET`, `ShadingType.CLEAR`, `PageNumber.CURRENT`. No `ImageRun` needed.
- **Rerunnable build script** -- `node build_advisory.js` from the `build/` directory regenerates the DOCX.
- **Conditional sections** -- the Escalation Brief section appears only when the Advisory Note includes one. The build script checks for its presence and omits the section cleanly if absent.

---

## Formatting Requirements Summary

| Element | Specification |
|---------|--------------|
| Page size | US Letter: 12,240 x 15,840 DXA |
| Margins | 1 inch all sides (1,440 DXA) |
| Font family | Arial |
| Title | 20pt bold |
| Heading 1 | 16pt bold |
| Heading 2 | 13pt bold |
| Body text | 12pt |
| Metadata table | 10pt labels, DXA widths, shaded label cells |
| Lists | LevelFormat.BULLET, never unicode bullets |
| Table widths | DXA only (WidthType.DXA), never percentage |
| Table shading | ShadingType.CLEAR |
| Headers | "Advisory Note -- [Domain]" right-aligned, 8pt gray |
| Footers | Page number centered (PageNumber.CURRENT) |
| Max length | 1-2 pages |

---

## Content Mapping from Advisory Note

| Advisory Note Section | DOCX Section | Transformation Notes |
|---|---|---|
| Header (Domain, Date, Mode) | Header Block metadata table | Structured into labeled table rows |
| Question line | Section 2: Question | Styled as indented callout |
| Advisory response (3-5 sentences) | Section 3: Advisory Response | Professional memo prose |
| Confidence line | Header Block metadata table | Added as fourth metadata row |
| Escalation Brief (if present) | Section 4: Escalation Brief | Structured with subsection headings |

The Advisory Document Agent formats the Advisory Note into the memo structure. The language remains as written by the C-suite agent -- the Document Agent formats, it does not rewrite.
