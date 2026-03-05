# Architecture: v1.1 Concern Fix Integration

**Domain:** Integrating 11 concern fixes into existing CDP multi-agent orchestration system
**Researched:** 2026-03-04
**Confidence:** HIGH (analysis based on direct reading of all affected source files)

## Executive Summary

The 11 v1.1 concern fixes fall into three architectural categories: **extraction** (pulling embedded specs into standalone documents), **augmentation** (adding new behaviors to existing agent/script flows), and **creation** (building entirely new components). The critical insight is that most fixes touch `agents/ceo.md` -- the 682-line CEO agent is the gravity well of the system. Six of the eleven fixes either read from, write to, or restructure content currently embedded in that file. This makes the CEO refactor (concern #1) the foundational change that most other fixes depend on or benefit from.

The existing architecture is a prompt-and-configuration system with zero application code for the deliberation engine itself (Python scripts handle only infographic generation). All 11 concern fixes are therefore markdown specification changes, Python script additions, or new markdown documents -- not traditional software engineering. The "build" metaphor here means "write and validate specification documents that agents follow."

## Existing Architecture (As-Is)

### System Components

```
agents/
  ceo.md                     (682 lines -- orchestration + identity + routing + modes)
  c-suite/
    cao.md, cfo.md, ciso.md, coo.md, cso.md, cto.md, vp-delivery.md, vp-sales.md
  team-leads/
    cao/, cfo/, ciso/, coo/, cso/, cto/, vp-delivery/, vp-sales/

config/
  routing-table.md            (routing rules + threshold conditions + CSO activation)
  decision-modes.md           (5 modes + mode/tier matrix + multi-mode comparison)
  company-profile.md          (archetype presets + overrides)

templates/
  decision-record.md          (Tier 3 output format)
  comparative-decision-record.md  (multi-mode output format)
  panel-assessment.md         (Tier 2 output format)
  advisory-note.md            (Tier 1 output format)
  production/
    infographics.md, board-presentation.md, board-document.md,
    advisory-document.md, decision-briefing-page.md, capsule-structure.md

scripts/
  config.py, preflight.py, generate_infographic.py, validation.py, session.py

SKILL.md                      (invocation grammar + orchestration protocol + production spec)
```

### Data Flow (Current)

```
User input
  -> SKILL.md (parses invocation, determines tier/mode)
  -> agents/ceo.md (Phase 0-1: frame, route, broadcast)
    -> config/routing-table.md (routing rules applied)
    -> agents/c-suite/cso.md (Phase 1.5: conditional research)
    -> agents/c-suite/*.md (Phase 2-4: domain analysis + synthesis)
      -> agents/team-leads/*/*.md (Phase 3: specialist findings)
    -> config/decision-modes.md (Phase 5: mode modifier applied)
  -> templates/decision-record.md (output formatted)
  -> templates/production/*.md (production artifacts)
    -> scripts/*.py (infographic generation only)
  -> .cdp-output/YYYY-MM-DD_<slug>/ (session output)
```

### Key Architectural Properties

1. **Prompt-as-code:** The deliberation engine has zero application code. Agent behavior is defined entirely by markdown specifications. "Changing architecture" means "editing markdown documents."
2. **CEO monolith:** The CEO agent contains the orchestration protocol (5-phase cascade), routing logic, mode application, triage protocol, multi-mode comparison, susceptibility mitigations, tier-specific behavior, and production pipeline trigger -- all in 682 lines.
3. **Config externalized:** Routing rules and decision modes already live in `config/` as separate documents. The CEO agent references them but duplicates key content inline.
4. **C-suite autonomy:** Each C-suite agent has self-contained identity, team composition, Tier 1 behavior, Tier 2/3 behavior, Phase 4.5 behavior, and synthesis instructions. They produce structured output (Advisory Note or Domain Recommendation) that the CEO ingests.
5. **Production pipeline is append-only:** After deliberation, production agents run sequentially/parallel to create artifacts. No feedback loop from production back to deliberation.
6. **Session directories are write-once:** `.cdp-output/` directories are created and written to, but never cleaned up, archived, or managed.

---

## Per-Concern Integration Analysis

### Concern 1: Extract Orchestration Protocol from CEO Agent

**Category:** Extraction
**What changes:** `agents/ceo.md`
**What is created:** New document (e.g., `config/orchestration-protocol.md` or `docs/orchestration-protocol.md`)
**What stays:** CEO identity, mandate, susceptibility mitigations, organizational roster

**Current state:** The CEO agent contains three distinct concerns in one file:
1. **Identity and judgment principles** (~30 lines) -- who the CEO is and how they think
2. **Orchestration protocol** (~350 lines) -- the 5-phase cascade, Phase 4.5 pre-mortem, multi-mode comparison, production pipeline trigger, session output setup
3. **Triage protocol** (~70 lines) -- `/evaluate` logic
4. **Configuration references and susceptibility mitigations** (~80 lines)

**Integration approach:**
- Extract the orchestration protocol (Phases 0-5, Phase 4.5, multi-mode comparison, production spawn sequence) into a standalone spec document
- CEO agent retains identity, mandate, principles, susceptibility mitigations, organizational roster, and `\`references\`` the orchestration spec
- The extracted spec becomes the canonical source of truth for phase execution; the CEO agent becomes the canonical source for CEO judgment and identity
- Production pipeline trigger and session output setup move with the orchestration protocol (they are procedural, not identity)

**Dependency:** This is the foundational refactor. Concerns 3, 5, 6, and 7 all modify content currently embedded in the CEO agent. Extracting the protocol first creates clean separation, so subsequent fixes modify the right document.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `agents/ceo.md` | MODIFY -- remove orchestration protocol, add reference to extracted spec | Major reduction (~350 lines removed) |
| `config/orchestration-protocol.md` (NEW) | CREATE -- extracted 5-phase cascade, production pipeline, session setup | ~350 lines |
| `SKILL.md` | MODIFY -- update references if SKILL.md currently delegates to CEO agent for protocol | Minor |

---

### Concern 2: Pre-Flight Validation for Production Pipeline

**Category:** Augmentation
**What changes:** Orchestration protocol (wherever it lives after concern #1)
**What is created:** Pre-flight checklist specification in orchestration protocol or production spec

**Current state:** The production pipeline trigger in the CEO agent immediately spawns 5 production tasks after the Decision Record is produced. There is no validation that prerequisites exist before production begins. The infographic pipeline has its own `scripts/preflight.py` for API validation, but the broader production pipeline (PPTX, DOCX, HTML, PDF) has no equivalent.

**What could fail without pre-flight:**
- Decision Record not fully formed (missing sections)
- Session output directory not created
- `.cdp-context/config.md` missing (API key for infographics)
- Build dependencies not available (Node.js for PPTX/DOCX generation scripts)

**Integration approach:**
- Add a "Production Pre-Flight" section to the orchestration protocol that executes between Decision Record completion and production task spawning
- Pre-flight validates: (a) Decision Record completeness (all mandatory sections present), (b) session output directory exists with correct structure, (c) `.cdp-context/config.md` accessible (for infographic generation), (d) RECORD.md written to session directory
- This is a spec addition, not code -- the CEO agent (or orchestrator) follows these steps as part of the protocol
- Failure at any step produces a structured error message and does not spawn production tasks

**Dependency:** Benefits from concern #1 being done first (adds to extracted orchestration protocol rather than bloating CEO agent further). But can be done independently by adding to whichever document owns the production pipeline trigger.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| Orchestration protocol (wherever it lives) | MODIFY -- add pre-flight section before production spawn | ~30-40 lines added |
| `templates/production/infographics.md` | No change -- infographic pre-flight already exists in `scripts/preflight.py` |  |

---

### Concern 3: CSO Phase 1.5 Timeout Handling

**Category:** Augmentation
**What changes:** Orchestration protocol (Phase 1.5 section), `agents/c-suite/cso.md`
**What stays:** CSO identity, research process, dossier format

**Current state:** Phase 1.5 describes the CSO research investigation but has no timeout or error handling. If the CSO research takes too long, stalls, or produces incomplete results, there is no specified fallback. The orchestration protocol says "the CSO produces a Research Dossier" but does not define what happens when the CSO fails to produce one.

**Integration approach:**
- Add timeout/fallback section to Phase 1.5 in the orchestration protocol
- Define three failure modes: (a) CSO produces no dossier (timeout/failure), (b) CSO produces partial dossier (some team leads responded, others did not), (c) CSO produces low-quality dossier (Grade D evidence quality)
- For each failure mode, specify the CEO's response: proceed without dossier (with explicit notation in Decision Record), proceed with partial dossier (flag gaps), request CSO to focus on highest-priority sub-questions only
- Add a "Research Scope Control" section to the CSO agent that accepts a `priority_subset` directive from the CEO, allowing narrower research scope under time pressure

**Dependency:** Independent. Can be done before or after concern #1. Touches the orchestration protocol (Phase 1.5 section) and the CSO agent spec.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| Orchestration protocol (Phase 1.5 section) | MODIFY -- add timeout handling, fallback protocol | ~40-50 lines added |
| `agents/c-suite/cso.md` | MODIFY -- add priority_subset directive handling, scope control | ~20-30 lines added |
| `templates/decision-record.md` | MODIFY -- add notation for "Research Dossier unavailable/partial" | ~5 lines |

---

### Concern 4: Executive Summary Layer for C-Suite Agents

**Category:** Augmentation
**What changes:** All 8 C-suite agent files
**What stays:** Agent identity, team composition, analytical process

**Current state:** In Tier 2/3 mode, each C-suite agent produces a Domain Recommendation that includes Summary (2-3 sentences), Team Lead Findings (1-2 sentences each, up to 5 team leads), Internal Contradictions, Key Risks, Key Opportunities, and Conditions for Approval. The CEO receives ALL of this from ALL activated agents before synthesizing. For a Tier 3 full-activation with 8 C-suite agents, each with 4-5 team leads, the CEO must process ~40+ team lead findings plus 8 domain syntheses.

**The token cost problem:** The CEO (Opus model) ingests the full output of every activated C-suite agent. More C-suite output = more Opus input tokens = higher cost. The Domain Recommendation format currently includes per-team-lead findings that the CEO should not need -- the CEO is supposed to engage with domain-level synthesis, not individual team lead findings (this is explicitly stated in Phase 3: "You do not see team lead outputs directly -- you see them only as synthesized through the C-suite officer's domain recommendation").

**Integration approach:**
- Add an "Executive Summary" output requirement to each C-suite agent's Tier 2/3 mode
- The Executive Summary is a 3-5 sentence structured block placed at the TOP of the Domain Recommendation, containing: recommendation, confidence, most determinative finding, strongest risk, strongest opportunity
- The CEO ingests only the Executive Summary from each agent for initial synthesis, then can reference the full Domain Recommendation if needed for fault line analysis
- This does NOT change the Domain Recommendation structure -- it ADDS a structured prefix that enables the CEO to work with compressed input
- Each C-suite agent adds ~10 lines to their Mode B section defining the Executive Summary format

**Dependency:** Independent of all other concerns. Purely a C-suite agent spec change. Can be done in any order.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `agents/c-suite/cao.md` | MODIFY -- add Executive Summary to Mode B output | ~10 lines |
| `agents/c-suite/cfo.md` | MODIFY -- add Executive Summary to Mode B output | ~10 lines |
| `agents/c-suite/ciso.md` | MODIFY -- add Executive Summary to Mode B output | ~10 lines |
| `agents/c-suite/coo.md` | MODIFY -- add Executive Summary to Mode B output | ~10 lines |
| `agents/c-suite/cso.md` | N/A -- CSO produces Research Dossier, not Domain Recommendation | No change |
| `agents/c-suite/cto.md` | MODIFY -- add Executive Summary to Mode B output | ~10 lines |
| `agents/c-suite/vp-delivery.md` | MODIFY -- add Executive Summary to Mode B output | ~10 lines |
| `agents/c-suite/vp-sales.md` | MODIFY -- add Executive Summary to Mode B output | ~10 lines |
| Orchestration protocol (Phase 4) | MODIFY -- specify CEO ingests Executive Summaries first | ~10 lines |

---

### Concern 5: Formalize Routing Thresholds into Decision Trees

**Category:** Extraction + Formalization
**What changes:** `config/routing-table.md`
**What stays:** Routing logic semantics (the actual rules do not change)

**Current state:** The routing table specifies 5 full-activation threshold conditions as prose descriptions:
1. Irreversibility
2. Headcount Impact (>30%)
3. Market Position Change
4. Existential Financial Risk
5. Domain Uncertainty

These are currently described in natural language in both `config/routing-table.md` AND duplicated in `agents/ceo.md` (Step 4 of Phase 1). The CEO must interpret prose to make routing decisions. There are no structured decision criteria, branching logic, or explicit examples distinguishing "triggered" from "not triggered."

**Integration approach:**
- Formalize each threshold condition into a structured decision tree with explicit criteria, examples of triggered vs. not-triggered, and edge cases
- Keep the decision trees in `config/routing-table.md` (its natural home)
- Remove the duplicated threshold prose from `agents/ceo.md` (or the extracted orchestration protocol) and replace with a reference to `config/routing-table.md`
- Each decision tree should have: condition name, trigger question (yes/no), positive examples, negative examples, edge cases, and escalation guidance

**Dependency:** Benefits from concern #1 (duplication in CEO agent is easier to clean up if orchestration is already extracted). But can proceed independently -- just needs to update both `config/routing-table.md` and `agents/ceo.md`.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `config/routing-table.md` | MODIFY -- expand threshold conditions into decision trees | Major expansion (~100-150 lines added) |
| `agents/ceo.md` or orchestration protocol | MODIFY -- remove duplicated threshold prose, add reference | Lines removed |

---

### Concern 6: Explicit Mode-to-Weighting Mappings

**Category:** Formalization
**What changes:** `config/decision-modes.md`
**What stays:** Mode semantics, mode/tier interaction matrix

**Current state:** Each decision mode has a "Resolution Pattern" description and a "CEO Prompt Modifier" block. The Resolution Pattern says things like "Weights skeptic roles (CISO, CFO, COO, VP Delivery) more heavily" (Guardian) or "Weights advocate roles (VP Sales, CTO) more heavily" (Pioneer). But there are no explicit condition-to-weighting tables showing HOW the weighting works. The CEO interprets prose modifiers to determine weighting.

**Integration approach:**
- Add a "Weighting Table" to each mode in `config/decision-modes.md`
- Each table maps: role -> base weight (equal) -> mode modifier -> effective weight direction
- Example for Guardian mode: `CISO: base + skeptic bonus = HIGH`, `CTO: base - advocate penalty = MODERATE`, `CFO: base + skeptic bonus = HIGH`
- These are directional indicators (HIGH/MODERATE/LOW), not numeric weights -- the CEO still exercises judgment, but the direction is formalized
- Add a "Conflict Resolution Rule" for each mode: what happens when two HIGH-weight roles disagree
- This makes implicit weighting explicit and auditable

**Dependency:** Independent. Modifies only `config/decision-modes.md`. Can proceed in any order.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `config/decision-modes.md` | MODIFY -- add weighting tables and conflict resolution rules per mode | ~100-120 lines added |

---

### Concern 7: Document Multi-Mode Cost Formula

**Category:** Creation (documentation)
**What changes:** `config/decision-modes.md` (Multi-Mode Comparison section)
**What stays:** Multi-mode comparison protocol

**Current state:** The multi-mode comparison section says "Approximately 1.1x a single deliberation for 5x the strategic insight" but does not show how this is calculated. The claim "domain analysis runs once; CEO synthesis runs N times" is stated but not quantified in terms of actual token costs, agent invocations, or practical cost implications.

**Integration approach:**
- Add a "Cost Model" subsection to the Multi-Mode Comparison section of `config/decision-modes.md`
- Document the actual cost components: (a) Phase 0-4 agent invocations (mode-independent, runs once), (b) Phase 5 CEO synthesis (mode-dependent, runs N times), (c) Phase 4.5 pre-mortem (mode-independent, runs once if Tier 3)
- Provide a formula: `Total cost = C(phases 0-4) + N * C(phase 5)` where N = number of modes
- Show example calculations for common scenarios: single mode Tier 2, single mode Tier 3, 2-mode comparison, all-modes (5x)
- Include the model cost basis: CEO = Opus, C-suite = Sonnet, Team leads = Haiku

**Dependency:** Independent. Documentation-only change to `config/decision-modes.md`.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `config/decision-modes.md` | MODIFY -- add Cost Model subsection | ~40-60 lines added |

---

### Concern 8: Session Output Cleanup Mechanism

**Category:** Creation (new component)
**What changes:** Nothing existing
**What is created:** New specification or script for session cleanup

**Current state:** Session output directories (`.cdp-output/YYYY-MM-DD_<slug>/`) are created during production and never cleaned up. Over time, this directory accumulates session directories with images, build artifacts, PPTX/DOCX/HTML/PDF files. There is no archive, cleanup, or lifecycle management.

**Integration approach:**
- Create a cleanup specification that can be invoked via a new slash command (`/cdp:cleanup`) or as a script
- Two options exist:
  - **Option A (Spec-only):** Add a cleanup protocol to `SKILL.md` that the CEO agent follows when invoked. Lists sessions, lets user confirm deletion, removes selected directories.
  - **Option B (Script):** Add a Python script `scripts/cleanup.py` that lists sessions with metadata (date, slug, file count, total size), supports `--older-than N` days, `--dry-run`, and `--confirm` flags.
- **Recommendation: Option B (Script)** -- cleanup is mechanical and benefits from actual code rather than prompt-based execution. File enumeration, size calculation, and date comparison are more reliable in Python than in an LLM prompt.
- The script should: (a) scan `.cdp-output/` for session directories, (b) parse date from directory name prefix, (c) calculate total size per session, (d) support `--older-than` days filter, (e) support `--dry-run` to preview without deleting, (f) require `--confirm` for actual deletion

**Dependency:** Fully independent. New component with no dependencies on any other concern.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `scripts/cleanup.py` (NEW) | CREATE -- session cleanup script | ~100-150 lines |
| `tests/test_cleanup.py` (NEW) | CREATE -- tests for cleanup script | ~80-120 lines |
| `SKILL.md` | MODIFY -- add `/cdp:cleanup` invocation documentation | ~15-20 lines |

---

### Concern 9: Test Scenario -- Tier 2 Routing Partial Activation Exclusion

**Category:** Creation (test specification)
**What changes:** Nothing existing
**What is created:** Test scenario document

**Current state:** Tier 2 routing activates 2-4 C-suite members. The routing table specifies default activation per decision type. But there is no test scenario that validates: (a) excluded agents are actually excluded (not consulted), (b) partial activation produces coherent output without missing domain coverage, (c) the CEO's exclusion reasoning is stated and justified.

**Integration approach:**
- Create a test scenario document that defines specific test cases for Tier 2 routing
- Each test case specifies: input issue, expected decision type classification, expected activated roles, expected excluded roles, validation criteria for exclusion reasoning
- Test cases should cover: (a) a pure Financial decision (only CEO, CFO, COO activated -- verify CISO, CTO, VP Sales, VP Delivery, CAO are excluded), (b) a multi-type decision (e.g., Financial + Technical) where activation sets merge, (c) an edge case where threshold conditions should trigger full activation but the issue was presented as narrow-scope
- These are specification-level test scenarios (manual or prompt-based validation), not pytest unit tests

**Dependency:** Benefits from concern #5 (formalized routing thresholds make test criteria clearer). But can proceed independently.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `tests/scenarios/tier-2-routing.md` (NEW) | CREATE -- test scenarios for partial activation | ~80-100 lines |

---

### Concern 10: Test Scenario -- Pre-Mortem Phase 4.5 with Partial/Missing Responses

**Category:** Creation (test specification)
**What changes:** Nothing existing
**What is created:** Test scenario document

**Current state:** Phase 4.5 pre-mortem requires each activated C-suite agent to produce a pre-mortem response. But the spec does not define what happens when: (a) an agent fails to produce a pre-mortem response, (b) an agent's pre-mortem is low-quality or tautological ("the decision fails because it was a bad decision"), (c) the CSO's evidence-gap-focused pre-mortem contradicts other agents' pre-mortem findings.

**Integration approach:**
- Create test scenarios for Phase 4.5 edge cases
- Test cases: (a) one C-suite agent produces no pre-mortem (CEO synthesis should note the gap), (b) pre-mortem responses that merely restate Phase 4 domain risks (quality validation), (c) CSO evidence-gap pre-mortem that invalidates assumptions used in other agents' pre-mortem responses (cross-reference validation)
- Include both "expected behavior" and "anti-pattern" examples
- May also surface a need to add fallback handling to the orchestration protocol (Phase 4.5 section)

**Dependency:** Independent. Can inform a future augmentation of Phase 4.5 in the orchestration protocol.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `tests/scenarios/pre-mortem-phase-4-5.md` (NEW) | CREATE -- test scenarios for pre-mortem edge cases | ~80-100 lines |

---

### Concern 11: Mode Sensitivity Criteria and Test

**Category:** Creation (specification + test)
**What changes:** `config/decision-modes.md` (Mode Sensitivity section)
**What is created:** Formal sensitivity criteria + test scenario document

**Current state:** Mode Sensitivity is defined in the Comparative Decision Record template as LOW/MEDIUM/HIGH with informal descriptions:
- LOW: "All modes converge on the same answer"
- MEDIUM: "Modes agree on direction but differ on conditions, pace, or scope"
- HIGH: "Modes produce fundamentally different decisions"

There are no formal criteria for what constitutes "same answer" vs "different direction" vs "fundamentally different." The CEO currently makes this judgment without guidance.

**Integration approach:**
- Formalize sensitivity criteria in `config/decision-modes.md`:
  - LOW: All modes produce the same recommendation category (Approve/Oppose/Defer) AND the same or compatible conditions
  - MEDIUM: All modes produce the same recommendation category but with materially different conditions, scope, or timeline
  - HIGH: Modes produce different recommendation categories (some Approve, some Oppose) or incompatible conditions
- Create test scenarios that exercise multi-mode comparison with known inputs to verify consistent sensitivity classification
- Test cases should include: (a) a clear-cut decision where all modes should converge (expected: LOW), (b) a balanced decision where modes agree on direction but differ on risk framing (expected: MEDIUM), (c) a polarizing decision where risk appetite is the deciding factor (expected: HIGH)

**Dependency:** Benefits from concern #6 (explicit mode weightings make sensitivity analysis more rigorous). Can proceed independently.

**Files affected:**
| File | Action | Scope |
|------|--------|-------|
| `config/decision-modes.md` | MODIFY -- formalize Mode Sensitivity criteria | ~30-40 lines added |
| `tests/scenarios/mode-sensitivity.md` (NEW) | CREATE -- test scenarios for sensitivity classification | ~80-100 lines |

---

## Component Dependency Map

```
Concern 1 (CEO Extraction)
    |
    |-- enables cleaner implementation of:
    |       Concern 2 (Production Pre-Flight)
    |       Concern 3 (CSO Timeout)
    |       Concern 5 (Routing Decision Trees)
    |
    v
Concern 5 (Routing Decision Trees)
    |
    |-- informs test criteria for:
    |       Concern 9 (Tier 2 Routing Test)
    |
    v
Concern 6 (Mode Weightings)
    |
    |-- informs sensitivity analysis for:
    |       Concern 11 (Mode Sensitivity)
    |
    v

Independent concerns (no dependencies):
    Concern 4 (Executive Summaries) -- touches only C-suite agents
    Concern 7 (Cost Formula) -- documentation only
    Concern 8 (Session Cleanup) -- new component, no existing deps
    Concern 10 (Pre-Mortem Test) -- new test scenario
```

## Recommended Build Order

The build order optimizes for: (1) foundational changes first, (2) dependent changes after their prerequisites, (3) independent concerns parallelized or interleaved freely.

### Phase 1: Foundation (do first)

| Order | Concern | Rationale |
|-------|---------|-----------|
| 1.1 | **#1: CEO Extraction** | Foundational. Creates clean separation between CEO identity and orchestration protocol. All subsequent orchestration changes go into the extracted spec instead of bloating the CEO agent further. |
| 1.2 | **#4: Executive Summaries** | Independent but high-value. Reduces CEO token ingestion. Touches only C-suite agents (no conflict with CEO extraction). |

### Phase 2: Orchestration Hardening (requires Phase 1)

| Order | Concern | Rationale |
|-------|---------|-----------|
| 2.1 | **#2: Production Pre-Flight** | Adds to extracted orchestration protocol. |
| 2.2 | **#3: CSO Timeout** | Adds to extracted orchestration protocol (Phase 1.5). |
| 2.3 | **#8: Session Cleanup** | Independent but groups naturally with production pipeline work. |

### Phase 3: Specification Formalization (benefits from Phase 1)

| Order | Concern | Rationale |
|-------|---------|-----------|
| 3.1 | **#5: Routing Decision Trees** | Removes duplication created/revealed by CEO extraction. |
| 3.2 | **#6: Mode Weightings** | Formalizes implicit weighting in decision modes. |
| 3.3 | **#7: Cost Formula** | Documentation addition to decision modes. Natural to do alongside #6. |

### Phase 4: Test Scenarios (benefits from Phases 2-3)

| Order | Concern | Rationale |
|-------|---------|-----------|
| 4.1 | **#9: Tier 2 Routing Test** | Tests routing logic formalized in #5. |
| 4.2 | **#10: Pre-Mortem Test** | Tests Phase 4.5 (benefits from orchestration hardening in Phase 2). |
| 4.3 | **#11: Mode Sensitivity** | Tests mode mechanics formalized in #6. |

### Phase ordering rationale

- **Phase 1 before Phase 2:** The CEO extraction (#1) creates the document where production pre-flight (#2) and CSO timeout (#3) will be added. Without extraction, those additions bloat the already-682-line CEO agent.
- **Phase 1 before Phase 3:** Routing decision trees (#5) need to clean up duplication between CEO agent and routing table. Extraction makes this cleaner -- the duplication in the CEO agent is removed as part of extraction, and the routing table becomes the single source of truth.
- **Phase 3 before Phase 4:** Test scenarios (#9, #10, #11) validate the specifications formalized in Phase 3. Writing tests before the specs are formalized means testing against ambiguous criteria.
- **Executive Summaries (#4) in Phase 1:** This is independent of all other concerns and high-value (token cost reduction). It can run in parallel with CEO extraction since it touches only C-suite agents, not the CEO agent.

---

## Change Impact Summary

### Files Modified

| File | Concerns | Total Change Estimate |
|------|----------|----------------------|
| `agents/ceo.md` | #1, #5 | Major reduction (~350 lines removed, ~20 lines reference added) |
| `agents/c-suite/cao.md` | #4 | Minor (~10 lines added) |
| `agents/c-suite/cfo.md` | #4 | Minor (~10 lines added) |
| `agents/c-suite/ciso.md` | #4 | Minor (~10 lines added) |
| `agents/c-suite/coo.md` | #4 | Minor (~10 lines added) |
| `agents/c-suite/cso.md` | #3, (no #4) | Minor (~20-30 lines added for timeout handling) |
| `agents/c-suite/cto.md` | #4 | Minor (~10 lines added) |
| `agents/c-suite/vp-delivery.md` | #4 | Minor (~10 lines added) |
| `agents/c-suite/vp-sales.md` | #4 | Minor (~10 lines added) |
| `config/routing-table.md` | #5 | Major expansion (~100-150 lines added) |
| `config/decision-modes.md` | #6, #7, #11 | Moderate expansion (~170-220 lines added) |
| `templates/decision-record.md` | #3 | Minor (~5 lines added) |
| `SKILL.md` | #1, #8 | Minor (~20-35 lines changed) |

### Files Created

| File | Concern | Type | Size Estimate |
|------|---------|------|---------------|
| `config/orchestration-protocol.md` | #1 | Specification | ~350 lines |
| `scripts/cleanup.py` | #8 | Python script | ~100-150 lines |
| `tests/test_cleanup.py` | #8 | Python tests | ~80-120 lines |
| `tests/scenarios/tier-2-routing.md` | #9 | Test scenario | ~80-100 lines |
| `tests/scenarios/pre-mortem-phase-4-5.md` | #10 | Test scenario | ~80-100 lines |
| `tests/scenarios/mode-sensitivity.md` | #11 | Test scenario | ~80-100 lines |

### Files Unchanged

- `agents/team-leads/**/*` -- No team lead agents are affected
- `config/company-profile.md` -- Company profile is not involved in any concern
- `scripts/config.py`, `scripts/generate_infographic.py`, `scripts/validation.py`, `scripts/session.py` -- Existing Python scripts are not affected
- `templates/production/*` -- Production templates are not affected
- `templates/comparative-decision-record.md`, `templates/panel-assessment.md`, `templates/advisory-note.md` -- Not affected

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Duplicating Orchestration Protocol After Extraction
**What:** Extracting the protocol from `ceo.md` but leaving a "summary" version in the CEO agent that drifts from the canonical spec.
**Why bad:** Two sources of truth for the same protocol = guaranteed inconsistency.
**Instead:** CEO agent references the extracted protocol by filepath. Zero duplication of procedural content.

### Anti-Pattern 2: Executive Summaries That Replace Domain Recommendations
**What:** Making Executive Summaries the ONLY output the CEO sees, eliminating the full Domain Recommendation.
**Why bad:** The CEO needs full Domain Recommendations for fault line analysis. Executive Summaries are for initial triage and token reduction, not for replacing the analytical substrate.
**Instead:** Executive Summary is a structured PREFIX added to the Domain Recommendation. The CEO reads summaries first, then drills into full recommendations for synthesis.

### Anti-Pattern 3: Overengineering Session Cleanup
**What:** Building a complex archive system with compression, cloud backup, retention policies.
**Why bad:** Sessions are local development artifacts. Users can manually delete old directories. The cleanup script should be simple and mechanical.
**Instead:** List, filter by age, delete with confirmation. Nothing more.

### Anti-Pattern 4: Numeric Weights for Decision Modes
**What:** Assigning specific numeric weights (e.g., "CISO gets 1.5x weight in Guardian mode") to mode weightings.
**Why bad:** The CEO is an LLM following a prompt. Numeric weights create false precision. The LLM will not reliably apply "1.5x" weighting.
**Instead:** Use directional indicators (HIGH/MODERATE/LOW priority) that guide the LLM's attention without pretending to be quantitative.

### Anti-Pattern 5: Test Scenarios as Pytest Tests
**What:** Writing the routing, pre-mortem, and mode sensitivity test scenarios as automated pytest tests.
**Why bad:** These test the behavior of LLM agents following markdown specifications. They cannot be deterministically tested with unit tests. The "test" is a structured prompt scenario with expected-behavior criteria, not an assertion.
**Instead:** Test scenario documents with input, expected behavior, and validation criteria that can be manually or semi-automatically evaluated by running the CDP system.

---

## Scalability Considerations

| Concern | At current scale (8 C-suite, 34 team leads) | If roster grows (12+ C-suite) |
|---------|----------------------------------------------|-------------------------------|
| CEO Extraction (#1) | Clean separation enables independent updates | Essential -- a 682-line agent only gets worse with more roles |
| Executive Summaries (#4) | Reduces Opus token cost by ~30-50% for Tier 3 | Critical -- token cost scales linearly with activated agents |
| Routing Decision Trees (#5) | Clearer routing for 6 decision types | Must scale to new decision types without combinatorial explosion |
| Mode Weightings (#6) | 5 modes x 8 roles = 40 directional weights | Must scale to new roles without redesigning weight tables |
| Session Cleanup (#8) | Manageable with manual cleanup | Essential with high session volume |

## Sources

- `agents/ceo.md` -- 682-line CEO agent (direct reading, lines 1-682)
- `agents/c-suite/*.md` -- All 8 C-suite agent specifications (direct reading)
- `config/routing-table.md` -- Routing rules and threshold conditions (direct reading)
- `config/decision-modes.md` -- 5 decision modes and multi-mode comparison (direct reading)
- `config/company-profile.md` -- Archetype presets (direct reading)
- `templates/decision-record.md` -- Tier 3 output template (direct reading)
- `templates/production/infographics.md` -- Production pipeline spec (direct reading)
- `scripts/session.py`, `scripts/preflight.py` -- Python infrastructure (direct reading)
- `SKILL.md` -- Skill entry point and orchestration overview (direct reading)
- `docs/ARCHITECTURE.md` -- Technical reference (direct reading)
- `.planning/PROJECT.md` -- Project context and v1.1 scope (direct reading)
- `.planning/milestones/v1.0-MILESTONE-AUDIT.md` -- v1.0 audit findings (direct reading)
