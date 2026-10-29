import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "hooks" / "evidence-mode" / "evidence.py"


def run(*args, state, lid="open", when="2026-10-29T14:00:00+01:00", stdin=""):
    env = {**os.environ, "FARPLANE_EVIDENCE_DIR": state, "FARPLANE_EVIDENCE_LID": lid, "FARPLANE_EVIDENCE_NOW": when}
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True, text=True, env=env)


class EvidenceModeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def mode(self, **kw):
        return run("--mode", state=self.state, **kw).stdout.strip()

    def test_daytime_lid_open_is_awake(self):
        self.assertEqual(self.mode(), "awake")

    def test_lid_closed_is_asleep(self):
        self.assertEqual(self.mode(lid="closed"), "asleep")

    def test_night_without_messages_is_asleep(self):
        self.assertEqual(self.mode(when="2026-10-29T03:00:00+01:00"), "asleep")

    def test_message_at_night_keeps_awake_for_30_min(self):
        run("--hook", state=self.state, when="2026-10-29T03:00:00+01:00", stdin=json.dumps({"prompt": "hi"}))
        self.assertEqual(self.mode(when="2026-10-29T03:20:00+01:00"), "awake")
        self.assertEqual(self.mode(when="2026-10-29T03:31:00+01:00"), "asleep")

    def test_hand_setting_wins_until_auto(self):
        run("asleep", state=self.state)
        self.assertEqual(self.mode(), "asleep")
        run("awake", state=self.state)
        self.assertEqual(self.mode(lid="closed"), "awake")
        run("auto", state=self.state)
        self.assertEqual(self.mode(lid="closed"), "asleep")

    def test_hook_prints_the_turn_line(self):
        out = run("--hook", state=self.state, lid="closed", stdin=json.dumps({"prompt": "go"})).stdout
        self.assertTrue(out.startswith("Evidence: asleep (auto: the lid is closed)"))
        out = run("--hook", state=self.state, stdin=json.dumps({"prompt": "go"})).stdout
        self.assertIn("no recordings", out)


if __name__ == "__main__":
    unittest.main()
