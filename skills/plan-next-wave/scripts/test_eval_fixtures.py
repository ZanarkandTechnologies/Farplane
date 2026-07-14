#!/usr/bin/env python3
"""Contract checks for Plan Next Wave eval fixtures."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MEMORY_VALIDATOR = ROOT / "skills" / "feed-scout" / "scripts" / "validate_memory.py"
FIXTURE = ROOT / "skills" / "plan-next-wave" / "evals" / "fixtures" / "icp-world-memory.md"
HARNESS = ROOT / "farplane" / "harness.yaml"


def load_memory_validator():
    module_spec = importlib.util.spec_from_file_location("feed_scout_memory_validator", MEMORY_VALIDATOR)
    assert module_spec and module_spec.loader
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


class EvalFixtureContractTest(unittest.TestCase):
    def test_icp_world_memory_fixture_passes_feed_scout_contract(self) -> None:
        validator = load_memory_validator()
        self.assertEqual([], validator.validate_memory(FIXTURE, harness_path=HARNESS))


if __name__ == "__main__":
    unittest.main()
