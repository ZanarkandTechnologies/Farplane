from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
import hook_delivery


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = patch.dict(os.environ, {"FARPLANE_STATE_DIR": self.tmp.name})
        self.env.start()
        self.addCleanup(self.env.stop)

    def receipt(self, event="Stop"):
        return json.loads((Path(self.tmp.name) / "state" / "hook-delivery" / f"{event}.json").read_text())

    def test_expected_event_requires_exact_stdin_event(self):
        for event in ({"hook_event_name": "SubagentStop"}, {"hookType": "Stop"}, {}):
            with patch("sys.stderr", io.StringIO()):
                self.assertFalse(hook_delivery.validate_event(event, ["--expect-event", "Stop"]))
            self.assertEqual(self.receipt()["reason"], "event_mismatch")
        self.assertTrue(hook_delivery.validate_event({"hook_event_name": "Stop"}, ["--expect-event", "Stop"]))

    def test_unconfigured_never_sends(self):
        with patch.object(hook_delivery.urllib.request, "urlopen") as send:
            hook_delivery.deliver({"hookType": "Stop"}, None, "secret")
        send.assert_not_called()
        self.assertEqual(self.receipt()["status"], "unconfigured")

    def test_attempted_before_accepted_and_receipt_has_no_private_data(self):
        def send(request, timeout):
            self.assertEqual(self.receipt()["status"], "attempted")
            self.assertEqual(timeout, 2)
            self.assertEqual(request.get_header("X-farplane-telemetry-token"), "secret")
            response = MagicMock()
            response.__enter__.return_value.status = 202
            return response
        with patch.object(hook_delivery.urllib.request, "urlopen", side_effect=send):
            hook_delivery.deliver({"hookType": "Stop", "payload": "private"}, "https://private.example", "secret")
        receipt = self.receipt()
        self.assertEqual(receipt["status"], "accepted")
        self.assertEqual(receipt["httpStatus"], 202)
        for private in ("secret", "private", "example"):
            self.assertNotIn(private, json.dumps(receipt))

    def test_http_and_transport_errors_are_sanitized(self):
        errors = [urllib.error.HTTPError("https://secret", 401, "secret", {}, None),
                  urllib.error.URLError("secret"), ValueError("secret")]
        for error in errors:
            with patch.object(hook_delivery.urllib.request, "urlopen", side_effect=error), patch("sys.stderr", io.StringIO()) as stderr:
                hook_delivery.deliver({"hookType": "Stop"}, "https://secret", "secret")
            self.assertEqual(self.receipt()["status"], "failed")
            self.assertNotIn("secret", json.dumps(self.receipt()) + stderr.getvalue())

    def test_receipt_write_failure_does_not_prevent_delivery(self):
        response = MagicMock()
        response.__enter__.return_value.status = 200
        with patch.object(hook_delivery.Path, "mkdir", side_effect=OSError("private")), patch.object(hook_delivery.urllib.request, "urlopen", return_value=response) as send, patch("sys.stderr", io.StringIO()):
            hook_delivery.deliver({"hookType": "Stop"}, "https://example.com", None)
        send.assert_called_once()


if __name__ == "__main__":
    unittest.main()
