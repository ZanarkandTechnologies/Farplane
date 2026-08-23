"""Explicit write boundary for checked-in skill projections."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_validate_skills(args: argparse.Namespace) -> int:
    """Refresh or check skill projections, then prove the complete read-only contract."""

    root = Path(args.root).expanduser().resolve()
    check_only = args.check
    graph_script = root / "skills" / "skill-maintenance" / "scripts" / "generate_graph_projection.py"
    lint_command = (
        "skill_lint",
        (sys.executable, str(root / "bin" / "farplane.py"), "lint", "skills"),
    )
    projection_commands = (
        (
            "skill_registry",
            (
                sys.executable,
                str(root / "bin" / "validators" / "sync_skill_registry.py"),
                "--check" if check_only else "--write",
            ),
        ),
        (
            "skill_graph",
            (
                sys.executable,
                str(graph_script),
                "--projection",
                "skill-registry",
                "--repo-root",
                str(root),
                *(("--check",) if check_only else ()),
            ),
        ),
        (
            "harness_graph",
            (
                sys.executable,
                str(graph_script),
                "--projection",
                "harness-reference",
                "--repo-root",
                str(root),
                *(("--check",) if check_only else ()),
            ),
        ),
    )
    commands = (lint_command, *projection_commands) if check_only else (*projection_commands, lint_command)
    results: list[dict[str, Any]] = []
    for check_id, command in commands:
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
        except OSError as exc:
            results.append({"id": check_id, "ok": False, "output": str(exc)})
            break
        output = "\n".join(
            part.strip() for part in (completed.stdout, completed.stderr) if part.strip()
        )
        results.append({"id": check_id, "ok": completed.returncode == 0, "output": output})
        if completed.returncode != 0:
            break

    ok = all(result["ok"] for result in results) and len(results) == len(commands)
    action = "checked" if check_only else "refreshed"
    payload = {
        "ok": ok,
        "scope": "skills",
        "changed": not check_only,
        "summary": (
            f"farplane validate skills {action}: checks={len(results)}"
            if ok
            else "farplane validate skills failed"
        ),
        "checks": results,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["summary"])
        for result in results:
            print(f"[{'pass' if result['ok'] else 'fail'}] {result['id']}")
            if result["output"]:
                print(result["output"])
    return 0 if ok else 1
