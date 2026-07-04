#!/usr/bin/env python3
"""Tests for the Instagram publish script without live API calls."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parent / "publish_media.py"


def load_module():
    if str(SCRIPT.parent) not in sys.path:
        sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("publish_media", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublishMediaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def write_payload(self, tmp: Path, payload: dict) -> Path:
        path = tmp / "payload.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def args(self, payload: Path, tmp: Path, execute: bool = False) -> argparse.Namespace:
        return argparse.Namespace(
            payload=str(payload),
            account_alias="farplane-instagram",
            approval_ref="tickets/TASK-0001/ticket.md" if execute else None,
            execute=execute,
            project_root=str(tmp),
            campaign="launch",
            kpis="instagram_views,instagram_likes",
            instagram_user_id=None,
            graph_version=None,
            container_timeout_seconds=1,
            no_ledger=False,
        )

    def test_dry_run_accepts_reel_public_url_without_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmp = Path(raw_tmp)
            payload = self.write_payload(tmp, {"caption": "Demo", "media_type": "reel", "media": "https://example.com/reel.mp4"})
            result = self.module.publish(self.args(payload, tmp))
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertFalse(result["mutated"])
        self.assertEqual(result["media_type"], "reel")

    def test_execute_publishes_media_and_writes_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmp = Path(raw_tmp)
            payload = self.write_payload(tmp, {"caption": "Demo", "media_type": "image", "media": "https://example.com/image.jpg"})
            with patch.object(
                self.module,
                "load_config_values",
                return_value={
                    "FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": "token",
                    "FARPLANE_INSTAGRAM_LOGIN_USER_ID": "17841400000000000",
                    "FARPLANE_META_GRAPH_VERSION": "v21.0",
                },
            ), patch.object(self.module, "create_container", return_value="container"), patch.object(
                self.module, "wait_for_container", return_value="FINISHED"
            ), patch.object(
                self.module, "publish_container", return_value="media"
            ), patch.object(
                self.module, "permalink", return_value="https://instagram.com/p/media"
            ):
                result = self.module.publish(self.args(payload, tmp, execute=True))
            ledger = tmp / ".farplane" / "content" / "ledger.jsonl"
            self.assertTrue(result["ok"])
            self.assertTrue(result["mutated"])
            self.assertEqual(result["media_id"], "media")
            self.assertTrue(ledger.exists())
            self.assertIn('"external_id": "media"', ledger.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
