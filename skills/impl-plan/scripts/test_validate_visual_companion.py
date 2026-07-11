#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_visual_companion import validate


VALID = """---
blocks_approval: false
canonical_contract: ticket.md
---
## Before
```mermaid
flowchart LR
classDef before fill:#fff
node["before"]:::before
```
Legend: before
## After
```mermaid
flowchart LR
classDef after fill:#000
node["after"]:::after
```
Legend: after
"""


class VisualCompanionTest(unittest.TestCase):
    def test_valid_companion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("# Ticket\n- Visual companion: `diagrams.md`\n")
            (root / "diagrams.md").write_text(VALID)
            self.assertEqual(validate(ticket), [])

    def test_missing_companion_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = Path(tmp) / "ticket.md"
            ticket.write_text("# Ticket\n")
            self.assertTrue(any("does not exist" in error for error in validate(ticket)))

    def test_missing_ticket_link_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("# Ticket\n")
            (root / "diagrams.md").write_text(VALID)
            self.assertTrue(any("missing required visual companion link" in error for error in validate(ticket)))

    def test_inline_diagram_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("```mermaid\nflowchart LR\n```\n")
            (root / "diagrams.md").write_text(VALID)
            self.assertTrue(any("embeds diagram" in error for error in validate(ticket)))

    def test_embedded_markdown_url_and_html_fail(self):
        for embedded in ("![system](architecture-diagram.png)", '<img src="flow.svg">'):
            with self.subTest(embedded=embedded), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                ticket = root / "ticket.md"
                ticket.write_text(f"- Visual companion: `diagrams.md`\n{embedded}\n")
                (root / "diagrams.md").write_text(VALID)
                self.assertTrue(any("embeds diagram" in error for error in validate(ticket)))

    def test_malformed_sections_and_unused_class_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("- Visual companion: `diagrams.md`\n")
            malformed = VALID.replace("## Before", "## Beforethought").replace(":::after", "")
            (root / "diagrams.md").write_text(malformed)
            errors = validate(ticket)
            self.assertTrue(any("anchored ## Before" in error for error in errors))
            self.assertTrue(any("applied semantic classes" in error for error in errors))

    def test_prose_mention_and_mismatched_classes_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("Visual companion: do not create diagrams.md\n")
            malformed = VALID.replace(":::before", ":::undefinedBefore").replace(":::after", ":::undefinedAfter")
            (root / "diagrams.md").write_text(malformed)
            errors = validate(ticket)
            self.assertTrue(any("missing required visual companion link" in error for error in errors))
            self.assertGreaterEqual(sum("matching defined" in error for error in errors), 2)


if __name__ == "__main__":
    unittest.main()
