#!/usr/bin/env python3
"""Core-owned event routing and deterministic local mining-run storage.

The module owns immutable program contracts, project-local route resolution,
at-least-once outbox draining, deterministic run identity, frozen replay, and
lean reports. It performs no transcript publication or deep model judgment.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from farplane_file_events import (
    DEFAULT_EVENTS,
    acknowledge_event,
    atomic_write_json,
    capture_payload,
    pending_events,
    read_json,
    sha256_value,
)


SCHEMA_VERSION = 1
CORE_DIR = Path(__file__).resolve().parent
DEFAULT_PROGRAM_ROOT = CORE_DIR / "mining_programs"
ALLOWED_VERDICTS = {"unreviewed", "promoted", "rejected"}


class MiningError(RuntimeError):
    """Raised when a mining contract, route, or run is invalid."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def bindings_path(project_root: Path) -> Path:
    return project_root / "farplane" / "bindings.yaml"


def mine_root(project_root: Path) -> Path:
    return project_root / ".farplane" / "mine"


def run_root(project_root: Path, run_id: str) -> Path:
    if not run_id or any(character not in "0123456789abcdef" for character in run_id.lower()):
        raise MiningError(f"unsafe_run_id:{run_id}")
    return mine_root(project_root) / "runs" / run_id.lower()


def _yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise MiningError(f"invalid_yaml:{path}:{exc}") from exc
    if not isinstance(payload, dict):
        raise MiningError(f"invalid_yaml_shape:{path}:expected_object")
    return payload


def _program_files(program_root: Path = DEFAULT_PROGRAM_ROOT) -> list[Path]:
    return sorted(program_root.glob("*.json")) if program_root.exists() else []


def load_program(program_ref: str, *, program_root: Path = DEFAULT_PROGRAM_ROOT) -> dict[str, Any]:
    for path in _program_files(program_root):
        program = read_json(path, {})
        if isinstance(program, dict) and program.get("program_ref") == program_ref:
            required = {"schema_version", "program_ref", "program_id", "version", "kind", "report_schema_version"}
            missing = sorted(required - set(program))
            if missing:
                raise MiningError(f"invalid_program:{path}:missing:{','.join(missing)}")
            return program
    raise MiningError(f"program_not_found:{program_ref}")


def list_programs(*, program_root: Path = DEFAULT_PROGRAM_ROOT) -> list[dict[str, Any]]:
    programs = []
    for path in _program_files(program_root):
        program = read_json(path, {})
        if not isinstance(program, dict) or not program.get("program_ref"):
            continue
        programs.append({**program, "program_digest": sha256_value(program), "source_path": str(path)})
    return sorted(programs, key=lambda row: str(row["program_ref"]))


def list_routes(project_root: Path) -> list[dict[str, Any]]:
    payload = _yaml_mapping(bindings_path(project_root))
    raw_routes = payload.get("event_routes")
    if raw_routes is None:
        return []
    if not isinstance(raw_routes, list):
        raise MiningError("invalid_event_routes:expected_list")
    if any(not isinstance(row, dict) for row in raw_routes):
        raise MiningError("invalid_event_routes:entries_must_be_objects")
    return [dict(row) for row in raw_routes]


def _route_issues(routes: list[dict[str, Any]], *, program_root: Path) -> list[str]:
    allowed_keys = {"route_id", "event_name", "program_ref", "enabled"}
    allowed_events = set(DEFAULT_EVENTS)
    issues: list[str] = []
    seen: set[str] = set()
    for index, route in enumerate(routes):
        prefix = f"event_routes.{index}"
        unsupported = sorted(set(route) - allowed_keys)
        if unsupported:
            issues.append(f"{prefix}.unsupported_keys:{','.join(unsupported)}")
        route_id = str(route.get("route_id") or "").strip()
        event_name = str(route.get("event_name") or "").strip()
        program_ref = str(route.get("program_ref") or "").strip()
        if not route_id:
            issues.append(f"{prefix}.route_id_missing")
        elif route_id in seen:
            issues.append(f"{prefix}.route_id_duplicate:{route_id}")
        else:
            seen.add(route_id)
        if not event_name:
            issues.append(f"{prefix}.event_name_missing")
        elif event_name not in allowed_events:
            issues.append(f"{prefix}.event_name_unsupported:{event_name}")
        if "enabled" in route and not isinstance(route["enabled"], bool):
            issues.append(f"{prefix}.enabled_not_boolean")
        if not program_ref:
            issues.append(f"{prefix}.program_ref_missing")
        else:
            try:
                load_program(program_ref, program_root=program_root)
            except MiningError as exc:
                issues.append(f"{prefix}.{exc}")
    return issues


def validate_routes(project_root: Path, *, program_root: Path = DEFAULT_PROGRAM_ROOT) -> dict[str, Any]:
    try:
        routes = list_routes(project_root)
    except MiningError as exc:
        return {"ok": False, "routes": [], "issues": [str(exc)]}
    issues = _route_issues(routes, program_root=program_root)
    return {"ok": not issues, "routes": routes, "issues": issues}


def _replace_top_level_yaml_section(text: str, key: str, replacement: str | None) -> str:
    lines = text.splitlines(keepends=True)
    start = None
    end = len(lines)
    for index, line in enumerate(lines):
        if line.startswith(f"{key}:"):
            start = index
            break
    if start is not None:
        for index in range(start + 1, len(lines)):
            line = lines[index]
            if re.match(r"^[A-Za-z0-9_-]+:\s*", line):
                end = index
                break
        del lines[start:end]
    if replacement:
        block = replacement if replacement.endswith("\n") else replacement + "\n"
        if start is None:
            if lines and lines[-1].strip():
                lines.append("\n")
            lines.append(block)
        else:
            lines.insert(start, block)
    return "".join(lines)


def _write_routes(project_root: Path, routes: list[dict[str, Any]]) -> None:
    path = bindings_path(project_root)
    if not path.exists():
        raise MiningError(f"bindings_missing:{path}")
    current = path.read_text(encoding="utf-8")
    replacement = yaml.safe_dump({"event_routes": routes}, sort_keys=False, allow_unicode=True).rstrip()
    updated = _replace_top_level_yaml_section(current, "event_routes", replacement)
    if updated == current:
        return
    # Bindings are tracked human config: use same-directory atomic replacement.
    temporary = path.with_name(f".{path.name}.farplane-mining.tmp")
    temporary.write_text(updated, encoding="utf-8")
    os.replace(temporary, path)


def set_route(
    project_root: Path,
    *,
    route_id: str,
    event_name: str,
    program_ref: str,
    program_root: Path = DEFAULT_PROGRAM_ROOT,
) -> list[dict[str, Any]]:
    load_program(program_ref, program_root=program_root)
    if not route_id.strip() or not event_name.strip():
        raise MiningError("route_id_and_event_name_required")
    route = {"route_id": route_id.strip(), "event_name": event_name.strip(), "program_ref": program_ref.strip()}
    current = list_routes(project_root)
    next_routes = [row for row in current if str(row.get("route_id") or "") != route["route_id"]]
    next_routes.append(route)
    next_routes.sort(key=lambda row: str(row.get("route_id") or ""))
    issues = _route_issues(next_routes, program_root=program_root)
    if issues:
        raise MiningError("invalid_event_routes_before_write:" + ",".join(issues))
    _write_routes(project_root, next_routes)
    validation = validate_routes(project_root, program_root=program_root)
    if not validation["ok"]:
        raise MiningError("invalid_event_routes_after_write:" + ",".join(validation["issues"]))
    return next_routes


def remove_route(project_root: Path, route_id: str) -> list[dict[str, Any]]:
    next_routes = [row for row in list_routes(project_root) if str(row.get("route_id") or "") != route_id]
    _write_routes(project_root, next_routes)
    return next_routes


def route_requests(event: dict[str, Any], project_root: Path) -> list[dict[str, Any]]:
    event_name = str(event.get("event_name") or "")
    requests = []
    for route in list_routes(project_root):
        if route.get("enabled", True) is False or str(route.get("event_name") or "") != event_name:
            continue
        route_id = str(route.get("route_id") or "").strip()
        program_ref = str(route.get("program_ref") or "").strip()
        if not route_id or not program_ref:
            raise MiningError(f"invalid_route_for_event:{event_name}")
        requests.append({"route_id": route_id, "event_id": event["event_id"], "program_ref": program_ref})
    return requests


def _file_manifest_entry(project_root: Path, relative_path: str, *, role: str, required: bool) -> dict[str, Any]:
    project_root = project_root.resolve()
    absolute = (project_root / relative_path).resolve()
    try:
        absolute.relative_to(project_root)
    except ValueError as exc:
        raise MiningError(f"unsafe_input_path:{relative_path}") from exc
    if not absolute.is_file():
        return {"role": role, "path": relative_path, "required": required, "exists": False}
    data = absolute.read_bytes()
    return {
        "role": role,
        "path": relative_path,
        "required": required,
        "exists": True,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }


def build_input(
    event: dict[str, Any],
    project_root: Path,
    *,
    parent_run_id: str | None = None,
    source_mode: str = "event",
) -> dict[str, Any]:
    entity_ref = event.get("entity_ref") if isinstance(event.get("entity_ref"), dict) else {}
    primary_path = str(entity_ref.get("path") or "")
    if not primary_path:
        raise MiningError("event_entity_path_missing")
    manifest = [_file_manifest_entry(project_root, primary_path, role="event_source", required=True)]
    if entity_ref.get("kind") == "ticket":
        ticket_dir = Path(primary_path).parent.as_posix()
        manifest.extend(
            [
                _file_manifest_entry(project_root, f"{ticket_dir}/program.md", role="program", required=False),
                _file_manifest_entry(project_root, f"{ticket_dir}/progress.md", role="progress", required=False),
            ]
        )
        artifact_root = project_root / ticket_dir / "artifacts"
        if artifact_root.exists():
            for path in sorted(artifact_root.rglob("*")):
                if path.is_file() and len(manifest) < 43:
                    relative = path.relative_to(project_root).as_posix()
                    manifest.append(_file_manifest_entry(project_root, relative, role="artifact", required=False))
    if manifest[0].get("exists"):
        manifest[0]["event_sha256"] = event.get("content_hash")
        manifest[0]["matches_event"] = manifest[0].get("sha256") == event.get("content_hash")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "source_mode": source_mode,
        "parent_run_id": parent_run_id,
        "event": event,
        "input_manifest": manifest,
    }
    payload["input_digest"] = sha256_value(
        {
            "schema_version": SCHEMA_VERSION,
            "source_mode": source_mode,
            "parent_run_id": parent_run_id,
            "event_identity": {
                key: event.get(key)
                for key in ("event_id", "event_name", "project_id", "entity_ref", "previous_hash", "content_hash", "terminal")
            },
            "input_manifest": manifest,
        }
    )
    return payload


def _build_report(input_payload: dict[str, Any], program: dict[str, Any], program_digest: str) -> dict[str, Any]:
    manifest = input_payload.get("input_manifest") if isinstance(input_payload.get("input_manifest"), list) else []
    required = [str(row.get("path")) for row in manifest if isinstance(row, dict) and row.get("required")]
    available = [str(row.get("path")) for row in manifest if isinstance(row, dict) and row.get("exists")]
    missing = [str(row.get("path")) for row in manifest if isinstance(row, dict) and row.get("required") and not row.get("exists")]
    mismatches = [
        str(row.get("path"))
        for row in manifest
        if isinstance(row, dict) and row.get("role") == "event_source" and row.get("exists") and row.get("matches_event") is False
    ]
    source_gaps = [
        {"id": f"missing:{path}", "reason": "required_input_missing", "input_ref": path} for path in missing
    ] + [
        {"id": f"changed:{path}", "reason": "source_changed_after_event", "input_ref": path} for path in mismatches
    ]
    event = input_payload.get("event") if isinstance(input_payload.get("event"), dict) else {}
    reason_codes = ["required_source_gap"] if source_gaps else []
    return {
        "schema_version": int(program.get("report_schema_version") or 1),
        "source": {
            "event_id": event.get("event_id"),
            "entity_ref": event.get("entity_ref"),
            "input_refs": available,
        },
        "program": {"ref": program.get("program_ref"), "digest": program_digest},
        "coverage": {"required": required, "available": available, "missing": missing},
        "observations": [
            {
                "id": "terminal-state",
                "kind": "ticket_terminal_state" if event.get("terminal") is not None else "file_change",
                "value": event.get("terminal"),
                "evidence_refs": [str((event.get("entity_ref") or {}).get("path") or "")],
            }
        ],
        "material_findings": [],
        "source_gaps": source_gaps,
        "escalation": {"decision": "deep" if reason_codes else "none", "reason_codes": reason_codes},
    }


def _attempt(run_id: str, ordinal: int, reason: str) -> dict[str, Any]:
    started = now_iso()
    return {
        "attempt_id": sha256_value({"run_id": run_id, "ordinal": ordinal, "reason": reason}),
        "run_id": run_id,
        "started_at": started,
        "completed_at": None,
        "status": "running",
        "reason": reason,
    }


def _load_run(project_root: Path, run_id: str) -> dict[str, Any]:
    payload = read_json(run_root(project_root, run_id) / "run.json", None)
    if not isinstance(payload, dict):
        raise MiningError(f"run_not_found:{run_id}")
    return payload


def ensure_run(
    project_root: Path,
    request: dict[str, Any],
    *,
    event: dict[str, Any],
    input_payload: dict[str, Any] | None = None,
    program_snapshot: dict[str, Any] | None = None,
    reason: str = "route",
    force_attempt: bool = False,
    program_root: Path = DEFAULT_PROGRAM_ROOT,
) -> dict[str, Any]:
    program = program_snapshot or load_program(str(request["program_ref"]), program_root=program_root)
    program_digest = sha256_value(program)
    inputs = input_payload or build_input(event, project_root)
    input_digest = str(inputs.get("input_digest") or sha256_value(inputs))
    route_id = str(request["route_id"])
    event_id = str(request["event_id"])
    run_id = sha256_value(
        {"event_id": event_id, "route_id": route_id, "program_digest": program_digest, "input_digest": input_digest}
    )
    root = run_root(project_root, run_id)
    claims = mine_root(project_root) / "claims"
    claims.mkdir(parents=True, exist_ok=True)
    lock_path = claims / f"{run_id}.lock"
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        current = read_json(root / "run.json", {})
        if isinstance(current, dict) and current.get("status") == "complete" and not force_attempt:
            return current
        root.mkdir(parents=True, exist_ok=True)
        stored_program = read_json(root / "program.json", None)
        stored_input = read_json(root / "input.json", None)
        if stored_program is not None and sha256_value(stored_program) != program_digest:
            raise MiningError(f"program_digest_mismatch:{run_id}")
        if stored_input is not None and str(stored_input.get("input_digest")) != input_digest:
            raise MiningError(f"input_digest_mismatch:{run_id}")
        if stored_program is None:
            atomic_write_json(root / "program.json", program)
        if stored_input is None:
            atomic_write_json(root / "input.json", inputs)
        attempts = read_json(root / "attempts.json", [])
        if not isinstance(attempts, list):
            attempts = []
        attempt = _attempt(run_id, len(attempts) + 1, reason)
        attempts.append(attempt)
        atomic_write_json(root / "attempts.json", attempts)
        created_at = str(current.get("created_at") or attempt["started_at"]) if isinstance(current, dict) else attempt["started_at"]
        running = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "route_id": route_id,
            "event_id": event_id,
            "program_ref": program.get("program_ref"),
            "program_digest": program_digest,
            "input_digest": input_digest,
            "input_manifest": inputs.get("input_manifest", []),
            "status": "running",
            "attempts": [row.get("attempt_id") for row in attempts if isinstance(row, dict)],
            "outputs": ["report.json"],
            "created_at": created_at,
            "parent_run_id": inputs.get("parent_run_id"),
        }
        atomic_write_json(root / "run.json", running)
        try:
            report = _build_report(inputs, program, program_digest)
            atomic_write_json(root / "report.json", report)
            completed_at = now_iso()
            attempt.update(status="complete", completed_at=completed_at)
            attempts[-1] = attempt
            atomic_write_json(root / "attempts.json", attempts)
            completed = {**running, "status": "complete", "completed_at": completed_at}
            atomic_write_json(root / "run.json", completed)
            return completed
        except Exception as exc:
            completed_at = now_iso()
            attempt.update(status="failed", completed_at=completed_at, error_ref=str(exc)[:500])
            attempts[-1] = attempt
            atomic_write_json(root / "attempts.json", attempts)
            atomic_write_json(root / "run.json", {**running, "status": "failed", "completed_at": completed_at})
            raise


def route_event(event: dict[str, Any], project_root: Path, *, program_root: Path = DEFAULT_PROGRAM_ROOT) -> list[dict[str, Any]]:
    runs = []
    for request in route_requests(event, project_root):
        inputs = build_input(event, project_root)
        request["input_manifest_digest"] = inputs["input_digest"]
        runs.append(
            ensure_run(
                project_root,
                request,
                event=event,
                input_payload=inputs,
                program_root=program_root,
            )
        )
    return runs


def drain_pending(project_root: Path, *, program_root: Path = DEFAULT_PROGRAM_ROOT) -> dict[str, Any]:
    processed = []
    failed = []
    for event in pending_events(project_root):
        event_id = str(event.get("event_id") or "")
        try:
            runs = route_event(event, project_root, program_root=program_root)
            acknowledge_event(project_root, event_id)
            processed.append({"event_id": event_id, "run_ids": [row["run_id"] for row in runs]})
        except Exception as exc:
            failed.append({"event_id": event_id, "error": str(exc)[:500]})
    return {"ok": not failed, "processed": processed, "failed": failed, "pending": len(pending_events(project_root))}


def handle_file_change(
    payload: dict[str, Any],
    project_root: Path,
    *,
    program_root: Path = DEFAULT_PROGRAM_ROOT,
) -> dict[str, Any]:
    """Run the required retry/capture/retry boundary for one hook payload."""

    before = drain_pending(project_root, program_root=program_root)
    events = capture_payload(payload, project_root=project_root)
    after = drain_pending(project_root, program_root=program_root)
    return {
        "ok": before["ok"] and after["ok"],
        "project_root": str(project_root.resolve()),
        "captured_event_ids": [event["event_id"] for event in events],
        "drain_before": before,
        "drain_after": after,
    }


def list_runs(project_root: Path) -> list[dict[str, Any]]:
    root = mine_root(project_root) / "runs"
    if not root.exists():
        return []
    rows = []
    for path in sorted(root.glob("*/run.json")):
        payload = read_json(path, None)
        if isinstance(payload, dict):
            rows.append(payload)
    return sorted(rows, key=lambda row: (str(row.get("created_at") or ""), str(row.get("run_id") or "")), reverse=True)


def show_run(project_root: Path, run_id: str) -> dict[str, Any]:
    root = run_root(project_root, run_id)
    run = _load_run(project_root, run_id)
    return {
        "run": run,
        "program": read_json(root / "program.json", None),
        "input": read_json(root / "input.json", None),
        "attempts": read_json(root / "attempts.json", []),
        "report": read_json(root / "report.json", None),
        "verdicts": read_json(root / "verdicts.json", {}),
    }


def replay_run(project_root: Path, run_id: str) -> dict[str, Any]:
    detail = show_run(project_root, run_id)
    run = detail["run"]
    program = detail["program"]
    inputs = detail["input"]
    if not isinstance(program, dict) or not isinstance(inputs, dict):
        raise MiningError(f"run_not_replayable:{run_id}")
    event = inputs.get("event") if isinstance(inputs.get("event"), dict) else {}
    request = {"route_id": run["route_id"], "event_id": run["event_id"], "program_ref": run["program_ref"]}
    return ensure_run(
        project_root,
        request,
        event=event,
        input_payload=inputs,
        program_snapshot=program,
        reason="replay_frozen",
        force_attempt=True,
    )


def rerun_run(project_root: Path, run_id: str, *, program_root: Path = DEFAULT_PROGRAM_ROOT) -> dict[str, Any]:
    detail = show_run(project_root, run_id)
    run = detail["run"]
    inputs = detail["input"]
    program = detail["program"]
    if not isinstance(inputs, dict) or not isinstance(program, dict):
        raise MiningError(f"run_not_rerunnable:{run_id}")
    event = inputs.get("event") if isinstance(inputs.get("event"), dict) else {}
    current_inputs = build_input(event, project_root, parent_run_id=run_id, source_mode="current_rerun")
    request = {"route_id": run["route_id"], "event_id": run["event_id"], "program_ref": run["program_ref"]}
    return ensure_run(
        project_root,
        request,
        event=event,
        input_payload=current_inputs,
        program_snapshot=program,
        reason="rerun_current_sources",
        program_root=program_root,
    )


def set_output_verdict(project_root: Path, run_id: str, output_id: str, verdict: str) -> dict[str, Any]:
    if verdict not in ALLOWED_VERDICTS:
        raise MiningError(f"invalid_verdict:{verdict}")
    if not output_id or "/" in output_id or ".." in output_id:
        raise MiningError(f"unsafe_output_id:{output_id}")
    root = run_root(project_root, run_id)
    _load_run(project_root, run_id)
    path = root / "verdicts.json"
    payload = read_json(path, {})
    if not isinstance(payload, dict):
        payload = {}
    payload[output_id] = {"verdict": verdict, "updated_at": now_iso()}
    atomic_write_json(path, payload)
    return payload[output_id]
