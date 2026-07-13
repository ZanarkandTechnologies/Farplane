#!/usr/bin/env python3
"""Validate canonical QA receipts and artifact honesty in a harness eval run."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_qa_result import validate


JSON_BLOCK = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
QA_RESULT = re.compile(
    r"QA_RESULT:\s+verdict=(?P<verdict>pass|revise|fail|blocked|not_provable)"
    r"\s+evidence=(?P<evidence>[^\s]+)"
)
PROJECT_ROOT = Path(__file__).resolve().parents[3]


def extract_receipt(answer: str) -> tuple[dict[str, Any] | None, list[str]]:
    receipts: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, raw in enumerate(JSON_BLOCK.findall(answer), start=1):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"json block {index}: {exc}")
            continue
        if isinstance(value, dict) and value.get("phase") == "qa":
            receipts.append(value)
    if len(receipts) != 1:
        errors.append(f"answer: expected exactly one canonical QA JSON block, found {len(receipts)}")
        return None, errors
    return receipts[0], errors


def validate_answer(answer: str, project_root: Path) -> list[str]:
    receipt, errors = extract_receipt(answer)
    if receipt is None:
        return errors
    errors.extend(validate(receipt))
    for field in ("artifacts", "judgment_receipts"):
        values = receipt.get(field, [])
        if not isinstance(values, list):
            continue
        for value in values:
            if not isinstance(value, str):
                continue
            path = project_root / value
            if not path.is_file():
                errors.append(f"{field}: fixture artifact does not exist: {value}")
    result_match = QA_RESULT.search(answer)
    if result_match is None:
        errors.append("answer: missing canonical QA_RESULT line")
    else:
        line_verdict = result_match.group("verdict")
        if line_verdict != receipt.get("verdict"):
            errors.append(
                f"QA_RESULT: verdict {line_verdict} does not match receipt verdict {receipt.get('verdict')}"
            )
        evidence = result_match.group("evidence").strip("`.,")
        if not evidence.endswith("result.json"):
            errors.append("QA_RESULT: evidence must name the result.json receipt, not best evidence")
    return errors


def validate_run(run_dir: Path, project_root: Path = PROJECT_ROOT) -> list[str]:
    errors: list[str] = []
    task_root = run_dir / "tasks"
    for answer_path in sorted(task_root.glob("*/agent_answer.txt")):
        task_id = answer_path.parent.name
        for error in validate_answer(answer_path.read_text(encoding="utf-8"), project_root):
            errors.append(f"{task_id}: {error}")
    if not list(task_root.glob("*/agent_answer.txt")):
        errors.append(f"run: no agent answers found under {task_root}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args()
    errors = validate_run(args.run_dir.resolve(), args.project_root.resolve())
    if errors:
        print("\n".join(errors))
        return 1
    print(f"QA eval receipts OK: {args.run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
