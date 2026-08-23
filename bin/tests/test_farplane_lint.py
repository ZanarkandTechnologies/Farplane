from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

CORE_DIR = Path(__file__).resolve().parents[1] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
from farplane_lint import _DuplicateKeyError, parse_source_file
from lint.source import MarkdownFrontmatterError, parse_markdown_frontmatter_document


class FarplaneLintSyntaxTests(unittest.TestCase):
    def write_source(self, suffix: str, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / f"source{suffix}"
        path.write_text(text, encoding="utf-8")
        return path

    def test_parses_valid_json_and_yaml(self) -> None:
        parse_source_file(self.write_source(".json", '{"ready": true}'))
        parse_source_file(self.write_source(".yaml", "ready: true\n"))

    def test_rejects_duplicate_json_keys(self) -> None:
        with self.assertRaisesRegex(_DuplicateKeyError, "ready"):
            parse_source_file(self.write_source(".json", '{"ready": true, "ready": false}'))

    def test_rejects_duplicate_yaml_keys(self) -> None:
        with self.assertRaisesRegex(_DuplicateKeyError, "ready"):
            parse_source_file(self.write_source(".yaml", "ready: true\nready: false\n"))

    def test_rejects_duplicate_markdown_frontmatter_keys(self) -> None:
        path = self.write_source(".md", "---\nready: true\nready: false\n---\n# Source\n")

        with self.assertRaisesRegex(MarkdownFrontmatterError, "duplicate frontmatter keys: ready"):
            parse_markdown_frontmatter_document(path.read_text(encoding="utf-8"), path, required=True)


if __name__ == "__main__":
    unittest.main()
