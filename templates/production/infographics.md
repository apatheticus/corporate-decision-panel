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

**Generation engine:** `scripts/session.py` -- Python session orchestrator
that calls the Gemini API directly via `google-genai` SDK. No browser
automation.

**Prompt format:** JSON templates in `templates/infographic-prompts/`
with six top-level keys: `core`, `style`, `technical`, `composition`,
`quality_keywords`, `extras`.

**Style overrides:** If `.cdp-context/style.md` exists, the script reads
it and appends style guidance to each prompt automatically.

**Configuration:** `.cdp-context/config.md` provides:
- **Gemini API Key** -- required for API access
- **Image Model** -- default: gemini-2.5-flash-image
- **Retry Limit** -- default: 2 (3 total attempts per infographic)

---

## Retry Behavior

Retry limit is configured in `.cdp-context/config.md` via the
**Retry Limit** field (default: 2, meaning 3 total attempts per
infographic). The script handles retries internally:

- **Transient errors** (429, 500, 503) trigger exponential backoff
  with jitter
- **Content/safety blocks** produce a placeholder PNG immediately
  (no retry)
- **Validation failures** retry with corrective feedback appended
  to the prompt
- **Budget exhaustion** saves the image as-is (if generated) or
  produces a placeholder PNG with a saved prompt JSON for manual retry

---

## Generation Workflow

For each session, the Image Agent follows this workflow:

1. **Extract data** -- Read the Decision Record and extract the required
   data for each infographic type per the Content Mapping table below
2. **Write data files** -- Save one JSON file per infographic type to
   `{session-output}/images/` with placeholder token values
3. **Run session** -- Call `scripts/session.py` with all type slugs,
   data paths, and the output directory. The session orchestrator:
   - Generates each type sequentially with 4-second inter-call delay
   - Runs vision-based validation after each successful generation
   - Retries with corrective feedback if validation fails
   - Doubles inter-call delay if 429 rate limit is encountered
   - Produces a summary table with status per type
4. **Report results** -- Parse the session summary and report
   OK / OK+WARN / FAILED / BLOCKED status per type to the CEO agent

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

1. **Placeholder on failure** -- When all attempts for an infographic
   are exhausted without a successful generation, a placeholder PNG is
   created (white background, centered error text) and the prompt is
   saved as `INFOGRAPHIC_<type-slug>_PROMPT.json` for manual retry.
2. **Content blocks** -- If the Gemini API blocks the prompt for
   content/safety reasons, a placeholder is generated immediately
   with no retry (the same prompt will always be blocked).
3. **Rate limiting** -- 429 responses trigger exponential backoff.
   The session orchestrator also doubles its inter-call delay for
   remaining types to reduce further rate limit hits.
4. **Session summary** -- After all types are processed, the script
   prints a summary table: `SUMMARY <type> <status> <attempts>/<max> <path>`
   where status is OK, OK+WARN, FAILED, or BLOCKED.
5. **Never block the pipeline** -- A PNG file exists at the standard
   path for every type regardless of outcome (real or placeholder)
   so downstream agents (Tasks B, C, D) are never blocked.

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
