#!/usr/bin/env python3
"""Run the standard Farplane skill-system checks."""

from __future__ import annotations

import argparse
import json
import re
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
REQUIRED_TEMPLATE_HEADINGS = ("Context", "Todo List", "Templates", "Gotchas", "Reference Map", "Output")
HEADING_RE = re.compile(r"^## (?P<heading>.+?)\s*$")
TOP_LEVEL_NUMBERED_TODO_RE = re.compile(r"^\d+\. \[ \] ")
TOP_LEVEL_PLAIN_TODO_RE = re.compile(r"^- \[ \] ")
UNORDERED_PROSE_TODO_RE = re.compile(r"^\s+- (?!\[ \])")


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


def iter_markdown_headings(text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((line_number, match.group("heading")))
    return headings


def markdown_section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    in_fence = False
    start: int | None = None
    for index, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        if start is None:
            if match.group("heading") == heading:
                start = index + 1
            continue
        return "\n".join(lines[start:index])
    if start is None:
        return None
    return "\n".join(lines[start:])


def marker_counts(text: str) -> tuple[int, int, int]:
    real_markers = 0
    fenced_markers = 0
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->" not in line:
            continue
        if in_fence:
            fenced_markers += 1
        else:
            real_markers += 1
    return real_markers, fenced_markers, text.count("<!-- END FARPLANE_IMPORTANT_CHECKLIST -->")


def template_structure_errors(current_version: str) -> list[str]:
    rows = [
        json.loads(line)
        for line in (REPO_ROOT / "docs/skills/registry.jsonl").read_text().splitlines()
        if line.strip()
    ]
    errors: list[str] = []
    for row in rows:
        if row.get("skill_template_version") != current_version:
            continue
        path = Path(str(row["path"]))
        skill_path = REPO_ROOT / path
        if not skill_path.exists():
            errors.append(f"{row['name']}: missing skill file at {path}")
            continue

        text = skill_path.read_text(encoding="utf-8")
        real_begin_count, fenced_begin_count, end_count = marker_counts(text)
        if real_begin_count != 1:
            errors.append(f"{row['name']}: expected exactly one real todo-list marker section")
        if fenced_begin_count:
            errors.append(f"{row['name']}: do not put todo-list marker comments inside fenced examples")
        if end_count != real_begin_count + fenced_begin_count:
            errors.append(f"{row['name']}: mismatched todo-list marker comments")

        headings = iter_markdown_headings(text)
        heading_names = [heading for _, heading in headings]
        heading_lines = {heading: line_number for line_number, heading in headings}

        for required_heading in REQUIRED_TEMPLATE_HEADINGS:
            if required_heading not in heading_names:
                errors.append(f"{row['name']}: missing ## {required_heading}")

        if "Job" in heading_names:
            errors.append(f"{row['name']}: remove generic ## Job; fold work into Context/Todo List")

        if "Context" in heading_lines and "Todo List" in heading_lines:
            if heading_lines["Context"] > heading_lines["Todo List"]:
                errors.append(f"{row['name']}: ## Context must appear before ## Todo List")

        todo_body = markdown_section(text, "Todo List")
        if todo_body is None:
            continue
        if not any(TOP_LEVEL_NUMBERED_TODO_RE.match(line) for line in todo_body.splitlines()):
            errors.append(f"{row['name']}: ## Todo List needs numbered task items like `1. [ ] ...`")
        for line_number, line in enumerate(todo_body.splitlines(), start=1):
            if TOP_LEVEL_PLAIN_TODO_RE.match(line):
                errors.append(
                    f"{row['name']}: top-level plain todo in ## Todo List line {line_number}; "
                    "use numbered todos for main work and indent plain todos under a numbered item"
                )
                break
            if UNORDERED_PROSE_TODO_RE.match(line):
                errors.append(
                    f"{row['name']}: unordered prose bullet in ## Todo List line {line_number}; "
                    "use numbered branch todos or embedded `- [ ]` checks"
                )
                break

    return errors


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

    structure_errors = template_structure_errors(current_version)
    if structure_errors:
        print("skill template structure errors:")
        for error in structure_errors:
            print(f"- {error}")
        return 1

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
