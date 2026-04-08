#!/usr/bin/env python3
"""
Run local Ralph smoke evals against the current prototype.

This script avoids live Codex sessions where possible and focuses on:
- hook payload replay behavior
- state-first active-ticket selection
- tmux follow-up lane spawning in bounded dry-run mode
- judge edge cases across completion, blocking, and retry paths
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STOP_HOOK_PATH = ROOT / "bin" / "stop_hook.py"


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd or ROOT, env=env, text=True, capture_output=True, check=False)


def load_stop_hook_module():
    bin_dir = str(STOP_HOOK_PATH.parent)
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    spec = importlib.util.spec_from_file_location("codexter_stop_hook_eval", STOP_HOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load stop hook module from {STOP_HOOK_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_case(results: list[dict[str, object]], *, name: str, predicate, message: str) -> None:
    case = next(item for item in results if item["name"] == name)
    if not predicate(case):
        raise AssertionError(f"{name}: {message}\nstdout={case['stdout']}\nstderr={case['stderr']}")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def wait_for_json(path: Path, *, timeout_secs: float = 20.0) -> dict[str, object] | None:
    deadline = time.time() + timeout_secs
    while time.time() < deadline:
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                payload = None
            if isinstance(payload, dict):
                return payload
        time.sleep(0.2)
    return None


def wait_for_lane_tail(run_state: Path, *, timeout_secs: float = 20.0) -> str:
    deadline = time.time() + timeout_secs
    latest = ""
    while time.time() < deadline:
        captured = run(
            [
                "python3",
                "skills/impl/scripts/tmux_helper.py",
                "tail",
                "--run-state",
                str(run_state),
                "--lines",
                "120",
            ],
            cwd=ROOT,
        )
        if captured.returncode == 0:
            latest = captured.stdout.strip()
            if "[impl tmux dry run] followup" in latest:
                return latest
        elif captured.stderr.strip():
            latest = captured.stderr.strip()
        time.sleep(0.2)
    return latest


def fixture_ticket(*, ticket_id: str, title: str, acceptance_checked: bool, evidence_checked: bool, blockers: list[str] | None = None, phase: str = "building") -> str:
    acc = "x" if acceptance_checked else " "
    ev = "x" if evidence_checked else " "
    blocker_lines = ["- none"] if not blockers else [f"- {item}" for item in blockers]
    status = "review" if phase == "planning" else "building"
    return f"""---
ticket_id: {ticket_id}
title: {title}
phase: {phase}
status: {status}
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T00:00:00Z
next_action: test fixture
last_verification: none
linked_docs: []
---

# {ticket_id}: {title}

## Acceptance Criteria
- [{acc}] AC-1

## Evidence
- [{ev}] Tests

## Blockers
{chr(10).join(blocker_lines)}
"""


def run_judge_fixture(*, ticket_text: str, phase: str, worker_result: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="ralph-fixture-") as td:
        root = Path(td)
        ticket_path = root / "TASK-9999-fixture.md"
        ticket_path.write_text(ticket_text, encoding="utf-8")
        stop_hook = load_stop_hook_module()
        ticket = stop_hook.load_ticket(ticket_path)
        verdict = stop_hook.run_ralph_judge(ticket, worker_result, {"phase": phase})
        if verdict is None:
            return subprocess.CompletedProcess(
                args=["python3", "bin/ralph_judge.py"],
                returncode=1,
                stdout="",
                stderr="unable to parse worker result",
            )
        return subprocess.CompletedProcess(
            args=["python3", "bin/ralph_judge.py"],
            returncode=0,
            stdout=json.dumps(verdict, indent=2),
            stderr="",
        )


def main() -> int:
    results: list[dict[str, object]] = []
    current_run_path = ROOT / ".ralph" / "state" / "current-run.json"
    hook_log_path = ROOT / ".ralph" / "logs" / "stop-hook.jsonl"
    had_current_run = current_run_path.exists()
    original_current_run = current_run_path.read_text(encoding="utf-8") if had_current_run else None
    had_hook_log = hook_log_path.exists()
    original_hook_log = hook_log_path.read_text(encoding="utf-8") if had_hook_log else None

    with tempfile.TemporaryDirectory(prefix="ralph-hook-fixtures-") as td:
        fixture_root = Path(td)
        hook_missing_ticket = fixture_root / "TASK-9998-hook-missing.md"
        hook_missing_ticket.write_text(
            fixture_ticket(
                ticket_id="TASK-9998",
                title="hook missing evidence fixture",
                acceptance_checked=False,
                evidence_checked=False,
            ),
            encoding="utf-8",
        )
        hook_complete_ticket = fixture_root / "TASK-9997-hook-complete.md"
        hook_complete_ticket.write_text(
            fixture_ticket(
                ticket_id="TASK-9997",
                title="hook complete evidence fixture",
                acceptance_checked=True,
                evidence_checked=True,
            ),
            encoding="utf-8",
        )

        try:
            payload_input = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "cwd": str(ROOT),
                    "last_assistant_message": "RALPH_RESULT: status=build_complete next=building reason=eval_build",
                }
            )
            build = subprocess.run(
                ["python3", "bin/stop_hook.py"],
                cwd=ROOT,
                env={
                    **os.environ,
                    "CODEXTER_RALPH_HOOK": "1",
                    "CODEXTER_HOME": str(Path.home() / ".codex"),
                    "RALPH_TICKET": str(hook_missing_ticket),
                },
                input=payload_input,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "name": "hook_build_payload",
                    "ok": build.returncode == 0,
                    "stdout": build.stdout.strip(),
                    "stderr": build.stderr.strip(),
                }
            )

            # 3. planning payload replay should stop safely (stdout empty) if ticket is in review
            planning_payload = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "cwd": str(ROOT),
                    "last_assistant_message": "RALPH_RESULT: status=plan_ready next=building reason=eval_plan",
                }
            )
            plan_hook = subprocess.run(
                ["python3", "bin/stop_hook.py"],
                cwd=ROOT,
                env={
                    **os.environ,
                    "CODEXTER_RALPH_HOOK": "1",
                    "CODEXTER_HOME": str(Path.home() / ".codex"),
                    "RALPH_TICKET": "tickets/TASK-0003-codexter-evaluator-scorecard.md",
                },
                input=planning_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "name": "hook_plan_payload",
                    "ok": plan_hook.returncode == 0,
                    "stdout": plan_hook.stdout.strip(),
                    "stderr": plan_hook.stderr.strip(),
                }
            )

            # 4. state-first ticket resolution via current-run.json (no env ticket selector)
            current_run_path.parent.mkdir(parents=True, exist_ok=True)
            current_run_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "run_id": "run-task-9998-building-fixture",
                        "ticket_id": "TASK-9998",
                        "ticket_path": str(hook_missing_ticket),
                        "phase": "building",
                        "status": "waiting_for_worker",
                        "prompt_file": "prompts/ralph.md",
                        "updated_at": "2026-04-05T00:00:00Z",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            state_payload = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "cwd": str(ROOT),
                    "last_assistant_message": "RALPH_RESULT: status=build_complete next=building reason=eval_state_selector",
                }
            )
            state_hook = subprocess.run(
                ["python3", "bin/stop_hook.py"],
                cwd=ROOT,
                env={
                    **os.environ,
                    "CODEXTER_RALPH_HOOK": "1",
                    "CODEXTER_HOME": str(Path.home() / ".codex"),
                },
                input=state_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "name": "hook_current_run_selector",
                    "ok": state_hook.returncode == 0,
                    "stdout": state_hook.stdout.strip(),
                    "stderr": state_hook.stderr.strip(),
                }
            )

            # 5. hook replay: Ralph-mode prose without RALPH_RESULT should continue instead of stopping as success
            prose_payload = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "cwd": str(ROOT),
                    "last_assistant_message": "I am doing it now. I still need to update the ticket and end this Ralph pass cleanly.",
                }
            )
            prose_hook = subprocess.run(
                ["python3", "bin/stop_hook.py"],
                cwd=ROOT,
                env={
                    **os.environ,
                    "CODEXTER_RALPH_HOOK": "1",
                    "CODEXTER_HOME": str(Path.home() / ".codex"),
                    "RALPH_TICKET": str(hook_complete_ticket),
                },
                input=prose_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "name": "hook_missing_ralph_result",
                    "ok": prose_hook.returncode == 0,
                    "stdout": prose_hook.stdout.strip(),
                    "stderr": prose_hook.stderr.strip(),
                }
            )

            # 6. judge: blocked worker result
            blocked_case = run_judge_fixture(
                ticket_text=fixture_ticket(ticket_id="TASK-9999", title="blocked fixture", acceptance_checked=False, evidence_checked=False),
                phase="building",
                worker_result="RALPH_RESULT: status=blocked next=none reason=fixture_blocked",
            )
            results.append({"name": "judge_blocked", "ok": blocked_case.returncode == 0, "stdout": blocked_case.stdout.strip(), "stderr": blocked_case.stderr.strip()})

            # 7. judge: continue_ralph
            continue_case = run_judge_fixture(
                ticket_text=fixture_ticket(ticket_id="TASK-9999", title="continue fixture", acceptance_checked=False, evidence_checked=False),
                phase="building",
                worker_result="RALPH_RESULT: status=continue_ralph next=building reason=fixture_continue",
            )
            results.append({"name": "judge_continue_ralph", "ok": continue_case.returncode == 0, "stdout": continue_case.stdout.strip(), "stderr": continue_case.stderr.strip()})

            # 8. judge: build_complete but evidence missing
            build_missing = run_judge_fixture(
                ticket_text=fixture_ticket(ticket_id="TASK-9999", title="missing evidence fixture", acceptance_checked=False, evidence_checked=False),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_build_missing",
            )
            results.append({"name": "judge_build_complete_missing", "ok": build_missing.returncode == 0, "stdout": build_missing.stdout.strip(), "stderr": build_missing.stderr.strip()})

            # 9. judge: build_complete with complete evidence
            build_complete = run_judge_fixture(
                ticket_text=fixture_ticket(ticket_id="TASK-9999", title="complete evidence fixture", acceptance_checked=True, evidence_checked=True),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_build_complete",
            )
            results.append({"name": "judge_build_complete_pass", "ok": build_complete.returncode == 0, "stdout": build_complete.stdout.strip(), "stderr": build_complete.stderr.strip()})

            # 10. judge: plan_ready
            plan_ready = run_judge_fixture(
                ticket_text=fixture_ticket(ticket_id="TASK-9999", title="plan ready fixture", acceptance_checked=False, evidence_checked=False, phase="planning"),
                phase="planning",
                worker_result="RALPH_RESULT: status=plan_ready next=building reason=fixture_plan_ready",
            )
            results.append({"name": "judge_plan_ready", "ok": plan_ready.returncode == 0, "stdout": plan_ready.stdout.strip(), "stderr": plan_ready.stderr.strip()})

            # 11. judge: docs_complete
            docs_complete = run_judge_fixture(
                ticket_text=fixture_ticket(ticket_id="TASK-9999", title="docs complete fixture", acceptance_checked=True, evidence_checked=True, phase="documenting"),
                phase="documenting",
                worker_result="RALPH_RESULT: status=docs_complete next=done reason=fixture_docs_complete",
            )
            results.append({"name": "judge_docs_complete", "ok": docs_complete.returncode == 0, "stdout": docs_complete.stdout.strip(), "stderr": docs_complete.stderr.strip()})

            # 12. stop hook: auto-continue spawns a visible tmux follow-up lane
            session_name = f"codexter-smoke-{os.getpid()}-{time.time_ns()}"
            tmux_session = run(["tmux", "new-session", "-d", "-s", session_name], cwd=ROOT)
            if tmux_session.returncode != 0:
                raise RuntimeError(tmux_session.stderr.strip() or tmux_session.stdout.strip() or "failed to create tmux session")
            try:
                current_run_path.parent.mkdir(parents=True, exist_ok=True)
                current_run_path.write_text(
                    json.dumps(
                        {
                            "schema_version": "1.0",
                            "run_id": "run-task-9998-building-tmux-fixture",
                            "ticket_id": "TASK-9998",
                            "ticket_path": str(hook_missing_ticket),
                            "phase": "building",
                            "status": "waiting_for_worker",
                            "prompt_file": "prompts/ralph.md",
                            "tmux_session": session_name,
                            "auto_continue": True,
                            "updated_at": "2026-04-05T00:00:00Z",
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                followup_payload = json.dumps(
                    {
                        "hook_event_name": "Stop",
                        "cwd": str(ROOT),
                        "last_assistant_message": "RALPH_RESULT: status=build_complete next=building reason=eval_tmux_followup",
                    }
                )
                followup_hook = subprocess.run(
                    ["python3", "bin/stop_hook.py"],
                    cwd=ROOT,
                    env={
                        **os.environ,
                        "CODEXTER_RALPH_HOOK": "1",
                        "CODEXTER_RALPH_TMUX_DRY_RUN": "1",
                        "CODEXTER_HOME": str(Path.home() / ".codex"),
                        "RALPH_TICKET": str(hook_missing_ticket),
                    },
                    input=followup_payload,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                followup_event = next(
                    (
                        item
                        for item in reversed(read_jsonl(hook_log_path))
                        if item.get("event") == "spawn_followup" and item.get("ticket_id") == "TASK-9998"
                    ),
                    None,
                )
                followup = followup_event.get("followup") if isinstance(followup_event, dict) else None
                run_state_payload: dict[str, object] | None = None
                lane_tail = ""
                if isinstance(followup, dict):
                    run_state_value = followup.get("run_state")
                    if isinstance(run_state_value, str) and run_state_value:
                        run_state_payload = wait_for_json(Path(run_state_value))
                        lane_tail = wait_for_lane_tail(Path(run_state_value))
                results.append(
                    {
                        "name": "hook_tmux_followup",
                        "ok": followup_hook.returncode == 0,
                        "stdout": followup_hook.stdout.strip(),
                        "stderr": followup_hook.stderr.strip(),
                        "session_name": session_name,
                        "followup": followup,
                        "run_state_json": run_state_payload,
                        "lane_tail": lane_tail,
                    }
                )
            finally:
                run(["tmux", "kill-session", "-t", session_name], cwd=ROOT)
        finally:
            if had_current_run and original_current_run is not None:
                current_run_path.write_text(original_current_run, encoding="utf-8")
            else:
                current_run_path.unlink(missing_ok=True)
            if had_hook_log and original_hook_log is not None:
                hook_log_path.write_text(original_hook_log, encoding="utf-8")
            else:
                hook_log_path.unlink(missing_ok=True)

    # Semantic assertions
    assert_case(
        results,
        name="hook_build_payload",
        predicate=lambda c: c["ok"] and "rerun TASK-9998 in building" in str(c["stdout"]),
        message="build payload should request same-ticket rerun",
    )
    assert_case(
        results,
        name="hook_plan_payload",
        predicate=lambda c: c["ok"] and str(c["stdout"]) == "",
        message="plan payload should stop safely with no continuation payload",
    )
    assert_case(
        results,
        name="hook_current_run_selector",
        predicate=lambda c: c["ok"] and "rerun TASK-9998 in building" in str(c["stdout"]),
        message="current-run selector should resolve the active ticket",
    )
    assert_case(
        results,
        name="hook_missing_ralph_result",
        predicate=lambda c: c["ok"]
        and "TASK-9997" in str(c["stdout"])
        and (
            "explicit RALPH_RESULT" in str(c["stdout"])
            or "continue_same_ticket" in str(c["stdout"])
            or "Finish the current ticket before stopping" in str(c["stdout"])
        ),
        message="Ralph-mode prose without RALPH_RESULT should force same-ticket continuation instead of stopping as success",
    )
    assert_case(
        results,
        name="judge_blocked",
        predicate=lambda c: c["ok"] and '"decision": "block_ticket"' in str(c["stdout"]),
        message="blocked result should block ticket",
    )
    assert_case(
        results,
        name="judge_continue_ralph",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]),
        message="continue_ralph should repeat ralph",
    )
    assert_case(
        results,
        name="judge_build_complete_missing",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and '"missing_evidence"' in str(c["stdout"]),
        message="build_complete with gaps should repeat and list missing evidence",
    )
    assert_case(
        results,
        name="judge_build_complete_pass",
        predicate=lambda c: c["ok"] and '"decision": "complete_ticket"' in str(c["stdout"]),
        message="build_complete with complete evidence should complete ticket",
    )
    assert_case(
        results,
        name="judge_plan_ready",
        predicate=lambda c: c["ok"] and '"decision": "advance_ticket"' in str(c["stdout"]),
        message="plan_ready should advance ticket",
    )
    assert_case(
        results,
        name="judge_docs_complete",
        predicate=lambda c: c["ok"] and '"decision": "complete_ticket"' in str(c["stdout"]),
        message="docs_complete should complete when no proof gaps remain",
    )
    assert_case(
        results,
        name="hook_tmux_followup",
        predicate=lambda c: c["ok"]
        and isinstance(c.get("followup"), dict)
        and c["followup"].get("tmux_session") == c["session_name"]
        and isinstance(c.get("run_state_json"), dict)
        and c["run_state_json"].get("tmux_session") == c["session_name"]
        and c["run_state_json"].get("auto_continue") is True
        and c["run_state_json"].get("tmux_window")
        and c["run_state_json"].get("tmux_pane")
        and "[impl tmux dry run] followup" in str(c.get("lane_tail", ""))
        and "phase=building" in str(c.get("lane_tail", ""))
        and "TASK-9998-hook-missing.md" in str(c.get("lane_tail", "")),
        message="auto-continue should spawn a visible dry-run tmux follow-up lane and record its location in run state",
    )

    out_path = ROOT / "experiments" / "latest-runs.json"
    out_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
