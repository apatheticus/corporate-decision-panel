---
name: cdp:cleanup
description: Clean up old CDP session directories
argument-hint: "[--older-than days?]"
---

The user has invoked the **Session Cleanup** command:

```
/cdp:cleanup [--older-than days?]
```

User arguments: $ARGUMENTS

## Instructions

Clean up old CDP session directories in `.cdp-output/`. Follow these steps exactly.

### 1. Parse Arguments

If the user provided `--older-than N`, use N as the age threshold in days. Otherwise default to **30 days**.

### 2. Discover Sessions

Scan the `.cdp-output/` directory for session subdirectories. Each session directory follows the naming convention `YYYY-MM-DD_<issue-slug>/`.

- If `.cdp-output/` does not exist or is empty, inform the user: "No CDP sessions found. The .cdp-output/ directory does not exist or is empty." and stop.

### 3. Filter by Age

Parse the `YYYY-MM-DD` date prefix from each directory name to determine session age. Compare against today's date. Identify sessions **older than** the threshold (default 30 days) as candidates for deletion.

- If no sessions are older than the threshold, inform the user: "No sessions older than N days found. Nothing to clean up." and stop.

### 4. Calculate Size

For each candidate session, calculate the directory size using `du -sh`.

### 5. Display Confirmation Table

Present a table of candidate sessions to the user:

```
Sessions older than N days:

| Date       | Session Slug                        | Size  |
|------------|-------------------------------------|-------|
| 2026-01-15 | should-we-acquire-competitor-x      | 2.1M  |
| 2026-01-20 | can-we-afford-to-hire-this-quarter  | 1.8M  |

Total: 2 sessions, 3.9M
```

### 6. Request Confirmation

Ask the user for explicit confirmation before proceeding:

> "Delete these N sessions? This will permanently remove the entire session directories. (yes/no)"

- If the user declines or says anything other than "yes", respond: "Cleanup cancelled. No sessions were deleted." and stop.

### 7. Delete Sessions

On confirmation, remove each candidate session directory entirely:

```bash
rm -rf .cdp-output/YYYY-MM-DD_<issue-slug>
```

This is a clean deletion. Do **not** archive or preserve RECORD.md or any other files before deletion. Users who want to preserve records should export or version-control separately.

### 8. Report Results

After deletion, report:

> "Deleted N sessions, reclaimed approximately X of disk space."
