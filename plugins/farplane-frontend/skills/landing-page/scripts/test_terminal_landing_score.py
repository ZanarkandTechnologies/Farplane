#!/usr/bin/env python3
"""Tests for Terminal landing score helper edge cases."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("terminal_landing_score.py")
SPEC = importlib.util.spec_from_file_location("terminal_landing_score", MODULE_PATH)
assert SPEC and SPEC.loader
terminal_landing_score = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = terminal_landing_score
SPEC.loader.exec_module(terminal_landing_score)


class TerminalLandingScoreTests(unittest.TestCase):
    def test_handoff_complete_accepts_semantic_headings(self) -> None:
        self.assertTrue(
            terminal_landing_score.handoff_complete(
                "\n".join(
                    [
                        "## Changed / Produced Files",
                        "- media-repair.js",
                        "## Self-Review Findings",
                        "- node --check passed",
                        "## Risks / Followups",
                        "- none",
                    ]
                )
            )
        )

    def test_handoff_complete_rejects_empty_section_bodies(self) -> None:
        self.assertFalse(
            terminal_landing_score.handoff_complete(
                "\n".join(
                    [
                        "## Changed Files",
                        "## Verification",
                        "- node --check passed",
                        "## Risks / Followups",
                        "- none",
                    ]
                )
            )
        )

    def test_output_quality_failed_is_not_ok(self) -> None:
        self.assertTrue(terminal_landing_score.output_quality_ok({}))
        self.assertTrue(terminal_landing_score.output_quality_ok({"output_quality": {"status": "pass"}}))
        self.assertFalse(terminal_landing_score.output_quality_ok({"output_quality": {"status": "failed"}}))


if __name__ == "__main__":
    unittest.main()
