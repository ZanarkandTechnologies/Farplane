#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
from demo_shelf import demo_line, pick, shelf_issues


class DemoShelfTest(unittest.TestCase):
    def test_demo_line_points_at_the_fixed_tag(self):
        self.assertEqual(
            demo_line("Acme/widgets", 12),
            "🎬 Demo: https://github.com/Acme/widgets/releases/download/demos/issue-12.mp4",
        )

    def test_only_issue_videos_count_as_shelved(self):
        self.assertEqual(shelf_issues(["issue-3.mp4", "issue-10.mp4", "reel.mp4", "issue-4.mov", "issue-x.mp4"]), {3, 10})

    def test_pick_keeps_shelved_issues_closed_after_the_release_in_closing_order(self):
        issues = [
            {"number": 1, "closedAt": "2026-10-01T00:00:00Z"},
            {"number": 2, "closedAt": "2026-10-09T00:00:00Z"},
            {"number": 3, "closedAt": "2026-10-07T00:00:00Z"},
            {"number": 4, "closedAt": "2026-10-08T00:00:00Z"},
            {"number": 5, "closedAt": None},
        ]
        chosen = pick(issues, {1, 2, 3, 5}, "2026-10-05T00:00:00Z")
        self.assertEqual([i["number"] for i in chosen], [3, 2])

    def test_pick_without_a_release_takes_every_shelved_issue(self):
        issues = [{"number": 1, "closedAt": "2026-10-01T00:00:00Z"}, {"number": 2, "closedAt": "2026-09-01T00:00:00Z"}]
        self.assertEqual([i["number"] for i in pick(issues, {1, 2}, None)], [2, 1])


if __name__ == "__main__":
    unittest.main()
