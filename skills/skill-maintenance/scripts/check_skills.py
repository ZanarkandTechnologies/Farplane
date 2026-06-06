#!/usr/bin/env python3
"""Run the standard Farplane skill-system checks."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "bin/sync_skill_registry.py").exists() and (candidate / "skills").exists():
            return candidate
    raise RuntimeError("could not find Farplane repo root")


REPO_ROOT = find_repo_root(Path(__file__).resolve())


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def registry_summary() -> dict[str, object]:
    rows = [
        json.loads(line)
        for line in (REPO_ROOT / "docs/skills/registry.jsonl").read_text().splitlines()
        if line.strip()
    ]
    return {
        "rows": len(rows),
        "tiers": dict(sorted(Counter(row["tier"] for row in rows).items())),
        "sources": dict(sorted(Counter(row["source"] for row in rows).items())),
        "checklists": dict(
            sorted(
                Counter("has" if row.get("has_checklist") else "missing" for row in rows).items()
            )
        ),
        "todos_files": dict(
            sorted(Counter("has" if row.get("has_todos") else "missing" for row in rows).items())
        ),
        "skill_template_versions": dict(
            sorted(Counter(str(row.get("skill_template_version") or "missing") for row in rows).items())
        ),
        "missing_skill_template_version": [
            {
                "name": row["name"],
                "tier": row["tier"],
                "source": row["source"],
            }
            for row in rows
            if not row.get("skill_template_version")
        ],
        "missing_checklists": [
            {
                "name": row["name"],
                "tier": row["tier"],
                "source": row["source"],
                "upstream_url": row.get("upstream_url"),
            }
            for row in rows
            if not row.get("has_checklist")
        ],
    }


def validate_template_version(current_version: str, require: bool) -> int:
    rows = [
        json.loads(line)
        for line in (REPO_ROOT / "docs/skills/registry.jsonl").read_text().splitlines()
        if line.strip()
    ]
    missing = [
        row
        for row in rows
        if not row.get("skill_template_version")
    ]
    not_current = [
        row
        for row in rows
        if row.get("skill_template_version") and row.get("skill_template_version") != current_version
    ]

    report = {
        "current_skill_template_version": current_version,
        "missing": [row["name"] for row in missing],
        "not_current": [
            {
                "name": row["name"],
                "skill_template_version": row.get("skill_template_version"),
            }
            for row in not_current
        ],
    }
    print("skill template version report:")
    print(json.dumps(report, indent=2, sort_keys=True))

    if require and (missing or not_current):
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="regenerate docs/skills/registry.jsonl before checking it",
    )
    parser.add_argument(
        "--strict-tier3",
        action="store_true",
        help="disallow peer Tier 3 todo links; default allows intentional Tier 3 handoffs",
    )
    parser.add_argument(
        "--template-version",
        help="report skills missing or differing from this current skill template version",
    )
    parser.add_argument(
        "--require-template-version",
        action="store_true",
        help="fail when --template-version finds missing or non-current skill template versions",
    )
    args = parser.parse_args()
    if args.require_template_version and not args.template_version:
        parser.error("--require-template-version requires --template-version")

    try:
        checklist_command = ["python3", "skills/skill-maintenance/scripts/sync_skill_checklists.py"]
        if args.write:
            checklist_command.append("--write")
        run(checklist_command)

        if args.write:
            run(["python3", "bin/sync_skill_registry.py", "--write"])
        run(["python3", "bin/sync_skill_registry.py", "--check"])

        tier_command = ["python3", "bin/check_skill_todo_tiers.py"]
        if not args.strict_tier3:
            tier_command.append("--allow-peer-tier3")
        run(tier_command)
        run(["python3", "bin/check_skill_capabilities.py", "validate"])

        run(
            [
                "python3",
                "-m",
                "py_compile",
                "bin/sync_skill_registry.py",
                "bin/check_skill_todo_tiers.py",
                "bin/check_skill_capabilities.py",
                "skills/skill-maintenance/scripts/check_skills.py",
                "skills/skill-maintenance/scripts/sync_skill_checklists.py",
            ]
        )
    except subprocess.CalledProcessError as exc:
        return exc.returncode

    print("skill system summary:")
    print(json.dumps(registry_summary(), indent=2, sort_keys=True))
    if args.template_version:
        return validate_template_version(args.template_version, args.require_template_version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
