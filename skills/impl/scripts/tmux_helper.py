#!/usr/bin/env python3
"""
IMPL TMUX HELPER
================
Purpose

Launch and inspect visible tmux-backed Codex lanes for the `impl` skill.

This helper owns tmux/session plumbing only. Orchestration policy lives in the
`impl` skill and Stop-hook logic, not here.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


BIN_DIR = Path(__file__).resolve().parents[3] / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

from user_turn import build_runtime_claim, capture_user_turn, current_session_id, session_state_path


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def root() -> Path:
    return Path(__file__).resolve().parents[3]


def current_run_state_path() -> Path:
    return root() / ".farplane" / "state" / "current-run.json"


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd or root(),
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def ensure_tmux() -> None:
    result = run(["tmux", "-V"])
    if result.returncode != 0:
        raise SystemExit("tmux is not available")


def current_tmux_session() -> str:
    result = run(["tmux", "display-message", "-p", "#S"])
    if result.returncode != 0 or not result.stdout.strip():
        raise SystemExit("not inside a tmux session")
    return result.stdout.strip()


def ticket_id_from_path(path: Path) -> str:
    for candidate in (path.parent.name, path.name, path.stem):
        match = re.search(r"(TASK-\d{4}|TKT-[0-9A-Za-z-]+)", candidate)
        if match:
            return match.group(1)
    raise ValueError(f"could not determine ticket id from {path}")


def default_run_state_path(ticket_id: str, phase: str) -> Path:
    return root() / ".farplane" / "runs" / f"{ticket_id.lower()}-{phase}-{now_stamp()}.json"


def path_stem(ticket_id: str, phase: str) -> str:
    return f"run-{ticket_id.lower()}-{phase}-{now_stamp()}"


def read_json(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_iso_timestamp(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    normalized = raw.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def stale_budget_secs() -> int:
    raw = str(os.environ.get("FARPLANE_WORKER_STALE_BUDGET_SECS", "")).strip()
    if not raw:
        return 60
    try:
        parsed = int(float(raw))
    except ValueError:
        return 60
    return max(parsed, 1)


def annotate_backpressure(payload: dict[str, object], *, now: datetime | None = None) -> dict[str, object]:
    enriched = dict(payload)
    status = str(payload.get("status") or "").strip()
    pane_dead = str(payload.get("pane_dead") or "").strip()
    if status not in {"running", "waiting_for_worker"} or pane_dead == "1":
        enriched["backpressure_state"] = "inactive"
        return enriched

    budget = stale_budget_secs()
    reference_timestamp = parse_iso_timestamp(payload.get("last_checkpoint_at"))
    basis = "last_checkpoint_at"
    if reference_timestamp is None:
        reference_timestamp = parse_iso_timestamp(payload.get("worker_started_at"))
        basis = "worker_started_at"
    if reference_timestamp is None:
        enriched["backpressure_state"] = "unknown"
        enriched["backpressure_budget_secs"] = budget
        return enriched

    current_time = now or datetime.now(timezone.utc)
    stale_for_secs = max(int((current_time - reference_timestamp).total_seconds()), 0)
    enriched["backpressure_budget_secs"] = budget
    enriched["stale_for_secs"] = stale_for_secs
    enriched["backpressure_basis"] = basis
    if stale_for_secs > budget:
        enriched["backpressure_state"] = "over_budget"
        enriched["recommended_action"] = (
            "split work, add instrumentation, narrow scope, or continue with explicit justification"
        )
    else:
        enriched["backpressure_state"] = "within_budget"
    return enriched


def skill_name_for_phase(phase: str, execution_phase: str = "") -> str:
    if phase == "building" and execution_phase in {"impl", "qa", "demo"}:
        return execution_phase
    mapping = {
        "planning": "impl-plan",
        "building": "impl",
        "documenting": "close-ticket",
    }
    return mapping[phase]


def required_worker_names(phase: str, execution_phase: str = "") -> list[str]:
    if phase == "building" and execution_phase == "qa":
        return ["qa"]
    if phase == "building" and execution_phase == "demo":
        return ["demo"]
    if phase == "building":
        return ["builder", "reviewer", "qa"]
    return [default_worker_name(phase, execution_phase)]


def default_worker_name(phase: str, execution_phase: str = "") -> str:
    if phase == "building" and execution_phase in {"qa", "demo"}:
        return execution_phase
    mapping = {
        "planning": "planner",
        "building": "builder",
        "documenting": "close-ticket",
    }
    return mapping[phase]


def default_main_artifact_path(ticket: Path, phase: str, worker_name: str, execution_phase: str = "") -> str:
    ticket_id = ticket_id_from_path(ticket)
    effective_phase = execution_phase or worker_name
    if phase == "building" and effective_phase == "qa":
        return str(root() / "tickets" / ticket_id / "artifacts" / "qa")
    if phase == "building" and effective_phase == "demo":
        return str(root() / "tickets" / ticket_id / "artifacts" / "demo")
    if phase == "building" and worker_name == "reviewer":
        return str(root() / "tickets" / ticket_id / "artifacts")
    return str(ticket)


def lane_directive(phase: str, worker_name: str, execution_phase: str = "") -> str:
    if phase != "building":
        return ""
    if execution_phase == "qa" or worker_name == "qa":
        return (
            "You are the independent QA lane. Capture proof under `tickets/TASK-XXXX/artifacts/qa/`. "
            "For any UI or user-visible run, always hand the captured artifacts to a separate `visual-qa` judgment pass, "
            "write `result.json`, and finish with `IMPL_RESULT: status=qa_complete next=building reason=...`.\n"
        )
    if execution_phase == "demo" or worker_name == "demo":
        return (
            "You are the demo lane. Reuse passing QA artifacts to produce demo-ready outputs under "
            "`tickets/TASK-XXXX/artifacts/demo/`, write `result.json`, and finish with "
            "`IMPL_RESULT: status=demo_complete next=building reason=...`.\n"
        )
    if worker_name == "builder":
        return (
            "You are the implementation lane. Before claiming `build_complete` or `done`, "
            "spawn independent reviewer and QA subagents or lanes and integrate their outputs. "
            "Do not self-approve implementation quality or user-visible proof.\n"
        )
    if worker_name == "reviewer":
        return (
            "You are the independent reviewer lane. Run the `review` skill against the active ticket path, "
            "start from the ticket `Done / Proof` reviewer handoff, use its caller-declared rubric families, "
            "required TAS gates, hard gates, linked evidence artifacts, and changed-file context, and return a skeptical verdict grounded in the current repo state. "
            "If Stop hook requests visible completion review with a nonce, write "
            "`tickets/TASK-XXXX/artifacts/review/<timestamp>-completion-receipt.json`, link it from the ticket `Links` or `State` section, "
            "and finish with `IMPL_RESULT: status=done next=building reason=completion review receipt written`.\n"
        )
    return ""


def build_phase_prompt(
    ticket: Path,
    phase: str,
    worker_name: str,
    main_artifact_path: str,
    execution_phase: str = "",
    followup_reason: str | None = None,
) -> str:
    skill_name = skill_name_for_phase(phase, execution_phase)
    ticket_id = ticket_id_from_path(ticket)
    base = (
        f"Run the `{skill_name}` skill on ticket `{ticket_id}`.\n"
        f"You are the `{worker_name}` lane.\n"
        f"Your main artifact is `{main_artifact_path}`.\n"
        f"Execution phase: `{execution_phase or 'impl'}`.\n"
        f"Required lanes for this phase: {', '.join(required_worker_names(phase, execution_phase))}.\n"
        f"{lane_directive(phase, worker_name, execution_phase)}"
        "Before substantive work, read that artifact and begin your first response with one line in the exact form "
        "`GROUNDING_SUMMARY: <one-sentence summary>`. Keep the summary specific to the artifact and the lane's role.\n"
        "Resolve the ticket from active run state or the explicit ticket selector, stay within that ticket's scope, "
        "write back to the ticket itself, and finish with one `IMPL_RESULT:` line.\n"
    )
    if not followup_reason:
        return base
    return (
        "Continue the current Codex lane.\n\n"
        f"Follow-up reason: {followup_reason.strip()}\n\n"
        + base
    )


def write_current_run(payload: dict[str, object], run_state: Path) -> None:
    current_payload = {
        "schema_version": "1.0",
        "run_id": payload["run_id"],
        "ticket_id": payload["ticket_id"],
        "ticket_path": payload["ticket_path"],
        "phase": payload["phase"],
        "status": payload["status"],
        "skill_name": payload["skill_name"],
        "compute_class": payload["compute_class"],
        "updated_at": payload["updated_at"],
        "run_state": str(run_state),
    }
    for key in (
        "session_id",
        "next_phase",
        "last_judge_verdict",
        "last_hook_decision",
        "last_hook_summary",
        "last_hook_timestamp",
        "last_user_turn",
        "last_intent_alignment",
        "last_intent_alignment_reason",
        "last_intent_turn_id",
        "worker_name",
        "lane_role",
        "execution_phase",
        "requires_qa",
        "requires_demo",
        "phase_requirements",
        "required_worker_names",
        "main_artifact_path",
        "grounding_summary",
        "worker_started_at",
        "last_checkpoint_at",
        "checkpoint_summary",
        "tmux_session",
        "tmux_window",
        "tmux_pane",
        "auto_continue",
        "impl_loop_active",
    ):
        if key in payload:
            current_payload[key] = payload[key]
    claim = build_runtime_claim(payload)
    if claim is not None:
        current_payload["claim"] = claim
    write_json(current_run_state_path(), current_payload)
    session_id = current_session_id(payload)
    if session_id:
        write_json(session_state_path(root(), session_id), current_payload)


def build_run_state(
    ticket: Path,
    phase: str,
    compute_class: str,
    worker_name: str,
    main_artifact_path: str,
    execution_phase: str,
    existing: dict[str, object] | None = None,
) -> dict[str, object]:
    ticket_id = ticket_id_from_path(ticket)
    attempt = 1
    if existing:
        raw_attempt = existing.get("attempt")
        if isinstance(raw_attempt, int) and raw_attempt >= 1:
            attempt = raw_attempt + 1
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "run_id": path_stem(ticket_id, phase),
        "ticket_id": ticket_id,
        "ticket_path": str(ticket),
        "phase": phase,
        "status": "running",
        "attempt": attempt,
        "skill_name": skill_name_for_phase(phase, execution_phase),
        "execution_phase": execution_phase or "impl",
        "compute_class": compute_class,
        "worker_name": worker_name,
        "lane_role": worker_name,
        "required_worker_names": required_worker_names(phase, execution_phase),
        "main_artifact_path": main_artifact_path,
        "worker_started_at": now_iso(),
        "last_checkpoint_at": now_iso(),
        "checkpoint_summary": "worker launched",
        "parallel_slots_reserved": 1,
        "updated_at": now_iso(),
    }
    payload["impl_loop_active"] = phase == "building"
    if existing:
        for key in (
            "executor_target",
            "session_id",
            "last_hook_decision",
            "last_hook_summary",
            "last_hook_timestamp",
            "last_user_turn",
            "last_intent_alignment",
            "last_intent_alignment_reason",
            "last_intent_turn_id",
            "grounding_summary",
            "required_worker_names",
            "requires_qa",
            "requires_demo",
            "phase_requirements",
        ):
            value = existing.get(key)
            if isinstance(value, str) and value:
                payload[key] = value
            elif key == "last_user_turn" and isinstance(value, dict) and value:
                payload[key] = value
    return payload


def capture_user_turn_fallback(prompt_text: str) -> None:
    capture_user_turn(
        project_root=root(),
        raw_text=prompt_text,
        turn_id=None,
        source="tmux_helper_fallback",
        only_if_missing=True,
    )


def lane_thread_name(ticket_id: str) -> str:
    return f"impl-{ticket_id.lower()}"


def lane_shell_command(
    ticket: Path,
    run_state: Path,
    ticket_id: str,
    phase: str,
    executor_target: str | None,
    prompt_text: str,
    resume_session_id: str | None,
    dry_run: bool,
) -> str:
    if dry_run:
        return (
            f"cd {shlex.quote(str(root()))} && "
            f"printf '[impl tmux dry run] phase=%s ticket=%s\\n' "
            f"{shlex.quote(phase)} {shlex.quote(ticket_id)}"
        )

    exports = [
        f"export FARPLANE_ACTIVE_TICKET={shlex.quote(str(ticket))}",
        f"export IMPL_RUN_STATE={shlex.quote(str(run_state))}",
    ]
    if executor_target:
        exports.append(f"export FARPLANE_EXECUTOR_TARGET={shlex.quote(executor_target)}")
    args = [
        "codex",
        "--no-alt-screen",
        "-C",
        str(root()),
        "-c",
        f'thread_name="{lane_thread_name(ticket_id)}"',
    ]
    if resume_session_id:
        args.extend(["resume", resume_session_id, prompt_text])
    else:
        args.append(prompt_text)
    quoted = " ".join(shlex.quote(part) for part in args)
    return (
        f"cd {shlex.quote(str(root()))} && "
        + " && ".join(exports)
        + f" && {quoted}"
    )


def create_tmux_surface(session: str, layout: str, name: str) -> tuple[str, str, str, str]:
    if layout == "window":
        create = run(
            [
                "tmux",
                "new-window",
                "-d",
                "-P",
                "-F",
                "#{session_name}\t#{window_id}\t#{window_index}\t#{pane_id}",
                "-t",
                session,
                "-n",
                name,
            ]
        )
    else:
        create = run(
            [
                "tmux",
                "split-window",
                "-d",
                "-P",
                "-F",
                "#{session_name}\t#{window_id}\t#{window_index}\t#{pane_id}",
                "-t",
                session,
            ]
        )
    if create.returncode != 0:
        raise SystemExit(create.stderr.strip() or create.stdout.strip() or "tmux launch failed")
    session_name, window_id, window_index, pane_id = create.stdout.strip().split("\t")
    run(["tmux", "set-window-option", "-t", window_id, "remain-on-exit", "on"])
    return session_name, window_id, window_index, pane_id


def resolve_existing_path(raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return (root() / candidate).resolve()


def relpath_for_display(raw: str) -> str:
    try:
        return str(Path(raw).resolve().relative_to(root()))
    except ValueError:
        return raw


def compact_ticket_label(raw_ticket: str, fallback_path: str = "") -> str:
    candidates: list[str] = []
    if raw_ticket:
        ticket_path = Path(raw_ticket)
        candidates.extend([ticket_path.parent.name, ticket_path.name, ticket_path.stem])
    elif fallback_path:
        fallback = Path(fallback_path)
        candidates.extend([fallback.parent.name, fallback.name, fallback.stem])
    for raw_name in candidates:
        match = re.search(r"(TASK-\d{4}|TKT-[0-9A-Za-z-]+)", raw_name)
        if match:
            return match.group(1)
    return candidates[1] if len(candidates) > 1 else fallback_path or "ticket"


def format_followup_success(payload: dict[str, object]) -> str:
    ticket_label = compact_ticket_label(str(payload.get("ticket") or ""), str(payload.get("run_state") or ""))
    phase = str(payload.get("phase") or "building")
    parts = [f"followup ok: {ticket_label} -> {phase}"]
    pane = str(payload.get("tmux_pane") or "").strip()
    session = str(payload.get("tmux_session") or "").strip()
    run_state = str(payload.get("run_state") or "").strip()
    if pane:
        parts.append(f"pane={pane}")
    if session:
        parts.append(f"session={session}")
    if run_state:
        parts.append(f"run={relpath_for_display(run_state)}")
    if bool(payload.get("dry_run")):
        parts.append("dry-run")
    return " ".join(parts)


def print_followup_failure(
    ticket_id: str,
    phase: str,
    detail: str,
    *,
    pane_id: str | None = None,
    stderr: str | None = None,
) -> int:
    line = f"followup failed: {ticket_id} -> {phase} | {detail}"
    if pane_id:
        line += f" | pane={pane_id}"
    print(line, file=sys.stderr)
    extra = (stderr or "").strip()
    if extra:
        print(extra, file=sys.stderr)
    return 1


def pane_metadata(pane: str) -> dict[str, str] | None:
    result = run(
        [
            "tmux",
            "display-message",
            "-p",
            "-t",
            pane,
            "#{session_name}\t#{window_id}\t#{window_index}\t#{pane_id}\t#{pane_dead}\t#{pane_current_command}",
        ]
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    session_name, window_id, window_index, pane_id, pane_dead, current_command = result.stdout.strip().split("\t")
    return {
        "tmux_session": session_name,
        "tmux_window": window_id,
        "tmux_window_index": window_index,
        "tmux_pane": pane_id,
        "pane_dead": pane_dead,
        "pane_current_command": current_command,
    }


def summarize_hook_entry(ticket_id: str, entry: dict[str, object]) -> dict[str, str] | None:
    timestamp = entry.get("timestamp")
    if not isinstance(timestamp, str) or not timestamp:
        return None
    decision = entry.get("decision")
    if isinstance(decision, str) and decision:
        next_phase = entry.get("next_phase")
        reason = entry.get("reason")
        next_value = next_phase if isinstance(next_phase, str) and next_phase else "none"
        reason_value = reason if isinstance(reason, str) and reason else "no reason recorded"
        if decision in {"repeat_impl", "repeat_impl_plan"}:
            summary = f"Impl repeat: {ticket_id} -> {next_value} ({reason_value})"
        elif decision == "advance_ticket":
            summary = f"Impl advance: {ticket_id} -> {next_value} ({reason_value})"
        elif decision == "complete_ticket":
            summary = f"Impl complete: {ticket_id} ({reason_value})"
        elif decision == "block_ticket":
            summary = f"Impl blocked: {ticket_id} ({reason_value})"
        else:
            summary = f"Hook {decision}: {ticket_id} ({reason_value})"
        return {
            "last_hook_decision": decision,
            "last_hook_summary": summary,
            "last_hook_timestamp": timestamp,
            "hook_status_source": "stop-hook-log",
        }
    outcome = entry.get("outcome")
    if isinstance(outcome, str) and outcome == "missing_impl_result":
        phase = entry.get("phase")
        phase_value = phase if isinstance(phase, str) and phase else "building"
        return {
            "last_hook_decision": outcome,
            "last_hook_summary": f"Impl missing result: {ticket_id} in {phase_value}",
            "last_hook_timestamp": timestamp,
            "hook_status_source": "stop-hook-log",
        }
    return None


def latest_hook_status(ticket_id: str) -> dict[str, str] | None:
    log_path = root() / ".farplane" / "logs" / "stop-hook.jsonl"
    try:
        lines = log_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(entry, dict):
            continue
        if entry.get("ticket_id") != ticket_id:
            continue
        summarized = summarize_hook_entry(ticket_id, entry)
        if summarized is not None:
            return summarized
    return None


def resolve_run_state_path(raw: str | None, ticket_id: str, phase: str) -> Path:
    if raw:
        return resolve_existing_path(raw)
    current_run = read_json(current_run_state_path())
    current_ticket_id = current_run.get("ticket_id")
    existing = current_run.get("run_state")
    if (
        isinstance(existing, str)
        and existing
        and isinstance(current_ticket_id, str)
        and current_ticket_id == ticket_id
    ):
        return resolve_existing_path(existing)
    return default_run_state_path(ticket_id, phase)


def existing_state_for_path(run_state: Path, ticket_id: str) -> dict[str, object]:
    payload = read_json(run_state)
    if payload:
        return payload
    current_run = read_json(current_run_state_path())
    if current_run.get("ticket_id") == ticket_id:
        return current_run
    return {}


def persist_lane_state(
    *,
    ticket: Path,
    phase: str,
    run_state: Path,
    compute_class: str,
    worker_name: str,
    main_artifact_path: str,
    execution_phase: str,
    tmux_session: str,
    tmux_window: str,
    tmux_pane: str,
    auto_continue: bool,
    existing: dict[str, object] | None,
) -> dict[str, object]:
    state = build_run_state(ticket, phase, compute_class, worker_name, main_artifact_path, execution_phase, existing)
    state["tmux_session"] = tmux_session
    state["tmux_window"] = tmux_window
    state["tmux_pane"] = tmux_pane
    if auto_continue:
        state["auto_continue"] = True
    claim = build_runtime_claim(state)
    if claim is not None:
        state["claim"] = claim
    write_json(run_state, state)
    write_current_run(state, run_state)
    return state


def launch(args: argparse.Namespace) -> int:
    ensure_tmux()
    ticket = resolve_existing_path(args.ticket)
    if not ticket.is_file():
        raise SystemExit(f"ticket not found: {ticket}")
    ticket_id = ticket_id_from_path(ticket)
    execution_phase = args.execution_phase or ("impl" if args.phase == "building" else "")
    worker_name = args.worker_name or default_worker_name(args.phase, execution_phase)
    main_artifact_path = default_main_artifact_path(ticket, args.phase, worker_name, execution_phase)
    run_state = resolve_run_state_path(args.run_state, ticket_id, args.phase)
    session = args.tmux_session or current_tmux_session()
    session_name, window_id, window_index, pane_id = create_tmux_surface(
        session,
        args.layout,
        args.name or f"impl-{ticket_id.lower()}",
    )
    state = persist_lane_state(
        ticket=ticket,
        phase=args.phase,
        run_state=run_state,
        compute_class=args.compute_class,
        worker_name=worker_name,
        main_artifact_path=main_artifact_path,
        execution_phase=execution_phase,
        tmux_session=session_name,
        tmux_window=window_id,
        tmux_pane=pane_id,
        auto_continue=args.auto_continue,
        existing=None,
    )
    prompt_text = build_phase_prompt(ticket, args.phase, worker_name, main_artifact_path, execution_phase)
    command = lane_shell_command(
        ticket,
        run_state,
        ticket_id,
        args.phase,
        None,
        prompt_text,
        None,
        args.dry_run,
    )
    capture_user_turn_fallback(prompt_text)
    sent = run(["tmux", "send-keys", "-t", pane_id, command, "C-m"])
    if sent.returncode != 0:
        raise SystemExit(sent.stderr.strip() or sent.stdout.strip() or "tmux send-keys failed")
    payload = {
        "action": "launch",
        "ticket": str(ticket),
        "phase": args.phase,
        "execution_phase": execution_phase,
        "worker_name": worker_name,
        "main_artifact_path": main_artifact_path,
        "tmux_session": session_name,
        "tmux_window": window_id,
        "tmux_window_index": window_index,
        "tmux_pane": pane_id,
        "run_state": str(run_state),
        "auto_continue": args.auto_continue,
        "dry_run": args.dry_run,
        "interactive_lane": not args.dry_run,
    }
    session_id = state.get("session_id")
    if isinstance(session_id, str) and session_id:
        payload["session_id"] = session_id
    print(json.dumps(payload, indent=2))
    return 0


def followup(args: argparse.Namespace) -> int:
    ensure_tmux()
    ticket = resolve_existing_path(args.ticket)
    if not ticket.is_file():
        ticket_label = compact_ticket_label(args.ticket, str(ticket))
        return print_followup_failure(ticket_label, args.phase, "ticket not found", stderr=str(ticket))
    ticket_id = ticket_id_from_path(ticket)
    run_state = resolve_run_state_path(args.run_state, ticket_id, args.phase)
    existing = existing_state_for_path(run_state, ticket_id)
    current_run = read_json(current_run_state_path())
    if current_run.get("ticket_id") == ticket_id:
        existing = {**existing, **current_run}
    compute_class = args.compute_class or str(existing.get("compute_class") or "local")
    auto_continue = bool(existing.get("auto_continue")) or args.auto_continue
    execution_phase = str(args.execution_phase or existing.get("execution_phase") or ("impl" if args.phase == "building" else "")).strip()
    worker_name = args.worker_name or str(existing.get("worker_name") or default_worker_name(args.phase, execution_phase))
    main_artifact_path = str(existing.get("main_artifact_path") or default_main_artifact_path(ticket, args.phase, worker_name, execution_phase))
    prompt_text = build_phase_prompt(ticket, args.phase, worker_name, main_artifact_path, execution_phase, args.reason)
    capture_user_turn_fallback(prompt_text)

    if args.dry_run:
        try:
            session = args.tmux_session or str(existing.get("tmux_session") or current_tmux_session())
        except SystemExit as exc:
            return print_followup_failure(ticket_id, args.phase, "resolve tmux session failed", stderr=str(exc))
        try:
            session_name, window_id, window_index, pane_id = create_tmux_surface(
                session,
                "pane",
                f"impl-{ticket_id.lower()}",
            )
        except SystemExit as exc:
            return print_followup_failure(ticket_id, args.phase, "tmux launch failed", stderr=str(exc))
        state = persist_lane_state(
            ticket=ticket,
            phase=args.phase,
            run_state=run_state,
            compute_class=compute_class,
            worker_name=worker_name,
            main_artifact_path=main_artifact_path,
            execution_phase=execution_phase,
            tmux_session=session_name,
            tmux_window=window_id,
            tmux_pane=pane_id,
            auto_continue=auto_continue,
            existing=existing,
        )
        message = (
            f"cd {shlex.quote(str(root()))} && "
            f"printf '[impl tmux dry run] followup phase=%s ticket=%s\\n' "
            f"{shlex.quote(args.phase)} {shlex.quote(ticket_id)}"
        )
        sent = run(["tmux", "send-keys", "-t", pane_id, message, "C-m"])
        if sent.returncode != 0:
            return print_followup_failure(
                ticket_id,
                args.phase,
                "tmux send-keys failed",
                pane_id=pane_id,
                stderr=sent.stderr.strip() or sent.stdout.strip(),
            )
        payload = {
            "action": "followup",
            "ticket": str(ticket),
            "phase": args.phase,
            "execution_phase": execution_phase,
            "worker_name": worker_name,
            "main_artifact_path": main_artifact_path,
            "tmux_session": session_name,
            "tmux_window": window_id,
            "tmux_window_index": window_index,
            "tmux_pane": pane_id,
            "run_state": str(run_state),
            "dry_run": True,
            "reused_existing_pane": False,
        }
        session_id = state.get("session_id")
        if isinstance(session_id, str) and session_id:
            payload["session_id"] = session_id
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(format_followup_success(payload))
        return 0

    try:
        session = args.tmux_session or str(existing.get("tmux_session") or current_tmux_session())
    except SystemExit as exc:
        return print_followup_failure(ticket_id, args.phase, "resolve tmux session failed", stderr=str(exc))
    resume_session_id = existing.get("session_id")
    resume_value = resume_session_id if isinstance(resume_session_id, str) and resume_session_id else None
    try:
        session_name, window_id, window_index, pane_id = create_tmux_surface(
            session,
            "pane",
            f"impl-{ticket_id.lower()}",
        )
    except SystemExit as exc:
        return print_followup_failure(ticket_id, args.phase, "tmux launch failed", stderr=str(exc))
    state = persist_lane_state(
        ticket=ticket,
        phase=args.phase,
        run_state=run_state,
        compute_class=compute_class,
        worker_name=worker_name,
        main_artifact_path=main_artifact_path,
        execution_phase=execution_phase,
        tmux_session=session_name,
        tmux_window=window_id,
        tmux_pane=pane_id,
        auto_continue=auto_continue,
        existing=existing,
    )
    command = lane_shell_command(
        ticket,
        run_state,
        ticket_id,
        args.phase,
        str(existing.get("executor_target") or "") or None,
        prompt_text,
        resume_value,
        False,
    )
    sent = run(["tmux", "send-keys", "-t", pane_id, command, "C-m"])
    if sent.returncode != 0:
        return print_followup_failure(
            ticket_id,
            args.phase,
            "tmux send-keys failed",
            pane_id=pane_id,
            stderr=sent.stderr.strip() or sent.stdout.strip(),
        )
    payload = {
        "action": "followup",
        "ticket": str(ticket),
        "phase": args.phase,
        "execution_phase": execution_phase,
        "worker_name": worker_name,
        "main_artifact_path": main_artifact_path,
        "tmux_session": session_name,
        "tmux_window": window_id,
        "tmux_window_index": window_index,
        "tmux_pane": pane_id,
        "run_state": str(run_state),
        "reused_existing_pane": False,
        "resumed_session": bool(resume_value),
    }
    session_id = state.get("session_id")
    if isinstance(session_id, str) and session_id:
        payload["session_id"] = session_id
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(format_followup_success(payload))
    return 0


def attach(args: argparse.Namespace) -> int:
    run_state = resolve_existing_path(args.run_state) if args.run_state else current_run_state_path()
    payload = read_json(run_state)
    pane = payload.get("tmux_pane")
    window = payload.get("tmux_window")
    session = payload.get("tmux_session")
    if isinstance(window, str) and window:
        run(["tmux", "select-window", "-t", window])
    elif isinstance(session, str) and session:
        run(["tmux", "switch-client", "-t", session])
    if isinstance(pane, str) and pane:
        run(["tmux", "select-pane", "-t", pane])
    result = {"session": session, "window": window, "pane": pane}
    session_id = payload.get("session_id")
    if isinstance(session_id, str) and session_id:
        result["session_id"] = session_id
    print(json.dumps(result, indent=2))
    return 0


def status(args: argparse.Namespace) -> int:
    run_state = resolve_existing_path(args.run_state) if args.run_state else current_run_state_path()
    payload = read_json(run_state)
    if not payload:
        raise SystemExit(f"run state not found or unreadable: {run_state}")
    ticket_id = payload.get("ticket_id")
    if isinstance(ticket_id, str) and ticket_id and "last_hook_decision" not in payload:
        hook_status = latest_hook_status(ticket_id)
        if hook_status is not None:
            payload.update(hook_status)
    elif "last_hook_decision" in payload:
        payload["hook_status_source"] = "run-state"
    pane = payload.get("tmux_pane")
    if isinstance(pane, str) and pane:
        metadata = pane_metadata(pane)
        if metadata:
            payload.update(metadata)
    payload = annotate_backpressure(payload)
    print(json.dumps(payload, indent=2))
    return 0


def tail(args: argparse.Namespace) -> int:
    run_state = resolve_existing_path(args.run_state) if args.run_state else current_run_state_path()
    payload = read_json(run_state)
    pane = payload.get("tmux_pane")
    if not isinstance(pane, str) or not pane:
        raise SystemExit("no tmux pane recorded in run state")
    result = run(["tmux", "capture-pane", "-t", pane, "-p", "-S", f"-{args.lines}"])
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or "tmux capture-pane failed")
    sys.stdout.write(result.stdout)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_launch = subparsers.add_parser("launch")
    p_launch.add_argument("--ticket", required=True)
    p_launch.add_argument("--phase", required=True, choices=["planning", "building", "documenting"])
    p_launch.add_argument("--run-state")
    p_launch.add_argument("--tmux-session")
    p_launch.add_argument("--layout", choices=["pane", "window"], default="pane")
    p_launch.add_argument("--name")
    p_launch.add_argument("--compute-class", default="local")
    p_launch.add_argument("--worker-name")
    p_launch.add_argument("--execution-phase", choices=["impl", "qa", "demo"])
    p_launch.add_argument("--auto-continue", action="store_true")
    p_launch.add_argument("--dry-run", action="store_true")
    p_launch.set_defaults(func=launch)

    p_followup = subparsers.add_parser("followup")
    p_followup.add_argument("--ticket", required=True)
    p_followup.add_argument("--phase", required=True, choices=["planning", "building", "documenting"])
    p_followup.add_argument("--run-state")
    p_followup.add_argument("--tmux-session")
    p_followup.add_argument("--compute-class")
    p_followup.add_argument("--worker-name")
    p_followup.add_argument("--execution-phase", choices=["impl", "qa", "demo"])
    p_followup.add_argument("--reason")
    p_followup.add_argument("--auto-continue", action="store_true")
    p_followup.add_argument("--dry-run", action="store_true")
    p_followup.add_argument("--json", action="store_true")
    p_followup.set_defaults(func=followup)

    p_attach = subparsers.add_parser("attach")
    p_attach.add_argument("--run-state")
    p_attach.set_defaults(func=attach)

    p_status = subparsers.add_parser("status")
    p_status.add_argument("--run-state")
    p_status.set_defaults(func=status)

    p_tail = subparsers.add_parser("tail")
    p_tail.add_argument("--run-state")
    p_tail.add_argument("--lines", type=int, default=80)
    p_tail.set_defaults(func=tail)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
