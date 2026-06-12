#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "bin" / "validators" / "check_doc_parity.py"
SUBPROCESS_TIMEOUT_SECONDS = 5


README_TEXT = """\
# Farplane

- Architecture map: [ARCHITECTURE.md](/abs/ARCHITECTURE.md)
- Feature inventory: [harness-techniques.md](/abs/docs/specs/harness-techniques.md)
- Review scoring: [skills/review/README.md](/abs/skills/review/README.md)
- Active queue: [tickets](/abs/tickets) is the live board; do not rely on hardcoded queue summaries here
"""

ARCHITECTURE_TEXT = """\
# Farplane Architecture

## Canonical Surfaces

- `README.md`
- `tickets/README.md`
- `docs/review/rubrics/review-rubric-index.md`
"""

SPECS_README_TEXT = """\
# Specs

- [`ARCHITECTURE.md`](/abs/ARCHITECTURE.md) - top-level system map and canonical surface guide
- `doc-governance.md` - structural versus narrative doc-audit policy
- `harness-techniques.md` - current-state feature and technique inventory

## Doc Gardening Loop

1. Run `python3 tickets/scripts/check_ticket_metadata.py`.
2. Run `python3 bin/validators/check_doc_parity.py`.
3. Use `codex exec` for narrative doc audits.
"""

TECHNIQUES_TEXT = """\
# Harness Techniques

This document is the repo's current-state feature inventory first. It is not a
generic harness wishlist.

## Audit Basis

- `ARCHITECTURE.md`
- `tickets/README.md`

## Implemented Techniques

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Mechanical knowledge-base entrypoint checks | Implemented | `bin/validators/check_doc_parity.py`, `docs/specs/doc-governance.md`, `README.md`, `ARCHITECTURE.md`, `docs/specs/README.md`, `tickets/README.md` | Keeps the top-level knowledge-base entry surfaces linked and catches stale queue claims without over-linting all prose | intentionally narrow; it does not replace narrative document review |
| Doc-governance workflow for narrative drift | Implemented | `docs/specs/doc-governance.md`, `docs/specs/README.md` | Gives flexible docs a repeatable audit path without requiring brittle substring validators for every story change | still depends on humans running the audit loop; no recurring maintainer agent yet |
"""

DOC_GOVERNANCE_TEXT = """\
# Doc Governance

## Structural Checks

- `python3 bin/validators/check_doc_parity.py`

## Narrative Audit

Use `codex exec` when the question is about the quality of the story rather than a required link.
"""

TICKETS_README_TEXT = """\
# Tickets

## Validator

Run:

```bash
python3 tickets/scripts/check_ticket_metadata.py
```

## Body Contract

- The default `Plan` should answer four things:
- task_program(vars, operations, proof) -> artifact + evidence + state_delta
- `Done / Proof`
- Store ticket artifacts under `tickets/TASK-XXXX/artifacts/`.

## Progress Surface Policy

- the ticket is the canonical durable progress surface
"""


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


class CheckDocParityTest(unittest.TestCase):
    def build_repo(self, root: Path) -> None:
        write_file(root / "README.md", README_TEXT)
        write_file(root / "ARCHITECTURE.md", ARCHITECTURE_TEXT)
        write_file(root / "docs/specs/README.md", SPECS_README_TEXT)
        write_file(root / "docs/specs/harness-techniques.md", TECHNIQUES_TEXT)
        write_file(root / "docs/specs/doc-governance.md", DOC_GOVERNANCE_TEXT)
        write_file(root / "tickets/README.md", TICKETS_README_TEXT)

    def run_validator(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
        )

    def test_validator_passes_for_valid_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("structural doc parity OK", result.stdout)

    def test_validator_fails_on_stale_queue_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "README.md",
                README_TEXT + "\n- Active queue: none currently; the next slice should be opened as a new ticket\n",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("contains forbidden stale text", result.stdout)

    def test_validator_fails_when_feature_inventory_pointer_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "README.md",
                """\
# Farplane

- Active queue: [tickets](/abs/tickets) is the live board; do not rely on hardcoded queue summaries here
""",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Feature inventory", result.stdout)


if __name__ == "__main__":
    unittest.main()
