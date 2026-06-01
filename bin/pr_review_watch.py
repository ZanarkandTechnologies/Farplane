#!/usr/bin/env python3
"""Normalize pull-request review state for the pr-review-watch skill."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


TERMINAL_SUCCESS = {"success", "neutral", "skipped", "pass", "passing"}
TERMINAL_FAILURE = {"failure", "fail", "failing", "timed_out", "cancelled", "action_required"}
PENDING_STATES = {"queued", "pending", "in_progress", "requested", "waiting", "expected"}


class PipelineConfigError(Exception):
    """Raised when project PR review memory is missing or invalid."""


@dataclass(frozen=True)
class PrReviewPipelineConfig:
    providers: list[str]
    poll_interval_minutes: int
    max_iterations: int
    pass_conditions: dict[str, bool]
    fix_commands: list[str]
    review_commands: list[str]
    notification_policy: dict[str, object]
    source_path: str


@dataclass(frozen=True)
class PullRequestWatchSnapshot:
    repo: str
    branch: str | None
    pr_number: int | None
    pr_url: str | None
    head_sha: str | None
    check_runs: list[dict[str, object]]
    reviews: list[dict[str, object]]
    review_comments: list[dict[str, object]]
    provider_comments: list[dict[str, object]]
    errors: list[dict[str, object]]
    fetched_at: str


@dataclass(frozen=True)
class ActionableReviewItem:
    provider: str
    severity: str
    file: str | None
    line: int | None
    body: str
    url: str | None
    suggested_action: str


@dataclass(frozen=True)
class WatchVerdict:
    state: Literal["pass", "wait", "actionable", "blocked"]
    actionable_items: list[ActionableReviewItem] = field(default_factory=list)
    blocking_items: list[str] = field(default_factory=list)
    next_wait_minutes: int | None = None
    terminal_message: str | None = None


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _run_json(command: list[str], cwd: Path) -> tuple[dict[str, object] | list[object] | None, str | None]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        return None, f"missing command: {command[0]}"

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        return None, detail
    try:
        return json.loads(result.stdout or "{}"), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON from {' '.join(command)}: {exc}"


def _git_branch(repo_path: Path) -> str | None:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _extract_json_blocks(text: str) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    for match in re.finditer(r"```(?:json)?[^\n]*\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE):
        body = match.group(1).strip()
        if not body:
            continue
        try:
            value = json.loads(body)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            blocks.append(value)
    return blocks


def _normalize_string_list(value: object, field_name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise PipelineConfigError(f"{field_name} must be a list of strings")
    return value


def _int_field(raw_pipeline: dict[str, object], field_name: str, default: int) -> int:
    try:
        return int(raw_pipeline.get(field_name, default))
    except (TypeError, ValueError) as exc:
        raise PipelineConfigError(f"{field_name} must be an integer") from exc


def _bool_field(raw_conditions: dict[str, object], field_name: str, default: bool) -> bool:
    value = raw_conditions.get(field_name, default)
    if not isinstance(value, bool):
        raise PipelineConfigError(f"{field_name} must be a boolean")
    return value


def parse_project_pipeline(text: str, source_path: str) -> PrReviewPipelineConfig:
    for block in _extract_json_blocks(text):
        raw_pipeline = block.get("pr_review_pipeline")
        if not isinstance(raw_pipeline, dict):
            continue

        providers = _normalize_string_list(raw_pipeline.get("providers", ["github"]), "providers")
        if not providers:
            raise PipelineConfigError("providers must not be empty")

        poll_interval = _int_field(raw_pipeline, "poll_interval_minutes", 10)
        if poll_interval < 5 or poll_interval > 10:
            raise PipelineConfigError("poll_interval_minutes must be between 5 and 10")

        max_iterations = _int_field(raw_pipeline, "max_iterations", 12)
        if max_iterations < 1:
            raise PipelineConfigError("max_iterations must be at least 1")

        raw_pass_conditions = raw_pipeline.get("pass_conditions", {})
        if raw_pass_conditions is None:
            raw_pass_conditions = {}
        if not isinstance(raw_pass_conditions, dict):
            raise PipelineConfigError("pass_conditions must be an object")
        pass_conditions = {
            "require_checks_pass": _bool_field(raw_pass_conditions, "require_checks_pass", True),
            "require_no_actionable_comments": _bool_field(
                raw_pass_conditions, "require_no_actionable_comments", True
            ),
            "require_approval": _bool_field(raw_pass_conditions, "require_approval", False),
        }

        raw_notification = raw_pipeline.get("notification_policy", {})
        if raw_notification is None:
            raw_notification = {}
        if not isinstance(raw_notification, dict):
            raise PipelineConfigError("notification_policy must be an object")

        return PrReviewPipelineConfig(
            providers=providers,
            poll_interval_minutes=poll_interval,
            max_iterations=max_iterations,
            pass_conditions=pass_conditions,
            fix_commands=_normalize_string_list(raw_pipeline.get("fix_commands"), "fix_commands"),
            review_commands=_normalize_string_list(
                raw_pipeline.get("review_commands"), "review_commands"
            ),
            notification_policy=raw_notification,
            source_path=source_path,
        )

    raise PipelineConfigError("missing fenced JSON block with pr_review_pipeline")


def load_project_pipeline(repo_path: Path) -> PrReviewPipelineConfig:
    candidates = [repo_path / "docs" / "pr-review-pipeline.md", repo_path / "PROJECT_RULES.md"]
    errors: list[str] = []
    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            return parse_project_pipeline(candidate.read_text(encoding="utf-8"), str(candidate))
        except PipelineConfigError as exc:
            errors.append(f"{candidate}: {exc}")
    if errors:
        raise PipelineConfigError("; ".join(errors))
    raise PipelineConfigError("missing docs/pr-review-pipeline.md or PROJECT_RULES.md")


def _normalize_check_runs(raw_checks: object) -> list[dict[str, object]]:
    if not isinstance(raw_checks, list):
        return []
    normalized: list[dict[str, object]] = []
    for check in raw_checks:
        if not isinstance(check, dict):
            continue
        name = check.get("name") or check.get("context") or check.get("workflowName") or "unnamed"
        status = check.get("status") or check.get("state") or check.get("bucket") or ""
        conclusion = check.get("conclusion") or check.get("state") or check.get("bucket")
        normalized.append(
            {
                "name": str(name),
                "status": str(status).lower() if status is not None else "",
                "conclusion": str(conclusion).lower() if conclusion is not None else None,
                "url": check.get("url") or check.get("link"),
            }
        )
    return normalized


def _normalize_reviews(raw_reviews: object) -> list[dict[str, object]]:
    if not isinstance(raw_reviews, list):
        return []
    normalized: list[dict[str, object]] = []
    for review in raw_reviews:
        if not isinstance(review, dict):
            continue
        author = review.get("author")
        if isinstance(author, dict):
            author = author.get("login")
        normalized.append(
            {
                "author": author,
                "state": str(review.get("state", "")).upper(),
                "body": review.get("body") or "",
                "url": review.get("url"),
            }
        )
    return normalized


def _normalize_comments(raw_comments: object) -> list[dict[str, object]]:
    if not isinstance(raw_comments, list):
        return []
    normalized: list[dict[str, object]] = []
    for comment in raw_comments:
        if not isinstance(comment, dict):
            continue
        author = comment.get("author")
        if isinstance(author, dict):
            author = author.get("login")
        normalized.append(
            {
                "provider": comment.get("provider") or "github",
                "author": author,
                "file": comment.get("path") or comment.get("file"),
                "line": comment.get("line"),
                "body": comment.get("body") or "",
                "url": comment.get("url"),
                "resolved": bool(comment.get("resolved", False)),
            }
        )
    return normalized


def discover(repo_path: Path, pr: int | None = None) -> PullRequestWatchSnapshot:
    errors: list[dict[str, object]] = []
    branch = _git_branch(repo_path)
    pr_selector = str(pr) if pr is not None else None

    view_command = [
        "gh",
        "pr",
        "view",
        *(["--json"] if pr_selector is None else [pr_selector, "--json"]),
        "number,url,headRefName,headRefOid,reviews,comments",
    ]
    raw_view, view_error = _run_json(view_command, repo_path)
    if view_error is not None:
        errors.append({"kind": "provider", "message": view_error})
        return PullRequestWatchSnapshot(
            repo=str(repo_path),
            branch=branch,
            pr_number=pr,
            pr_url=None,
            head_sha=None,
            check_runs=[],
            reviews=[],
            review_comments=[],
            provider_comments=[],
            errors=errors,
            fetched_at=_now(),
        )
    if not isinstance(raw_view, dict):
        raw_view = {}

    pr_number_raw = raw_view.get("number") or pr
    pr_number = int(pr_number_raw) if pr_number_raw is not None else None
    checks_command = [
        "gh",
        "pr",
        "checks",
        *(str(pr_number) for _ in [0] if pr_number is not None),
        "--json",
        "name,state,conclusion,link,bucket",
    ]
    raw_checks, checks_error = _run_json(checks_command, repo_path)
    if checks_error is not None:
        errors.append({"kind": "checks", "message": checks_error})

    return PullRequestWatchSnapshot(
        repo=str(repo_path),
        branch=str(raw_view.get("headRefName") or branch or ""),
        pr_number=pr_number,
        pr_url=str(raw_view.get("url") or "") or None,
        head_sha=str(raw_view.get("headRefOid") or "") or None,
        check_runs=_normalize_check_runs(raw_checks),
        reviews=_normalize_reviews(raw_view.get("reviews")),
        review_comments=_normalize_comments(raw_view.get("comments")),
        provider_comments=[],
        errors=errors,
        fetched_at=_now(),
    )


def load_fixture(path: Path) -> PullRequestWatchSnapshot:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("fixture must contain a JSON object")
    return PullRequestWatchSnapshot(
        repo=str(data.get("repo") or ""),
        branch=data.get("branch") if isinstance(data.get("branch"), str) else None,
        pr_number=data.get("pr_number") if isinstance(data.get("pr_number"), int) else None,
        pr_url=data.get("pr_url") if isinstance(data.get("pr_url"), str) else None,
        head_sha=data.get("head_sha") if isinstance(data.get("head_sha"), str) else None,
        check_runs=data.get("check_runs") if isinstance(data.get("check_runs"), list) else [],
        reviews=data.get("reviews") if isinstance(data.get("reviews"), list) else [],
        review_comments=data.get("review_comments")
        if isinstance(data.get("review_comments"), list)
        else [],
        provider_comments=data.get("provider_comments")
        if isinstance(data.get("provider_comments"), list)
        else [],
        errors=data.get("errors") if isinstance(data.get("errors"), list) else [],
        fetched_at=str(data.get("fetched_at") or _now()),
    )


def _comment_to_actionable(comment: dict[str, object]) -> ActionableReviewItem:
    line = comment.get("line")
    return ActionableReviewItem(
        provider=str(comment.get("provider") or "github"),
        severity=str(comment.get("severity") or "warning"),
        file=str(comment.get("file")) if comment.get("file") is not None else None,
        line=line if isinstance(line, int) else None,
        body=str(comment.get("body") or ""),
        url=str(comment.get("url")) if comment.get("url") is not None else None,
        suggested_action="address unresolved review comment",
    )


def _check_to_actionable(check: dict[str, object]) -> ActionableReviewItem:
    return ActionableReviewItem(
        provider="github",
        severity="error",
        file=None,
        line=None,
        body=f"Check failed: {check.get('name', 'unnamed')}",
        url=str(check.get("url")) if check.get("url") is not None else None,
        suggested_action="run configured fix commands and inspect failing check",
    )


def classify(snapshot: PullRequestWatchSnapshot, config: PrReviewPipelineConfig) -> WatchVerdict:
    blocking_items: list[str] = []
    actionable_items: list[ActionableReviewItem] = []
    pending_items: list[str] = []

    if snapshot.errors:
        for error in snapshot.errors:
            message = error.get("message") if isinstance(error, dict) else str(error)
            blocking_items.append(str(message))
        return WatchVerdict(
            state="blocked",
            blocking_items=blocking_items,
            terminal_message=_terminal_message(
                snapshot,
                "PR review watch blocked by provider/config error.",
            ),
        )

    if snapshot.pr_number is None:
        return WatchVerdict(
            state="blocked",
            blocking_items=["No active pull request was found."],
            terminal_message="PR review watch blocked because no active PR was found.",
        )

    if config.pass_conditions.get("require_checks_pass", True):
        for check in snapshot.check_runs:
            status = str(check.get("status") or "").lower()
            conclusion = str(check.get("conclusion") or "").lower()
            if status in PENDING_STATES or conclusion in PENDING_STATES or not conclusion:
                pending_items.append(f"Check pending: {check.get('name', 'unnamed')}")
                continue
            if conclusion in TERMINAL_FAILURE or (
                status == "completed" and conclusion not in TERMINAL_SUCCESS
            ):
                actionable_items.append(_check_to_actionable(check))

    review_states = {str(review.get("state") or "").upper() for review in snapshot.reviews}
    if "CHANGES_REQUESTED" in review_states:
        actionable_items.append(
            ActionableReviewItem(
                provider="github",
                severity="error",
                file=None,
                line=None,
                body="A GitHub review requested changes.",
                url=None,
                suggested_action="inspect requested changes and update the PR",
            )
        )
    if config.pass_conditions.get("require_approval", False) and "APPROVED" not in review_states:
        pending_items.append("Approval is required but no approving review was found.")

    if config.pass_conditions.get("require_no_actionable_comments", True):
        for comment in [*snapshot.review_comments, *snapshot.provider_comments]:
            if not isinstance(comment, dict):
                continue
            if bool(comment.get("resolved", False)):
                continue
            actionable_items.append(_comment_to_actionable(comment))

    if actionable_items:
        return WatchVerdict(
            state="actionable",
            actionable_items=actionable_items,
            next_wait_minutes=None,
            terminal_message=None,
        )
    if pending_items:
        return WatchVerdict(
            state="wait",
            blocking_items=pending_items,
            next_wait_minutes=config.poll_interval_minutes,
            terminal_message=None,
        )
    return WatchVerdict(
        state="pass",
        terminal_message=_terminal_message(
            snapshot,
            f"PR #{snapshot.pr_number} passed configured review watch conditions.",
        ),
    )


def _terminal_message(snapshot: PullRequestWatchSnapshot, message: str) -> str:
    if snapshot.pr_url:
        return f"{message} {snapshot.pr_url}"
    return message


def _json_default(value: object) -> object:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _load_config_from_args(repo_path: Path, config_path: str | None) -> PrReviewPipelineConfig:
    if config_path:
        path = Path(config_path)
        return parse_project_pipeline(path.read_text(encoding="utf-8"), str(path))
    return load_project_pipeline(repo_path)


def _blocked_for_config_error(message: str) -> WatchVerdict:
    return WatchVerdict(
        state="blocked",
        blocking_items=[message],
        terminal_message="PR review watch blocked by missing or invalid project pipeline config.",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    classify_parser = subparsers.add_parser("classify", help="classify fixture or live PR state")
    classify_parser.add_argument("--repo", default=".", help="target repository path")
    classify_parser.add_argument("--pr", type=int, help="pull request number")
    classify_parser.add_argument("--fixture", help="fixture JSON snapshot")
    classify_parser.add_argument("--config", help="pipeline Markdown file")
    classify_parser.add_argument("--json", action="store_true", help="emit JSON")

    args = parser.parse_args(argv)
    repo_path = Path(args.repo).resolve()

    if args.command == "classify":
        snapshot = load_fixture(Path(args.fixture)) if args.fixture else discover(repo_path, args.pr)
        try:
            config = _load_config_from_args(repo_path, args.config)
            verdict = classify(snapshot, config)
        except PipelineConfigError as exc:
            config = None
            verdict = _blocked_for_config_error(str(exc))

        payload = {
            "snapshot": asdict(snapshot),
            "config": asdict(config) if config is not None else None,
            "verdict": asdict(verdict),
        }
        if args.json:
            print(json.dumps(payload, default=_json_default, indent=2, sort_keys=True))
        else:
            print(f"state={verdict.state}")
            if verdict.terminal_message:
                print(verdict.terminal_message)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
