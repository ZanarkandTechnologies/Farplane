#!/usr/bin/env python3
"""Scaffold skill-local self-improvement memory."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", help="Target skill directory")
    parser.add_argument("--goal", default="Improve this skill with measured evals.")
    parser.add_argument("--force", action="store_true", help="Overwrite program.md if it exists")
    parser.add_argument("--prompt-profile", action="store_true", help="Add prompt candidate/history eval profile")
    return parser.parse_args()


def now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def render_program(skill_name: str, goal: str) -> str:
    return f"""# Self-Improve Program: {skill_name}

## Objective
{goal}

## Current Contract
- Trigger:
- First-load workflow:
- Outcome:
- Validation:

## Eval Metric
- Primary: `skill_eval_pass_rate`
- Direction: higher
- Minimum meaningful delta:
- Simplicity guard:

## Rubric
- Correct trigger selection
- Reliable first-load workflow
- Useful, bounded outcome

## Durable Evals
- `evals/test_cases.jsonl`
- `evals/assertions.md`

## Experiment Log
| Date | Run | Hypothesis | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- |
| {now_date()} | setup | Create skill-local memory | Baseline memory surface created | yes | Future runs should record durable lessons here. |

## Accepted Learnings
- Preserve only lessons that future runs should know before editing.

## Rejected Ideas
- None yet.

## Next Hypotheses
- Build at least 3 smoke eval cases before mutating the skill.
- Build 20-100 diverse cases before trusting overnight optimization.
"""


def render_assertions_py() -> str:
    return '''#!/usr/bin/env python3
"""Deterministic binary assertions for prompt-like skill evals."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class AssertionResult:
    name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def evaluate_case(case: dict[str, Any], output: dict[str, Any]) -> list[AssertionResult]:
    text = str(output.get("output", ""))
    files = set(_as_list(output.get("files")))
    results: list[AssertionResult] = []

    for expected in _as_list(case.get("must_contain")):
        results.append(
            AssertionResult(
                name=f"must_contain:{expected}",
                passed=expected in text,
                message="found required text" if expected in text else "missing required text",
            )
        )

    for forbidden in _as_list(case.get("must_not_contain")):
        results.append(
            AssertionResult(
                name=f"must_not_contain:{forbidden}",
                passed=forbidden not in text,
                message="forbidden text absent" if forbidden not in text else "forbidden text present",
            )
        )

    for path in _as_list(case.get("expected_files")):
        results.append(
            AssertionResult(
                name=f"expected_file:{path}",
                passed=path in files,
                message="expected file reported" if path in files else "expected file missing",
            )
        )

    if not results:
        results.append(
            AssertionResult(
                name="has_output",
                passed=bool(text.strip()),
                message="output exists" if text.strip() else "output is empty",
            )
        )

    return results
'''


def render_runner_py() -> str:
    return '''#!/usr/bin/env python3
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
    path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")


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
    latest_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
    with (results_dir / "scores.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({key: summary[key] for key in summary if key != "case_results"}, sort_keys=True) + "\\n")
    write_failure_analysis(results_dir / "failure_analysis.md", case_results)

    print(f"skill_eval_pass_rate={pass_rate:.6f}")
    print(f"latest_run={latest_path}")
    return 0 if pass_rate >= 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def write_if_missing(path: Path, content: str, force: bool = False, executable: bool = False) -> None:
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | 0o755)


def scaffold_prompt_profile(memory_dir: Path, force: bool) -> None:
    prompts_dir = memory_dir / "prompts"
    candidates_dir = prompts_dir / "candidates"
    history_dir = prompts_dir / "history"
    evals_dir = memory_dir / "evals"
    results_dir = memory_dir / "results"

    for directory in [prompts_dir, candidates_dir, history_dir, evals_dir, results_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    write_if_missing(prompts_dir / "current.txt", "Paste or summarize the active prompt-like instruction here.\n", force)
    write_if_missing(candidates_dir / ".gitkeep", "", force)
    write_if_missing(history_dir / ".gitkeep", "", force)
    write_if_missing(
        evals_dir / "test_cases.jsonl",
        '{"id":"tc_001","input":"Example operator request","must_contain":["Example"],"metadata":{"category":"smoke"}}\n',
        force,
    )
    write_if_missing(evals_dir / "assertions.py", render_assertions_py(), force, executable=True)
    write_if_missing(evals_dir / "runner.py", render_runner_py(), force, executable=True)
    write_if_missing(results_dir / "scores.jsonl", "", force)
    write_if_missing(results_dir / "latest_run.json", "{}\n", force)
    write_if_missing(results_dir / "failure_analysis.md", "# Failure Analysis\n\n- No runs yet.\n", force)
    write_if_missing(results_dir / "candidate_outputs.jsonl", "", force)


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        raise SystemExit(f"Skill directory does not exist: {skill_dir}")
    if not (skill_dir / "SKILL.md").exists():
        raise SystemExit(f"Expected SKILL.md in target skill directory: {skill_dir}")

    memory_dir = skill_dir / "self-improve"
    evals_dir = memory_dir / "evals"
    runs_dir = memory_dir / "runs"
    evals_dir.mkdir(parents=True, exist_ok=True)
    runs_dir.mkdir(parents=True, exist_ok=True)

    program_path = memory_dir / "program.md"
    if program_path.exists() and not args.force:
        print(f"Keeping existing {program_path}")
    else:
        program_path.write_text(render_program(skill_dir.name, args.goal), encoding="utf-8")

    cases_path = evals_dir / "test_cases.jsonl"
    if not args.prompt_profile and not cases_path.exists():
        cases_path.write_text("", encoding="utf-8")

    assertions_path = evals_dir / "assertions.md"
    if not assertions_path.exists():
        assertions_path.write_text(
            "# Skill Eval Assertions\n\nAdd binary assertions before mutating the skill.\n",
            encoding="utf-8",
        )

    if args.prompt_profile:
        scaffold_prompt_profile(memory_dir, args.force)

    print(f"Skill self-improvement memory ready in {memory_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
