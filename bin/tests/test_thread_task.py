from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "hooks/shared", ROOT / "hooks/continuation", ROOT / "hooks/user-turn",
                  ROOT / "bin/core"):
    sys.path.insert(0, str(directory))
import continuation as gate
import thread_task

TASK = """Fast walk mode
In scope:
- hold Shift to run
Out of scope:
- fly mode
Done when:
- 60 fps on iPhone
Design: https://www.figma.com/design/abc/Rooms"""


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


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        for target in (patch.object(thread_task, "TASKS_DIR", self.dir / "tasks"),
                       patch.object(gate, "append_decision", lambda row: None)):
            target.start()
            self.addCleanup(target.stop)
        self.transcript = self.dir / "t.jsonl"

    def write(self, rows):
        self.transcript.write_text("\n".join(json.dumps(row) for row in rows))


class ContinuationWithTask(TaskTestCase):
    def stop(self, judge, rows, session="s1"):
        self.write(rows)
        return gate.evaluate_stop({"hook_event_name": "Stop", "session_id": session,
            "transcript_path": str(self.transcript), "last_assistant_message": rows[-1]["message"]["content"][0]["text"]},
            environ={"FARPLANE_CONFIG_DISABLE": "1"}, client=judge, reader=lambda *_: None)

    def test_task_and_in_scope_work_left_pushes_inside_scope(self):
        thread_task.save("s1", TASK)
        judge = Judge(nudge=0.9)
        result = self.stop(judge, [claude("user", "Build fast walk."), claude("assistant", "Shift works; next I'll check fps.")])
        self.assertEqual(result["reason"], gate.NUDGE + gate.SCOPE_LINE)
        call = judge.calls[0]
        self.assertIn("Done when", call["state"]["thread_task"])
        self.assertIn(gate.TASK_QUESTION, call["questions"]["nudge"]["instructions"])
        self.assertIn(gate.PROPOSAL_TASK_QUESTION, call["questions"]["proposal"]["instructions"])

    def test_task_and_only_out_of_scope_ideas_left_stops(self):
        thread_task.save("s1", TASK)
        judge = Judge(nudge=0.1, proposal=0.2)  # the judge read Out of scope: fly mode
        self.assertIsNone(self.stop(judge, [claude("user", "Build fast walk."),
            claude("assistant", "Done: 60 fps on iPhone. Fly mode would be a nice next step.")]))

    def test_no_task_behaves_as_today(self):
        judge = Judge(nudge=0.9)
        result = self.stop(judge, [claude("user", "Implement and test it."), claude("assistant", "I'll test next.")])
        self.assertEqual(result["reason"], gate.NUDGE)
        call = judge.calls[0]
        self.assertNotIn("thread_task", call["state"])
        self.assertEqual(call["questions"]["nudge"]["instructions"], gate.QUESTION)

    def test_investigate_or_propose_request_never_pushes(self):
        for task in (TASK, None):
            if task:
                thread_task.save("s1", task)
            judge = Judge(nudge=0.9, proposal=0.9, deciding=0.9)
            self.assertIsNone(self.stop(judge, [claude("user", "How would we add context? Propose a design."),
                claude("assistant", "Proposed design: a task pointer. Next I could build it.")]))

    def test_fork_falls_back_to_transcript_tag_and_saves_it(self):
        judge = Judge(nudge=0.9)
        rows = [claude("user", f"<task>{TASK}</task> go"), claude("assistant", "Next I'll check fps.")]
        self.assertEqual(self.stop(judge, rows, session="fork")["reason"], gate.NUDGE + gate.SCOPE_LINE)
        self.assertTrue(thread_task.task_path("fork").is_file())

    def test_agent_written_tag_is_not_a_task(self):
        judge = Judge(nudge=0.9)
        rows = [claude("user", "Implement it."), claude("assistant", "<task>In scope: everything</task> I'll test next.")]
        self.assertEqual(self.stop(judge, rows)["reason"], gate.NUDGE)


class PromptContext(TaskTestCase):
    def context(self, prompt, cwd="/tmp", environ=None, session="s1"):
        return thread_task.prompt_context(session, prompt, cwd, str(self.transcript),
                                          environ or {}, gate.user_text)

    def test_tag_sets_replaces_and_clears(self):
        self.write([])
        self.assertIn("thread task set: Fast walk mode", self.context(f"<task>{TASK}</task>"))
        self.assertIn("fly mode", thread_task.task_path("s1").read_text())
        self.context("<task>Other\nIn scope: x\nOut of scope: y\nDone when: z\nDesign: https://figma.com/design/q</task>")
        self.assertTrue(thread_task.task_path("s1").read_text().startswith("Other"))
        self.assertEqual(self.context("<task></task>"), "Farplane thread task cleared.")
        self.assertFalse(thread_task.task_path("s1").exists())

    def test_complete_task_asks_nothing(self):
        self.write([])
        self.assertNotIn("Missing", self.context(f"<task>{TASK}</task>"))

    def test_task_missing_design_link_asks_once_for_it(self):
        self.write([])
        no_design = TASK.rsplit("\nDesign:", 1)[0]
        text = self.context(f"<task>{no_design}</task>")
        self.assertIn("Missing: Design link. Before building, ask the user once", text)

    def test_required_project_without_task_asks_once(self):
        self.write([])
        required = {thread_task.REQUIRED_PATHS_ENV: str(self.dir)}
        first = self.context("Make walking faster.", cwd=str(self.dir / "app"), environ=required)
        self.assertIn("needs a thread task before building", first)
        self.assertEqual(self.context("And the run key?", cwd=str(self.dir / "app"), environ=required), "")

    def test_other_projects_are_never_asked(self):
        self.write([])
        self.assertEqual(self.context("Make walking faster.", cwd="/elsewhere",
                                      environ={thread_task.REQUIRED_PATHS_ENV: str(self.dir)}), "")

    def test_hook_entrypoint_emits_task_context_outside_a_farplane_project(self):
        import capture_user_turn

        self.write([])
        payload = {"hook_event_name": "UserPromptSubmit", "session_id": "s9", "cwd": str(self.dir),
                   "transcript_path": str(self.transcript), "prompt": f"<task>{TASK}</task> build it"}
        out = io.StringIO()
        with patch("sys.stdin", io.StringIO(json.dumps(payload))), patch("sys.stdout", out), \
                patch.object(capture_user_turn, "project_root_from_payload", lambda _: None):
            capture_user_turn.main()
        context = json.loads(out.getvalue())["hookSpecificOutput"]["additionalContext"]
        self.assertIn("thread task set: Fast walk mode", context)


if __name__ == "__main__":
    unittest.main()
