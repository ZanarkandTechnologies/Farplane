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
    (farplane / "goals.yaml").write_text(
        """
kind: project-goals
updated_at: 2026-07-03
goals:
  validated_self_improvement:
    smart_goals:
      - id: improvement_q3
        kpis:
          - id: accepted_harness_improvements
            target: 20
            direction: above
current_bets:
  - id: framework_standardization
    horizon: 1 week
    output: clear tracked config split
    proof_signal: validators pass
    owner: harness-creator
current_milestone: Make strategy visible in the project snapshot.
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
        metric_def = snapshot["metrics"]["definitions"]["accepted_harness_improvements"]
        self.assertIn("description", metric_def)
        self.assertEqual(metric_def["tooltip"], metric_def["description"])
        self.assertEqual(metric_def["target_spec"], {"value": 20.0, "direction": "above", "unit": "improvements"})
        self.assertEqual(metric_card["description"], metric_def["description"])
        self.assertEqual(metric_card["target_spec"], metric_def["target_spec"])
        self.assertEqual(metric_card["current"], 2)
        self.assertEqual(metric_card["series"][-1]["daily_diff"], 1)
        self.assertEqual(metric_card["series"][-1]["cumulative"], 3)
        self.assertEqual(snapshot["tabs"]["overview"]["pinned_metric_cards"][0]["metric_id"], "accepted_harness_improvements")
        self.assertEqual(
            snapshot["tabs"]["overview"]["team_focus"]["current_bet"],
            "framework_standardization: clear tracked config split",
        )
        self.assertEqual(snapshot["tabs"]["overview"]["team_focus"]["active_milestone"], "Make strategy visible in the project snapshot.")
        self.assertEqual(snapshot["tabs"]["overview"]["team_focus"]["top_goal_id"], "validated_self_improvement")
        self.assertIn("ticket_ref", snapshot["shared_shapes"])
        self.assertEqual(snapshot["tabs"]["products"]["products"][0]["ticket_count"], 2)
        goal_kpi = snapshot["tabs"]["goals"]["axes"][0]["smart_goals"][0]["kpis"][0]
        self.assertEqual(goal_kpi["latest_status"], "available")
        self.assertEqual(goal_kpi["status"], "available")
        self.assertEqual(goal_kpi["current"], 2)
        self.assertEqual(goal_kpi["value"], 2)
        self.assertEqual(goal_kpi["trend"][-1]["value"], 2)
        self.assertEqual(goal_kpi["description"], metric_def["description"])
        self.assertEqual(goal_kpi["target_spec"], metric_def["target_spec"])
        self.assertIn("source_gap_ids", snapshot["tabs"]["distribution"])
        self.assertNotIn("feed_scout", snapshot["tabs"]["distribution"])
        self.assertIn("missing_content_ledger", snapshot["tabs"]["distribution"]["source_gap_ids"])
        self.assertIn("news", snapshot["tabs"])
        self.assertFalse(snapshot["tabs"]["news"]["feed_scout"]["enabled"])
        self.assertEqual(snapshot["tabs"]["news"]["items"], [])
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

    def test_snapshot_joins_feed_scout_daily_feed_into_news_tab(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                bindings.read_text(encoding="utf-8")
                + """
feed_scout:
  enabled: true
  cadence: daily
  timezone: UTC
  daily_feed_root: .farplane/feed-scout/daily
  ledger: .farplane/feed-scout/ledger.jsonl
  proposal_ledger: .farplane/feed-scout/proposals.jsonl
  latest_report: .farplane/reports/feed-scout/latest.json
  ui:
    latest_feed: .farplane/feed-scout/daily/latest.json
""",
                encoding="utf-8",
            )
            feed_path = root / ".farplane" / "feed-scout" / "daily" / "latest.json"
            feed_path.parent.mkdir(parents=True)
            feed_path.write_text(
                json.dumps(
                    {
                        "date": "2026-07-03",
                        "generated_at": "2026-07-03T00:00:00Z",
                        "summary": {"item_count": 1, "changed_item_count": 1},
                        "groups": {
                            "paperclip": {
                                "name": "Paperclip",
                                "item_count": 1,
                            }
                        },
                        "items": [
                            {
                                "title": "Paperclip moved today",
                                "summary": "Stars and forks changed.",
                                "canonical_url": "https://github.com/paperclipai/paperclip",
                                "platform": "github",
                                "rank": 1,
                                "signal": "medium",
                            }
                        ],
                        "source_gaps": [],
                    }
                ),
                encoding="utf-8",
            )
            report_path = root / ".farplane" / "reports" / "feed-scout" / "latest.json"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(
                json.dumps(
                    {
                        "generated_at": "2026-07-03T00:01:00Z",
                        "report_path": ".farplane/reports/feed-scout/2026-07-03.md",
                        "daily_feed_path": ".farplane/feed-scout/daily/feed-2026-07-03.json",
                        "summary": {"item_count": 1},
                        "source_gaps": [],
                    }
                ),
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        news = snapshot["tabs"]["news"]
        self.assertEqual(news["summary"]["item_count"], 1)
        self.assertEqual(news["items"][0]["title"], "Paperclip moved today")
        self.assertEqual(news["groups"][0]["group_id"], "paperclip")
        self.assertEqual(news["latest_report"]["report_path"], ".farplane/reports/feed-scout/2026-07-03.md")
        self.assertTrue(news["feed_scout"]["enabled"])
        self.assertEqual(news["feed_scout"]["config"]["latest_feed"], ".farplane/feed-scout/daily/latest.json")
        self.assertEqual(news["source_gap_ids"], [])

    def test_enabled_feed_scout_reports_news_source_gaps_when_latest_files_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                bindings.read_text(encoding="utf-8")
                + """
feed_scout:
  enabled: true
  latest_report: .farplane/reports/feed-scout/latest.json
  ui:
    latest_feed: .farplane/feed-scout/daily/latest.json
""",
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        self.assertEqual(
            snapshot["tabs"]["news"]["source_gap_ids"],
            ["missing_feed_scout_latest_feed", "missing_feed_scout_latest_report"],
        )
        self.assertEqual(snapshot["tabs"]["news"]["items"], [])
        self.assertIn(
            "missing_feed_scout_latest_feed",
            [gap["id"] for gap in snapshot["source_gaps"]],
        )

    def test_ticket_count_kpis_zero_fill_when_primitive_has_no_matching_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            daily = root / ".farplane" / "metrics" / "daily"
            (daily / "2026-07-03.json").write_text(
                json.dumps(
                    {
                        "date": "2026-07-03",
                        "primitives": {
                            "ticket_count_by_kpi": {},
                        },
                        "source_gaps": [],
                    }
                ),
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        metric_card = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}["accepted_harness_improvements"]
        self.assertEqual(metric_card["status"], "available")
        self.assertEqual(metric_card["current"], 0)
        self.assertEqual(metric_card["source_gaps"], [])
        goal_kpi = snapshot["tabs"]["goals"]["axes"][0]["smart_goals"][0]["kpis"][0]
        self.assertEqual(goal_kpi["latest_status"], "available")
        self.assertEqual(goal_kpi["status"], "available")
        self.assertEqual(goal_kpi["current"], 0)
        self.assertEqual(goal_kpi["value"], 0)

    def test_interval_provider_observations_back_goal_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                bindings.read_text(encoding="utf-8")
                + """
  auto_time_ratio:
    label: Autonomous time ratio
    product: productization
    kind: point
    unit: ratio
    display: reading
    refresh: Call $interval-update.calculate_autonomy_time_ratio(runtime_dir=".farplane", date="<YYYY-MM-DD>").
  ticket_intervention_turn_count:
    label: Ticket intervention turns
    product: productization
    kind: daily_count
    unit: turns
    display: bar_plus_cumulative
    refresh: Call $interval-update.calculate_ticket_intervention_metrics(ticket_dir="tickets", runtime_dir=".farplane", date="<YYYY-MM-DD>").
  intervention_free_ticket_count:
    label: Intervention-free tickets
    product: productization
    kind: daily_count
    unit: tickets
    display: bar_plus_cumulative
    refresh: Call $interval-update.calculate_ticket_intervention_metrics(ticket_dir="tickets", runtime_dir=".farplane", date="<YYYY-MM-DD>").
  auto_completion_rate:
    label: Auto completion rate
    product: productization
    kind: point
    unit: ratio
    display: reading
    refresh: Call $interval-update.calculate_ticket_intervention_metrics(ticket_dir="tickets", runtime_dir=".farplane", date="<YYYY-MM-DD>").
""",
                encoding="utf-8",
            )
            observations = root / ".farplane" / "metrics" / "observations"
            (observations / "autonomy_time_feedback").mkdir(parents=True)
            (observations / "autonomy_time_feedback" / "2026-07-01.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "date": "2026-07-01",
                        "source_id": "autonomy_time_feedback",
                        "status": "available",
                        "observations": [
                            {
                                "metric_id": "auto_time_ratio",
                                "date": "2026-07-01",
                                "value": 0.2541,
                                "status": "available",
                                "payload": {},
                            }
                        ],
                        "gaps": [],
                        "payload": {},
                    }
                ),
                encoding="utf-8",
            )
            (observations / "ticket_intervention_feedback").mkdir(parents=True)
            (observations / "ticket_intervention_feedback" / "2026-07-01.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "date": "2026-07-01",
                        "source_id": "ticket_intervention_feedback",
                        "status": "available",
                        "observations": [
                            {"metric_id": "ticket_intervention_turn_count", "date": "2026-07-01", "value": 0, "status": "available"},
                            {"metric_id": "intervention_free_ticket_count", "date": "2026-07-01", "value": 8, "status": "available"},
                            {"metric_id": "auto_completion_rate", "date": "2026-07-01", "value": 1.0, "status": "available"},
                        ],
                        "gaps": [],
                        "payload": {},
                    }
                ),
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        definitions = snapshot["metrics"]["definitions"]
        self.assertEqual(definitions["auto_time_ratio"]["primitive_id"], "autonomy_time_feedback")
        self.assertEqual(definitions["ticket_intervention_turn_count"]["primitive_id"], "ticket_intervention_feedback")
        cards = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}
        self.assertEqual(cards["auto_time_ratio"]["status"], "available")
        self.assertEqual(cards["auto_time_ratio"]["current"], 0.2541)
        self.assertEqual(cards["ticket_intervention_turn_count"]["status"], "available")
        self.assertEqual(cards["ticket_intervention_turn_count"]["current"], 0)
        self.assertEqual(cards["intervention_free_ticket_count"]["current"], 8)
        self.assertEqual(cards["auto_completion_rate"]["current"], 1.0)

    def test_missing_observation_is_not_promoted_to_global_source_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                bindings.read_text(encoding="utf-8")
                + """
  external_metric:
    label: External metric
    product: experiments
    kind: point
    unit: score
    display: reading
    refresh: External owner writes this later.
""",
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        gaps = [gap["message"] for gap in snapshot["source_gaps"]]
        self.assertNotIn("no available observation for metric", gaps)
        metric_card = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}["external_metric"]
        self.assertEqual(metric_card["status"], "missing")
        self.assertEqual(metric_card["source_gaps"], [])

    def test_unpinned_metric_source_gap_stays_on_metric_card_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                bindings.read_text(encoding="utf-8")
                + """
  instagram_retention_score:
    label: Instagram retention score
    product: distribution
    kind: point
    unit: ratio
    display: reading
    refresh: Instagram account writes this when duration is available.
""",
                encoding="utf-8",
            )
            daily = root / ".farplane" / "metrics" / "daily"
            (daily / "2026-07-03.json").write_text(
                json.dumps(
                    {
                        "date": "2026-07-03",
                        "metrics": {
                            "instagram_retention_score": {
                                "value": None,
                                "status": "source_gap",
                                "payload": {"gaps": ["instagram_retention_score_requires_duration_seconds"]},
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        gap_ids = [gap["id"] for gap in snapshot["source_gaps"]]
        self.assertNotIn("metric_source_gap:instagram_retention_score", gap_ids)
        metric_card = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}["instagram_retention_score"]
        self.assertEqual(metric_card["status"], "source_gap")
        self.assertEqual(metric_card["source_gaps"][0]["reason"], "instagram_retention_score_requires_duration_seconds")

    def test_write_project_ui_snapshot_creates_parent_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / ".farplane" / "project" / "ui" / "latest.json"
            write_project_ui_snapshot({"schema_version": 1}, output)

            written = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(written["schema_version"], 1)


if __name__ == "__main__":
    unittest.main()
