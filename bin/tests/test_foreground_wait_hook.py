from __future__ import annotations

import json
import os
import subprocess
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / "hooks/foreground-wait/foreground_wait.sh"

# Foreground waits taken from real Claude threads (15-26 Oct 2026), paths shortened.
REAL_POLLS = (
    "K=~/.runpod/ssh/key; until ssh -i $K -p 22022 root@203.0.113.5 'test -f /workspace/ALLDONE' 2>/dev/null; do sleep 30; done; echo done",
    "cd ~/research/split && until grep -q QDONE queue3.log 2>/dev/null; do sleep 15; done; grep -E ROW queue2.log queue3.log",
    'until grep -q "ok\\|Error" tasks/bmmd936po.output 2>/dev/null; do sleep 10; done; cd ~/research',
    "sleep 30; cat scratchpad/restart.log",
    "for i in $(seq 1 30); do st=$(curl -s $URL); [ \"$st\" = done ] && break; sleep 20; done",
    "while ! adb -s emulator-5600 shell getprop sys.boot_completed | grep -q 1; do\n  sleep 3\ndone",
    "sleep 2m && tail -5 train.log",
)
NOT_WAITS = (
    "ls -la && git status",
    "sleep 5; curl -s localhost:3000",
    "grep -rn 'sleep' hooks/",
    "python3 -m unittest bin/tests/test_stop_gate.py",
)


def run_hook(payload: dict, runtime: str | None = "claude") -> tuple[str, float]:
    env = {key: value for key, value in os.environ.items() if key != "FARPLANE_AGENT_RUNTIME"}
    if runtime:
        env["FARPLANE_AGENT_RUNTIME"] = runtime
    started = time.perf_counter()
    result = subprocess.run(["sh", str(HOOK_PATH)], input=json.dumps(payload), capture_output=True, text=True, env=env, check=True)
    return result.stdout, time.perf_counter() - started


def bash(command: str, **extra: object) -> dict:
    return {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command, **extra}}


def denies(command: str, **extra: object) -> bool:
    return bool(run_hook(bash(command, **extra))[0])


class ForegroundWaitTests(unittest.TestCase):
    def test_real_foreground_polls_are_flagged(self) -> None:
        for command in REAL_POLLS:
            with self.subTest(command=command):
                self.assertTrue(denies(command))

    def test_short_or_unrelated_commands_pass(self) -> None:
        for command in NOT_WAITS:
            with self.subTest(command=command):
                self.assertFalse(denies(command))

    def test_background_and_short_timeout_calls_pass(self) -> None:
        self.assertFalse(denies(REAL_POLLS[0], run_in_background=True))
        self.assertFalse(denies(REAL_POLLS[1], timeout=20000))
        self.assertTrue(denies(REAL_POLLS[1], timeout=600000))

    def test_denies_with_the_rerun_route(self) -> None:
        stdout, _ = run_hook(bash(REAL_POLLS[0]))
        output = json.loads(stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PreToolUse")
        self.assertEqual(output["permissionDecision"], "deny")
        for route in ("run_in_background: true", "Monitor", "timeout: 30000"):
            self.assertIn(route, output["permissionDecisionReason"])

    def test_silent_for_codex_other_tools_and_bad_input(self) -> None:
        self.assertEqual(run_hook(bash(REAL_POLLS[0]), runtime=None)[0], "")
        self.assertEqual(run_hook({"tool_name": "Read", "tool_input": {"file_path": "/tmp/until do sleep 90"}})[0], "")
        self.assertEqual(run_hook({"tool_name": "Bash"})[0], "")

    def test_overhead_stays_under_50_ms(self) -> None:
        """Time above a bare `sh` start, so machine load does not decide the result."""
        def median(command: list[str], payload: str) -> float:
            timings = []
            for _ in range(9):
                started = time.perf_counter()
                subprocess.run(command, input=payload, capture_output=True, text=True, env={**os.environ, "FARPLANE_AGENT_RUNTIME": "claude"})
                timings.append(time.perf_counter() - started)
            return sorted(timings)[4]

        baseline = median(["sh", "-c", "cat >/dev/null"], "{}")
        for command in ("ls -la", REAL_POLLS[0]):
            with self.subTest(command=command):
                self.assertLess(median(["sh", str(HOOK_PATH)], json.dumps(bash(command))) - baseline, 0.05)

if __name__ == "__main__":
    unittest.main()
