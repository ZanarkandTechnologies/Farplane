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
CAPTURE_USER_TURN_PATH = ROOT / "bin" / "capture_user_turn.py"


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd or ROOT, env=env, text=True, capture_output=True, check=False)


def load_stop_hook_module():
    bin_dir = str(STOP_HOOK_PATH.parent)
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    spec = importlib.util.spec_from_file_location("farplane_stop_hook_eval", STOP_HOOK_PATH)
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


def load_json(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


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


def fixture_review_packet(
    *,
    overall_verdict: str = "pass",
    rerun_required: bool = False,
    evidence_quality: str = "pass",
    integration_readiness: str = "pass",
    traceability: str = "pass",
    freshness: str = "pass",
    hard_gate_failures: list[str] | None = None,
    blocking_findings: list[str] | None = None,
    next_action: str = "none",
    overall_score: float = 4.5,
    overall_threshold: float = 4.0,
) -> str:
    hard_gate_failures = hard_gate_failures or []
    blocking_findings = blocking_findings or []
    return f"""
## Review Packet
- `reviewed_at:` 2026-04-05 01:00 +0100
- `rubrics_used:` ["evidence-quality", "integration-readiness"]
- `overall_score:` {overall_score}
- `overall_threshold:` {overall_threshold}
- `overall_verdict:` {overall_verdict}
- `rerun_required:` {"true" if rerun_required else "false"}
- `evidence_quality:` {evidence_quality}
- `integration_readiness:` {integration_readiness}
- `traceability:` {traceability}
- `freshness:` {freshness}
- `hard_gate_failures:` {json.dumps(hard_gate_failures)}
- `blocking_findings:` {json.dumps(blocking_findings)}
- `next_action:` {next_action}
"""


def fixture_ticket(
    *,
    ticket_id: str,
    title: str,
    acceptance_checked: bool,
    evidence_checked: bool,
    blockers: list[str] | None = None,
    phase: str = "building",
    review_packet_text: str | None = None,
    updated_at: str = "2026-04-05T00:00:00Z",
) -> str:
    acc = "x" if acceptance_checked else " "
    ev = "x" if evidence_checked else " "
    blocker_lines = ["- none"] if not blockers else [f"- {item}" for item in blockers]
    status = "review" if phase == "planning" else "building"
    if review_packet_text is None and phase != "planning" and acceptance_checked and evidence_checked:
        review_packet_text = fixture_review_packet()
    review_packet_block = f"\n{review_packet_text.strip()}\n" if review_packet_text else "\n"
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
updated_at: {updated_at}
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
{review_packet_block}"""


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


def write_current_run_fixture(
    *,
    current_run_path: Path,
    ticket_path: Path,
    ticket_id: str,
    phase: str,
    run_state_path: Path,
) -> None:
    current_run_path.parent.mkdir(parents=True, exist_ok=True)
    run_state_payload = {
        "schema_version": "1.0",
        "run_id": f"run-{ticket_id.lower()}-{phase}-fixture",
        "ticket_id": ticket_id,
        "ticket_path": str(ticket_path),
        "phase": phase,
        "status": "waiting_for_worker",
        "skill_name": "ralph" if phase != "planning" else "impl-plan",
        "compute_class": "local",
        "parallel_slots_reserved": 1,
        "updated_at": "2026-04-05T00:00:00Z",
    }
    run_state_path.parent.mkdir(parents=True, exist_ok=True)
    run_state_path.write_text(json.dumps(run_state_payload, indent=2) + "\n", encoding="utf-8")
    current_run_path.write_text(
        json.dumps(
            {
                **run_state_payload,
                "run_state": str(run_state_path),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
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
        hook_planning_ticket = fixture_root / "TASK-9996-hook-planning.md"
        hook_planning_ticket.write_text(
            fixture_ticket(
                ticket_id="TASK-9996",
                title="hook planning fixture",
                acceptance_checked=False,
                evidence_checked=False,
                phase="planning",
            ),
            encoding="utf-8",
        )

        try:
            capture_run_state = fixture_root / "run-task-9998-building-capture.json"
            write_current_run_fixture(
                current_run_path=current_run_path,
                ticket_path=hook_missing_ticket,
                ticket_id="TASK-9998",
                phase="building",
                run_state_path=capture_run_state,
            )
            capture_payload = json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "cwd": str(ROOT),
                    "turn_id": "turn-capture-build",
                    "prompt": "Continue working on TASK-9998 with $impl and keep it ticket-local.",
                }
            )
            capture_hook = subprocess.run(
                ["python3", str(CAPTURE_USER_TURN_PATH)],
                cwd=ROOT,
                env={**os.environ, "FARPLANE_HOME": str(Path.home() / ".codex")},
                input=capture_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            captured_current_run = load_json(current_run_path)
            captured_run_state = load_json(capture_run_state)
            results.append(
                {
                    "name": "user_prompt_capture",
                    "ok": capture_hook.returncode == 0,
                    "stdout": capture_hook.stdout.strip(),
                    "stderr": capture_hook.stderr.strip(),
                    "current_run": captured_current_run,
                    "run_state": captured_run_state,
                }
            )

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
                    "FARPLANE_RALPH_HOOK": "1",
                    "FARPLANE_HOME": str(Path.home() / ".codex"),
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

            planning_run_state = fixture_root / "run-task-9996-planning-capture.json"
            write_current_run_fixture(
                current_run_path=current_run_path,
                ticket_path=hook_planning_ticket,
                ticket_id="TASK-9996",
                phase="planning",
                run_state_path=planning_run_state,
            )
            planning_capture_payload = json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "cwd": str(ROOT),
                    "turn_id": "turn-capture-plan",
                    "prompt": "Return to TASK-9996 and produce the ticket plan only.",
                }
            )
            subprocess.run(
                ["python3", str(CAPTURE_USER_TURN_PATH)],
                cwd=ROOT,
                env={**os.environ, "FARPLANE_HOME": str(Path.home() / ".codex")},
                input=planning_capture_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            planning_mismatch_payload = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "cwd": str(ROOT),
                    "last_assistant_message": "RALPH_RESULT: status=build_complete next=building reason=eval_planning_mismatch",
                }
            )
            planning_mismatch = subprocess.run(
                ["python3", "bin/stop_hook.py"],
                cwd=ROOT,
                env={
                    **os.environ,
                    "FARPLANE_RALPH_HOOK": "1",
                    "FARPLANE_HOME": str(Path.home() / ".codex"),
                    "RALPH_TICKET": str(hook_planning_ticket),
                },
                input=planning_mismatch_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "name": "hook_planning_soft_mismatch",
                    "ok": planning_mismatch.returncode == 0,
                    "stdout": planning_mismatch.stdout.strip(),
                    "stderr": planning_mismatch.stderr.strip(),
                }
            )

            mismatch_run_state = fixture_root / "run-task-9998-building-mismatch.json"
            write_current_run_fixture(
                current_run_path=current_run_path,
                ticket_path=hook_missing_ticket,
                ticket_id="TASK-9998",
                phase="building",
                run_state_path=mismatch_run_state,
            )
            mismatch_capture_payload = json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "cwd": str(ROOT),
                    "turn_id": "turn-capture-hard-mismatch",
                    "prompt": "Continue working on TASK-9997 with $impl.",
                }
            )
            subprocess.run(
                ["python3", str(CAPTURE_USER_TURN_PATH)],
                cwd=ROOT,
                env={**os.environ, "FARPLANE_HOME": str(Path.home() / ".codex")},
                input=mismatch_capture_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            hard_mismatch_payload = json.dumps(
                {
                    "hook_event_name": "Stop",
                    "cwd": str(ROOT),
                    "last_assistant_message": "RALPH_RESULT: status=build_complete next=building reason=eval_hard_mismatch",
                }
            )
            hard_mismatch = subprocess.run(
                ["python3", "bin/stop_hook.py"],
                cwd=ROOT,
                env={
                    **os.environ,
                    "FARPLANE_RALPH_HOOK": "1",
                    "FARPLANE_HOME": str(Path.home() / ".codex"),
                    "RALPH_TICKET": str(hook_missing_ticket),
                },
                input=hard_mismatch_payload,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "name": "hook_explicit_ticket_hard_mismatch",
                    "ok": hard_mismatch.returncode == 0,
                    "stdout": hard_mismatch.stdout.strip(),
                    "stderr": hard_mismatch.stderr.strip(),
                }
            )

            # 3. planning payload replay should advance the same planning
            # fixture into building. Reset the runtime fixture first so the
            # case does not inherit hard-mismatch `last_user_turn` state from
            # the prior explicit-ticket mismatch scenario.
            plan_replay_run_state = fixture_root / "run-task-9996-plan-replay.json"
            write_current_run_fixture(
                current_run_path=current_run_path,
                ticket_path=hook_planning_ticket,
                ticket_id="TASK-9996",
                phase="planning",
                run_state_path=plan_replay_run_state,
            )
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
                    "FARPLANE_RALPH_HOOK": "1",
                    "FARPLANE_HOME": str(Path.home() / ".codex"),
                    "RALPH_TICKET": str(hook_planning_ticket),
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
                    "FARPLANE_RALPH_HOOK": "1",
                    "FARPLANE_HOME": str(Path.home() / ".codex"),
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
                    "FARPLANE_RALPH_HOOK": "1",
                    "FARPLANE_HOME": str(Path.home() / ".codex"),
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

            malformed_packet = run_judge_fixture(
                ticket_text=fixture_ticket(
                    ticket_id="TASK-9999",
                    title="malformed packet fixture",
                    acceptance_checked=True,
                    evidence_checked=True,
                    review_packet_text="""
## Review Packet
- `reviewed_at:` 2026-04-05 00:00 +0100
- `overall_verdict:` pass
- `rerun_required:` maybe
""",
                ),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_packet_malformed",
            )
            results.append({"name": "judge_build_complete_malformed_packet", "ok": malformed_packet.returncode == 0, "stdout": malformed_packet.stdout.strip(), "stderr": malformed_packet.stderr.strip()})

            stale_packet = run_judge_fixture(
                ticket_text=fixture_ticket(
                    ticket_id="TASK-9999",
                    title="stale packet fixture",
                    acceptance_checked=True,
                    evidence_checked=True,
                    review_packet_text=fixture_review_packet(freshness="fail", hard_gate_failures=["freshness"]),
                ),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_packet_stale",
            )
            results.append({"name": "judge_build_complete_stale_packet", "ok": stale_packet.returncode == 0, "stdout": stale_packet.stdout.strip(), "stderr": stale_packet.stderr.strip()})

            contradictory_packet = run_judge_fixture(
                ticket_text=fixture_ticket(
                    ticket_id="TASK-9999",
                    title="contradictory packet fixture",
                    acceptance_checked=True,
                    evidence_checked=True,
                    review_packet_text=fixture_review_packet(
                        overall_verdict="revise",
                        rerun_required=True,
                        evidence_quality="fail",
                        integration_readiness="fail",
                        hard_gate_failures=["evidence-quality", "integration-readiness"],
                        blocking_findings=["empty state proof missing"],
                        next_action="capture empty-state proof and rerun review",
                    ),
                ),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_packet_contradictory",
            )
            results.append({"name": "judge_build_complete_contradictory_packet", "ok": contradictory_packet.returncode == 0, "stdout": contradictory_packet.stdout.strip(), "stderr": contradictory_packet.stderr.strip()})

            low_traceability_packet = run_judge_fixture(
                ticket_text=fixture_ticket(
                    ticket_id="TASK-9999",
                    title="traceability packet fixture",
                    acceptance_checked=True,
                    evidence_checked=True,
                    review_packet_text=fixture_review_packet(traceability="fail", hard_gate_failures=["traceability"]),
                ),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_packet_traceability",
            )
            results.append({"name": "judge_build_complete_low_traceability_packet", "ok": low_traceability_packet.returncode == 0, "stdout": low_traceability_packet.stdout.strip(), "stderr": low_traceability_packet.stderr.strip()})

            stale_timestamp_packet = run_judge_fixture(
                ticket_text=fixture_ticket(
                    ticket_id="TASK-9999",
                    title="stale timestamp packet fixture",
                    acceptance_checked=True,
                    evidence_checked=True,
                    updated_at="2026-04-05T01:30:00Z",
                    review_packet_text=fixture_review_packet(freshness="pass"),
                ),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_packet_timestamp_stale",
            )
            results.append({"name": "judge_build_complete_stale_timestamp_packet", "ok": stale_timestamp_packet.returncode == 0, "stdout": stale_timestamp_packet.stdout.strip(), "stderr": stale_timestamp_packet.stderr.strip()})

            valid_packet_checkbox_gap = run_judge_fixture(
                ticket_text=fixture_ticket(
                    ticket_id="TASK-9999",
                    title="valid packet checkbox gap fixture",
                    acceptance_checked=False,
                    evidence_checked=False,
                    review_packet_text=fixture_review_packet(),
                ),
                phase="building",
                worker_result="RALPH_RESULT: status=build_complete next=building reason=fixture_packet_checkbox_gap",
            )
            results.append({"name": "judge_build_complete_valid_packet_checkbox_gap", "ok": valid_packet_checkbox_gap.returncode == 0, "stdout": valid_packet_checkbox_gap.stdout.strip(), "stderr": valid_packet_checkbox_gap.stderr.strip()})

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
            session_name = f"farplane-smoke-{os.getpid()}-{time.time_ns()}"
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
                        "FARPLANE_RALPH_HOOK": "1",
                        "FARPLANE_RALPH_TMUX_DRY_RUN": "1",
                        "FARPLANE_HOME": str(Path.home() / ".codex"),
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
        name="user_prompt_capture",
        predicate=lambda c: c["ok"]
        and isinstance(c.get("current_run"), dict)
        and isinstance(c["current_run"].get("last_user_turn"), dict)
        and c["current_run"]["last_user_turn"].get("turn_id") == "turn-capture-build"
        and c["current_run"]["last_user_turn"].get("intent_mode") == "building"
        and c["current_run"]["last_user_turn"].get("requested_outcome") == "code_change"
        and c["current_run"]["last_user_turn"].get("explicit_ticket_id") == "TASK-9998"
        and "ticket_local_only" in c["current_run"]["last_user_turn"].get("hard_constraints", [])
        and isinstance(c.get("run_state"), dict)
        and isinstance(c["run_state"].get("last_user_turn"), dict)
        and c["run_state"]["last_user_turn"].get("turn_id") == "turn-capture-build",
        message="UserPromptSubmit should persist the current-turn intent into both current-run and run-state files",
    )
    assert_case(
        results,
        name="hook_build_payload",
        predicate=lambda c: c["ok"] and "rerun TASK-9998 in building" in str(c["stdout"]),
        message="build payload should request same-ticket rerun",
    )
    assert_case(
        results,
        name="hook_planning_soft_mismatch",
        predicate=lambda c: c["ok"]
        and '"decision": "block"' in str(c["stdout"])
        and "requested `planning` work" in str(c["stdout"]),
        message="planning-vs-building relevance mismatch should force same-ticket corrective continuation before normal continuation checks",
    )
    assert_case(
        results,
        name="hook_explicit_ticket_hard_mismatch",
        predicate=lambda c: c["ok"]
        and '"continue": false' in str(c["stdout"])
        and "targets TASK-9997" in str(c["stdout"]),
        message="explicit ticket mismatch should stop immediately instead of entering the continuation gate",
    )
    assert_case(
        results,
        name="hook_plan_payload",
        predicate=lambda c: c["ok"]
        and '"decision": "block"' in str(c["stdout"])
        and "advance TASK-9996 to building" in str(c["stdout"]),
        message="plan payload should emit the planning-to-building continuation payload",
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
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and '"review_gate_failures"' in str(c["stdout"]),
        message="build_complete with missing review packet should repeat and list review gate failures",
    )
    assert_case(
        results,
        name="judge_build_complete_pass",
        predicate=lambda c: c["ok"] and '"decision": "complete_ticket"' in str(c["stdout"]),
        message="build_complete with complete evidence should complete ticket",
    )
    assert_case(
        results,
        name="judge_build_complete_malformed_packet",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and "review packet is malformed" in str(c["stdout"]),
        message="malformed review packet should repeat ralph",
    )
    assert_case(
        results,
        name="judge_build_complete_stale_packet",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and "hard_gate_failure=freshness" in str(c["stdout"]),
        message="stale packet should repeat ralph",
    )
    assert_case(
        results,
        name="judge_build_complete_contradictory_packet",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and "blocking_finding=empty state proof missing" in str(c["stdout"]),
        message="contradictory packet should repeat ralph and surface the blocking finding",
    )
    assert_case(
        results,
        name="judge_build_complete_low_traceability_packet",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and "hard_gate_failure=traceability" in str(c["stdout"]),
        message="low-traceability packet should repeat ralph",
    )
    assert_case(
        results,
        name="judge_build_complete_stale_timestamp_packet",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and "reviewed_at=stale" in str(c["stdout"]),
        message="stale reviewed_at timestamp should repeat ralph even when freshness says pass",
    )
    assert_case(
        results,
        name="judge_build_complete_valid_packet_checkbox_gap",
        predicate=lambda c: c["ok"] and '"decision": "repeat_ralph"' in str(c["stdout"]) and '"missing_evidence"' in str(c["stdout"]),
        message="valid packet with unchecked acceptance/evidence boxes should still repeat and list missing evidence",
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
