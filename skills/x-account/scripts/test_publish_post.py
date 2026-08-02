#!/usr/bin/env python3
"""Tests for the X publish script without live API calls."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parent / "publish_post.py"


def load_module():
    if str(SCRIPT.parent) not in sys.path:
        sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("publish_post", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublishPostTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def write_payload(self, tmp: Path, payload: dict) -> Path:
        path = tmp / "payload.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def args(self, payload: Path, tmp: Path, execute: bool = False) -> argparse.Namespace:
        return argparse.Namespace(
            payload=str(payload),
            account_alias="farplane-x",
            approval_ref="tickets/TASK-0001/ticket.md" if execute else None,
            execute=execute,
            project_root=str(tmp),
            content_id=None,
            campaign="launch",
            kpis="x_views,x_likes",
            username="farplane",
            limit=280,
            media_timeout_seconds=1,
            no_ledger=False,
        )

    def test_dry_run_does_not_require_credentials_or_mutate(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmp = Path(raw_tmp)
            payload = self.write_payload(tmp, {"tweets": [{"text": "First"}, {"text": "Second"}]})
            result = self.module.publish(self.args(payload, tmp))
            ledger = tmp / ".farplane" / "content" / "ledger.jsonl"
            self.assertTrue(ledger.exists())
            ledger_text = ledger.read_text(encoding="utf-8")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertFalse(result["mutated"])
        self.assertEqual(result["tweet_count"], 2)
        self.assertTrue(result["content_id"].startswith("x:draft:"))
        self.assertIn('"status": "draft"', ledger_text)

    def test_execute_publishes_thread_and_writes_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmp = Path(raw_tmp)
            payload = self.write_payload(tmp, {"tweets": [{"text": "First"}, {"text": "Second"}]})
            with patch.object(self.module, "load_runtime_values", return_value={"FARPLANE_X_OAUTH2_ACCESS_TOKEN": "token"}), patch.object(
                self.module, "create_tweet", side_effect=["111", "222"]
            ) as create_tweet:
                result = self.module.publish(self.args(payload, tmp, execute=True))
            ledger = tmp / ".farplane" / "content" / "ledger.jsonl"
            self.assertTrue(result["ok"])
            self.assertTrue(result["mutated"])
            self.assertEqual(result["tweet_ids"], ["111", "222"])
            self.assertTrue(result["content_id"].startswith("x:draft:"))
            self.assertEqual(create_tweet.call_args_list[1].args[3], "111")
            self.assertTrue(ledger.exists())
            self.assertIn('"external_id": "111"', ledger.read_text(encoding="utf-8"))
            self.assertIn('"status": "posted"', ledger.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
