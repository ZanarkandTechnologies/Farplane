#!/usr/bin/env python3
"""Fetch incomplete Notion Tasks rows by Act Time date range.

This is a deterministic fallback for sessions where the Notion MCP can fetch
database metadata but cannot query saved-view rows. It uses the public Notion
Data Sources API when NOTION_API_KEY or NOTION_TOKEN is available.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any


DEFAULT_TASKS_DATA_SOURCE_ID = "43a439fd-74c5-4b43-9afb-950f047e5d4f"
DEFAULT_NOTION_VERSION = "2026-03-11"


class NotionTasksError(RuntimeError):
    """Raised when the Notion task fallback cannot complete."""


@dataclass(frozen=True)
class QueryWindow:
    start: date
    end: date


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid ISO date: {value}") from exc


def default_window(today: date | None = None, lookback_days: int = 7) -> QueryWindow:
    end = today or date.today()
    return QueryWindow(start=end - timedelta(days=lookback_days), end=end)


def title_text(title_property: dict[str, Any]) -> str:
    title_items = title_property.get("title")
    if not isinstance(title_items, list):
        return ""
    return "".join(
        item.get("plain_text", "")
        for item in title_items
        if isinstance(item, dict)
    ).strip()


def plain_rich_text(text_property: dict[str, Any]) -> str:
    rich_text = text_property.get("rich_text")
    if not isinstance(rich_text, list):
        return ""
    return "".join(
        item.get("plain_text", "")
        for item in rich_text
        if isinstance(item, dict)
    ).strip()


def select_name(select_property: dict[str, Any]) -> str:
    value = select_property.get("select")
    return value.get("name", "") if isinstance(value, dict) else ""


def status_name(status_property: dict[str, Any]) -> str:
    value = status_property.get("status")
    return value.get("name", "") if isinstance(value, dict) else ""


def checkbox_value(checkbox_property: dict[str, Any]) -> bool:
    return checkbox_property.get("checkbox") is True


def date_value(date_property: dict[str, Any]) -> dict[str, str | None]:
    value = date_property.get("date")
    if not isinstance(value, dict):
        return {"start": None, "end": None}
    return {"start": value.get("start"), "end": value.get("end")}


def relation_urls(relation_property: dict[str, Any]) -> list[str]:
    relation = relation_property.get("relation")
    if not isinstance(relation, list):
        return []
    urls: list[str] = []
    for item in relation:
        if not isinstance(item, dict):
            continue
        page_id = str(item.get("id", "")).replace("-", "")
        if page_id:
            urls.append(f"https://www.notion.so/{page_id}")
    return urls


def multi_select_names(property_value: dict[str, Any]) -> list[str]:
    values = property_value.get("multi_select")
    if not isinstance(values, list):
        return []
    return [
        item.get("name", "")
        for item in values
        if isinstance(item, dict) and item.get("name")
    ]


def is_not_done_status(status: str) -> bool:
    return status.strip().casefold() != "done"


def normalize_page(page: dict[str, Any]) -> dict[str, Any]:
    properties = page.get("properties")
    if not isinstance(properties, dict):
        raise NotionTasksError("page missing properties")
    act_time = date_value(properties.get("Act Time", {}))
    return {
        "Name": title_text(properties.get("Name", {})),
        "Status": status_name(properties.get("Status", {})),
        "Act Time": act_time,
        "Project": relation_urls(properties.get("Project", {})),
        "Projects": relation_urls(properties.get("Projects", {})),
        "Related Entities": relation_urls(properties.get("Related Entities", {})),
        "Description": plain_rich_text(properties.get("Description", {})),
        "Attention Required": select_name(properties.get("Attention Required", {})),
        "Pinned": checkbox_value(properties.get("Pinned", {})),
        "Tags": multi_select_names(properties.get("Tags", {})),
        "execution_context": "needs_project_context",
        "context_gap": "api_data_source_query_project_context_not_enriched",
        "url": page.get("url"),
    }


def build_query_payload(window: QueryWindow, page_size: int, start_cursor: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "page_size": page_size,
        "filter": {
            "and": [
                {
                    "property": "Act Time",
                    "date": {"on_or_after": window.start.isoformat()},
                },
                {
                    "property": "Act Time",
                    "date": {"on_or_before": window.end.isoformat()},
                },
                {
                    "property": "Status",
                    "status": {"does_not_equal": "Done"},
                },
            ]
        },
        "sorts": [
            {"property": "Act Time", "direction": "ascending"},
            {"property": "Status", "direction": "ascending"},
        ],
    }
    if start_cursor:
        payload["start_cursor"] = start_cursor
    return payload


def notion_request(url: str, token: str, version: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": version,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise NotionTasksError(f"Notion API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise NotionTasksError(f"Notion API request failed: {exc.reason}") from exc
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise NotionTasksError("Notion API response was not an object")
    return data


def query_tasks(
    *,
    token: str,
    data_source_id: str,
    window: QueryWindow,
    page_size: int,
    version: str,
) -> list[dict[str, Any]]:
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    rows: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        payload = build_query_payload(window, page_size, cursor)
        data = notion_request(url, token, version, payload)
        results = data.get("results")
        if not isinstance(results, list):
            raise NotionTasksError("Notion API response missing results")
        for page in results:
            if isinstance(page, dict):
                normalized = normalize_page(page)
                if is_not_done_status(str(normalized["Status"])):
                    rows.append(normalized)
        if data.get("has_more") is not True:
            return rows
        next_cursor = data.get("next_cursor")
        if not isinstance(next_cursor, str) or not next_cursor:
            return rows
        cursor = next_cursor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-source-id", default=DEFAULT_TASKS_DATA_SOURCE_ID)
    parser.add_argument("--start", type=parse_date)
    parser.add_argument("--end", type=parse_date)
    parser.add_argument("--lookback-days", type=int, default=7)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument(
        "--notion-version",
        default=os.environ.get("NOTION_VERSION", DEFAULT_NOTION_VERSION),
    )
    parser.add_argument("--json", action="store_true", help="print normalized JSON rows")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    token = os.environ.get("NOTION_API_KEY") or os.environ.get("NOTION_TOKEN")
    if not token:
        print("error: set NOTION_API_KEY or NOTION_TOKEN for API-backed fallback", file=sys.stderr)
        return 2
    if bool(args.start) != bool(args.end):
        print("error: provide both --start and --end, or neither", file=sys.stderr)
        return 2
    window = QueryWindow(args.start, args.end) if args.start and args.end else default_window(lookback_days=args.lookback_days)
    if window.start > window.end:
        print("error: --start must be on or before --end", file=sys.stderr)
        return 2
    try:
        rows = query_tasks(
            token=token,
            data_source_id=args.data_source_id,
            window=window,
            page_size=args.page_size,
            version=args.notion_version,
        )
    except NotionTasksError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"window": {"start": window.start.isoformat(), "end": window.end.isoformat()}, "rows": rows}, indent=2))
    else:
        for index, row in enumerate(rows, start=1):
            print(f"{index}. {row['Name']} [{row['Status']}] {row['Act Time']['start'] or ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
