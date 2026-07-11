#!/usr/bin/env python3
"""Tests for eval-drain discovery."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_evals_edited_since_last_run.py"
SPEC = importlib.util.spec_from_file_location("fetch_evals_edited_since_last_run", SCRIPT_PATH)
assert SPEC is not None
fetcher = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["fetch_evals_edited_since_last_run"] = fetcher
SPEC.loader.exec_module(fetcher)


def write_eval(path: Path, task_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "skill_name": path.parents[1].name,
                "evals": [
                    {
                        "id": task_id,
                        "prompt": "Do the thing.",
                        "expected_output": "Names the thing.",
                        "files": [],
                        "assertions": ["Names the thing"],
                    }
                ],
            }
        )
    )


class FetchEvalChangesTests(unittest.TestCase):
    def test_missing_state_marks_skill_eval_files_new(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_eval(root / "skills" / "eval" / "evals/evals.json", "eval_01")

            result = fetcher.changed_eval_files(root, root / ".farplane/state/eval-drain/processed.jsonl")

        self.assertEqual(result["changed_count"], 1)
        self.assertEqual(result["eval_files"][0]["path"], "skills/eval/evals/evals.json")
        self.assertEqual(result["eval_files"][0]["reason"], "new")
        self.assertEqual(result["eval_files"][0]["task_count"], 1)

    def test_processed_hash_suppresses_unchanged_eval_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_path = root / "skills" / "eval" / "evals/evals.json"
            state_path = root / ".farplane/state/eval-drain/processed.jsonl"
            write_eval(eval_path, "eval_01")
            content_hash = fetcher.sha256_text(eval_path.read_text())
            state_path.parent.mkdir(parents=True)
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "eval_ref": "skills/eval/evals/evals.json",
                        "content_hash": content_hash,
                        "drained_at": "2026-06-13T00:00:00Z",
                        "disposition": "consolidated",
                    }
                )
                + "\n"
            )

            result = fetcher.changed_eval_files(root, state_path)

        self.assertEqual(result["changed_count"], 0)
        self.assertEqual(result["eval_files"], [])

    def test_changed_hash_reports_changed_eval_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_path = root / "skills" / "eval" / "evals/evals.json"
            state_path = root / ".farplane/state/eval-drain/processed.jsonl"
            write_eval(eval_path, "eval_01")
            old_hash = fetcher.sha256_text(eval_path.read_text())
            state_path.parent.mkdir(parents=True)
            state_path.write_text(
                json.dumps(
                    {
                        "eval_ref": "skills/eval/evals/evals.json",
                        "content_hash": old_hash,
                    }
                )
                + "\n"
            )
            write_eval(eval_path, "eval_02")

            result = fetcher.changed_eval_files(root, state_path)

        self.assertEqual(result["changed_count"], 1)
        self.assertEqual(result["eval_files"][0]["reason"], "changed")
        self.assertEqual(result["eval_files"][0]["previous_hash"], old_hash)

    def test_invalid_eval_json_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "skills" / "eval" / "evals/evals.json"
            path.parent.mkdir(parents=True)
            path.write_text("{not json")

            with self.assertRaises(fetcher.FetchError):
                fetcher.changed_eval_files(root, root / "state.jsonl")


if __name__ == "__main__":
    unittest.main()
