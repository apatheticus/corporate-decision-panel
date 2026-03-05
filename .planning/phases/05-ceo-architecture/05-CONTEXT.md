# Phase 5: CEO Architecture - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Extract orchestration protocol from the monolithic 682-line CEO agent into a separate referenced document, and add structured executive summaries to all 8 C-suite agents so the CEO can synthesize from compact summaries first. CEO agent ends up under 350 lines, focused on identity, judgment, and synthesis.

</domain>

<decisions>
## Implementation Decisions

### CEO identity boundary
- `/evaluate` triage logic STAYS in CEO — triage is judgment (assessing tier/mode), not orchestration
- Multi-mode comparison protocol STAYS in CEO — it's the CEO running synthesis N times with different mode modifiers
- Susceptibility mitigation STAYS in CEO — self-awareness directives are identity
- Tier-specific behavior STAYS in CEO — defines synthesis style per tier
- Mode/tier interaction matrix STAYS in CEO — defines CEO's weighting behavior
- Config references section STAYS in CEO — brief, helpful pointers
- Five-phase cascade (Phases 0-5) EXTRACTED — core orchestration protocol
- Production pipeline trigger EXTRACTED — session setup, DAG spawning, artifact dependencies are orchestration
- Organizational roster EXTRACTED — reference data for routing, CEO doesn't need it for synthesis

### Executive summary design
- Executive summary is an ADDITIONAL BLOCK prepended to the existing Domain Recommendation — not a replacement
- Full recommendation stays intact below the executive summary block
- Format: structured fields only, ~4-6 lines total:
  - Role: [agent role]
  - Position: [Approve / Approve with Conditions / Oppose / Neutral]
  - Confidence: [High / Medium / Low]
  - Key Risks: [2-3 bullet points]
- IDENTICAL format across all 8 C-suite agents (including CSO — CSO translates its dossier into the same fields)
- Risks only in the summary — no opportunities field (opportunities are in the full recommendation)

### Deep-dive trigger criteria
- CEO reads executive summaries FIRST for all domain recommendations
- Trigger to read full recommendations: CONFLICTING POSITIONS between executive summaries (e.g., CTO Approve vs CISO Oppose on the same risk dimension)
- When deep-diving, CEO reads ONLY the conflicting domains' full recommendations — not all of them
- CEO explicitly states in the Decision Record which domains were read in full vs summary-only, and why (audit trail — fits existing "transparency over elegance" principle)
- Summary-first approach applies to ALL tiers (Tier 2 and Tier 3) — consistent cognitive pattern regardless of panel size

### Extraction destination
- Orchestration protocol goes to `config/orchestration-protocol.md` — alongside routing-table.md, decision-modes.md, company-profile.md
- CEO.md references the protocol with a section pointer + 2-3 sentence summary per phase (CEO knows the flow without embedding the full protocol)
- Orchestration protocol REFERENCES existing config files (routing-table.md, decision-modes.md) — no duplication
- Routing logic currently inline in CEO.md moves to orchestration-protocol.md, which references config/routing-table.md for actual table data

### Claude's Discretion
- Exact section ordering within the refactored CEO.md
- How to phrase the phase summaries in the CEO's reference section
- Whether config references section needs updating after extraction
- Exact wording of the executive summary block header/template in C-suite agents

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `agents/ceo.md` (682 lines): Source file for extraction — contains all five phases, routing, production pipeline, roster, triage, multi-mode comparison, susceptibility mitigation, tier behavior, mode/tier matrix
- `agents/c-suite/*.md` (8 files): Each has Mode B output template (Domain Recommendation) that needs executive summary block prepended
- `config/routing-table.md`: Already exists — orchestration protocol can reference it instead of duplicating routing tables
- `config/decision-modes.md`: Already exists — orchestration protocol can reference it for mode definitions
- `config/company-profile.md`: Already exists — orchestration protocol can reference it for archetype presets

### Established Patterns
- Agent files use YAML frontmatter (name, description, model, maxTurns) + markdown sections
- C-suite agents have three modes: Mode A (Tier 1 direct consult), Mode B (Tier 2/3 full analysis), Mode C (Phase 4.5 pre-mortem)
- Config files live in `config/` directory and are referenced by agents
- Two-tier visibility principle: team leads report through C-suite parents, not directly to CEO

### Integration Points
- CEO.md Phase 5 synthesis section needs to add summary-first reading logic and audit trail output
- All 8 C-suite agent files need executive summary block added to Mode B output template
- New `config/orchestration-protocol.md` needs to be created
- SKILL.md and slash commands may reference CEO orchestration — these references need updating
- Decision Record template (in CEO Phase 5 Step 5) needs a new field noting which domains were read in full

</code_context>

<specifics>
## Specific Ideas

- The executive summary block should be compact enough that for a typical 8-agent Tier 3 panel, all 8 summaries fit in ~40-50 lines — giving the CEO a single-screen overview before any deep-dive
- The "conflicting positions" trigger should be interpretable by the model naturally — e.g., "If any two executive summaries show opposing positions (one Approve, one Oppose) on related risk dimensions, read those domains' full recommendations"
- The extracted orchestration protocol should be the single authoritative source for phase sequencing — no phase definitions remain in CEO.md, only brief summaries acknowledging the phases exist

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 05-ceo-architecture*
*Context gathered: 2026-03-04*
