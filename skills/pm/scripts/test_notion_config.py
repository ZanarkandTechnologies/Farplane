#!/usr/bin/env python3
"""Tests for notion_config.py."""

from __future__ import annotations

import unittest

import notion_config


class NotionConfigTests(unittest.TestCase):
    def test_reads_injected_notion_token(self) -> None:
        value = notion_config.notion_token({"NOTION_TOKEN": "runtime-token"})
        self.assertEqual(value, "runtime-token")

    def test_private_config_and_legacy_aliases_are_not_supported(self) -> None:
        self.assertEqual(
            notion_config.notion_token(
                {"FARPLANE_STATE_DIR": "/tmp/unused", "NOTION_API_KEY": "legacy-key"}
            ),
            "",
        )


if __name__ == "__main__":
    unittest.main()
