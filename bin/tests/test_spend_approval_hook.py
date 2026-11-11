from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "hooks/spend-approval/spend_approval.sh"
APPROVE = ROOT / "hooks/spend-approval/approve.py"

# Commands that cost money on Modal in the week of 10 Nov 2026 (paths shortened).
SPENDS = (
    "cd research/corl-2026/robosnap && modal run --detach modal_app.py::build",
    "modal deploy -e dev services/walls/modal_app.py",
    "cd ~/Eddison/oures && sh deploy/release.sh dev idol 2>&1 | tail -6",
    "MODAL_PROFILE=kenjipcx modal shell --env dev oures-walls",
    "doppler run -p oures -c prd -- modal serve services/stream/modal_app.py",
)
FREE = (
    "modal app list --env dev",
    "modal billing report --for today --json",
    "modal volume ls --env dev oures-ai-cache /",
    "cat services/scan-build/modal_app.py",
    "git status",
)


def hook(cmd: str, approvals: Path) -> str:
    payload = {"tool_name": "Bash", "tool_input": {"command": cmd}}
    env = {**os.environ, "FARPLANE_APPROVALS": str(approvals)}
    return subprocess.run(["sh", str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env=env, check=True).stdout


def approve(*args: str, approvals: Path, sent: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "FARPLANE_APPROVALS": str(approvals), "FARPLANE_APPROVAL_SEND": f"cat > '{sent}'"}
    return subprocess.run(["python3", str(APPROVE), *args], capture_output=True, text=True, env=env)


class SpendApprovalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.dir, self.sent = self.tmp / "approvals", self.tmp / "sent.txt"

    def test_spends_are_denied_without_a_grant(self) -> None:
        for cmd in SPENDS:
            self.assertIn('"permissionDecision":"deny"', hook(cmd, self.dir), cmd)

    def test_free_commands_pass(self) -> None:
        for cmd in FREE:
            self.assertEqual(hook(cmd, self.dir), "", cmd)

    def test_code_goes_to_the_phone_only_and_opens_a_window(self) -> None:
        r = approve("request", "RoboSnap image build", "--usd", "5", "--minutes", "30", approvals=self.dir, sent=self.sent)
        self.assertEqual(r.returncode, 0)
        code = self.sent.read_text().split("Code: ")[1][:6]
        self.assertNotIn(code, r.stdout)
        self.assertNotIn(code, (self.dir / "pending.json").read_text())
        self.assertEqual(approve("grant", "000000" if code != "000000" else "111111", approvals=self.dir, sent=self.sent).returncode, 1)
        self.assertEqual(approve("grant", code, approvals=self.dir, sent=self.sent).returncode, 0)
        self.assertEqual(hook(SPENDS[0], self.dir), "")
        (self.dir / "grant").write_text(f"{int(time.time()) - 1}\nold\n5\n")
        self.assertIn("deny", hook(SPENDS[0], self.dir))

    def test_three_wrong_codes_cancel(self) -> None:
        approve("request", "x", "--usd", "1", approvals=self.dir, sent=self.sent)
        code = self.sent.read_text().split("Code: ")[1][:6]
        wrong = "000000" if code != "000000" else "111111"
        for _ in range(3):
            approve("grant", wrong, approvals=self.dir, sent=self.sent)
        self.assertEqual(approve("grant", code, approvals=self.dir, sent=self.sent).returncode, 1)
        self.assertIn("deny", hook(SPENDS[0], self.dir))


if __name__ == "__main__":
    unittest.main()
