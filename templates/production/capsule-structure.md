# Deliberation Capsule PDF Specification

## Purpose

The **Deliberation Capsule PDF** is a comprehensive, layered archive of the **entire** deliberation process. Unlike the other four artifacts (which present only the synthesized decision briefing), the Capsule contains the full analytical record: every domain analysis, every team lead finding, the CEO's routing rationale, Phase 4.5 pre-mortem responses, and the original issue submission.

> **Note:** The Results PDF is produced separately by the permanent script `scripts/build_results_pdf.py` (native reportlab generation from RECORD.md). This file specifies only the Capsule PDF.

**Capsule PDF filename:** `{session-output}/CAPSULE_<issue-slug>.pdf`
**Build script:** `{session-output}/build/build_capsule.py`

> `{session-output}` and `<issue-slug>` are provided by the CCO in your prompt. Use them directly.

**Runs in Wave 4.** The Capsule PDF is produced after all other artifacts are complete.

---

## Supplemental Skills

Before starting implementation, review available skills for any relevant to this artifact type. Invoke applicable skills using the Skill tool to load additional guidance into your context. If no relevant skills are found, proceed — this template is self-contained and sufficient on its own.

---

## Technology

**Primary:** Python build script using `weasyprint` for HTML-to-PDF rendering.
**Fallback:** `pdfkit` with `wkhtmltopdf` if weasyprint is unavailable.

The Publisher writes a build script (`build_capsule.py`) that produces the Capsule PDF. The script is rerunnable: `python3 build_capsule.py` from the `build/` directory regenerates from current artifacts.

> **Results PDF** is handled separately by the permanent script `scripts/build_results_pdf.py` using reportlab. The build_capsule.py script does **not** produce the Results PDF.

```python
# build_capsule.py structure
import weasyprint
import os

OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def build_capsule_pdf():
    """Build the layered deliberation archive."""
    # 1. Generate capsule HTML (Cover + 5 layers)
    # 2. Apply capsule-specific styling
    # 3. Render to PDF via weasyprint

if __name__ == '__main__':
    build_capsule_pdf()
```

---

## Deliberation Capsule PDF

### Design Principles

- **"The capsule is the frame. The content is the art."** -- Deliberately neutral design (consistent typography, clean layout, clear section dividers). The decision content carries its own analytical voice; the capsule provides structure without interpretation.

- **Temperature-neutral** -- The capsule presents what happened with structural clarity, not interpretive spin. No editorial commentary beyond section labels and navigation aids.

- **Plain-language layer names** -- "Decision", "Analysis", "Process", "Context" -- not jargon or system terminology.

- **Dual-audience Overview** -- Layer 1 is readable by a human scanning for content AND parseable by an AI agent looking for structured metadata. Use consistent formatting that serves both audiences.

- **Handle variable content gracefully** -- Tier 2 runs have less content than Tier 3 full cascades. Some runs activate 3 C-suite domains, others activate all 7+. The layout accommodates variability without breaking or looking sparse. Use conditional sections that appear only when content exists.

### Structure: Cover + 5 Layers

#### Cover Page
**Content source:** Decision Record header

| Element | Specification |
|---------|--------------|
| Issue title | Large, prominent (28-32pt), centered |
| Decision statement | The CEO's decision in 1-2 sentences |
| Decision Mode | Mode name and brief description |
| Date | Full timestamp |
| Tier | "Tier 2 -- Working Session" or "Tier 3 -- Board Meeting" |
| Decision Type | Classification badge |
| Key infographic | Routing diagram thumbnail (`INFOGRAPHIC_routing-diagram.png`) at reduced size |
| Decision ID | For reference tracking |
| Page footer | "Deliberation Capsule -- Comprehensive Archive" |

---

#### Layer 1: Overview
**Content source:** Generated from all capsule contents

**Purpose:** Table of contents with page references and a content inventory listing every artifact included with type and source. Structured for both human scanning and AI agent parsing.

| Element | Specification |
|---------|--------------|
| Layer heading | "Layer 1: Overview" |
| Table of contents | Hierarchical listing of all layers and subsections with page numbers |
| Content inventory | Structured table listing every item in the capsule |

**Content Inventory Format:**
```
CONTENT INVENTORY

| Item | Type | Layer | Source |
|------|------|-------|--------|
| Executive Summary | Narrative | Layer 2 | Decision Record |
| Issue Statement | Verbatim | Layer 2 | Decision Record Sec. 1 |
| CEO Framing | Analysis | Layer 2 | Decision Record Sec. 2 |
| [C-Suite Role] Domain Analysis | Analysis | Layer 3 | Domain Analysis Data |
| [Team Lead] Findings | Analysis | Layer 3 | Team Lead Output |
| Routing Diagram | Infographic | Layer 3 | Graphic Designer |
| Domain Scorecard | Infographic | Layer 3 | Graphic Designer |
| Fault Line Map | Infographic | Layer 3 | Graphic Designer |
| Risk-Opportunity Matrix | Infographic | Layer 3 | Graphic Designer |
| Action Plan Timeline | Infographic | Layer 3 | Graphic Designer |
| CEO Routing Rationale | Process | Layer 4 | CEO Framing Data |
| Phase 4.5 Pre-Mortem Responses | Process | Layer 4 | Pre-Mortem Data |
| Original Issue Submission | Context | Layer 5 | User Input |
| Company Profile Configuration | Context | Layer 5 | Config File |
| Routing Table Configuration | Context | Layer 5 | Config File |
```

The content inventory should be machine-parseable: consistent column structure, no merged cells, predictable type labels.

---

#### Layer 2: Decision
**Content source:** Decision Record (synthesized briefing)

**Purpose:** The complete synthesized decision briefing in full. A reader who only reads Layer 2 gets the full decision story.

| Section | Content | Source |
|---------|---------|--------|
| Executive Summary | 3-5 sentence decision summary | DR Executive Summary |
| Issue Statement | The question as originally posed | DR Section 1 |
| CEO Framing | Evaluation dimensions, activation rationale | DR Section 2 |
| Decision with Rationale | Decision statement, determinative perspective, weight rationale | DR Section 5 |
| Conditions & Guardrails | Non-negotiable prerequisites | DR Section 5 |
| Dissenting Views | Strongest objections with full reasoning | DR Section 6 |
| Next Steps | Actions, owners, timelines | DR Section 7 |
| Decision Review Triggers | Conditions for revisitation | DR Section 7 |
| Metadata | Full metadata block | DR Section 8 |

Formatting: Narrative style with clear headings. Each subsection starts on a clear boundary. The decision statement should be visually prominent (larger text, bordered container, or shaded background).

---

#### Layer 3: Analysis
**Content source:** Domain analysis data, infographic images

**Purpose:** Full domain analyses at complete detail. Every C-suite domain analysis at full depth, every team lead finding unabridged, all infographic images at readable size. This is the analytical evidence base -- what Layer 2 summarizes, Layer 3 presents in full.

| Section | Content | Source |
|---------|---------|--------|
| Domain Scorecard Overview | `INFOGRAPHIC_domain-scorecard.png` at full size | Graphic Designer |
| Per-Domain Analysis | One major section per activated C-suite domain | DR Section 3 |
| -- Domain Recommendation | Approve/Oppose/Conditions/Neutral + confidence | C-Suite synthesis |
| -- Domain Summary | Full synthesis narrative | C-Suite synthesis |
| -- Team Lead Findings | **Every team lead finding, not summarized** | Team Lead outputs |
| -- -- [Team Lead Name] | Full analytical output including framework-specific artifacts | Per team lead |
| -- Key Risks | Complete risk inventory with severity | C-Suite synthesis |
| -- Key Opportunities | Complete opportunity inventory with impact | C-Suite synthesis |
| -- Internal Contradictions | Where team leads within this domain disagreed | C-Suite synthesis |
| Fault Line Analysis | Full fault line analysis | DR Section 4 |
| -- Fault Line Map | `INFOGRAPHIC_fault-lines.png` at full size | Graphic Designer |
| -- Points of Agreement | Complete listing | DR Section 4 |
| -- Points of Contention | Complete listing with domain attribution | DR Section 4 |
| -- Pre-Mortem Findings | All Phase 4.5 failure modes | DR Section 4 |
| -- Unresolved Tensions | Complete listing | DR Section 4 |
| Risk-Opportunity Matrix | `INFOGRAPHIC_risk-matrix.png` at full size | Graphic Designer |

**Key difference from Layer 2:** Layer 2 presents domain analyses as summaries. Layer 3 presents the **complete team lead output** for every activated team lead -- the full analytical framework output including scenario models, compliance assessments, stress tests, etc. Nothing is summarized or abbreviated.

---

#### Layer 4: Process
**Content source:** Process artifacts, CEO framing data, pre-mortem data

**Purpose:** How the deliberation was conducted. The CEO's reasoning about framing and routing, the activation and exclusion decisions, the Phase 4.5 pre-mortem challenge responses, and the mode selection rationale. A reader of Layer 4 can reconstruct WHY the deliberation took the shape it did.

| Section | Content | Source |
|---------|---------|--------|
| CEO Framing Rationale | Full CEO framing narrative: how the issue was interpreted, what dimensions were identified, why | CEO Phase 1 output |
| Routing Decisions | Decision type classification reasoning | CEO Phase 1 output |
| Activation Reasoning | Per-role: why each activated domain was included | CEO Phase 1 output |
| Exclusion Reasoning | Per-role: why each excluded domain was not activated | CEO Phase 1 output |
| Full-Activation Assessment | Threshold condition evaluation (irreversibility, headcount, market position, financial risk, uncertainty) | CEO Phase 1 output |
| CSO Research Directive | If applicable: what the CEO directed the CSO to investigate and why | CEO Phase 1 output |
| CSO Research Dossier | If applicable: full research dossier including evidence summary, assumption registry, evidence quality grade | CSO Phase 1.5 output |
| Phase 4.5 Pre-Mortem Responses | **Each C-suite member's individual failure mode analysis** | Phase 4.5 output |
| -- [C-Suite Role] Pre-Mortem | "Assume this decision fails. What caused the failure?" -- full response | Per C-suite agent |
| Decision Mode Selection | Which mode was applied and why | CEO Phase 5 configuration |
| Mode Prompt Modifier | The actual prompt modifier text applied to CEO synthesis | Config |

---

#### Layer 5: Context
**Content source:** User input, config files

**Purpose:** The raw inputs and configuration context. Everything needed to reproduce or understand the deliberation's starting conditions.

| Section | Content | Source |
|---------|---------|--------|
| Original Issue | The issue as submitted by the user, verbatim | User input |
| Reference Materials | Any additional context or documents the user provided | User input |
| Company Profile | The company profile configuration used for this analysis | `config/company-profile.md` active profile |
| -- Archetype | Which preset was active |  |
| -- Overrides | Any user customizations |  |
| -- Compliance Frameworks | Active compliance focus areas |  |
| Routing Table | The routing table configuration used | `config/routing-table.md` |
| -- Default Activation Rules | Decision type -> default C-suite activation | |
| -- Full-Activation Thresholds | The five threshold conditions | |
| -- CSO Activation Patterns | CSO activation guidance by decision type | |
| Decision Mode Configuration | All five mode definitions and prompt modifiers | `config/decision-modes.md` |
| Invocation Details | Exact invocation command, any flags, user-specified parameters | Session data |

---

## Multi-Mode Capsule Variant

When the source is a Comparative Decision Record:

### Layer 2 Additions
- **All mode syntheses**: Each mode's decision, determinative perspective, key factor, conditions, and accepted risks presented in parallel
- **Divergence Analysis**: Where modes agree, where they diverge, and The Key Choice
- **Mode Sensitivity**: Rating and detailed explanation

### Layer 4 Additions
- **Mode Selection Rationale**: Why multi-mode comparison was chosen (or if all-modes was invoked, note that)
- **Per-Mode CEO Synthesis Process**: How the same domain analysis was processed through each mode's prompt modifier
- **Mode Sensitivity Analysis**: Detailed analysis of how sensitive the decision is to synthesis posture -- which aspects are robust across modes and which depend on risk appetite
- **Mode comparison infographic**: `INFOGRAPHIC_mode-comparison.png` embedded

---

## Capsule PDF Styling

### Typography
- Body: 11pt serif font (e.g., Georgia or system serif) for readability in long-form reading
- Headings: Sans-serif (Arial or system sans) for clear hierarchy
- Layer headings: 24pt bold, with a horizontal rule below
- Section headings within layers: 16pt bold
- Subsection headings: 13pt bold

### Layout
- US Letter or A4 (detect system preference, default to Letter)
- 0.75-inch margins
- Single-column layout throughout
- Clear layer transitions: full-page divider between layers with layer number and name
- Running header: "Deliberation Capsule -- [Issue Title]"
- Running footer: "Layer N: [Layer Name]" on left, page number on right

### Color
- **Deliberately neutral**: No domain-specific color theming. The capsule is the frame, not the art.
- Primary text: dark gray (#333333) on white
- Headings: black (#000000)
- Layer divider pages: light gray background (#F5F5F5) with black text
- Infographic images provide the only color -- they carry the analytical visualization

### Tables
- Clean borders, alternating row shading (white / #F9F9F9)
- Header row: bold, light gray background (#E8E8E8)
- Consistent column widths within similar table types

### Images
- All infographic images embedded at readable size (minimum 5 inches wide)
- Alt text included for accessibility
- Captions below each image: "Figure N: [Description]"

---

## Build Script Requirements

The `build_capsule.py` script must:

1. **Produce the Capsule PDF** (the Results PDF is produced by `scripts/build_results_pdf.py`)
2. **Be rerunnable**: Running `python3 build_capsule.py` from the `build/` directory regenerates the Capsule PDF from current artifacts without side effects
3. **Handle missing content gracefully**: If a Tier 2 run has fewer domain analyses or no pre-mortem data, the capsule should omit those sections cleanly rather than showing empty sections or breaking
4. **Convert all images to base64**: For complete self-containment
5. **Report output**: Print the filename and size of the Capsule PDF on completion
6. **Fallback gracefully**: If weasyprint is unavailable, attempt pdfkit/wkhtmltopdf with a clear warning about potential rendering differences

```python
#!/usr/bin/env python3
"""
Build Deliberation Capsule PDF.

Usage: python3 build_capsule.py
Run from the build/ directory. Reads artifacts from the parent directory.
Outputs to the parent directory.

Note: Results PDF is produced separately by scripts/build_results_pdf.py

Requires: weasyprint (preferred) or pdfkit + wkhtmltopdf (fallback)
"""

import os
import sys
import base64
import re

OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import weasyprint
    PDF_ENGINE = 'weasyprint'
except ImportError:
    try:
        import pdfkit
        PDF_ENGINE = 'pdfkit'
        print("WARNING: Using pdfkit fallback. Install weasyprint for best results.")
    except ImportError:
        print("ERROR: Neither weasyprint nor pdfkit available.")
        sys.exit(1)

# ... implementation ...
```

---

## Quality Criteria

1. **The Capsule must be a complete institutional record.** A reader with no prior context should be able to reconstruct the entire deliberation from the Capsule alone: the issue, the framing, the analyses, the disagreements, the decision, and the reasoning.

2. **Layer boundaries must be clear.** Each layer serves a distinct purpose (Decision, Analysis, Process, Context) and a reader should be able to navigate directly to any layer.

3. **The Overview (Layer 1) must be dual-audience.** A human scanning for "where is the CSO research?" and an AI agent looking for structured metadata should both find what they need in the content inventory.

4. **Variable content must be handled gracefully.** A capsule from a Tier 2 run with 3 domains should look intentional, not incomplete. A capsule from a Tier 3 full cascade with all 8 domains and CSO research should not overflow or break layout.

5. **The Results PDF must faithfully present the decision briefing.** Generated natively from RECORD.md via `scripts/build_results_pdf.py` (reportlab), with proper page break control, embedded infographics, and no content clipping. The Results PDF and HTML page are sibling artifacts — both built from RECORD.md using the same content mapping, optimized for their respective media (print vs. screen).
