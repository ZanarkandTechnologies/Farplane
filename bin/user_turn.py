from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping


TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")
INTENT_MODES = {"planning", "building", "documenting", "question", "backlog", "unknown"}
CLAIM_PHASES = {"planning", "building", "documenting"}
CLAIM_STATUSES = {
    "pending",
    "running",
    "waiting_for_judge",
    "waiting_for_worker",
    "blocked",
    "complete",
    "failed",
    "cancelled",
}
REQUESTED_OUTCOMES = {
    "ticket_plan",
    "code_change",
    "docs_update",
    "review_or_analysis",
    "answer_only",
    "unknown",
}
HARD_CONSTRAINTS = {
    "ticket_local_only",
    "no_edits",
    "source_required",
    "specific_ticket_required",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def discover_project_root(start: Path | None) -> Path | None:
    if start is None:
        return None
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".ralph").exists() or (candidate / "tickets").exists():
            return candidate
    return None


def project_root_from_payload(payload: Mapping[str, object]) -> Path | None:
    for key in ("cwd", "workdir", "current_working_directory"):
        raw = payload.get(key)
        if isinstance(raw, str) and raw.strip():
            candidate = discover_project_root(Path(raw).expanduser())
            if candidate is not None:
                return candidate
    return discover_project_root(Path.cwd())


def current_run_state_path(project_root: Path) -> Path:
    return project_root / ".ralph" / "state" / "current-run.json"


def session_state_dir(project_root: Path) -> Path:
    return project_root / ".ralph" / "state" / "sessions"


def normalize_session_id(raw: str | None) -> str:
    if not isinstance(raw, str):
        return ""
    return raw.strip()


def session_state_filename(session_id: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", session_id.strip())
    sanitized = sanitized.strip("._") or "session"
    return f"{sanitized}.json"


def session_state_path(project_root: Path, session_id: str) -> Path:
    return session_state_dir(project_root) / session_state_filename(session_id)


def load_json_dict(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def resolve_runtime_path(project_root: Path, raw: str) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_absolute():
        return candidate
    return (project_root / candidate).resolve()


def current_session_id(payload: Mapping[str, object] | None) -> str:
    if payload is None:
        return ""
    direct = payload.get("session_id")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    claim = payload.get("claim")
    if isinstance(claim, Mapping):
        nested = claim.get("session_id")
        if isinstance(nested, str) and nested.strip():
            return nested.strip()
    return ""


def explicit_run_state_selector(payload: Mapping[str, object] | None = None) -> str:
    if payload is not None:
        for key in ("run_state", "ralph_run_state"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    raw = os.environ.get("RALPH_RUN_STATE", "").strip()
    if raw:
        return raw
    return ""


def _with_runtime_metadata(
    payload: dict[str, object],
    *,
    session_id: str = "",
    explicit_run_state: str = "",
) -> dict[str, object]:
    merged = dict(payload)
    if explicit_run_state and "run_state" not in merged:
        merged["run_state"] = explicit_run_state
    if session_id and "session_id" not in merged:
        merged["session_id"] = session_id
    return merged


def _matches_session(payload: Mapping[str, object] | None, session_id: str) -> bool:
    if not session_id:
        return True
    return current_session_id(payload) == session_id


def load_current_run(
    project_root: Path,
    *,
    session_id: str | None = None,
    explicit_run_state: str | None = None,
) -> dict[str, object] | None:
    normalized_session_id = normalize_session_id(session_id)
    selected_run_state = explicit_run_state.strip() if isinstance(explicit_run_state, str) else ""

    if selected_run_state:
        payload = load_json_dict(resolve_runtime_path(project_root, selected_run_state))
        return (
            _with_runtime_metadata(
                payload,
                session_id=normalized_session_id,
                explicit_run_state=selected_run_state,
            )
            if payload
            else None
        )

    if normalized_session_id:
        payload = load_json_dict(session_state_path(project_root, normalized_session_id))
        if payload:
            return _with_runtime_metadata(payload, session_id=normalized_session_id)

    current_payload = load_json_dict(current_run_state_path(project_root))
    if not current_payload:
        return None

    current_with_metadata = _with_runtime_metadata(current_payload, session_id=normalized_session_id)
    if _matches_session(current_with_metadata, normalized_session_id):
        return current_with_metadata

    run_state = current_payload.get("run_state")
    if isinstance(run_state, str) and run_state.strip():
        nested = load_json_dict(resolve_runtime_path(project_root, run_state))
        if nested and _matches_session(nested, normalized_session_id):
            return _with_runtime_metadata(nested, session_id=normalized_session_id, explicit_run_state=run_state.strip())

    return None


def build_runtime_claim(payload: Mapping[str, object]) -> dict[str, object] | None:
    existing_claim = payload.get("claim")

    def claim_value(key: str) -> str:
        direct = payload.get(key)
        if isinstance(direct, str) and direct.strip():
            return direct.strip()
        if isinstance(existing_claim, Mapping):
            nested = existing_claim.get(key)
            if isinstance(nested, str) and nested.strip():
                return nested.strip()
        return ""

    ticket_id = claim_value("ticket_id")
    run_id = claim_value("run_id")
    if not ticket_id or not run_id:
        return None

    claimed_at = claim_value("claimed_at")
    if not claimed_at:
        claimed_at = str(payload.get("updated_at") or "").strip() or now_iso()

    phase = claim_value("phase")
    status = claim_value("status")
    claim: dict[str, object] = {
        "ticket_id": ticket_id,
        "run_id": run_id,
        "claimed_at": claimed_at,
        "phase": phase if phase in CLAIM_PHASES else "building",
        "status": status if status in CLAIM_STATUSES else "running",
    }

    for key in (
        "ticket_path",
        "skill_name",
        "compute_class",
        "executor_target",
        "worker_name",
        "main_artifact_path",
        "grounding_summary",
        "worker_started_at",
        "last_checkpoint_at",
        "checkpoint_summary",
        "session_id",
        "tmux_session",
        "tmux_window",
        "tmux_pane",
    ):
        value = claim_value(key)
        if value:
            claim[key] = value

    return claim


def persist_runtime_update(
    project_root: Path,
    current_run: dict[str, object],
    updates: dict[str, object],
) -> dict[str, object]:
    merged_current = dict(current_run)
    merged_current.update(updates)
    merged_current["updated_at"] = str(updates.get("updated_at") or now_iso())
    claim = build_runtime_claim(merged_current)
    if claim is not None:
        merged_current["claim"] = claim

    current_session = current_session_id(merged_current)
    if current_session:
        merged_current["session_id"] = current_session

    write_json(current_run_state_path(project_root), merged_current)

    if current_session:
        write_json(session_state_path(project_root, current_session), merged_current)

    run_state = merged_current.get("run_state")
    if isinstance(run_state, str) and run_state.strip():
        run_state_path = resolve_runtime_path(project_root, run_state)
        existing_run_state = load_json_dict(run_state_path)
        for key in (
            "schema_version",
            "run_id",
            "ticket_id",
            "ticket_path",
            "phase",
            "status",
            "attempt",
            "skill_name",
            "compute_class",
            "parallel_slots_reserved",
            "executor_target",
            "worker_name",
            "main_artifact_path",
            "grounding_summary",
            "worker_started_at",
            "last_checkpoint_at",
            "checkpoint_summary",
            "session_id",
            "tmux_session",
            "tmux_window",
            "tmux_pane",
            "auto_continue",
            "next_phase",
        ):
            value = merged_current.get(key)
            if value is not None:
                existing_run_state[key] = value
        existing_run_state.update(updates)
        existing_run_state["updated_at"] = merged_current["updated_at"]
        claim = build_runtime_claim(existing_run_state) or build_runtime_claim(merged_current)
        if claim is not None:
            existing_run_state["claim"] = claim
        write_json(run_state_path, existing_run_state)

    return merged_current


def extract_ticket_id(text: str) -> str | None:
    match = TICKET_ID_PATTERN.search(text)
    return match.group(0) if match else None


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def classify_intent_mode(raw_text: str) -> str:
    lowered = raw_text.lower()

    if _contains_any(
        lowered,
        (
            "$impl",
            "implement",
            "implementation",
            "build it",
            "build this",
            "fix ",
            "patch ",
            "code change",
            "continue working",
            "work on ",
            "ship ",
        ),
    ):
        return "building"

    if _contains_any(
        lowered,
        (
            "docs-closeout",
            "documenting",
            "close out",
            "closeout",
            "archive ",
            "write back docs",
            "update docs",
            "docs update",
        ),
    ):
        return "documenting"

    if _contains_any(
        lowered,
        (
            "$impl-plan",
            "impl-plan",
            "impl plan",
            "plan ready",
            "ticket plan",
            "planning pass",
            "write the plan",
            "plan this",
            "execution plan",
        ),
    ):
        return "planning"

    if _contains_any(
        lowered,
        (
            "backlog",
            "queue this",
            "create ticket",
            "new ticket",
            "defer ",
            "spec-to-ticket",
        ),
    ):
        return "backlog"

    if "?" in raw_text or _contains_any(
        lowered,
        (
            "explain",
            "what ",
            "why ",
            "how ",
            "review ",
            "analyze ",
            "look into",
            "investigate",
        ),
    ):
        return "question"

    return "unknown"


def classify_requested_outcome(raw_text: str, intent_mode: str) -> str:
    lowered = raw_text.lower()

    if intent_mode == "documenting" or _contains_any(
        lowered,
        ("history.md", "memory.md", "troubles.md", "readme", "docs update", "document "),
    ):
        return "docs_update"

    if intent_mode == "planning":
        return "ticket_plan"

    if intent_mode == "building":
        return "code_change"

    if _contains_any(lowered, ("review", "analyze", "audit", "investigate", "look into")):
        return "review_or_analysis"

    if intent_mode == "question":
        return "answer_only"

    if intent_mode == "backlog":
        return "review_or_analysis"

    return "unknown"


def classify_hard_constraints(raw_text: str, explicit_ticket_id: str | None) -> list[str]:
    lowered = raw_text.lower()
    constraints: list[str] = []

    if _contains_any(
        lowered,
        (
            "no edits",
            "do not edit",
            "don't edit",
            "without editing",
            "read-only",
            "just explain",
            "answer only",
        ),
    ):
        constraints.append("no_edits")

    if _contains_any(
        lowered,
        (
            "cite",
            "citations",
            "sources",
            "source required",
            "link to",
            "browse",
            "look it up",
            "verify",
        ),
    ):
        constraints.append("source_required")

    if explicit_ticket_id:
        constraints.append("specific_ticket_required")
        if _contains_any(
            lowered,
            (
                "$impl",
                "continue working",
                "work on this ticket",
                "ticket-local",
                "this ticket",
            ),
        ):
            constraints.append("ticket_local_only")

    return [item for item in constraints if item in HARD_CONSTRAINTS]


def normalize_user_turn(
    raw_text: str,
    *,
    turn_id: str | None,
    source: str,
    captured_at: str | None = None,
) -> dict[str, object]:
    raw_text = raw_text.strip()
    captured_at_value = captured_at or now_iso()
    explicit_ticket_id = extract_ticket_id(raw_text)
    intent_mode = classify_intent_mode(raw_text)
    requested_outcome = classify_requested_outcome(raw_text, intent_mode)
    hard_constraints = classify_hard_constraints(raw_text, explicit_ticket_id)
    ticket_part = explicit_ticket_id or "no-ticket"
    constraints_part = ",".join(hard_constraints) if hard_constraints else "none"
    summary = f"{intent_mode} {requested_outcome} {ticket_part} constraints={constraints_part}"
    return {
        "turn_id": turn_id or f"turn-{captured_at_value}",
        "captured_at": captured_at_value,
        "source": source,
        "raw_text": raw_text,
        "intent_mode": intent_mode if intent_mode in INTENT_MODES else "unknown",
        "requested_outcome": requested_outcome if requested_outcome in REQUESTED_OUTCOMES else "unknown",
        "explicit_ticket_id": explicit_ticket_id or "",
        "hard_constraints": hard_constraints,
        "summary": summary,
    }


def capture_user_turn(
    *,
    project_root: Path,
    raw_text: str,
    turn_id: str | None,
    source: str,
    session_id: str | None = None,
    explicit_run_state: str | None = None,
    captured_at: str | None = None,
    only_if_missing: bool = False,
) -> dict[str, object] | None:
    current_run = load_current_run(
        project_root,
        session_id=session_id,
        explicit_run_state=explicit_run_state,
    )
    if current_run is None:
        return None

    existing = current_run.get("last_user_turn")
    if only_if_missing and isinstance(existing, dict) and existing:
        return existing

    last_user_turn = normalize_user_turn(
        raw_text,
        turn_id=turn_id,
        source=source,
        captured_at=captured_at,
    )
    persist_runtime_update(
        project_root,
        current_run,
        {
            "last_user_turn": last_user_turn,
            "updated_at": str(last_user_turn["captured_at"]),
        },
    )
    return last_user_turn


def load_last_user_turn(
    project_root: Path,
    current_run: dict[str, object] | None = None,
) -> dict[str, object] | None:
    current_payload = current_run or load_current_run(project_root)
    if current_payload is None:
        return None

    last_user_turn = current_payload.get("last_user_turn")
    if isinstance(last_user_turn, dict) and last_user_turn:
        return last_user_turn

    run_state = current_payload.get("run_state")
    if isinstance(run_state, str) and run_state.strip():
        run_state_payload = load_json_dict(resolve_runtime_path(project_root, run_state))
        nested = run_state_payload.get("last_user_turn")
        if isinstance(nested, dict) and nested:
            return nested

    return None


def load_runtime_claim(
    project_root: Path,
    current_run: dict[str, object] | None = None,
) -> dict[str, object] | None:
    current_payload = current_run or load_current_run(project_root)
    if current_payload is None:
        return None

    claim = current_payload.get("claim")
    if isinstance(claim, dict) and claim:
        return claim

    run_state = current_payload.get("run_state")
    if isinstance(run_state, str) and run_state.strip():
        run_state_payload = load_json_dict(resolve_runtime_path(project_root, run_state))
        nested = run_state_payload.get("claim")
        if isinstance(nested, dict) and nested:
            return nested
        derived_run_state = build_runtime_claim(run_state_payload)
        if derived_run_state is not None:
            return derived_run_state

    return build_runtime_claim(current_payload)
