#!/usr/bin/env python3
"""Tests for notion_tasks_this_week.py."""

from __future__ import annotations

import unittest
import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch

BIN_DIR = Path(__file__).resolve().parent
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import notion_tasks_this_week as ntw


class NotionTasksThisWeekTests(unittest.TestCase):
    def test_build_query_payload_filters_act_time_and_incomplete_status(self) -> None:
        payload = ntw.build_query_payload(
            ntw.QueryWindow(date(2026, 5, 16), date(2026, 5, 23)),
            page_size=50,
        )
        self.assertEqual(payload["page_size"], 50)
        filters = payload["filter"]["and"]
        self.assertEqual(filters[0], {"property": "Act Time", "date": {"on_or_after": "2026-05-16"}})
        self.assertEqual(filters[1], {"property": "Act Time", "date": {"on_or_before": "2026-05-23"}})
        self.assertEqual(filters[2], {"property": "Status", "status": {"does_not_equal": "Done"}})

    def test_default_window_uses_lookback_days(self) -> None:
        window = ntw.default_window(date(2026, 5, 23), lookback_days=7)
        self.assertEqual(window.start, date(2026, 5, 16))
        self.assertEqual(window.end, date(2026, 5, 23))

    def test_normalize_page_extracts_task_fields(self) -> None:
        page = {
            "url": "https://www.notion.so/task",
            "properties": {
                "Name": {"title": [{"plain_text": "Fix fallback"}]},
                "Status": {"status": {"name": "Review"}},
                "Act Time": {"date": {"start": "2026-05-23", "end": None}},
                "Project": {"relation": [{"id": "abc-def"}]},
                "Projects": {"relation": [{"id": "123-456"}]},
                "Related Entities": {"relation": [{"id": "789-abc"}]},
                "Description": {"rich_text": [{"plain_text": "desc"}]},
                "Attention Required": {"select": {"name": "Foreground"}},
                "Pinned": {"checkbox": True},
                "Tags": {"multi_select": [{"name": "Technical"}]},
            },
        }
        row = ntw.normalize_page(page)
        self.assertEqual(row["Name"], "Fix fallback")
        self.assertEqual(row["Status"], "Review")
        self.assertEqual(row["Act Time"], {"start": "2026-05-23", "end": None})
        self.assertEqual(row["Project"], ["https://www.notion.so/abcdef"])
        self.assertEqual(row["Projects"], ["https://www.notion.so/123456"])
        self.assertEqual(row["Related Entities"], ["https://www.notion.so/789abc"])
        self.assertEqual(row["Attention Required"], "Foreground")
        self.assertTrue(row["Pinned"])
        self.assertEqual(row["Tags"], ["Technical"])
        self.assertEqual(row["execution_context"], "needs_project_context")
        self.assertEqual(row["context_gap"], "api_data_source_query_project_context_not_enriched")

    def test_query_tasks_preserves_any_non_done_status_returned_by_notion(self) -> None:
        active_page = {
            "url": "https://www.notion.so/task-active",
            "properties": {
                "Name": {"title": [{"plain_text": "Blocked task"}]},
                "Status": {"status": {"name": "Blocked"}},
                "Act Time": {"date": {"start": "2026-05-23", "end": None}},
            },
        }
        done_page = {
            "url": "https://www.notion.so/task-done",
            "properties": {
                "Name": {"title": [{"plain_text": "Done task"}]},
                "Status": {"status": {"name": "Done"}},
                "Act Time": {"date": {"start": "2026-05-23", "end": None}},
            },
        }

        with patch.object(
            ntw,
            "notion_request",
            return_value={"results": [active_page, done_page], "has_more": False},
        ):
            rows = ntw.query_tasks(
                token="token",
                data_source_id="source",
                window=ntw.QueryWindow(date(2026, 5, 16), date(2026, 5, 23)),
                page_size=100,
                version="2026-03-11",
            )

        self.assertEqual([row["Name"] for row in rows], ["Blocked task"])

    def test_main_rejects_partial_custom_date_range(self) -> None:
        with patch.dict("os.environ", {"NOTION_API_KEY": "token"}):
            self.assertEqual(ntw.main(["--start", "2026-05-16"]), 2)


if __name__ == "__main__":
    unittest.main()
