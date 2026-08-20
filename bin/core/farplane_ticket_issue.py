#!/usr/bin/env python3
"""GitHub issue rendering and lifecycle for ticket finalization."""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import urlparse


ISSUE_PATH_RE = re.compile(r"^/([^/]+)/([^/]+)/issues/([1-9]\d*)$")
GitHubRunner = Callable[[list[str], Path], subprocess.CompletedProcess[str]]
FrontmatterReader = Callable[[str], tuple[dict[str, Any], list[str], str]]


class TicketFinalizeError(RuntimeError):
    """Raised when a ticket cannot be finalized safely."""


def parse_issue_url(issue_url: str) -> tuple[str, int, str]:
    parsed = urlparse(issue_url.strip())
    match = ISSUE_PATH_RE.fullmatch(parsed.path)
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.params
        or parsed.query
        or parsed.fragment
        or not match
    ):
        raise TicketFinalizeError(f"invalid_github_issue_url:{issue_url}")
    repository = f"{match.group(1)}/{match.group(2)}"
    number = int(match.group(3))
    return repository, number, f"https://github.com/{repository}/issues/{number}"


def default_github_runner(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, check=False)


def _github_text(runner: GitHubRunner, command: list[str], root: Path) -> str:
    result = runner(command, root)
    if result.returncode != 0:
        detail = str(result.stderr or result.stdout or "unknown_error").strip().replace("\n", " ")[:500]
        raise TicketFinalizeError(f"github_command_failed:{' '.join(command[1:])}:{detail}")
    return str(result.stdout or "").strip()


def _github_json(runner: GitHubRunner, command: list[str], root: Path) -> dict[str, Any]:
    output = _github_text(runner, command, root)
    try:
        payload = json.loads(output or "{}")
    except json.JSONDecodeError as exc:
        raise TicketFinalizeError(f"github_response_invalid_json:{exc}") from exc
    if not isinstance(payload, dict):
        raise TicketFinalizeError("github_response_invalid_shape")
    return payload


def _paginated_issues(
    runner: GitHubRunner,
    *,
    project_root: Path,
    configured_repository: str,
) -> list[dict[str, Any]]:
    command = [
        "gh",
        "api",
        "--paginate",
        "--slurp",
        f"repos/{configured_repository}/issues?state=all&per_page=100",
    ]
    output = _github_text(runner, command, project_root)
    try:
        pages = json.loads(output or "[]")
    except json.JSONDecodeError as exc:
        raise TicketFinalizeError(f"github_response_invalid_json:{exc}") from exc
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise TicketFinalizeError("github_response_invalid_pages")
    issues: list[dict[str, Any]] = []
    for page in pages:
        for item in page:
            if not isinstance(item, dict):
                raise TicketFinalizeError("github_response_invalid_issue")
            if "pull_request" not in item:
                issues.append(
                    {
                        "number": item.get("number"),
                        "title": item.get("title"),
                        "state": item.get("state"),
                        "body": item.get("body"),
                        "url": item.get("html_url"),
                    }
                )
    return issues


def _markdown_section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)", text)
    return match.group(1).strip() if match else ""


def _plain_markdown(value: str) -> str:
    lines = []
    for raw in value.splitlines():
        line = re.sub(r"^\s*>\s?", "", raw).strip()
        if line and line != ">":
            lines.append(line)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def _delta_value(delta: str, label: str) -> str:
    match = re.search(
        rf"(?ms)^\s*>?\s*\*\*{re.escape(label)}:\*\*\s*(.*?)"
        rf"(?=^\s*>?\s*\*\*(?:Before|After|Example):\*\*|\Z)",
        delta,
    )
    return _plain_markdown(match.group(1)) if match else ""


def _markdown_items(section: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    for raw in section.splitlines():
        match = re.match(r"^\s*-\s+(?:\[[ xX]\]\s+)?(.*)$", raw)
        if match:
            if current:
                items.append(_plain_markdown(" ".join(current)))
            current = [match.group(1)]
        elif current and raw.strip() and not raw.lstrip().startswith("```"):
            current.append(raw.strip())
    if current:
        items.append(_plain_markdown(" ".join(current)))
    return [item for item in items if item]


def render_github_issue(
    ticket_path: Path,
    ticket_id: str,
    frontmatter: FrontmatterReader,
) -> tuple[str, str]:
    text = ticket_path.read_text(encoding="utf-8")
    metadata, _, _ = frontmatter(text)
    title = str(metadata.get("title") or "").strip()
    if not title:
        raise TicketFinalizeError("ticket_title_missing")
    delta = _markdown_section(text, "Delta")
    values = {label: _delta_value(delta, label) for label in ("Before", "After", "Example")}
    for label, value in values.items():
        if not value:
            raise TicketFinalizeError(f"ticket_delta_missing:{label.lower()}")
    decisions = _markdown_items(_markdown_section(text, "Notes"))
    decisions = decisions or _markdown_items(_markdown_section(text, "Scope"))
    if not decisions:
        summary = _plain_markdown(_markdown_section(text, "Summary"))
        decisions = [summary] if summary else []
    if not decisions:
        raise TicketFinalizeError("ticket_key_decisions_missing")
    done_items = re.findall(r"(?m)^\s*-\s+\[([ xX])\]\s+", _markdown_section(text, "Done"))
    completed = sum(1 for marker in done_items if marker.lower() == "x")
    proof = [f"{completed}/{len(done_items)} completion items checked"] if done_items else ["ticket marked complete"]
    review_path = ticket_path.parent / "artifacts" / "completion-review.md"
    if review_path.is_file():
        review_metadata, _, _ = frontmatter(review_path.read_text(encoding="utf-8"))
        verdict = str(review_metadata.get("verdict") or "").strip()
        if verdict:
            proof.append(f"completion review {verdict}")
    body = (
        f"## Before\n\n- {values['Before']}\n\n"
        f"## After\n\n- {values['After']}\n\n"
        f"## Example\n\n- {values['Example']}\n\n"
        "## Key decisions\n\n"
        + "\n".join(f"- {item}" for item in decisions[:3])
        + "\n\n## Proof\n\n- Checks: "
        + "; ".join(proof)
        + f".\n\n<!-- farplane-ticket-id:{ticket_id} -->\n"
    )
    return f"[{ticket_id}] {title}", body


def _body_file(ticket_id: str, body: str) -> tuple[int, Path]:
    descriptor, raw_path = tempfile.mkstemp(prefix=f"farplane-{ticket_id.lower()}-", suffix=".md")
    path = Path(raw_path)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(body)
    return descriptor, path


def find_or_create_issue(
    ticket_id: str,
    title: str,
    body: str,
    runner: GitHubRunner,
    *,
    project_root: Path,
    configured_repository: str,
) -> str:
    marker = f"<!-- farplane-ticket-id:{ticket_id} -->"
    matches = [
        issue
        for issue in _paginated_issues(
            runner,
            project_root=project_root,
            configured_repository=configured_repository,
        )
        if str(issue.get("body") or "").count(marker) == 1
    ]
    if len(matches) > 1:
        raise TicketFinalizeError(f"github_issue_marker_duplicate:{ticket_id}")
    if matches:
        match = matches[0]
        _, number, canonical_url = parse_issue_url(str(match.get("url") or ""))
        if str(match.get("title") or "") != title or str(match.get("body") or "") != body:
            if str(match.get("state") or "").upper() == "CLOSED":
                raise TicketFinalizeError(f"github_issue_closed_content_mismatch:{ticket_id}")
            _, body_path = _body_file(ticket_id, body)
            try:
                _github_text(
                    runner,
                    ["gh", "issue", "edit", str(number), "--repo", configured_repository, "--title", title, "--body-file", str(body_path)],
                    project_root,
                )
            finally:
                body_path.unlink(missing_ok=True)
        return canonical_url
    _, body_path = _body_file(ticket_id, body)
    try:
        output = _github_text(
            runner,
            ["gh", "issue", "create", "--repo", configured_repository, "--title", title, "--body-file", str(body_path)],
            project_root,
        )
    finally:
        body_path.unlink(missing_ok=True)
    match = re.search(r"https://github\.com/[^\s]+/issues/[1-9]\d*", output)
    if not match:
        raise TicketFinalizeError("github_issue_create_url_missing")
    repository, _, canonical_url = parse_issue_url(match.group(0))
    if repository != configured_repository:
        raise TicketFinalizeError(f"github_issue_repo_mismatch:expected={configured_repository}:actual={repository}")
    return canonical_url


def verify_github_issue(
    ticket_id: str,
    issue_url: str,
    expected_media: Sequence[dict[str, str]],
    runner: GitHubRunner,
    *,
    project_root: Path,
    configured_repository: str,
    require_closed: bool = True,
) -> dict[str, Any]:
    url_repository, issue_number, canonical_url = parse_issue_url(issue_url)
    if url_repository != configured_repository:
        raise TicketFinalizeError(f"github_issue_repo_mismatch:expected={configured_repository}:actual={url_repository}")
    issue = _github_json(
        runner,
        ["gh", "issue", "view", str(issue_number), "--repo", configured_repository, "--json", "number,title,state,stateReason,body,comments,closedAt,url"],
        project_root,
    )
    try:
        returned_repository, returned_number, returned_url = parse_issue_url(str(issue.get("url") or ""))
    except TicketFinalizeError as exc:
        raise TicketFinalizeError("github_issue_response_url_invalid") from exc
    if returned_repository != configured_repository or returned_number != issue_number or returned_url != canonical_url:
        raise TicketFinalizeError("github_issue_response_mismatch")
    if int(issue.get("number") or 0) != issue_number:
        raise TicketFinalizeError("github_issue_number_mismatch")
    state = str(issue.get("state") or "").upper()
    if state not in {"OPEN", "CLOSED"}:
        raise TicketFinalizeError(f"github_issue_state_invalid:{issue_number}:{state or 'missing'}")
    if require_closed and state != "CLOSED":
        raise TicketFinalizeError(f"github_issue_not_closed:{issue_number}")
    reason = str(issue.get("stateReason") or "").upper()
    if state == "CLOSED" and reason != "COMPLETED":
        raise TicketFinalizeError(f"github_issue_state_reason_invalid:{issue_number}:{reason or 'missing'}")
    closed_at = str(issue.get("closedAt") or "").strip()
    if state == "CLOSED" and not closed_at:
        raise TicketFinalizeError(f"github_issue_closed_at_missing:{issue_number}")
    body = str(issue.get("body") or "")
    ticket_marker = f"<!-- farplane-ticket-id:{ticket_id} -->"
    if body.count(ticket_marker) != 1:
        raise TicketFinalizeError(f"github_issue_ticket_marker_missing:{ticket_id}")
    for heading in ("Before", "After", "Example", "Key decisions", "Proof"):
        match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)", body)
        section = match.group(1).replace(ticket_marker, "").strip() if match else ""
        if not section:
            raise TicketFinalizeError(f"github_issue_section_missing:{heading.lower().replace(' ', '_')}")
    title = str(issue.get("title") or "").strip()
    if not title:
        raise TicketFinalizeError(f"github_issue_title_missing:{issue_number}")
    comments = issue.get("comments")
    if not isinstance(comments, list):
        raise TicketFinalizeError("github_issue_comments_invalid")
    media_urls: list[str] = []
    for media in expected_media:
        marker = f"<!-- farplane-ticket-media:{ticket_id}:{media['sha256']} -->"
        matches = [comment for comment in comments if isinstance(comment, dict) and marker in str(comment.get("body") or "")]
        count = sum(str(comment.get("body") or "").count(marker) for comment in comments if isinstance(comment, dict))
        if count != 1 or len(matches) != 1:
            raise TicketFinalizeError(f"github_issue_media_marker_count:{media['sha256']}:{count}")
        matched_body = str(matches[0].get("body") or "")
        if re.search(r"https://github\.com/user-attachments/(?:assets|files)/[^\s)<>'\"]+", matched_body) is None:
            raise TicketFinalizeError(f"github_issue_media_attachment_missing:{media['sha256']}")
        matched_url = str(matches[0].get("url") or "")
        parsed = urlparse(matched_url)
        if not matched_url:
            raise TicketFinalizeError(f"github_issue_media_comment_url_missing:{media['sha256']}")
        if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.path != urlparse(canonical_url).path or re.fullmatch(r"issuecomment-[1-9]\d*", parsed.fragment) is None:
            raise TicketFinalizeError(f"github_issue_media_comment_url_invalid:{media['sha256']}")
        media_urls.append(matched_url)
    return {
        "github_issue_url": canonical_url,
        "github_issue_number": issue_number,
        "title": title,
        "remote_state": state.lower(),
        "closed_at": closed_at,
        "media_comment_urls": media_urls,
    }


def close_issue(
    issue_url: str,
    runner: GitHubRunner,
    *,
    project_root: Path,
    configured_repository: str,
) -> None:
    _, issue_number, _ = parse_issue_url(issue_url)
    _github_text(
        runner,
        ["gh", "issue", "close", str(issue_number), "--repo", configured_repository, "--reason", "completed"],
        project_root,
    )
