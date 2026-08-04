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
    def test_no_companion_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = Path(tmp) / "ticket.md"
            ticket.write_text("# Ticket\n")
            self.assertEqual(validate(ticket), [])

    def test_valid_companion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("# Ticket\n- Visual companion: `diagrams.md`\n")
            (root / "diagrams.md").write_text(VALID)
            self.assertEqual(validate(ticket), [])

    def test_linked_missing_companion_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = Path(tmp) / "ticket.md"
            ticket.write_text("# Ticket\n- Visual companion: `diagrams.md`\n")
            self.assertTrue(any("does not exist" in error for error in validate(ticket)))

    def test_missing_ticket_link_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("# Ticket\n")
            (root / "diagrams.md").write_text(VALID)
            self.assertTrue(any("orphaned companion" in error for error in validate(ticket)))

    def test_inline_mermaid_is_valid_without_companion(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = Path(tmp) / "ticket.md"
            ticket.write_text("```mermaid\nflowchart LR\n```\n")
            self.assertEqual(validate(ticket), [])

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

    def test_prose_mention_does_not_count_as_companion_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "ticket.md"
            ticket.write_text("Visual companion: do not create diagrams.md\n")
            (root / "diagrams.md").write_text(VALID)
            errors = validate(ticket)
            self.assertTrue(any("orphaned companion" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
