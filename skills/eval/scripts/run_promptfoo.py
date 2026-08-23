#!/usr/bin/env python3
"""Project Agent Skills evals into ephemeral Promptfoo comparisons.

Farplane owns source validation, isolated workspaces, and a normalized receipt.
Promptfoo owns agent execution, skill-use detection, assertions, and raw export.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bin.core.eval_contract import EvalContractError, lint_agent_skills_eval_suite


SCHEMA_VERSION = 2
DEFAULT_PROMPTFOO_VERSION = "0.122.0"
DEFAULT_CODEX_SDK_VERSION = "0.148.0"
COMPLETED_EXIT_CODES = {0, 100}
IGNORED_WORKSPACE_PARTS = {".agents", ".git", ".promptfoo", "node_modules", "__pycache__"}


class AdapterError(RuntimeError):
    """Raised when the adapter cannot produce an honest comparison receipt."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"cannot read JSON {path}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_under(root: Path, value: str, *, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise AdapterError(f"{label} must be a non-empty relative path")
    if Path(value).is_absolute():
        raise AdapterError(f"{label} must be relative: {value}")
    root = root.resolve()
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise AdapterError(f"{label} escapes {root}: {value}") from exc
    if not candidate.exists():
        raise AdapterError(f"{label} does not exist: {candidate}")
    return candidate


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AdapterError(f"{label} must be a non-empty string")
    return value.strip()


def _normalize_eval_id(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise AdapterError("eval id must be a non-empty string or integer")
    normalized = str(value).strip()
    if not normalized:
        raise AdapterError("eval id must be a non-empty string or integer")
    return normalized


def load_manifest(path: Path) -> dict[str, Any]:
    """Load the shared strict contract before any run workspace is created."""

    try:
        suite = lint_agent_skills_eval_suite(path, root=REPO_ROOT)
    except EvalContractError as exc:
        raise AdapterError(f"eval contract invalid: {exc}") from exc
    return suite.model_dump(mode="json", exclude_none=True)


def load_profile(path: Path) -> dict[str, Any]:
    data = read_json(path)
    if not isinstance(data, dict):
        raise AdapterError("provider profile must be a JSON object")
    provider = _required_text(data.get("provider"), "provider profile provider")
    config = data.get("config", {})
    if not isinstance(config, dict):
        raise AdapterError("provider profile config must be an object")
    forbidden = {"working_dir", "workingDir"}.intersection(config)
    if forbidden:
        raise AdapterError("working_dir belongs to the adapter, not the shared provider profile")
    if config.get("enable_streaming") is not True:
        raise AdapterError("provider profile must set enable_streaming=true for skill-use evidence")
    return {"provider": provider, "config": copy.deepcopy(config)}


def _is_ignored(path: Path) -> bool:
    return any(part in IGNORED_WORKSPACE_PARTS for part in path.parts)


def snapshot_tree(root: Path, *, ignore_runtime: bool = False) -> dict[str, str]:
    if not root.exists():
        return {}
    result: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if ignore_runtime and _is_ignored(relative):
            continue
        result[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def snapshot_digest(snapshot: dict[str, str]) -> str:
    payload = json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def tree_delta(before: dict[str, str], after: dict[str, str]) -> dict[str, list[str]]:
    before_keys = set(before)
    after_keys = set(after)
    return {
        "created": sorted(after_keys - before_keys),
        "modified": sorted(key for key in before_keys & after_keys if before[key] != after[key]),
        "deleted": sorted(before_keys - after_keys),
    }


def _copy_skill(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("evals", "__pycache__", ".DS_Store"),
    )


def materialize_workspace(
    *,
    skill_root: Path,
    case: dict[str, Any],
    destination: Path,
    installed_skill: Path | None,
    skill_name: str,
) -> dict[str, str]:
    metadata = case.get("metadata", {})
    farplane = metadata.get("farplane", {}) if isinstance(metadata, dict) else {}
    fixture_value = farplane.get("workspace_fixture") if isinstance(farplane, dict) else None
    if fixture_value is not None:
        fixture = resolve_under(skill_root, fixture_value, label="workspace_fixture")
        if not fixture.is_dir():
            raise AdapterError("workspace_fixture must resolve to a directory")
        shutil.copytree(fixture, destination)
    else:
        destination.mkdir(parents=True, exist_ok=False)

    for file_value in case["files"]:
        source = resolve_under(skill_root, file_value, label=f"eval {case['id']} file")
        if source.is_dir():
            raise AdapterError(f"eval {case['id']} file must not be a directory: {file_value}")
        target = destination / file_value
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    fixture_snapshot = snapshot_tree(destination, ignore_runtime=True)
    if installed_skill is not None:
        _copy_skill(installed_skill, destination / ".agents" / "skills" / skill_name)
    return fixture_snapshot


def build_rubric(case: dict[str, Any]) -> str:
    lines = [
        "Pass only if the final response satisfies the expected outcome and every listed expectation.",
        f"Expected outcome: {case['expected_output']}",
    ]
    if case["assertions"]:
        lines.append("Expectations:")
        lines.extend(f"- {item}" for item in case["assertions"])
    lines.append("Judge only the visible final response. Do not assume unreported workspace contents.")
    return "\n".join(lines)


def build_promptfoo_config(
    *,
    skill_name: str,
    case: dict[str, Any],
    profile: dict[str, Any],
    candidate_dir: Path,
    baseline_dir: Path,
    grader_dir: Path,
) -> dict[str, Any]:
    providers = []
    for label, working_dir in (("candidate", candidate_dir), ("baseline", baseline_dir)):
        config = copy.deepcopy(profile["config"])
        config["working_dir"] = str(working_dir.resolve())
        providers.append({"id": profile["provider"], "label": label, "config": config})
    grader_config = copy.deepcopy(profile["config"])
    grader_config.update(
        {
            "working_dir": str(grader_dir.resolve()),
            "sandbox_mode": "read-only",
            "approval_policy": "never",
            "network_access_enabled": False,
            "web_search_mode": "disabled",
            "enable_streaming": False,
        }
    )
    return {
        "description": f"Agent Skills comparison: {skill_name}/{case['id']}",
        "prompts": ["{{request}}"],
        "providers": providers,
        "tests": [
            {
                "description": case["id"],
                "vars": {"request": case["prompt"]},
                "assert": [
                    {"type": "skill-used", "value": skill_name, "metric": "skill-used"},
                    {
                        "type": "llm-rubric",
                        "value": build_rubric(case),
                        "metric": "behavior",
                        "provider": {"id": profile["provider"], "config": grader_config},
                    },
                ],
            }
        ],
    }


def _provider_label(row: dict[str, Any]) -> str:
    provider = row.get("provider")
    if isinstance(provider, dict):
        for key in ("label", "displayName", "id"):
            value = provider.get(key)
            if isinstance(value, str) and value:
                return value
    if isinstance(provider, str):
        return provider
    return ""


def _find_variant_row(rows: list[dict[str, Any]], label: str) -> dict[str, Any]:
    exact = [row for row in rows if _provider_label(row) == label]
    if len(exact) == 1:
        return exact[0]
    fuzzy = [row for row in rows if label in _provider_label(row)]
    if len(fuzzy) == 1:
        return fuzzy[0]
    raise AdapterError(f"expected exactly one Promptfoo row for provider label {label}; found {len(exact) or len(fuzzy)}")


def _response_output(response: Any) -> Any:
    if isinstance(response, dict):
        return response.get("output")
    return response


def normalize_row(row: dict[str, Any], *, workspace_delta: dict[str, list[str]]) -> dict[str, Any]:
    grading = row.get("gradingResult")
    if not isinstance(grading, dict):
        grading = {}
    response = row.get("response")
    response_dict = response if isinstance(response, dict) else {}
    success = row.get("success")
    if not isinstance(success, bool):
        success = grading.get("pass") if isinstance(grading.get("pass"), bool) else False
    return {
        "provider": _provider_label(row),
        "pass": success,
        "score": row.get("score", grading.get("score")),
        "reason": row.get("reason", grading.get("reason")),
        "output": _response_output(response),
        "error": response_dict.get("error") or row.get("error"),
        "latency_ms": response_dict.get("latencyMs", row.get("latencyMs")),
        "token_usage": response_dict.get("tokenUsage", row.get("tokenUsage")),
        "metadata": response_dict.get("metadata", {}),
        "assertions": grading.get("componentResults", row.get("componentResults", [])),
        "workspace_delta": workspace_delta,
    }


def normalize_export(
    raw: dict[str, Any],
    *,
    candidate_delta: dict[str, list[str]],
    baseline_delta: dict[str, list[str]],
) -> dict[str, Any]:
    results = raw.get("results")
    rows = None
    if isinstance(results, dict):
        rows = results.get("results")
        if rows is None:
            rows = results.get("outputs")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise AdapterError("Promptfoo export is missing results.results rows")
    candidate = normalize_row(_find_variant_row(rows, "candidate"), workspace_delta=candidate_delta)
    baseline = normalize_row(_find_variant_row(rows, "baseline"), workspace_delta=baseline_delta)
    return {
        "candidate": candidate,
        "baseline": baseline,
        "comparison": {
            "pass_delta": int(candidate["pass"]) - int(baseline["pass"]),
            "candidate_passed": candidate["pass"],
            "baseline_passed": baseline["pass"],
        },
    }


def _safe_label(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-.")
    if not cleaned:
        raise AdapterError("label must contain at least one safe character")
    return cleaned


def _output_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=2, sort_keys=True) if value is not None else ""


def _variant_reason(row: dict[str, Any]) -> str:
    for assertion in reversed(row.get("assertions", [])):
        if isinstance(assertion, dict) and isinstance(assertion.get("reason"), str):
            return assertion["reason"]
    return str(row.get("reason") or row.get("error") or "")


def _office_assertions(row: dict[str, Any]) -> list[dict[str, Any]]:
    projected = []
    for index, component in enumerate(row.get("assertions", []), start=1):
        if not isinstance(component, dict):
            continue
        assertion = component.get("assertion")
        assertion = assertion if isinstance(assertion, dict) else {}
        metric = assertion.get("metric") or assertion.get("type")
        target = assertion.get("value") if assertion.get("type") == "skill-used" else None
        text = f"{metric}: {target}" if metric and target else str(metric or f"Assertion {index}")
        projected.append(
            {
                "text": text,
                "passed": component.get("pass") if isinstance(component.get("pass"), bool) else None,
                "evidence": component.get("reason") if isinstance(component.get("reason"), str) else "",
            }
        )
    return projected


def _office_variant(row: dict[str, Any], artifact_dir: Path) -> dict[str, Any]:
    assertions = _office_assertions(row)
    passed_count = sum(item["passed"] is True for item in assertions)
    failed_count = sum(item["passed"] is False for item in assertions)
    passed = bool(row.get("pass"))
    skill_calls = row.get("metadata", {}).get("skillCalls", []) if isinstance(row.get("metadata"), dict) else []
    return {
        "agent": {"answer": _output_text(row.get("output"))},
        "judge": {
            "pass": passed,
            "verdict": "A" if passed else "D",
            "score": row.get("score"),
            "reason": _variant_reason(row),
        },
        "timing": {
            "duration_ms": row.get("latency_ms"),
            "total_tokens": row.get("token_usage", {}).get("total")
            if isinstance(row.get("token_usage"), dict)
            else None,
        },
        "grading": {
            "assertion_results": assertions,
            "summary": {
                "passed": passed_count,
                "failed": failed_count,
                "total": len(assertions),
            },
        },
        "artifact_dir": str(artifact_dir),
        "skill_triggered": bool(skill_calls),
    }


def _case_title(case: dict[str, Any]) -> str:
    metadata = case.get("metadata")
    farplane = metadata.get("farplane") if isinstance(metadata, dict) else None
    if isinstance(farplane, dict) and isinstance(farplane.get("title"), str):
        return farplane["title"]
    return str(case.get("title") or case["id"])


def write_office_task_detail(
    *, task_dir: Path, case: dict[str, Any], skill_name: str, result: dict[str, Any]
) -> Path:
    task_id = _safe_label(case["id"])
    candidate = _office_variant(result["candidate"], task_dir / "candidate")
    baseline = _office_variant(result["baseline"], task_dir / "baseline")
    for label, variant in (("candidate", candidate), ("baseline", baseline)):
        output_dir = task_dir / label / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "agent_answer.txt").write_text(variant["agent"]["answer"], encoding="utf-8")
        write_json(task_dir / label / "timing.json", variant["timing"])
        write_json(task_dir / label / "grading.json", variant["grading"])
    comparison = result["comparison"]
    delta = (
        "candidate_wins"
        if comparison["candidate_passed"] and not comparison["baseline_passed"]
        else "baseline_wins"
        if comparison["baseline_passed"] and not comparison["candidate_passed"]
        else "no_measured_lift"
    )
    office_comparison = {
        "delta": delta,
        "skill_value": comparison["candidate_passed"] and not comparison["baseline_passed"],
    }
    write_json(task_dir / "comparison.json", office_comparison)
    detail_path = task_dir.parent / f"{task_id}.json"
    write_json(
        detail_path,
        {
            "schema_version": SCHEMA_VERSION,
            "task_id": task_id,
            "title": _case_title(case),
            "task": {
                "id": task_id,
                "title": _case_title(case),
                "prompt": case["prompt"],
                "expected": case["expected_output"],
                "rubric": build_rubric(case),
                "tags": ["skill", skill_name, "promptfoo"],
            },
            "candidate": candidate,
            "baseline": baseline,
            "comparison": office_comparison,
            "artifacts": {
                "promptfoo_config": str(task_dir / "promptfooconfig.json"),
                "promptfoo_result": str(task_dir / "promptfoo-results.json"),
                "normalized_result": str(task_dir / "normalized.json"),
                "comparison": str(task_dir / "comparison.json"),
            },
            "raw": result,
        },
    )
    return detail_path


def publish_office_run(
    *,
    runs_dir: Path,
    job_dir: Path,
    summary: dict[str, Any],
    cases: list[dict[str, Any]],
    label: str,
    judge_harness: str,
) -> None:
    cases_by_id = {case["id"]: case for case in cases}
    tasks = []
    verdict_counts: dict[str, int] = {}
    completed_results = [result for result in summary["results"] if "candidate" in result]
    for result in completed_results:
        case = cases_by_id[result["eval_id"]]
        task_id = _safe_label(case["id"])
        task_dir = job_dir / "tasks" / task_id
        detail_path = write_office_task_detail(
            task_dir=task_dir,
            case=case,
            skill_name=summary["skill_name"],
            result=result,
        )
        passed = bool(result["candidate"]["pass"])
        verdict = "A" if passed else "D"
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
        tasks.append(
            {
                "task_id": task_id,
                "title": _case_title(case),
                "pass": passed,
                "verdict": verdict,
                "reason": _variant_reason(result["candidate"]),
                "detail_path": str(detail_path),
                "tags": ["skill", summary["skill_name"], "promptfoo"],
            }
        )
    summary.update(
        {
            "label": label,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "harness": "promptfoo",
            "judge_harness": judge_harness,
            "suite": summary["skill_name"],
            "task_count": len(tasks),
            "pass_rate": (sum(task["pass"] for task in tasks) / len(tasks)) if tasks else None,
            "verdict_counts": verdict_counts,
            "tasks": tasks,
        }
    )
    write_json(job_dir / "summary.json", summary)
    if summary.get("dry_run"):
        return
    index_path = runs_dir / "index.json"
    existing = read_json(index_path) if index_path.exists() else []
    if isinstance(existing, dict):
        existing = existing.get("runs")
    if not isinstance(existing, list) or any(not isinstance(row, dict) for row in existing):
        raise AdapterError(f"eval run index must be a list or an object with runs: {index_path}")
    entry = {
        "schema_version": SCHEMA_VERSION,
        "job_id": summary["job_id"],
        "label": label,
        "created_at": summary["created_at"],
        "completed_at": summary["completed_at"],
        "summary_path": str(job_dir / "summary.json"),
        "task_count": summary["task_count"],
        "pass_rate": summary["pass_rate"],
        "verdict_counts": verdict_counts,
        "harness": "promptfoo",
    }
    write_json(index_path, [entry, *(row for row in existing if row.get("job_id") != summary["job_id"])])


def _new_job_dir(root: Path, label: str) -> tuple[str, Path]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = f"{timestamp}-{_safe_label(label)}"
    for suffix in range(1000):
        job_id = base if suffix == 0 else f"{base}-{suffix}"
        path = root / job_id
        try:
            path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        return job_id, path
    raise AdapterError("could not allocate a unique eval job directory")


def default_office_runs_dir() -> Path:
    explicit_root = os.environ.get("FARPLANE_EVALS_ROOT", "").strip()
    if explicit_root:
        return Path(explicit_root).expanduser() / "runs"
    global_runs = Path.home() / ".farplane" / "evals" / "runs"
    if (global_runs / "index.json").exists():
        return global_runs
    return Path(".farplane/evals/runs")


def _selected_cases(manifest: dict[str, Any], requested: Iterable[str]) -> list[dict[str, Any]]:
    requested_set = {_normalize_eval_id(item) for item in requested}
    if not requested_set:
        return manifest["evals"]
    selected = [case for case in manifest["evals"] if case["id"] in requested_set]
    found = {case["id"] for case in selected}
    missing = sorted(requested_set - found)
    if missing:
        raise AdapterError(f"unknown eval ids: {', '.join(missing)}")
    return selected


def run_case(
    *,
    case: dict[str, Any],
    skill_name: str,
    skill_root: Path,
    candidate_skill: Path,
    baseline_skill: Path | None,
    profile: dict[str, Any],
    task_dir: Path,
    promptfoo_version: str,
    codex_sdk_version: str,
    dry_run: bool,
) -> dict[str, Any]:
    task_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"farplane-eval-{_safe_label(case['id'])}-") as temp:
        workspace_root = Path(temp)
        candidate_dir = workspace_root / "candidate"
        baseline_dir = workspace_root / "baseline"
        grader_dir = workspace_root / "grader"
        grader_dir.mkdir()
        try:
            candidate_before = materialize_workspace(
                skill_root=skill_root,
                case=case,
                destination=candidate_dir,
                installed_skill=candidate_skill,
                skill_name=skill_name,
            )
            baseline_before = materialize_workspace(
                skill_root=skill_root,
                case=case,
                destination=baseline_dir,
                installed_skill=baseline_skill,
                skill_name=skill_name,
            )
            if candidate_before != baseline_before:
                raise AdapterError(f"eval {case['id']} candidate and baseline fixtures differ before execution")

            config = build_promptfoo_config(
                skill_name=skill_name,
                case=case,
                profile=profile,
                candidate_dir=candidate_dir,
                baseline_dir=baseline_dir,
                grader_dir=grader_dir,
            )
            config_path = task_dir / "promptfooconfig.json"
            raw_path = task_dir / "promptfoo-results.json"
            write_json(config_path, config)
            command = [
                "npx",
                "--yes",
                "--package",
                f"promptfoo@{promptfoo_version}",
                "--package",
                f"@openai/codex-sdk@{codex_sdk_version}",
                "promptfoo",
                "eval",
                "--config",
                str(config_path),
                "--no-cache",
                "--max-concurrency",
                "1",
                "--output",
                str(raw_path),
            ]
            write_json(task_dir / "command.json", {"argv": command})
            if dry_run:
                return {
                    "eval_id": case["id"],
                    "status": "dry-run",
                    "fixture_digest": snapshot_digest(candidate_before),
                    "config": str(config_path),
                }

            env = os.environ.copy()
            env["PROMPTFOO_DISABLE_TELEMETRY"] = "1"
            env["PROMPTFOO_DISABLE_UPDATE"] = "1"
            completed = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
            (task_dir / "stdout.log").write_text(completed.stdout, encoding="utf-8")
            (task_dir / "stderr.log").write_text(completed.stderr, encoding="utf-8")
            if completed.returncode not in COMPLETED_EXIT_CODES:
                raise AdapterError(f"Promptfoo runtime failed for eval {case['id']} with exit {completed.returncode}")
            if not raw_path.exists():
                raise AdapterError(f"Promptfoo completed eval {case['id']} without a JSON export")

            candidate_after = snapshot_tree(candidate_dir, ignore_runtime=True)
            baseline_after = snapshot_tree(baseline_dir, ignore_runtime=True)
            normalized = normalize_export(
                read_json(raw_path),
                candidate_delta=tree_delta(candidate_before, candidate_after),
                baseline_delta=tree_delta(baseline_before, baseline_after),
            )
            normalized.update(
                {
                    "eval_id": case["id"],
                    "promptfoo_exit_code": completed.returncode,
                    "fixture_digest": snapshot_digest(candidate_before),
                    "config": str(config_path),
                    "raw_result": str(raw_path),
                }
            )
            normalized["candidate"]["workspace_artifact"] = str(task_dir / "candidate" / "workspace")
            normalized["baseline"]["workspace_artifact"] = str(task_dir / "baseline" / "workspace")
            write_json(task_dir / "normalized.json", normalized)
            return normalized
        finally:
            for label, source in (("candidate", candidate_dir), ("baseline", baseline_dir)):
                if source.exists():
                    shutil.copytree(source, task_dir / label / "workspace")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-file", type=Path, required=True)
    parser.add_argument("--provider-profile", type=Path, required=True)
    parser.add_argument("--candidate-skill", type=Path)
    parser.add_argument("--baseline-skill", type=Path)
    parser.add_argument("--eval-id", action="append", default=[])
    parser.add_argument("--runs-dir", type=Path, default=default_office_runs_dir())
    parser.add_argument("--label", required=True)
    parser.add_argument("--promptfoo-version", default=DEFAULT_PROMPTFOO_VERSION)
    parser.add_argument("--codex-sdk-version", default=DEFAULT_CODEX_SDK_VERSION)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        eval_file = args.eval_file.resolve()
        manifest = load_manifest(eval_file)
        profile = load_profile(args.provider_profile.resolve())
        skill_root = eval_file.parent.parent.resolve()
        candidate_skill = (args.candidate_skill or skill_root).resolve()
        baseline_skill = args.baseline_skill.resolve() if args.baseline_skill else None
        if not candidate_skill.is_dir():
            raise AdapterError(f"candidate skill directory does not exist: {candidate_skill}")
        if baseline_skill is not None and not baseline_skill.is_dir():
            raise AdapterError(f"baseline skill directory does not exist: {baseline_skill}")

        source_paths = [eval_file, candidate_skill]
        if baseline_skill:
            source_paths.append(baseline_skill)
        source_before = {str(path): snapshot_tree(path) if path.is_dir() else hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
        job_id, job_dir = _new_job_dir(args.runs_dir.resolve(), args.label)
        selected_cases = _selected_cases(manifest, args.eval_id)
        results = []
        for case in selected_cases:
            results.append(
                run_case(
                    case=case,
                    skill_name=manifest["skill_name"],
                    skill_root=skill_root,
                    candidate_skill=candidate_skill,
                    baseline_skill=baseline_skill,
                    profile=profile,
                    task_dir=job_dir / "tasks" / _safe_label(case["id"]),
                    promptfoo_version=args.promptfoo_version,
                    codex_sdk_version=args.codex_sdk_version,
                    dry_run=args.dry_run,
                )
            )
        source_after = {str(path): snapshot_tree(path) if path.is_dir() else hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
        summary = {
            "schema_version": SCHEMA_VERSION,
            "runner": "promptfoo",
            "job_id": job_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source_eval_file": str(eval_file),
            "skill_name": manifest["skill_name"],
            "promptfoo_version": args.promptfoo_version,
            "codex_sdk_version": args.codex_sdk_version,
            "dry_run": args.dry_run,
            "source_hashes_unchanged": source_before == source_after,
            "candidate_gate_passed": None
            if args.dry_run
            else all(result["candidate"]["pass"] for result in results),
            "results": results,
        }
        if not summary["source_hashes_unchanged"]:
            raise AdapterError("eval execution mutated source fixtures or skills")
        publish_office_run(
            runs_dir=args.runs_dir.resolve(),
            job_dir=job_dir,
            summary=summary,
            cases=selected_cases,
            label=args.label,
            judge_harness=profile["provider"],
        )
        print(job_dir / "summary.json")
        return 0 if summary["candidate_gate_passed"] is not False else 3
    except AdapterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
