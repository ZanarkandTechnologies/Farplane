from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_project_snapshot import (
    collect_ticket_refs,
    load_project_snapshot,
    write_project_ui_snapshot,
)


def add_metric(root: Path, metric_id: str, definition: dict, refresh: str) -> None:
    metrics_path = root / "farplane" / "metrics.yaml"
    metrics_payload = yaml.safe_load(metrics_path.read_text(encoding="utf-8"))
    metrics_payload["metrics"][metric_id] = definition
    metrics_path.write_text(yaml.safe_dump(metrics_payload, sort_keys=False), encoding="utf-8")

    bindings_path = root / "farplane" / "bindings.yaml"
    bindings_payload = yaml.safe_load(bindings_path.read_text(encoding="utf-8"))
    bindings_payload["metric_bindings"][metric_id] = {"refresh": refresh}
    bindings_path.write_text(yaml.safe_dump(bindings_payload, sort_keys=False), encoding="utf-8")


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
    (farplane / "harness.yaml").write_text(
        """kind: project-harness
framework_template_version: "0.4.0"
identity:
  mission: Make useful work.
  human_thesis: Preserve intent.
  north_star: Make reliable work normal.
metric_refs:
  objectives:
    - metric_id: accepted_harness_improvements
      priority: 1
  guards: []
products: {}
feature_definition: {}
operating_principles: [Prefer visible artifacts.]
stable_capabilities: []
leverage_commitments: []
constraints: {non_tradeoffs: []}
authority: {agents_may: [], human_approval_required: []}
change_rule: Protected changes require approval.
""",
        encoding="utf-8",
    )
    (farplane / "metrics.yaml").write_text(
        """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted harness improvements.
    pinned: true
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
    direction: maximize
    max_age_days: 7
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project:
  id: test_project
metric_bindings:
  accepted_harness_improvements:
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
                        "accepted_harness_improvements": {
                            "value": 1,
                            "status": "available",
                            "payload": {"reward_contract": "terminal_evidence_v1"},
                        }
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
                    "ticket_count_by_kpi": {
                        "accepted_harness_improvements": {
                            "value": 2,
                            "status": "available",
                            "payload": {"reward_contract": "terminal_evidence_v1"},
                        }
                    },
                },
                "source_gaps": [],
            }
        ),
        encoding="utf-8",
    )


class FarplaneProjectSnapshotTests(unittest.TestCase):
    def test_ticket_reward_projection_uses_canonical_reward_identity_and_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "tickets" / "TASK-0001" / "ticket.md"
            ticket.parent.mkdir(parents=True)
            ticket.write_text(
                """---
ticket_id: TASK-0001
title: Reward projection
status: done
phase: complete
---

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-7d
    kpi_id: accepted_harness_improvements
    expected_reward: one accepted improvement
    check_in_at: 2026-07-12T00:00:00Z
    actual_result: improvement retained
    decision: accept
    evaluated_at: 2026-07-12T01:00:00Z
    evaluation_key: eval-accepted-7d
    evidence_refs: [artifacts/proof.md]
  - kpi_id: legacy_missing_identity
```
""",
                encoding="utf-8",
            )

            refs, rewards = collect_ticket_refs(root)

        self.assertEqual(refs[0]["kpi_rewards"], ["accepted_harness_improvements"])
        self.assertEqual(refs[0]["reward_rows"][0]["reward_id"], "accepted-7d")
        self.assertEqual(rewards[0]["decision"], "accept")
        self.assertEqual(rewards[0]["ticket_status"], "done")
        self.assertEqual(rewards[0]["ticket_phase"], "complete")

    def test_snapshot_joins_objectives_metrics_and_primitives_without_products(self) -> None:
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
        self.assertEqual(metric_def["source_ref"]["path"], "farplane/metrics.yaml")
        self.assertEqual(metric_def["binding_source_ref"]["path"], "farplane/bindings.yaml")
        self.assertIn("farplane/metrics.yaml", {source["path"] for source in snapshot["sources"]})
        self.assertEqual(metric_def["tooltip"], metric_def["description"])
        self.assertEqual(metric_def["selection_role"], "objective")
        self.assertEqual(metric_def["target_spec"], {"value": None, "direction": "above", "unit": "improvements"})
        self.assertEqual(metric_card["description"], metric_def["description"])
        self.assertEqual(metric_card["target_spec"], metric_def["target_spec"])
        self.assertEqual(metric_card["current"], 2)
        self.assertEqual(metric_card["series"][-1]["daily_diff"], 1)
        self.assertEqual(metric_card["series"][-1]["cumulative"], 3)
        self.assertEqual(snapshot["tabs"]["overview"]["pinned_metric_cards"][0]["metric_id"], "accepted_harness_improvements")
        self.assertEqual(snapshot["tabs"]["overview"]["charter"]["mission"], "Make useful work.")
        self.assertEqual(snapshot["tabs"]["overview"]["charter"]["north_star"], "Make reliable work normal.")
        self.assertEqual(snapshot["metrics"]["selection"]["objectives"][0]["scope"], "project")
        self.assertIn("ticket_ref", snapshot["shared_shapes"])
        self.assertNotIn("products", snapshot["tabs"])
        self.assertNotIn("goals", snapshot["tabs"])
        self.assertEqual(snapshot["tabs"]["objectives"]["metric_cards"][0]["current"], 2)
        self.assertIn("source_gap_ids", snapshot["tabs"]["distribution"])
        self.assertNotIn("feed_scout", snapshot["tabs"]["distribution"])
        self.assertIn("missing_content_ledger", snapshot["tabs"]["distribution"]["source_gap_ids"])
        self.assertIn("news", snapshot["tabs"])
        self.assertFalse(snapshot["tabs"]["news"]["feed_scout"]["enabled"])
        self.assertEqual(snapshot["tabs"]["news"]["items"], [])
        self.assertIn("source_gap_ids", snapshot["tabs"]["kanban"])

    def test_snapshot_ignores_intent_era_reward_observations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            add_metric(
                root,
                "accepted_evidence_cycles",
                {
                    "label": "Accepted evidence cycles",
                    "kind": "daily_count",
                    "unit": "cycles",
                    "display": "bar_plus_cumulative",
                    "direction": "maximize",
                    "max_age_days": 7,
                },
                "Call count_ticket_kpi_rewards for accepted_evidence_cycles.",
            )
            legacy_root = root / ".farplane" / "metrics" / "observations" / "ticket_reward_feedback"
            legacy_root.mkdir(parents=True)
            (legacy_root / "2026-07-01.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "source_id": "ticket_reward_feedback",
                        "date": "2026-07-01",
                        "status": "available",
                        "observations": [
                            {
                                "metric_id": "accepted_evidence_cycles",
                                "date": "2026-07-01",
                                "value": 2,
                                "status": "available",
                                "payload": {"items": [{"expected_reward": "declared intent"}]},
                            },
                            {
                                "metric_id": "accepted_harness_improvements",
                                "date": "2026-07-01",
                                "value": 30,
                                "status": "available",
                                "payload": {"items": [{"expected_reward": "declared intent"}]},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        metric = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}[
            "accepted_harness_improvements"
        ]
        self.assertEqual(metric["current"], 2)
        self.assertEqual(metric["series"][-1]["cumulative"], 3)
        self.assertNotIn(30, [point["value"] for point in metric["series"]])
        evidence_cycles = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}[
            "accepted_evidence_cycles"
        ]
        self.assertEqual(evidence_cycles["current"], 0)
        self.assertNotIn(2, [point["value"] for point in evidence_cycles["series"]])

    def test_snapshot_does_not_fall_back_to_legacy_bindings_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            (root / "farplane" / "metrics.yaml").unlink()
            bindings_path = root / "farplane" / "bindings.yaml"
            bindings = yaml.safe_load(bindings_path.read_text(encoding="utf-8"))
            bindings["metrics"] = {
                "legacy_metric": {
                    "label": "Legacy metric",
                    "kind": "point",
                    "unit": "score",
                    "display": "reading",
                }
            }
            bindings_path.write_text(yaml.safe_dump(bindings, sort_keys=False), encoding="utf-8")

            snapshot = load_project_snapshot(root, "2026-07-03")

        self.assertEqual(snapshot["metrics"]["definitions"], {})
        metric_gap = next(gap for gap in snapshot["source_gaps"] if "metrics.yaml#metrics" in gap["id"])
        self.assertEqual(metric_gap["source_ref"]["path"], "farplane/metrics.yaml")

    def test_snapshot_reports_missing_metric_binding_from_bindings_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            bindings_path = root / "farplane" / "bindings.yaml"
            bindings = yaml.safe_load(bindings_path.read_text(encoding="utf-8"))
            bindings["metric_bindings"] = {}
            bindings_path.write_text(yaml.safe_dump(bindings, sort_keys=False), encoding="utf-8")

            snapshot = load_project_snapshot(root, "2026-07-03")

        metric_gap = next(gap for gap in snapshot["source_gaps"] if "metric_bindings" in gap["id"])
        self.assertEqual(metric_gap["source_ref"]["path"], "farplane/bindings.yaml")

    def test_snapshot_builds_content_metric_cards_from_daily_readings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            add_metric(
                root,
                "x_views",
                {
                    "label": "X views",
                    "description": "Daily X views.",
                    "unit": "views",
                    "display": "bar_plus_cumulative",
                    "kind": "daily_count",
                },
                "x-account writes a daily metric reading.",
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
        objective_card = snapshot["tabs"]["objectives"]["metric_cards"][0]
        self.assertEqual(objective_card["status"], "available")
        self.assertEqual(objective_card["current"], 0)

    def test_interval_provider_observations_back_goal_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            provider_refresh = 'Call $interval-update.calculate_ticket_intervention_metrics(ticket_dir="tickets", runtime_dir=".farplane", date="<YYYY-MM-DD>").'
            add_metric(root, "auto_time_ratio", {"label": "Autonomous time ratio", "description": "Autonomous time ratio.", "kind": "point", "unit": "ratio", "display": "reading"}, 'Call $interval-update.calculate_autonomy_time_ratio(runtime_dir=".farplane", date="<YYYY-MM-DD>").')
            add_metric(root, "ticket_intervention_turn_count", {"label": "Ticket intervention turns", "description": "Ticket intervention turns.", "kind": "daily_count", "unit": "turns", "display": "bar_plus_cumulative"}, provider_refresh)
            add_metric(root, "intervention_free_ticket_count", {"label": "Intervention-free tickets", "description": "Intervention-free tickets.", "kind": "daily_count", "unit": "tickets", "display": "bar_plus_cumulative"}, provider_refresh)
            add_metric(root, "auto_completion_rate", {"label": "Auto completion rate", "description": "Auto completion rate.", "kind": "point", "unit": "ratio", "display": "reading"}, provider_refresh)
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
            add_metric(
                root,
                "external_metric",
                {"label": "External metric", "description": "External metric.", "kind": "point", "unit": "score", "display": "reading"},
                "External owner writes this later.",
            )

            snapshot = load_project_snapshot(root, "2026-07-03")

        gaps = [gap["message"] for gap in snapshot["source_gaps"]]
        self.assertNotIn("no available observation for metric", gaps)
        metric_card = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}["external_metric"]
        self.assertEqual(metric_card["status"], "missing")
        self.assertEqual(metric_card["source_gaps"], [])

    def test_snapshot_discovers_nested_active_and_archived_ticket_proof(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            active_report = root / "tickets" / "TASK-0001" / "artifacts" / "qa" / "run-1" / "report.md"
            active_report.parent.mkdir(parents=True)
            active_report.write_text("# QA report\n", encoding="utf-8")
            archived_receipt = root / "tickets" / "archive" / "TASK-0002" / "artifacts" / "review" / "completion.json"
            archived_receipt.parent.mkdir(parents=True)
            archived_receipt.write_text("{}\n", encoding="utf-8")

            snapshot = load_project_snapshot(root, "2026-07-03")

        proof_paths = {item["path"] for item in snapshot["tabs"]["proof"]["qa_artifacts"]}
        self.assertEqual(
            proof_paths,
            {
                "tickets/TASK-0001/artifacts/qa/run-1/report.md",
                "tickets/archive/TASK-0002/artifacts/review/completion.json",
            },
        )
        self.assertNotIn("missing_qa_artifacts", snapshot["tabs"]["proof"]["source_gap_ids"])

    def test_unpinned_metric_source_gap_stays_on_metric_card_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            add_metric(
                root,
                "instagram_retention_score",
                {"label": "Instagram retention score", "description": "Instagram retention score.", "kind": "point", "unit": "ratio", "display": "reading"},
                "Instagram account writes this when duration is available.",
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

    def test_selected_metric_becomes_stale_after_max_age(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            metrics_path = root / "farplane" / "metrics.yaml"
            metrics = yaml.safe_load(metrics_path.read_text(encoding="utf-8"))
            metrics["metrics"]["accepted_harness_improvements"]["max_age_days"] = 2
            metrics_path.write_text(yaml.safe_dump(metrics, sort_keys=False), encoding="utf-8")

            snapshot = load_project_snapshot(root, "2026-07-10")

        card = snapshot["tabs"]["objectives"]["metric_cards"][0]
        self.assertEqual(card["status"], "stale")
        self.assertIsNone(card["current"])
        self.assertIn("max_age_days=2", card["source_gaps"][-1]["reason"])


if __name__ == "__main__":
    unittest.main()
