"""The merged Stop gate sends at most one nudge: length, continuation, then format."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "hooks/shared", ROOT / "hooks/continuation", ROOT / "bin/core"):
    sys.path.insert(0, str(directory))
import continuation  # noqa: E402
import response_format  # noqa: E402

spec = importlib.util.spec_from_file_location("stop_gate", ROOT / "hooks/stop-gate/stop_gate.py")
stop_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stop_gate)

ALL = frozenset({"continuation", "format"})


class Client:
    def __init__(self, nudge=0.1, shape="completed_change", gaps=None):
        self.answers = {"nudge": {"noul": nudge}, "shape": {"choice": shape}}
        for name in response_format.GAPS:
            self.answers[f"gap::{name}"] = {"noul": (gaps or {}).get(name, 0.1)}
        self.calls = []

    def system_one(self, **kwargs):
        self.calls.append(kwargs)
        return {"answers": {key: self.answers[key] for key in kwargs["questions"]}}


def human(text):
    return {"type": "user", "origin": {"kind": "human"}, "message": {"role": "user", "content": text}}


def assistant(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def edit_call(name="Edit"):
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "name": name, "input": {"file_path": "/tmp/x.py"}}]}}


def hook(text):
    return {"type": "user", "isMeta": True,
            "message": {"role": "user", "content": "Stop hook feedback:\n" + text}}


class StopGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "transcript.jsonl"
        self.env = {"FARPLANE_CONFIG_DISABLE": "1"}

    def tearDown(self):
        self.temp.cleanup()

    def evaluate(self, rows, final, client, *, active=False, checks=ALL):
        self.path.write_text("\n".join(json.dumps(row) for row in rows))
        return continuation.evaluate_stop(
            {"hook_event_name": "Stop", "transcript_path": str(self.path),
             "last_assistant_message": final, "stop_hook_active": active},
            environ=self.env, client=client, checks=checks)

    def test_uncited_completed_change_with_edits_gets_one_proof_nudge(self):
        client = Client()
        result = self.evaluate([human("Add the toggle."), edit_call()], "Done, toggle added.", client)
        self.assertIn(response_format.TAG, result["reason"])
        self.assertIn("Cite the proof", result["reason"])
        self.assertEqual(len(client.calls), 1)
        self.assertIn("nudge", client.calls[0]["questions"])
        self.assertTrue(client.calls[0]["state"]["files_changed"])

    def test_any_citation_means_proof_was_not_forgotten(self):
        for final in ("Done. Verified: 6 tests pass.", "Done: [diff](https://x.test/pr/1)",
                      "Done.\n```text\n6 passed\n```", "Done.\n![after](/tmp/after.png)"):
            with self.subTest(final=final):
                self.assertIsNone(self.evaluate([human("Fix it."), edit_call()], final, Client()))

    def test_no_edits_means_no_proof_nudge(self):
        self.assertIsNone(self.evaluate([human("Fix it."), edit_call("Read")], "Done.", Client()))

    def test_continuation_wins_over_format(self):
        result = self.evaluate([human("Fix it."), edit_call()], "I'll test next.", Client(nudge=0.9))
        self.assertEqual(result["reason"], continuation.NUDGE)

    def test_only_gaps_of_the_chosen_shape_count(self):
        client = Client(shape="simple_answer", gaps={"decision_choice": 0.95, "conclusion_first": 0.65})
        result = self.evaluate([human("Why?")], "Because the loop exits early.", client)
        self.assertIn("Lead with the conclusion", result["reason"])
        self.assertNotIn("recommendation", result["reason"])

    def test_format_nudges_once_per_user_turn(self):
        rows = [human("Fix it."), edit_call(), assistant("Done."),
                hook(response_format.feedback(["proof"]))]
        client = Client()
        self.assertIsNone(self.evaluate(rows, "Done again.", client, active=True))
        self.assertNotIn("shape", client.calls[0]["questions"])

    def test_new_user_turn_resets_edits_and_format_count(self):
        rows = [human("Fix it."), edit_call(), hook(response_format.feedback(["proof"])),
                human("Now explain it.")]
        self.assertIsNone(self.evaluate(rows, "It skips blanks.", Client()))

    def test_codex_rollout_tracks_apply_patch_and_wrapped_format_feedback(self):
        def codex(role, text, kinds):
            item = {"type": "message", "role": role,
                    "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}],
                    "internal_chat_message_metadata_passthrough": {"turn_id": "t1", "content_item_kinds": kinds}}
            return {"type": "response_item", "payload": item}
        patch_call = {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "apply_patch"}}
        rows = [codex("user", "Fix it.", ["user.text"]), patch_call]
        self.assertIn("Cite the proof", self.evaluate(rows, "Done.", Client())["reason"])
        wrapped = f'<hook_prompt hook_run_id="stop:1">{response_format.feedback(["proof"])}</hook_prompt>'
        rows += [codex("assistant", "Done.", []), codex("user", wrapped, ["unknown"])]
        self.assertIsNone(self.evaluate(rows, "Done again.", Client(), active=True))

    def test_continuation_only_checks_ask_only_the_nudge(self):
        client = Client()
        self.evaluate([human("Fix it."), edit_call()], "Done.", client, checks=frozenset({"continuation"}))
        self.assertEqual(list(client.calls[0]["questions"]), ["nudge"])

    def test_gaps_capped_at_two_and_feedback_never_adds_headings(self):
        client = Client(shape="proposed_change", gaps={"before_after_example": 0.9, "proof_planned": 0.8})
        result = self.evaluate([human("Plan it.")], "We should improve caching.", client)
        self.assertEqual(result["reason"].count("**Add:**"), 2)
        self.assertIn("no empty headings", result["reason"])


class EntrypointTests(unittest.TestCase):
    def test_length_blocks_first_without_a_jev_call(self):
        payload = {"hook_event_name": "Stop", "last_assistant_message": "word " * 600}
        with patch.object(stop_gate, "load_runtime_env", return_value={}), \
                patch.object(stop_gate, "jev_gate") as jev:
            result = stop_gate.run_gate(payload)
        self.assertIn("Response length", result["reason"])
        jev.assert_not_called()

    def test_checks_env_selects_checks(self):
        self.assertEqual(stop_gate.configured_checks({}), stop_gate.ALL_CHECKS)
        self.assertEqual(stop_gate.configured_checks({"FARPLANE_STOP_CHECKS": "length, bogus"}),
                         frozenset({"length"}))
        with patch.object(stop_gate, "load_runtime_env", return_value={"FARPLANE_STOP_CHECKS": "length"}), \
                patch.object(stop_gate, "jev_gate") as jev:
            self.assertIsNone(stop_gate.run_gate({"hook_event_name": "Stop", "last_assistant_message": "ok"}))
        jev.assert_not_called()

    def test_gate_names_follow_the_reason_marker(self):
        self.assertEqual(stop_gate.gate_name(response_format.feedback(["proof"])), "response-format")
        self.assertEqual(stop_gate.gate_name(continuation.NUDGE), "continuation")
        self.assertEqual(stop_gate.gate_name("#### Response length"), "response-length")

    def test_root_hooks_register_only_the_merged_blocking_gate(self):
        payload = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        commands = [hook["command"] for group in payload["hooks"]["Stop"] for hook in group["hooks"]]
        self.assertIn('python3 "$HOME/.codex/hooks/stop-gate/stop_gate.py"', commands)
        self.assertFalse(any("continuation_gate" in c or "final_response_gate" in c for c in commands))


class CatalogTests(unittest.TestCase):
    def test_every_shape_mirrors_an_agents_template_heading(self):
        headings = set(re.findall(r"^### (.+)$",
                                  (ROOT / "runtimes/AGENTS.md").read_text(), re.M))
        for name, spec in response_format.SHAPES.items():
            with self.subTest(shape=name):
                self.assertIn(spec["template"], headings)
                self.assertTrue(set(spec["gaps"]) <= set(response_format.GAPS))

    def test_eval_cases_use_known_shapes_and_gaps(self):
        cases = json.loads((ROOT / "hooks/stop-gate/eval_cases.json").read_text())
        known = set(response_format.GAPS) | {"proof", "status_line"}
        for case in cases:
            self.assertIn(case["expected_shape"], response_format.SHAPES)
            self.assertTrue(set(case["expected_fixes"]) <= known, case["id"])


if __name__ == "__main__":
    unittest.main()
