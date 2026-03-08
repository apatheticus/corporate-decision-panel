---
description: Resume an interrupted CDP session from last checkpoint
user_invocable: true
---

Resume an interrupted CDP deliberation session.

**Session resolution:** $ARGUMENTS (or most recent session if empty).
Apply the same session resolution rules as `/cdp:production`: explicit
path, slug substring match, or most recent by date prefix.

**Detection and resume logic:** Follow the Session Resume Protocol defined
in `config/orchestration-protocol.md`. Scan for file-based state markers
in the session directory to determine the resume point.

**Limitations:**
- Cannot resume with zero `_RECOMMENDATION_*.md` files — re-run the original command
- Cannot change routing or decision mode after resume
