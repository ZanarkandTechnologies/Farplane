import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = ROOT / "runtime" / "file_growth_hook.py"


def load_hook_module():
    spec = importlib.util.spec_from_file_location("file_growth_hook_test", HOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load hook module from {HOOK_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FileGrowthHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hook = load_hook_module()

    def test_apply_patch_payload_summarizes_overgrown_matching_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="file-growth-hook-") as td:
            root = Path(td)
            (root / "farplane").mkdir()
            (root / "farplane" / "hooks.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "hooks": {
                            "file_growth": {
                                "enabled": True,
                                "rules": [
                                    {
                                        "name": "memory",
                                        "patterns": ["memory.mb"],
                                        "max_lines": 3,
                                        "target_lines": 2,
                                        "action": "summarize_in_place",
                                    }
                                ],
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            (root / "memory.mb").write_text("one\ntwo\nthree\nfour\n", encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "apply_patch",
                "cwd": str(root),
                "tool_input": "*** Begin Patch\n*** Update File: memory.mb\n@@\n+four\n*** End Patch\n",
            }

            with patch.dict(os.environ, {"FARPLANE_FILE_GROWTH_FAKE_SUMMARY": "compact\nmemory"}, clear=False):
                rows = self.hook.handle_payload(payload)

            self.assertEqual(rows[0]["event"], "summarized")
            self.assertEqual((root / "memory.mb").read_text(encoding="utf-8"), "compact\nmemory\n")
            log_rows = [
                json.loads(line)
                for line in (root / ".farplane" / "logs" / "file-growth-hook.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
            ]
            self.assertEqual(log_rows[-1]["event"], "summarized")

    def test_matching_file_below_threshold_is_logged_and_left_unchanged(self) -> None:
        with tempfile.TemporaryDirectory(prefix="file-growth-hook-") as td:
            root = Path(td)
            (root / "farplane").mkdir()
            (root / "farplane" / "hooks.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "hooks": {
                            "file_growth": {
                                "enabled": True,
                                "rules": [
                                    {
                                        "name": "memory",
                                        "patterns": ["memory.mb"],
                                        "max_lines": 10,
                                        "target_lines": 2,
                                        "action": "summarize_in_place",
                                    }
                                ],
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            (root / "memory.mb").write_text("one\ntwo\n", encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "cwd": str(root),
                "changedFiles": ["memory.mb"],
            }

            rows = self.hook.handle_payload(payload)

            self.assertEqual(rows[0]["event"], "skip_file")
            self.assertEqual(rows[0]["reason"], "below_threshold")
            self.assertEqual((root / "memory.mb").read_text(encoding="utf-8"), "one\ntwo\n")


if __name__ == "__main__":
    unittest.main()
