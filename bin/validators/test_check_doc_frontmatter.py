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
            (docs / "typed.md").write_text(
                "---\n"
                "title: Typed\n"
                "status: active\n"
                "owner: docs\n"
                "created_at: 2026-01-01\n"
                "updated_at: 2026-01-01\n"
                "---\n",
                encoding="utf-8",
            )
            (docs / "plain.md").write_text("# Plain\n", encoding="utf-8")

            checked, errors = check_doc_frontmatter.lint_docs_frontmatter(root)

        self.assertEqual(checked, {"narrative": 1})
        self.assertEqual(errors, [])

    def test_entity_page_templates_use_template_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "skills" / "manage-wiki" / "templates"
            folder.mkdir(parents=True)
            (folder / "creator-page.md").write_text(
                "---\n"
                "template_id: creator-page\n"
                'template_version: "0.1.0"\n'
                "kind: entity-page\n"
                "consumer_scope: wiki\n"
                "applies_to:\n"
                "  - .farplane/entities/*.md\n"
                "---\n",
                encoding="utf-8",
            )

            checked, errors = check_doc_frontmatter.lint_docs_frontmatter(root)

        self.assertEqual(checked, {"template": 1})
        self.assertEqual(errors, [])

    def test_moved_skill_templates_keep_template_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "skills" / "harness" / "templates"
            folder.mkdir(parents=True)
            (folder / "SKILL_TEMPLATE.md").write_text(
                "---\n"
                "template_id: skill-template\n"
                'template_version: "0.1.0"\n'
                "consumer_scope: skill\n"
                "---\n",
                encoding="utf-8",
            )
            (folder / "README.md").write_text(
                "---\n"
                "title: Templates\n"
                "status: active\n"
                "owner: harness\n"
                "created_at: 2026-01-01\n"
                "updated_at: 2026-01-01\n"
                "---\n",
                encoding="utf-8",
            )

            checked, errors = check_doc_frontmatter.lint_docs_frontmatter(root)

        self.assertEqual(checked, {"narrative": 1, "template": 1})
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

    def test_rejects_wrong_types_and_unknown_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "invalid.md").write_text(
                "---\n"
                "title: [not, text]\n"
                "status: active\n"
                "owner: docs\n"
                "created_at: 2026-01-01\n"
                "updated_at: 2026-01-01\n"
                "unowned: true\n"
                "---\n",
                encoding="utf-8",
            )

            _checked, errors = check_doc_frontmatter.lint_docs_frontmatter(root)

        self.assertEqual(len(errors), 1)
        self.assertIn("title: Input should be a valid string", errors[0])
        self.assertIn("unowned: Extra inputs are not permitted", errors[0])


if __name__ == "__main__":
    unittest.main()
