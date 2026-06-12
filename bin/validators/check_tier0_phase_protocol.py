#!/usr/bin/env python3
"""Validate the Tier 0 phase protocol migration guardrails."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_LINK_RE = re.compile(r"\[[^\]]+\]\(\.\./(?P<skill>plan|execute)/SKILL\.md\)")
OLD_REVIEW_PATH_RE = re.compile(
    re.escape("skills/review" + "/references") + r"|(?<!coderabbit-)review/references/"
)


def registry_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    registry = ROOT / "docs/skills/registry.jsonl"
    if not registry.exists():
        return rows
    for line in registry.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def checklist_body(text: str) -> str:
    match = re.search(
        r"<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->(.*?)<!-- END FARPLANE_IMPORTANT_CHECKLIST -->",
        text,
        re.DOTALL,
    )
    return match.group(1) if match else ""


def live_text_files() -> list[Path]:
    roots = [
        ROOT / "AGENTS.md",
        ROOT / "templates",
        ROOT / "docs",
        ROOT / "skills",
        ROOT / "agents",
        ROOT / "tickets/README.md",
        ROOT / "tickets/templates",
        ROOT / "bin",
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(
                path
                for path in root.rglob("*")
                if path.is_file() and path.suffix in {".md", ".py", ".toml", ".json", ".jsonl"}
            )
    return files


def is_historical_skill_run(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        len(rel.parts) >= 5
        and rel.parts[0] == "skills"
        and rel.parts[2] == "self-improve"
        and rel.parts[3] == "runs"
    )


def main() -> int:
    errors: list[str] = []

    for skill_path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill_path.read_text()
        if re.search(r"(?m)^tier:\s*0\s*$", text):
            errors.append(f"{skill_path.relative_to(ROOT)}: tier: 0 is forbidden; Tier 0 is a phase protocol")

    for row in registry_rows():
        path = ROOT / str(row.get("path"))
        if not path.exists():
            continue
        body = checklist_body(path.read_text())
        for line_number, line in enumerate(body.splitlines(), start=1):
            if SKILL_LINK_RE.search(line):
                errors.append(
                    f"{path.relative_to(ROOT)} todo line {line_number}: "
                    "skill todo lists must not link to plan/execute compatibility wrappers"
                )

    for path in live_text_files():
        if path.name == "check_tier0_phase_protocol.py":
            continue
        if is_historical_skill_run(path):
            continue
        text = path.read_text(errors="ignore")
        if OLD_REVIEW_PATH_RE.search(text):
            rel = path.relative_to(ROOT)
            if rel.parts[:2] == ("tickets", "archive") or rel.parts[0] in {"docs"} and "HISTORY.md" in rel.parts:
                continue
            errors.append(f"{rel}: old review rubric path found; use docs/review/rubrics/*")

    if errors:
        print("Tier 0 phase protocol check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Tier 0 phase protocol check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
