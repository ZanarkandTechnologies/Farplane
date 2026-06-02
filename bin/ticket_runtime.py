#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKOUT_MODES = ("shared", "worktree")
RUNTIME_MODES = ("shared", "branch-runtime", "branch-compose")
RESERVATION_KINDS = ("frontend", "backend", "db")
COMMAND_ENV_DEFAULTS = {
    "frontend_cmd": "FARPLANE_RUNTIME_FRONTEND_CMD",
    "backend_cmd": "FARPLANE_RUNTIME_BACKEND_CMD",
    "compose_up_cmd": "FARPLANE_RUNTIME_COMPOSE_UP_CMD",
    "compose_down_cmd": "FARPLANE_RUNTIME_COMPOSE_DOWN_CMD",
}
PROCESS_KINDS = ("frontend", "backend", "compose")
LIVE_PROCESSES: dict[int, subprocess.Popen[bytes]] = {}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def runtime_state_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / ".harness" / "state"


def ticket_runtime_dir(root: Path | None = None) -> Path:
    return runtime_state_dir(root) / "tickets"


def ticket_log_dir(root: Path | None = None) -> Path:
    return ticket_runtime_dir(root) / "logs"


def ports_state_path(root: Path | None = None) -> Path:
    return runtime_state_dir(root) / "ports.json"


def runtime_record_path(ticket_id: str, root: Path | None = None) -> Path:
    # MEM-0060: ticket-scoped runtime metadata lives under `.harness/state/tickets/`.
    return ticket_runtime_dir(root) / f"{ticket_id}.runtime.json"


def qa_artifacts_path(ticket_id: str, root: Path | None = None) -> str:
    return str((root or project_root()) / "tickets" / ticket_id / "artifacts" / "qa")


def worktree_root(root: Path | None = None) -> Path:
    resolved_root = root or project_root()
    override = str(os.environ.get("FARPLANE_WORKTREE_ROOT") or "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return resolved_root.parent / f".{resolved_root.name}-worktrees"


def slugify(raw: str) -> str:
    lowered = raw.strip().lower()
    collapsed = re.sub(r"[^a-z0-9._-]+", "-", lowered)
    return collapsed.strip("-") or "work"


def default_branch_for_ticket(ticket_id: str) -> str:
    return f"codex/{ticket_id.lower()}"


def default_worktree_path(branch: str, root: Path | None = None) -> Path:
    return worktree_root(root) / slugify(branch)


def service_log_path(ticket_id: str, service: str, root: Path | None = None) -> Path:
    return ticket_log_dir(root) / f"{ticket_id.lower()}-{service}.log"


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def checked_mode(value: str, allowed: tuple[str, ...], label: str) -> str:
    if value not in allowed:
        raise SystemExit(f"invalid {label}: {value}")
    return value


def branch_exists(branch: str, root: Path | None = None) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=root or project_root(),
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def ensure_worktree(
    branch: str,
    *,
    create: bool,
    root: Path | None = None,
) -> Path:
    resolved_root = root or project_root()
    destination = default_worktree_path(branch, resolved_root)
    if destination.exists():
        return destination
    if not create:
        raise SystemExit(
            f"worktree checkout does not exist for {branch}; rerun with --create-worktree"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    if branch_exists(branch, resolved_root):
        cmd = ["git", "worktree", "add", str(destination), branch]
    else:
        cmd = ["git", "worktree", "add", "-b", branch, str(destination)]
    result = subprocess.run(
        cmd,
        cwd=resolved_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"git worktree add failed for {branch}")
    return destination


def load_ports_state(root: Path | None = None) -> dict[str, dict[str, str]]:
    payload = read_json(ports_state_path(root), {"used": {}})
    used = payload.get("used")
    if not isinstance(used, dict):
        return {"used": {}}
    normalized: dict[str, str] = {}
    for port, owner in used.items():
        if isinstance(port, str) and isinstance(owner, str):
            normalized[port] = owner
    return {"used": normalized}


def save_ports_state(payload: dict[str, dict[str, str]], root: Path | None = None) -> None:
    write_json(ports_state_path(root), payload)


def port_base(kind: str) -> int:
    mapping = {
        "frontend": int(os.environ.get("FARPLANE_FRONTEND_PORT_BASE", "3100")),
        "backend": int(os.environ.get("FARPLANE_BACKEND_PORT_BASE", "4100")),
        "db": int(os.environ.get("FARPLANE_DB_PORT_BASE", "5400")),
    }
    return mapping[kind]


def allocate_port(kind: str, owner: str, *, root: Path | None = None) -> int:
    state = load_ports_state(root)
    used = state["used"]
    base = port_base(kind)
    for candidate in range(base, base + 200):
        key = str(candidate)
        if key not in used:
            used[key] = owner
            save_ports_state(state, root)
            return candidate
    raise SystemExit(f"no free {kind} port available in range starting at {base}")


def release_ports(ports: dict[str, int], *, root: Path | None = None) -> None:
    state = load_ports_state(root)
    used = state["used"]
    changed = False
    for port in ports.values():
        key = str(port)
        if key in used:
            del used[key]
            changed = True
    if changed:
        save_ports_state(state, root)


def normalize_targets(
    *,
    runtime_mode: str,
    ports: dict[str, int],
    frontend_url: str,
    backend_url: str,
) -> dict[str, str]:
    targets: dict[str, str] = {}
    if frontend_url:
        targets["frontend_url"] = frontend_url
    elif runtime_mode != "shared" and "frontend" in ports:
        targets["frontend_url"] = f"http://127.0.0.1:{ports['frontend']}"
    if backend_url:
        targets["backend_url"] = backend_url
    elif runtime_mode != "shared" and "backend" in ports:
        targets["backend_url"] = f"http://127.0.0.1:{ports['backend']}"
    return targets


def normalize_ticket_id(ticket_id: str) -> str:
    normalized = ticket_id.strip().upper()
    if not re.fullmatch(r"TASK-\d{4}", normalized):
        raise SystemExit(f"invalid ticket id: {ticket_id}")
    return normalized


def normalize_commands(
    existing: dict[str, Any],
    *,
    frontend_cmd: str,
    backend_cmd: str,
    compose_up_cmd: str,
    compose_down_cmd: str,
) -> dict[str, str]:
    existing_commands = existing.get("commands")
    previous = existing_commands if isinstance(existing_commands, dict) else {}
    commands: dict[str, str] = {}
    explicit = {
        "frontend_cmd": frontend_cmd,
        "backend_cmd": backend_cmd,
        "compose_up_cmd": compose_up_cmd,
        "compose_down_cmd": compose_down_cmd,
    }
    for key, env_name in COMMAND_ENV_DEFAULTS.items():
        value = explicit[key].strip()
        if not value:
            raw_previous = previous.get(key)
            if isinstance(raw_previous, str):
                value = raw_previous.strip()
        if not value:
            value = str(os.environ.get(env_name) or "").strip()
        if value:
            commands[key] = value
    return commands


def persist_runtime_record(record: dict[str, Any], *, root: Path | None = None) -> None:
    write_json(runtime_record_path(str(record["ticket_id"]), root), record)


def process_alive(pid: int) -> bool:
    proc = LIVE_PROCESSES.get(pid)
    if proc is not None:
        return proc.poll() is None
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def stop_process_group(pid: int) -> bool:
    if pid <= 0:
        return True
    try:
        pgid = os.getpgid(pid)
    except ProcessLookupError:
        proc = LIVE_PROCESSES.pop(pid, None)
        if proc is not None:
            proc.wait(timeout=0.1)
        return True
    try:
        os.killpg(pgid, signal.SIGTERM)
    except PermissionError:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            proc = LIVE_PROCESSES.pop(pid, None)
            if proc is not None:
                proc.wait(timeout=0.1)
            return True
    deadline = time.time() + 5.0
    while time.time() < deadline:
        if not process_alive(pid):
            proc = LIVE_PROCESSES.pop(pid, None)
            if proc is not None:
                proc.wait(timeout=0.1)
            return True
        time.sleep(0.1)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except PermissionError:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            proc = LIVE_PROCESSES.pop(pid, None)
            if proc is not None:
                proc.wait(timeout=0.1)
            return True
    except ProcessLookupError:
        proc = LIVE_PROCESSES.pop(pid, None)
        if proc is not None:
            proc.wait(timeout=0.1)
        return True
    deadline = time.time() + 2.0
    while time.time() < deadline:
        if not process_alive(pid):
            proc = LIVE_PROCESSES.pop(pid, None)
            if proc is not None:
                proc.wait(timeout=0.1)
            return True
        time.sleep(0.1)
    alive = process_alive(pid)
    if not alive:
        proc = LIVE_PROCESSES.pop(pid, None)
        if proc is not None:
            proc.wait(timeout=0.1)
    return not alive


def runtime_environment(record: dict[str, Any], *, service: str) -> dict[str, str]:
    env = os.environ.copy()
    env["TICKET_ID"] = str(record["ticket_id"])
    env["TICKET_BRANCH"] = str(record.get("branch") or "")
    env["TICKET_RUNTIME_MODE"] = str(record.get("runtime_mode") or "")
    env["TICKET_CHECKOUT_MODE"] = str(record.get("checkout_mode") or "")
    env["TICKET_CHECKOUT_PATH"] = str(record.get("checkout_path") or "")
    ports = record.get("ports", {})
    if isinstance(ports, dict):
        for kind in RESERVATION_KINDS:
            raw = ports.get(kind)
            if isinstance(raw, int):
                env[f"{kind.upper()}_PORT"] = str(raw)
    if service in ("frontend", "backend"):
        raw = ports.get(service) if isinstance(ports, dict) else None
        if isinstance(raw, int):
            env["PORT"] = str(raw)
    return env


def launch_service_process(
    *,
    ticket_id: str,
    service: str,
    command: str,
    checkout_path: Path,
    record: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    if not command.strip():
        raise SystemExit(f"missing {service} command")
    log_path = service_log_path(ticket_id, service, root)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = runtime_environment(record, service=service)
    with log_path.open("ab") as log_handle:
        proc = subprocess.Popen(
            command,
            shell=True,
            cwd=checkout_path,
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    time.sleep(0.05)
    exit_code = proc.poll()
    if exit_code is not None:
        proc.wait(timeout=0.1)
        raise SystemExit(
            f"{service} command exited during startup with code {exit_code}; see {log_path}"
        )
    LIVE_PROCESSES[proc.pid] = proc
    return {
        "kind": "process",
        "command": command,
        "pid": proc.pid,
        "log_path": str(log_path),
        "started_at": now_iso(),
        "running": True,
    }


def run_compose_command(
    *,
    ticket_id: str,
    command: str,
    stage: str,
    checkout_path: Path,
    record: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    if not command.strip():
        raise SystemExit(f"missing compose {stage} command")
    log_path = service_log_path(ticket_id, "compose", root)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = runtime_environment(record, service="compose")
    with log_path.open("ab") as log_handle:
        result = subprocess.run(
            command,
            shell=True,
            cwd=checkout_path,
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if result.returncode != 0:
        raise SystemExit(f"compose {stage} command failed with exit code {result.returncode}")
    return {
        "kind": "compose",
        "command": command,
        "stage": stage,
        "log_path": str(log_path),
        "started_at": now_iso(),
        "running": stage == "up",
        "last_exit_code": result.returncode,
    }


def refresh_process_states(record: dict[str, Any]) -> dict[str, Any]:
    refreshed = dict(record)
    processes = record.get("processes", {})
    if not isinstance(processes, dict):
        return refreshed
    updated_processes: dict[str, Any] = {}
    running_services = False
    for key, value in processes.items():
        if not isinstance(value, dict):
            continue
        meta = dict(value)
        pid = meta.get("pid")
        if isinstance(pid, int):
            meta["running"] = process_alive(pid)
            running_services = running_services or bool(meta["running"])
        elif key == "compose":
            running_services = running_services or bool(meta.get("running"))
        updated_processes[key] = meta
    refreshed["processes"] = updated_processes
    if refreshed.get("status") == "running":
        if refreshed.get("runtime_mode") == "branch-compose":
            compose_meta = updated_processes.get("compose", {})
            if isinstance(compose_meta, dict) and not compose_meta.get("running", False):
                refreshed["status"] = "stopped"
        elif not running_services:
            refreshed["status"] = "stopped"
    return refreshed


def ensure_runtime_record(
    *,
    ticket_id: str,
    branch: str,
    checkout_mode: str,
    runtime_mode: str,
    owner_session: str,
    reason: str,
    reserve: tuple[str, ...],
    frontend_url: str,
    backend_url: str,
    create_worktree: bool,
    frontend_cmd: str = "",
    backend_cmd: str = "",
    compose_up_cmd: str = "",
    compose_down_cmd: str = "",
    root: Path | None = None,
) -> dict[str, Any]:
    resolved_root = root or project_root()
    normalized_ticket_id = normalize_ticket_id(ticket_id)
    normalized_branch = branch.strip() or default_branch_for_ticket(normalized_ticket_id)
    checked_mode(checkout_mode, CHECKOUT_MODES, "checkout mode")
    checked_mode(runtime_mode, RUNTIME_MODES, "runtime mode")
    existing = read_json(runtime_record_path(normalized_ticket_id, resolved_root), {})
    ports: dict[str, int] = {}
    existing_ports = existing.get("ports")
    if isinstance(existing_ports, dict):
        for kind in RESERVATION_KINDS:
            raw = existing_ports.get(kind)
            if isinstance(raw, int):
                ports[kind] = raw
    owner_label = f"{normalized_ticket_id}:{normalized_branch}"
    for kind in reserve:
        if kind not in ports:
            ports[kind] = allocate_port(kind, f"{owner_label}:{kind}", root=resolved_root)
    if checkout_mode == "worktree":
        checkout_path = str(
            ensure_worktree(normalized_branch, create=create_worktree, root=resolved_root)
        )
    else:
        checkout_path = str(resolved_root)
    targets = normalize_targets(
        runtime_mode=runtime_mode,
        ports=ports,
        frontend_url=frontend_url.strip(),
        backend_url=backend_url.strip(),
    )
    existing_processes = existing.get("processes")
    commands = normalize_commands(
        existing,
        frontend_cmd=frontend_cmd,
        backend_cmd=backend_cmd,
        compose_up_cmd=compose_up_cmd,
        compose_down_cmd=compose_down_cmd,
    )
    record = {
        "ticket_id": normalized_ticket_id,
        "branch": normalized_branch,
        "checkout_mode": checkout_mode,
        "checkout_path": checkout_path,
        "runtime_mode": runtime_mode,
        "reason": reason.strip(),
        "owner_session": owner_session.strip(),
        "ports": ports,
        "targets": targets,
        "commands": commands,
        "processes": existing_processes if isinstance(existing_processes, dict) else {},
        "status": str(existing.get("status") or "prepared"),
        "updated_at": now_iso(),
    }
    persist_runtime_record(record, root=resolved_root)
    return record


def load_runtime_record(ticket_id: str, *, root: Path | None = None) -> dict[str, Any]:
    record = read_json(runtime_record_path(normalize_ticket_id(ticket_id), root), {})
    if not isinstance(record, dict) or not record:
        raise SystemExit(f"no runtime record found for {ticket_id}")
    return record


def status_payload(ticket_id: str, *, root: Path | None = None) -> dict[str, Any]:
    record = refresh_process_states(load_runtime_record(ticket_id, root=root))
    persist_runtime_record(record, root=root)
    return record


def has_running_processes(record: dict[str, Any]) -> bool:
    processes = record.get("processes", {})
    if not isinstance(processes, dict):
        return False
    for value in processes.values():
        if isinstance(value, dict) and bool(value.get("running")):
            return True
    return False


def runtime_open_targets(record: dict[str, Any]) -> dict[str, str]:
    targets = record.get("targets", {})
    if not isinstance(targets, dict):
        return {}
    runtime_mode = str(record.get("runtime_mode") or "")
    if runtime_mode == "shared":
        return {k: v for k, v in targets.items() if isinstance(v, str)}
    processes = record.get("processes", {})
    if not isinstance(processes, dict):
        return {}
    if runtime_mode == "branch-compose":
        compose = processes.get("compose")
        if isinstance(compose, dict) and bool(compose.get("running")):
            return {k: v for k, v in targets.items() if isinstance(v, str)}
        return {}
    open_targets: dict[str, str] = {}
    for service_key in ("frontend", "backend"):
        meta = processes.get(service_key)
        target_key = f"{service_key}_url"
        target_value = targets.get(target_key)
        if (
            isinstance(meta, dict)
            and bool(meta.get("running"))
            and isinstance(target_value, str)
            and target_value
        ):
            open_targets[target_key] = target_value
    return open_targets


def releasable_ports(record: dict[str, Any]) -> dict[str, int]:
    ports = record.get("ports", {})
    if not isinstance(ports, dict):
        return {}
    runtime_mode = str(record.get("runtime_mode") or "")
    processes = record.get("processes", {})
    if not isinstance(processes, dict):
        processes = {}
    releasable: dict[str, int] = {}
    if runtime_mode == "branch-compose":
        compose = processes.get("compose")
        compose_running = isinstance(compose, dict) and bool(compose.get("running"))
        if compose_running:
            return {}
        return {k: v for k, v in ports.items() if isinstance(v, int)}
    for kind, raw in ports.items():
        if not isinstance(raw, int):
            continue
        if kind in ("frontend", "backend"):
            meta = processes.get(kind)
            if isinstance(meta, dict) and bool(meta.get("running")):
                continue
        releasable[kind] = raw
    return releasable


def qa_payload(ticket_id: str, *, root: Path | None = None) -> dict[str, Any]:
    record = status_payload(ticket_id, root=root)
    return {
        "ticket_id": record["ticket_id"],
        "runtime_mode": record.get("runtime_mode", ""),
        "status": record.get("status", ""),
        "open_targets": runtime_open_targets(record),
        "artifacts_path": qa_artifacts_path(str(record["ticket_id"]), root),
    }


def stop_runtime_processes(record: dict[str, Any], *, root: Path) -> dict[str, Any]:
    processes = record.get("processes", {})
    if not isinstance(processes, dict):
        return {}
    updated: dict[str, Any] = {}
    checkout_path = Path(str(record.get("checkout_path") or root))
    for key in PROCESS_KINDS:
        value = processes.get(key)
        if not isinstance(value, dict):
            continue
        meta = dict(value)
        pid = meta.get("pid")
        if isinstance(pid, int):
            stop_succeeded = stop_process_group(pid)
            meta["running"] = not stop_succeeded
            meta["stop_succeeded"] = stop_succeeded
            meta["stopped_at"] = now_iso()
        elif key == "compose":
            commands = record.get("commands", {})
            down_command = ""
            if isinstance(commands, dict):
                raw = commands.get("compose_down_cmd")
                if isinstance(raw, str):
                    down_command = raw.strip()
            if down_command:
                try:
                    down_meta = run_compose_command(
                        ticket_id=str(record["ticket_id"]),
                        command=down_command,
                        stage="down",
                        checkout_path=checkout_path,
                        record=record,
                        root=root,
                    )
                    meta["down_command"] = down_command
                    meta["down_log_path"] = down_meta["log_path"]
                    meta["last_exit_code"] = down_meta["last_exit_code"]
                    meta["running"] = False
                    meta["stop_succeeded"] = True
                    meta.pop("stop_error", None)
                except SystemExit as error:
                    meta["running"] = True
                    meta["stop_succeeded"] = False
                    meta["stop_error"] = str(error)
            else:
                meta["running"] = True
                meta["stop_succeeded"] = False
                meta["stop_error"] = "missing compose down command"
            meta["stopped_at"] = now_iso()
        updated[key] = meta
    return updated


def up_runtime_record(
    *,
    ticket_id: str,
    branch: str,
    checkout_mode: str,
    runtime_mode: str,
    owner_session: str,
    reason: str,
    reserve: tuple[str, ...],
    frontend_url: str,
    backend_url: str,
    create_worktree: bool,
    frontend_cmd: str = "",
    backend_cmd: str = "",
    compose_up_cmd: str = "",
    compose_down_cmd: str = "",
    root: Path | None = None,
) -> dict[str, Any]:
    resolved_root = root or project_root()
    record = ensure_runtime_record(
        ticket_id=ticket_id,
        branch=branch,
        checkout_mode=checkout_mode,
        runtime_mode=runtime_mode,
        owner_session=owner_session,
        reason=reason,
        reserve=reserve,
        frontend_url=frontend_url,
        backend_url=backend_url,
        create_worktree=create_worktree,
        frontend_cmd=frontend_cmd,
        backend_cmd=backend_cmd,
        compose_up_cmd=compose_up_cmd,
        compose_down_cmd=compose_down_cmd,
        root=resolved_root,
    )
    existing_processes = stop_runtime_processes(record, root=resolved_root)
    if existing_processes:
        record["processes"] = existing_processes
    if has_running_processes(record):
        record["status"] = "stop_failed"
        record["updated_at"] = now_iso()
        persist_runtime_record(record, root=resolved_root)
        raise SystemExit("cannot start a new runtime while an existing tracked runtime is still running")
    record["status"] = "prepared"
    record["updated_at"] = now_iso()
    persist_runtime_record(record, root=resolved_root)
    checkout_path = Path(str(record.get("checkout_path") or ""))
    if not checkout_path.exists():
        raise SystemExit(f"checkout path does not exist: {checkout_path}")
    commands = record.get("commands", {})
    if not isinstance(commands, dict):
        commands = {}

    processes: dict[str, Any] = {}
    try:
        if runtime_mode == "branch-compose":
            raw = commands.get("compose_up_cmd")
            compose_up = raw.strip() if isinstance(raw, str) else ""
            if not compose_up:
                raise SystemExit(
                    "branch-compose mode requires --compose-up-cmd or FARPLANE_RUNTIME_COMPOSE_UP_CMD"
                )
            down_raw = commands.get("compose_down_cmd")
            compose_down = down_raw.strip() if isinstance(down_raw, str) else ""
            if not compose_down:
                raise SystemExit(
                    "branch-compose mode requires --compose-down-cmd or FARPLANE_RUNTIME_COMPOSE_DOWN_CMD"
                )
            compose_meta = run_compose_command(
                ticket_id=str(record["ticket_id"]),
                command=compose_up,
                stage="up",
                checkout_path=checkout_path,
                record=record,
                root=resolved_root,
            )
            compose_meta["down_command"] = compose_down
            processes["compose"] = compose_meta
        else:
            for service_key, command_key in (
                ("frontend", "frontend_cmd"),
                ("backend", "backend_cmd"),
            ):
                raw = commands.get(command_key)
                command = raw.strip() if isinstance(raw, str) else ""
                if not command:
                    continue
                processes[service_key] = launch_service_process(
                    ticket_id=str(record["ticket_id"]),
                    service=service_key,
                    command=command,
                    checkout_path=checkout_path,
                    record=record,
                    root=resolved_root,
                )
            if not processes:
                raise SystemExit(
                    "no frontend/backend runtime commands configured; pass --frontend-cmd and/or --backend-cmd"
                )
    except BaseException:
        cleanup_record = deepcopy(record)
        if processes:
            cleanup_record["processes"] = processes
            cleanup_record["processes"] = stop_runtime_processes(
                cleanup_record, root=resolved_root
            )
        cleanup_record["status"] = "stop_failed" if has_running_processes(cleanup_record) else "launch_failed"
        cleanup_record["updated_at"] = now_iso()
        persist_runtime_record(cleanup_record, root=resolved_root)
        raise

    record["processes"] = processes
    record["status"] = "running"
    record["updated_at"] = now_iso()
    persist_runtime_record(record, root=resolved_root)
    refreshed = refresh_process_states(record)
    persist_runtime_record(refreshed, root=resolved_root)
    return refreshed


def down_runtime_record(
    ticket_id: str,
    *,
    remove_worktree: bool,
    root: Path | None = None,
) -> dict[str, Any]:
    resolved_root = root or project_root()
    record = load_runtime_record(ticket_id, root=resolved_root)
    record["processes"] = stop_runtime_processes(record, root=resolved_root)
    release_ports(releasable_ports(record), root=resolved_root)
    record["status"] = "stop_failed" if has_running_processes(record) else "stopped"
    record["updated_at"] = now_iso()
    persist_runtime_record(record, root=resolved_root)
    if remove_worktree and record.get("checkout_mode") == "worktree" and record["status"] == "stopped":
        checkout_path = Path(str(record.get("checkout_path") or ""))
        if checkout_path.exists():
            result = subprocess.run(
                ["git", "worktree", "remove", str(checkout_path)],
                cwd=resolved_root,
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode != 0:
                raise SystemExit(
                    result.stderr.strip() or f"git worktree remove failed for {checkout_path}"
                )
    return record


def render(payload: dict[str, Any], *, as_json: bool) -> str:
    if as_json:
        return json.dumps(payload, indent=2)
    summary = payload.get("ticket_id") or payload.get("ticket") or "runtime"
    status = payload.get("status") or payload.get("runtime_mode") or "ok"
    return f"{summary}: {status}"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Ticket runtime helper")
    sub = p.add_subparsers(dest="command", required=True)

    def add_common(cmd: argparse.ArgumentParser) -> None:
        cmd.add_argument("--ticket", required=True)
        cmd.add_argument("--branch", default="")
        cmd.add_argument("--checkout-mode", default="shared", choices=CHECKOUT_MODES)
        cmd.add_argument("--runtime-mode", default="shared", choices=RUNTIME_MODES)
        cmd.add_argument("--owner-session", default="")
        cmd.add_argument("--reason", default="")
        cmd.add_argument("--frontend-url", default="")
        cmd.add_argument("--backend-url", default="")
        cmd.add_argument("--frontend-cmd", default="")
        cmd.add_argument("--backend-cmd", default="")
        cmd.add_argument("--compose-up-cmd", default="")
        cmd.add_argument("--compose-down-cmd", default="")
        cmd.add_argument(
            "--reserve",
            action="append",
            default=[],
            choices=RESERVATION_KINDS,
            help="Reserve a port for the given target kind; repeat for multiple kinds",
        )
        cmd.add_argument("--create-worktree", action="store_true")
        cmd.add_argument("--json", action="store_true")

    p_ensure = sub.add_parser("ensure")
    add_common(p_ensure)

    p_up = sub.add_parser("up")
    add_common(p_up)

    p_status = sub.add_parser("status")
    p_status.add_argument("--ticket", required=True)
    p_status.add_argument("--json", action="store_true")

    p_qa = sub.add_parser("qa")
    p_qa.add_argument("--ticket", required=True)
    p_qa.add_argument("--json", action="store_true")

    p_down = sub.add_parser("down")
    p_down.add_argument("--ticket", required=True)
    p_down.add_argument("--remove-worktree", action="store_true")
    p_down.add_argument("--json", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    if args.command == "ensure":
        payload = ensure_runtime_record(
            ticket_id=args.ticket,
            branch=args.branch,
            checkout_mode=args.checkout_mode,
            runtime_mode=args.runtime_mode,
            owner_session=args.owner_session,
            reason=args.reason,
            reserve=tuple(args.reserve),
            frontend_url=args.frontend_url,
            backend_url=args.backend_url,
            create_worktree=args.create_worktree,
            frontend_cmd=args.frontend_cmd,
            backend_cmd=args.backend_cmd,
            compose_up_cmd=args.compose_up_cmd,
            compose_down_cmd=args.compose_down_cmd,
        )
    elif args.command == "up":
        payload = up_runtime_record(
            ticket_id=args.ticket,
            branch=args.branch,
            checkout_mode=args.checkout_mode,
            runtime_mode=args.runtime_mode,
            owner_session=args.owner_session,
            reason=args.reason,
            reserve=tuple(args.reserve),
            frontend_url=args.frontend_url,
            backend_url=args.backend_url,
            create_worktree=args.create_worktree,
            frontend_cmd=args.frontend_cmd,
            backend_cmd=args.backend_cmd,
            compose_up_cmd=args.compose_up_cmd,
            compose_down_cmd=args.compose_down_cmd,
        )
    elif args.command == "status":
        payload = status_payload(args.ticket)
    elif args.command == "qa":
        payload = qa_payload(args.ticket)
    else:
        payload = down_runtime_record(args.ticket, remove_worktree=args.remove_worktree)
    print(render(payload, as_json=getattr(args, "json", False)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
