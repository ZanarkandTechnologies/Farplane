from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "hooks/shared", ROOT / "hooks/after-reset"):
    sys.path.insert(0, str(directory))
import after_reset
import thread_notes

SESSION = "387c4ea3-c470-4e42-a2cf-464652b76c14"
GOAL = "Medusa reads the catalogue straight from Supabase, no copy, no sync"


def row(text, **extra):
    return json.dumps({"type": "user", "message": {"role": "user", "content": text}, **extra})


class AfterResetTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        patcher = patch.object(thread_notes, "NOTES_DIR", self.dir / "notes")
        patcher.start()
        self.addCleanup(patcher.stop)
        (self.dir / "notes").mkdir()
        self.transcript = self.dir / "t.jsonl"
        self.transcript.write_text("\n".join([
            row("how bout we just customize the medusa server"),
            row("<system-reminder>linked sessions</system-reminder>\n\nwhy is chairhorse down again"),
            row("Stop hook feedback:\n#### Response format and more words"),
            row("<task-notification>done and more words</task-notification>"),
            row("yes"),
            row([{"type": "tool_result", "content": "tool output with several words"}]),
            row("summary text with several words here", isCompactSummary=True),
            row("subagent prompt with several words here", isSidechain=True),
            "not json with a \"user\" in it",
        ]), encoding="utf-8")

    def test_only_the_users_own_words_come_back(self):
        self.assertEqual(after_reset.user_messages(str(self.transcript)),
                         ["how bout we just customize the medusa server", "why is chairhorse down again"])

    def test_goal_and_messages_survive_a_reset(self):
        (self.dir / "notes" / f"{SESSION}.md").write_text(f"## Open goals\n- {GOAL}\n", encoding="utf-8")
        text = after_reset.context(SESSION, str(self.transcript))
        self.assertIn(GOAL, text)
        self.assertIn("customize the medusa server", text)
        self.assertIn("Your context was just reset", text)

    def test_thread_without_notes_still_gets_the_messages_and_the_path(self):
        text = after_reset.context(SESSION, str(self.transcript))
        self.assertIn("no notes yet", text)
        self.assertIn(f"{SESSION}.md", text)
        self.assertIn("customize the medusa server", text)

    def test_context_stays_under_the_hook_limit_and_keeps_the_latest_message(self):
        self.transcript.write_text("\n".join(row(f"message {i} " + "word " * 80) for i in range(200)),
                                   encoding="utf-8")
        (self.dir / "notes" / f"{SESSION}.md").write_text("x" * 9000, encoding="utf-8")
        text = after_reset.context(SESSION, str(self.transcript))
        self.assertLessEqual(len(text), after_reset.MAX_CONTEXT)
        self.assertIn("message 199", text)

    def test_long_notes_keep_open_goals_when_they_sit_past_the_limit(self):
        notes = "## Task\n" + "old progress\n" * 800 + f"\n## Open goals\n- {GOAL}\n\n## Later\nmore\n"
        kept = thread_notes.with_goals_first(notes, thread_notes.MAX_OWN)
        self.assertLessEqual(len(kept), thread_notes.MAX_OWN)
        self.assertTrue(kept.startswith("## Open goals"))
        self.assertIn(GOAL, kept)

    def test_short_notes_are_unchanged(self):
        self.assertEqual(thread_notes.with_goals_first("## Task\nshort", 100), "## Task\nshort")

    def run_hook(self, payload):
        return subprocess.run([sys.executable, str(ROOT / "hooks/after-reset/after_reset.py")],
                              input=json.dumps(payload), capture_output=True, text=True, check=True).stdout

    def test_hook_speaks_only_after_a_reset(self):
        payload = {"session_id": SESSION, "transcript_path": str(self.transcript)}
        self.assertEqual(self.run_hook({**payload, "source": "startup"}), "")
        output = json.loads(self.run_hook({**payload, "source": "compact"}))["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "SessionStart")
        self.assertIn("customize the medusa server", output["additionalContext"])

    def test_bad_input_never_blocks(self):
        result = subprocess.run([sys.executable, str(ROOT / "hooks/after-reset/after_reset.py")],
                                input="not json", capture_output=True, text=True)
        self.assertEqual((result.returncode, result.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
