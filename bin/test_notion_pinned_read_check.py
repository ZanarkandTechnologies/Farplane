#!/usr/bin/env python3
"""Tests for notion_pinned_read_check.py."""

from __future__ import annotations

import tempfile
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import notion_pinned_read_check as read_check


def pinned_row(
    *,
    url: str = "https://www.notion.so/task-a",
    name: str = "Pinned task",
    marker: str | None = "2026-05-24T01:00:00Z",
) -> dict[str, object]:
    row: dict[str, object] = {
        "url": url,
        "Name": name,
        "Pinned": "__YES__",
    }
    if marker is not None:
        row["last_edited_time"] = marker
    return row


class PinnedReadCheckTests(unittest.TestCase):
    def test_parse_tasks_filters_unpinned_rows(self) -> None:
        rows = [
            pinned_row(url="https://www.notion.so/pinned"),
            {"url": "https://www.notion.so/other", "Name": "Other", "Pinned": "__NO__"},
        ]
        tasks = read_check.parse_tasks(rows)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].url, "https://www.notion.so/pinned")

    def test_new_week_reads_all_pinned_tasks(self) -> None:
        tasks = read_check.parse_tasks([pinned_row(url="https://www.notion.so/a")])
        state = {
            "last_full_read_week": "2026-W20",
            "tasks": {
                "https://www.notion.so/a": {
                    "last_edited_time": "2026-05-24T01:00:00Z",
                    "last_read_at": "2026-05-18T00:00:00Z",
                }
            },
        }
        due, week_changed = read_check.due_tasks(
            tasks,
            state,
            current_week="2026-W21",
            weekly_full_read=True,
        )
        self.assertTrue(week_changed)
        self.assertEqual(due[0]["reasons"], ["weekly_full_read"])

    def test_same_week_reads_only_changed_tasks(self) -> None:
        tasks = read_check.parse_tasks(
            [
                pinned_row(url="https://www.notion.so/a", marker="2026-05-24T01:00:00Z"),
                pinned_row(url="https://www.notion.so/b", marker="2026-05-24T02:00:00Z"),
            ]
        )
        state = {
            "last_full_read_week": "2026-W21",
            "tasks": {
                "https://www.notion.so/a": {"last_edited_time": "2026-05-24T01:00:00Z"},
                "https://www.notion.so/b": {"last_edited_time": "2026-05-23T02:00:00Z"},
            },
        }
        due, week_changed = read_check.due_tasks(
            tasks,
            state,
            current_week="2026-W21",
            weekly_full_read=True,
        )
        self.assertFalse(week_changed)
        self.assertEqual([item["url"] for item in due], ["https://www.notion.so/b"])
        self.assertEqual(due[0]["reasons"], ["last_edited_changed"])

    def test_missing_update_marker_requires_read(self) -> None:
        tasks = read_check.parse_tasks([pinned_row(marker=None)])
        state = {
            "last_full_read_week": "2026-W21",
            "tasks": {"https://www.notion.so/task-a": {"last_edited_time": None}},
        }
        due, _ = read_check.due_tasks(
            tasks,
            state,
            current_week="2026-W21",
            weekly_full_read=True,
        )
        self.assertEqual(due[0]["reasons"], ["missing_update_marker"])

    def test_record_reads_updates_state_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            tasks = read_check.parse_tasks([pinned_row()])
            next_state = read_check.record_reads(
                {"tasks": {}},
                tasks,
                {"https://www.notion.so/task-a"},
                current_week=read_check.iso_week(date(2026, 5, 24)),
                read_at="2026-05-24T01:23:00Z",
            )
            read_check.write_json(state_path, next_state)
            restored = read_check.read_json(state_path)
            self.assertEqual(restored["last_full_read_week"], "2026-W21")
            self.assertEqual(
                restored["tasks"]["https://www.notion.so/task-a"]["last_read_at"],
                "2026-05-24T01:23:00Z",
            )


if __name__ == "__main__":
    unittest.main()
