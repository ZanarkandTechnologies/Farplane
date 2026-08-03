from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / "hooks" / "shared_checkout_guard.py"
SPEC = importlib.util.spec_from_file_location("shared_checkout_guard", HOOK_PATH)
assert SPEC is not None and SPEC.loader is not None
shared_checkout_guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shared_checkout_guard)


class SharedCheckoutGuardTests(unittest.TestCase):
    def git(self, cwd: Path, *args: str) -> None:
        subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL)

    def payload(self, event: str, session: str, cwd: Path) -> dict[str, object]:
        return {
            "hook_event_name": event,
            "session_id": session,
            "turn_id": f"turn-{session}",
            "cwd": str(cwd),
        }

    def test_primary_checkout_allows_one_writer_and_blocks_another_until_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            self.git(root, "init")
            self.assertIsNone(shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "one", root), now=100.0))
            reason = shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "two", root), now=101.0)
            self.assertIn("active Codex writer (one)", reason or "")
            shared_checkout_guard.evaluate(self.payload("Stop", "one", root), now=102.0)
            self.assertIsNone(shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "two", root), now=103.0))

    def test_stop_from_non_owner_does_not_release_lease(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            self.git(root, "init")
            shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "one", root), now=100.0)
            shared_checkout_guard.evaluate(self.payload("Stop", "two", root), now=101.0)
            self.assertIsNotNone(shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "two", root), now=102.0))

    def test_stale_lease_can_be_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            self.git(root, "init")
            shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "old", root), now=100.0)
            with patch.dict("os.environ", {"FARPLANE_SHARED_CHECKOUT_LEASE_SECONDS": "60"}):
                self.assertIsNone(shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "new", root), now=161.0))

    def test_linked_worktree_is_always_isolated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            linked = Path(tmp) / "linked"
            root.mkdir()
            self.git(root, "init")
            (root / "README.md").write_text("x\n", encoding="utf-8")
            self.git(root, "add", "README.md")
            self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init")
            self.git(root, "worktree", "add", "--detach", str(linked), "HEAD")
            self.assertIsNone(shared_checkout_guard.evaluate(self.payload("UserPromptSubmit", "one", linked), now=100.0))
            self.assertFalse((root / ".git" / shared_checkout_guard.LEASE_NAME).exists())

    def test_main_emits_codex_block_decision(self) -> None:
        with patch.object(shared_checkout_guard, "read_payload", return_value={}), patch.object(
            shared_checkout_guard, "evaluate", return_value="use a worktree"
        ), patch("sys.stdout.write") as stdout:
            self.assertEqual(shared_checkout_guard.main(), 0)
            rendered = "".join(call.args[0] for call in stdout.call_args_list)
            self.assertEqual(json.loads(rendered), {"decision": "block", "reason": "use a worktree"})


if __name__ == "__main__":
    unittest.main()
