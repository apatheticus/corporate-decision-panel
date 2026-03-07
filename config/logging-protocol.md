# Agent Error Logging Protocol

This document defines the shared error logging behavior for all CDP agents. It is the single source of truth for log format, activation, and writing mechanics.

---

## Activation

Agent logging is active for your session when **both** of the following appear in your prompt or the Phase 0 broadcast:

1. `LOGGING: ON`
2. `SESSION PATH: <absolute-path>`

**You do NOT read config files to determine logging status.** The CEO reads `.cdp-context/config.md` once per session and broadcasts the status. If your prompt does not contain both signals, logging is not active -- take no logging action.

---

## When to Log

Create a log file **only** when you encounter one or more of these during execution:

- **Tool failures**: A tool call returns an error, times out, or produces unexpected output
- **Workarounds applied**: You had to deviate from your standard workflow to complete a task
- **Data quality issues**: Input data was malformed, missing, ambiguous, or inconsistent
- **Instruction ambiguity**: Agent definition instructions were unclear, contradictory, or incomplete
- **Timeout/capacity issues**: You hit maxTurns limits, context window pressure, or other capacity constraints

**If no issues are encountered, do not create a log file.** No file = clean execution.

---

## File Naming

```
errors-{YYYYMMDD-HHmm}-{agent-name}.md
```

Written to the `logs/` subdirectory of the session output directory provided in `SESSION PATH:`.

Example: `errors-20260306-1430-controller.md`

---

## Log Format

```markdown
# Agent Error Log: {Role Title}

**Agent:** {name}  |  **Session:** {session-path}  |  **Date:** {date}

---

## Issue 1: {Brief title}

**What happened:** {Description of what went wrong or what was unexpected}

**Expected:** {What should have happened according to instructions or normal behavior}

**Workaround:** {What you did instead to complete your task, or "None -- issue unresolved"}

**Impact:** {How this affected your output quality, completeness, or confidence}

---

## Issue 2: {Brief title}

...
```

Repeat the issue block for each problem encountered. Keep descriptions concise and factual.

---

## How to Write the Log File

**C-suite agents, CEO, and CCO production team leads** (Graphic Designer, Writer, Publisher): Use the **Write** tool to create the log file.

**Analytical team leads**: Use **Bash** with a heredoc:

```bash
cat <<'LOGEOF' > {session-path}/logs/errors-{YYYYMMDD-HHmm}-{agent-name}.md
# Agent Error Log: {Role Title}

**Agent:** {name}  |  **Session:** {session-path}  |  **Date:** {date}

---

## Issue 1: {Brief title}

**What happened:** ...

**Expected:** ...

**Workaround:** ...

**Impact:** ...
LOGEOF
```

Use `'LOGEOF'` (single-quoted) to prevent variable expansion in the heredoc.

---

## Timing

Log writing is your **last action** before SendMessage and TaskUpdate. Complete your primary analysis or production work first. Logging never blocks or delays your primary output.

---

## Failure Handling

If the log file write fails for any reason (path issue, permission error, tool failure), **abandon logging and complete your task normally**. Logging is best-effort. A failed log write must never prevent you from delivering your primary work product.

---

## Constraints

- Logging does **not** change your analysis, output template, synthesis, or communication
- Do **not** mention logging activity in your analytical output
- Do **not** reference the logging system in your SendMessage findings
- Do **not** spend more than one tool call on logging (write the file, move on)
