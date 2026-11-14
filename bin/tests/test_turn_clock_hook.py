from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import unittest
import unittest.mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "hooks/turn-clock/turn_clock.sh"
SID = "11111111-2222-4333-8444-555555555555"


def hook(turns: Path, runtime: str | None = "claude", **extra: object) -> str:
    # a tool result that quotes another session id must not be read as this session's
    payload = {"session_id": SID, "hook_event_name": "PostToolUse", "tool_name": "Bash", **extra,
               "tool_response": {"stdout": '"session_id": "someone-else"'}}
    env = {k: v for k, v in os.environ.items() if k != "FARPLANE_AGENT_RUNTIME"} | {"FARPLANE_TURNS": str(turns)}
    if runtime:
        env["FARPLANE_AGENT_RUNTIME"] = runtime
    return subprocess.run(["sh", str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env=env, check=True).stdout


class TurnClockTest(unittest.TestCase):
    def setUp(self) -> None:
        self.turns = Path(tempfile.mkdtemp())

    def start(self, minutes_ago: float) -> None:
        (self.turns / SID).write_text(f"{int(time.time() - minutes_ago * 60)}\n0\n")

    def test_quiet_in_the_first_45_minutes(self) -> None:
        self.start(44)
        self.assertEqual(hook(self.turns), "")

    def test_says_once_per_45_minutes(self) -> None:
        self.start(46)
        out = json.loads(hook(self.turns))["hookSpecificOutput"]
        self.assertEqual(out["hookEventName"], "PostToolUse")
        self.assertIn("46 minutes since the last user message", out["additionalContext"])
        self.assertEqual(hook(self.turns), "")
        self.start(91)
        (self.turns / SID).write_text((self.turns / SID).read_text().replace("\n0\n", "\n1\n"))
        self.assertIn("91 minutes", hook(self.turns))

    def test_quiet_for_subagents_other_runtimes_and_unknown_sessions(self) -> None:
        self.start(120)
        self.assertEqual(hook(self.turns, agent_id="a61337"), "")
        self.assertEqual(hook(self.turns, runtime=None), "")
        (self.turns / SID).unlink()
        self.assertEqual(hook(self.turns), "")

    def test_a_user_message_restarts_the_clock(self) -> None:
        import sys
        sys.path.insert(0, str(ROOT / "hooks" / "user-turn"))
        import capture_user_turn as capture
        self.start(300)
        with unittest.mock.patch.dict(os.environ, {"FARPLANE_TURNS": str(self.turns)}):
            capture.start_turn_clock({"session_id": SID})
        self.assertEqual(hook(self.turns), "")
        self.assertEqual((self.turns / SID).read_text().split()[1], "0")


if __name__ == "__main__":
    unittest.main()
