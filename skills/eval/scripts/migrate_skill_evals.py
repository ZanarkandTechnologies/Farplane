#!/usr/bin/env python3
"""Convert Farplane skill eval_task.json files to Agent Skills evals/evals.json."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any


LEGACY_NAME = "eval_task.json"
STANDARD_RELATIVE_PATH = Path("evals/evals.json")


class MigrationError(ValueError):
    """Raised when a legacy eval cannot be converted without guessing."""


def read_legacy_tasks(path: Path) -> list[dict[str, Any]]:
    try:
        raw = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise MigrationError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(raw, list) or not all(isinstance(row, dict) for row in raw):
        raise MigrationError(f"{path}: expected a JSON list of task objects")
    return raw


def require_non_empty_string(row: dict[str, Any], field: str, path: Path) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        raise MigrationError(f"{path}: task {row.get('id', '<unknown>')} {field} must be a non-empty string")
    return value.strip()


def convert_task(row: dict[str, Any], path: Path) -> dict[str, Any]:
    task_id = row.get("id")
    if not isinstance(task_id, (str, int)) or isinstance(task_id, bool):
        raise MigrationError(f"{path}: task id must be a string or integer")
    prompt = require_non_empty_string(row, "query", path)
    expectation_field = next(
        (field for field in ("reference_points", "expected_behavior", "expected") if row.get(field)),
        None,
    )
    assertions = row.get(expectation_field) if expectation_field else None
    if not isinstance(assertions, list) or not assertions or not all(
        isinstance(item, str) and item.strip() for item in assertions
    ):
        raise MigrationError(
            f"{path}: task {task_id} needs non-empty reference_points, expected_behavior, or expected strings"
        )
    assertions = [item.strip() for item in assertions]

    expected_output = str(row.get("expected_output", "")).strip()
    if not expected_output:
        expected_output = "; ".join(assertions)

    files = row.get("files", [])
    if not isinstance(files, list) or not all(isinstance(item, str) and item.strip() for item in files):
        raise MigrationError(f"{path}: task {task_id} files must be strings")

    farplane: dict[str, Any] = {}
    for field in ("title", "context", "tags", "notes"):
        if field in row:
            farplane[field] = row[field]

    converted: dict[str, Any] = {
        "id": task_id,
        "prompt": prompt,
        "expected_output": expected_output,
        "files": [item.strip() for item in files],
        "assertions": assertions,
    }
    if farplane:
        converted["metadata"] = {"farplane": farplane}
    return converted


def convert_file(path: Path) -> dict[str, Any]:
    return {
        "skill_name": path.parent.name,
        "evals": [convert_task(row, path) for row in read_legacy_tasks(path)],
    }


def discover_legacy_files(root: Path, skills: list[str]) -> list[Path]:
    skills_root = root / "skills"
    if skills:
        invalid = [name for name in skills if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)]
        if invalid:
            raise MigrationError("invalid skill names: " + ", ".join(invalid))
        paths = [skills_root / name / LEGACY_NAME for name in skills]
        missing = [path for path in paths if not path.is_file()]
        if missing:
            raise MigrationError("legacy eval files not found: " + ", ".join(str(path) for path in missing))
        return paths
    return sorted(skills_root.glob(f"*/{LEGACY_NAME}"))


def prepare_migration(path: Path, *, force: bool) -> tuple[Path, dict[str, Any]]:
    destination = path.parent / STANDARD_RELATIVE_PATH
    converted = convert_file(path)
    if destination.exists() and not force:
        raise MigrationError(f"{destination}: already exists; use --force to replace it")
    return destination, converted


def write_migration(destination: Path, converted: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=destination.parent, delete=False) as handle:
        handle.write(json.dumps(converted, indent=2) + "\n")
        temporary = Path(handle.name)
    temporary.replace(destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root containing skills/.")
    parser.add_argument("--skill", action="append", default=[], help="Convert only this skill; repeat as needed.")
    parser.add_argument("--write", action="store_true", help="Write evals/evals.json. The default is a dry run.")
    parser.add_argument("--force", action="store_true", help="Replace an existing evals/evals.json.")
    parser.add_argument(
        "--remove-legacy",
        action="store_true",
        help="Delete eval_task.json after every destination has been written successfully. Requires --write.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    try:
        if args.remove_legacy and not args.write:
            raise MigrationError("--remove-legacy requires --write")
        paths = discover_legacy_files(root, args.skill)
        if not paths:
            raise MigrationError(f"{root}: no skills/*/{LEGACY_NAME} files found")
        prepared = [prepare_migration(path, force=args.force) for path in paths]
        total = 0
        for destination, converted in prepared:
            count = len(converted["evals"])
            total += count
            if args.write:
                write_migration(destination, converted)
            action = "wrote" if args.write else "would write"
            print(f"{action} {destination.relative_to(root)} ({count} evals)")
        if args.remove_legacy:
            for path in paths:
                path.unlink()
            print(f"Removed {len(paths)} legacy {LEGACY_NAME} files")
        print(f"{'Converted' if args.write else 'Dry run:'} {len(paths)} skill files, {total} evals")
        return 0
    except MigrationError as exc:
        print(f"error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
