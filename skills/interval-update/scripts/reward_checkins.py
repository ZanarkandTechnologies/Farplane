#!/usr/bin/env python3
"""Find ticket reward check-ins that are due or scored poorly."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml


def parse_iso_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def missing(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(markdown: str) -> dict[str, Any]:
    if not markdown.startswith("---\n") or "\n---\n" not in markdown:
        return {}
    raw = markdown.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def markdown_heading_section(markdown: str, heading: str) -> str:
    target = f"## {heading}"
    lines = markdown.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def parse_fenced_yaml(section: str) -> dict[str, Any]:
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return {}
    yaml_start = section.find("\n", fence_start)
    fence_end = section.find("```", yaml_start + 1)
    if yaml_start == -1 or fence_end == -1:
        return {}
    try:
        loaded = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def iter_ticket_files(ticket_dir: Path, include_archive: bool = True) -> list[Path]:
    roots = [ticket_dir]
    if include_archive:
        roots.append(ticket_dir / "archive")
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(root.glob("TASK-*/ticket.md"))
    return sorted(set(files))


def reward_items(
    ticket_dir: Path,
    now: datetime,
    lookback_days: int,
    include_archive: bool,
) -> dict[str, Any]:
    due: list[dict[str, Any]] = []
    not_due: list[dict[str, Any]] = []
    scored: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    legacy_missing_check_in: list[dict[str, Any]] = []
    cutoff = now - timedelta(days=lookback_days) if lookback_days > 0 else None
    root = ticket_dir.resolve()
    base = root.parent if root.name == "tickets" else root

    for path in iter_ticket_files(root, include_archive=include_archive):
        markdown = read_markdown(path)
        frontmatter = parse_frontmatter(markdown)
        ticket_id = str(frontmatter.get("ticket_id") or path.parent.name)
        rel_path = str(path.relative_to(base))
        reward = parse_fenced_yaml(markdown_heading_section(markdown, "Reward"))
        raw_rewards = reward.get("kpi_rewards")
        if not isinstance(raw_rewards, list):
            continue
        for index, raw_item in enumerate(raw_rewards):
            if not isinstance(raw_item, dict):
                gaps.append({"ticket": rel_path, "index": index, "gap": "invalid_reward_item"})
                continue
            check_in_at = parse_iso_datetime(raw_item.get("check_in_at"))
            item = {
                "ticket_id": ticket_id,
                "ticket": rel_path,
                "index": index,
                "kpi_id": str(raw_item.get("kpi_id") or ""),
                "expected_reward": str(raw_item.get("expected_reward") or ""),
                "check_in_at": str(raw_item.get("check_in_at") or ""),
                "actual_result": ""
                if raw_item.get("actual_result") is None
                else str(raw_item.get("actual_result")),
                "reward_score": raw_item.get("reward_score"),
                "reward_score_reason": ""
                if raw_item.get("reward_score_reason") is None
                else str(raw_item.get("reward_score_reason")),
                "status": str(frontmatter.get("status") or ""),
                "phase": str(frontmatter.get("phase") or ""),
            }
            if check_in_at is None:
                legacy_missing_check_in.append(item)
                continue
            if cutoff is not None and check_in_at < cutoff:
                continue
            if check_in_at > now:
                not_due.append(item)
                continue

            score_raw = raw_item.get("reward_score")
            actual_missing = missing(raw_item.get("actual_result"))
            score_missing = missing(score_raw)
            if actual_missing or score_missing:
                due.append(item)
                continue
            try:
                score = float(score_raw)
            except (TypeError, ValueError):
                gaps.append({"ticket": rel_path, "index": index, "gap": "invalid_reward_score"})
                due.append(item)
                continue
            if score < -1 or score > 1:
                gaps.append({"ticket": rel_path, "index": index, "gap": "reward_score_out_of_range"})
                due.append(item)
                continue
            next_item = dict(item)
            next_item["reward_score"] = score
            scored.append(next_item)

    return {
        "due": due,
        "not_due": not_due,
        "scored": scored,
        "gaps": gaps,
        "legacy_missing_check_in": legacy_missing_check_in,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket-dir", default="tickets")
    parser.add_argument("--now", default="")
    parser.add_argument("--lookback-days", type=int, default=14)
    parser.add_argument("--bad-threshold", type=float, default=0.5)
    parser.add_argument("--active-only", action="store_true")
    args = parser.parse_args()

    now = parse_iso_datetime(args.now) if args.now else datetime.now(timezone.utc)
    if now is None:
        parser.error("--now must be ISO-8601 when supplied")
    packet = reward_items(
        Path(args.ticket_dir),
        now=now,
        lookback_days=args.lookback_days,
        include_archive=not args.active_only,
    )
    bad_predictions = [
        item
        for item in packet["scored"]
        if isinstance(item.get("reward_score"), float)
        and item["reward_score"] < args.bad_threshold
    ]
    output = {
        "now": now.isoformat(),
        "lookback_days": args.lookback_days,
        "bad_threshold": args.bad_threshold,
        "due": packet["due"],
        "bad_predictions": bad_predictions,
        "scored": packet["scored"],
        "not_due": packet["not_due"],
        "legacy_missing_check_in": packet["legacy_missing_check_in"],
        "gaps": packet["gaps"],
        "summary": {
            "due_count": len(packet["due"]),
            "bad_prediction_count": len(bad_predictions),
            "scored_count": len(packet["scored"]),
            "not_due_count": len(packet["not_due"]),
            "legacy_missing_check_in_count": len(packet["legacy_missing_check_in"]),
            "gap_count": len(packet["gaps"]),
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
