from __future__ import annotations

import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "hooks" / "final_response_gate.py"
SPEC = importlib.util.spec_from_file_location("final_response_gate", MODULE_PATH)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class FinalResponseGateTests(unittest.TestCase):
    def payload(self, message: str | None, *, active: bool = False) -> dict[str, object]:
        return {
            "hook_event_name": "Stop",
            "last_assistant_message": message,
            "stop_hook_active": active,
        }

    def test_under_cap_allows(self) -> None:
        self.assertIsNone(gate.gate_response(self.payload("one two"), 3, 2))

    def test_exact_cap_allows(self) -> None:
        self.assertIsNone(gate.gate_response(self.payload("one two three"), 3, 2))

    def test_exact_line_cap_allows(self) -> None:
        self.assertIsNone(gate.gate_response(self.payload("one\ntwo"), 10, 2))

    def test_over_cap_requests_semantic_compression(self) -> None:
        result = gate.gate_response(self.payload("one two three four"), 3, 2)
        self.assertEqual(result["decision"], "block")
        self.assertIn("at most 3 prose words", result["reason"])
        self.assertIn("current: 4", result["reason"])
        self.assertIn("safety-critical", result["reason"])
        self.assertNotIn("truncate", result["reason"].lower())

    def test_over_line_cap_requests_one_semantic_compression_pass(self) -> None:
        result = gate.gate_response(self.payload("one\ntwo\nthree"), 10, 2)
        self.assertEqual(result["decision"], "block")
        self.assertIn("at most 2 nonblank prose lines", result["reason"])
        self.assertIn("current: 3", result["reason"])

    def test_blank_lines_do_not_count(self) -> None:
        self.assertIsNone(gate.gate_response(self.payload("one\n\n  \ntwo"), 10, 2))

    def test_line_only_retry_yields_to_detail_or_safety_judgment(self) -> None:
        self.assertIsNone(
            gate.gate_response(self.payload("one\ntwo\nthree", active=True), 10, 2)
        )

    def test_repeated_continuation_gets_stronger_feedback(self) -> None:
        result = gate.gate_response(self.payload("one two three four", active=True), 3, 2)
        self.assertIn("previous compression attempt", result["reason"])

    def test_missing_message_and_other_events_allow(self) -> None:
        self.assertIsNone(gate.gate_response(self.payload(None), 3, 2))
        payload = self.payload("one two three four")
        payload["hook_event_name"] = "SubagentStop"
        self.assertIsNone(gate.gate_response(payload, 3, 2))

    def test_invalid_env_uses_default(self) -> None:
        self.assertEqual(
            gate.configured_max_prose_words({gate.ENV_MAX_PROSE_WORDS: "bad"}), 500
        )
        self.assertEqual(
            gate.configured_max_prose_words({gate.ENV_MAX_PROSE_WORDS: "0"}), 500
        )
        self.assertEqual(
            gate.configured_max_prose_lines({gate.ENV_MAX_PROSE_LINES: "bad"}),
            20,
        )
        self.assertEqual(
            gate.configured_max_prose_lines({gate.ENV_MAX_PROSE_LINES: "0"}),
            20,
        )

    def test_main_emits_valid_stop_json_only_when_blocked(self) -> None:
        stdin = io.StringIO(json.dumps(self.payload("one two three four")))
        stdout = io.StringIO()
        with patch.dict(
            os.environ,
            {gate.ENV_MAX_PROSE_WORDS: "3", gate.ENV_MAX_PROSE_LINES: "20"},
        ), patch("sys.stdin", stdin), patch("sys.stdout", stdout):
            self.assertEqual(gate.main(), 0)
        result = json.loads(stdout.getvalue())
        self.assertEqual(result["decision"], "block")

    def test_root_hook_config_invokes_managed_gate(self) -> None:
        payload = json.loads((ROOT / "hooks.json").read_text(encoding="utf-8"))
        commands = [
            hook["command"]
            for group in payload["hooks"]["Stop"]
            for hook in group["hooks"]
        ]
        self.assertIn(
            'python3 "$HOME/.codex/hooks/final_response_gate.py"', commands
        )


if __name__ == "__main__":
    unittest.main()
