#!/usr/bin/env python3
"""Verified GitHub issue ticket finalization and completion mining."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import urlparse

import yaml

from farplane_event_store import atomic_write_json, pending_events
from farplane_mining import CodexRunner, MiningError, mine_ticket


TICKET_ID_RE = re.compile(r"^TASK-\d{4}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ISSUE_PATH_RE = re.compile(r"^/([^/]+)/([^/]+)/issues/([1-9]\d*)$")
SUCCESS_STATUSES = {"done", "complete", "completed", "closed"}
GitHubRunner = Callable[[list[str], Path], subprocess.CompletedProcess[str]]


class TicketFinalizeError(RuntimeError):
    """Raised when a ticket cannot be finalized safely."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _frontmatter(text: str) -> tuple[dict[str, Any], list[str], str]:
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, flags=re.S)
    if not match:
        raise TicketFinalizeError("ticket_frontmatter_missing")
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise TicketFinalizeError(f"ticket_frontmatter_invalid:{exc}") from exc
    if not isinstance(payload, dict):
        raise TicketFinalizeError("ticket_frontmatter_invalid_shape")
    return payload, match.group(1).splitlines(), text[match.end() :]


def _closed_text(text: str, *, updated_at: str) -> tuple[str, dict[str, Any]]:
    before, lines, body = _frontmatter(text)
    status = str(before.get("status") or "").strip().lower()
    if status in {"failed", "rejected"}:
        raise TicketFinalizeError(f"ticket_has_non_success_terminal_status:{status}")
    if status in SUCCESS_STATUSES and not before.get("claimed_by"):
        return text, {}

    output: list[str] = []
    saw_status = False
    saw_updated = False
    for line in lines:
        key = line.split(":", 1)[0].strip() if ":" in line else ""
        if key == "claimed_by":
            continue
        if key == "status":
            output.append("status: done")
            saw_status = True
            continue
        if key == "updated_at":
            output.append(f"updated_at: {updated_at}")
            saw_updated = True
            continue
        output.append(line)
    if not saw_status:
        output.append("status: done")
    if not saw_updated:
        output.append(f"updated_at: {updated_at}")
    frontmatter_text = "\n".join(output)
    return f"---\n{frontmatter_text}\n---\n{body}", before


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TicketFinalizeError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(payload, dict):
        raise TicketFinalizeError(f"invalid_json_shape:{path}:expected_object")
    return payload


def _load_bindings(root: Path) -> dict[str, Any]:
    path = root / "farplane" / "bindings.yaml"
    if not path.is_file():
        raise TicketFinalizeError("github_repo_not_configured")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise TicketFinalizeError(f"bindings_invalid:{exc}") from exc
    if not isinstance(payload, dict):
        raise TicketFinalizeError("bindings_invalid_shape")
    return payload


def _configured_repository(root: Path) -> str:
    bindings = _load_bindings(root)
    integrations = bindings.get("integrations")
    github = integrations.get("github") if isinstance(integrations, dict) else None
    repository = str(github.get("repo") or "").strip() if isinstance(github, dict) else ""
    if not REPOSITORY_RE.fullmatch(repository):
        raise TicketFinalizeError("github_repo_not_configured")
    return repository


def _parse_issue_url(issue_url: str) -> tuple[str, int, str]:
    raw = issue_url.strip()
    parsed = urlparse(raw)
    match = ISSUE_PATH_RE.fullmatch(parsed.path)
    if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.params or parsed.query or parsed.fragment or not match:
        raise TicketFinalizeError(f"invalid_github_issue_url:{issue_url}")
    repository = f"{match.group(1)}/{match.group(2)}"
    number = int(match.group(3))
    return repository, number, f"https://github.com/{repository}/issues/{number}"


def _default_github_runner(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, check=False)


def _github_json(runner: GitHubRunner, command: list[str], root: Path) -> dict[str, Any]:
    result = runner(command, root)
    if result.returncode != 0:
        detail = str(result.stderr or result.stdout or "unknown_error").strip().replace("\n", " ")[:500]
        raise TicketFinalizeError(f"github_command_failed:{' '.join(command[1:])}:{detail}")
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise TicketFinalizeError(f"github_response_invalid_json:{exc}") from exc
    if not isinstance(payload, dict):
        raise TicketFinalizeError("github_response_invalid_shape")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _issue_section(body: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)",
        body,
    )
    return match.group(1).strip() if match else ""


def _stored_media(receipt: dict[str, Any]) -> list[dict[str, str]]:
    raw = receipt.get("media")
    if not receipt:
        return []
    if not isinstance(raw, list):
        raise TicketFinalizeError("closure_receipt_invalid_media")
    media: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            raise TicketFinalizeError("closure_receipt_invalid_media")
        path = str(item.get("path") or "")
        digest = str(item.get("sha256") or "")
        if not path or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise TicketFinalizeError("closure_receipt_invalid_media")
        if digest in seen:
            raise TicketFinalizeError("closure_receipt_duplicate_media")
        seen.add(digest)
        media.append({"path": path, "sha256": digest})
    return media


def _expected_media(root: Path, media_paths: Sequence[str | Path], receipt: dict[str, Any]) -> list[dict[str, str]]:
    stored = _stored_media(receipt)
    if receipt:
        if media_paths:
            supplied: list[str] = []
            for raw in media_paths:
                candidate = Path(raw).expanduser()
                candidate = candidate if candidate.is_absolute() else root / candidate
                candidate = candidate.resolve()
                try:
                    supplied.append(candidate.relative_to(root).as_posix())
                except ValueError:
                    supplied.append(str(candidate))
            stored_paths = [item["path"] for item in stored]
            if supplied != stored_paths:
                raise TicketFinalizeError("media_paths_conflict_with_closure_receipt")
            for raw, item in zip(media_paths, stored):
                candidate = Path(raw).expanduser()
                candidate = candidate if candidate.is_absolute() else root / candidate
                if candidate.is_file() and _sha256(candidate) != item["sha256"]:
                    raise TicketFinalizeError(f"media_digest_changed:{raw}")
        return stored

    media: list[dict[str, str]] = []
    seen: set[str] = set()
    for raw in media_paths:
        path = Path(raw).expanduser()
        path = path if path.is_absolute() else root / path
        path = path.resolve()
        if not path.is_file():
            raise TicketFinalizeError(f"media_not_found:{raw}")
        digest = _sha256(path)
        if digest in seen:
            raise TicketFinalizeError(f"duplicate_media_digest:{digest}")
        seen.add(digest)
        try:
            display = path.relative_to(root).as_posix()
        except ValueError:
            display = str(path)
        media.append({"path": display, "sha256": digest})
    return media


def verify_github_issue(
    ticket_id: str,
    issue_url: str,
    expected_media: Sequence[dict[str, str]],
    runner: GitHubRunner,
    *,
    project_root: Path,
    configured_repository: str,
) -> dict[str, Any]:
    """Verify the exact configured-project issue and return its stable locator fields."""

    url_repository, issue_number, canonical_url = _parse_issue_url(issue_url)
    if url_repository != configured_repository:
        raise TicketFinalizeError(f"github_issue_repo_mismatch:expected={configured_repository}:actual={url_repository}")

    issue = _github_json(
        runner,
        [
            "gh",
            "issue",
            "view",
            str(issue_number),
            "--repo",
            configured_repository,
            "--json",
            "number,title,state,body,comments,closedAt,url",
        ],
        project_root,
    )
    try:
        returned_repository, returned_number, returned_url = _parse_issue_url(str(issue.get("url") or ""))
    except TicketFinalizeError as exc:
        raise TicketFinalizeError("github_issue_response_url_invalid") from exc
    if returned_repository != configured_repository or returned_number != issue_number or returned_url != canonical_url:
        raise TicketFinalizeError("github_issue_response_mismatch")
    if int(issue.get("number") or 0) != issue_number:
        raise TicketFinalizeError("github_issue_number_mismatch")
    if str(issue.get("state") or "").upper() != "CLOSED":
        raise TicketFinalizeError(f"github_issue_not_closed:{issue_number}")
    closed_at = str(issue.get("closedAt") or "").strip()
    if not closed_at:
        raise TicketFinalizeError(f"github_issue_closed_at_missing:{issue_number}")
    body = str(issue.get("body") or "")
    ticket_marker = f"<!-- farplane-ticket-id:{ticket_id} -->"
    if body.count(ticket_marker) != 1:
        raise TicketFinalizeError(f"github_issue_ticket_marker_missing:{ticket_id}")
    for heading in ("Before", "After", "Example", "Key decisions", "Proof"):
        section = _issue_section(body, heading).replace(ticket_marker, "").strip()
        if not section:
            raise TicketFinalizeError(f"github_issue_section_missing:{heading.lower().replace(' ', '_')}")
    title = str(issue.get("title") or "").strip()
    if not title:
        raise TicketFinalizeError(f"github_issue_title_missing:{issue_number}")

    raw_comments = issue.get("comments")
    if not isinstance(raw_comments, list):
        raise TicketFinalizeError("github_issue_comments_invalid")
    media_comment_urls: list[str] = []
    for media in expected_media:
        marker = f"<!-- farplane-ticket-media:{ticket_id}:{media['sha256']} -->"
        marker_count = sum(
            str(comment.get("body") or "").count(marker)
            for comment in raw_comments
            if isinstance(comment, dict)
        )
        matches = [
            comment
            for comment in raw_comments
            if isinstance(comment, dict) and marker in str(comment.get("body") or "")
        ]
        if marker_count != 1 or len(matches) != 1:
            raise TicketFinalizeError(f"github_issue_media_marker_count:{media['sha256']}:{marker_count}")
        matched_body = str(matches[0].get("body") or "")
        if re.search(r"https://github\.com/user-attachments/(?:assets|files)/[^\s)<>'\"]+", matched_body) is None:
            raise TicketFinalizeError(f"github_issue_media_attachment_missing:{media['sha256']}")
        matched_url = str(matches[0].get("url") or "")
        if not matched_url:
            raise TicketFinalizeError(f"github_issue_media_comment_url_missing:{media['sha256']}")
        parsed_comment = urlparse(matched_url)
        if (
            parsed_comment.scheme != "https"
            or parsed_comment.netloc != "github.com"
            or parsed_comment.path != urlparse(canonical_url).path
            or re.fullmatch(r"issuecomment-[1-9]\d*", parsed_comment.fragment) is None
        ):
            raise TicketFinalizeError(f"github_issue_media_comment_url_invalid:{media['sha256']}")
        media_comment_urls.append(matched_url)

    return {
        "github_issue_url": canonical_url,
        "github_issue_number": issue_number,
        "title": title,
        "remote_state": "closed",
        "closed_at": closed_at,
        "media_comment_urls": media_comment_urls,
    }


def _load_archive_index(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TicketFinalizeError(f"archive_index_invalid_json:line={number}:{exc}") from exc
        if not isinstance(row, dict) or not TICKET_ID_RE.fullmatch(str(row.get("ticket_id") or "")):
            raise TicketFinalizeError(f"archive_index_invalid_row:line={number}")
        rows.append(row)
    return rows


def _matching_index_row(rows: Sequence[dict[str, Any]], ticket_id: str, issue_url: str) -> dict[str, Any]:
    matches = [row for row in rows if row.get("ticket_id") == ticket_id]
    if len(matches) > 1:
        raise TicketFinalizeError(f"archive_index_duplicate_ticket_id:{ticket_id}")
    if matches and str(matches[0].get("github_issue_url") or "") != issue_url:
        raise TicketFinalizeError(f"archive_index_issue_conflict:{ticket_id}")
    return matches[0] if matches else {}


def _upsert_archive_index(path: Path, rows: Sequence[dict[str, Any]], record: dict[str, Any]) -> None:
    output = [row for row in rows if row.get("ticket_id") != record["ticket_id"]]
    output.append(record)
    output.sort(key=lambda row: str(row.get("ticket_id") or ""))
    text = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in output)
    _atomic_write_text(path, text)


def _receipt_payload(
    *,
    ticket_id: str,
    remote: dict[str, Any],
    media: Sequence[dict[str, str]],
    status: str,
    metadata_delta: dict[str, Any],
    mining_status: str,
    mining_error: str | None,
    event_id: str | None,
    runs: Sequence[dict[str, Any]],
    local_packet_deleted: bool,
    phase: str,
) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "ok": mining_status == "complete" and local_packet_deleted,
        "ticket_id": ticket_id,
        "status": status,
        "phase": phase,
        "github_issue_url": remote["github_issue_url"],
        "github_issue_number": remote["github_issue_number"],
        "remote_state": remote["remote_state"],
        "media_comment_urls": list(remote["media_comment_urls"]),
        "media": list(media),
        "archive_index_path": "tickets/archive-index.jsonl",
        "local_packet_deleted": local_packet_deleted,
        "metadata_delta": metadata_delta,
        "mining_status": mining_status,
        "mining_error": mining_error,
        "event_id": event_id,
        "runs": list(runs),
        "closed_at": remote["closed_at"],
    }


def finalize_ticket(
    project_root: Path,
    ticket_id: str,
    github_issue_url: str,
    media_paths: Sequence[str | Path] = (),
    *,
    codex_runner: CodexRunner | None = None,
    github_runner: GitHubRunner | None = None,
) -> dict[str, Any]:
    """Verify, terminalize, mine, index, and delete one active ticket packet."""

    root = project_root.resolve()
    normalized = ticket_id.strip().upper()
    if not TICKET_ID_RE.fullmatch(normalized):
        raise TicketFinalizeError(f"invalid_ticket_id:{ticket_id}")

    active_dir = root / "tickets" / normalized
    active_ticket = active_dir / "ticket.md"
    legacy_ticket = root / "tickets" / "archive" / normalized / "ticket.md"
    index_path = root / "tickets" / "archive-index.jsonl"
    receipt_path = root / ".farplane" / "tickets" / "closures" / f"{normalized}.json"
    if active_dir.is_symlink() or active_dir.parent.resolve() != (root / "tickets").resolve():
        raise TicketFinalizeError(f"unsafe_ticket_packet_path:{active_dir}")
    receipt = _load_json(receipt_path)
    if receipt and str(receipt.get("github_issue_url") or "") != github_issue_url.strip():
        raise TicketFinalizeError(f"closure_receipt_issue_conflict:{normalized}")

    configured_repository = _configured_repository(root)
    url_repository, _, canonical_url = _parse_issue_url(github_issue_url)
    if url_repository != configured_repository:
        raise TicketFinalizeError(f"github_issue_repo_mismatch:expected={configured_repository}:actual={url_repository}")
    rows = _load_archive_index(index_path)
    existing_row = _matching_index_row(rows, normalized, canonical_url)
    if existing_row and not receipt:
        raise TicketFinalizeError(f"archive_index_without_closure_receipt:{normalized}")

    if active_ticket.is_file() and legacy_ticket.is_file():
        raise TicketFinalizeError(f"ticket_exists_active_and_archived:{normalized}")
    if not active_ticket.is_file() and active_dir.exists() and not (receipt and existing_row):
        raise TicketFinalizeError(f"ticket_packet_incomplete:{normalized}")
    if not active_ticket.is_file() and not active_dir.exists() and not (receipt and existing_row):
        if legacy_ticket.is_file():
            raise TicketFinalizeError(f"legacy_ticket_already_archived:{normalized}")
        raise TicketFinalizeError(f"ticket_not_found:{normalized}")
    if active_ticket.is_file():
        current, _, _ = _frontmatter(active_ticket.read_text(encoding="utf-8"))
        current_ticket_id = str(current.get("ticket_id") or "").strip().upper()
        if current_ticket_id != normalized:
            raise TicketFinalizeError(
                f"ticket_frontmatter_id_mismatch:expected={normalized}:actual={current_ticket_id or 'missing'}"
            )
        current_status = str(current.get("status") or "").strip().lower()
        if current_status in {"failed", "rejected"}:
            raise TicketFinalizeError(f"ticket_has_non_success_terminal_status:{current_status}")

    media = _expected_media(root, media_paths, receipt)
    remote = verify_github_issue(
        normalized,
        canonical_url,
        media,
        github_runner or _default_github_runner,
        project_root=root,
        configured_repository=configured_repository,
    )

    prior_complete = bool(
        receipt
        and existing_row
        and receipt.get("mining_status") == "complete"
        and receipt.get("event_id") == existing_row.get("event_id")
    )
    metadata_delta: dict[str, Any] = {}
    if prior_complete:
        mining_status = "complete"
        mining_error = None
        event_id = str(receipt.get("event_id") or "") or None
        runs = receipt.get("runs") if isinstance(receipt.get("runs"), list) else []
        status = "already_closed"
    else:
        if not active_ticket.is_file():
            raise TicketFinalizeError(f"ticket_not_found_for_mining:{normalized}")
        original = active_ticket.read_text(encoding="utf-8")
        closed_text, before = _closed_text(original, updated_at=now_iso())
        if closed_text != original:
            _atomic_write_text(active_ticket, closed_text)
        metadata_delta = {
            "status": {"before": before.get("status"), "after": "done"} if before else {},
            "claimed_by_cleared": bool(before.get("claimed_by")) if before else False,
        }
        try:
            mining = mine_ticket(root, normalized, codex_runner=codex_runner)
            mining_status = "complete"
            mining_error = None
            event_id = str(mining.get("event_id") or "") or None
            runs = mining.get("runs", []) if isinstance(mining.get("runs"), list) else []
        except MiningError as exc:
            mining_status = "pending"
            mining_error = str(exc)
            event_id = next(
                (
                    str(event.get("event_id"))
                    for event in pending_events(root)
                    if (event.get("entity_ref") or {}).get("id") == normalized
                ),
                None,
            )
            runs = []
        status = "closed"

        if mining_status != "complete":
            failed = _receipt_payload(
                ticket_id=normalized,
                remote=remote,
                media=media,
                status=status,
                metadata_delta=metadata_delta,
                mining_status=mining_status,
                mining_error=mining_error,
                event_id=event_id,
                runs=runs,
                local_packet_deleted=False,
                phase="mining_pending",
            )
            atomic_write_json(receipt_path, failed)
            return {**failed, "receipt_path": str(receipt_path)}

        mined = _receipt_payload(
            ticket_id=normalized,
            remote=remote,
            media=media,
            status=status,
            metadata_delta=metadata_delta,
            mining_status=mining_status,
            mining_error=mining_error,
            event_id=event_id,
            runs=runs,
            local_packet_deleted=False,
            phase="mined",
        )
        atomic_write_json(receipt_path, mined)

    index_record = {
        "schema_version": 1,
        "ticket_id": normalized,
        "title": remote["title"],
        "status": "done",
        "storage": "github_issue",
        "closed_at": remote["closed_at"],
        "github_issue_url": remote["github_issue_url"],
        "github_issue_number": remote["github_issue_number"],
        "media_comment_urls": remote["media_comment_urls"],
        "event_id": event_id,
        "mining_run_ids": [str(run.get("run_id")) for run in runs if isinstance(run, dict) and run.get("run_id")],
    }
    _upsert_archive_index(index_path, rows, index_record)
    indexed = _receipt_payload(
        ticket_id=normalized,
        remote=remote,
        media=media,
        status=status,
        metadata_delta=metadata_delta,
        mining_status="complete",
        mining_error=None,
        event_id=event_id,
        runs=runs,
        local_packet_deleted=False,
        phase="indexed",
    )
    atomic_write_json(receipt_path, indexed)

    if active_dir.is_symlink() or active_dir.parent.resolve() != (root / "tickets").resolve():
        raise TicketFinalizeError(f"unsafe_ticket_delete_path:{active_dir}")
    if active_dir.exists():
        shutil.rmtree(active_dir)

    complete = {
        **indexed,
        "ok": True,
        "status": "already_closed" if prior_complete else status,
        "phase": "complete",
        "local_packet_deleted": True,
    }
    atomic_write_json(receipt_path, complete)
    return {**complete, "receipt_path": str(receipt_path)}
