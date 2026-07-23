from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("guard_preflight.py")
SPEC = importlib.util.spec_from_file_location("guard_preflight", MODULE_PATH)
preflight = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(preflight)


class GuardPreflightTest(unittest.TestCase):
    def fixture(self) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "farplane").mkdir()
        (root / "farplane" / "harness.yaml").write_text("metric_refs:\n  guards: [health_gap_count]\n", encoding="utf-8")
        (root / "farplane" / "metrics.yaml").write_text(
            """refreshers:
  health:
    refresh: Run the health compiler.
    provides: [health_gap_count]
metrics:
  health_gap_count:
    refresh_ref: health
    max_age_days: 1
    guard:
      operator: less_than_or_equal
      threshold: 0
""",
            encoding="utf-8",
        )
        return root

    def add_shared_guard(self, root: Path) -> None:
        (root / "farplane" / "harness.yaml").write_text(
            "metric_refs:\n  guards: [health_gap_count, second_gap_count]\n", encoding="utf-8"
        )
        path = root / "farplane" / "metrics.yaml"
        path.write_text(path.read_text(encoding="utf-8") + """  second_gap_count:
    refresh_ref: health
    max_age_days: 1
    guard:
      operator: less_than_or_equal
      threshold: 0
""", encoding="utf-8")

    def write_observation(self, root: Path, observed_at: str, value: float | None, status: str = "available") -> None:
        path = root / ".farplane" / "metrics" / "observations" / "health" / f"{observed_at}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"observations": [{"metric_id": "health_gap_count", "date": observed_at, "value": value, "status": status}]}), encoding="utf-8")

    def test_stale_healthy_refreshes_then_allows_same_wave_planning(self) -> None:
        root = self.fixture()
        self.write_observation(root, "2026-07-13", 0)
        started = preflight.begin(root, "2026-07-16")
        self.assertEqual(started["status"], "refresh_required")
        self.assertEqual(started["refresh_dispatches"][0]["refresh_ref"], "health")
        self.write_observation(root, "2026-07-16", 0)
        finished = preflight.finish(root, "2026-07-16", ["health"])
        self.assertEqual(finished["status"], "ready")
        self.assertTrue(finished["planner_allowed"])
        self.assertEqual(finished["wave_slots_consumed"], 0)

    def test_refreshed_failing_guard_blocks_real_gap(self) -> None:
        root = self.fixture()
        self.write_observation(root, "2026-07-13", 0)
        self.assertEqual(preflight.begin(root, "2026-07-16")["status"], "refresh_required")
        self.write_observation(root, "2026-07-16", 2)
        finished = preflight.finish(root, "2026-07-16", ["health"])
        self.assertEqual(finished["status"], "blocked_guard")
        self.assertFalse(finished["planner_allowed"])

    def test_refresh_failure_returns_source_gap_without_wave_slot(self) -> None:
        root = self.fixture()
        self.write_observation(root, "2026-07-13", 0)
        finished = preflight.finish(root, "2026-07-16", ["health"])
        self.assertEqual(finished["status"], "source_gap")
        self.assertFalse(finished["planner_allowed"])
        self.assertEqual(finished["wave_slots_consumed"], 0)

    def test_two_stale_guards_share_one_provider_dispatch(self) -> None:
        root = self.fixture()
        self.add_shared_guard(root)
        started = preflight.begin(root, "2026-07-16")
        self.assertEqual(len(started["refresh_dispatches"]), 1)
        self.assertEqual(
            started["refresh_dispatches"][0]["metric_ids"],
            ["health_gap_count", "second_gap_count"],
        )

    def test_planning_fingerprint_only_begins_after_current_healthy_reload(self) -> None:
        root = self.fixture()
        self.write_observation(root, "2026-07-13", 0)
        blocked = preflight.begin_planning_if_ready(
            root, "2026-07-16", ["health"], ["health"], {"candidate_pool": ["D1"]}, 5
        )
        self.assertIsNone(blocked["planning"])
        self.assertFalse((root / ".farplane" / "automation" / "plan-next-wave.lock").exists())
        self.write_observation(root, "2026-07-16", 0)
        ready = preflight.begin_planning_if_ready(
            root, "2026-07-16", ["health"], ["health"], {"candidate_pool": ["D1"]}, 5
        )
        self.assertEqual(ready["planning"]["status"], "acquired")
        self.assertIn("planning_fingerprint", ready["planning"])


if __name__ == "__main__":
    unittest.main()
