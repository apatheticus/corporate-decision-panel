---
name: cdp:production
description: Re-run the production pipeline for an existing CDP session
argument-hint: "[session-path?]"
---

Read the full skill specification at `.claude/skills/corporate-decision-panel/SKILL.md` and follow all instructions there.

The user has invoked the **Production Re-run** path:

```
/cdp:production [session-path?]
```

User arguments: $ARGUMENTS

Execute the Production Re-run protocol exactly as described in the Orchestration Protocol section. All configuration, templates, and agent definitions are relative to the `.claude/skills/corporate-decision-panel/` directory.
