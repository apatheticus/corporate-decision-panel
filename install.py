#!/usr/bin/env python3
"""Install CDP agent definitions and slash commands into .claude/ directory.

Run after cloning the skill repo:
    python3 .claude/skills/corporate-decision-panel/install.py

Idempotent -- safe to re-run after git pull to pick up updates.
"""

import shutil
import sys
from pathlib import Path


def main():
    # Resolve paths relative to this script's location
    script_dir = Path(__file__).resolve().parent
    agents_src = script_dir / "agents"
    commands_src = script_dir / "commands"

    # The .claude/ directory is two levels up from the skill repo
    # e.g., .claude/skills/corporate-decision-panel/ -> .claude/
    claude_dir = script_dir.parent.parent

    # Project root is one level above .claude/
    project_root = claude_dir.parent

    # Detect global install (parent of .claude/ is user's home directory)
    # Resolve both sides to handle symlinks (e.g., /tmp -> /private/tmp on macOS)
    is_global = project_root == Path.home().resolve()

    # Validate source directories exist
    if not agents_src.is_dir():
        print(f"Error: agents directory not found at {agents_src}", file=sys.stderr)
        sys.exit(1)
    if not commands_src.is_dir():
        print(f"Error: commands directory not found at {commands_src}", file=sys.stderr)
        sys.exit(1)

    # Copy agent definitions to .claude/agents/
    agents_dest = claude_dir / "agents"
    agents_dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(agents_src, agents_dest, dirs_exist_ok=True)

    # Copy slash commands to .claude/commands/
    commands_dest = claude_dir / "commands"
    commands_dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(commands_src, commands_dest, dirs_exist_ok=True)

    # Count installed files
    agent_count = sum(1 for _ in agents_dest.rglob("*.md"))
    command_count = sum(1 for _ in (commands_dest / "cdp").rglob("*.md"))

    # Project-level only: update .gitignore and create .cdp-context/
    if not is_global:
        gitignore_path = project_root / ".gitignore"
        entries = [".cdp-output/", ".cdp-context/"]
        existing = ""
        if gitignore_path.exists():
            existing = gitignore_path.read_text()
        to_add = [e for e in entries if e not in existing]
        if to_add:
            with gitignore_path.open("a") as f:
                if existing and not existing.endswith("\n"):
                    f.write("\n")
                for entry in to_add:
                    f.write(f"{entry}\n")

        cdp_context = project_root / ".cdp-context"
        cdp_context.mkdir(exist_ok=True)

    print("CDP installed successfully.")
    print(f"  - {agent_count} agent definitions copied to .claude/agents/")
    print(f"  - {command_count} slash commands copied to .claude/commands/cdp/")
    if not is_global:
        print("  - .gitignore updated")
        print("  - .cdp-context/ directory created")
    print()
    print("Quick start:")
    print("  /cdp:consult cfo: Can we afford to hire this quarter?")
    print("  /cdp:panel finance tech: Should we build or buy?")
    print("  /cdp:deliberate: Should we pivot to a platform model?")
    print("  /cdp:evaluate: Should we acquire CompetitorX?")


if __name__ == "__main__":
    main()
