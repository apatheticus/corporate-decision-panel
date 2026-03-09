# Domain Pitfalls: v1.4 Team Refactor

**Domain:** Adding CEO-as-universal-dispatcher, file-based inter-agent coordination, and bulk agent updates to existing CDP multi-agent framework
**Researched:** 2026-03-08
**Confidence:** HIGH (derived from direct codebase analysis of all 48 agent files, both dispatch protocols, orchestration protocol, reference documents from 2026-03-08 error session, and Claude Code platform documentation)

---

## Critical Pitfalls

Mistakes that cause the dispatch architecture to break, design goals to be silently lost, or regressions in the existing working system.

### Pitfall 1: CEO Becomes an Orchestration Bottleneck (Context Window Exhaustion)

**What goes wrong:** The CEO agent absorbs all dispatch responsibilities previously spread across 9 C-suite agents. In a full Tier 3 engagement with CSO research, the CEO must: create ~8 division teams, dispatch ~8 C-suite agents, poll for sub-question files across ~8 directories, read ~30+ sub-question files, dispatch ~30 team leads with sub-questions in their prompts, monitor for recommendation files, read recommendations, dispatch pre-mortem agents, read pre-mortems, synthesize, write RECORD.md, then manage 4 CCO production waves with polling between each. This is easily 80-100+ tool calls and massive context accumulation in a single session, risking context window exhaustion or auto-compaction that loses critical dispatch state.

**Why it happens:** The original design distributed orchestration load across 10 agents (CEO + 9 C-suite). The new design concentrates it in one. Each sub-question file read, each team lead dispatch prompt (containing the sub-question content), and each recommendation file read adds context. The CEO's context window was already near capacity in Tier 3 sessions with the old architecture.

**Consequences:** CEO auto-compacts mid-session, losing track of which team leads have been dispatched, which divisions are complete, or which sub-question directories still need polling. Late-dispatched divisions may receive inconsistent context. Production pipeline management (4 sequential waves) happens after an already-exhausted deliberation phase.

**Prevention:**
1. Minimize what the CEO reads verbatim. Sub-question files should be SHORT (the context brief + sub-question, not the full CEO framing repeated). Team lead dispatch prompts should reference the sub-question file path rather than embedding full content when possible.
2. The CEO should dispatch team leads using the sub-question file content directly -- do not re-summarize or re-process it. Read file, paste into prompt, dispatch. No analytical overhead.
3. Consider dispatching team leads in batches per division as sub-questions appear, rather than waiting for all C-suite agents to finish writing sub-questions. This spreads the dispatch load temporally.
4. Document explicit turn budget guidance: "Expect ~60-80 tool calls for a full Tier 3. If context pressure is high after deliberation, the CEO should proceed directly to production without re-reading already-synthesized material."

**Detection:** If CEO Decision Records become shallow or miss domain analyses that were dispatched, context pressure is the likely cause. If auto-compaction messages appear in the CEO session transcript, the turn budget is exceeded.

**Phase to address:** Phase 1 (dispatch protocol rewrite) and Phase 3 (CEO agent additions). The dispatch protocol must specify lean sub-question file format. The CEO agent must have turn budget guidance.

---

### Pitfall 2: Sub-Question File Polling Creates a Timing Deadlock

**What goes wrong:** The CEO dispatches C-suite agents as teammates, then must poll `{session}/sub-questions/{role}/` directories to detect when sub-questions are written. But C-suite agents are teammates in their division team, and the CEO is the team lead. If the CEO blocks on polling (repeatedly checking directories), it consumes turns without progressing. If the CEO dispatches all C-suite agents and then tries to poll 8 directories simultaneously, the polling loop becomes expensive and fragile. Worse: if a C-suite agent fails before writing sub-questions, the CEO polls forever for files that will never appear.

**Why it happens:** File-based coordination requires a polling pattern (there is no event-driven notification for file creation in Claude Code). The CEO must balance between "check too often" (wasting turns) and "check too rarely" (delaying team lead dispatch). With 8 divisions running in parallel, the combinatorial polling problem is significant.

**Consequences:** CEO burns 10-20 turns just polling for sub-question files. If one C-suite agent is slow, all downstream team leads in that division are delayed while the CEO polls. If a C-suite agent fails, the CEO may loop indefinitely checking for files that never appear.

**Prevention:**
1. Use `run_in_background: true` for C-suite teammate dispatch. The system sends a task completion notification when each C-suite agent finishes. The CEO should wait for completion notifications, THEN read sub-question files -- not poll during execution. This eliminates the polling problem entirely for the "C-suite writes sub-questions" phase.
2. BUT: This means C-suite agents must write sub-questions AND THEN WAIT for team lead findings. If dispatched with `run_in_background: true`, the C-suite agent's task completes when it finishes all its turns. The C-suite agent needs to stay alive to receive SendMessage from team leads. This is the core tension.
3. Resolution: C-suite agents should NOT be run in background. They are teammates in a team. The CEO dispatches them as teammates (Agent with team_name, NOT run_in_background). The CEO then uses a controlled polling pattern: wait a reasonable period (e.g., 30 seconds), then check all sub-question directories in a single ls sweep, dispatch any ready team leads, repeat. Include a max-poll-cycles limit (e.g., 10 cycles) after which the CEO proceeds with whatever divisions have sub-questions and logs gaps for the rest.
4. Alternatively: C-suite agents could signal completion of sub-question writing by creating a sentinel file like `{session}/sub-questions/{role}/_READY`. The CEO polls for `_READY` files instead of counting individual sub-question files, which is simpler and faster.

**Detection:** If team lead dispatches are delayed by more than 2 minutes after C-suite dispatch, the polling pattern is too slow. If the CEO's turn count exceeds 100 before Phase 4, polling overhead is too high.

**Phase to address:** Phase 1 (dispatch protocol) and Phase 3 (CEO agent). The dispatch protocol must specify the exact polling pattern and sentinel file convention. The CEO agent must have the polling implementation with timeout.

---

### Pitfall 3: C-Suite Agents Lose the Ability to Decide Which Team Leads Are Relevant

**What goes wrong:** In the current architecture, each C-suite agent decides which team leads to dispatch based on the specific decision. The CFO might skip the Tax Lead for a purely operational question. In the new architecture, C-suite agents write sub-question files, and the CEO dispatches team leads. If the CEO dispatches ALL team leads listed in sub-question directories without checking relevance, or if the C-suite agent writes sub-questions for all team leads "just in case," the relevance filtering design goal is lost. Conversely, if the CEO second-guesses the C-suite agent's team lead selection, the domain translation design goal is undermined.

**Why it happens:** The original dispatch mechanism made relevance filtering implicit -- the C-suite agent simply didn't call the Agent tool for irrelevant team leads. In the file-based protocol, relevance filtering requires an explicit convention: either the C-suite agent writes sub-questions ONLY for relevant team leads (absence = irrelevant), or the C-suite agent includes a relevance marker in each file.

**Consequences:** Over-dispatch wastes tokens and time (30+ team leads when 15 would suffice). Under-dispatch misses relevant domain analysis. CEO intervention in team lead selection breaks the C-suite domain translation principle.

**Prevention:**
1. Establish a clear convention: **C-suite agents write sub-question files ONLY for relevant team leads.** The absence of a sub-question file for a team lead means that team lead is not relevant. The CEO dispatches exactly the team leads that have sub-question files. No more, no less.
2. Document this in both the dispatch protocol and every C-suite agent definition. The current language ("Not every question requires all five team leads. Use judgment about which sub-domains are relevant") must be preserved and adapted to the file-writing context.
3. The CEO must NOT add team leads that the C-suite agent did not request, and must NOT skip team leads that have sub-question files. The CEO is a messenger for team lead dispatch, not a decision-maker about team composition.

**Detection:** Compare team lead dispatch counts between the old architecture (from error logs) and the new architecture for the same test issue. If significantly more team leads are dispatched, relevance filtering is broken. If the CEO's dispatch reasoning mentions "I think the CFO should also have the Tax Lead look at this," the CEO is overstepping.

**Phase to address:** Phase 1 (dispatch protocol) and Phase 2 (C-suite agent updates). The dispatch protocol must state the convention explicitly. C-suite agents must be updated to write sub-question files only for relevant team leads.

---

### Pitfall 4: Inconsistent Removal of Old Dispatch Instructions Across 9 C-Suite Agents

**What goes wrong:** The 9 C-suite agent files all contain TeamCreate, Agent tool call, and SendMessage shutdown_request instructions that must be removed and replaced with sub-question file writing. If even one agent retains old instructions, that agent will attempt to use TeamCreate/Agent (which will fail, since it's a teammate without those tools), waste turns on failed tool calls, and potentially not write sub-question files at all -- silently producing an incomplete analysis.

**Why it happens:** The 9 C-suite agents have similar but NOT identical Mode B sections. The CFO has 5 team leads, the CTO has 4, the CSO has 5 research-specific team leads with a different dispatch context (Phase 1.5 vs Phase 2), the CCO has a completely different 4-wave production pattern, etc. A find-and-replace approach will miss agent-specific variations. The CSO is particularly dangerous because it operates in Phase 1.5 (before other C-suite agents) and has research-specific language that differs from analytical team lead dispatch.

**Consequences:** An agent that retains old dispatch instructions will fail at runtime. The failure is silent from the CEO's perspective -- the CEO polls for sub-question files that never appear, eventually times out, and the division is recorded as a gap. The user sees a degraded Decision Record without understanding why.

**Prevention:**
1. Create a transformation checklist for each agent BEFORE starting edits. The checklist should list every block to remove, every block to add, and every block to preserve, specific to that agent.
2. Process agents in order of uniqueness: CCO first (most different), CSO second (Phase 1.5 context), then one "template" analytical agent (CFO), then apply the template pattern to the remaining 6 with agent-specific adaptations.
3. After all 9 agents are updated, run verification greps:
   - `grep -r "TeamCreate" agents/c-suite/` -- should return 0 matches
   - `grep -r "subagent_type" agents/c-suite/` -- should return 0 matches
   - `grep -r "shutdown_request" agents/c-suite/` -- should return 0 matches
   - `grep -r "sub-questions" agents/c-suite/` -- should return matches in all 9 files (confirming new protocol added)
4. Read each updated agent end-to-end to confirm Mode B flow coherence. Do not rely on grep alone -- structural coherence matters more than keyword presence.

**Detection:** Post-update grep verification (above). Additionally, the first test run will immediately reveal any agent that retained old instructions, because it will fail to write sub-question files.

**Phase to address:** Phase 2 (C-suite agent updates). This should be a dedicated phase with its own verification step, not combined with protocol rewrites.

---

### Pitfall 5: CCO Production Pipeline Responsibility Split Creates Ambiguity

**What goes wrong:** The CCO currently owns the entire production pipeline: creating its team, dispatching in waves, reading reports between waves, managing the editorial review gate, and handling revision cycles. In the new architecture, the CEO manages wave dispatch (because only the CEO can use Agent/TeamCreate), but the CCO still owns creative direction, editorial quality, and revision decisions. This creates a split-brain problem: the CEO dispatches agents but the CCO decides what to dispatch and when. If the CEO and CCO disagree about whether to proceed after Wave 3 (Editor returns REVISION REQUIRED), or if the CCO's revision instructions aren't properly relayed through the CEO's dispatch, production quality degrades.

**Why it happens:** The division of responsibility between "who can dispatch" (CEO, platform constraint) and "who should decide what to dispatch" (CCO, domain expertise) is inherently awkward. The original design cleanly put both in the CCO's hands. The new design splits them.

**Consequences:** The CEO dispatches the Writer before the CCO has finished reviewing the Graphic Designer's report. The CEO proceeds to Wave 4 without the CCO's editorial verdict. Revision cycles are skipped because the CEO doesn't understand the CCO's revision instructions. The CCO writes a Creative Brief but the CEO doesn't include it in team lead prompts.

**Prevention:**
1. Define the CEO's role in production as PURELY MECHANICAL. The CEO reads report files, reads CCO directives (written to files), and dispatches the next wave agent with the content the CCO specifies. The CEO does not make production decisions.
2. The CCO should write wave dispatch directives to files: `{session}/_DIRECTIVE_wave2.md`, `{session}/_DIRECTIVE_wave3.md`, etc. Each directive contains: (a) whether to proceed, (b) what to include in the next agent's prompt, (c) any revision instructions. The CEO reads the directive and dispatches accordingly.
3. Alternatively (simpler): The CEO dispatches the CCO as a teammate, and the CCO stays alive throughout production. After each wave agent completes (CEO monitors via report files), the CEO notifies the CCO via SendMessage. The CCO reads the report, makes the quality decision, and writes the next wave's dispatch content to a file. The CEO reads the file and dispatches the next agent. This preserves the CCO's decision authority while using the CEO's dispatch capability.
4. The editorial review gate (APPROVED / APPROVED WITH NOTES / REVISION REQUIRED) must be communicated via file, not assumed by the CEO. The CEO reads `_REPORT_editor.md`, but the CCO interprets the verdict and writes the dispatch directive.

**Detection:** If production artifacts have quality issues that the Editor flagged but the Publisher didn't address, the revision cycle was likely skipped. If the Creative Brief is missing from team lead prompts, the CEO is dispatching without CCO direction.

**Phase to address:** Phase 1 (CCO dispatch protocol rewrite). This must be resolved in the protocol design before any implementation. The protocol must specify the exact file-based handshake between CEO and CCO for each wave transition.

---

### Pitfall 6: Design Goals Silently Lost During Architectural Transition

**What goes wrong:** The three design goals -- (1) engineered dissent via independent C-suite perspectives, (2) expert collaboration via team lead SendMessage within divisions, (3) domain translation via C-suite sub-question formulation -- are preserved "on paper" in the new architecture but subtly degraded in practice. Specifically:

- **Engineered dissent:** C-suite agents are now teammates in CEO-created teams. If the CEO's team-wide context leaks between divisions (it shouldn't, but the team architecture documentation is unclear on this), cross-pollination could reduce independence.
- **Expert collaboration:** Team leads can still SendMessage within their division team. BUT: if the CEO dispatches team leads into the wrong team (e.g., a CFO team lead into the CTO's division team), SendMessage goes to the wrong C-suite agent.
- **Domain translation:** C-suite agents write sub-questions to files instead of embedding them in Agent tool prompts. If the sub-question file format is too structured/rigid, it may constrain the C-suite agent's ability to provide rich context. If too loose, the CEO may not include all necessary context in the team lead dispatch prompt.

**Why it happens:** Architectural changes that preserve function but change mechanism often introduce subtle behavioral shifts. The team-based dispatch is functionally equivalent to the old architecture, but the communication paths are different. Every path change is an opportunity for information loss.

**Consequences:** Decision Records from the new architecture show less analytical depth, less inter-team-lead cross-referencing, or more uniform (less dissenting) C-suite perspectives. These are hard to detect because there's no "crash" -- just gradually lower quality output.

**Prevention:**
1. Document the three design goals prominently in the new dispatch protocol with specific mechanisms that preserve each one:
   - Engineered dissent: Each division team is separate. No cross-division SendMessage. CEO bridges divisions only via recommendation files (unchanged from current).
   - Expert collaboration: Team leads are dispatched into their correct division team (team_name matches). Team leads can SendMessage to peers AND their C-suite parent within the team.
   - Domain translation: Sub-question files contain the C-suite agent's translated question, not the CEO's original framing. The CEO includes the sub-question file content verbatim in the team lead dispatch prompt without modification.
2. The CEO agent must include team lead-to-division mapping to prevent misdispatch. Each team lead must be dispatched with the correct `team_name` matching their C-suite parent's division team.
3. Run a comparative test: same issue, old architecture (inline workaround from 2026-03-08 session) vs new architecture. Compare Decision Record depth, dissent levels, and team lead finding specificity.

**Detection:** Compare analytical depth metrics across pre- and post-refactor sessions. If C-suite recommendations become shorter or more uniform, independence is degraded. If team lead findings are less specific, collaboration or domain translation is broken.

**Phase to address:** Phase 1 (dispatch protocol) and Phase 3 (CEO agent). The protocol must explicitly map design goals to mechanism. The CEO agent must include the division-team mapping table.

---

## Moderate Pitfalls

### Pitfall 7: 48-File Bulk Update Introduces Inconsistent Logging Protocol Text

**What goes wrong:** All 48 agent files reference `config/logging-protocol.md` with slightly different surrounding text. A bulk find-and-replace catches the filepath but produces inconsistent inline summaries because the surrounding context differs across agents. Some agents say "follow the error logging protocol at `config/logging-protocol.md`", others say "follow the logging protocol at `config/logging-protocol.md`", and some have additional context like "after completing your production report." A single replacement string produces grammatically awkward results in some files.

**Why it happens:** The logging protocol reference was added to all 48 agents in a single pass during v1.0, but subsequent edits to individual agents introduced minor variations in the surrounding text. A mechanical replacement treats all 48 as identical when they are not.

**Consequences:** Agents receive slightly confusing instructions. An agent that reads "follow the error logging protocol: if `LOGGING: ON`... after completing your production report" when it's not a production agent may be confused about timing. This is unlikely to cause failures but degrades instruction clarity.

**Prevention:**
1. Before replacing, grep for the exact text variants across all 48 files. Count how many unique surrounding-context patterns exist.
2. Create 2-3 replacement templates that match the major variants (C-suite agents, analytical team leads, production team leads).
3. After replacement, read the logging section of at least one agent from each category (C-suite, analytical team lead, production team lead) to verify the inline summary reads naturally in context.
4. The inline summary should be self-contained: "If `LOGGING: ON` and `SESSION PATH:` appear in your prompt, write `{session-path}/logs/errors-{YYYYMMDD-HHmm}-{agent-name}.md` as your last action before completing. Log only tool failures, workarounds, data quality issues, or instruction ambiguity. If no issues, do not create a log file."

**Detection:** After replacement, grep for `config/logging-protocol.md` -- should return 0 matches across agents. Then spot-check 3-4 files from different categories for natural reading.

**Phase to address:** Should be its own dedicated phase (bulk update), separate from the dispatch architecture changes. Mixing bulk text updates with structural protocol changes increases error risk.

---

### Pitfall 8: Sub-Question File Path Convention Conflicts with Session Resume Protocol

**What goes wrong:** The session resume protocol (in orchestration-protocol.md) uses file-based state scanning to detect how far a session progressed: `_RECOMMENDATION_*.md` files indicate Phase 4, `_PREMORTEM_*.md` files indicate Phase 4.5, `RECORD.md` indicates Phase 5. The new sub-question files (`{session}/sub-questions/{role}/{team-lead}.md`) introduce a new state layer. If the resume protocol doesn't account for sub-question files, a resumed session may re-dispatch C-suite agents that already wrote sub-questions, causing duplicate team lead dispatch.

**Why it happens:** The resume protocol was designed before the sub-question file convention existed. Adding new file-based state without updating the resume detection logic creates a gap.

**Consequences:** A session that crashed after C-suite agents wrote sub-questions but before team leads were dispatched cannot be correctly resumed. The CEO re-dispatches C-suite agents, which may produce different sub-questions (non-deterministic LLM output), leading to different team lead analyses and ultimately a different Decision Record than would have been produced without the crash.

**Prevention:**
1. Add sub-question files to the resume protocol's detection logic. New rule: "If `{session}/sub-questions/{role}/` directories contain files but no `_RECOMMENDATION_{role}.md` exists, the C-suite agent completed sub-question writing but team leads haven't been dispatched. Resume by dispatching team leads using existing sub-question files."
2. This rule should be inserted between the current rules 1 (no recommendations) and 2 (some recommendations missing).
3. The resume protocol update should be included in the orchestration-protocol.md changes, not deferred.

**Detection:** Test resume: create a session directory with sub-question files but no recommendations. Run `/cdp:resume`. If it re-dispatches C-suite agents instead of team leads, the resume protocol is not sub-question-aware.

**Phase to address:** Phase 1 (orchestration protocol update). Must be included in the Phase 2/3/4 surgical updates to orchestration-protocol.md.

---

### Pitfall 9: Infographic Slug Alias Map Creates a Permanent Workaround Layer

**What goes wrong:** Adding `SLUG_ALIASES` to `generate_infographic.py` and `session.py` fixes the immediate mismatch, but creates a permanent compatibility layer that masks future slug naming errors. If a new infographic type is added with the wrong slug, the alias map silently resolves it, and the developer never knows they used the wrong slug. Over time, the alias map grows with more workarounds rather than fixing the root cause.

**Why it happens:** Defensive programming ("accept anything, produce something") is the right instinct for production robustness but the wrong instinct for configuration correctness. The alias map treats a configuration error (wrong slug in agent definition) as a runtime resolution problem.

**Consequences:** The graphic designer agent definition drifts further from the actual template slugs. New contributors read the agent definition, use the wrong slugs in other contexts, and rely on the alias map to fix them. The alias map becomes a source of truth instead of the template directory.

**Prevention:**
1. Fix the root cause FIRST: update `agents/team-leads/cco/graphic-designer.md` to use the correct slugs (`fault-line-map`, `risk-opportunity-matrix`, `action-plan-timeline`).
2. THEN add the alias map as a TEMPORARY compatibility layer with a deprecation warning: `warnings.warn(f"Slug '{type_slug}' is deprecated, use '{SLUG_ALIASES[type_slug]}' instead", DeprecationWarning)`.
3. Add a comment in the alias map: "These aliases exist to support old agent definitions. They should be removed once all agent definitions use canonical slugs."
4. Consider NOT adding the alias map if the graphic designer agent definition is the only place that uses the wrong slugs. If the fix is contained to one file, a compatibility layer is overkill.

**Detection:** If the alias map grows beyond the initial 3 entries without new infographic types being added, slug naming discipline has been lost.

**Phase to address:** Phase 1 (quick win fixes). Fix the agent definition first, then decide whether the alias map is necessary for robustness.

---

### Pitfall 10: CSO Phase 1.5 Dispatch Doesn't Fit the Division Team Pattern

**What goes wrong:** The CSO operates in Phase 1.5 (before other C-suite agents), dispatching research team leads to gather evidence before the Phase 0 broadcast. In the new architecture, the CEO creates a CSO division team and dispatches the CSO as a teammate. But: the CSO needs to complete BEFORE other C-suite agents are dispatched (its Research Dossier feeds the Phase 0 broadcast). If the CEO creates all division teams and dispatches all C-suite agents simultaneously, the CSO's output arrives too late to be included in the broadcast.

**Why it happens:** The CSO has a fundamentally different timing requirement than other C-suite agents. Other C-suite agents are dispatched in parallel during Phase 2. The CSO is dispatched alone during Phase 1.5 and must complete before Phase 2 begins. The "CEO dispatches all C-suite agents" pattern works for Phase 2 but not for the CSO's Phase 1.5 role.

**Consequences:** If the CSO is dispatched with other C-suite agents, the Research Dossier is not available for the Phase 0 broadcast. Other C-suite agents make assumptions without evidence, producing lower-quality domain analyses. The CSO's entire purpose is undermined.

**Prevention:**
1. The CSO must be dispatched FIRST, in its own division team, as a separate dispatch action. The CEO creates the CSO division team, dispatches the CSO, waits for the Research Dossier, THEN creates other division teams and dispatches other C-suite agents with the dossier included in the broadcast.
2. The dispatch protocol must explicitly call out the CSO as a special case with Phase 1.5 sequencing requirements.
3. The CSO's sub-question file protocol works the same as other C-suite agents (CSO writes sub-questions for research team leads, CEO dispatches them), but it happens in Phase 1.5, not Phase 2.
4. The CEO agent must have clear sequencing: Phase 1 (frame/route) -> Phase 1.5 (CSO division if CSO activated) -> Phase 0 broadcast (with Research Dossier if available) -> Phase 2 (all other divisions in parallel).

**Detection:** If the Phase 0 broadcast doesn't include Research Dossier findings when the CSO was activated, the CSO was dispatched too late.

**Phase to address:** Phase 1 (dispatch protocol and orchestration protocol). The CSO's special timing must be designed into the protocol, not treated as an afterthought.

---

### Pitfall 11: Orchestration Protocol Surgical Updates Create Internal Contradictions

**What goes wrong:** The orchestration protocol (436 lines) needs "surgical updates" to Phases 2, 3, 4, and the Production Spawn Sequence, while leaving Phases 0, 1, 1.5, 4.5, 5, and the resume protocol largely intact. But the Phase descriptions reference each other: Phase 2 says "C-suite agents are dispatched by the CEO as standalone background subagents," Phase 3 says "Team leads report to their C-suite parent via SendMessage," Phase 4 says "CEO dispatches all C-suite agents as background subagents (run_in_background: true)." If Phase 2 is rewritten to say "C-suite agents are dispatched as teammates" but Phase 4's synchronization section still says "background subagents with run_in_background: true," the protocol contradicts itself.

**Why it happens:** Surgical edits to a long document with internal cross-references inevitably miss some references. The orchestration protocol was written as a coherent whole; editing parts while preserving others creates seams.

**Consequences:** The CEO reads the protocol and encounters contradictory instructions about dispatch mechanism. It may follow the first instruction encountered (due to primacy bias), which might be a stale reference in an unedited section.

**Prevention:**
1. After all surgical edits, do a full read-through of the entire orchestration protocol. Every reference to "standalone background subagent," "without team_name," "run_in_background: true," "TeamCreate," and "Agent tool" must be checked for consistency with the new architecture.
2. Search for these specific terms and verify each occurrence:
   - "standalone" -- should only appear in historical context or the CSO Phase 1.5 description (if CSO remains standalone)
   - "without team_name" -- should not appear in C-suite dispatch context
   - "run_in_background" -- verify usage is correct for the new teammate-based dispatch
   - "TeamCreate" -- should appear ONLY in the CEO's dispatch actions, not in C-suite agent descriptions
3. The Phase 4 Synchronization section is particularly dangerous because it describes how the CEO waits for C-suite agent completion. The synchronization mechanism changes from "background task completion notifications" to "monitoring for recommendation files" (or remains the same if teammates can be run in background).

**Detection:** Read the complete orchestration protocol after edits and flag any sentence that describes an agent dispatch mechanism. If two sentences describe different mechanisms for the same dispatch, there is a contradiction.

**Phase to address:** Phase 1 (orchestration protocol update). Verification step after all surgical edits.

---

### Pitfall 12: Team Lead Agent Path References Become Stale

**What goes wrong:** All C-suite agent definitions reference team lead agent paths like `.claude/agents/team-leads/cfo/{agent-name}.md` in their sub-question prompt templates. These paths are correct when the skill is installed to `.claude/`, but may be wrong if the installation path changes or if the skill is used as a plugin. In the new architecture, the CEO -- not the C-suite agent -- includes this path reference in the team lead dispatch prompt. If the CEO copies the path from the sub-question file without validating it, and the path is wrong, every team lead gets an invalid agent definition reference.

**Why it happens:** Agent definition paths are currently embedded in C-suite agent files as literal strings. The path is correct for the standard installation but is not dynamically resolved.

**Consequences:** Team leads cannot find their agent definition and may produce generic analysis instead of their specialized analytical framework output. The output looks reasonable but lacks the specific forcing questions, domain-specific lenses, and output template structure that make team lead analysis valuable.

**Prevention:**
1. Keep the path references in C-suite agent definitions AS-IS. The CEO already knows the correct skill installation path (it's the CEO's own agent definition directory). The C-suite agent writes the path in its sub-question file; the CEO includes it in the dispatch prompt.
2. Alternatively: The CEO can substitute the correct base path when building team lead dispatch prompts, using its knowledge of the actual installation directory. This makes the CEO responsible for path correctness but centralizes the fix.
3. Do NOT try to make paths dynamic within the markdown files -- LLM agents cannot reliably perform path interpolation.

**Detection:** If team lead outputs lack the structured analytical framework (forcing questions, specific output template sections), they may not be reading their agent definitions correctly.

**Phase to address:** Phase 3 (CEO agent additions). The CEO's dispatch prompt template should include the correct agent definition path.

---

## Minor Pitfalls

### Pitfall 13: PDF Module Path Fix Is Fragile Across Installation Methods

**What goes wrong:** The fix for `scripts.build_results_pdf` ModuleNotFoundError is to add `cd <skill-directory> &&` prefix to the Publisher agent's invocation. But `<skill-directory>` is a placeholder that must be resolved at runtime. If the Publisher agent doesn't receive the skill directory path in its dispatch prompt, or if the path contains spaces, the fix fails.

**Prevention:** Include the skill directory absolute path in the Publisher's dispatch prompt (already done for the Graphic Designer). Verify the path uses double quotes in the bash command to handle spaces: `cd "<skill-directory>" && python3 -m scripts.build_results_pdf`.

**Phase to address:** Phase 1 (quick win). Verify the Publisher receives the same path context as the Graphic Designer.

---

### Pitfall 14: Validation Leniency Scope Creep

**What goes wrong:** Adding `LENIENT_TYPES` to `validate_infographic()` for routing diagrams is the right fix, but developers later add every infographic type that ever fails validation to the lenient set. Eventually, validation is lenient for all types, making the quality gate meaningless.

**Prevention:** Document that `LENIENT_TYPES` is for infographic types that have inherently high text density where PARTIAL labels are expected and acceptable. Add a comment: "Only types with 6+ distinct text labels should be lenient. If a simple infographic is failing, the issue is generation quality, not validation strictness."

**Phase to address:** Phase 1 (code fix). Add the guard comment when creating the LENIENT_TYPES set.

---

### Pitfall 15: Large File Read Guidance Doesn't Reach Team Leads

**What goes wrong:** The guidance about using Read with `offset`/`limit` for large recommendation files is added to the orchestration protocol and CEO agent. But team leads also produce large files (particularly the Writer and Graphic Designer reports). The Editor, which reads ALL prior wave reports, may hit the same truncation issue. The guidance needs to reach production team leads, not just the CEO.

**Prevention:** Include the Read offset/limit guidance in the dispatch protocol (for general awareness) AND specifically in the Editor agent definition (which reads multiple large report files). The inline logging protocol update (48-file bulk change) could include a brief mention: "If reading large files, use Read with offset/limit parameters."

**Phase to address:** Phase 1 (documentation fix). Include in the logging protocol inline summary if practical, or add to the Editor agent definition specifically.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Dispatch protocol rewrite | #2: Polling deadlock, #3: Relevance filtering lost, #10: CSO timing | Design polling pattern with sentinel files, state convention for relevance, CSO special-case Phase 1.5 |
| CCO dispatch protocol rewrite | #5: Split responsibility, CEO/CCO handshake | Define CEO as mechanical dispatcher, CCO writes wave directives to files |
| Orchestration protocol surgical updates | #8: Resume protocol gap, #11: Internal contradictions | Add sub-question file state to resume detection, full read-through after all edits |
| CEO agent additions | #1: Context exhaustion, #6: Design goals lost, #12: Path references | Lean sub-question format, division-team mapping table, correct agent definition paths |
| C-suite agent updates (9 files) | #4: Inconsistent removal | Per-agent transformation checklist, CCO and CSO first, grep verification |
| 48-file logging bulk update | #7: Inconsistent replacement text | Category-based templates, spot-check 3-4 files from different agent types |
| Slug alias fix | #9: Permanent workaround layer | Fix root cause first, add alias with deprecation warning only if needed |
| Validation leniency | #14: Scope creep | Document criteria for lenient types, guard comment |

## Integration Risk Matrix

| If You Change... | Watch Out For... | Why |
|------------------|------------------|-----|
| dispatch-protocol.md (#2, #3) | orchestration-protocol.md (#11) | Protocol describes dispatch flow that orchestration protocol references. Inconsistency between the two is invisible until runtime. |
| cco-dispatch-protocol.md (#5) | CEO agent (#1) | CEO must implement the CCO wave management pattern. Protocol and agent must agree on the file-based handshake. |
| orchestration-protocol.md Phases 2-4 (#11) | Session resume protocol (#8) | Resume uses file-based state detection that must account for new sub-question files. |
| C-suite agents (#4) | dispatch-protocol.md (#3) | C-suite agents reference the dispatch protocol. If the protocol describes a different sub-question convention than the agents implement, files won't match expectations. |
| CEO agent team lead dispatch (#6) | C-suite agent team lead tables (#4) | CEO must know which team leads belong to which division. If C-suite agent tables are edited and CEO mapping isn't updated, team leads go to wrong teams. |
| 48-file logging update (#7) | C-suite agent updates (#4) | If both changes happen in the same phase, there's a risk of editing the same file twice with conflicting changes. Do logging update BEFORE dispatch changes. |
| Slug alias fix (#9) | Graphic designer agent (#4) | Fix the agent definition slugs AND the alias map. If only the alias map is added, the agent definition still has wrong slugs that confuse future editors. |

## Sources

- `agents/ceo.md` -- CEO agent structure, 361 lines (direct reading)
- `config/orchestration-protocol.md` -- Full orchestration protocol, 436 lines (direct reading)
- `config/dispatch-protocol.md` -- Current dispatch protocol, 115 lines (direct reading)
- `config/cco-dispatch-protocol.md` -- CCO production dispatch, 198 lines (direct reading)
- `agents/c-suite/*.md` -- All 9 C-suite agent files (direct reading, dispatch sections analyzed)
- `agents/team-leads/cco/graphic-designer.md` lines 45-68 -- Slug mismatch source (direct reading)
- `config/logging-protocol.md` -- Canonical logging protocol, 124 lines (direct reading)
- `ref/team-refactor-context-260308.md` -- Full error analysis from 2026-03-08 session (direct reading)
- `ref/team-refactor-plan-260308.md` -- Implementation plan with all file changes (direct reading)
- `.planning/research/PITFALLS.md` (v1.1) -- Prior pitfall analysis for CEO extraction (direct reading)
- [Claude Code Subagent Documentation](https://code.claude.com/docs/en/sub-agents) -- Official platform constraint confirmation: "Subagents cannot spawn other subagents"
- [GitHub Issue #4182: Sub-Agent Task Tool Not Exposed](https://github.com/anthropics/claude-code/issues/4182) -- Platform limitation details and community workarounds
- [Multi-Agent Coordination Patterns](https://tacnode.io/post/ai-agent-coordination) -- File-based coordination race conditions and single-writer ownership pattern
