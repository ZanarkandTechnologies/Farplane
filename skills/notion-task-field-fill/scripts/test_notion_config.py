#!/usr/bin/env python3
"""Tests for notion_config.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import notion_config


class NotionConfigTests(unittest.TestCase):
    def test_reads_canonical_farplane_integration_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.toml").write_text(
                '[integrations]\nnotion_api_key = "canonical-key"\n',
                encoding="utf-8",
            )

            value = notion_config.notion_api_key({"FARPLANE_STATE_DIR": str(root)})

        self.assertEqual(value, "canonical-key")

    def test_explicit_notion_api_key_overrides_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.toml").write_text(
                '[integrations]\nnotion_api_key = "canonical-key"\n',
                encoding="utf-8",
            )

            value = notion_config.notion_api_key(
                {"FARPLANE_STATE_DIR": str(root), "NOTION_API_KEY": "runtime-key"}
            )

        self.assertEqual(value, "runtime-key")

    def test_notion_token_is_not_a_supported_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.toml").write_text(
                '[env]\nNOTION_TOKEN = "legacy-token"\n',
                encoding="utf-8",
            )

            value = notion_config.notion_api_key({"FARPLANE_STATE_DIR": str(root)})

        self.assertEqual(value, "")


if __name__ == "__main__":
    unittest.main()
