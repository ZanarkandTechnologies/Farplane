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
- Feature/spec registry: [docs/features/README.md](/abs/docs/features/README.md)
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

FEATURES_README_TEXT = """\
# Feature Docs

Farplane feature docs are the spec files for first-class capabilities.
This folder is the authored source for feature specs and generated feature records.
Do not create a second spec-folder truth shelf for feature behavior.

Run:

```bash
python3 docs/features/validate_features.py --write
```

Delete a `FEAT-*` handle when it no longer earns a feature spec page.
Do not keep a retired alias just to preserve noise.
"""

REGISTRY_OS_TEXT = """\
# Registry-backed documentation OS

Feature docs are the spec files.

Run `python3 bin/validators/check_doc_parity.py`.

No parallel spec-folder truth shelf.

No compatibility feature rows for capabilities that do not earn their own feature spec.
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
- ticket_change_plan(delta, change_units, qa_strategy) -> artifact_delta + evidence + state_delta
- `QA Strategy`
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
        write_file(root / "docs/features/README.md", FEATURES_README_TEXT)
        write_file(root / "docs/features/FEAT-0060-registry-backed-documentation-os.md", REGISTRY_OS_TEXT)
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
            self.assertIn("Feature/spec registry", result.stdout)


if __name__ == "__main__":
    unittest.main()
