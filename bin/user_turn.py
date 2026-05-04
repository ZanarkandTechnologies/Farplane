from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping


TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")
CONTROL_SURFACE_PATTERN = re.compile(
    r"(?<!\S)\$(?P<skill>brainstorm|deep-interview|impl-plan|impl|qa|demo|loop|ralph|close-ticket|docs-closeout)(?=$|[\s.,:;!?()\[\]{}\"'`])",
    re.IGNORECASE,
)
CONTROL_SURFACE_ALIASES = {
    "docs-closeout": "close-ticket",
}
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
SESSION_ALIAS_POOL = tuple(f"agent-{index:02d}" for index in range(1, 11))
EXECUTION_PHASES = {"impl", "qa", "demo"}
TICKET_PATH_ID_PATTERN = re.compile(r"(TASK-\d{4}|TKT-[0-9A-Za-z-]+)")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def discover_project_root(start: Path | None) -> Path | None:
    if start is None:
        return None
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".harness").exists() or (candidate / "tickets").exists():
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
    return project_root / ".harness"


def current_run_state_path(project_root: Path) -> Path:
    return runtime_dir(project_root) / "state" / "current-run.json"


def session_state_dir(project_root: Path) -> Path:
    return runtime_dir(project_root) / "state" / "sessions"


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


def legacy_active_ticket_candidates(project_root: Path, ticket_id: str) -> list[Path]:
    return sorted(
        path for path in tickets_dir(project_root).glob(f"{ticket_id}*.md") if path.is_file()
    )


def legacy_archive_ticket_candidates(project_root: Path, ticket_id: str) -> list[Path]:
    archive_dir = tickets_dir(project_root) / "archive"
    return sorted(path for path in archive_dir.glob(f"{ticket_id}*.md") if path.is_file())


def ticket_path_candidates(project_root: Path, ticket_id: str) -> list[Path]:
    candidates: list[Path] = []
    for path in (
        canonical_active_ticket_path(project_root, ticket_id),
        *legacy_active_ticket_candidates(project_root, ticket_id),
        canonical_archive_ticket_path(project_root, ticket_id),
        *legacy_archive_ticket_candidates(project_root, ticket_id),
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
    legacy_tickets = sorted(
        path
        for path in ticket_root.glob("TASK-*.md")
        if path.is_file()
    )
    return directory_tickets + legacy_tickets


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


def resolve_ticket_path(project_root: Path, current_run: Mapping[str, object]) -> Path | None:
    ticket_path = current_run.get("ticket_path")
    if isinstance(ticket_path, str) and ticket_path.strip():
        candidate = Path(ticket_path)
        if not candidate.is_absolute():
            candidate = (project_root / ticket_path).resolve()
        if candidate.is_file():
            return candidate

    ticket_id = current_run.get("ticket_id")
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        return None
    return resolve_ticket_path_by_id(project_root, ticket_id.strip())


def has_runtime_ownership(payload: Mapping[str, object] | None) -> bool:
    if not isinstance(payload, Mapping):
        return False
    run_state = payload.get("run_state")
    if isinstance(run_state, str) and run_state.strip():
        return True
    claim = payload.get("claim")
    if isinstance(claim, Mapping) and claim:
        return True
    ticket_id = payload.get("ticket_id")
    run_id = payload.get("run_id")
    return (
        isinstance(ticket_id, str)
        and bool(ticket_id.strip())
        and isinstance(run_id, str)
        and bool(run_id.strip())
    )


def set_ticket_claim_alias(project_root: Path, current_run: Mapping[str, object], session_name: str) -> None:
    ticket_path = resolve_ticket_path(project_root, current_run)
    if ticket_path is None:
        return
    text = read_ticket_text(ticket_path)
    parts = split_frontmatter(text)
    if parts is None:
        return
    raw_frontmatter, body = parts
    updated_frontmatter = update_frontmatter_field(raw_frontmatter, "claimed_by", session_name, after_key="owner")
    write_ticket_text(ticket_path, updated_frontmatter, body)


def clear_ticket_claim_alias(project_root: Path, ticket_id: str, session_name: str) -> None:
    ticket_path = resolve_ticket_path_by_id(project_root, ticket_id.strip())
    if ticket_path is None:
        return
    text = read_ticket_text(ticket_path)
    parts = split_frontmatter(text)
    if parts is None:
        return
    raw_frontmatter, body = parts
    claimed_prefix = "claimed_by:"
    claimed_value = ""
    for line in raw_frontmatter.splitlines():
        if line.startswith(claimed_prefix):
            claimed_value = line.split(":", 1)[1].strip()
            break
    if claimed_value != session_name:
        return
    updated_frontmatter = clear_frontmatter_field(raw_frontmatter, "claimed_by")
    write_ticket_text(ticket_path, updated_frontmatter, body)


def allocate_session_name(project_root: Path, session_id: str, existing_payload: Mapping[str, object] | None = None) -> str:
    if isinstance(existing_payload, Mapping):
        existing_name = existing_payload.get("session_name")
        if isinstance(existing_name, str) and existing_name.strip():
            return existing_name.strip()

    used: set[str] = set()
    for candidate in session_state_dir(project_root).glob("*.json"):
        payload = load_json_dict(candidate)
        if candidate == session_state_path(project_root, session_id):
            continue
        session_name = payload.get("session_name")
        if isinstance(session_name, str) and session_name.strip():
            used.add(session_name.strip())
    for alias in SESSION_ALIAS_POOL:
        if alias not in used:
            return alias
    suffix = re.sub(r"[^A-Za-z0-9]+", "", session_id)[-4:] or "x"
    return f"agent-{suffix.lower()}"


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
    raw = os.environ.get("IMPL_RUN_STATE", "").strip()
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


def parse_inline_json(raw: str) -> object:
    text = raw.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def parse_inline_scalar(raw: str) -> str:
    text = raw.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        return text[1:-1]
    return text


def parse_loop_contract(raw_text: str) -> dict[str, object]:
    done_when: list[dict[str, object]] = []
    completion_marker = ""
    retry_message = ""

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("done_when=") or line.startswith("done_when:"):
            _, value = re.split(r"[:=]", line, maxsplit=1)
            parsed = parse_inline_json(value)
            if isinstance(parsed, list):
                normalized: list[dict[str, object]] = []
                for item in parsed:
                    if isinstance(item, dict):
                        normalized.append(dict(item))
                done_when = normalized
        elif line.startswith("completion_marker=") or line.startswith("completion_marker:"):
            _, value = re.split(r"[:=]", line, maxsplit=1)
            completion_marker = parse_inline_scalar(value)
        elif line.startswith("retry_message=") or line.startswith("retry_message:"):
            _, value = re.split(r"[:=]", line, maxsplit=1)
            retry_message = parse_inline_scalar(value)

    contract: dict[str, object] = {
        "done_when": done_when,
        "retry_message": retry_message or "Continue the current loop until the loop contract is satisfied.",
    }
    if completion_marker:
        contract["completion_marker"] = completion_marker
    return contract


def loop_contract_ready(contract: Mapping[str, object]) -> bool:
    done_when = contract.get("done_when")
    if isinstance(done_when, list) and done_when:
        return True
    completion_marker = contract.get("completion_marker")
    return isinstance(completion_marker, str) and bool(completion_marker.strip())


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

    session_payload_fallback: dict[str, object] | None = None
    if normalized_session_id:
        payload = load_json_dict(session_state_path(project_root, normalized_session_id))
        if payload:
            session_payload = _with_runtime_metadata(payload, session_id=normalized_session_id)
            if has_runtime_ownership(session_payload):
                return session_payload
            session_payload_fallback = session_payload

    current_payload = load_json_dict(current_run_state_path(project_root))
    if not current_payload:
        return session_payload_fallback

    current_with_metadata = _with_runtime_metadata(current_payload, session_id=normalized_session_id)
    if _matches_session(current_with_metadata, normalized_session_id) and has_runtime_ownership(current_with_metadata):
        return current_with_metadata

    run_state = current_payload.get("run_state")
    if isinstance(run_state, str) and run_state.strip():
        nested = load_json_dict(resolve_runtime_path(project_root, run_state))
        if nested and _matches_session(nested, normalized_session_id):
            return _with_runtime_metadata(nested, session_id=normalized_session_id, explicit_run_state=run_state.strip())

    if session_payload_fallback is not None:
        return session_payload_fallback
    if _matches_session(current_with_metadata, normalized_session_id):
        return current_with_metadata
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
        "tmux_session",
        "tmux_window",
        "tmux_pane",
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


def build_phase_requirements(project_root: Path, ticket_id: str, *, requires_qa: bool, requires_demo: bool) -> dict[str, object]:
    artifact_root = canonical_active_ticket_path(project_root, ticket_id).parent / "artifacts"
    requirements: dict[str, object] = {
        "impl": {
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
    requires_qa = ticket_frontmatter_bool(text, "requires_qa", default=True)
    requires_demo = ticket_frontmatter_bool(text, "requires_demo", default=False)
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


def seeded_impl_run_id(ticket_id: str, session_id: str) -> str:
    suffix = re.sub(r"[^A-Za-z0-9]+", "", session_id.strip().lower())[:8] or "session"
    return f"run-{ticket_id.lower()}-building-seed-{suffix}"


def maybe_seed_impl_runtime(
    *,
    project_root: Path,
    current_run: Mapping[str, object] | None,
    last_user_turn: Mapping[str, object],
    session_id: str,
) -> dict[str, object] | None:
    if has_runtime_ownership(current_run):
        seeded_existing = dict(current_run) if isinstance(current_run, Mapping) else None
    else:
        seeded_existing = dict(current_run) if isinstance(current_run, Mapping) else {}
    control_surface = str(last_user_turn.get("control_surface") or "").strip().lower()
    if control_surface not in EXECUTION_PHASES:
        return seeded_existing if seeded_existing else None
    if control_surface == "impl" and not bool(last_user_turn.get("explicit_impl_requested")):
        return seeded_existing if seeded_existing else None
    ticket_id = str((current_run or {}).get("ticket_id") or "").strip()
    ticket_path = str((current_run or {}).get("ticket_path") or "").strip()
    if not ticket_id or not ticket_path:
        explicit_ticket_id = str(last_user_turn.get("explicit_ticket_id") or "").strip()
        selection = resolve_ticket_for_impl_seed(project_root, explicit_ticket_id)
        if selection is None:
            return seeded_existing if seeded_existing else None
        ticket_id, ticket_path = selection
    execution_contract = load_ticket_execution_contract(project_root, ticket_path, control_surface=control_surface)
    seeded = dict(current_run) if isinstance(current_run, Mapping) else {}
    seeded["ticket_id"] = ticket_id
    seeded["current_ticket_id"] = ticket_id
    seeded["ticket_path"] = ticket_path
    seeded["run_id"] = str(seeded.get("run_id") or seeded_impl_run_id(ticket_id, session_id))
    seeded["phase"] = "building"
    seeded["status"] = "running"
    seeded["skill_name"] = control_surface
    seeded["execution_phase"] = control_surface if control_surface in EXECUTION_PHASES else "impl"
    seeded["requires_qa"] = bool(execution_contract["requires_qa"])
    seeded["requires_demo"] = bool(execution_contract["requires_demo"])
    seeded["phase_requirements"] = dict(execution_contract["phase_requirements"])
    if session_id:
        seeded["session_id"] = session_id
    seeded["impl_loop_active"] = True
    if "next_phase" not in seeded:
        seeded["next_phase"] = "building"
    return seeded


def maybe_seed_loop_runtime(
    *,
    current_run: Mapping[str, object] | None,
    last_user_turn: Mapping[str, object],
    session_id: str,
) -> dict[str, object] | None:
    seeded = dict(current_run) if isinstance(current_run, Mapping) else {}
    skill_name = str(seeded.get("skill_name") or "").strip().lower()

    if bool(last_user_turn.get("explicit_loop_stop_requested")):
        return seeded if seeded else None

    if not bool(last_user_turn.get("explicit_loop_requested")):
        if skill_name == "loop":
            return seeded
        return seeded if has_runtime_ownership(seeded) else None

    contract = last_user_turn.get("loop_contract")
    if not isinstance(contract, Mapping) or not loop_contract_ready(contract):
        return seeded if seeded else None

    for key in (
        "ticket_id",
        "current_ticket_id",
        "ticket_path",
        "run_id",
        "phase",
        "next_phase",
        "claim",
        "run_state",
        "impl_loop_active",
        "execution_phase",
        "requires_qa",
        "requires_demo",
        "phase_requirements",
        "worker_name",
        "main_artifact_path",
        "tmux_session",
        "tmux_window",
        "tmux_pane",
        "auto_continue",
    ):
        seeded.pop(key, None)
    seeded["skill_name"] = "loop"
    seeded["status"] = "running"
    seeded["loop_active"] = True
    seeded["loop_contract"] = dict(contract)
    seeded["loop_last_checked_at"] = ""
    seeded["loop_last_check_summary"] = "loop started"
    if session_id:
        seeded["session_id"] = session_id
    return seeded


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
            "execution_phase",
            "requires_qa",
            "requires_demo",
            "phase_requirements",
            "grounding_summary",
            "worker_started_at",
            "last_checkpoint_at",
            "checkpoint_summary",
            "session_id",
            "tmux_session",
            "tmux_window",
            "tmux_pane",
            "auto_continue",
            "impl_loop_active",
            "loop_active",
            "loop_contract",
            "loop_last_checked_at",
            "loop_last_check_summary",
            "session_origin",
            "session_origin_source",
            "session_origin_reason",
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


def initialize_session_state(
    *,
    project_root: Path,
    session_id: str,
    current_run: Mapping[str, object] | None,
    explicit_run_state: str | None,
    captured_at: str,
    session_origin: str = "",
    session_origin_source: str = "",
    session_origin_reason: str = "",
) -> dict[str, object]:
    normalized_session_id = normalize_session_id(session_id)
    if not normalized_session_id:
        return {}

    session_path = session_state_path(project_root, normalized_session_id)
    existing_session = load_json_dict(session_path)
    session_name = allocate_session_name(project_root, normalized_session_id, existing_session)
    previous_ticket_id = ""
    if isinstance(existing_session.get("current_ticket_id"), str):
        previous_ticket_id = str(existing_session.get("current_ticket_id") or "").strip()
    current_skill_name = ""
    if isinstance(current_run, Mapping) and isinstance(current_run.get("skill_name"), str):
        current_skill_name = str(current_run.get("skill_name") or "").strip()

    ticket_id = ""
    ticket_path = ""
    run_id = ""
    phase = ""
    status = ""
    if isinstance(current_run, Mapping):
        for key in ("ticket_id", "ticket_path", "run_id", "phase", "status"):
            value = current_run.get(key)
            if not isinstance(value, str) or not value.strip():
                continue
            if key == "ticket_id":
                ticket_id = value.strip()
            elif key == "ticket_path":
                ticket_path = value.strip()
            elif key == "run_id":
                run_id = value.strip()
            elif key == "phase":
                phase = value.strip()
            elif key == "status":
                status = value.strip()

    session_payload: dict[str, object] = dict(existing_session)
    session_payload["session_id"] = normalized_session_id
    session_payload["session_name"] = session_name
    session_payload["last_seen_at"] = captured_at
    session_payload["updated_at"] = captured_at
    if session_origin:
        session_payload["session_origin"] = session_origin
    if session_origin_source:
        session_payload["session_origin_source"] = session_origin_source
    if session_origin_reason:
        session_payload["session_origin_reason"] = session_origin_reason
    if explicit_run_state and "run_state" not in session_payload:
        session_payload["run_state"] = explicit_run_state
    elif isinstance(current_run, Mapping):
        run_state = current_run.get("run_state")
        if isinstance(run_state, str) and run_state.strip():
            session_payload["run_state"] = run_state.strip()
    if ticket_id:
        session_payload["current_ticket_id"] = ticket_id
    elif "current_ticket_id" not in session_payload:
        session_payload["current_ticket_id"] = ""
    if ticket_path:
        session_payload["ticket_path"] = ticket_path
    if run_id:
        session_payload["run_id"] = run_id
    if phase:
        session_payload["phase"] = phase
    if status:
        session_payload["status"] = status
    if isinstance(current_run, Mapping) and isinstance(current_run.get("impl_loop_active"), bool):
        session_payload["impl_loop_active"] = bool(current_run.get("impl_loop_active"))
    for key in ("execution_phase",):
        value = (current_run or {}).get(key) if isinstance(current_run, Mapping) else None
        if isinstance(value, str) and value.strip():
            session_payload[key] = value.strip()
    for key in ("requires_qa", "requires_demo"):
        value = (current_run or {}).get(key) if isinstance(current_run, Mapping) else None
        if isinstance(value, bool):
            session_payload[key] = value
    phase_requirements = (current_run or {}).get("phase_requirements") if isinstance(current_run, Mapping) else None
    if isinstance(phase_requirements, Mapping):
        session_payload["phase_requirements"] = dict(phase_requirements)

    write_json(session_path, session_payload)

    if previous_ticket_id and ticket_id and previous_ticket_id != ticket_id:
        clear_ticket_claim_alias(project_root, previous_ticket_id, session_name)
    if previous_ticket_id and not ticket_id and current_skill_name == "loop":
        clear_ticket_claim_alias(project_root, previous_ticket_id, session_name)
    if ticket_id and isinstance(current_run, Mapping):
        set_ticket_claim_alias(project_root, current_run, session_name)

    return session_payload


def extract_ticket_id(text: str) -> str | None:
    match = TICKET_ID_PATTERN.search(text)
    return match.group(0) if match else None


def has_explicit_impl_invocation(text: str) -> bool:
    return extract_control_surface(text) == "impl"


def has_explicit_loop_invocation(text: str) -> bool:
    return extract_control_surface(text) == "loop"


def has_explicit_loop_stop_request(text: str) -> bool:
    lowered = text.strip().lower()
    if not lowered:
        return False
    return bool(
        re.search(r"(?<!\S)(?:stop|cancel|exit)\s+loop(?=$|[\s.,:;!?()\[\]{}\"'`])", lowered)
        or re.search(r"(?<!\S)\$loop\s+(?:stop|cancel|exit)(?=$|[\s.,:;!?()\[\]{}\"'`])", lowered)
    )


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
        return "control", "legacy_last_user_turn", f"persisted last_user_turn invoked ${control_surface}"

    raw_text = last_user_turn.get("raw_text")
    if isinstance(raw_text, str) and raw_text.strip():
        if is_internal_user_prompt(raw_text):
            return "internal", "legacy_last_user_turn", "persisted raw_text matches internal prompt signature"
        legacy_control_surface = extract_control_surface(raw_text)
        if legacy_control_surface:
            return "control", "legacy_last_user_turn", f"persisted raw_text invoked ${legacy_control_surface}"

    if bool(last_user_turn.get("explicit_impl_requested")):
        return "control", "legacy_last_user_turn", "persisted explicit impl request implies a control session"

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
    if text.startswith("Run the `impl` skill on ticket "):
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
    lowered = raw_text.lower()
    control_surface = extract_control_surface(raw_text)

    if control_surface == "impl-plan":
        return "planning"

    if control_surface == "impl":
        return "building"

    if control_surface == "qa":
        return "building"

    if control_surface == "demo":
        return "building"

    if control_surface == "loop":
        return "building"

    if control_surface == "ralph":
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
    lowered = raw_text.lower()

    if intent_mode == "documenting" or _contains_any(
        lowered,
        ("history.md", "memory.md", "troubles.md", "readme", "docs update", "document "),
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
    control_surface = extract_control_surface(raw_text)
    execution_phase = requested_execution_phase(control_surface)
    explicit_impl_requested = has_explicit_impl_invocation(raw_text)
    explicit_loop_requested = has_explicit_loop_invocation(raw_text)
    explicit_loop_stop_requested = has_explicit_loop_stop_request(raw_text)
    loop_contract = parse_loop_contract(raw_text) if explicit_loop_requested and not explicit_loop_stop_requested else {}
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
        "control_surface": control_surface,
        "requested_execution_phase": execution_phase,
        "explicit_impl_requested": explicit_impl_requested,
        "explicit_loop_requested": explicit_loop_requested,
        "explicit_loop_stop_requested": explicit_loop_stop_requested,
        "loop_contract": loop_contract,
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
    captured_at_value = captured_at or now_iso()
    current_run = load_current_run(
        project_root,
        session_id=session_id,
        explicit_run_state=explicit_run_state,
    )
    normalized_session_id = normalize_session_id(session_id)
    existing_session = load_json_dict(session_state_path(project_root, normalized_session_id)) if normalized_session_id else {}
    session_origin, session_origin_source, session_origin_reason = resolve_session_origin(
        raw_text,
        current_run=current_run,
        existing_session=existing_session,
    )
    if session_origin != "control":
        return None

    last_user_turn = normalize_user_turn(
        raw_text,
        turn_id=turn_id,
        source=source,
        captured_at=captured_at_value,
    )
    current_run = maybe_seed_impl_runtime(
        project_root=project_root,
        current_run=current_run,
        last_user_turn=last_user_turn,
        session_id=normalized_session_id,
    )
    current_run = maybe_seed_loop_runtime(
        current_run=current_run,
        last_user_turn=last_user_turn,
        session_id=normalized_session_id,
    )
    execution_loop_requested = bool(last_user_turn.get("requested_execution_phase"))
    session_state = (
        initialize_session_state(
            project_root=project_root,
            session_id=normalized_session_id,
            current_run=current_run,
            explicit_run_state=explicit_run_state,
            captured_at=captured_at_value,
            session_origin=session_origin,
            session_origin_source=session_origin_source,
            session_origin_reason=session_origin_reason,
        )
        if normalized_session_id
        else {}
    )

    existing_source = current_run if current_run is not None else session_state
    existing = existing_source.get("last_user_turn") if isinstance(existing_source, Mapping) else None
    if only_if_missing and isinstance(existing, dict) and existing:
        return existing

    if current_run is not None:
        updates: dict[str, object] = {
            "last_user_turn": last_user_turn,
            "impl_loop_active": execution_loop_requested,
            "session_origin": session_origin,
            "session_origin_source": session_origin_source,
            "session_origin_reason": session_origin_reason,
            "updated_at": str(last_user_turn["captured_at"]),
        }
        if isinstance(current_run.get("skill_name"), str) and str(current_run.get("skill_name") or "").strip():
            updates["skill_name"] = str(current_run.get("skill_name") or "").strip()
        if isinstance(current_run.get("execution_phase"), str):
            updates["execution_phase"] = str(current_run.get("execution_phase") or "").strip()
        for key in ("requires_qa", "requires_demo"):
            if isinstance(current_run.get(key), bool):
                updates[key] = bool(current_run.get(key))
        if isinstance(current_run.get("phase_requirements"), Mapping):
            updates["phase_requirements"] = dict(current_run.get("phase_requirements") or {})
        if isinstance(current_run.get("loop_active"), bool):
            updates["loop_active"] = bool(current_run.get("loop_active"))
        if isinstance(current_run.get("loop_contract"), Mapping):
            updates["loop_contract"] = dict(current_run.get("loop_contract") or {})
        if isinstance(current_run.get("loop_last_checked_at"), str):
            updates["loop_last_checked_at"] = str(current_run.get("loop_last_checked_at") or "")
        if isinstance(current_run.get("loop_last_check_summary"), str):
            updates["loop_last_check_summary"] = str(current_run.get("loop_last_check_summary") or "")
        if session_state:
            session_name = session_state.get("session_name")
            current_ticket_id = session_state.get("current_ticket_id")
            if isinstance(session_name, str) and session_name.strip():
                updates["session_name"] = session_name.strip()
            if (
                str(current_run.get("skill_name") or "").strip() != "loop"
                and isinstance(current_ticket_id, str)
                and current_ticket_id.strip()
            ):
                updates["current_ticket_id"] = current_ticket_id.strip()
        persist_runtime_update(
            project_root,
            current_run,
            updates,
        )
    elif normalized_session_id:
        session_path = session_state_path(project_root, normalized_session_id)
        payload = dict(session_state)
        payload["last_user_turn"] = last_user_turn
        payload["impl_loop_active"] = execution_loop_requested
        if isinstance(current_run, Mapping):
            if isinstance(current_run.get("skill_name"), str) and str(current_run.get("skill_name") or "").strip():
                payload["skill_name"] = str(current_run.get("skill_name") or "").strip()
            if isinstance(current_run.get("execution_phase"), str):
                payload["execution_phase"] = str(current_run.get("execution_phase") or "").strip()
            for key in ("requires_qa", "requires_demo"):
                if isinstance(current_run.get(key), bool):
                    payload[key] = bool(current_run.get(key))
            if isinstance(current_run.get("phase_requirements"), Mapping):
                payload["phase_requirements"] = dict(current_run.get("phase_requirements") or {})
            if isinstance(current_run.get("loop_active"), bool):
                payload["loop_active"] = bool(current_run.get("loop_active"))
            if isinstance(current_run.get("loop_contract"), Mapping):
                payload["loop_contract"] = dict(current_run.get("loop_contract") or {})
            if isinstance(current_run.get("loop_last_checked_at"), str):
                payload["loop_last_checked_at"] = str(current_run.get("loop_last_checked_at") or "")
            if isinstance(current_run.get("loop_last_check_summary"), str):
                payload["loop_last_check_summary"] = str(current_run.get("loop_last_check_summary") or "")
        payload["updated_at"] = str(last_user_turn["captured_at"])
        payload["last_seen_at"] = str(last_user_turn["captured_at"])
        write_json(session_path, payload)
        write_json(current_run_state_path(project_root), payload)
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
