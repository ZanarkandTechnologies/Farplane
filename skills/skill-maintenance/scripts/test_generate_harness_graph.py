#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import generate_harness_graph as generator


class GenerateHarnessGraphTests(unittest.TestCase):
    def test_runtime_state_is_excluded_from_reference_scan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            runtime_graph = repo_root / ".farplane" / "generated" / "graphs" / "skill-graph.json"
            runtime_graph.parent.mkdir(parents=True)
            runtime_graph.write_text("{}\n")

            self.assertFalse(generator.should_scan(runtime_graph, repo_root))


if __name__ == "__main__":
    unittest.main()
