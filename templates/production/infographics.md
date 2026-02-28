# Infographic Specifications (Image Agent -- Task A)

## Purpose

The Image Agent generates 5-6 analytical infographics that visualize
the key analytical artifacts from the Decision Record. These infographics
are embedded in the HTML briefing page, the PPTX presentation, and the
DOCX report -- providing visual summaries that make complex multi-domain
analysis scannable.

**Output directory:** `{session-output}/images/`
**Filename pattern:** `INFOGRAPHIC_<type-slug>.png`

> `{session-output}` and `<issue-slug>` are provided by the CEO in your
> task description. Use them directly.

**Runs in parallel** with Presentation Agent (Task B) and Document Agent
(Task C) -- no dependencies on other production agents.

---

## Technology

**Target platform:** Browser automation targeting `gemini.google.com`
**Required model mode:** Pro (select via the mode picker in the Gemini
input bar -- Fast mode may not generate images or may produce lower
structural fidelity)
**Prompt format:** JSON templates following the Pauhu schema hybrid
convention with six top-level keys: `core`, `style`, `technical`,
`composition`, `quality_keywords`, `extras`
**Template directory:** `templates/infographic-prompts/`

### Prompt Population Workflow

For each infographic, follow this 5-step workflow:

1. **Load template** -- Read the JSON template from
   `templates/infographic-prompts/<type-slug>.json`
2. **Extract data** -- Pull the required data from the Decision Record
   sections identified in the Content Mapping table below
3. **Populate placeholders** -- Replace all `{{PLACEHOLDER}}` tokens in
   the template with extracted Decision Record data
4. **Apply style overrides** -- If `.cdp-context/style.md` exists, read
   it and override the corresponding JSON values using the mapping table
   below
5. **Submit to Gemini** -- Send the populated JSON as the image generation
   prompt via browser automation

### Style Configuration Integration

| `.cdp-context/style.md` Section | JSON Key Overridden |
|----------------------------------|---------------------|
| Visual Style: primary_style | `style.primary_style` |
| Visual Style: render_quality | `style.render_quality` |
| Visual Style: lighting | `style.lighting` |
| Visual Style: color_profile | `style.color_profile` |
| Brand Colors | `extras.color_mapping` (all templates) |
| Color Overrides | `extras.color_mapping` (per-template) |
| Composition: perspective | `composition.perspective` |
| Composition: framing | `composition.framing` |
| Quality Control: include | `quality_keywords.include` |
| Quality Control: avoid | `quality_keywords.avoid` |

---

## Attempt Budget

**Hard limits -- these are not suggestions. Do not exceed them.**

- **Per-infographic limit:** 3 total Gemini submissions maximum.
  - **Attempt 1:** Submit the fully populated JSON prompt.
  - **Attempt 2:** Send corrective feedback in the **SAME** conversation.
  - **Attempt 3:** Send a simplified prompt (reduce `extras.data` to essential
    fields only) in the **SAME** conversation.
  - **After attempt 3:** STOP. Generate a placeholder. Move to the next
    infographic.
- **Session-wide limit:** 12 total Gemini submissions across all infographics
  in a single session. If this limit is reached, generate placeholders (with
  saved prompt files) for all remaining infographics immediately.
- **Conversation rule:** Retries NEVER open a new Gemini conversation. A new
  conversation is opened ONLY when moving to the next infographic.
- **Tracking instruction:** Before each submission, state:
  `"Infographic [N] of [total], attempt [X] of 3, session total [Y] of 12."`

---

## Browser Automation Workflow

For each infographic, execute this 8-step cycle:

1. **Navigate** -- Open `gemini.google.com` in a new conversation
2. **Select mode** -- Ensure the model mode picker (bottom of input
   bar) is set to **Pro**. Fast mode may not generate images from
   JSON prompts.
3. **Submit prompt** -- Paste the populated JSON prompt and request
   image generation
4. **Wait for generation** -- Allow Gemini to process and produce the
   image (monitor for completion indicators)
5. **Inspect output** -- Verify the generated image against these 5
   quality criteria:
   - Text is legible at 6.5 inch print width
   - No decorative or extraneous visual elements
   - Background is white or transparent
   - Color mapping matches the template specification
   - All data elements from the prompt are represented
6. **Iterate if needed** -- If any quality criterion fails, follow this
   decision tree:
   - **Attempt 1 failed:** Send corrective feedback describing the specific
     failures in the **SAME** conversation (this is attempt 2). Do NOT open
     a new Gemini conversation.
   - **Attempt 2 failed:** Send a simplified prompt -- reduce `extras.data`
     to essential fields only -- in the **SAME** conversation (this is
     attempt 3). Do NOT open a new Gemini conversation.
   - **Attempt 3 failed:** STOP. Do NOT submit again. Proceed to step 7
     for placeholder generation.
7. **Download or placeholder** -- If an attempt produced an acceptable
   image, save it as
   `{session-output}/images/INFOGRAPHIC_<type-slug>.png`.
   If all 3 attempts failed:
   1. Generate a placeholder PNG (white background, centered text:
      `"[Infographic type] -- generation failed. See
      INFOGRAPHIC_<type-slug>_PROMPT.json to generate manually."`) and
      save it at `{session-output}/images/INFOGRAPHIC_<type-slug>.png`.
   2. Save the fully populated JSON prompt (the final version submitted
      to Gemini) to
      `{session-output}/images/INFOGRAPHIC_<type-slug>_PROMPT.json` so
      the user can paste it into Gemini manually.
   A PNG file must exist at the standard path regardless of outcome so
   downstream agents (Tasks B, C, D) are never blocked.
8. **New conversation for next infographic only** -- Start a fresh Gemini
   conversation for the next infographic to avoid context contamination.
   This step applies only when moving between infographics. Retries within
   the same infographic never trigger this step -- they stay in the same
   conversation.

---

## Infographic Specifications

### 1. Routing Diagram

**Filename:** `INFOGRAPHIC_routing-diagram.png`
**Template:** `templates/infographic-prompts/routing-diagram.json`
**Content source:** Decision Record Section 2 (CEO Framing)

**Visualizes:** Which C-suite executives were activated for this decision
and why, showing the routing logic from decision type classification
through activation and exclusion reasoning.

**Required data elements:**
- Activated C-suite roles with disposition type (skeptic / advocate /
  systemic / investigative / synthesizer)
- Excluded C-suite roles with exclusion rationale
- Decision type classification (primary and secondary)
- Full-activation threshold assessment
- CSO activation status

**Layout:** Overhead perspective, centered. CEO at top with connection
lines to activated roles below. Excluded roles shown as dimmed/grayed
nodes. Disposition types color-coded per `extras.color_mapping`.

**Constraints:** Text legible at 6.5 inch print width. No decorative
elements. White or transparent background.

### 2. Domain Scorecard

**Filename:** `INFOGRAPHIC_domain-scorecard.png`
**Template:** `templates/infographic-prompts/domain-scorecard.json`
**Content source:** Decision Record Section 4 (Domain Analyses)

**Visualizes:** The recommendation and confidence matrix across all
activated domains -- a consolidated view of where each domain stands.

**Required data elements:**
- Per-domain recommendation (approve / approve with conditions / oppose /
  neutral)
- Per-domain confidence level (high / medium / low)
- Key risk per domain
- Key opportunity per domain
- Internal contradictions within any domain

**Layout:** Natural human vision perspective, centered. Matrix or card
layout with one row or card per domain. Recommendations and confidence
levels color-coded per `extras.color_mapping`.

**Constraints:** Text legible at 6.5 inch print width. No decorative
elements. White or transparent background.

### 3. Fault Line Map

**Filename:** `INFOGRAPHIC_fault-lines.png`
**Template:** `templates/infographic-prompts/fault-line-map.json`
**Content source:** Decision Record Section 5 (Fault Line Analysis)

**Visualizes:** Where domain recommendations agree and where they
diverge, showing the contention lines that define the decision landscape.

**Required data elements:**
- Points of agreement (consensus findings)
- Points of contention with domains on each side
- Whether each contention is factual or values-based
- Unresolved tensions
- Pre-mortem failure modes (Tier 3 only)

**Layout:** Overhead perspective, centered. Agreement areas shown as
connected zones in green. Contention lines shown as fault lines with
domains positioned on opposing sides. Pre-mortem callouts as distinct
warning markers.

**Constraints:** Text legible at 6.5 inch print width. No decorative
elements. White or transparent background.

### 4. Risk-Opportunity Matrix

**Filename:** `INFOGRAPHIC_risk-matrix.png`
**Template:** `templates/infographic-prompts/risk-opportunity-matrix.json`
**Content source:** Decision Record Section 5 (CEO Decision -- Accepted
Risks, Mitigations) + Section 4 (Domain Analyses -- Key Risks, Key
Opportunities)

**Visualizes:** An impact/likelihood grid plotting all identified risks
and opportunities, with accepted risks distinguished from mitigated ones.

**Required data elements:**
- Risks from all domain analyses with source domain
- Accepted risks with CEO reasoning
- Opportunities from all domain analyses with source domain
- Directed mitigations for high-impact risks

**Layout:** Natural human vision perspective, centered. 2x2 or graduated
grid with impact on the vertical axis and likelihood on the horizontal
axis. Risk markers in red tones, opportunity markers in green tones.
Background zones color-coded per `extras.color_mapping`.

**Constraints:** Text legible at 6.5 inch print width. No decorative
elements. White or transparent background.

### 5. Action Plan Timeline

**Filename:** `INFOGRAPHIC_action-plan.png`
**Template:** `templates/infographic-prompts/action-plan-timeline.json`
**Content source:** Decision Record Section 7 (Next Steps)

**Visualizes:** Gantt-style timeline of next steps with owners,
priorities, dependencies, and review triggers.

**Required data elements:**
- Action items with owner, timeline, and priority level
- Dependencies between action items
- Review triggers (conditions or dates for decision review)
- Guardrail-linked actions from CEO conditions

**Layout:** Natural human vision perspective, rule-of-thirds framing.
Horizontal timeline with action items as bars or blocks. Priority
levels color-coded per `extras.color_mapping`. Dependencies shown as
arrows. Review triggers as milestone markers.

**Constraints:** Text legible at 6.5 inch print width. No decorative
elements. White or transparent background.

### 6. Mode Comparison

**Filename:** `INFOGRAPHIC_mode-comparison.png`
**Template:** `templates/infographic-prompts/mode-comparison.json`
**Content source:** Comparative Decision Record (Divergence Analysis)

**Visualizes:** How different synthesis modes produce different decisions
from the same domain analysis, showing convergence and divergence points
as a tree structure.

**Required data elements:**
- Per-mode decision statement and most determinative perspective
- Where modes converge (same decision)
- Where modes diverge (different outcomes)
- The Key Choice (underlying values question)
- Mode Sensitivity rating

**Layout:** Overhead perspective, centered. Shared analysis trunk at
top, branching into per-mode decision leaves. Convergence points shown
in green, divergence points in red. Mode colors per `extras.color_mapping`.

**Constraints:** Text legible at 6.5 inch print width. No decorative
elements. White or transparent background.

---

## Output Requirements

- **Format:** PNG
- **Minimum resolution:** 2000px on the longest edge
- **Background:** White or transparent
- **Visual consistency:** All 5-6 infographics in a session must share
  the same visual style, typography weight, and color temperature
- **Color fidelity:** Hex values in `extras.color_mapping` must be
  reproduced accurately -- do not approximate

**Embedding contexts:**

| Consumer | Usage |
|----------|-------|
| HTML briefing page (Task D) | Embedded as `<img>` tags, responsive scaling |
| PPTX presentation (Task B) | Embedded via `addImage()`, scaled to slide dimensions |
| DOCX report (Task C) | Embedded via `ImageRun`, scaled to US Letter margins |
| Results PDF (Task E) | Inherited from HTML rendering |

---

## Multi-Mode Variant

For standard (single-mode) Decision Records, produce infographics 1-5:
routing diagram, domain scorecard, fault line map, risk-opportunity
matrix, and action plan timeline.

For Comparative Decision Records (multi-mode), produce all 6
infographics. Infographic #6 (mode comparison) is only generated when
the source is a Comparative Decision Record.

---

## Error Handling

1. **Placeholder on exhaustion** -- When all 3 attempts for an infographic
   are consumed, generate a placeholder PNG immediately (white background,
   centered text: `"[Infographic type] -- generation failed. See
   INFOGRAPHIC_<type-slug>_PROMPT.json to generate manually."`). Save the
   fully populated JSON prompt alongside it as
   `{session-output}/images/INFOGRAPHIC_<type-slug>_PROMPT.json` so the
   user can manually generate the graphic. Do not attempt a fourth
   submission.
2. **Check session budget** -- Before each submission, verify the session
   total has not reached 12. If it has, stop and generate placeholders
   (with saved prompt JSON files) for all remaining infographics
   immediately.
3. **Log status** -- In your task completion message, report:
   - Successes on first attempt
   - Corrective feedback uses (attempt 2)
   - Simplified prompt uses (attempt 3)
   - Placeholder fallbacks (with list of saved prompt files)
   - Total submissions used out of 12
4. **Never block the pipeline** -- Task A must complete (with real or
   placeholder images) so Task D can proceed. Do not halt on a single
   infographic failure.

---

## Content Mapping from Decision Record

| Decision Record Section | Infographic(s) | Key Data Extracted |
|---|---|---|
| Section 2: CEO Framing | Routing Diagram | Activated/excluded roles, decision type, thresholds, CSO status |
| Section 4: Domain Analyses | Domain Scorecard | Recommendations, confidence, risks, opportunities, contradictions |
| Section 5: Fault Line Analysis | Fault Line Map | Agreement/contention points, pre-mortem findings, unresolved tensions |
| Section 5: CEO Decision | Risk-Opportunity Matrix | Accepted risks, mitigations, risk/opportunity sources |
| Section 4: Domain Analyses | Risk-Opportunity Matrix | Per-domain key risks and key opportunities |
| Section 7: Next Steps | Action Plan Timeline | Actions, owners, timelines, priorities, dependencies, review triggers |
| Comparative: Divergence Analysis | Mode Comparison | Per-mode decisions, convergence/divergence, Key Choice, Mode Sensitivity |
