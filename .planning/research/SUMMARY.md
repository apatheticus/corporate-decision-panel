# Research Summary: v1.4 Team Refactor

**Domain:** Division team dispatch architecture, slug alias resolution, validation leniency, inline logging protocol, production fixes
**Researched:** 2026-03-08
**Overall confidence:** HIGH

## Executive Summary

The v1.4 milestone addresses a fundamental architectural failure discovered during the 2026-03-08 production session: Claude Code enforces a strict "no nested teams" constraint where only the main session (the lead) can use TeamCreate and Agent tools. Teammates and subagents cannot spawn further agents. This makes the current three-tier dispatch architecture (CEO dispatches C-suite as standalone subagents, C-suite creates division teams, C-suite dispatches team leads) impossible. Three of four error-producing agents in the session independently confirmed this limitation.

The fix is an architectural inversion: the CEO becomes the universal dispatcher, creating all division teams and dispatching all agents (both C-suite and team leads). C-suite agents become teammates within CEO-created division teams who communicate domain-specific sub-questions via files rather than via Agent tool calls. This preserves the three design goals (engineered dissent, expert collaboration, domain translation) while working within the platform constraint.

The critical finding for the technology stack is that zero new library dependencies are needed. All fixes operate within the existing Python stdlib, google-genai SDK, Pillow, reportlab, and pytest footprint. The changes fall into two categories: (1) small Python code modifications to three scripts (slug aliases in generate_infographic.py/session.py, validation leniency in validation.py/generate_infographic.py), and (2) large-scale markdown specification rewrites across 48+ agent/config files.

Five additional production fixes accompany the dispatch rewrite: infographic slug alias resolution (3 wrong slugs), PDF module path fix (1-line publisher agent change), inline logging protocol (48-file bulk update removing file-path dependency), validation leniency for high-density infographics (routing diagram PARTIAL labels), and large file read guidance (documentation addition).

## Key Findings

**Stack:** Zero new dependencies. Python stdlib + existing google-genai + Pillow + reportlab + pytest. All code changes are modifications to existing scripts (validation.py, generate_infographic.py, session.py). All other changes are markdown specification edits.

**Architecture:** CEO-as-universal-dispatcher with file-based sub-question protocol. C-suite agents write sub-question files; CEO polls for files and dispatches team leads. CCO production pipeline moves from CCO-managed to CEO-managed wave sequencing. Team lead definitions require zero changes (dispatch mechanism is transparent to them).

**Critical pitfall:** CEO context window exhaustion. The CEO absorbs all dispatch responsibilities previously spread across 9 C-suite agents. A full Tier 3 with 7 divisions of 4 team leads each = 28 team lead dispatches + 7 C-suite dispatches + polling turns + production waves. Keep CEO agent lean (instructions reference protocol files, not embed them). Keep sub-question files short.

## Implications for Roadmap

Based on research, suggested phase structure:

1. **Quick Wins** - Slug aliases + PDF path + validation leniency
   - Addresses: Fix 1 (slug aliases), Fix 2 (PDF path), Fix 5 (validation leniency)
   - Avoids: Touching files that the dispatch rewrite will modify
   - Rationale: These are independent code/config fixes that prevent the exact production failures seen on 2026-03-08. They can ship immediately and reduce regression risk during the larger dispatch rewrite. Slug aliases and validation leniency touch the same Python files (generate_infographic.py, validation.py) so grouping them avoids merge conflicts.

2. **Bulk Agent Update** - Inline logging protocol
   - Addresses: Fix 3 (inline logging)
   - Avoids: Combining with dispatch rewrite (both touch C-suite agent files)
   - Rationale: 48-file bulk update with a single, identical replacement pattern. Do BEFORE the dispatch rewrite so the C-suite agent rewrites in Phase 3 use the new inline protocol text. If done after the dispatch rewrite, the C-suite files would need to be re-edited.

3. **Dispatch Architecture Rewrite** - Division team dispatch + CEO wave management
   - Addresses: Fix 4 (dispatch architecture) including sub-question file protocol and CCO wave sequencing
   - Avoids: Pitfalls #1 (CEO overload), #2 (polling deadlock), #3 (stale patterns), #4 (CCO role confusion)
   - Rationale: This is the core change. Internal sub-order is critical:
     a. `config/dispatch-protocol.md` -- sets the sub-question file convention
     b. `config/cco-dispatch-protocol.md` -- sets the CEO wave management convention
     c. `config/orchestration-protocol.md` -- references (a) and (b), rewrites Phases 2/3/4
     d. `agents/ceo.md` -- implements (a), (b), (c) in CEO instructions
     e. `agents/c-suite/*.md` (all 9) -- transforms Mode B dispatch sections
     f. Verification grep pass

4. **Documentation** - Large file read guidance
   - Addresses: Fix 6 (large file guidance)
   - Avoids: Double-editing orchestration-protocol.md and ceo.md
   - Rationale: Apply after Phase 3 because both files (orchestration-protocol.md, ceo.md) are heavily modified in the dispatch rewrite. Adding documentation to a moving target creates merge conflicts. Adding it after the rewrite is settled is clean.

**Phase ordering rationale:**
- Phase 1 before Phase 2: Quick wins ship independently and prove the Python test suite still passes
- Phase 2 before Phase 3: Inline logging update prevents double-editing C-suite agents
- Phase 3 internal ordering (a-b-c-d-e-f): Protocol specs before agent definitions (agents reference protocols)
- Phase 4 after Phase 3: Documentation additions go into files that Phase 3 stabilized

**Research flags for phases:**
- Phase 1: Standard code changes, unlikely to need deeper research. Existing test patterns cover everything.
- Phase 2: Bulk text operation. Verify 48 files with grep after completion. Low risk per file.
- Phase 3: Needs careful attention to CSO Phase 1.5 special timing (dispatched before other C-suite agents). Needs resolution on CEO polling pattern (simple polling vs. sentinel files). Needs clarity on CCO-CEO file-based handshake for production wave management.
- Phase 4: Trivial documentation. No research needed.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Zero new dependencies confirmed by direct codebase reading. All changes are modifications to existing files. |
| Features | HIGH | All features driven by documented production errors with specific line-level references to affected code and agent definitions. |
| Architecture | HIGH | Platform constraint confirmed by three independent agent failures. Selected architecture (CEO-as-universal-dispatcher) was analyzed against three alternatives and chosen by user. |
| Pitfalls | HIGH | Pitfalls derived from direct analysis of the dispatch flow, polling semantics, file naming conventions, and CEO context budget. Critical pitfalls (#1 CEO overload, #2 polling deadlock, #3 stale patterns) are structurally inherent to the architectural inversion. |
| Build order | HIGH | Dependency analysis based on which files each fix modifies and where semantic conflicts arise. |

## Gaps to Address

- **CEO polling pattern resolution:** The exact polling mechanism (simple directory listing vs. sentinel `_READY` files vs. background task completion notifications) needs resolution during Phase 3 implementation. Research suggests simple polling with timeout is sufficient, but the protocol must be explicit.
- **C-suite agent lifetime management:** When a C-suite agent is dispatched as a teammate, it must remain alive long enough to receive team lead findings via SendMessage. The `maxTurns` setting and expected wait time need tuning based on team lead analysis duration.
- **CCO-CEO production handshake:** The exact file-based protocol for CCO editorial decisions (APPROVED / REVISION REQUIRED) being communicated to the CEO for wave gating needs detailed design in the cco-dispatch-protocol.md rewrite.
- **Session resume protocol update:** The resume protocol uses file-based state detection. Adding sub-question files as a new state layer requires updating the resume detection logic. This should be addressed in the Phase 3 orchestration protocol update but is easy to overlook.
- **CSO Phase 1.5 integration:** The CSO has unique timing requirements (dispatched before Phase 2, Research Dossier feeds Phase 0 broadcast). The dispatch protocol must handle CSO as a special case, not a generic C-suite agent.
