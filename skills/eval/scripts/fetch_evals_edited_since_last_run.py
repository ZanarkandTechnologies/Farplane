#!/usr/bin/env python3
"""Find skill eval files whose content changed since the last eval drain."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STATE_PATH = ".farplane/state/eval-drain/processed.jsonl"
SKILL_EVAL_GLOB = "skills/*/evals/evals.json"


class FetchError(ValueError):
    """Raised when eval-drain discovery input is invalid."""


@dataclass(frozen=True)
class EvalFile:
    path: Path
    relative_path: str
    content_hash: str
    task_count: int


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FetchError(f"{path}: invalid JSON: {exc}") from exc


def normalize_task_count(data: Any, path: Path) -> int:
    if not isinstance(data, dict) or not isinstance(data.get("evals"), list):
        raise FetchError(f"{path}: expected an Agent Skills evals object")
    return len(data["evals"])


def discover_eval_files(project_root: Path) -> list[EvalFile]:
    files: list[EvalFile] = []
    for path in sorted(project_root.glob(SKILL_EVAL_GLOB)):
        text = path.read_text(encoding="utf-8")
        task_count = normalize_task_count(read_json(path), path)
        files.append(
            EvalFile(
                path=path,
                relative_path=path.relative_to(project_root).as_posix(),
                content_hash=sha256_text(text),
                task_count=task_count,
            )
        )
    return files


def load_processed_hashes(state_path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not state_path.exists():
        return hashes

    for line_number, raw_line in enumerate(state_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise FetchError(f"{state_path}:{line_number}: invalid JSONL row: {exc}") from exc
        eval_ref = row.get("eval_ref")
        content_hash = row.get("content_hash")
        if isinstance(eval_ref, str) and isinstance(content_hash, str):
            hashes[eval_ref] = content_hash
    return hashes


def changed_eval_files(project_root: Path, state_path: Path, include_unchanged: bool = False) -> dict[str, Any]:
    eval_files = discover_eval_files(project_root)
    processed_hashes = load_processed_hashes(state_path)
    rows: list[dict[str, Any]] = []

    for eval_file in eval_files:
        previous_hash = processed_hashes.get(eval_file.relative_path)
        changed = previous_hash != eval_file.content_hash
        if changed or include_unchanged:
            rows.append(
                {
                    "path": eval_file.relative_path,
                    "previous_hash": previous_hash,
                    "current_hash": eval_file.content_hash,
                    "task_count": eval_file.task_count,
                    "reason": "new" if previous_hash is None else "changed" if changed else "unchanged",
                }
            )

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "project_root": project_root.as_posix(),
        "processed_state": state_path.as_posix(),
        "changed_count": sum(1 for row in rows if row["reason"] in {"new", "changed"}),
        "eval_files": rows,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--state",
        default=DEFAULT_STATE_PATH,
        help="Eval-drain processed JSONL path, relative to project root unless absolute.",
    )
    parser.add_argument("--include-unchanged", action="store_true", help="Include unchanged files in output.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    project_root = Path(args.project_root).resolve()
    state_path = Path(args.state)
    if not state_path.is_absolute():
        state_path = project_root / state_path

    try:
        result = changed_eval_files(project_root, state_path, include_unchanged=args.include_unchanged)
    except FetchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
