from __future__ import annotations

import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compile_review_call  # noqa: E402

ISSUE_BODY = """## Summary

Ship the CSV export.

## Done / Proof

- [ ] Export downloads.

## Current Goal state

decision: report_now
"""


def run_main(argv: list[str]) -> dict:
    out = io.StringIO()
    with mock.patch.object(sys, "argv", ["compile_review_call.py", *argv]), redirect_stdout(out):
        compile_review_call.main()
    return json.loads(out.getvalue())


class CompileReviewCallTests(unittest.TestCase):
    def test_issue_reads_title_and_sections_through_gh(self) -> None:
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=json.dumps({"title": "CSV export", "body": ISSUE_BODY}), stderr=""
        )
        with mock.patch.object(compile_review_call.subprocess, "run", return_value=completed) as run:
            metadata = run_main(["--issue", "acme/app#421", "--dry-run"])
        self.assertEqual(
            ["gh", "issue", "view", "421", "-R", "acme/app", "--json", "title,body"], run.call_args.args[0]
        )
        context = metadata["review_context"]
        self.assertEqual("CSV export", context["title"])
        self.assertEqual("Ship the CSV export.", context["objective"])
        self.assertEqual("decision: report_now", context["why_it_matters"])

    def test_issue_ref_must_name_repo_and_number(self) -> None:
        with self.assertRaises(SystemExit):
            run_main(["--issue", "421", "--dry-run"])

    def test_issue_and_ticket_are_mutually_exclusive(self) -> None:
        with self.assertRaises(SystemExit), redirect_stdout(io.StringIO()), mock.patch.object(sys, "stderr", io.StringIO()):
            run_main(["--issue", "acme/app#1", "--ticket", "t.md", "--dry-run"])


if __name__ == "__main__":
    unittest.main()
