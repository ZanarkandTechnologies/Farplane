"""`farplane desk`: launch Codex or Claude as one Capability Map desk."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from farplane_cli_base import CORE_ROOT, DEFAULT_CODEX_HOME, CliError
from skill_departments import desk_identity, load_skill_specialists

DEFAULT_CLAUDE_HOME = Path.home() / ".claude"


def desk_launch_plan(desk_id: str, runtime: str, extra: list[str], home: Path) -> list[str]:
    """Check the desk is installed for `runtime`, then return the command that launches it."""
    desks = load_skill_specialists(CORE_ROOT)
    desk = desks.get(desk_id)
    if desk is None:
        raise CliError(f"unknown desk {desk_id!r}; `farplane desk --list` shows the desks", 2)
    profile = home / f"{desk_id}.config.toml" if runtime == "codex" else home / "farplane" / "desks" / f"{desk_id}.settings.json"
    missing = [] if profile.is_file() else [str(profile)]
    missing += [str(home / "skills" / skill / "SKILL.md") for skill in desk["skills"] if not (home / "skills" / skill / "SKILL.md").is_file()]
    if missing:
        install = "farplane install" if runtime == "codex" else "bash install.sh --runtime claude"
        raise CliError(f"desk {desk_id!r} is not installed for {runtime}; missing {', '.join(missing)}. Run {install}.", 2)
    if runtime == "codex":
        return ["codex", "-p", desk_id, *extra]
    return ["claude", "--settings", str(profile), "--append-system-prompt", desk_identity(desk_id, desk), *extra]


def run_desk_cli(args: argparse.Namespace) -> int:
    if args.list or not args.desk:
        for desk_id, desk in load_skill_specialists(CORE_ROOT).items():
            print(f"{desk_id:22} {desk['label']}: {', '.join(desk['skills'])}")
        return 0
    home = Path(args.home).expanduser() if args.home else (DEFAULT_CODEX_HOME if args.runtime == "codex" else DEFAULT_CLAUDE_HOME)
    command = desk_launch_plan(args.desk, args.runtime, args.extra, home)
    if args.dry_run:
        print(json.dumps(command))
        return 0
    os.execvp(command[0], command)
    return 0
