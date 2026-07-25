#!/usr/bin/env python3
"""Atomically guard one Work Pulse planning wave and record its outcome."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FINAL_OUTCOMES = {"completed", "no_op", "source_gap", "human_request"}
SERIALIZATION_TIME_KEYS = {"as_of", "serialized_at"}
SERIALIZATION_COUNTER_KEYS = {"unanswered_pulse_turns"}
BOARD_SOURCE_COORDINATE_KEYS = {"ledger", "worker_index"}
BOARD_DIAGNOSTIC_KEYS = {"released_worker_rows"}
SEMANTIC_TIME_FIELDS = {
    "metric_freshness",
    "matured_reward_ids",
    "operator_availability",
}


def canonical_fingerprint(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def is_temporary_json_ref(key: str, value: Any) -> bool:
    if not key.endswith("ref") or not isinstance(value, str):
        return False
    normalized = value.replace("\\", "/")
    return "/.farplane/tmp/" in f"/{normalized.lstrip('/')}" and normalized.endswith(".json")


def normalized_legacy_clock(value: Any) -> str:
    """Canonicalize an old planning clock without weakening time correctness."""

    raw = str(value or "").strip()
    if not raw:
        return "missing"
    candidate = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return raw
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_semantic_time_state(value: Any) -> dict[str, Any]:
    """Validate the derived time boundaries that can change planning."""

    if not isinstance(value, dict):
        raise ValueError("semantic_time_state must be an object")
    missing = sorted(SEMANTIC_TIME_FIELDS.difference(value))
    if missing:
        raise ValueError(
            "semantic_time_state missing required fields: " + ", ".join(missing)
        )
    if not isinstance(value["metric_freshness"], dict):
        raise ValueError("semantic_time_state.metric_freshness must be an object")
    if not isinstance(value["matured_reward_ids"], list):
        raise ValueError("semantic_time_state.matured_reward_ids must be a list")
    if not isinstance(value["operator_availability"], dict):
        raise ValueError("semantic_time_state.operator_availability must be an object")
    return {
        **value,
        "matured_reward_ids": sorted(
            {str(item).strip() for item in value["matured_reward_ids"] if str(item).strip()}
        ),
    }


def semantic_planning_value(
    project_root: Path,
    value: Any,
) -> Any:
    """Remove run-envelope churn while preserving planning evidence changes.

    With explicit ``semantic_time_state``, ``as_of`` and ``serialized_at`` are
    serialization metadata while derived freshness, maturation, and
    availability boundaries remain fingerprinted. Legacy inputs without that
    state retain their canonical top-level ``as_of`` as a safe semantic clock;
    they may replan more often but can never suppress a time transition.
    """

    root = project_root.resolve()
    explicit_time_state = value.get("semantic_time_state") if isinstance(value, dict) else None
    normalized_time_state = (
        normalize_semantic_time_state(explicit_time_state)
        if explicit_time_state is not None
        else None
    )
    legacy_clock = value.get("as_of") if isinstance(value, dict) else None

    def project(item: Any, path: tuple[str, ...] = ()) -> Any:
        if isinstance(item, dict):
            result: dict[str, Any] = {}
            for raw_key, child in item.items():
                key = str(raw_key)
                if key in SERIALIZATION_TIME_KEYS:
                    continue
                if normalized_time_state is not None and key in SERIALIZATION_COUNTER_KEYS:
                    continue
                if key == "semantic_time_state" and normalized_time_state is not None:
                    result[key] = project(normalized_time_state, (*path, key))
                    continue
                if path == ("board",) and key in BOARD_SOURCE_COORDINATE_KEYS:
                    continue
                if path == ("board",) and key in BOARD_DIAGNOSTIC_KEYS:
                    continue
                if is_temporary_json_ref(key, child):
                    ref_path = Path(child)
                    if not ref_path.is_absolute():
                        ref_path = root / ref_path
                    try:
                        loaded = json.loads(ref_path.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        # A missing or malformed input is itself meaningful and
                        # must not silently dedupe with a valid receipt.
                        result[key] = child
                    else:
                        result[f"{key}_content"] = project(loaded, (*path, key))
                    continue
                result[key] = project(child, (*path, key))
            return result
        if isinstance(item, list):
            return [project(child, path) for child in item]
        return item

    projected = project(value)
    if isinstance(projected, dict) and normalized_time_state is None:
        projected["legacy_semantic_clock"] = normalized_legacy_clock(legacy_clock)
    return projected


def semantic_planning_fingerprint(project_root: Path, value: Any) -> str:
    return canonical_fingerprint(semantic_planning_value(project_root, value))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def automation_root(project_root: Path) -> Path:
    return project_root.resolve() / ".farplane" / "automation"


def decision_path(project_root: Path) -> Path:
    return automation_root(project_root) / "decisions.jsonl"


def lock_root(project_root: Path) -> Path:
    return automation_root(project_root) / "plan-next-wave.lock"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def load_claim(project_root: Path) -> dict[str, Any]:
    path = lock_root(project_root) / "claim.json"
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def begin_wave(project_root: Path, planning_input: Any, wave_size: int) -> dict[str, Any]:
    if wave_size < 0:
        raise ValueError("wave_size must be non-negative")
    project_root = project_root.resolve()
    fingerprint = semantic_planning_fingerprint(project_root, planning_input)
    decisions = read_jsonl(decision_path(project_root))
    if any(
        row.get("action") == "plan_next_wave"
        and row.get("planning_fingerprint") == fingerprint
        and row.get("status") in FINAL_OUTCOMES
        for row in reversed(decisions)
    ):
        return {
            "ok": True,
            "status": "no_op_unchanged_input",
            "planning_fingerprint": fingerprint,
            "no_op_category": "unchanged_planning_fingerprint",
        }

    root = lock_root(project_root)
    root.parent.mkdir(parents=True, exist_ok=True)
    try:
        root.mkdir()
    except FileExistsError:
        claim = load_claim(project_root)
        pid = int(claim.get("pid") or 0)
        if pid:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                shutil.rmtree(root)
                return begin_wave(project_root, planning_input, wave_size)
            except PermissionError:
                pass
        return {
            "ok": False,
            "status": "blocked_overlap",
            "planning_fingerprint": fingerprint,
            "blocker_category": "planning_wave_already_claimed",
            "active_claim_id": claim.get("claim_id"),
        }

    claim_id = canonical_fingerprint(
        {"planning_fingerprint": fingerprint, "pid": os.getpid(), "at": now_iso()}
    )
    claim = {
        "schema": "farplane.plan_wave_claim.v1",
        "claim_id": claim_id,
        "planning_fingerprint": fingerprint,
        "wave_size": wave_size,
        "claimed_at": now_iso(),
        "pid": os.getpid(),
    }
    (root / "claim.json").write_text(json.dumps(claim, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_jsonl(
        decision_path(project_root),
        {"action": "plan_next_wave", "status": "claimed", **claim},
    )
    return {"ok": True, "status": "acquired", **claim}


def finish_wave(
    project_root: Path,
    claim_id: str,
    outcome: str,
    admitted: list[str],
    admitted_skills: dict[str, str] | None = None,
    admitted_areas: dict[str, str] | None = None,
    reason: str = "",
) -> dict[str, Any]:
    if outcome not in FINAL_OUTCOMES:
        raise ValueError(f"invalid outcome: {outcome}")
    project_root = project_root.resolve()
    claim = load_claim(project_root)
    if not claim or claim.get("claim_id") != claim_id:
        raise ValueError("claim_id does not own the active planning wave")
    admitted = [ticket_id.strip() for ticket_id in admitted if ticket_id.strip()]
    if len(admitted) != len(set(admitted)):
        raise ValueError("duplicate admitted ticket id in one wave")
    wave_size = int(claim.get("wave_size") or 0)
    if len(admitted) > wave_size:
        raise ValueError(f"admitted count {len(admitted)} exceeds wave_size {wave_size}")
    prior_ids = {
        str(ticket_id)
        for row in read_jsonl(decision_path(project_root))
        for ticket_id in (row.get("admitted") if isinstance(row.get("admitted"), list) else [])
    }
    repeated = sorted(set(admitted).intersection(prior_ids))
    if repeated:
        raise ValueError(f"ticket ids already admitted: {', '.join(repeated)}")
    admitted_skills = {
        str(ticket_id).strip(): str(skill_ref).strip()
        for ticket_id, skill_ref in (admitted_skills or {}).items()
    }
    if set(admitted_skills) != set(admitted):
        raise ValueError("every admitted ticket must have exactly one selected skill_ref")
    if any(not str(skill_ref).strip() for skill_ref in admitted_skills.values()):
        raise ValueError("selected skill_ref cannot be blank")
    admitted_areas = {
        str(ticket_id).strip(): str(area_id).strip()
        for ticket_id, area_id in (admitted_areas or {}).items()
    }
    unexpected_area_ids = sorted(set(admitted_areas).difference(admitted))
    if unexpected_area_ids:
        raise ValueError(
            "area bindings reference non-admitted tickets: "
            + ", ".join(unexpected_area_ids)
        )
    if any(not str(area_id).strip() for area_id in admitted_areas.values()):
        raise ValueError("selected area_id cannot be blank")

    row = {
        "schema": "farplane.plan_wave_decision.v2",
        "action": "plan_next_wave",
        "status": outcome,
        "claim_id": claim_id,
        "planning_fingerprint": claim["planning_fingerprint"],
        "wave_size": wave_size,
        "admitted": admitted,
        "admitted_skill_calls": [
            {
                "ticket_id": ticket_id,
                "skill_ref": admitted_skills[ticket_id],
                **(
                    {"area_id": admitted_areas[ticket_id]}
                    if ticket_id in admitted_areas
                    else {}
                ),
            }
            for ticket_id in admitted
        ],
        "reason": reason,
        "no_op_category": reason if outcome == "no_op" else "",
        "completed_at": now_iso(),
    }
    append_jsonl(decision_path(project_root), row)
    shutil.rmtree(lock_root(project_root))
    return {"ok": True, **row}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    begin = subparsers.add_parser("begin")
    begin.add_argument("--project-root", default=".")
    begin.add_argument("--input", required=True, help="JSON file, or - for stdin")
    begin.add_argument("--wave-size", type=int, required=True)
    finish = subparsers.add_parser("finish")
    finish.add_argument("--project-root", default=".")
    finish.add_argument("--claim-id", required=True)
    finish.add_argument("--outcome", choices=sorted(FINAL_OUTCOMES), required=True)
    finish.add_argument("--admitted", action="append", default=[])
    finish.add_argument(
        "--admitted-skill",
        action="append",
        default=[],
        help="TICKET_ID=SKILL_REF; required once for every admitted ticket",
    )
    finish.add_argument(
        "--admitted-area",
        action="append",
        default=[],
        help="TICKET_ID=AREA_ID; optional passive context for an admitted ticket",
    )
    finish.add_argument("--reason", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "begin":
            raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
            result = begin_wave(Path(args.project_root), json.loads(raw), args.wave_size)
        else:
            admitted_skills = {}
            for raw in args.admitted_skill:
                ticket_id, separator, skill_ref = raw.partition("=")
                ticket_id = ticket_id.strip()
                if not separator or not ticket_id or ticket_id in admitted_skills:
                    raise ValueError(f"invalid or duplicate --admitted-skill: {raw}")
                admitted_skills[ticket_id] = skill_ref.strip()
            admitted_areas = {}
            for raw in args.admitted_area:
                ticket_id, separator, area_id = raw.partition("=")
                ticket_id = ticket_id.strip()
                if not separator or not ticket_id or ticket_id in admitted_areas:
                    raise ValueError(f"invalid or duplicate --admitted-area: {raw}")
                admitted_areas[ticket_id] = area_id.strip()
            result = finish_wave(
                Path(args.project_root), args.claim_id, args.outcome, args.admitted,
                admitted_skills, admitted_areas, args.reason
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 3


if __name__ == "__main__":
    raise SystemExit(main())
