# Phase 4: Scale and Docs - Research

**Researched:** 2026-03-04
**Domain:** Documentation rewrite, browser automation removal, 6-type verification
**Confidence:** HIGH

## Summary

Phase 4 is a documentation and verification phase with no new code to write. The generation engine (Phase 2) and error handling/validation pipeline (Phase 3) are complete. The work is: (1) rewrite `templates/production/infographics.md` to describe the API-based script workflow instead of browser automation, (2) update the `agents/ceo.md` Task A spawn instruction, (3) sweep the entire repo for remaining browser automation references and remove them, and (4) verify all 6 infographic types generate successfully via the existing `scripts/session.py` orchestrator.

The codebase grep reveals exactly 6 files containing browser automation references: `templates/production/infographics.md`, `agents/ceo.md`, `SKILL.md`, `README.md`, `docs/README.md`, and `docs/ARCHITECTURE.md`. The Python scripts (`scripts/`) are already fully API-based and contain zero browser automation references. The task is a clean documentation migration.

**Primary recommendation:** Treat this as two parallel work streams -- doc rewrite (infographics.md + ceo.md + repo sweep) and verification (run all 6 types through session.py). The doc rewrite can reference existing code patterns directly since the API implementation is complete and stable.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Image Agent remains a separate spawned agent (Task A), preserving the parallel task architecture (A/B/C run simultaneously)
- Image Agent reads the Decision Record, extracts data per infographic type, and writes a data JSON file to `{session}/images/` per type
- Agent calls the session orchestrator (`scripts/session.py`) to generate all 6 types at once -- does not call `generate_infographic` individually
- Agent reports the session summary (OK/FAILED/BLOCKED per type) back to the CEO agent
- Script is a pure generation tool; the agent handles all data extraction from the Decision Record
- Infographics.md rewrite: Replace Technology, Attempt Budget, Browser Automation Workflow, Error Handling sections; Keep Purpose, all 6 Infographic Specifications, Output Requirements, Content Mapping, Multi-Mode Variant
- Simplify Attempt Budget to brief "Retry Behavior" section referencing `config.md` `Retry Limit` field
- Remove Style Configuration Integration mapping table -- replace with brief note that script applies `.cdp-context/style.md` automatically if present
- Audience shift: from "Image Agent doing browser automation" to "Image Agent calling a Python script with data JSON files"
- Live test all 6 infographic types with real Decision Record data (OK or OK+WARN passes)
- Full repo sweep: grep entire codebase for browser automation references -- remove completely
- Platform field in config.md already removed in Phase 1 -- verify it is gone during sweep

### Claude's Discretion
- Session orchestrator CLI invocation details (how Image Agent calls session.py)
- Data JSON schema for each infographic type (field names, structure)
- Exact wording of new infographics.md sections (Technology, Workflow, Retry Behavior, Error Handling)
- CEO spawn description wording for Task A
- Test data source (existing session vs synthetic record)
- Order of operations: docs update first vs verification first

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DOC-01 | Update `templates/production/infographics.md` Task A spec for API-based flow | Full analysis of current doc (363 lines), section-by-section keep/replace mapping, and new workflow pattern based on session.py/generate_infographic.py code |
| DOC-03 | Update `agents/ceo.md` Task A spawn instruction | Exact location identified (line 595-599), replacement text pattern documented |
| DOC-04 | Remove all browser automation references from image generation workflow | Complete file inventory: 6 files with references, line-level locations identified, removal patterns documented |

</phase_requirements>

## Standard Stack

### Core

This phase does not introduce new libraries. All work is documentation edits and verification using existing infrastructure.

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| `scripts/session.py` | current | Session orchestrator for 6-type batch generation | Already built in Phase 3 |
| `scripts/generate_infographic.py` | current | Per-type generation with retry, validation | Already built in Phases 2-3 |
| `scripts/validation.py` | current | Vision-based quality validation | Already built in Phase 3 |
| pytest | 9.0.2 | Test runner for verification | Already configured |

### Supporting

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `grep -rn` / `rg` | Browser automation reference sweep | During DOC-04 cleanup |
| `python -m scripts.generate_infographic` | CLI for individual type testing | If debugging a single type |

## Architecture Patterns

### Current Script Architecture (Reference for Doc Rewrite)

```
scripts/
  __init__.py            # Package marker
  __main__.py            # CLI: python -m scripts.generate_infographic
  config.py              # load_config() -> api_key, model_id, retry_limit
  preflight.py           # run_preflight() -> PreflightResult
  generate_infographic.py # generate_infographic(), generate_with_retry(), CLI main()
  validation.py          # validate_infographic() -> ValidationResult
  session.py             # run_session() -> SessionResult
```

### Image Agent Workflow (New Doc Pattern)

The infographics.md rewrite should describe this workflow:

```
1. Agent reads Decision Record
2. Agent extracts data per infographic type
3. Agent writes data JSON files to {session}/images/
4. Agent calls: python scripts/session.py (or session.run_session())
5. Session orchestrator iterates over 6 types:
   a. Loads template from templates/infographic-prompts/<type>.json
   b. Substitutes placeholders with data from JSON
   c. Reads .cdp-context/style.md for style overrides (if present)
   d. Serializes to natural language prompt
   e. Calls Gemini API with image modalities
   f. Runs vision validation on result
   g. Retries with corrective feedback if validation fails
   h. Applies inter-call delay (4s base, adaptive doubling on 429)
6. Agent reads session summary (OK/OK+WARN/FAILED/BLOCKED per type)
7. Agent reports results to CEO
```

### Data JSON Schema Pattern

Each data JSON file maps placeholder tokens to concrete values. The existing sample fixture shows the pattern:

```json
{
  "DOMAIN_RECOMMENDATIONS": "Finance: Approve (High confidence), ...",
  "KEY_RISKS": "Finance: Budget overrun...",
  "KEY_OPPORTUNITIES": "Finance: 15% cost reduction...",
  "INTERNAL_CONTRADICTIONS": "Finance projects 15% savings but...",
  "ACTIVATED_DOMAINS": "Finance, Legal, Operations, Technology",
  "DECISION_MODE": "Architect",
  "DOMAIN_COUNT": "4",
  "CONSENSUS_LEVEL": "mild dissent",
  "MOST_DETERMINATIVE": "Finance"
}
```

Placeholder tokens match `{{TOKEN}}` patterns in JSON templates. Unknown tokens resolve to `[TOKEN]` bracketed form.

### Session Orchestrator API

```python
from scripts.session import run_session, SessionResult

result: SessionResult = run_session(
    types_list=["routing-diagram", "domain-scorecard", "fault-line-map",
                "risk-opportunity-matrix", "action-plan-timeline", "mode-comparison"],
    data_paths={"routing-diagram": Path("data/routing.json"), ...},
    output_dir=Path("{session}/images/"),
    config_dir=Path(".cdp-context"),
)

# result.any_succeeded -> bool
# result.results -> dict[str, GenerationResult]
# result.summary_lines -> list[str] (SUMMARY lines)
```

### Anti-Patterns to Avoid
- **Do not invent new CLI interfaces:** session.py is the entry point. No new scripts needed.
- **Do not modify generation code:** This phase is docs-only. If a type fails verification, fix the prompt template, not the generation engine.
- **Do not keep "historical notes" about browser automation:** The cleanup is a complete removal, not a transition note.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Session orchestration | New batch script | `scripts/session.py` `run_session()` | Already handles delay, retry, summary |
| Individual generation | Direct API calls | `scripts/generate_infographic.py` | Already handles preflight, templates, validation |
| Validation | Manual PNG inspection | `scripts/validation.py` | Already does vision-based quality checks |
| Test data | Hand-written JSON | Existing `tests/fixtures/sample-domain-scorecard-data.json` pattern | Extend for other types |

## Common Pitfalls

### Pitfall 1: Incomplete Browser Automation Sweep
**What goes wrong:** Missing references in docs causes confusion -- users see "browser automation" in one place and "API script" in another.
**Why it happens:** References are scattered across 6 files in different contexts (user-facing docs, architecture docs, agent instructions, spawn commands).
**How to avoid:** Use the complete file inventory below. After edits, run the grep pattern again to verify zero matches.
**Warning signs:** Any remaining match for `browser`, `chatgpt.com`, `gemini.google.com`, `platform profile`, `model picker`, `fast-mode`, `conversation` (in Image Agent context), `navigate` (in workflow context).

### Pitfall 2: Breaking Infographics.md Sections That Should Be Kept
**What goes wrong:** Accidentally modifying or removing the 6 infographic specification sections, Output Requirements, Content Mapping, or Multi-Mode Variant.
**Why it happens:** The file is 363 lines and the keep/replace boundary is not obvious.
**How to avoid:** The CONTEXT.md is explicit: Replace Technology (lines 22-68), Attempt Budget (lines 72-90), Browser Automation Workflow (lines 93-140), Error Handling (lines 326-349). Keep everything else.
**Warning signs:** Infographic specifications (lines 144-290) or Content Mapping (lines 352-363) changed.

### Pitfall 3: Inconsistent Terminology in New Docs
**What goes wrong:** New sections use different terms for the same concept (e.g., "generation script" vs "session orchestrator" vs "generate_infographic").
**Why it happens:** Multiple code entry points exist (session.py, generate_infographic.py, CLI).
**How to avoid:** Standardize on: "session orchestrator" for the batch runner, "generation pipeline" for the per-type flow, "scripts/session.py" for the specific file reference.
**Warning signs:** Doc mentions `generate_infographic.py` directly instead of the session orchestrator (per CONTEXT.md decision: agent calls session.py, not individual generation).

### Pitfall 4: Verification Requires Real API Key
**What goes wrong:** Live 6-type verification needs a configured Gemini API key with billing enabled. Tests fail with API_ERROR or preflight failure.
**Why it happens:** The generation pipeline calls the real Gemini API. No mock mode for integration testing.
**How to avoid:** Ensure `.cdp-context/config.md` has a valid API key before verification. Budget for API costs (6 images minimum, up to 18 with retries). Mark live tests with `@pytest.mark.live`.
**Warning signs:** Preflight check fails, 429 rate limits on rapid sequential calls.

## Code Examples

### Infographics.md Technology Section Replacement

Replace the current Technology section (lines 22-68: Platform Profiles table, Prompt Population Workflow, Style Configuration Integration table) with:

```markdown
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
```

### Infographics.md Workflow Section Replacement

Replace the current Browser Automation Workflow (lines 93-140: 8-step browser cycle) with:

```markdown
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
```

### Infographics.md Retry Behavior Section Replacement

Replace the current Attempt Budget section (lines 72-90: hard limits, conversation rules, tracking instruction) with:

```markdown
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
```

### Infographics.md Error Handling Section Replacement

Replace the current Error Handling section (lines 326-349: placeholder on exhaustion, session budget, log status, never block pipeline) with:

```markdown
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
```

### CEO.md Task A Spawn Instruction Replacement

Replace lines 594-599:
```
TaskCreate: "Generate analytical infographics via browser automation
  Read .cdp-context/config.md for platform selection (gemini or chatgpt)
  Use JSON prompt templates from templates/infographic-prompts/
  Read .cdp-context/style.md for visual style overrides if present
  Session output: <absolute-path>  Issue slug: <issue-slug>"            -> Task A
```

With:
```
TaskCreate: "Generate analytical infographics via Gemini API script
  Extract data from Decision Record per infographic type
  Write data JSON files to {session}/images/ per type
  Run scripts/session.py to generate all types
  Session output: <absolute-path>  Issue slug: <issue-slug>"            -> Task A
```

## Browser Automation Reference Inventory

Complete inventory of files and locations requiring edits for DOC-04:

### File 1: `templates/production/infographics.md` (PRIMARY -- DOC-01)
| Line(s) | Content | Action |
|---------|---------|--------|
| 24-25 | Platform field / platform selection reference | Remove |
| 31-37 | Platform Profiles table (Gemini/ChatGPT URLs, model picker, fast-mode) | Remove entirely |
| 53 | "browser automation to the configured platform" | Replace with API script reference |
| 56-68 | Style Configuration Integration mapping table | Replace with brief note |
| 72-90 | Attempt Budget (conversation rules, session-wide limit, tracking) | Replace with Retry Behavior |
| 93-140 | Browser Automation Workflow (8-step browser cycle) | Replace with Generation Workflow |
| 326-349 | Error Handling (session budget, conversation references) | Replace with new Error Handling |

### File 2: `agents/ceo.md` (DOC-03)
| Line(s) | Content | Action |
|---------|---------|--------|
| 595 | "Generate analytical infographics via browser automation" | Replace with API script description |
| 596 | "Read .cdp-context/config.md for platform selection (gemini or chatgpt)" | Remove platform selection reference |

### File 3: `SKILL.md`
| Line(s) | Content | Action |
|---------|---------|--------|
| 427-428 | "via browser automation targeting the configured AI platform (Gemini or ChatGPT)" | Replace with API description |
| 430-434 | "submitting to the platform with a 3-attempt escalation... same conversation" | Replace with script-based description |
| 532 | "Generate analytical infographics via browser automation" | Update spawn text |
| 613-625 | Platform Configuration section (Gemini or ChatGPT references) | Rewrite for API key config |
| 637 | "Platform configuration for Image Agent" | Update description |

### File 4: `README.md`
| Line(s) | Content | Action |
|---------|---------|--------|
| 564-598 | Platform Configuration section with mermaid diagram ("browser automation") | Rewrite for API-based flow |
| 722 | "Browser automation (Gemini or ChatGPT / JSON prompts)" | Replace with "Gemini API (Python script / JSON prompts)" |

### File 5: `docs/README.md`
| Line(s) | Content | Action |
|---------|---------|--------|
| 614 | "browser automation issues" in production re-run description | Update to "API errors" |
| 1394-1425 | Platform Configuration section (Gemini or ChatGPT, mermaid diagram) | Rewrite for API-based flow |
| 1658 | "Browser automation (Gemini or ChatGPT / JSON prompts)" | Replace with "Gemini API (Python script / JSON prompts)" |

### File 6: `docs/ARCHITECTURE.md`
| Line(s) | Content | Action |
|---------|---------|--------|
| 305-309 | Level 3.5: Platform Configuration (Gemini or ChatGPT) | Rewrite for API key config |
| 385 | "Browser automation (Gemini or ChatGPT / JSON prompts)" | Replace with "Gemini API (Python script / JSON prompts)" |

### Verification Grep Pattern
After all edits, this pattern should return ZERO matches (excluding `.planning/` and `.git/`):
```bash
grep -rn --include="*.md" \
  -e "browser.automation" -e "Browser Automation" \
  -e "chatgpt\.com" -e "gemini\.google\.com" \
  -e "Platform Profile" -e "platform selection" \
  -e "model picker" -e "fast-mode" -e "fast mode" \
  -e "ChatGPT" \
  --exclude-dir=.planning --exclude-dir=.git .
```

Note: "conversation" and "navigate" may appear legitimately in other contexts (team lead agent files, capsule structure). Only Image Agent / Task A contexts need removal.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Browser automation (Gemini/ChatGPT web UI) | Direct Gemini API via `google-genai` SDK | Phases 1-3 (this project) | No browser needed, scriptable, retryable |
| Platform selection (Gemini vs ChatGPT) | Gemini-only API | Phase 1 decision | Simplified to single platform |
| Manual conversation-based retry | Automated vision validation + corrective feedback retry | Phase 3 | Quality gate without human inspection |
| Per-infographic conversation management | Session orchestrator with inter-call delay | Phase 3 | Rate limit aware, adaptive delays |

## Open Questions

1. **Test Data for All 6 Types**
   - What we know: One sample data file exists (`tests/fixtures/sample-domain-scorecard-data.json`). Templates exist for all 6 types.
   - What's unclear: Whether test data files exist or need to be created for the other 5 types (routing-diagram, fault-line-map, risk-opportunity-matrix, action-plan-timeline, mode-comparison).
   - Recommendation: Check each template's `{{PLACEHOLDER}}` tokens and create representative data JSON files for each type. This is within Claude's Discretion per CONTEXT.md.

2. **Session.py CLI Entry Point**
   - What we know: `generate_infographic.py` has a CLI (`main()` + `__main__.py`). `session.py` does NOT have a CLI -- only a Python API (`run_session()`).
   - What's unclear: Whether the Image Agent should call session.py as a Python import or if a CLI wrapper is needed.
   - Recommendation: The Image Agent (running as a Claude Code agent) can call `run_session()` directly via Python. No CLI wrapper needed for session.py. The infographics.md doc should describe the Python API, not a CLI command.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 |
| Config file | `pytest.ini` |
| Quick run command | `cd /Volumes/Data/dev/corporate-decision-panel && python -m pytest tests/ -x -m "not live"` |
| Full suite command | `cd /Volumes/Data/dev/corporate-decision-panel && python -m pytest tests/ -x` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DOC-01 | infographics.md updated for API-based flow | manual-only | Visual review of markdown content | N/A -- doc change |
| DOC-03 | ceo.md Task A spawn updated | manual-only | Visual review of markdown content | N/A -- doc change |
| DOC-04 | No browser automation refs remain | smoke | `grep -rn --include="*.md" -e "browser.automation" -e "ChatGPT" --exclude-dir=.planning --exclude-dir=.git . \| wc -l` should equal 0 | N/A -- grep command |
| DOC-04 (verify) | All 6 types generate successfully | integration (live) | `python -m pytest tests/ -x -m live` (if live tests exist) or manual session run | Partial -- existing tests mock API |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/ -x -m "not live"` (existing unit tests still pass)
- **Per wave merge:** Grep verification pattern for zero browser automation matches
- **Phase gate:** All 6 types generate OK or OK+WARN via live session run

### Wave 0 Gaps
- [ ] Test data JSON files for all 6 infographic types (only domain-scorecard exists)
- [ ] Live verification script or test that runs all 6 types through `run_session()`

## Sources

### Primary (HIGH confidence)
- Direct code reading: `scripts/session.py`, `scripts/generate_infographic.py`, `scripts/validation.py` -- all generation code is API-based, zero browser references
- Direct code reading: `templates/production/infographics.md` -- current doc with browser automation workflow (363 lines)
- Direct code reading: `agents/ceo.md` -- current Task A spawn instruction (line 595)
- Direct code reading: `tests/conftest.py`, `tests/fixtures/` -- test infrastructure
- Grep results: 6 files with browser automation references identified

### Secondary (MEDIUM confidence)
- CONTEXT.md decisions: Section-by-section keep/replace mapping from user discussion

### Tertiary (LOW confidence)
- None -- all findings are from direct code/file inspection

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries, all tools already exist
- Architecture: HIGH -- direct code reading of session.py and generate_infographic.py
- Pitfalls: HIGH -- based on actual file inventory and grep analysis
- Browser automation inventory: HIGH -- exhaustive grep with line numbers verified

**Research date:** 2026-03-04
**Valid until:** 2026-04-04 (stable -- documentation-only phase)
