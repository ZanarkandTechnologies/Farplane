#!/usr/bin/env python3
"""Run a local Feed Scout pass from farplane/bindings.yaml#feed_scout."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from normalize_items import normalize  # noqa: E402


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def resolve_project_path(path: str) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    return candidate


def load_config(config_ref: str) -> dict[str, Any]:
    path_text, _, pointer = config_ref.partition("#")
    path = resolve_project_path(path_text)
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if pointer:
        for key in pointer.split("."):
            payload = payload[key]
    if not isinstance(payload, dict):
        raise ValueError(f"config ref did not resolve to an object: {config_ref}")
    return payload


def run_git(root: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        raise FileNotFoundError(path)
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            row = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL row: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_no}: row must be an object")
        rows.append(row)
    return rows


def profile_group_id(profile: dict[str, Any]) -> str:
    profile_id = str(profile["id"])
    return profile_id.removeprefix("x-").removeprefix("yt-").removeprefix("blog-")


def fixture_items_for_bootstrap(config: dict[str, Any], generated_at: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    bootstrap = config.get("bootstrap", {})
    if not isinstance(bootstrap, dict) or bootstrap.get("mode") != "skill_fixture":
        return [], [], []

    source_gaps: list[str] = []
    profiles_ref = bootstrap.get("profiles_ref")
    items_ref = bootstrap.get("items_ref")
    if not profiles_ref or not items_ref:
        return [], [], ["bootstrap: skill_fixture requires profiles_ref and items_ref"]

    try:
        profiles = read_jsonl(resolve_project_path(str(profiles_ref)))
        raw_items = read_jsonl(resolve_project_path(str(items_ref)))
    except (FileNotFoundError, ValueError) as exc:
        return [], [], [f"bootstrap: {exc}"]

    profiles_by_id = {
        str(profile["id"]): profile
        for profile in profiles
        if profile.get("enabled", True) and profile.get("id")
    }

    grouped_items: dict[str, list[dict[str, Any]]] = {}
    items: list[dict[str, Any]] = []
    for raw in raw_items:
        profile_id = str(raw.get("profile_id", ""))
        profile = profiles_by_id.get(profile_id)
        if not profile:
            source_gaps.append(f"{profile_id or 'unknown'}: missing enabled profile row")
            continue
        try:
            item = normalize(raw, generated_at)
        except ValueError as exc:
            source_gaps.append(f"{profile_id}: {exc}")
            continue
        group_id = profile_group_id(profile)
        item.update({
            "entity_group_id": group_id,
            "entity_group_name": profile.get("display_name", profile_id),
            "source_id": profile_id,
            "source_name": profile.get("display_name", profile_id),
            "tags": profile.get("tags", []),
        })
        items.append(item)
        grouped_items.setdefault(group_id, []).append(item)

    groups = []
    for profile_id, profile in profiles_by_id.items():
        group_id = profile_group_id(profile)
        group_items = grouped_items.get(group_id, [])
        groups.append({
            "id": group_id,
            "name": profile.get("display_name", profile_id),
            "kind": "profile",
            "tags": profile.get("tags", []),
            "sources": [{
                "id": profile_id,
                "name": profile.get("display_name", profile_id),
                "kind": profile.get("platform"),
                "fetch_method": profile.get("fetch_method"),
                "item_count": len(group_items),
                "enabled": True,
            }],
            "item_count": len(group_items),
        })

    return items, groups, source_gaps


def git_items_for_source(group: dict[str, Any], source: dict[str, Any], since: str, generated_at: str) -> tuple[list[dict[str, Any]], list[str]]:
    root = resolve_project_path(str(source.get("url", "")))
    if not root.exists():
        return [], [f"{source['id']}: missing local project path {root}"]
    if not (root / ".git").exists():
        return [], [f"{source['id']}: not a git repo {root}"]

    watch_paths = [str(path) for path in source.get("watch_paths", [])]
    git_args = ["log", f"--since={since}", "--date=iso-strict", "--pretty=format:%H%x1f%ad%x1f%s"]
    if watch_paths:
        git_args.extend(["--", *watch_paths])
    try:
        raw = run_git(root, git_args)
    except subprocess.CalledProcessError:
        return [], [f"{source['id']}: git log failed"]

    items: list[dict[str, Any]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        commit, published_at, title = line.split("\x1f", 2)
        canonical_key = f"git-{source['id']}-{commit[:12]}"
        items.append(
            {
                "canonical_key": canonical_key,
                "canonical_url": f"{root}#commit={commit}",
                "content_hash": commit,
                "discovered_at": generated_at,
                "entity_group_id": group["id"],
                "entity_group_name": group["name"],
                "kind": "repo_change",
                "platform": "local_git",
                "published_at": published_at,
                "source_id": source["id"],
                "source_name": source.get("name", source["id"]),
                "status": "new",
                "tags": list(dict.fromkeys([*group.get("tags", []), *source.get("tags", [])])),
                "title": title,
            }
        )
    return items, []


def read_seen_keys(ledger_path: Path) -> set[str]:
    if not ledger_path.exists():
        return set()
    keys: set[str] = set()
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        key = row.get("canonical_key")
        if isinstance(key, str):
            keys.add(key)
    return keys


def append_ledger(ledger_path: Path, items: list[dict[str, Any]]) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_seen_keys(ledger_path)
    with ledger_path.open("a", encoding="utf-8") as handle:
        for item in items:
            if item["canonical_key"] in existing:
                continue
            handle.write(json.dumps({
                "canonical_key": item["canonical_key"],
                "canonical_url": item["canonical_url"],
                "entity_group_id": item["entity_group_id"],
                "first_seen_at": item["discovered_at"],
                "last_seen_at": item["discovered_at"],
                "source_id": item["source_id"],
                "status": "seen",
            }, sort_keys=True) + "\n")


def write_outputs(config: dict[str, Any], config_ref: str, review_window: str) -> dict[str, Path]:
    generated = utc_now()
    generated_at = generated.isoformat().replace("+00:00", "Z")
    since = (generated - timedelta(days=1)).isoformat()
    date = generated.date().isoformat()

    source_gaps: list[str] = []
    items: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []

    bootstrap_items, bootstrap_groups, bootstrap_gaps = fixture_items_for_bootstrap(config, generated_at)
    items.extend(bootstrap_items)
    groups.extend(bootstrap_groups)
    source_gaps.extend(bootstrap_gaps)

    entity_rows = config.get("entities", {})
    if isinstance(entity_rows, list):
        entity_iter = [(str(group.get("id")), group) for group in entity_rows]
    else:
        entity_iter = list(entity_rows.items())

    for group_id, group in entity_iter:
        if not group.get("enabled", True):
            continue
        group = {"id": group_id, **group}
        group_items: list[dict[str, Any]] = []
        group_sources = []
        source_rows = group.get("sources", {})
        if isinstance(source_rows, list):
            source_iter = [(str(source.get("id")), source) for source in source_rows]
        else:
            source_iter = list(source_rows.items())
        for source_id, source in source_iter:
            if not source.get("enabled", True):
                continue
            source = {"id": source_id, **source}
            fetch_method = source.get("fetch_method")
            if fetch_method == "local_git":
                found, gaps = git_items_for_source(group, source, since, generated_at)
            else:
                found, gaps = [], [f"{source['id']}: unsupported fetch_method {fetch_method!r}"]
            source_gaps.extend(gaps)
            group_items.extend(found)
            items.extend(found)
            group_sources.append({
                "id": source["id"],
                "name": source.get("name", source["id"]),
                "kind": source.get("kind"),
                "fetch_method": fetch_method,
                "item_count": len(found),
                "enabled": True,
            })
        groups.append({
            "id": group["id"],
            "name": group.get("name", group["id"]),
            "kind": group.get("kind"),
            "tags": group.get("tags", []),
            "sources": group_sources,
            "item_count": len(group_items),
        })

    daily_root = resolve_project_path(config["daily_feed_root"])
    report_root = resolve_project_path(config["report_root"])
    ledger_path = resolve_project_path(config["ledger"])
    daily_root.mkdir(parents=True, exist_ok=True)
    report_root.mkdir(parents=True, exist_ok=True)

    seen = read_seen_keys(ledger_path)
    for item in items:
        if item["canonical_key"] in seen:
            item["status"] = "seen"

    feed_payload = {
        "schema": "farplane_feed_scout_daily_feed",
        "schema_version": "0.1.0",
        "config_ref": config_ref,
        "date": date,
        "generated_at": generated_at,
        "review_window": review_window,
        "summary": {
            "group_count": len(groups),
            "source_count": sum(len(group["sources"]) for group in groups),
            "item_count": len(items),
            "new_item_count": sum(1 for item in items if item["status"] == "new"),
            "source_gap_count": len(source_gaps),
        },
        "groups": groups,
        "items": items,
        "source_gaps": source_gaps,
    }

    feed_path = daily_root / f"feed-{date}.json"
    latest_feed = resolve_project_path(config.get("ui", {}).get("latest_feed", str(daily_root / "latest.json")))
    report_path = report_root / f"{generated.strftime('%Y-%m-%dT%H%M%SZ')}.md"
    latest_report = resolve_project_path(config["latest_report"])
    feed_payload["report_ref"] = str(report_path.relative_to(REPO_ROOT))
    feed_payload["latest_report_ref"] = str(latest_report.relative_to(REPO_ROOT))

    feed_text = json.dumps(feed_payload, indent=2, sort_keys=True) + "\n"
    feed_path.write_text(feed_text, encoding="utf-8")
    latest_feed.parent.mkdir(parents=True, exist_ok=True)
    latest_feed.write_text(feed_text, encoding="utf-8")

    report = [
        "---",
        "kind: feed-scout-report",
        f"generated_at: {generated_at}",
        f"config_ref: {config_ref}",
        f"daily_feed: {feed_path.relative_to(REPO_ROOT)}",
        "---",
        "",
        "# Feed Scout Report",
        "",
        f"- Groups: {feed_payload['summary']['group_count']}",
        f"- Sources: {feed_payload['summary']['source_count']}",
        f"- Items: {feed_payload['summary']['item_count']}",
        f"- New items: {feed_payload['summary']['new_item_count']}",
        f"- Source gaps: {feed_payload['summary']['source_gap_count']}",
        "",
        "## Groups",
        "",
    ]
    for group in groups:
        report.append(f"- `{group['id']}`: {group['item_count']} item(s)")
    if source_gaps:
        report.extend(["", "## Source Gaps", ""])
        report.extend(f"- {gap}" for gap in source_gaps)
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    latest_report.parent.mkdir(parents=True, exist_ok=True)
    latest_report.write_text(json.dumps({
        "schema": "farplane_feed_scout_latest_report",
        "generated_at": generated_at,
        "report_path": str(report_path.relative_to(REPO_ROOT)),
        "daily_feed_path": str(feed_path.relative_to(REPO_ROOT)),
        "summary": feed_payload["summary"],
        "source_gaps": source_gaps,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    append_ledger(ledger_path, [item for item in items if item["status"] == "new"])
    return {"feed": feed_path, "latest_feed": latest_feed, "report": report_path, "latest_report": latest_report}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-ref", default="farplane/bindings.yaml#feed_scout")
    parser.add_argument("--review-window", default="last_24h")
    args = parser.parse_args()

    config = load_config(args.config_ref)
    paths = write_outputs(config, args.config_ref, args.review_window)
    print(json.dumps({key: str(path.relative_to(REPO_ROOT)) for key, path in paths.items()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
