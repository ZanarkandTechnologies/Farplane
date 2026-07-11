from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping


TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")
CONTROL_SURFACE_PATTERN = re.compile(
    r"(?<!\S)\$(?P<skill>brainstorm|deep-interview|impl-plan|goal-advisor|qa|demo|close-ticket)(?=$|[\s.,:;!?()\[\]{}\"'`])",
    re.IGNORECASE,
)
CONTROL_SURFACE_ALIASES: dict[str, str] = {}
RETIRED_DOCS_CLOSEOUT_ALIAS_PATTERN = re.compile(
    r"(?<!\S)\$docs-closeout(?=$|[\s.,:;!?()\[\]{}\"'`])",
    re.IGNORECASE,
)
APPROVAL_REVIEW_PROMPT_PREFIX = (
    "The following is the Codex agent history whose request action you are assessing."
)
DELEGATED_LANE_PROMPT_PATTERN = re.compile(
    r"^TASK-\d{4}\s+(?:review|reviewer|qa(?:/evidence| evidence)?)\s+lane[.,]",
    re.IGNORECASE,
)
DELEGATED_REVIEW_PROMPT_PATTERN = re.compile(r"^(?:Review|QA-check)\s+TASK-\d{4}\b")
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
    "qa_pass",
    "demo_pass",
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
SESSION_ORIGINS = {"control", "internal", "non_owning"}
EXECUTION_PHASES = {"build", "qa", "demo"}
TICKET_PATH_ID_PATTERN = re.compile(r"(TASK-\d{4}|TKT-[0-9A-Za-z-]+)")
SELF_IMPROVEMENT_WINDOW_SCHEMA_VERSION = 1


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def discover_project_root(start: Path | None) -> Path | None:
    if start is None:
        return None
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".farplane").exists() or (candidate / "tickets").exists():
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


def runtime_dir(project_root: Path) -> Path:
    return project_root / ".farplane"


def normalize_session_id(raw: str | None) -> str:
    if not isinstance(raw, str):
        return ""
    return raw.strip()


def session_json_filename(session_id: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", session_id.strip())
    sanitized = sanitized.strip("._") or "session"
    return f"{sanitized}.json"


def self_improvement_state_dir(project_root: Path) -> Path:
    return runtime_dir(project_root) / "state"


def conversation_window_dir(project_root: Path) -> Path:
    return runtime_dir(project_root) / "state" / "message-windows"


def skill_opportunity_application_dir(project_root: Path) -> Path:
    return runtime_dir(project_root) / "state" / "learning-reviews"


def ensure_self_improvement_state_setup(project_root: Path) -> None:
    conversation_window_dir(project_root).mkdir(parents=True, exist_ok=True)
    skill_opportunity_application_dir(project_root).mkdir(parents=True, exist_ok=True)


def conversation_window_path(project_root: Path, session_id: str) -> Path:
    return conversation_window_dir(project_root) / session_json_filename(session_id)


def load_json_dict(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def configured_positive_int(raw: str | None, default: int, *, minimum: int = 1) -> int:
    if not isinstance(raw, str) or not raw.strip():
        return default
    try:
        value = int(raw.strip())
    except ValueError:
        return default
    return value if value >= minimum else default


def max_conversation_exchanges() -> int:
    return configured_positive_int(os.environ.get("FARPLANE_SKILL_OPPORTUNITY_MAX_EXCHANGES"), 10)


def load_conversation_window(project_root: Path, session_id: str) -> dict[str, object]:
    normalized_session_id = normalize_session_id(session_id)
    ensure_self_improvement_state_setup(project_root)
    payload = load_json_dict(conversation_window_path(project_root, normalized_session_id))
    if not payload:
        return {
            "schema_version": SELF_IMPROVEMENT_WINDOW_SCHEMA_VERSION,
            "session_id": normalized_session_id,
            "turn_count": 0,
            "last_review_turn_count": 0,
            "last_review_at": "",
            "last_review_run_path": "",
            "rolling_exchanges": [],
            "pending_user_turn": {},
            "updated_at": "",
        }
    payload["schema_version"] = SELF_IMPROVEMENT_WINDOW_SCHEMA_VERSION
    payload["session_id"] = normalized_session_id
    payload.setdefault("turn_count", 0)
    payload.setdefault("last_review_turn_count", 0)
    payload.setdefault("last_review_at", "")
    payload.setdefault("last_review_run_path", "")
    payload.setdefault("rolling_exchanges", [])
    payload.setdefault("pending_user_turn", {})
    payload.setdefault("updated_at", "")
    return payload


def normalized_window_int(window: Mapping[str, object], key: str) -> int:
    value = window.get(key)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return int(value.strip())
        except ValueError:
            return 0
    return 0


def rolling_exchanges_from_window(window: Mapping[str, object]) -> list[dict[str, object]]:
    raw = window.get("rolling_exchanges")
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def recent_conversation_windows(
    project_root: Path,
    *,
    current_session_id: str,
    limit: int = 5,
) -> list[dict[str, object]]:
    ensure_self_improvement_state_setup(project_root)
    normalized_current = normalize_session_id(current_session_id)
    windows: list[dict[str, object]] = []
    directory = conversation_window_dir(project_root)
    if directory.exists():
        for path in directory.glob("*.json"):
            payload = load_json_dict(path)
            if not payload:
                continue
            session_id = normalize_session_id(str(payload.get("session_id") or path.stem))
            if not session_id:
                continue
            payload["session_id"] = session_id
            payload.setdefault("updated_at", "")
            payload.setdefault("rolling_exchanges", [])
            payload.setdefault("pending_user_turn", {})
            windows.append(payload)

    windows.sort(
        key=lambda item: (
            normalize_session_id(str(item.get("session_id") or "")) == normalized_current,
            str(item.get("updated_at") or ""),
        ),
        reverse=True,
    )
    return windows[: max(limit, 1)]


def trim_conversation_window(window: dict[str, object], *, max_exchanges: int | None = None) -> dict[str, object]:
    limit = max_exchanges if isinstance(max_exchanges, int) and max_exchanges > 0 else max_conversation_exchanges()
    exchanges = rolling_exchanges_from_window(window)
    window["rolling_exchanges"] = exchanges[-limit:]
    return window


def promote_pending_conversation_exchange(
    window: dict[str, object],
    *,
    assistant_text: str = "",
    assistant_captured_at: str = "",
    assistant_source: str = "",
) -> dict[str, object]:
    pending = window.get("pending_user_turn")
    if not isinstance(pending, Mapping) or not pending:
        return window
    exchange = dict(pending)
    exchange["assistant_captured_at"] = assistant_captured_at
    exchange["assistant_text"] = assistant_text
    exchange["assistant_source"] = assistant_source
    exchanges = rolling_exchanges_from_window(window)
    exchanges.append(exchange)
    window["rolling_exchanges"] = exchanges
    window["pending_user_turn"] = {}
    return trim_conversation_window(window)


def append_conversation_user_turn(
    project_root: Path,
    session_id: str,
    last_user_turn: Mapping[str, object],
) -> dict[str, object]:
    normalized_session_id = normalize_session_id(session_id)
    if not normalized_session_id:
        return {}
    captured_at = str(last_user_turn.get("captured_at") or now_iso())
    window = load_conversation_window(project_root, normalized_session_id)
    window = promote_pending_conversation_exchange(
        window,
        assistant_source="missing_stop_before_next_user_turn",
    )
    turn_count = normalized_window_int(window, "turn_count") + 1
    turn_id = str(last_user_turn.get("turn_id") or f"turn-{captured_at}").strip()
    window["turn_count"] = turn_count
    window["pending_user_turn"] = {
        "exchange_id": f"{normalized_session_id}-{turn_count}",
        "user_turn_id": turn_id,
        "user_captured_at": captured_at,
        "user_text": str(last_user_turn.get("raw_text") or ""),
        "user_summary": str(last_user_turn.get("summary") or ""),
        "intent_mode": str(last_user_turn.get("intent_mode") or ""),
        "control_surface": str(last_user_turn.get("control_surface") or ""),
        "source": str(last_user_turn.get("source") or ""),
        "assistant_captured_at": "",
        "assistant_text": "",
        "assistant_source": "",
    }
    runtime = normalize_runtime_metadata(
        last_user_turn.get("runtime") if isinstance(last_user_turn.get("runtime"), Mapping) else None
    )
    if runtime:
        window["pending_user_turn"]["runtime"] = runtime
        window["runtime"] = runtime
    window["updated_at"] = captured_at
    trim_conversation_window(window)
    write_json(conversation_window_path(project_root, normalized_session_id), window)
    return window


def append_conversation_assistant_response(
    project_root: Path,
    session_id: str,
    response: str,
    *,
    captured_at: str | None = None,
    source: str = "assistant_response_capture",
) -> dict[str, object]:
    normalized_session_id = normalize_session_id(session_id)
    if not normalized_session_id:
        return {}
    captured_at_value = captured_at or now_iso()
    window = load_conversation_window(project_root, normalized_session_id)
    pending = window.get("pending_user_turn")
    if isinstance(pending, Mapping) and pending:
        window = promote_pending_conversation_exchange(
            window,
            assistant_text=response,
            assistant_captured_at=captured_at_value,
            assistant_source=source,
        )
    window["updated_at"] = captured_at_value
    trim_conversation_window(window)
    write_json(conversation_window_path(project_root, normalized_session_id), window)
    return window


def should_review_skill_opportunities(
    window: Mapping[str, object],
    *,
    cadence: int = 10,
) -> dict[str, object]:
    interval = cadence if cadence > 0 else 10
    turn_count = normalized_window_int(window, "turn_count")
    last_review_turn_count = normalized_window_int(window, "last_review_turn_count")
    delta = turn_count - last_review_turn_count
    due = turn_count > 0 and delta >= interval
    reason = (
        f"{delta} captured user turns since last review"
        if due
        else f"{max(delta, 0)} captured user turns since last review; waiting for {interval}"
    )
    return {
        "due": due,
        "turn_count": turn_count,
        "last_review_turn_count": last_review_turn_count,
        "cadence": interval,
        "reason": reason,
    }


def mark_skill_opportunity_review_launched(
    project_root: Path,
    session_id: str,
    *,
    review_run_path: str,
    reviewed_at: str | None = None,
    current_window: Mapping[str, object] | None = None,
) -> dict[str, object]:
    normalized_session_id = normalize_session_id(session_id)
    if not normalized_session_id:
        return {}
    reviewed_at_value = reviewed_at or now_iso()
    window = dict(current_window) if isinstance(current_window, Mapping) else load_conversation_window(project_root, normalized_session_id)
    window["last_review_turn_count"] = normalized_window_int(window, "turn_count")
    window["last_review_at"] = reviewed_at_value
    window["last_review_run_path"] = review_run_path
    window["updated_at"] = reviewed_at_value
    write_json(conversation_window_path(project_root, normalized_session_id), window)
    return window


def read_ticket_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def tickets_dir(project_root: Path) -> Path:
    return project_root / "tickets"


def ticket_id_from_path(path: Path) -> str:
    for candidate in (path.parent.name, path.stem, path.name):
        match = TICKET_PATH_ID_PATTERN.search(candidate)
        if match:
            return match.group(1)
    return ""


def canonical_active_ticket_path(project_root: Path, ticket_id: str) -> Path:
    return tickets_dir(project_root) / ticket_id / "ticket.md"


def canonical_archive_ticket_path(project_root: Path, ticket_id: str) -> Path:
    return tickets_dir(project_root) / "archive" / ticket_id / "ticket.md"


def ticket_path_candidates(project_root: Path, ticket_id: str) -> list[Path]:
    candidates: list[Path] = []
    for path in (
        canonical_active_ticket_path(project_root, ticket_id),
        canonical_archive_ticket_path(project_root, ticket_id),
    ):
        if path not in candidates:
            candidates.append(path)
    return candidates


def resolve_ticket_path_by_id(
    project_root: Path,
    ticket_id: str,
    *,
    prefer_archive: bool = False,
) -> Path | None:
    if not ticket_id.strip():
        return None
    candidates = ticket_path_candidates(project_root, ticket_id.strip())
    if prefer_archive:
        candidates = sorted(
            candidates,
            key=lambda path: (
                0 if path.parent.name == ticket_id.strip() and path.parent.parent.name == "archive" else 1,
                str(path),
            ),
        )
    for path in candidates:
        if path.is_file():
            return path
    return None


def iter_active_ticket_files(project_root: Path) -> list[Path]:
    ticket_root = tickets_dir(project_root)
    directory_tickets = sorted(
        path
        for path in ticket_root.glob("TASK-*/ticket.md")
        if path.is_file()
    )
    return directory_tickets


def ticket_artifact_root(project_root: Path, ticket_path: Path, ticket_id: str = "") -> Path:
    resolved_ticket_id = ticket_id.strip() or ticket_id_from_path(ticket_path)
    if ticket_path.name == "ticket.md" and ticket_path.parent.name.startswith("TASK-"):
        return ticket_path.parent / "artifacts"
    return tickets_dir(project_root) / "artifacts" / resolved_ticket_id


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None
    return parts[0][4:], parts[1]


def update_frontmatter_field(raw_frontmatter: str, key: str, value: str, *, after_key: str | None = None) -> str:
    lines = raw_frontmatter.splitlines()
    key_prefix = f"{key}:"
    replacement = f"{key}: {value}"
    for index, line in enumerate(lines):
        if line.startswith(key_prefix):
            lines[index] = replacement
            return "\n".join(lines)

    insert_at = len(lines)
    if after_key:
        after_prefix = f"{after_key}:"
        for index, line in enumerate(lines):
            if line.startswith(after_prefix):
                insert_at = index + 1
                break
    lines.insert(insert_at, replacement)
    return "\n".join(lines)


def clear_frontmatter_field(raw_frontmatter: str, key: str) -> str:
    key_prefix = f"{key}:"
    lines = [line for line in raw_frontmatter.splitlines() if not line.startswith(key_prefix)]
    return "\n".join(lines)


def write_ticket_text(path: Path, raw_frontmatter: str, body: str) -> None:
    path.write_text(f"---\n{raw_frontmatter}\n---\n{body}", encoding="utf-8")


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
        value = payload.get("run_state")
        if isinstance(value, str) and value.strip():
            return value.strip()
    raw = os.environ.get("FARPLANE_RUN_STATE", "").strip()
    if raw:
        return raw
    return ""


def normalize_session_origin(raw: object) -> str:
    if not isinstance(raw, str):
        return ""
    normalized = raw.strip().lower()
    return normalized if normalized in SESSION_ORIGINS else ""


def extract_control_surface(raw_text: str) -> str:
    match = CONTROL_SURFACE_PATTERN.search(raw_text)
    if not match:
        return ""
    matched = str(match.group("skill") or "").strip().lower()
    return CONTROL_SURFACE_ALIASES.get(matched, matched)


def extract_control_surfaces(raw_text: str) -> list[str]:
    surfaces: list[str] = []
    for match in CONTROL_SURFACE_PATTERN.finditer(raw_text):
        matched = str(match.group("skill") or "").strip().lower()
        normalized = CONTROL_SURFACE_ALIASES.get(matched, matched)
        if normalized and normalized not in surfaces:
            surfaces.append(normalized)
    return surfaces


def extract_skill_mentions(raw_text: str) -> list[str]:
    return extract_control_surfaces(raw_text)


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
        "execution_phase",
        "compute_class",
        "executor_target",
        "session_name",
        "current_ticket_id",
        "worker_name",
        "main_artifact_path",
        "grounding_summary",
        "worker_started_at",
        "last_checkpoint_at",
        "checkpoint_summary",
        "session_id",
    ):
        value = claim_value(key)
        if value:
            claim[key] = value
    for key in ("requires_qa", "requires_demo"):
        value = payload.get(key)
        if isinstance(value, bool):
            claim[key] = value
    for key in ("phase_requirements",):
        value = payload.get(key)
        if isinstance(value, Mapping) and value:
            claim[key] = dict(value)

    return claim


def ticket_frontmatter_value(text: str, key: str) -> str:
    parts = split_frontmatter(text)
    if parts is None:
        return ""
    raw_frontmatter, _ = parts
    prefix = f"{key}:"
    for line in raw_frontmatter.splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def ticket_frontmatter_bool(text: str, key: str, *, default: bool = False) -> bool:
    value = ticket_frontmatter_value(text, key).strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    return default


def ticket_qa_requirements(text: str) -> tuple[bool, bool]:
    lines = text.splitlines()
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == "## QA Strategy") + 1
    except StopIteration:
        return False, False
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    strategy = "\n".join(lines[start:end]).lower()
    requires_demo = "proof_weight: demo" in strategy or "- demo" in strategy
    requires_qa = requires_demo or any(
        token in strategy
        for token in ("proof_weight: qa", "proof_weight: visual_qa", "proof_weight: agent_qa", "qa-tester")
    )
    return requires_qa, requires_demo


def build_phase_requirements(project_root: Path, ticket_id: str, *, requires_qa: bool, requires_demo: bool) -> dict[str, object]:
    artifact_root = canonical_active_ticket_path(project_root, ticket_id).parent / "artifacts"
    requirements: dict[str, object] = {
        "build": {
            "completion_statuses": ["build_complete", "done"],
            "artifact_root": str(artifact_root),
        }
    }
    if requires_qa:
        requirements["qa"] = {
            "artifact_root": str(artifact_root / "qa"),
            "result_glob": "**/result.json",
            "required_verdict": "pass",
        }
    if requires_demo:
        requirements["demo"] = {
            "artifact_root": str(artifact_root / "demo"),
            "result_glob": "**/result.json",
            "required_verdict": "pass",
        }
    return requirements


def load_ticket_execution_contract(project_root: Path, ticket_path: str, *, control_surface: str) -> dict[str, object]:
    ticket_candidate = Path(ticket_path)
    if not ticket_candidate.is_absolute():
        ticket_candidate = (project_root / ticket_path).resolve()
    text = read_ticket_text(ticket_candidate)
    requires_qa, requires_demo = ticket_qa_requirements(text)
    if control_surface == "qa":
        requires_qa = True
    if control_surface == "demo":
        requires_qa = True
        requires_demo = True
    ticket_id = ticket_id_from_path(ticket_candidate) or extract_ticket_id(ticket_candidate.name) or ticket_candidate.stem
    return {
        "requires_qa": requires_qa,
        "requires_demo": requires_demo,
        "phase_requirements": build_phase_requirements(
            project_root,
            ticket_id,
            requires_qa=requires_qa,
            requires_demo=requires_demo,
        ),
    }


def requested_execution_phase(control_surface: str) -> str:
    if control_surface == "goal-advisor":
        return "build"
    if control_surface in EXECUTION_PHASES:
        return control_surface
    return ""


def resolve_ticket_for_impl_seed(project_root: Path, explicit_ticket_id: str) -> tuple[str, str] | None:
    if explicit_ticket_id:
        ticket_path = resolve_ticket_path_by_id(project_root, explicit_ticket_id)
        if ticket_path is not None:
            return (explicit_ticket_id, str(ticket_path))
        return None

    all_tickets = iter_active_ticket_files(project_root)
    if not all_tickets:
        return None

    active_matches: list[Path] = []
    for ticket_path in all_tickets:
        status = ticket_frontmatter_value(read_ticket_text(ticket_path), "status").strip()
        if status in {"review", "building"}:
            active_matches.append(ticket_path)

    candidates = active_matches if len(active_matches) == 1 else all_tickets if len(all_tickets) == 1 else []
    if len(candidates) != 1:
        return None

    ticket_path = candidates[0]
    ticket_id = ticket_id_from_path(ticket_path) or extract_ticket_id(ticket_path.name) or ticket_path.stem
    return ticket_id, str(ticket_path)


def extract_ticket_id(text: str) -> str | None:
    match = TICKET_ID_PATTERN.search(text)
    return match.group(0) if match else None


def has_explicit_goal_execution_invocation(text: str) -> bool:
    return extract_control_surface(text) == "goal-advisor"


def infer_session_origin_from_state(payload: Mapping[str, object] | None) -> tuple[str, str, str]:
    if not isinstance(payload, Mapping):
        return "", "", ""

    stored_origin = normalize_session_origin(payload.get("session_origin"))
    if stored_origin:
        source = str(payload.get("session_origin_source") or "").strip() or "stored_session_origin"
        reason = str(payload.get("session_origin_reason") or "").strip() or f"session origin already marked {stored_origin}"
        return stored_origin, source, reason

    last_user_turn = payload.get("last_user_turn")
    if not isinstance(last_user_turn, Mapping):
        return "", "", ""

    control_surface = str(last_user_turn.get("control_surface") or "").strip().lower()
    if control_surface:
        return "control", "persisted_last_user_turn", f"persisted last_user_turn invoked ${control_surface}"

    raw_text = last_user_turn.get("raw_text")
    if isinstance(raw_text, str) and raw_text.strip():
        if is_internal_user_prompt(raw_text):
            return "internal", "persisted_last_user_turn", "persisted raw_text matches internal prompt signature"
        persisted_control_surface = extract_control_surface(raw_text)
        if persisted_control_surface:
            return "control", "persisted_last_user_turn", f"persisted raw_text invoked ${persisted_control_surface}"

    if bool(last_user_turn.get("explicit_goal_execution_requested")):
        return "control", "persisted_last_user_turn", "persisted explicit goal execution request implies a control session"

    return "", "", ""


def resolve_session_origin(
    raw_text: str,
    *,
    current_run: Mapping[str, object] | None,
    existing_session: Mapping[str, object] | None,
) -> tuple[str, str, str]:
    for payload in (existing_session, current_run):
        inferred_origin, inferred_source, inferred_reason = infer_session_origin_from_state(payload)
        if inferred_origin:
            return inferred_origin, inferred_source, inferred_reason

    if is_internal_user_prompt(raw_text):
        return "internal", "internal_prompt_signature", "prompt matches an internal harness prompt signature"

    control_surface = extract_control_surface(raw_text)
    if control_surface:
        return "control", "first_prompt_control_surface", f"first prompt invoked ${control_surface}"

    return "non_owning", "default_non_owning", "session did not begin with a public control-skill invocation"


def is_internal_user_prompt(raw_text: str) -> bool:
    text = raw_text.strip()
    if not text:
        return False

    lowered = text.lower()
    has_structured_return = "return:" in lowered or "return only:" in lowered
    is_read_only_contract = "do not edit" in lowered or "read-only only." in lowered

    if text.startswith(APPROVAL_REVIEW_PROMPT_PREFIX):
        return True
    if text.startswith("Continue the current live Codex lane."):
        return True
    if text.startswith("Continue the current Codex lane."):
        return True
    if text.startswith("Run the `goal-advisor` skill on ticket "):
        return True
    if text.startswith("Run the `qa` skill on ticket "):
        return True
    if text.startswith("Run the `demo` skill on ticket "):
        return True
    if DELEGATED_LANE_PROMPT_PATTERN.match(text):
        return True
    if DELEGATED_REVIEW_PROMPT_PATTERN.match(text) and has_structured_return and is_read_only_contract:
        return True
    if lowered.startswith("use agent-browser") and has_structured_return and is_read_only_contract:
        return True

    return False


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def classify_intent_mode(raw_text: str) -> str:
    lowered = RETIRED_DOCS_CLOSEOUT_ALIAS_PATTERN.sub("", raw_text).lower()
    control_surface = extract_control_surface(raw_text)

    if control_surface == "impl-plan":
        return "planning"

    if control_surface == "goal-advisor":
        return "building"

    if control_surface == "qa":
        return "building"

    if control_surface == "demo":
        return "building"

    if control_surface == "close-ticket":
        return "documenting"

    if _contains_any(
        lowered,
        (
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
    lowered = RETIRED_DOCS_CLOSEOUT_ALIAS_PATTERN.sub("", raw_text).lower()

    if intent_mode == "documenting" or _contains_any(
        lowered,
        ("history.md", "memory.md", "troubles.md", "lessons.md", "readme", "docs update", "document "),
    ):
        return "docs_update"

    control_surface = extract_control_surface(raw_text)
    if control_surface == "qa":
        return "qa_pass"
    if control_surface == "demo":
        return "demo_pass"

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
                "$goal-advisor",
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
    runtime: Mapping[str, object] | None = None,
) -> dict[str, object]:
    raw_text = raw_text.strip()
    captured_at_value = captured_at or now_iso()
    explicit_ticket_id = extract_ticket_id(raw_text)
    control_surface = extract_control_surface(raw_text)
    execution_phase = requested_execution_phase(control_surface)
    explicit_goal_execution_requested = has_explicit_goal_execution_invocation(raw_text)
    intent_mode = classify_intent_mode(raw_text)
    requested_outcome = classify_requested_outcome(raw_text, intent_mode)
    hard_constraints = classify_hard_constraints(raw_text, explicit_ticket_id)
    ticket_part = explicit_ticket_id or "no-ticket"
    constraints_part = ",".join(hard_constraints) if hard_constraints else "none"
    summary = f"{intent_mode} {requested_outcome} {ticket_part} constraints={constraints_part}"
    row: dict[str, object] = {
        "turn_id": turn_id or f"turn-{captured_at_value}",
        "captured_at": captured_at_value,
        "source": source,
        "raw_text": raw_text,
        "intent_mode": intent_mode if intent_mode in INTENT_MODES else "unknown",
        "requested_outcome": requested_outcome if requested_outcome in REQUESTED_OUTCOMES else "unknown",
        "explicit_ticket_id": explicit_ticket_id or "",
        "control_surface": control_surface,
        "requested_execution_phase": execution_phase,
        "explicit_goal_execution_requested": explicit_goal_execution_requested,
        "hard_constraints": hard_constraints,
        "summary": summary,
    }
    normalized_runtime = normalize_runtime_metadata(runtime)
    if normalized_runtime:
        row["runtime"] = normalized_runtime
    return row


def normalize_runtime_metadata(runtime: Mapping[str, object] | None) -> dict[str, object]:
    if not isinstance(runtime, Mapping):
        return {}
    kind = str(runtime.get("kind") or "").strip().lower()
    if kind not in {"interactive", "headless", "ephemeral", "automation"}:
        kind = ""
    purpose = str(runtime.get("purpose") or "").strip().lower()
    if purpose and not re.match(r"^[a-z0-9_.:-]{1,80}$", purpose):
        purpose = ""
    source = str(runtime.get("source") or "").strip().lower()
    if source and not re.match(r"^[a-z0-9_.:-]{1,80}$", source):
        source = ""
    output: dict[str, object] = {}
    if kind:
        output["kind"] = kind
    if purpose:
        output["purpose"] = purpose
    if source:
        output["source"] = source
    return output


def runtime_metadata_from_payload(payload: Mapping[str, object], raw_text: str = "") -> dict[str, object]:
    env_kind = str(os.environ.get("FARPLANE_CODEX_RUNTIME_KIND") or "").strip().lower()
    env_purpose = str(os.environ.get("FARPLANE_CODEX_RUNTIME_PURPOSE") or "").strip().lower()
    payload_kind = str(payload.get("runtime_kind") or payload.get("codex_runtime_kind") or "").strip().lower()
    payload_purpose = str(payload.get("runtime_purpose") or payload.get("codex_runtime_purpose") or "").strip().lower()
    is_eval_like = bool(
        re.search(
            r"(^|\n)\s*You are judging an agent answer(?:\s+for\s+(?:a\s+)?harness eval)?\b|\b(harness eval|run_evals\.py|\.farplane/evals)\b",
            raw_text,
            re.IGNORECASE,
        )
    )
    kind = env_kind or payload_kind
    purpose = env_purpose or payload_purpose
    if not kind and is_eval_like:
        kind = "ephemeral"
    if not purpose and is_eval_like:
        purpose = "eval"
    return normalize_runtime_metadata({"kind": kind, "purpose": purpose, "source": "hook_payload"})


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
    runtime: Mapping[str, object] | None = None,
) -> dict[str, object] | None:
    captured_at_value = captured_at or now_iso()
    session_origin, _session_origin_source, _session_origin_reason = resolve_session_origin(
        raw_text,
        current_run=None,
        existing_session={},
    )
    if session_origin != "control":
        return None

    last_user_turn = normalize_user_turn(
        raw_text,
        turn_id=turn_id,
        source=source,
        captured_at=captured_at_value,
        runtime=runtime,
    )
    return last_user_turn
