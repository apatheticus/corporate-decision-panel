# Phase 2: API Integration - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Build `scripts/generate_infographic.py` that accepts a template type, a data JSON file, and an output path, then generates a single infographic via the Gemini API and writes a valid PNG (2000px+ on longest edge). The Domain Scorecard type must generate with real Decision Record data. Aspect ratios are set per infographic type; thinking mode is active for Fault-Line Map and Mode Comparison. This phase does NOT handle retries, rate limiting, quality validation, or batch generation — those are Phases 3 and 4.

</domain>

<decisions>
## Implementation Decisions

### Prompt serialization
- Flatten JSON templates to natural language prompts (not raw JSON, not structured text blocks)
- Include hex color codes from template `extras.color_mapping` in the prompt for brand consistency (e.g., "Use #2E7D32 for Approve, #C62828 for Oppose")
- Always save the assembled prompt to `{output_dir}/INFOGRAPHIC_<type-slug>_PROMPT.txt` alongside the PNG, for debugging and iteration

### Data input contract
- CEO agent (or Image Agent) creates a data JSON file with populated placeholder values extracted from the Decision Record
- Script reads the data JSON file path as input — it does not extract data from RECORD.md itself
- Script is a pure function: template type + data file + output path → PNG

### Style override integration
- If `.cdp-context/style.md` exists, append its contents to the generated prompt as additional style guidance
- style.md is optional — if absent, generate with template defaults only

### Pre-generation flow
- Auto-run preflight before generation by default
- Provide `--skip-preflight` flag for when CEO agent has already validated in the session
- Hard stop on preflight failure — no PNG produced, no placeholder, operator must fix config
- Print structured status lines during generation: GENERATING, PROMPT assembled, IMAGE received, SAVED — parseable by CEO agent

### Script architecture
- Expose an importable Python function `generate_infographic(type, data_path, output_path, skip_preflight=False)` as the core API
- CLI wrapper via `python -m scripts.generate_infographic` for standalone invocation
- Matches Phase 1 pattern where `run_preflight()` is both importable and CLI-accessible

### Claude's Discretion
- Data layout in prompt: inline vs separate data section — pick what produces better images
- Quality cue selection: which `quality_keywords` and `technical` specs are meaningful for Gemini image gen vs noise
- CLI interface details: exact flag names, positional vs named arguments
- Data JSON schema: whether to use template `{{PLACEHOLDER}}` token names or a cleaner schema
- Whether to include `.cdp-context/company.md` context in the prompt for branding
- Module structure within `scripts/` (new file vs extending existing)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/config.py`: `load_config()` returns `api_key`, `model_id`, `retry_limit` — direct import for generation
- `scripts/preflight.py`: `run_preflight()` returns `PreflightResult` dataclass — designed for Phase 2 auto-run
- `google.genai` SDK already imported and used in preflight — same client pattern for image generation
- 6 JSON prompt templates in `templates/infographic-prompts/*.json` with core/style/technical/composition/quality_keywords/extras structure
- `{{PLACEHOLDER}}` token syntax in templates: `{{DOMAIN_RECOMMENDATIONS}}`, `{{ACTIVATED_ROLES}}`, etc.

### Established Patterns
- `scripts/` Python package with `__init__.py` — new modules go here
- `ConfigError` with `error_code` + `remediation` for dual-audience errors (human + CEO agent)
- `PreflightResult` dataclass returns result (not sys.exit) for importability
- `genai.Client(api_key=api_key)` client instantiation pattern from preflight.py
- `types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=...)` for image generation calls

### Integration Points
- `preflight.py` Step 4 already does a minimal image generation probe — same API pattern scales to full generation
- Output path convention: `{session}/images/INFOGRAPHIC_<type-slug>.png` — script must match this
- `templates/production/infographics.md` Task A spec describes how Image Agent invokes generation — Phase 4 updates this
- `agents/ceo.md` Task A spawn instruction — Phase 4 updates to reference the script

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 02-api-integration*
*Context gathered: 2026-03-04*
