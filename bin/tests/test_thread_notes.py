from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "hooks/shared", ROOT / "hooks/continuation", ROOT / "bin/core"):
    sys.path.insert(0, str(directory))
import continuation as gate
import thread_notes

PARENT_ID = "6f1c2a9e-0000-4000-8000-00000000abcd"
PARENT = """## Task
Fast walk mode
In scope:
- hold Shift to run
Out of scope:
- fly mode
Done when:
- 60 fps on a mid-range phone"""
CHILD = f"""parent: {PARENT_ID}

## Task
Profile walking frame rate.
Done when:
- a number for walking and running"""


def claude(kind, text):
    if kind == "user":
        return {"type": "user", "origin": {"kind": "human"}, "message": {"role": "user", "content": text}}
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


class Judge:
    """Answers the shared Jev request with fixed scores."""

    def __init__(self, nudge=0.9, proposal=0.0, deciding=0.1):
        self.answers = {"nudge": {"noul": nudge}, "proposal": {"noul": proposal},
                        "user_deciding": {"noul": deciding}}
        self.calls = []

    def system_one(self, **kwargs):
        self.calls.append(kwargs)
        return {"answers": self.answers}


class ThreadNotesTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        for target in (patch.object(thread_notes, "NOTES_DIR", self.dir / "notes"),
                       patch.object(gate, "append_decision", lambda row: None)):
            target.start()
            self.addCleanup(target.stop)
        (self.dir / "notes").mkdir()
        self.transcript = self.dir / "t.jsonl"

    def note(self, session, text):
        (self.dir / "notes" / f"{session}.md").write_text(text)

    def stop(self, judge, rows, session="child-session-1"):
        self.transcript.write_text("\n".join(json.dumps(row) for row in rows))
        return gate.evaluate_stop({"hook_event_name": "Stop", "session_id": session,
            "transcript_path": str(self.transcript),
            "last_assistant_message": rows[-1]["message"]["content"][0]["text"]},
            environ={"FARPLANE_CONFIG_DISABLE": "1"}, client=judge, reader=lambda *_: None)

    def test_own_notes_scope_the_push(self):
        self.note("child-session-1", PARENT)
        judge = Judge(nudge=0.9)
        result = self.stop(judge, [claude("user", "Build fast walk."), claude("assistant", "Next I'll check fps.")])
        self.assertEqual(result["reason"], gate.NUDGE + gate.SCOPE_LINE)
        call = judge.calls[0]
        self.assertIn("Out of scope", call["state"]["thread_notes"])
        self.assertNotIn("parent_notes", call["state"])
        self.assertIn(gate.NOTES_QUESTION, call["questions"]["nudge"]["instructions"])
        self.assertIn(gate.PROPOSAL_NOTES_QUESTION, call["questions"]["proposal"]["instructions"])

    def test_sub_thread_also_loads_its_parents_notes(self):
        self.note(PARENT_ID, PARENT)
        self.note("child-session-1", CHILD)
        judge = Judge(nudge=0.9)
        self.stop(judge, [claude("user", "Profile it."), claude("assistant", "Walking: 62 fps.")])
        state = judge.calls[0]["state"]
        self.assertIn("Profile walking", state["thread_notes"])
        self.assertIn("fly mode", state["parent_notes"])

    def test_out_of_scope_only_lets_the_turn_end(self):
        self.note("child-session-1", PARENT)
        judge = Judge(nudge=0.1, proposal=0.2)  # the judge read Out of scope: fly mode
        self.assertIsNone(self.stop(judge, [claude("user", "Build fast walk."),
            claude("assistant", "Done: 61 fps. A fly mode could come next.")]))

    def test_no_notes_behaves_as_today(self):
        judge = Judge(nudge=0.9)
        rows = []
        for index in range(8):
            rows += [claude("user", f"Step {index}."), claude("assistant", f"Did {index}; I'll test next.")]
        self.assertEqual(self.stop(judge, rows)["reason"], gate.NUDGE)
        call = judge.calls[0]
        self.assertNotIn("thread_notes", call["state"])
        self.assertEqual(call["questions"]["nudge"]["instructions"], gate.QUESTION)
        self.assertEqual(len(call["state"]["recent_dialogue"]), 16)

    def test_notes_trim_the_dialogue_to_the_last_five_and_keep_the_original_request(self):
        self.note("child-session-1", PARENT)
        judge = Judge(nudge=0.9)
        rows = []
        for index in range(8):
            rows += [claude("user", f"Step {index}."), claude("assistant", f"Did {index}; I'll test next.")]
        self.stop(judge, rows)
        state = judge.calls[0]["state"]
        self.assertEqual(len(state["recent_dialogue"]), gate.NOTES_MESSAGES)
        self.assertEqual(state["original_request"], "Step 0.")

    def test_investigate_or_propose_request_never_pushes(self):
        self.note("child-session-1", PARENT)
        judge = Judge(nudge=0.9, proposal=0.9, deciding=0.9)
        self.assertIsNone(self.stop(judge, [claude("user", "How would we do this? Propose a design."),
            claude("assistant", "Proposed design: notes. Next I could build it.")]))

    def test_bad_ids_and_self_parent_are_ignored(self):
        self.assertIsNone(thread_notes.notes_path("../../etc/passwd"))
        self.note("child-session-1", "parent: child-session-1\n## Task\nx")
        self.assertEqual(thread_notes.load("child-session-1")[1], None)
        self.note("child-session-1", "parent: missing-session-9\n## Task\nx")
        self.assertEqual(thread_notes.load("child-session-1")[1], None)


if __name__ == "__main__":
    unittest.main()
