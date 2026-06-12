#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Mapping
from urllib import error, request


MAX_MESSAGE_EXCERPT = 180


def _safe_str(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _safe_int(value: object) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return int(value.strip())
        except ValueError:
            return 0
    return 0


def _load_json_dict(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _redact_text(raw: object, *, limit: int = MAX_MESSAGE_EXCERPT) -> str:
    text = " ".join(_safe_str(raw).split())
    text = re.sub(r"/Users/[^ ]+", "[local path]", text)
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def _event_files(project_root: Path) -> list[Path]:
    event_dir = project_root / ".farplane" / "events"
    if not event_dir.exists():
        return []
    return sorted(
        path
        for path in event_dir.glob("*.jsonl")
        if path.is_file() and path.name != "failed-sync.jsonl"
    )


def load_events(project_root: Path) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for path in _event_files(project_root):
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            if not raw_line.strip():
                continue
            try:
                payload = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                events.append(payload)
    return events


def _counter(events: list[dict[str, object]], key: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for event in events:
        value = _safe_str(event.get(key))
        if value:
            counts[value] += 1
    return dict(sorted(counts.items()))


def summarize_events(project_root: Path) -> dict[str, object]:
    events = load_events(project_root)
    failed_sync_path = project_root / ".farplane" / "events" / "failed-sync.jsonl"
    failed_sync_count = 0
    if failed_sync_path.exists():
        failed_sync_count = len([line for line in failed_sync_path.read_text(encoding="utf-8").splitlines() if line.strip()])
    return {
        "total": len(events),
        "by_event_type": _counter(events, "event_type"),
        "by_skill": _counter(events, "skill_name"),
        "by_hook": _counter(events, "hook_name"),
        "by_ticket": _counter(events, "ticket_id"),
        "by_status": _counter(events, "status"),
        "latest": events[-10:],
        "failed_sync_count": failed_sync_count,
    }


def self_improve_root(project_root: Path) -> Path:
    return project_root / ".farplane" / "state" / "self-improve"


def _windows(project_root: Path) -> list[dict[str, object]]:
    windows_dir = self_improve_root(project_root) / "windows"
    if not windows_dir.exists():
        return []
    windows = [_load_json_dict(path) for path in sorted(windows_dir.glob("*.json"))]
    return [window for window in windows if window]


def _proof_hop_summary(report: Mapping[str, object]) -> dict[str, object]:
    raw_hops = report.get("proof_hops")
    if not isinstance(raw_hops, list):
        return {"present": 0, "total": 0, "missing": []}
    missing: list[str] = []
    present = 0
    for index, hop in enumerate(raw_hops, start=1):
        if not isinstance(hop, Mapping):
            missing.append(f"hop_{index}")
            continue
        status = _safe_str(hop.get("status")).lower()
        label = _safe_str(hop.get("label")) or _safe_str(hop.get("name")) or f"hop_{index}"
        if status in {"pass", "present", "done", "complete", "ok"}:
            present += 1
        else:
            missing.append(label)
    return {"present": present, "total": len(raw_hops), "missing": missing}


def _messages_from_input(input_payload: Mapping[str, object], *, limit: int = 4) -> list[dict[str, object]]:
    window = input_payload.get("window")
    if not isinstance(window, Mapping):
        return []
    raw_exchanges = window.get("rolling_exchanges")
    if not isinstance(raw_exchanges, list):
        return []
    messages: list[dict[str, object]] = []
    for exchange in raw_exchanges[-limit:]:
        if not isinstance(exchange, Mapping):
            continue
        user_turn = exchange.get("user_turn")
        user_map = user_turn if isinstance(user_turn, Mapping) else exchange
        user_text = _safe_str(user_map.get("summary")) or _safe_str(user_map.get("raw_text"))
        assistant_text = _safe_str(exchange.get("assistant_text"))
        if user_text:
            messages.append(
                {
                    "id": _safe_str(user_map.get("turn_id")) or _safe_str(exchange.get("user_turn_id")),
                    "role": "user",
                    "occurred_at": _safe_str(user_map.get("captured_at")),
                    "summary": _redact_text(user_text, limit=110),
                    "redacted_excerpt": _redact_text(user_map.get("raw_text") or user_text),
                }
            )
        if assistant_text:
            messages.append(
                {
                    "id": _safe_str(exchange.get("assistant_turn_id")),
                    "role": "assistant",
                    "occurred_at": _safe_str(exchange.get("assistant_captured_at")),
                    "summary": _redact_text(assistant_text, limit=110),
                    "redacted_excerpt": _redact_text(assistant_text),
                }
            )
    return messages[-limit:]


def _first_mapping(raw: object) -> Mapping[str, object]:
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, Mapping):
                return item
    return {}


def _learning_status(report: Mapping[str, object], run_dir: Path) -> str:
    raw_status = _safe_str(report.get("status"))
    if raw_status == "task_created":
        return "task_created"
    if raw_status == "no_change":
        return "no_signal"
    if raw_status == "dry_run":
        return "dry_run"
    if raw_status in {"failed", "blocked", "error"}:
        return "failed"
    if not report and ((run_dir / "stderr.log").exists() or (run_dir / "stdout.log").exists()):
        return "running_or_failed"
    return raw_status or "unknown"


def _run_summary(run_dir: Path) -> dict[str, object]:
    input_payload = _load_json_dict(run_dir / "input.json")
    report = _load_json_dict(run_dir / "report.json")
    trigger = input_payload.get("trigger") if isinstance(input_payload.get("trigger"), Mapping) else {}
    task = _first_mapping(report.get("notion_tasks"))
    decision = _first_mapping(report.get("decisions"))
    proof = _proof_hop_summary(report)
    title = (
        _safe_str(task.get("title"))
        or _safe_str(decision.get("summary"))
        or _safe_str(report.get("summary"))
        or "No learning suggestion recorded"
    )
    owner = _safe_str(decision.get("target")) or _safe_str(task.get("target")) or _safe_str(task.get("owner"))
    status = _learning_status(report, run_dir)
    return {
        "run_path": str(run_dir),
        "session_id": _safe_str(input_payload.get("session_id")),
        "status": status,
        "cadence": _safe_int(trigger.get("cadence")) if isinstance(trigger, Mapping) else 0,
        "turn_count": _safe_int(trigger.get("turn_count")) if isinstance(trigger, Mapping) else 0,
        "last_review_turn_count": _safe_int(trigger.get("last_review_turn_count")) if isinstance(trigger, Mapping) else 0,
        "candidate_title": title,
        "plain_summary": _safe_str(report.get("speak")) or title,
        "recommended_owner": owner or "unassigned",
        "confidence": _safe_str(decision.get("confidence")) or _safe_str(task.get("confidence")),
        "message_count": len(_messages_from_input(input_payload)),
        "messages": _messages_from_input(input_payload),
        "proof_hops_present": proof["present"],
        "proof_hops_total": proof["total"],
        "proof_hops_missing": proof["missing"],
        "artifacts": {
            "input": str(run_dir / "input.json") if (run_dir / "input.json").exists() else "",
            "report": str(run_dir / "report.json") if (run_dir / "report.json").exists() else "",
            "stdout": str(run_dir / "stdout.log") if (run_dir / "stdout.log").exists() else "",
            "stderr": str(run_dir / "stderr.log") if (run_dir / "stderr.log").exists() else "",
        },
        "reason": _safe_str(report.get("reason")) or _safe_str(trigger.get("reason")) if isinstance(trigger, Mapping) else "",
    }


def load_learning_runs(project_root: Path) -> list[dict[str, object]]:
    applications_dir = self_improve_root(project_root) / "applications"
    if not applications_dir.exists():
        return []
    run_dirs = [path for path in applications_dir.iterdir() if path.is_dir()]
    return [_run_summary(path) for path in sorted(run_dirs, key=lambda item: item.name, reverse=True)]


def summarize_learning(project_root: Path) -> dict[str, object]:
    windows = _windows(project_root)
    runs = load_learning_runs(project_root)
    statuses = Counter(_safe_str(run.get("status")) for run in runs if _safe_str(run.get("status")))
    return {
        "window_count": len(windows),
        "turn_count": sum(_safe_int(window.get("turn_count")) for window in windows),
        "reviewed_turn_count": sum(_safe_int(window.get("last_review_turn_count")) for window in windows),
        "run_count": len(runs),
        "by_status": dict(sorted(statuses.items())),
        "latest_runs": runs[:10],
    }


def build_status(project_root: Path) -> dict[str, object]:
    root = project_root.resolve()
    return {
        "schema_version": 1,
        "project_root": str(root),
        "project_name": root.name,
        "events": summarize_events(root),
        "learning": summarize_learning(root),
    }


def _cloud_event(event: object) -> dict[str, object]:
    if not isinstance(event, Mapping):
        return {}
    allowed = {
        "event_id",
        "event_type",
        "timestamp",
        "source",
        "project_name",
        "session_id",
        "turn_id",
        "ticket_id",
        "skill_name",
        "hook_name",
        "phase",
        "status",
        "outcome",
        "summary",
        "counts",
    }
    return {key: value for key, value in event.items() if key in allowed}


def _cloud_learning_run(run: object) -> dict[str, object]:
    if not isinstance(run, Mapping):
        return {}
    artifact_map = run.get("artifacts")
    artifact_labels = []
    if isinstance(artifact_map, Mapping):
        artifact_labels = [str(key) for key, value in artifact_map.items() if _safe_str(value)]
    allowed = {
        "session_id",
        "status",
        "cadence",
        "turn_count",
        "last_review_turn_count",
        "candidate_title",
        "plain_summary",
        "recommended_owner",
        "confidence",
        "message_count",
        "messages",
        "proof_hops_present",
        "proof_hops_total",
        "proof_hops_missing",
        "reason",
    }
    payload = {key: value for key, value in run.items() if key in allowed}
    payload["run_path"] = Path(_safe_str(run.get("run_path"))).name or "learning-run"
    payload["artifacts"] = {label: "present" for label in artifact_labels}
    return payload


def build_cloud_payload(status: Mapping[str, object]) -> dict[str, object]:
    events = status.get("events") if isinstance(status.get("events"), Mapping) else {}
    learning = status.get("learning") if isinstance(status.get("learning"), Mapping) else {}
    latest_events = events.get("latest") if isinstance(events, Mapping) else []
    latest_runs = learning.get("latest_runs") if isinstance(learning, Mapping) else []
    return {
        "schema_version": 1,
        "project_name": _safe_str(status.get("project_name")) or "Farplane",
        "events": {
            "latest": [_cloud_event(event) for event in latest_events if isinstance(event, Mapping)][-10:],
        },
        "learning": {
            "latest_runs": [_cloud_learning_run(run) for run in latest_runs if isinstance(run, Mapping)][:10],
        },
    }


def _human(status: Mapping[str, object]) -> str:
    events = status.get("events") if isinstance(status.get("events"), Mapping) else {}
    learning = status.get("learning") if isinstance(status.get("learning"), Mapping) else {}
    lines = [
        f"Farplane telemetry for {status.get('project_name')}",
        f"Events: {events.get('total', 0)} total",
        f"Learning: {learning.get('run_count', 0)} runs across {learning.get('window_count', 0)} windows",
    ]
    latest_runs = learning.get("latest_runs")
    if isinstance(latest_runs, list) and latest_runs:
        lines.append("Latest learning suggestions:")
        for run in latest_runs[:5]:
            if isinstance(run, Mapping):
                lines.append(f"- [{run.get('status')}] {run.get('candidate_title')} ({run.get('recommended_owner')})")
    return "\n".join(lines)


def post_status(status: Mapping[str, object], *, token: str, url: str, timeout: float = 5.0) -> tuple[bool, str]:
    if not url.strip():
        return False, "missing URL"
    if not token.strip():
        return False, "missing token"

    data = json.dumps(build_cloud_payload(status)).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    req = request.Request(url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return 200 <= response.status < 300, body
    except (error.URLError, TimeoutError, OSError) as exc:
        return False, str(exc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize Farplane hook telemetry and learning reviews.")
    parser.add_argument("--project-root", default=".", help="Farplane project root to inspect.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--post", action="store_true", help="POST the summary to the Farplane telemetry endpoint.")
    parser.add_argument("--url", default=os.environ.get("FARPLANE_TELEMETRY_API_URL", ""), help="Telemetry endpoint URL.")
    parser.add_argument(
        "--token",
        default=os.environ.get("FARPLANE_TELEMETRY_API_TOKEN", ""),
        help="Telemetry bearer token or Farplane Console ingest key.",
    )
    args = parser.parse_args(argv)

    status = build_status(Path(args.project_root))
    if args.post:
        ok, body = post_status(status, token=args.token, url=args.url)
        print(json.dumps({"ok": ok, "response": body}, indent=2, sort_keys=True))
        return 0 if ok else 1
    if args.json:
        print(json.dumps(status, indent=2, sort_keys=True))
    else:
        print(_human(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
