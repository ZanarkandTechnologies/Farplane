#!/usr/bin/env python3
"""Scaffold and run harness-native evals for Codex and Claude."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_MAX_PARALLEL_TASKS = 2
SUITE_FILES = {
    "harness": "harness_tasks.json",
}
REQUIRED_EVAL_FILES = (
    "run_evals.py",
    "viewer.html",
    "viewer-react/package.json",
    "viewer-react/src/App.tsx",
    "prompts/agent.md",
    "prompts/judge.md",
    "tasks/harness_tasks.json",
)


class EvalError(ValueError):
    """Raised when eval input, command execution, or judge output is invalid."""


@dataclass(frozen=True)
class EvalTask:
    id: str
    title: str
    query: str
    reference_points: tuple[str, ...]
    tags: tuple[str, ...]
    notes: str


@dataclass(frozen=True)
class CommandResult:
    text: str
    returncode: int
    raw_stdout: str
    raw_stderr: str


def script_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_eval_dir(harness: str, target_root: Path) -> Path:
    if harness == "codex":
        return target_root / ".codex" / "evals"
    if harness == "claude":
        return target_root / ".claude" / "evals"
    raise EvalError("custom harness requires --eval-dir")


def read_text(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError as exc:
        raise EvalError(f"file not found: {path}") from exc


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise EvalError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvalError(f"{path}: invalid JSON: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def require_string(raw: dict[str, Any], field: str, path: Path) -> str:
    value = raw.get(field)
    if not isinstance(value, str) or not value.strip():
        raise EvalError(f"{path}: {field} must be a non-empty string")
    return value.strip()


def load_tasks(path: Path, limit: int | None = None) -> list[EvalTask]:
    raw = read_json(path)
    if not isinstance(raw, list):
        raise EvalError(f"{path}: task file must contain a JSON list")
    tasks: list[EvalTask] = []
    for item in raw:
        if not isinstance(item, dict):
            raise EvalError(f"{path}: each task must be an object")
        refs = item.get("reference_points")
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref.strip() for ref in refs):
            raise EvalError(f"{path}: task {item.get('id', '<unknown>')} reference_points must be non-empty strings")
        tags = item.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise EvalError(f"{path}: task {item.get('id', '<unknown>')} tags must be strings")
        tasks.append(
            EvalTask(
                id=require_string(item, "id", path),
                title=require_string(item, "title", path),
                query=require_string(item, "query", path),
                reference_points=tuple(ref.strip() for ref in refs),
                tags=tuple(tag.strip() for tag in tags if tag.strip()),
                notes=str(item.get("notes", "")).strip(),
            )
        )
    return tasks[:limit] if limit else tasks


def resolve_task_paths(eval_dir: Path, tasks: str | None, suite: str) -> list[Path]:
    if tasks:
        return [Path(tasks)]
    return [eval_dir / "tasks" / SUITE_FILES[suite]]


def load_task_suite(paths: Sequence[Path], limit: int | None = None) -> list[EvalTask]:
    loaded: list[EvalTask] = []
    for path in paths:
        loaded.extend(load_tasks(path))
    return loaded[:limit] if limit else loaded


def task_to_json(task: EvalTask) -> str:
    return json.dumps(
        {
            "id": task.id,
            "title": task.title,
            "query": task.query,
            "reference_points": list(task.reference_points),
            "tags": list(task.tags),
            "notes": task.notes,
        },
        indent=2,
    )


def render_template(template: str, task: EvalTask, answer: str = "") -> str:
    rendered = template
    replacements = {
        "{query}": task.query,
        "{task_json}": task_to_json(task),
        "{answer}": answer,
        "{reference_points}": json.dumps(list(task.reference_points), indent=2),
    }
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def build_job_id(label: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", label.strip().lower()).strip("-") or "run"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{safe}"


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise EvalError("judge output did not contain a JSON object")
        parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise EvalError("judge output JSON must be an object")
    return parsed


def normalize_judge(raw: dict[str, Any]) -> dict[str, Any]:
    verdict = str(raw.get("verdict", "")).strip().upper()
    legacy_verdicts = {
        "PASS": "A",
        "PARTIAL": "B",
        "FAIL": "D",
        "BLOCKED": "D",
    }
    verdict = legacy_verdicts.get(verdict, verdict)
    if verdict not in {"A", "B", "C", "D"}:
        verdict = "A" if bool(raw.get("pass", False)) else "D"
    rubric = raw.get("rubric", {})
    if not isinstance(rubric, dict):
        rubric = {}
    return {
        "verdict": verdict,
        "pass": bool(raw.get("pass", verdict == "A")),
        "rubric": rubric,
        "reference_point_results": raw.get("reference_point_results", []),
        "reason": str(raw.get("reason", "")).strip(),
        "raw": raw,
    }


def run_custom_command(command_template: str, prompt: str, output_file: Path, cwd: Path) -> CommandResult:
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".md") as prompt_file:
        prompt_file.write(prompt)
        prompt_path = Path(prompt_file.name)
    command = command_template.format(
        prompt_file=str(prompt_path),
        output_file=str(output_file),
        cwd=str(cwd),
    )
    try:
        completed = subprocess.run(
            shlex.split(command),
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        prompt_path.unlink(missing_ok=True)
    text = output_file.read_text() if output_file.exists() else completed.stdout
    return CommandResult(text=text, returncode=completed.returncode, raw_stdout=completed.stdout, raw_stderr=completed.stderr)


def run_codex(prompt: str, output_file: Path, cwd: Path, extra_args: Sequence[str]) -> CommandResult:
    command = [
        "codex",
        "exec",
        "--json",
        "-C",
        str(cwd),
        "-o",
        str(output_file),
        *extra_args,
        "-",
    ]
    completed = subprocess.run(command, input=prompt, text=True, capture_output=True, check=False)
    text = output_file.read_text() if output_file.exists() else completed.stdout
    return CommandResult(text=text, returncode=completed.returncode, raw_stdout=completed.stdout, raw_stderr=completed.stderr)


def run_claude(prompt: str, output_file: Path, cwd: Path, extra_args: Sequence[str]) -> CommandResult:
    command = ["claude", "-p", "--output-format", "text", *extra_args, prompt]
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    output_file.write_text(completed.stdout)
    return CommandResult(text=completed.stdout, returncode=completed.returncode, raw_stdout=completed.stdout, raw_stderr=completed.stderr)


def run_harness(
    harness: str,
    prompt: str,
    output_file: Path,
    cwd: Path,
    command_template: str | None,
    extra_args: Sequence[str],
) -> CommandResult:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if command_template:
        return run_custom_command(command_template, prompt, output_file, cwd)
    if harness == "codex":
        return run_codex(prompt, output_file, cwd, extra_args)
    if harness == "claude":
        return run_claude(prompt, output_file, cwd, extra_args)
    raise EvalError("custom harness requires a command template")


def task_detail_path(job_dir: Path, task_id: str) -> Path:
    return job_dir / "tasks" / f"{task_id}.json"


def run_task(
    task: EvalTask,
    args: argparse.Namespace,
    eval_dir: Path,
    job_dir: Path,
    agent_template: str,
    judge_template: str,
) -> dict[str, Any]:
    task_dir = job_dir / "tasks" / task.id
    task_dir.mkdir(parents=True, exist_ok=True)
    agent_prompt = render_template(agent_template, task)
    agent_prompt_path = task_dir / "agent_prompt.md"
    agent_answer_path = task_dir / "agent_answer.txt"
    agent_prompt_path.write_text(agent_prompt)
    agent_result = run_harness(
        args.farplane,
        agent_prompt,
        agent_answer_path,
        Path(args.target_root).resolve(),
        args.agent_command_template,
        args.agent_extra_arg,
    )
    if agent_result.returncode != 0:
        judge = {
            "verdict": "D",
            "pass": False,
            "rubric": {},
            "reference_point_results": [],
            "reason": f"agent command failed with exit code {agent_result.returncode}",
        }
    else:
        judge_prompt = render_template(judge_template, task, answer=agent_result.text)
        judge_prompt_path = task_dir / "judge_prompt.md"
        judge_answer_path = task_dir / "judge_answer.txt"
        judge_prompt_path.write_text(judge_prompt)
        judge_result = run_harness(
            args.judge_harness or args.farplane,
            judge_prompt,
            judge_answer_path,
            Path(args.target_root).resolve(),
            args.judge_command_template,
            args.judge_extra_arg,
        )
        if judge_result.returncode != 0:
            judge = {
                "verdict": "D",
                "pass": False,
                "rubric": {},
                "reference_point_results": [],
                "reason": f"judge command failed with exit code {judge_result.returncode}",
                "raw_response": judge_result.text,
            }
        else:
            judge = normalize_judge(extract_json_object(judge_result.text))
            judge["raw_response"] = judge_result.text
            (task_dir / "judge_stdout.log").write_text(judge_result.raw_stdout)
            (task_dir / "judge_stderr.log").write_text(judge_result.raw_stderr)
    (task_dir / "agent_stdout.log").write_text(agent_result.raw_stdout)
    (task_dir / "agent_stderr.log").write_text(agent_result.raw_stderr)
    detail = {
        "task": json.loads(task_to_json(task)),
        "run_config": {
            "harness": args.farplane,
            "judge_harness": args.judge_harness or args.farplane,
        },
        "agent": {
            "returncode": agent_result.returncode,
            "answer_path": str(agent_answer_path),
        },
        "judge": judge,
    }
    write_json(task_detail_path(job_dir, task.id), detail)
    return {
        "task_id": task.id,
        "title": task.title,
        "verdict": judge.get("verdict", "fail"),
        "pass": judge["pass"],
        "reason": judge["reason"],
        "detail_path": str(task_detail_path(job_dir, task.id)),
    }


def update_index(runs_dir: Path, summary: dict[str, Any]) -> None:
    index_path = runs_dir / "index.json"
    existing = read_json(index_path) if index_path.exists() else []
    if not isinstance(existing, list):
        existing = []
    compact = {
        "job_id": summary["job_id"],
        "label": summary["label"],
        "created_at": summary["created_at"],
        "task_count": summary["task_count"],
        "pass_rate": summary["pass_rate"],
        "verdict_counts": summary["verdict_counts"],
        "harness": summary["harness"],
    }
    write_json(index_path, [compact, *[row for row in existing if row.get("job_id") != summary["job_id"]]])


def inspect_eval_setup(harness: str, target_root: Path, eval_dir: str | None) -> tuple[Path, list[str]]:
    resolved_eval_dir = Path(eval_dir).resolve() if eval_dir else default_eval_dir(harness, target_root.resolve())
    missing = [relative for relative in REQUIRED_EVAL_FILES if not (resolved_eval_dir / relative).exists()]
    return resolved_eval_dir, missing


def command_status(args: argparse.Namespace) -> int:
    eval_dir, missing = inspect_eval_setup(args.farplane, Path(args.target_root), args.eval_dir)
    if missing:
        print(f"Eval setup missing in {eval_dir}")
        for relative in missing:
            print(f"- {relative}")
        print("")
        print(f"Initialize it with: python3 skills/eval/scripts/run_evals.py init --harness {args.farplane} --target-root {Path(args.target_root).resolve()}")
        return 1
    print(f"Eval setup ready in {eval_dir}")
    return 0


def command_run(args: argparse.Namespace) -> int:
    eval_dir = Path(args.eval_dir).resolve() if args.eval_dir else default_eval_dir(args.farplane, Path(args.target_root).resolve())
    task_paths = resolve_task_paths(eval_dir, args.tasks, args.suite)
    tasks = load_task_suite(task_paths, args.limit)
    if args.max_parallel_tasks < 1:
        raise EvalError("--max-parallel-tasks must be at least 1")
    agent_template = read_text(Path(args.agent_prompt or eval_dir / "prompts" / "agent.md"))
    judge_template = read_text(Path(args.judge_prompt or eval_dir / "prompts" / "judge.md"))
    runs_dir = Path(args.runs_dir).resolve() if args.runs_dir else eval_dir / "runs"
    job_id = build_job_id(args.label)
    job_dir = runs_dir / job_id
    (job_dir / "tasks").mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc).isoformat()
    summary_tasks: list[dict[str, Any] | None] = [None] * len(tasks)
    max_workers = min(args.max_parallel_tasks, len(tasks)) or 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(run_task, task, args, eval_dir, job_dir, agent_template, judge_template): index
            for index, task in enumerate(tasks)
        }
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            summary_tasks[index] = future.result()
    rows = [row for row in summary_tasks if row is not None]
    pass_rate = round(sum(1 for row in rows if row["pass"]) / len(rows), 2) if rows else 0
    verdict_counts: dict[str, int] = {}
    for row in rows:
        verdict = str(row["verdict"])
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
    summary = {
        "job_id": job_id,
        "label": args.label,
        "created_at": created_at,
        "harness": args.farplane,
        "judge_harness": args.judge_harness or args.farplane,
        "suite": args.suite if not args.tasks else "custom",
        "task_files": [str(path) for path in task_paths],
        "task_count": len(rows),
        "pass_rate": pass_rate,
        "verdict_counts": verdict_counts,
        "tasks": rows,
    }
    write_json(job_dir / "summary.json", summary)
    update_index(runs_dir, summary)
    print(f"Wrote {job_dir}")
    return 0 if all(row["pass"] for row in rows) else 1


def copy_template(src: Path, dest: Path, force: bool) -> None:
    if dest.exists() and not force:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)


def copy_template_dir(src: Path, dest: Path, force: bool) -> None:
    if dest.exists() and not force:
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("node_modules", "dist", ".vite", "*.tsbuildinfo"))


def command_init(args: argparse.Namespace) -> int:
    target_root = Path(args.target_root).resolve()
    eval_dir = Path(args.eval_dir).resolve() if args.eval_dir else default_eval_dir(args.farplane, target_root)
    templates = script_root() / "templates"
    copy_template(templates / "harness_tasks.json", eval_dir / "tasks" / "harness_tasks.json", args.force)
    copy_template(templates / "agent.md", eval_dir / "prompts" / "agent.md", args.force)
    copy_template(templates / "judge.md", eval_dir / "prompts" / "judge.md", args.force)
    copy_template(templates / "README.md", eval_dir / "README.md", args.force)
    copy_template(templates / "viewer.html", eval_dir / "viewer.html", args.force)
    copy_template_dir(templates / "viewer-react", eval_dir / "viewer-react", args.force)
    copy_template(Path(__file__).resolve(), eval_dir / "run_evals.py", args.force)
    (eval_dir / "runs").mkdir(parents=True, exist_ok=True)
    print(f"Initialized {eval_dir}")
    print("")
    print("Next steps:")
    print(f"  1. Edit {eval_dir / 'tasks' / 'harness_tasks.json'} with one important skill, workflow, or system-prompt task.")
    print("  2. Use tags/notes to mark whether a task is skill, workflow, or system-prompt level.")
    print(f"  3. Run: python3 {eval_dir / 'run_evals.py'} run --harness {args.farplane} --label baseline --limit 1")
    print(f"  4. Inspect results with either {eval_dir / 'viewer.html'} or the React viewer:")
    print(f"     cd {eval_dir / 'viewer-react'} && pnpm install && pnpm dev --host 127.0.0.1")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create .codex/evals or .claude/evals")
    init_parser.add_argument("--harness", choices=["codex", "claude", "custom"], required=True)
    init_parser.add_argument("--target-root", default=".")
    init_parser.add_argument("--eval-dir")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=command_init)

    status_parser = subparsers.add_parser("status", help="Check whether eval files are installed")
    status_parser.add_argument("--harness", choices=["codex", "claude", "custom"], required=True)
    status_parser.add_argument("--target-root", default=".")
    status_parser.add_argument("--eval-dir")
    status_parser.set_defaults(func=command_status)

    run_parser = subparsers.add_parser("run", help="Run eval tasks")
    run_parser.add_argument("--harness", choices=["codex", "claude", "custom"], required=True)
    run_parser.add_argument("--judge-harness", choices=["codex", "claude", "custom"])
    run_parser.add_argument("--target-root", default=".")
    run_parser.add_argument("--eval-dir")
    run_parser.add_argument("--tasks")
    run_parser.add_argument(
        "--suite",
        choices=["harness"],
        default="harness",
        help="Built-in task suite to run when --tasks is not provided.",
    )
    run_parser.add_argument("--agent-prompt")
    run_parser.add_argument("--judge-prompt")
    run_parser.add_argument("--label", required=True)
    run_parser.add_argument("--limit", type=int, default=0)
    run_parser.add_argument("--max-parallel-tasks", type=int, default=DEFAULT_MAX_PARALLEL_TASKS)
    run_parser.add_argument("--runs-dir")
    run_parser.add_argument("--agent-command-template")
    run_parser.add_argument("--judge-command-template")
    run_parser.add_argument("--agent-extra-arg", action="append", default=[])
    run_parser.add_argument("--judge-extra-arg", action="append", default=[])
    run_parser.set_defaults(func=command_run)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except EvalError as exc:
        print(f"eval error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
