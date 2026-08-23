"""Explicit writer for checked-in skill registry and graph projections."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_sync_skills(args: argparse.Namespace) -> int:
    """Refresh skill projections, then prove their complete read-only contract."""

    root = Path(args.root).expanduser().resolve()
    graph_script = root / "skills" / "skill-maintenance" / "scripts" / "generate_graph_projection.py"
    commands = (
        (
            "skill_registry",
            (
                sys.executable,
                str(root / "bin" / "validators" / "sync_skill_registry.py"),
                "--write",
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
            ),
        ),
        (
            "skill_lint",
            (sys.executable, str(root / "bin" / "farplane.py"), "lint", "skills"),
        ),
    )
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
    payload = {
        "ok": ok,
        "scope": "skills",
        "changed": True,
        "summary": (
            f"farplane skills sync refreshed: checks={len(results)}"
            if ok
            else "farplane skills sync failed"
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
