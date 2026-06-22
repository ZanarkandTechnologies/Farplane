#!/usr/bin/env python3
"""Reject skill eval queries that leak the target skill's answer policy."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SKILL_EVAL_TASK_FILE = "eval_task.json"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def normalized_skill_names(skill_name: str) -> set[str]:
    return {skill_name.lower(), skill_name.lower().replace("-", " ")}


def query_spoilers(skill_name: str, query: str) -> list[str]:
    lowered = query.lower()
    spoilers: list[str] = []
    for name in normalized_skill_names(skill_name):
        escaped = re.escape(name)
        patterns = {
            f"using-the-skill-contract:{name}": rf"\busing\s+the\s+{escaped}\s+contract\b",
            f"use-the-skill-contract:{name}": rf"\buse\s+the\s+{escaped}\s+contract\b",
            f"using-the-skill:{name}": rf"\busing\s+the\s+{escaped}\s+skill\b",
            f"use-the-skill:{name}": rf"\buse\s+the\s+{escaped}\s+skill\b",
            f"read-skill-md:{name}": rf"\bread\s+`?skills/{re.escape(skill_name)}/skill\.md`?",
        }
        for label, pattern in patterns.items():
            if re.search(pattern, lowered):
                spoilers.append(label)
    return spoilers


def check_file(path: Path, root: Path) -> list[str]:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        relative = path
    parts = relative.parts
    if len(parts) != 3 or parts[0] != "skills" or parts[2] != SKILL_EVAL_TASK_FILE:
        return []
    skill_name = parts[1]
    raw = read_json(path)
    if not isinstance(raw, list):
        return [f"{relative}: task file must contain a JSON list"]
    errors: list[str] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        query = str(item.get("query", ""))
        spoilers = query_spoilers(skill_name, query)
        if spoilers:
            task_id = item.get("id", f"index-{index}")
            errors.append(
                f"{relative}: {task_id}: query leaks skill invocation policy ({', '.join(spoilers)}); "
                "keep the user query natural and rely on owner SKILL.md context"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    for path in sorted((root / "skills").glob(f"*/{SKILL_EVAL_TASK_FILE}")):
        errors.extend(check_file(path, root))
    if errors:
        for error in errors:
            print(error)
        return 1
    print("skill eval query lint OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
