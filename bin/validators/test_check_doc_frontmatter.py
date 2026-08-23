from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_doc_frontmatter",
    ROOT / "bin" / "validators" / "check_doc_frontmatter.py",
)
assert SPEC and SPEC.loader
check_doc_frontmatter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_doc_frontmatter)


class DocumentFrontmatterLintTests(unittest.TestCase):
    def test_lints_valid_frontmatter_and_ignores_plain_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "typed.md").write_text("---\ntitle: Typed\n---\n", encoding="utf-8")
            (docs / "plain.md").write_text("# Plain\n", encoding="utf-8")

            checked, errors = check_doc_frontmatter.lint_docs_frontmatter(root)

        self.assertEqual(checked, 1)
        self.assertEqual(errors, [])

    def test_rejects_duplicate_frontmatter_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "duplicate.md").write_text(
                "---\ntitle: One\ntitle: Two\n---\n",
                encoding="utf-8",
            )

            _checked, errors = check_doc_frontmatter.lint_docs_frontmatter(root)

        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate frontmatter keys: title", errors[0])


if __name__ == "__main__":
    unittest.main()
