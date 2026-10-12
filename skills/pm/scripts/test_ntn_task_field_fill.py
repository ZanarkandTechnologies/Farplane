#!/usr/bin/env python3
"""Tests for ntn_task_field_fill.py."""

from __future__ import annotations

import unittest
from unittest import mock

import ntn_task_field_fill as field_fill


class NtnTaskFieldFillTests(unittest.TestCase):
    def test_ntn_env_bridges_canonical_token(self) -> None:
        env = field_fill.ntn_env({"NOTION_TOKEN": "runtime-token"})

        self.assertEqual(env["NOTION_TOKEN"], "runtime-token")
        self.assertEqual(env["NOTION_API_TOKEN"], "runtime-token")

    def test_no_notion_api_key_fallback(self) -> None:
        with self.assertRaises(RuntimeError):
            field_fill.ntn_env({"NOTION_API_KEY": "legacy-token"})

    def test_query_data_source_uses_api_subcommand_and_filter_properties(self) -> None:
        recipe = {
            "data_source_id": "43a439fd-74c5-4b43-9afb-950f047e5d4f",
            "page_size": 1,
            "filter_properties": ["title", "rlQm"],
            "filter": {"property": "Act Time", "date": {"on_or_after": "<local-window-date>"}},
        }
        with mock.patch.object(field_fill, "run_ntn") as run_ntn:
            run_ntn.return_value = field_fill.NtnResult(["ntn"], "{}", "", {})

            field_fill.query_data_source(recipe, local_window_date="2026-07-06", env={"NOTION_TOKEN": "token"})

        args, body, _env = run_ntn.call_args.args
        self.assertEqual(args[:3], ["api", "/v1/data_sources/43a439fd-74c5-4b43-9afb-950f047e5d4f/query", "-X"])
        self.assertIn("filter_properties==title", args)
        self.assertIn("filter_properties==rlQm", args)
        self.assertEqual(body["filter"]["date"]["on_or_after"], "2026-07-06")

    def test_redact_removes_token_ids_and_notion_urls(self) -> None:
        raw = (
            "ntn_abc 43a439fd-74c5-4b43-9afb-950f047e5d4f "
            "https://www.notion.so/private"
        )

        redacted = field_fill.redact(raw, {"NOTION_TOKEN": "ntn_abc"})

        self.assertNotIn("ntn_abc", redacted)
        self.assertNotIn("43a439fd-74c5-4b43-9afb-950f047e5d4f", redacted)
        self.assertNotIn("https://www.notion.so/private", redacted)

    def test_reel_task_gets_high_confidence_content_tags(self) -> None:
        tags, confidence, _reasons = field_fill.infer_tags("[Reel] Zap myself", "")

        self.assertEqual(confidence, "high")
        self.assertEqual(tags, ["Reel", "Content"])

    def test_explicit_writing_tag_is_high_confidence(self) -> None:
        tags, confidence, _reasons = field_fill.infer_tags("Write stronger push back", "")

        self.assertEqual(confidence, "high")
        self.assertIn("Writing", tags)


if __name__ == "__main__":
    unittest.main()
