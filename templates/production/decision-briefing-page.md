# Decision Briefing Page Specification (HTML)

## Purpose

The interactive decision briefing page is the **primary distribution artifact** -- the designed, definitive rendering of the decision briefing. This is the artifact people will actually use day-to-day: browsing, sharing, reviewing. It must feel like a designed product, not a document dump.

**Filename:** `{session-output}/index.html`

> `{session-output}` and `<issue-slug>` are provided by the CEO in your task description. Use them directly.

**Blocked until:** Image Agent (Task A), Presentation Agent (Task B), AND Document Agent (Task C) complete. The page needs infographic images from Task A and download links to PPTX (Task B) and DOCX (Task C).

---

## Technology Constraints

- **Self-contained**: Everything in one HTML file -- CSS and JS inline. No external stylesheets, no external scripts.
- **No external dependencies**: No CDN links, no frameworks (no Bootstrap, no Tailwind, no React). Vanilla HTML, CSS, and JavaScript only.
- **Works from `file://` protocol**: Must open correctly when double-clicked from the filesystem. No server required. All asset references use relative paths.
- **Responsive**: Readable on desktop, tablet, and mobile screen sizes.
- **PDF-compatible**: Design patterns must work when rendered to PDF by the Archivist (see PDF Compatibility section below).

---

## Page Structure

### 1. Hero Section
**Content source:** Decision Record header + Executive Summary

- Issue title (large, prominent)
- Decision type badge (color-coded: Strategic/blue, Operational/green, Financial/amber, Technical/purple, Personnel/teal, Compliance/red)
- Tier indicator (Tier 2 Working Session or Tier 3 Board Meeting)
- Decision Mode badge
- Date
- **Decision callout**: The conclusion displayed prominently upfront in a visually distinct container. 1-2 sentences showing the decision itself. The reader should know the outcome before scrolling.
- Key takeaway: The executive summary's opening sentence, styled as a pull quote.

### 2. Executive Summary
**Content source:** Decision Record Executive Summary

- Full 3-5 sentence summary
- The decision, reasoning, and primary dissent presented as flowing narrative
- Styled as a distinct section with slightly larger body text for emphasis

### 3. Problem Context
**Content source:** Decision Record Section 1 (Issue Statement) + Section 2 (CEO Framing, partial)

- The issue as originally posed
- Business background and why this decision matters
- Context that frames the analytical work that follows

### 4. Analytical Framework
**Content source:** Decision Record Section 2 (CEO Framing)

- How the issue was decomposed: evaluation dimensions
- **Routing diagram infographic** (`images/INFOGRAPHIC_routing-diagram.png`): embedded, showing which domains were activated and why, which were excluded
- Activated vs. excluded teams with rationale (can be a styled table or structured layout)
- Full-activation threshold assessment (if triggered)
- CSO research activation status

### 5. Domain Analysis Cards
**Content source:** Decision Record Section 3 (Domain Analyses)

- One visual card per activated C-suite domain
- Each card contains:
  - Domain title and mandate
  - **Recommendation badge**: Color-coded (green = Approve, amber = Approve with Conditions, red = Oppose, gray = Neutral)
  - **Confidence level indicator**: Visual (e.g., filled circles, progress bar)
  - Synthesis summary (2-3 sentences)
  - **Expandable team lead detail**: Click/tap to expand detailed team lead findings. Collapsed by default to keep the page scannable.
  - Key risks (styled as warning callouts)
  - Key opportunities (styled as positive callouts)
- **Domain scorecard infographic** (`images/INFOGRAPHIC_domain-scorecard.png`): Embedded in this section, showing the recommendation/confidence matrix across all domains at a glance
- Cards laid out in a responsive grid (2 columns on desktop, 1 on mobile)

### 6. Fault Line Visualization
**Content source:** Decision Record Section 4 (Fault Line Analysis)

- **The most valuable analytical section -- given maximum visual prominence**
- **Fault line map infographic** (`images/INFOGRAPHIC_fault-lines.png`): Prominently displayed
- Points of Agreement: styled as connected/aligned elements
- Points of Contention: styled as opposing/divergent elements with the domains on each side clearly identified
- Pre-mortem failure modes: presented in distinct callout boxes, each attributed to the C-suite member who identified it
- Unresolved tensions: styled differently from resolved contentions (e.g., dashed borders, muted colors) to signal "open questions"

### 7. The Decision
**Content source:** Decision Record Section 5 (CEO Decision)

- **Prominent decision callout**: The decision statement in a visually dominant container (larger text, distinct background, clear framing)
- Most determinative perspective: Highlighted with explanation
- Decision weight rationale: How perspectives were weighed
- Conditions and guardrails: Styled as a checklist or requirement list, each linked to the domain concern it addresses
- **Risk-opportunity matrix infographic** (`images/INFOGRAPHIC_risk-matrix.png`): Embedded in this section
- Accepted risks with reasoning
- Mitigations directed

### 8. Dissenting Views
**Content source:** Decision Record Section 6 (Dissenting Views)

- **Given visible placement -- NOT buried at the bottom or hidden in a collapsible**
- Each dissenting view presented in a sidebar or callout element with:
  - The dissenting role and their recommendation
  - The core objection with full reasoning
  - The risk if ignored
  - The CEO's response to the objection
- Visual treatment signals "this was heard and weighed" not "this was dismissed"

### 9. Action Plan
**Content source:** Decision Record Section 7 (Next Steps)

- **Action plan timeline infographic** (`images/INFOGRAPHIC_action-plan.png`): Gantt-style visualization
- Structured action items with owners, timelines, and priority levels
- Decision review triggers: conditions under which this decision should be revisited

### 10. Download Section
**Content source:** Production artifacts

- Links to downloadable artifacts via relative paths:
  - `PRESENTATION_<issue-slug>.pptx` -- "Download Board Presentation"
  - `REPORT_<issue-slug>.docx` -- "Download Board Document"
- Clean download buttons or card layout
- Brief description of each artifact's purpose (presenting, editing/annotating)

### 11. Metadata
**Content source:** Decision Record Section 8 (Metadata)

- Decision classification, complexity, dissent level
- Decision Mode used
- Total roles consulted
- Key assumptions
- Company profile archetype
- Footer/sidebar treatment -- present but not visually dominant

### 12. Navigation
- **Sticky navigation bar** (top or side) with smooth-scroll links to each section
- Table of contents visible on desktop, hamburger menu on mobile
- "Back to top" button
- Current-section indicator in the nav

---

## Design Principles

### Typography
- Professional font stack: system fonts (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`) for body, with a serif option for headings if desired
- Body text: 16-18px, comfortable line height (1.6-1.7)
- Headings: clear hierarchy with size and weight differentiation
- Pull quotes and callouts: distinct styling for decision callouts, dissent callouts

### Color Palette
- Content-informed, not generic. The color palette should reflect the decision domain:
  - Financial decisions: deep blues and greens (trust, stability)
  - Technical decisions: purples and teals (innovation, precision)
  - Strategic decisions: navy and gold (authority, ambition)
  - Compliance/Risk decisions: deep red and slate (urgency, gravity)
- Recommendation badge colors are fixed: green (Approve), amber (Conditions), red (Oppose), gray (Neutral)
- Dark background for hero section, light backgrounds for content sections
- Sufficient contrast ratios for accessibility (WCAG AA minimum)

### Layout
- Max content width: 900-1000px, centered
- Generous whitespace between sections
- Card-based layout for domain analyses
- Grid layout that adapts from 2 columns to 1 column on narrow screens
- Section dividers that create visual rhythm without clutter

### Interactivity
- Smooth-scroll navigation
- Expandable/collapsible team lead detail sections (JS toggle)
- Scroll-triggered section reveals (subtle opacity/transform animations)
- No framework dependencies -- vanilla JS event listeners

---

## PDF Compatibility Requirements

The Archivist renders this page to PDF via weasyprint. The following patterns ensure PDF output is clean:

1. **Scroll-reveal animations**: Use class-based patterns (`.reveal` with `opacity: 0`, JS adds `.visible` class on scroll). The Archivist injects print CSS: `.reveal { opacity: 1 !important; transform: none !important; }` to neutralize these.

2. **`backdrop-filter`**: Not supported in weasyprint. Use solid fallback backgrounds for any frosted-glass effects:
   ```css
   .glass-panel {
     background: rgba(255, 255, 255, 0.95); /* fallback */
     backdrop-filter: blur(10px); /* enhancement for browsers */
   }
   ```

3. **CSS custom properties**: Supported and encouraged. Use `var(--name)` for the color palette to enable easy theme adjustment.

4. **Fixed-position elements**: The sticky nav bar will be hidden in PDF. Use `@media print { .nav { display: none; } }` and the Archivist will also strip it.

5. **Viewport units**: Avoid `vh`/`vw` for critical sizing. Use `rem`, `em`, or `px` for content dimensions.

6. **Page breaks**: Add `page-break-before: always` hints on major section boundaries for clean PDF pagination:
   ```css
   @media print {
     .section { page-break-before: always; }
     .section:first-child { page-break-before: avoid; }
   }
   ```

7. **Image sizing**: Infographic images should have explicit `width` and `height` attributes or CSS dimensions, not rely on `max-width: 100%` alone.

8. **Script blocks**: The Archivist strips all `<script>` blocks before PDF rendering. All critical content must be in the HTML/CSS, not JS-generated.

---

## Multi-Mode Variant

When the source is a Comparative Decision Record (multi-mode comparison), the page structure adapts:

### Hero Section Changes
- Per-mode decision summary cards replacing the single decision callout
- Mode Sensitivity indicator (visual gauge or spectrum)
- List of modes compared

### Domain Analysis Section
- Presented once (shared analysis) -- identical to single-mode

### After "The Decision" Section, Add:

#### Mode Comparisons Section
- **Tabbed interface** or **side-by-side panels** (depending on number of modes)
  - 2 modes: side-by-side layout
  - 3-5 modes: tabbed interface with one tab per mode
- Each mode panel shows:
  - Decision statement
  - Most determinative perspective
  - Key factor that tipped this mode
  - Conditions and guardrails
  - Accepted risks

#### Divergence Analysis Section
- **Mode comparison infographic** (`images/INFOGRAPHIC_mode-comparison.png`): Divergence tree
- Where modes agree (robust conclusions)
- Where modes diverge (pivot points)
- The Key Choice: the underlying values/priorities question

### Metadata Section Changes
- Mode Sensitivity rating with expanded explanation
- All modes listed with individual decisions for quick reference

---

## HTML Structure Reference

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Decision Briefing: [Issue Title]</title>
  <style>
    /* All CSS inline -- see Design Principles */
    :root {
      --color-primary: /* domain-appropriate */;
      --color-accent: /* domain-appropriate */;
      --color-approve: #2d8a4e;
      --color-conditions: #d4a017;
      --color-oppose: #c0392b;
      --color-neutral: #7f8c8d;
      --color-bg: #ffffff;
      --color-bg-dark: #1a1a2e;
      --color-text: #2c3e50;
      --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-heading: Georgia, 'Times New Roman', serif;
      --content-width: 960px;
    }
    /* ... full stylesheet ... */
    @media print {
      .nav, .back-to-top { display: none; }
      .reveal { opacity: 1 !important; transform: none !important; }
      .section { page-break-before: always; }
      .section:first-child { page-break-before: avoid; }
      .expandable-content { display: block !important; }
    }
  </style>
</head>
<body>
  <nav class="nav"><!-- Sticky navigation --></nav>

  <section id="hero" class="hero"><!-- Hero section --></section>
  <section id="summary" class="section"><!-- Executive Summary --></section>
  <section id="context" class="section"><!-- Problem Context --></section>
  <section id="framework" class="section"><!-- Analytical Framework --></section>
  <section id="analysis" class="section"><!-- Domain Analysis Cards --></section>
  <section id="fault-lines" class="section"><!-- Fault Line Visualization --></section>
  <section id="decision" class="section"><!-- The Decision --></section>
  <section id="dissent" class="section"><!-- Dissenting Views --></section>
  <section id="action" class="section"><!-- Action Plan --></section>
  <section id="downloads" class="section"><!-- Download Section --></section>
  <footer id="metadata" class="section"><!-- Metadata --></footer>

  <button class="back-to-top"><!-- Back to top --></button>

  <script>
    /* All JS inline -- smooth scroll, section reveals, expandable sections */
  </script>
</body>
</html>
```

---

## Content Mapping from Decision Record

| Decision Record Section | Page Section | Transformation |
|---|---|---|
| Executive Summary | Hero + Executive Summary | Split: decision callout in Hero, full summary in next section |
| Section 1: Issue Statement | Problem Context | Framed with business background narrative |
| Section 2: CEO Framing | Analytical Framework | Routing diagram infographic + structured layout |
| Section 3: Domain Analyses | Domain Analysis Cards | Card layout with expandable team lead detail |
| Section 4: Fault Line Analysis | Fault Line Visualization | Visual prominence, infographic, callout boxes |
| Section 5: CEO Decision | The Decision | Prominent callout + risk matrix infographic |
| Section 6: Dissenting Views | Dissenting Views | Sidebar/callout elements, visible placement |
| Section 7: Next Steps | Action Plan | Timeline infographic + structured table |
| Section 8: Metadata | Metadata footer | Footer/sidebar treatment |

The Web Page Agent synthesizes the Decision Record into a narrative briefing -- not a formatted transcription. Section headings, content flow, and language should feel like a designed report, not a form output.
