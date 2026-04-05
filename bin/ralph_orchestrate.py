#!/usr/bin/env python3
"""
RALPH ORCHESTRATOR
==================
Purpose

Compose one Ralph `skill` worker plus one judge into a minimal explicit loop step.

KEY CONCEPTS:
- prompt file is the `skill` contract
- worker runs one bounded `skill`
- judge reads ticket + result and decides the next transition

USAGE:
- python3 bin/ralph_orchestrate.py --ticket <path> --phase <phase>

MEMORY REFERENCES:
- MEM-0001
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ALLOWED_PHASES = {
    "planning",
    "building",
    "documenting",
}

RESULT_PATTERN = re.compile(r"^RALPH_RESULT:\s+status=.*$", re.MULTILINE)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def resolve_root() -> Path:
    return Path(__file__).resolve().parent.parent


def resolve_existing_path(root: Path, raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    if candidate.exists():
        return candidate.resolve()
    return (root / candidate).resolve()


def ticket_id_from_path(path: Path) -> str:
    match = re.search(r"(TASK-\d{4})", path.name)
    if not match:
        raise ValueError(f"could not determine ticket id from {path}")
    return match.group(1)


def default_run_state_path(root: Path, ticket_id: str, phase: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return root / ".ralph" / "runs" / f"{ticket_id.lower()}-{phase}-{stamp}.json"


def current_run_state_path(root: Path) -> Path:
    return root / ".ralph" / "state" / "current-run.json"


def write_run_state(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_current_run(root: Path, payload: dict[str, object]) -> None:
    current_path = current_run_state_path(root)
    current_payload = {
        "schema_version": "1.0",
        "run_id": payload["run_id"],
        "ticket_id": payload["ticket_id"],
        "ticket_path": payload["ticket_path"],
        "phase": payload["phase"],
        "status": payload["status"],
        "prompt_file": payload["prompt_file"],
        "updated_at": payload["updated_at"],
    }
    if "session_id" in payload:
        current_payload["session_id"] = payload["session_id"]
    if "next_phase" in payload:
        current_payload["next_phase"] = payload["next_phase"]
    if "last_judge_verdict" in payload:
        current_payload["last_judge_verdict"] = payload["last_judge_verdict"]
    write_run_state(current_path, current_payload)


def build_initial_run_state(ticket_id: str, ticket_path: Path, phase: str, prompt_file: str, compute_class: str) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "run_id": path_stem(ticket_id, phase),
        "ticket_id": ticket_id,
        "ticket_path": str(ticket_path),
        "phase": phase,
        "status": "running",
        "attempt": 1,
        "prompt_file": prompt_file,
        "compute_class": compute_class,
        "parallel_slots_reserved": 1,
        "updated_at": now_iso(),
    }


def path_stem(ticket_id: str, phase: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"run-{ticket_id.lower()}-{phase}-{stamp}"


def worker_script(root: Path) -> Path:
    return root / "bin" / "ralph_worker.sh"


def judge_script(root: Path) -> Path:
    return root / "bin" / "ralph_judge.py"


def prompt_file_for_phase(phase: str) -> str:
    mapping = {
        "planning": "prompts/ralphplan.md",
        "building": "prompts/ralph.md",
        "documenting": "prompts/ralph-docs.md",
    }
    return mapping[phase]


def run_worker(root: Path, ticket: Path, phase: str, run_state: Path, executor_target: str | None, dry_run: bool) -> str:
    command = [
        "bash",
        str(worker_script(root)),
        "--ticket",
        str(ticket),
        "--phase",
        phase,
        "--run-state",
        str(run_state),
    ]
    if executor_target:
        command.extend(["--executor-target", executor_target])
    if dry_run:
        command.append("--dry-run")

    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        cwd=root,
        check=False,
    )
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

    if completed.returncode != 0:
        message = stderr or stdout or "worker failed"
        raise RuntimeError(message)

    if dry_run:
        dry_run_result = {
            "planning": "RALPH_RESULT: status=plan_ready next=building reason=dry_run",
            "building": "RALPH_RESULT: status=build_complete next=building reason=dry_run",
            "documenting": "RALPH_RESULT: status=docs_complete next=done reason=dry_run",
        }
        return dry_run_result[phase]

    match = RESULT_PATTERN.findall(stdout)
    if not match:
        raise RuntimeError("worker output missing RALPH_RESULT line")
    return match[-1].strip()


def run_judge(root: Path, ticket: Path, phase: str, worker_result: str) -> dict[str, object]:
    completed = subprocess.run(
        [
            sys.executable,
            str(judge_script(root)),
            "--ticket",
            str(ticket),
            "--phase",
            phase,
            "--worker-result",
            worker_result,
        ],
        text=True,
        capture_output=True,
        cwd=root,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "judge failed")
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--phase", required=True, choices=sorted(ALLOWED_PHASES))
    parser.add_argument("--run-state")
    parser.add_argument("--executor-target")
    parser.add_argument("--compute-class", default="local", choices=["local", "local_worktree", "remote_vm", "remote_container"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = resolve_root()
    ticket = resolve_existing_path(root, args.ticket)
    if not ticket.is_file():
        raise SystemExit(f"ticket not found: {ticket}")

    ticket_id = ticket_id_from_path(ticket)
    run_state = resolve_existing_path(root, args.run_state) if args.run_state else default_run_state_path(root, ticket_id, args.phase)

    state = build_initial_run_state(ticket_id, ticket, args.phase, prompt_file_for_phase(args.phase), args.compute_class)
    if args.executor_target:
        state["executor_target"] = args.executor_target
    write_run_state(run_state, state)
    write_current_run(root, state)

    try:
        worker_result = run_worker(root, ticket, args.phase, run_state, args.executor_target, args.dry_run)
        verdict = run_judge(root, ticket, args.phase, worker_result)

        state["last_worker_result"] = worker_result
        state["last_judge_verdict"] = str(verdict["decision"])
        next_phase = verdict.get("next_phase")
        if isinstance(next_phase, str):
            state["next_phase"] = next_phase
        state["status"] = "complete" if verdict["decision"] in {"complete_ticket", "block_ticket", "escalate_to_operator"} else "waiting_for_worker"
        state["updated_at"] = now_iso()
        write_run_state(run_state, state)
        write_current_run(root, state)
    except Exception as exc:
        state["status"] = "failed"
        state["error"] = str(exc)
        state["updated_at"] = now_iso()
        write_run_state(run_state, state)
        write_current_run(root, state)
        raise

    payload = {
        "ticket": str(ticket),
        "phase": args.phase,
        "run_state": str(run_state),
        "worker_result": worker_result,
        "judge_verdict": verdict,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"ticket={ticket}")
        print(f"phase={args.phase}")
        print(f"run_state={run_state}")
        print(worker_result)
        print(json.dumps(verdict, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
