#!/usr/bin/env python3
"""Run deterministic eval assertions for a prompt-like skill candidate."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", default="test_cases.jsonl")
    parser.add_argument("--outputs", default="../results/candidate_outputs.jsonl")
    parser.add_argument("--candidate", default="../prompts/current.txt")
    parser.add_argument("--results-dir", default="../results")
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def load_assertions_module() -> Any:
    path = Path(__file__).with_name("assertions.py")
    spec = importlib.util.spec_from_file_location("skill_eval_assertions", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load assertions from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def result_to_dict(result: Any) -> dict[str, Any]:
    if hasattr(result, "to_dict"):
        return result.to_dict()
    if isinstance(result, dict):
        return result
    return {"name": str(result), "passed": bool(result), "message": ""}


def write_failure_analysis(path: Path, case_results: list[dict[str, Any]]) -> None:
    failures = [
        item
        for case in case_results
        for item in case["assertions"]
        if not item.get("passed")
    ]
    counts = Counter(item.get("name", "unknown") for item in failures)
    lines = ["# Failure Analysis", ""]
    if not failures:
        lines.append("- No failures.")
    else:
        for name, count in counts.most_common():
            lines.append(f"- {name}: {count}")
    lines.extend(["", "## Next Hypothesis", "", "- TBD"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    cases_path = (base_dir / args.cases).resolve()
    outputs_path = (base_dir / args.outputs).resolve()
    candidate_path = (base_dir / args.candidate).resolve()
    results_dir = (base_dir / args.results_dir).resolve()
    results_dir.mkdir(parents=True, exist_ok=True)

    cases = load_jsonl(cases_path)
    outputs = {str(row.get("id")): row for row in load_jsonl(outputs_path)}
    assertions = load_assertions_module()

    case_results: list[dict[str, Any]] = []
    passed_assertions = 0
    total_assertions = 0

    for case in cases:
        case_id = str(case.get("id"))
        output = outputs.get(case_id, {"id": case_id, "output": "", "files": []})
        assertion_dicts = [result_to_dict(item) for item in assertions.evaluate_case(case, output)]
        total_assertions += len(assertion_dicts)
        passed_assertions += sum(1 for item in assertion_dicts if item.get("passed"))
        case_results.append({"id": case_id, "assertions": assertion_dicts})

    pass_rate = passed_assertions / total_assertions if total_assertions else 0.0
    summary = {
        "candidate": str(candidate_path),
        "cases": len(cases),
        "passed_assertions": passed_assertions,
        "total_assertions": total_assertions,
        "pass_rate": pass_rate,
        "timestamp": now_iso(),
        "case_results": case_results,
    }

    latest_path = results_dir / "latest_run.json"
    latest_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (results_dir / "scores.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({key: summary[key] for key in summary if key != "case_results"}, sort_keys=True) + "\n")
    write_failure_analysis(results_dir / "failure_analysis.md", case_results)

    print(f"skill_eval_pass_rate={pass_rate:.6f}")
    print(f"latest_run={latest_path}")
    return 0 if pass_rate >= 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
