#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "bin" / "validators" / "check_doc_refs.py"
SUBPROCESS_TIMEOUT_SECONDS = 5


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


def init_git(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True)


class CheckDocRefsTest(unittest.TestCase):
    def run_validator(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
        )

    def test_validator_passes_for_existing_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_file(
                root / "README.md",
                """\
# Fixture

- [Guide](docs/fundamentals/prompt-engineering.md)
- See `skills/harness-advisor/SKILL.md`.
""",
            )
            write_file(root / "docs/fundamentals/prompt-engineering.md", "# Prompt\n")
            write_file(root / "skills/harness-advisor/SKILL.md", "# Skill\n")
            init_git(root)

            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("doc refs OK", result.stdout)

    def test_validator_fails_for_missing_markdown_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_file(
                root / "README.md",
                """\
# Fixture

- [Old prompt doc](docs/specs/prompt-engineering.md)
""",
            )
            init_git(root)

            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing local ref", result.stdout)
            self.assertIn("docs/specs/prompt-engineering.md", result.stdout)

    def test_validator_fails_for_missing_backticked_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_file(root / "docs/specs/README.md", "See `docs/specs/missing.md`.\n")
            init_git(root)

            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("docs/specs/missing.md", result.stdout)

    def test_validator_ignores_external_urls_and_globs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_file(
                root / "README.md",
                """\
# Fixture

- [OpenAI](https://developers.openai.com/api/docs/guides/prompt-engineering)
- Use `skills/*` and `tickets/TASK-XXXX/ticket.md` as examples.
""",
            )
            init_git(root)

            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
