# Codebase Concerns

**Analysis Date:** 2026-03-04

## Tech Debt

**Heavy CEO Agent Prompt**

- **Issue:** The CEO agent definition (`agents/ceo.md`) is 682 lines, containing the full five-phase orchestration protocol, phase definitions, routing logic, decision mode application, and synthesis instructions. This makes it fragile to modification and difficult to test changes in isolation.
- **Files:** `agents/ceo.md`
- **Impact:** Changes to routing logic, phase definitions, or synthesis protocols affect the monolithic CEO agent. A syntax error or prompt change that breaks phase coordination fails silently until tested against a full cascade. Small refinements to phase execution can inadvertently change synthesis weighting.
- **Fix approach:** Refactor CEO orchestration logic into SKILL.md (the authoritative protocol definition) with CEO.md focused solely on synthesis weighting and final decision production. CEO should read or reference the phase protocol rather than embedding it. This separates orchestration specification (maintained once) from synthesis execution (specific to CEO).

**Production Pipeline Dependency on External Skills**

- **Issue:** Tier 2 and Tier 3 artifacts require optional skill dependencies (`docx`, `pdf`, `frontend-design`, `web-design-guidelines`) that are not bundled with CDP. The deliberation cascade completes successfully, but artifact generation fails silently if dependencies are missing.
- **Files:** `templates/production/infographics.md`, `templates/production/board-presentation.md`, `templates/production/board-document.md`, `templates/production/decision-briefing-page.md`, `templates/production/capsule-structure.md`
- **Impact:** Users expecting production artifacts (HTML, PPTX, DOCX, PDFs) after `--produce` flag or Tier 3 deliberation may receive incomplete output. No clear error message signals missing dependencies. The `/cdp:production` re-run command fails to regenerate artifacts without explicit skill installation.
- **Fix approach:** (1) Add pre-flight validation in the production pipeline agents to check skill availability and fail explicitly with a clear install instruction, (2) Document required skills in SKILL.md setup check, (3) Provide a diagnostic command that lists which production tasks will succeed/fail based on installed skills.

**Image Agent Gemini Retry Behavior**

- **Issue:** The infographics specification (`templates/production/infographics.md`) defines hard attempt limits (3 per infographic, 12 per session) to prevent runaway image submissions. However, there is no centralized state tracking across concurrent Image Agent invocations if multiple infographics are submitted in parallel. If an agent submits attempt 2 before another agent has submitted attempt 1, the session budget tracking becomes unreliable.
- **Files:** `templates/production/infographics.md` (lines 73-90)
- **Impact:** Sessions with concurrent image generation can exceed the 12-submission session budget, leading to wasted Gemini API quota. Placeholder fallback logic executes inconsistently. Users cannot rely on the budgets to bound costs predictably.
- **Fix approach:** Implement a per-session submission counter that Image Agents check before each submission (passed in task description or stored in shared context). Fail fast when the limit is reached with explicit messaging. Document that image generation must be sequential, not parallel.

## Known Issues

**Fast Mode Incompatibility with Image Agent**

- **Symptom:** When a Tier 3 deliberation is run in Claude Code fast mode, the Image Agent (production Task A) fails to generate infographics from JSON prompts. The agent may submit the prompt but receives an error or no image output.
- **Files:** `templates/production/infographics.md` (line 37: "Fast-mode warning | Fast mode may not generate images from JSON prompts | N/A")
- **Trigger:** Running `/cdp:deliberate` or `/cdp:panel --produce` in fast mode, allowing the production pipeline to execute
- **Workaround:** (1) Run deliberations in normal (non-fast) mode when infographics are required, or (2) Run deliberation in fast mode, then re-run `/cdp:production` in normal mode to generate only the missing artifacts. Document this prominently in the README quick start section.

**CSO Research Dossier Broadcast Timing Uncertainty**

- **Symptom:** Phase 1.5 (CSO Research Investigation) is conditional on CEO activation. If the CEO activates CSO, Phase 1.5 executes and broadcasts the Research Dossier before Phase 2. However, the CEO's phase definition in `agents/ceo.md` does not have explicit error handling if CSO dispatch fails or times out. C-suite agents proceed to Phase 2 without research data they may be expecting.
- **Files:** `agents/ceo.md` (Phase 1.5 definition)
- **Impact:** In high-complexity decisions where the CEO activates CSO, if CSO execution stalls or errors silently, C-suite agents have no signal that research is missing. They produce domain recommendations without the evidentiary foundation Phase 1.5 was supposed to provide.
- **Fix approach:** Add explicit timeout and error handling in CEO Phase 1.5 execution: (1) Set a max execution time for CSO research, (2) If CSO does not deliver Research Dossier within time window, broadcast an explicit "Research Incomplete" message to all C-suite with items that could not be researched, (3) C-suite agents annotate their recommendations with confidence caveats when CSO research is incomplete.

## Security Considerations

**Company Context Data Exposure**

- **Risk:** The `.cdp-context/company.md` file (created by `install.py` from template) is gitignored by default and contains sensitive business data: financial position, headcount, tech stack, strategic constraints. If a user accidentally commits this file to a public repository, or forwards a session output directory containing `.cdp-context/`, proprietary information is exposed.
- **Files:** `install.py` (line 57: adds `.cdp-context/` to gitignore), `templates/company-context.md`, agents read this at session start
- **Current mitigation:** `.cdp-context/` is gitignored by default; README documents that it "should never be committed"; user must manually protect this directory.
- **Recommendations:** (1) Add a runtime check in the CEO agent: before reading `.cdp-context/company.md`, verify it is not world-readable, (2) Never include company context in session output (`.cdp-output/`) -- document this explicitly, (3) Provide a `--redact` flag for session exports that removes or masks company data, (4) Add a pre-session warning if `.cdp-context/company.md` exists and contains obvious sensitive patterns (e.g., "revenue > $100M", numeric financials).

**Style Configuration Platform Credentials**

- **Risk:** The `.cdp-context/config.md` file (platform configuration for Image Agent) may in the future be extended to include API keys or credentials for Gemini/ChatGPT authentication. Currently, it only specifies platform selection (Gemini vs. ChatGPT), but the precedent is dangerous.
- **Files:** `templates/config-context.md`, `.cdp-context/config.md` (user-created)
- **Current mitigation:** No credentials are currently stored in config.md. The Image Agent uses browser automation and user login, not API authentication.
- **Recommendations:** (1) Document explicitly in `config-context.md` that this file should never contain API keys or secrets, (2) If future versions require authentication, use environment variables or OS credential stores, not config files, (3) Add a .gitignore enforcement check in install.py to catch accidental commits.

## Performance Bottlenecks

**CEO Agent Token Usage for Large Teams**

- **Problem:** The CEO agent (running on Opus) receives the full Phase 0 broadcast including company context (potentially 500+ tokens), issue framing, routing rationale, and all previous phase outputs. In a full Tier 3 deliberation with all 8 C-suite agents and 34 team leads, the CEO's input context can approach 10,000+ tokens before the CEO begins synthesis. This inflates costs and may approach context window limits in future scenarios.
- **Files:** `agents/ceo.md` (Phase 0 broadcast definition, Phase 5 input collection)
- **Cause:** No summarization or truncation of C-suite recommendations before CEO synthesis. CEO receives every finding verbatim.
- **Improvement path:** (1) C-suite agents produce both a full recommendation AND a 2-3 sentence executive summary, (2) CEO reads full recommendations only if ambiguity requires it, (3) For very large panels (9+ C-suite members, if extended), implement a "synthesis layer" where two intermediate synthesizers (e.g., financial cluster: CFO+CAO, operational cluster: COO+VP Delivery) pre-synthesize before CEO reads.

**Team Lead Execution Parallelization**

- **Problem:** Phase 3 (Team Leads Produce Findings) can activate up to 34 Haiku agents in parallel, but there is no explicit coordination mechanism to ensure they complete before Phase 4 begins. If a single team lead times out or executes slowly, all other C-suite agents waiting on Phase 4 are blocked.
- **Files:** `agents/ceo.md` (Phase 3 dispatch and Phase 4 triggering)
- **Cause:** No explicit max turn budget or timeout enforcement at the C-suite parent level. A team lead can consume its 5 maxTurns and never return a finding.
- **Improvement path:** (1) Add explicit timeout (e.g., 5 minutes) for Phase 3 team lead execution, (2) C-suite agents implement timeout handling: if a team lead does not respond within window, mark that finding as "timeout -- confidence: low" and proceed to Phase 4, (3) Document in C-suite agent definitions what to do when team lead findings are partial or missing.

## Fragile Areas

**Routing Table Threshold Conditions**

- **Files:** `config/routing-table.md` (Full-Activation Threshold Conditions section)
- **Why fragile:** Five threshold conditions (Irreversibility, Headcount Impact >30%, Market Position Change, Existential Financial Risk, Domain Uncertainty) are defined in prose but not formally specified. A CEO agent must interpret "irreversibility" (e.g., is a large CapEx irreversible? is market entry?). Disagreement on threshold interpretation can cause unexpected roster activation/deactivation across different issues.
- **Safe modification:** Create a decision tree or checklist for each threshold condition (e.g., "Irreversibility: Can the decision be undone within 12 months at <50% sunk cost? YES=reversible, NO=irreversible"). Add concrete examples for each threshold. Have the CEO explicitly evaluate each threshold in Phase 1 framing output so routing is auditable.
- **Test coverage:** Manual testing only. No automated test cases verify that the same issue type triggers full activation consistently across multiple runs. Add test scenarios: acquire competitor (should trigger Irreversibility), layoff 50% of team (should trigger Headcount), pivot to new market (should trigger Market Position).

**Decision Mode Weighting Consistency**

- **Files:** `config/decision-modes.md`, `agents/ceo.md` (Phase 5 CEO Deliberation, mode-specific prompt injection)
- **Why fragile:** Each decision mode (Guardian, Pioneer, Architect, Analyst, Sentinel) is defined with disposition and resolution pattern, but the actual weighting logic lives in the CEO agent's prompt. If mode definitions in the config file change without corresponding changes to the CEO's prompt implementation, modes may not behave as documented.
- **Safe modification:** Create an explicit mapping table: "Mode X: If [condition], weight [perspective] at [strength]." Run the calibration protocol after any mode changes (documented in `docs/DEVELOPMENT.md`): select a contentious test issue, run with all-modes, verify 3+ modes produce materially different outcomes. Without this verification, mode changes are risky.
- **Test coverage:** Manual calibration only. No automated test framework validates that mode definitions match implementation. Recommend: create test cases for each mode (e.g., "Guardian mode must reject high-risk proposals unless all skeptics approve").

**Multi-Mode Comparison Cost Variability**

- **Files:** `agents/ceo.md` (multi-mode invocation), `config/decision-modes.md` (mode definitions)
- **Why fragile:** Multi-mode comparison (`all-modes`, `guardian vs pioneer`) runs domain analysis once and CEO synthesis N times. However, if domain analysis is very expensive (many C-suite agents, many team leads), the "~1.1x cost" claim in the README may not hold. Actual cost scales with both analysis complexity and mode count. Users making cost predictions based on the README may be surprised.
- **Safe modification:** Document actual cost formula: "Deliberation cost = (1 × Domain Analysis Cost) + (N × CEO Synthesis Cost), where N = number of modes." Provide cost estimates for typical panels (e.g., "4-agent panel: ~$0.XX per analysis, ~$0.XX per synthesis"). Add a `--cost-estimate` flag to pre-flight estimate token usage before executing.
- **Test coverage:** Run a multi-mode comparison deliberation, measure actual token usage, compare to README claim. Document the variance range.

## Scaling Limits

**Maximum Panel Size**

- **Current capacity:** The system is tested and documented with 1 CEO, 8 C-suite agents, and 34 team leads (43 total agents). Each team lead has maxTurns=5.
- **Limit:** Adding more than 8 C-suite agents or more than 34 team leads (or more than ~5 turns per agent) risks context window exhaustion in the CEO agent's Phase 5 synthesis. No formal limit is enforced or tested.
- **Scaling path:** (1) Measure CEO context size for current 43-agent panel (likely 15,000-20,000 tokens), (2) Test with extended panel (e.g., 10 C-suite, 50 team leads) and measure token cost, (3) If context window becomes limiting, implement "synthesis clustering" where intermediate synthesizers pre-aggregate C-suite recommendations before CEO reads them, (4) Document tested maximum panel size in SKILL.md.

**Session Output Directory Growth**

- **Current capacity:** A typical Tier 3 deliberation produces:
  - 1 RECORD.md (~5-10 KB)
  - 6 PNG infographics (~100-300 KB each = ~1-2 MB total)
  - 1 PPTX (~2-5 MB)
  - 1 DOCX (~1-2 MB)
  - 2 PDFs (~3-8 MB total)
  - Total: ~10-20 MB per session
- **Limit:** 100+ sessions in `.cdp-output/` becomes unwieldy. No cleanup or archival mechanism is provided. Users may accidentally fill disk space.
- **Scaling path:** (1) Implement a `--archive` flag for `/cdp:production` that zips old sessions and moves to archive, (2) Provide a cleanup script that removes sessions older than N days, (3) Document disk usage expectations in README, (4) Add a `--no-artifacts` flag to skip production pipeline if the user only wants the Decision Record.

## Dependencies at Risk

**Optional Production Skills -- Unclear Status**

- **Risk:** The production pipeline depends on external Anthropic and Vercel skills (`docx`, `pdf`, `frontend-design`, `web-design-guidelines`, `find-skills`, `skill-creator`). If these skills are archived, removed, or no longer maintained, CDP users cannot generate board documents, presentations, or PDFs. There is no fallback or graceful degradation.
- **Impact:** Tier 2 `--produce` and Tier 3 artifact generation fails without clear error messaging. Users have no way to know whether skills are available before running a deliberation.
- **Migration plan:** (1) Bundle minimal artifact generation into CDP itself (e.g., simple markdown-to-DOCX converter using Python docx library as fallback), (2) Implement fallback: if `docx` skill unavailable, generate plain text report, (3) Document which skills are "nice to have" vs. "required for Tier 3" in README, (4) Add a `--check-dependencies` command that verifies all installed skills are available.

## Test Coverage Gaps

**Untested Tier 2 Routing with Partial Activation**

- **What's not tested:** When a user calls `/cdp:panel finance tech`, only CFO and CTO are activated (plus their team leads). No C-suite thresholds are evaluated. If the CEO's routing table changes, this behavior is not validated. Does the CEO correctly exclude non-requested C-suite members even if the issue meets full-activation thresholds?
- **Files:** `commands/cdp/panel.md`, `agents/ceo.md` (Tier 2 variant of Phase 1 routing logic)
- **Risk:** A change to full-activation thresholds in `config/routing-table.md` could inadvertently affect Tier 2 behavior, activating the CSO for a panel that should be finance+tech only. No test catches this regression.
- **Test scenario:** Create a "major acquisition" test issue. Run `/cdp:panel finance tech: ...`. Verify that only CFO, CTO activated and CSO is not activated. Run again after changing routing table thresholds. Verify behavior doesn't change unless explicitly intended.

**Untested Pre-Mortem Challenge Propagation (Phase 4.5)**

- **What's not tested:** Phase 4.5 (Pre-Mortem Challenge, Tier 3 only) requires C-suite agents to receive summaries of ALL peer recommendations, challenge their own positions, and provide pre-mortem responses. If a C-suite agent times out in Phase 4 before Phase 4.5 begins, do other agents receive incomplete peer summaries? Does the CEO still execute Phase 4.5?
- **Files:** `agents/ceo.md` (Phase 4.5 definition and triggering)
- **Risk:** Pre-mortem responses may be based on incomplete peer context. A test with one C-suite agent timing out could silently break the pre-mortem logic without error messaging.
- **Test scenario:** Simulate a C-suite agent timeout in Phase 4 (e.g., manually inject an incomplete recommendation). Run a Tier 3 deliberation. Verify that Phase 4.5 still executes and that other agents' pre-mortem responses acknowledge the missing input.

**No Validation of Company Context Syntax or Completeness**

- **What's not tested:** The CEO reads `.cdp-context/company.md` at session start if it exists. If the file is malformed, empty, or contains invalid YAML/markdown, the CEO still proceeds without error. No validation ensures the file parses or contains expected sections.
- **Files:** `agents/ceo.md` (Company Context Loading step)
- **Risk:** A user may create `.cdp-context/company.md` with poor syntax (e.g., unclosed markdown tables). The CEO ignores it silently. The user thinks company context is being used when it's not.
- **Test scenario:** Create a malformed `.cdp-context/company.md` (e.g., missing closing `|` in a table). Run `/cdp:consult cfo: ...`. Verify that an error is raised or at least logged, not silently ignored.

**Multi-Mode Sensitivity Interpretation Untested**

- **What's not tested:** Comparative Decision Records (multi-mode) include a "Mode Sensitivity" rating indicating whether evidence speaks for itself (all modes converge) or user risk appetite decides (modes diverge). The interpretation of "material divergence" is undefined. Is 3 modes agreeing and 2 diverging "sensitive"? Is it high sensitivity or low?
- **Files:** `templates/comparative-decision-record.md`, `agents/ceo.md` (multi-mode synthesis)
- **Risk:** Users interpret the Mode Sensitivity rating inconsistently. Two different CDP sessions analyzing similar decisions produce different sensitivity ratings due to undefined criteria.
- **Test scenario:** Create 3 test issues of similar complexity. Run all-modes on each. Extract the Mode Sensitivity rating. Verify that the rating criteria is consistent and explainable (e.g., "High sensitivity if modes diverge on >50% of recommendations").

---

*Concerns audit: 2026-03-04*
