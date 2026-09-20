from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "bin/runtime", ROOT / "bin/core", ROOT / "hooks"):
    sys.path.insert(0, str(directory))
import continuation as gate


class Client:
    def __init__(self, score=0.8):
        self.score = score
        self.calls = []

    def system_one(self, **kwargs):
        self.calls.append(kwargs)
        if isinstance(self.score, Exception):
            raise self.score
        return {"answers": {"nudge": {"noul": self.score}}}


def message(role, text, channel=None):
    return {"type": "response_item", "payload": {
        "type": "message", "role": role, "channel": channel,
        "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}]}}


def user(text):
    row = message("user", text)
    row["payload"]["internal_chat_message_metadata_passthrough"] = {
        "turn_id": "synthetic-turn", "create_time": 123,
        "content_item_kinds": ["user.text"]}
    return [row]



class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "rollout.jsonl"
        self.env = {"FARPLANE_CONFIG_DISABLE": "1"}
        self.rows = user("Implement and test it.") + [message("assistant", "Implemented. I'll test next.")]
        self.client = Client()

    def tearDown(self):
        self.temp.cleanup()

    def run_gate(self, *, final="I'll test next.", active=False):
        self.path.write_text("\n".join(json.dumps(row) for row in self.rows))
        return gate.evaluate_stop({"hook_event_name": "Stop", "transcript_path": str(self.path),
            "last_assistant_message": final, "stop_hook_active": active},
            environ=self.env, client=self.client)

    def test_positive_at_threshold_is_fixed_scoped_feedback(self):
        self.client.score = 0.5
        self.assertEqual(self.run_gate(), {"decision": "block", "reason": gate.NUDGE})
        self.assertIn("earlier turns", self.client.calls[0]["questions"]["nudge"]["instructions"])

    def test_negative_allows_completed_or_deliberative_request(self):
        self.rows = user("Compare options only; do not implement.")
        self.client.score = 0.49
        self.assertIsNone(self.run_gate(final="Here are the options."))

    def test_malformed_decision_and_outage_fail_open(self):
        for value in (None, True, "0.8", float("nan"), 2, -1, RuntimeError("outage")):
            self.client.score = value
            self.assertIsNone(self.run_gate())

    def test_defers_to_unchanged_response_gate_without_api(self):
        self.env["FARPLANE_FINAL_RESPONSE_MAX_PROSE_WORDS"] = "3"
        self.assertIsNone(self.run_gate(final="one two three four"))
        self.assertEqual(self.client.calls, [])

    def test_rewritten_promise_reassessed_after_exact_length_feedback(self):
        self.env["FARPLANE_FINAL_RESPONSE_MAX_PROSE_WORDS"] = "3"
        candidate = "Implemented this change; I will run the tests next."
        self.rows[-1] = message("assistant", candidate)
        self.assertIsNone(self.run_gate(final=candidate))
        self.assertEqual(self.client.calls, [])
        feedback = gate.gate_response({"hook_event_name": "Stop",
            "last_assistant_message": candidate}, 3, 50)["reason"]
        self.rows += [message("user", feedback), message("assistant", "Will test next.")]
        self.assertIsNotNone(self.run_gate(final="Will test next.", active=True))
        state = self.client.calls[0]["state"]
        self.assertEqual(state["own_nudges_this_user_turn"], 0)
        self.assertTrue(state["recognized_length_feedback_this_user_turn"])
        self.assertEqual(state["recent_dialogue"][-2]["role"], "hook")

    def test_user_quoted_length_feedback_is_not_hook_provenance(self):
        candidate = "word " * 501
        feedback = gate.gate_response({"hook_event_name": "Stop",
            "last_assistant_message": candidate}, 500, 50)["reason"]
        self.rows += [message("assistant", candidate), message("user", feedback)]
        self.rows += user(feedback)
        self.rows += [message("assistant", "What does this feedback mean?")]
        self.assertIsNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls, [])

    def test_wrong_length_feedback_or_assistant_quote_is_not_provenance(self):
        feedback = gate.gate_response({"hook_event_name": "Stop",
            "last_assistant_message": "word " * 501}, 500, 50)["reason"]
        self.rows += [message("user", feedback), message("assistant", feedback)]
        self.assertIsNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls, [])

    def test_three_own_nudges_cap_and_actual_user_resets(self):
        self.rows += [message("user", gate.NUDGE) for _ in range(3)]
        self.assertIsNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls, [])
        self.rows += user("Continue with this newly requested feature.")
        self.assertIsNotNone(self.run_gate())

    def desktop_hook(self, body):
        row = message("user", '<hook_prompt hook_run_id="stop:5:/synthetic/hooks.json">'
                      + body + '</hook_prompt>')
        row["payload"]["internal_chat_message_metadata_passthrough"] = {
            "turn_id": "synthetic-turn", "content_item_kinds": ["unknown"]}
        return row

    def test_desktop_hook_envelope_counts_and_caps_nudges(self):
        self.rows += [self.desktop_hook(gate.NUDGE)]
        self.assertIsNotNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls[-1]["state"]["own_nudges_this_user_turn"], 1)
        self.rows += [self.desktop_hook(gate.NUDGE) for _ in range(2)]
        self.client.calls.clear()
        self.assertIsNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls, [])

    def test_desktop_length_feedback_allows_reassessment(self):
        candidate = "word " * 501
        feedback = gate.gate_response({"hook_event_name": "Stop",
            "last_assistant_message": candidate}, 500, 50)["reason"]
        self.rows += [message("assistant", candidate), self.desktop_hook(feedback),
                      message("assistant", "I will test next.")]
        self.assertIsNotNone(self.run_gate(active=True))
        self.assertTrue(self.client.calls[-1]["state"]["recognized_length_feedback_this_user_turn"])

    def test_real_user_envelope_quote_does_not_grant_hook_provenance(self):
        envelope = self.desktop_hook(gate.NUDGE)["payload"]["content"][0]["text"]
        self.rows += user(envelope)
        self.assertIsNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls, [])

    def test_unknown_or_changed_desktop_hook_body_does_not_grant_provenance(self):
        for body in ("Other hook feedback", gate.NUDGE + " extra"):
            with self.subTest(body=body):
                self.rows = user("Implement it.") + [self.desktop_hook(body)]
                self.assertIsNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls, [])

    def test_one_prior_nudge_allows_progress_sensitive_reassessment(self):
        self.rows += [message("user", gate.NUDGE), message("assistant", "Tests found a bug; I'll fix it.")]
        self.assertIsNotNone(self.run_gate(active=True))
        self.assertEqual(self.client.calls[0]["state"]["own_nudges_this_user_turn"], 1)

    def test_unknown_hook_retry_and_unrecognized_marker_fail_open(self):
        self.assertIsNone(self.run_gate(active=True))
        self.rows += [message("user", gate.TAG + " malformed")]
        self.assertIsNone(self.run_gate())
        self.assertEqual(self.client.calls, [])

    def test_missing_real_user_provenance_fails_open(self):
        self.rows = [message("user", "Continue")]
        self.assertIsNone(self.run_gate())

    def test_redacts_secrets_and_excludes_tool_reasoning(self):
        self.rows += user("token=secret123 email me at private@example.com /Users/alice/private")
        self.rows += [message("assistant", "SECRET REASONING", "analysis"),
                      message("assistant", "SECRET COMMENTARY", "commentary"),
                      message("tool", "SECRET TOOL OUTPUT")]
        self.assertIsNotNone(self.run_gate())
        sent = json.dumps(self.client.calls[0]["state"])
        for forbidden in ("secret123", "private@example.com", "/Users/alice", "SECRET REASONING", "SECRET COMMENTARY", "SECRET TOOL OUTPUT"):
            self.assertNotIn(forbidden, sent)

    def test_json_and_query_credentials_and_configured_key_are_redacted(self):
        self.env["OPENROUTER_API_KEY"] = "unusual-provider-key-value"
        self.rows += user('Check {"api_key": "json-secret"} and '
            'https://example.test/?access_token=query-secret&next=public '
            'and unusual-provider-key-value')
        self.run_gate()
        sent = json.dumps(self.client.calls[0]["state"])
        for secret in ("json-secret", "query-secret", "unusual-provider-key-value"):
            self.assertNotIn(secret, sent)
        self.assertIn("next=public", sent)

    def test_bounds_context_preserves_original_and_latest_request(self):
        self.rows += [message("assistant", "x" * 3000) for _ in range(25)]
        self.rows += user("Now finish verification.")
        self.run_gate()
        state = self.client.calls[0]["state"]
        self.assertEqual(state["original_request"], "Implement and test it.")
        self.assertEqual(state["latest_user_request"], "Now finish verification.")
        self.assertTrue(state["source_truncated"])
        self.assertLessEqual(len(state["recent_dialogue"]), gate.MAX_MESSAGES)
        self.assertIn("[TEXT TRUNCATED]", json.dumps(state))

    def test_assistant_quoting_nudge_does_not_count(self):
        self.rows += [message("assistant", gate.NUDGE) for _ in range(3)]
        self.assertIsNotNone(self.run_gate())

    def test_instruction_injections_do_not_become_original_request(self):
        injected = message("user", "Private environment configuration")
        injected["payload"]["internal_chat_message_metadata_passthrough"] = {
            "content_item_kinds": ["agents_md.instructions", "environments.environment_context"]}
        self.rows.insert(0, injected)
        self.run_gate()
        state = self.client.calls[0]["state"]
        self.assertEqual(state["original_request"], "Implement and test it.")
        self.assertNotIn("Private environment", json.dumps(state))

    def test_provider_model_is_shared_configuration(self):
        self.env["FARPLANE_JEV_PROVIDER"] = "featherless"
        self.env["FARPLANE_JEV_MODEL"] = "configured-model"
        self.run_gate()
        self.assertEqual(self.client.calls[0]["model"], "configured-model")

    def test_corrupt_and_oversized_transcripts_fail_open(self):
        for raw in ("not-json", "x" * (gate.MAX_BYTES + 1)):
            self.path.write_text(raw)
            self.assertIsNone(gate.evaluate_stop({"hook_event_name": "Stop",
                "transcript_path": str(self.path), "last_assistant_message": "I'll test next."},
                environ=self.env, client=self.client))
        self.assertEqual(self.client.calls, [])

    def test_no_credentials_fails_open(self):
        self.client = None
        self.assertIsNone(self.run_gate())



if __name__ == "__main__":
    unittest.main()
