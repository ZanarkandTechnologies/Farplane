from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_project_snapshot import load_project_snapshot, write_project_ui_snapshot


def write_minimal_project(root: Path) -> None:
    farplane = root / "farplane"
    farplane.mkdir()
    (farplane / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "farplane_project",
                "project": {
                    "name": "Test Project",
                    "description": "Project description.",
                    "archetype": "test_lab",
                },
            }
        ),
        encoding="utf-8",
    )
    (farplane / "harness.md").write_text("---\nupdated_at: 2026-07-03\n---\n\n# Harness\n", encoding="utf-8")
    (farplane / "ops-memory.md").write_text("---\nupdated_at: 2026-07-03\n---\n\n# Ops\n", encoding="utf-8")
    (farplane / "products.md").write_text(
        """---
updated_at: 2026-07-03
---

# Products

## Products

| ID | Product | Audience | Output | Reward |
| --- | --- | --- | --- | --- |
| productization | Harness improvements | operators | shipped behavior | accepted improvement |

## Work Lanes

| Lane | Default Weight | Purpose |
| --- | ---: | --- |
| productization | 20 | Ship improvements |
""",
        encoding="utf-8",
    )
    (farplane / "goals.md").write_text(
        """---
updated_at: 2026-07-03
---

# Goals

## Goals

```yaml
goals:
  validated_self_improvement:
    smart_goals:
      - id: improvement_q3
        kpis:
          - id: accepted_harness_improvements
            target: 20
            direction: above
```
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
project:
  id: test_project
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: productization
    pinned: true
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
    refresh: Call count_ticket_kpi_rewards for accepted_harness_improvements.
""",
        encoding="utf-8",
    )
    daily = root / ".farplane" / "metrics" / "daily"
    daily.mkdir(parents=True)
    (daily / "2026-07-02.json").write_text(
        json.dumps(
            {
                "date": "2026-07-02",
                "primitives": {
                    "ticket_count_by_kpi": {
                        "accepted_harness_improvements": {"value": 1, "status": "available", "payload": {}}
                    },
                },
                "source_gaps": [],
            }
        ),
        encoding="utf-8",
    )
    (daily / "2026-07-03.json").write_text(
        json.dumps(
            {
                "date": "2026-07-03",
                "primitives": {
                    "ticket_count_by_product": {
                        "productization": {"value": 2, "status": "available", "payload": {"kpi_ids": ["accepted_harness_improvements"]}}
                    },
                    "ticket_count_by_kpi": {
                        "accepted_harness_improvements": {"value": 2, "status": "available", "payload": {}}
                    },
                },
                "source_gaps": [],
            }
        ),
        encoding="utf-8",
    )


class FarplaneProjectSnapshotTests(unittest.TestCase):
    def test_snapshot_joins_goals_products_metrics_and_primitives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)

            snapshot = load_project_snapshot(root, "2026-07-03")

        self.assertEqual(snapshot["project"]["id"], "test_project")
        metric = snapshot["metrics"]["definitions"]["accepted_harness_improvements"]
        self.assertEqual(metric["primitive_id"], "ticket_count_by_kpi")
        self.assertIn("command", snapshot["metrics"]["primitives"]["ticket_count_by_kpi"])
        self.assertIn("ticket_count_by_kpi", snapshot["metrics"]["readings"])
        metric_card = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}["accepted_harness_improvements"]
        self.assertEqual(metric_card["current"], 2)
        self.assertEqual(metric_card["series"][-1]["daily_diff"], 1)
        self.assertEqual(metric_card["series"][-1]["cumulative"], 3)
        self.assertEqual(snapshot["tabs"]["overview"]["pinned_metric_cards"][0]["metric_id"], "accepted_harness_improvements")
        self.assertIn("ticket_ref", snapshot["shared_shapes"])
        self.assertEqual(snapshot["tabs"]["products"]["products"][0]["ticket_count"], 2)
        self.assertEqual(snapshot["tabs"]["goals"]["axes"][0]["smart_goals"][0]["kpis"][0]["latest_status"], "available")
        self.assertEqual(snapshot["tabs"]["goals"]["axes"][0]["smart_goals"][0]["kpis"][0]["current"], 2)
        self.assertIn("source_gap_ids", snapshot["tabs"]["distribution"])
        self.assertIn("missing_content_ledger", snapshot["tabs"]["distribution"]["source_gap_ids"])
        self.assertIn("source_gap_ids", snapshot["tabs"]["kanban"])

    def test_snapshot_builds_content_metric_cards_from_daily_readings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                bindings.read_text(encoding="utf-8")
                + """
  x_views:
    label: X views
    product: distribution
    unit: views
    display: bar_plus_cumulative
    kind: daily_count
    refresh: x-account writes a daily metric reading.
""",
                encoding="utf-8",
            )
            ledger = root / ".farplane" / "content" / "ledger.jsonl"
            ledger.parent.mkdir(parents=True)
            ledger.write_text(
                json.dumps(
                    {
                        "content_id": "x:1",
                        "platform": "x",
                        "external_id": "1",
                        "campaign": "launch",
                        "status": "posted",
                        "published_at": "2026-07-03T09:00:00Z",
                        "kpis": ["x_views"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            daily = root / ".farplane" / "metrics" / "daily"
            (daily / "2026-07-03.json").write_text(
                json.dumps(
                    {
                        "date": "2026-07-03",
                        "metrics": {
                            "x_views": {
                                "value": 9,
                                "status": "available",
                                "payload": {
                                    "items": [
                                        {
                                            "content_id": "x:1",
                                            "platform": "x",
                                            "external_id": "1",
                                            "value": 9,
                                        }
                                    ]
                                },
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        metric_card = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}["x_views"]
        content_card = snapshot["tabs"]["distribution"]["content_metric_cards"][0]
        self.assertEqual(metric_card["current"], 9)
        self.assertEqual(content_card["content_id"], "x:1")
        self.assertEqual(content_card["metrics"][0]["metric_id"], "x_views")
        self.assertEqual(content_card["metrics"][0]["current"], 9)

    def test_write_project_ui_snapshot_creates_parent_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / ".farplane" / "project" / "ui" / "latest.json"
            write_project_ui_snapshot({"schema_version": 1}, output)

            written = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(written["schema_version"], 1)


if __name__ == "__main__":
    unittest.main()
