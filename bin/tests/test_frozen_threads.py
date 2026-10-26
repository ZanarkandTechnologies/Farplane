from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "frozen-threads.py"
spec = importlib.util.spec_from_file_location("frozen_threads", SCRIPT)
watch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(watch)

T0 = "2026-10-26T01:00:00Z"
NOW = watch.ts("2026-10-26T01:20:00Z")


def at(minute: int) -> str:
    return f"2026-10-26T01:{minute:02d}:00Z"


def prompt(minute, text="hi", origin="human", meta=False):
    return {"type": "user", "timestamp": at(minute), "uuid": f"u{minute}", "turnOrigin": origin, "isMeta": meta,
            "message": {"content": text}}


def note(minute, text):
    return {"type": "user", "timestamp": at(minute), "uuid": f"n{minute}", "message": {"content": text}}


def reply(minute, mid="m1", tools=()):
    content = [{"type": "tool_use", "id": t} for t in tools] or [{"type": "text", "text": "done"}]
    return {"type": "assistant", "timestamp": at(minute), "uuid": f"a{minute}", "message": {"id": mid, "content": content}}


def result(minute, tool_id, text="ok"):
    return {"type": "user", "timestamp": at(minute), "uuid": f"r{minute}",
            "message": {"content": [{"type": "tool_result", "tool_use_id": tool_id, "content": text}]}}


class PendingTests(unittest.TestCase):
    def test_unanswered_message_is_pending(self):
        e = watch.pending([reply(0), prompt(1)], NOW)
        self.assertEqual(e["uuid"], "u1")

    def test_answered_message_is_not_pending(self):
        self.assertIsNone(watch.pending([prompt(1), reply(2)], NOW))

    def test_running_tool_is_not_a_freeze(self):
        self.assertIsNone(watch.pending([prompt(1), reply(2, tools=["t1"])], NOW))

    def test_tool_result_waits_on_the_model(self):
        e = watch.pending([prompt(1), reply(2, tools=["t1"]), result(3, "t1")], NOW)
        self.assertEqual(e["uuid"], "r3")

    def test_parallel_tool_still_running_is_not_a_freeze(self):
        events = [prompt(1), reply(2, tools=["t1", "t2"]), result(3, "t1")]
        self.assertIsNone(watch.pending(events, NOW))

    def test_refused_tool_ends_the_turn(self):
        events = [prompt(1), reply(2, tools=["t1"]), result(3, "t1", "The user doesn't want to proceed with this tool use.")]
        self.assertIsNone(watch.pending(events, NOW))

    def test_cleanup_notice_without_a_turn_is_ignored(self):
        events = [prompt(1), reply(2), note(5, "<task-notification>\n<task-id>__orphan_summary__:shell</task-id>")]
        self.assertIsNone(watch.pending(events, NOW))

    def test_local_command_output_is_ignored(self):
        events = [reply(2), prompt(5, "<local-command-stdout>Set model to opus</local-command-stdout>")]
        self.assertIsNone(watch.pending(events, NOW))

    def test_events_after_now_are_ignored_in_replays(self):
        events = [prompt(1), reply(30)]
        self.assertEqual(watch.pending(events, NOW)["uuid"], "u1")


class FindFrozenTests(unittest.TestCase):
    def test_replay_flags_only_after_the_threshold(self):
        import json, tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            for e in [reply(0), prompt(4, "reply my message")]:
                f.write(json.dumps(e) + "\n")
        path = Path(f.name)
        self.assertEqual(watch.find_frozen(10, watch.ts(at(13)), path), [])
        found = watch.find_frozen(10, watch.ts(at(15)), path)
        self.assertEqual(found[0]["minutes"], 11)
        self.assertIn("reply my message", found[0]["waiting_on"])
        path.unlink()


if __name__ == "__main__":
    unittest.main()
