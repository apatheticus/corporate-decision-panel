# Research: Claude Code Agent Teams Capabilities and Constraints

**Requested by:** Arbiter (initial research assignment)
**Date:** 2026-02-22

## Question
What are the technical limits of Agent Teams? How many agents can run simultaneously? What are the communication patterns? What are known constraints or best practices?

## Findings

### Architecture Overview
Claude Code Agent Teams consist of:
- **Team lead**: The main Claude Code session that creates the team, spawns teammates, coordinates work
- **Teammates**: Separate Claude Code instances that each work on assigned tasks
- **Task list**: Shared work items with dependency tracking and auto-unblocking
- **Mailbox**: Inbox-based messaging system for inter-agent communication

Teams are experimental (as of Feb 2026), requiring explicit opt-in via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

### Communication Patterns

1. **Direct Messages (SendMessage)**: One teammate sends to one specific teammate. The primary communication mechanism.

2. **Broadcasts**: One teammate sends to ALL teammates simultaneously. Expensive -- costs scale linearly with team size. Should be used sparingly, only for critical team-wide information.

3. **Shared Task List (TaskCreate, TaskUpdate, TaskList, TaskGet)**: All agents can see task status and claim available work. Tasks have three states: pending, in_progress, completed. Tasks support dependency tracking -- a pending task with unresolved blockedBy cannot be claimed until those dependencies complete. When a blocking task completes, downstream tasks automatically unblock.

4. **Idle Notifications**: When a teammate finishes work and stops, they automatically notify the lead.

5. **Automatic Message Delivery**: Messages are delivered automatically to recipients. No polling required.

### Agent Limits and Scalability

**No documented hard maximum** on number of teammates. The docs show examples with 3-5 teammates. One example spawns "5 agent teammates." Practical limits are driven by:
- **Token cost**: Each teammate is a separate Claude instance with its own context window. Usage scales linearly with active teammates.
- **Coordination overhead**: More agents = more messages = more tokens spent on coordination
- **File conflicts**: Two teammates editing the same file leads to overwrites

**Best practice**: 5-6 tasks per teammate keeps everyone productive. Having clear, non-overlapping file ownership is critical.

### Key Capabilities

1. **Parallel Execution**: Multiple teammates investigate different aspects simultaneously
2. **Self-Coordination**: Teammates claim tasks independently when they finish current work
3. **Dependency Tracking**: Tasks can block other tasks, with auto-unblocking on completion
4. **Direct Inter-Agent Communication**: Unlike subagents, teammates can talk to each other directly
5. **Adversarial Debate**: Teammates can be configured to challenge each other's findings
6. **Plan Approval**: Teammates can be required to plan before implementing; lead approves/rejects
7. **Display Modes**: In-process (single terminal) or split panes (tmux/iTerm2)
8. **Delegate Mode**: Lead restricted to coordination only -- can't write code, only manage tasks and communicate

### Critical Constraints

1. **No Session Resumption**: `/resume` and `/rewind` do not restore in-process teammates. After resuming, the lead may attempt to message non-existent teammates.

2. **No Nested Teams**: Teammates cannot spawn their own teams or teammates. Only the lead manages the team. **This is the biggest constraint for a multi-level org structure.**

3. **One Team Per Session**: A lead can only manage one team at a time.

4. **No Tool Isolation Between Teammates**: All teammates inherit the lead's full permission set. You cannot spawn a read-only "researcher" alongside a full-access "implementer." This is enforced at spawn time and cannot be changed per-teammate.

5. **No Per-Teammate Hooks**: Unlike subagents, teammates cannot have PreToolUse hooks for conditional validation.

6. **No Persistent Memory for Teammates**: Teammates start fresh each time. Subagents support `memory: user|project|local` but teammates do not.

7. **No Skill Preloading**: Teammates rely entirely on the spawn-time prompt. Subagents can preload skills, teammates cannot.

8. **Lead Is Fixed**: Cannot promote a teammate to lead or transfer leadership.

9. **Shutdown Can Be Slow**: Teammates finish their current request/tool call before shutting down.

10. **Task Status Can Lag**: Teammates sometimes fail to mark tasks as completed, blocking dependent tasks.

### Subagents vs. Agent Teams (Key Distinction)

| Aspect | Subagents | Agent Teams |
|--------|-----------|-------------|
| Context | Own window; results return to caller | Fully independent windows |
| Communication | Report results back to main only | Direct teammate messaging |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Tool Restrictions | Full customization per agent | All inherit lead's permissions |
| Hooks | Supported (PreToolUse, etc.) | Not supported |
| Skills | Can preload skills | Cannot preload skills |
| Memory | Persistent memory support | No persistent memory |
| Best for | Focused tasks, cost-effective | Complex work requiring discussion |
| Token cost | Lower (summarized results) | Higher (separate instances) |

### Custom Subagent Configuration (Relevant for Design)
Custom subagents (`.claude/agents/`) support rich configuration via YAML frontmatter:
- `name`, `description`: Identity and delegation trigger
- `tools` / `disallowedTools`: Tool access control
- `model`: `sonnet`, `opus`, `haiku`, or `inherit`
- `permissionMode`: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- `skills`: Preloaded domain knowledge
- `memory`: Persistent cross-session memory (`user`, `project`, `local`)
- `hooks`: Lifecycle hooks for conditional validation
- `maxTurns`: Maximum agentic turns
- `isolation`: `worktree` for isolated git worktree

### Skills System (Relevant for Skill Design)
Skills are defined in `SKILL.md` with YAML frontmatter:
- `name`: Slash command identifier
- `description`: When Claude should use it
- `disable-model-invocation`: Manual-only trigger
- `user-invocable`: Whether users can invoke directly
- `allowed-tools`: Tool restrictions when active
- `model`: Model override
- `context`: `fork` for subagent execution
- `agent`: Which subagent type to use with `context: fork`
- Supports `$ARGUMENTS` substitution, `!`command`` for dynamic context injection
- Supporting files (templates, scripts, references) in skill directory

### Open Feature Request (GitHub Issue #24316)
There is an active feature request to allow agent team teammates to be spawned from `.claude/agents/` definitions, which would enable:
- Per-teammate tool restrictions
- Per-teammate hooks
- Per-teammate persistent memory
- Skill preloading for teammates
- Deterministic role enforcement (not just prompt-based)

**Current status**: Open, not implemented. Workarounds include using subagents instead of teams (loses inter-agent communication) or per-teammate inline overrides.

## Key Takeaways
- **Agent Teams provide the inter-agent communication the Team of Teams concept needs**, but lack the per-agent customization that subagents offer. The ideal solution would combine both.
- **The "no nested teams" constraint is the biggest design challenge** for a multi-level org structure (CEO -> C-suite -> team leads). The skill will need a creative architectural solution, likely using subagents within a team structure, or a staged execution model.
- **Token cost is a real constraint**: 7 C-suite agents + ~35 team leads running simultaneously would be extremely expensive. The design should use tiered models (Haiku for team leads, Sonnet/Opus for C-suite/CEO) and staged execution (not all agents active simultaneously).
- **The Skills system provides the right packaging mechanism** for distributing this as a reusable capability. A skill can include SKILL.md, supporting agent definitions, templates, and scripts.
- **Prompt-only role enforcement is fragile but currently the only option** for agent team teammates. The spec should include robust system prompts with clear boundaries, decision domains, and interaction protocols.

## Sources
| # | Source | URL/Path | What It Contributed |
|---|--------|----------|---------------------|
| 1 | Claude Code Docs - Agent Teams | https://code.claude.com/docs/en/agent-teams | Official documentation, architecture, constraints, best practices |
| 2 | Claude Code Docs - Skills | https://code.claude.com/docs/en/skills | Skills system details, configuration options |
| 3 | Claude Code Docs - Subagents | https://code.claude.com/docs/en/sub-agents | Custom agent configuration, YAML frontmatter, tool restrictions |
| 4 | Addy Osmani - Claude Code Swarms | https://addyosmani.com/blog/claude-code-agent-teams/ | Practical insights, constraints, best practices |
| 5 | GitHub Issue #24316 | https://github.com/anthropics/claude-code/issues/24316 | Feature request for custom agent definitions in teams |
| 6 | alexop.dev - From Tasks to Swarms | https://alexop.dev/posts/from-tasks-to-swarms-agent-teams-in-claude-code/ | Agent team usage patterns |
| 7 | claudefast.com - Agent Teams Guide | https://claudefa.st/blog/guide/agents/agent-teams | Comprehensive practical guide |
| 8 | Medium (Haberlah) - Configure Agent Teams | https://medium.com/@haberlah/configure-claude-code-to-power-your-agent-team-90c8d3bca392 | Configuration patterns |

## Citation Log
- Search: `Claude Code Agent Teams capabilities constraints multi-agent communication patterns`
- Search: `Claude Code skills custom agents CLAUDE.md configuration agent instructions prompts 2025 2026`
- Search: `Claude Code custom agents .claude/agents/ subagent definition YAML configuration`
- Fetched: https://code.claude.com/docs/en/agent-teams (full documentation)
- Fetched: https://addyosmani.com/blog/claude-code-agent-teams/
- Fetched: https://code.claude.com/docs/en/skills (full documentation)
- Fetched: https://code.claude.com/docs/en/sub-agents (full documentation)
- Fetched: https://github.com/anthropics/claude-code/issues/24316
