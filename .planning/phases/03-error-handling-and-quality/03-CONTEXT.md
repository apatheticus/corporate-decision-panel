# Phase 3: Error Handling and Quality - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Make infographic generation reliable across a full 6-infographic session. Transient API failures retry with exponential backoff, content/safety blocks skip cleanly with distinct placeholders, rate limiting prevents 429 storms, and AI vision validation catches bad text rendering. This phase does NOT add new infographic types, modify prompt templates, or update instruction documents — those are Phase 4.

</domain>

<decisions>
## Implementation Decisions

### Placeholder behavior on failure
- White PNG with centered error text identifying which infographic failed (e.g., "INFOGRAPHIC_domain-scorecard — Generation Failed")
- Content/safety blocks use same placeholder but with different error text (e.g., "BLOCKED: content policy") to distinguish from transient failures
- Save prompt as both PROMPT.txt (human-readable) and PROMPT.json (machine-readable with metadata: error code, timestamp, type) for manual retry capability
- Session continues past individual failures — one failure does not block remaining infographics

### Quality validation
- Vision quality pass runs on all 6 infographic types (consistent quality gate)
- Validation checks: send generated image + list of expected data labels (extracted from data JSON) to Gemini vision model; verify labels are present and readable
- Does NOT verify structural correctness (grid layout, timeline ordering) — only data label presence and readability
- Marginal readability (partially truncated labels) passes with warning, does not trigger retry
- On validation failure: re-generate with original prompt PLUS vision model's corrective feedback appended (e.g., "The label X was missing/garbled — ensure it appears clearly")

### Retry budget
- Shared budget: one configurable retry limit (from config.md `Retry Limit` field) covers both transient API errors (429/503) and quality validation retries
- Default 2 retries = 3 total attempts max per infographic
- Content/safety blocks do NOT retry — immediate placeholder, no budget consumed
- Exponential backoff with jitter on 429/503 errors (base delay at Claude's discretion based on Gemini rate limit research)
- Inter-call delay between sequential infographics in a session (configurable vs hardcoded at Claude's discretion)
- Adaptive inter-call delay: if a 429 occurs, double the inter-call delay for remaining images in the session

### Failure summary reporting
- Per-image structured status lines during generation (extending existing GENERATING/PROMPT/IMAGE/SAVED pattern)
- Final summary table after all 6 infographics: type, status (OK/FAILED/BLOCKED), attempts used, output path
- Summary shows overall validation result per image (OK with optional WARN flag, FAILED, BLOCKED) — no per-label details in summary
- Exit code 0 if any infographic succeeded; exit 1 only on total session failure (all 6 failed)
- Warnings count as succeeded — clean reporting model where only hard failures affect status

### Claude's Discretion
- Exponential backoff base delay (research Gemini's typical rate limit windows)
- Inter-call delay: whether hardcoded 3-5s or configurable in config.md
- Vision validation prompt construction (how to format the expected labels for the vision check)
- Where retry logic lives architecturally (wrapper around generate_infographic vs internal)
- Placeholder PNG dimensions and text styling
- Summary table formatting

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/generate_infographic.py`: `generate_infographic()` function with `GenerationResult` dataclass — retry logic wraps or extends this
- `scripts/config.py`: `load_config()` already returns `retry_limit` field — ready for Phase 3 consumption
- `scripts/preflight.py`: `run_preflight()` with `PreflightResult` pattern — same result-dataclass approach for validation
- `ConfigError` with `error_code` + `remediation` — reusable for Phase 3 error classification
- `_status()` function for structured output lines parseable by CEO agent
- `save_prompt()` already saves PROMPT.txt — extend for JSON variant

### Established Patterns
- `GenerationResult` returns result dataclass (not sys.exit) for composability
- `ClientError` catch returns `API_ERROR_{code}` — Phase 3 adds retry around this
- Dual-audience messaging: human-readable + CEO-agent-parseable
- Status line pattern: `STAGE detail` format (GENERATING, PROMPT, IMAGE, SAVED)
- `google.genai` SDK with `genai.Client(api_key=...)` instantiation

### Integration Points
- `generate_infographic()` is the core function to wrap/extend with retry logic
- CEO agent calls the script via CLI — exit codes and status lines are the interface contract
- Config `retry_limit` field already exists in `.cdp-context/config.md` template
- Phase 4 will call this for all 6 types sequentially — inter-call delay must work at that level

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 03-error-handling-and-quality*
*Context gathered: 2026-03-04*
