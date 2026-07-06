#!/usr/bin/env python3
"""Tests for notion_config.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import notion_config


class NotionConfigTests(unittest.TestCase):
    def test_reads_canonical_farplane_integration_token(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.toml").write_text(
                '[integrations]\nnotion_token = "canonical-token"\n',
                encoding="utf-8",
            )

            value = notion_config.notion_token({"FARPLANE_STATE_DIR": str(root)})

        self.assertEqual(value, "canonical-token")

    def test_explicit_notion_token_overrides_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.toml").write_text(
                '[integrations]\nnotion_token = "canonical-token"\n',
                encoding="utf-8",
            )

            value = notion_config.notion_token(
                {"FARPLANE_STATE_DIR": str(root), "NOTION_TOKEN": "runtime-token"}
            )

        self.assertEqual(value, "runtime-token")

    def test_notion_api_key_is_not_a_supported_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.toml").write_text(
                '[env]\nNOTION_API_KEY = "legacy-key"\n',
                encoding="utf-8",
            )

            value = notion_config.notion_token({"FARPLANE_STATE_DIR": str(root)})

        self.assertEqual(value, "")


if __name__ == "__main__":
    unittest.main()
