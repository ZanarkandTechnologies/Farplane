#!/usr/bin/env python3
"""Regression tests for Phone Chaser dispatch metadata validation."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import dispatch_call


class DispatchCallMetadataTest(unittest.TestCase):
    def write_metadata(self, value: dict[str, object]) -> str:
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        with handle:
            json.dump(value, handle)
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def test_rejects_nested_thread_and_app_server_fields(self) -> None:
        path = self.write_metadata(
            {
                "review_callback": {
                    "review_id": "review-1",
                    "webhook_url": "http://127.0.0.1:8789/phone-chaser/review",
                    "capability": "capability",
                    "thread_id": "thread-source",
                    "app_server_url": "ws://127.0.0.1:47892",
                }
            }
        )

        with self.assertRaisesRegex(SystemExit, "review_callback contains unsupported fields"):
            dispatch_call.load_metadata_file(path)

    def test_accepts_review_context_and_callback_allowlist(self) -> None:
        path = self.write_metadata(
            {
                "message": "Review the artifact.",
                "call_id": "call-1",
                "review_context": {
                    "title": "Artifact review",
                    "objective": "Decide whether to approve.",
                    "produced": "A case study.",
                    "why_it_matters": "It gates distribution.",
                    "decision_question": "Approve, revise, or reject?",
                    "approve_effect": "Return the decision only.",
                    "revision_examples": ["Tighten the claim."],
                    "limits": ["No publishing."],
                },
                "review_callback": {
                    "review_id": "review-1",
                    "webhook_url": "http://127.0.0.1:8789/phone-chaser/review",
                    "capability": "capability",
                },
            }
        )

        self.assertEqual(dispatch_call.load_metadata_file(path)["call_id"], "call-1")


if __name__ == "__main__":
    unittest.main()
