from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_metrics import compile_metric_snapshots, generate_metric_snapshots


GOALS = """---
kind: project-goals
---

# Goals

## Goals

```yaml
goals:
  value_delivery:
    smart_goals:
      - id: fixture_goal
        target: Exercise metric recipes
        kpis:
          - x_followers
          - x_views
          - accepted_output_events
          - ready_unclaimed_ticket_count
```
"""


BINDINGS = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  x_followers:
    label: X followers
    product: distribution
    aggregation: point
    target: 100
    unit: followers
    display: reading
    observation:
      id: manual_x_account
      route: manual_snapshot
      writes: .farplane/metrics/manual/x_account.json
    update_prompt: Read compact manual X account snapshot.
  x_views:
    label: X views
    product: distribution
    aggregation: daily
    cumulative: true
    target: 10
    unit: views
    display: bar_plus_cumulative
    observation:
      id: manual_x_account
      route: manual_snapshot
      writes: .farplane/metrics/manual/x_account.json
    update_prompt: Read compact manual X account snapshot.
  accepted_output_events:
    label: Accepted output events
    product: productization
    aggregation: daily
    cumulative: true
    target: 2
    unit: events
    display: bar_plus_cumulative
    observation:
      id: pulse_reward_ledger
      route: local_jsonl
      path: .farplane/automation/rewards.jsonl
    update_prompt: Count accepted reward ledger rows with evidence.
  ready_unclaimed_ticket_count:
    label: Ready unclaimed tickets
    product: project_control
    aggregation: point
    target: 1
    unit: tickets
    display: reading
    observation:
      id: ticket_board
      route: local_files
      path: tickets/TASK-*/ticket.md
    update_prompt: Count ready unclaimed tickets.
```
"""

LEAN_GOALS = """---
kind: project-goals
---

# Goals

## Goals

```yaml
goals:
  distribution_from_evidence:
    question: Can Farplane turn evidence into audience?
    evidence_hints:
      - content views
    smart_goals:
      - id: evidence_distribution_q3
        target: 100000 evidence-backed views by 2026-09-30
        kpis:
          - x_views
          - x_likes
        interpretation: Use x-account snapshots and tracked content.

  project_control:
    question: Can Farplane control projects?
    evidence_hints:
      - ready ticket count
    smart_goals:
      - id: project_control_q3
        target: Keep ready tickets under 3 by 2026-09-30
        kpis:
          - ready_unclaimed_ticket_count
        interpretation: Use ticket board readings.
      - id: budget_accountability_weekly
        target: Active projects get weekly runway decisions
        kpis:
          - weekly_runway_review_count
          - projects_with_runway_decisions
        interpretation: Use weekly interval reports.
```
"""


LEAN_BINDINGS = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  x_views:
    label: X views
    product: distribution
    aggregation: daily
    cumulative: true
    unit: views
    display: bar_plus_cumulative
    observation:
      id: x_account_metrics
      route: skill_snapshot
      skill: x-account
      writes: .farplane/metrics/manual/x_account.json
    update_prompt: Read compact X account snapshot.
  x_likes:
    label: X likes
    product: distribution
    aggregation: daily
    cumulative: true
    unit: likes
    display: bar_plus_cumulative
    observation:
      id: x_account_metrics
      route: skill_snapshot
      skill: x-account
      writes: .farplane/metrics/manual/x_account.json
    update_prompt: Read compact X account snapshot.
  ready_unclaimed_ticket_count:
    label: Ready unclaimed tickets
    product: project_control
    aggregation: point
    unit: tickets
    display: reading
    observation:
      id: ticket_board
      route: local_files
      path: tickets/TASK-*/ticket.md
    update_prompt: Count ready unclaimed tickets.
  weekly_runway_review_count:
    label: Weekly runway reviews
    product: market_learning
    aggregation: daily
    cumulative: true
    unit: reviews
    display: bar_plus_cumulative
    observation:
      id: runway_review_notes
      route: interval_report
      path: .farplane/reports/interval/weekly_interval
    update_prompt: Count weekly interval reports with runway review sections.
  projects_with_runway_decisions:
    label: Projects with runway decisions
    product: market_learning
    aggregation: daily
    cumulative: true
    unit: projects
    display: bar_plus_cumulative
    observation:
      id: runway_review_notes
      route: interval_report
      path: .farplane/reports/interval/weekly_interval
    update_prompt: Count project decision rows in runway review tables.
```
"""

AUTONOMY_GOALS = """---
kind: project-goals
---

# Goals

## Goals

```yaml
goals:
  validated_self_improvement:
    question: Can Farplane run with less human thread attention?
    smart_goals:
      - id: autonomy_time
        target: More auto time than human time
        kpis:
          - human_prompt_count
          - human_active_thread_count
          - human_attention_minutes_estimated
          - autonomous_thread_count
          - autonomous_worker_elapsed_minutes
          - rewarded_autonomous_thread_count
          - auto_time_ratio
          - output_per_human_prompt
  distribution_from_evidence:
    question: Can Farplane show adoption?
    smart_goals:
      - id: github_adoption
        target: GitHub repo gets usage
        kpis:
          - github_stars
          - github_forks
          - github_open_issues
          - github_open_prs
          - github_merged_prs
          - github_views
          - github_unique_cloners
```
"""

AUTONOMY_BINDINGS = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  human_prompt_count:
    label: Human prompt count
    product: cross_product_autonomy
    aggregation: daily
    cumulative: true
    unit: prompts
    display: bar_plus_cumulative
    observation: &autonomy_source
      id: autonomy_time_feedback
      route: local_runtime
      paths:
        events: .farplane/events/*.jsonl
        spawned_threads: .farplane/automation/spawned-threads.jsonl
        rewards: .farplane/automation/rewards.jsonl
    update_prompt: Count human prompt events.
  human_active_thread_count:
    label: Human active thread count
    product: cross_product_autonomy
    aggregation: daily
    cumulative: true
    unit: threads
    display: bar_plus_cumulative
    observation: *autonomy_source
    update_prompt: Count human active threads.
  human_attention_minutes_estimated:
    label: Human attention minutes estimated
    product: cross_product_autonomy
    aggregation: daily
    cumulative: true
    unit: minutes
    display: bar_plus_cumulative
    observation: *autonomy_source
    update_prompt: Estimate human attention minutes.
  autonomous_thread_count:
    label: Autonomous thread count
    product: cross_product_autonomy
    aggregation: daily
    cumulative: true
    unit: threads
    display: bar_plus_cumulative
    observation: *autonomy_source
    update_prompt: Count spawned autonomous threads.
  autonomous_worker_elapsed_minutes:
    label: Autonomous worker elapsed minutes
    product: cross_product_autonomy
    aggregation: daily
    cumulative: true
    unit: minutes
    display: bar_plus_cumulative
    observation: *autonomy_source
    update_prompt: Estimate autonomous worker elapsed minutes.
  rewarded_autonomous_thread_count:
    label: Rewarded autonomous thread count
    product: cross_product_autonomy
    aggregation: daily
    cumulative: true
    unit: threads
    display: bar_plus_cumulative
    observation: *autonomy_source
    update_prompt: Count rewarded autonomous threads.
  auto_time_ratio:
    label: Autonomous time ratio
    product: cross_product_autonomy
    aggregation: point
    target: 1
    unit: ratio
    display: reading
    observation: *autonomy_source
    update_prompt: Compare autonomous time against human attention.
  output_per_human_prompt:
    label: Output per human prompt
    product: cross_product_autonomy
    aggregation: point
    unit: outputs_per_prompt
    display: reading
    observation: *autonomy_source
    update_prompt: Divide accepted outputs by human prompts.
  github_stars:
    label: GitHub stars
    product: distribution
    aggregation: point
    unit: stars
    display: reading
    observation: &github_source
      id: github_repo_feedback
      route: github_repo
      repo: ZanarkandTechnologies/Farplane
    update_prompt: Fetch repository metadata.
  github_forks:
    label: GitHub forks
    product: distribution
    aggregation: point
    unit: forks
    display: reading
    observation: *github_source
    update_prompt: Fetch repository metadata.
  github_open_issues:
    label: GitHub open issues
    product: productization
    aggregation: point
    unit: issues
    display: reading
    observation: *github_source
    update_prompt: Fetch open issue count.
  github_open_prs:
    label: GitHub open PRs
    product: productization
    aggregation: point
    unit: prs
    display: reading
    observation: *github_source
    update_prompt: Fetch open PR count.
  github_merged_prs:
    label: GitHub merged PRs
    product: productization
    aggregation: daily
    cumulative: true
    unit: prs
    display: bar_plus_cumulative
    observation: *github_source
    update_prompt: Count merged PRs.
  github_views:
    label: GitHub views
    product: distribution
    aggregation: daily
    cumulative: true
    unit: views
    display: bar_plus_cumulative
    observation: *github_source
    update_prompt: Fetch GitHub traffic views.
  github_unique_cloners:
    label: GitHub unique cloners
    product: distribution
    aggregation: daily
    cumulative: true
    unit: cloners
    display: bar_plus_cumulative
    observation: *github_source
    update_prompt: Fetch GitHub traffic clones.
```
"""

REWARD_GOALS = """---
kind: project-goals
---

# Goals

## Goals

```yaml
goals:
  validated_self_improvement:
    question: Can completed proof move KPIs?
    smart_goals:
      - id: reward_connector
        target: Count completed ticket rewards
        kpis:
          - accepted_harness_improvements
          - accepted_evidence_cycles
```
"""

REWARD_BINDINGS = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: productization
    aggregation: daily
    cumulative: true
    unit: improvements
    display: bar_plus_cumulative
    observation: &ticket_reward_source
      id: ticket_reward_feedback
      route: local_files
      path: tickets/TASK-*/ticket.md
    update_prompt: Count completed ticket rewards.
  accepted_evidence_cycles:
    label: Accepted evidence cycles
    product: experiments
    aggregation: daily
    cumulative: true
    unit: cycles
    display: bar_plus_cumulative
    observation: *ticket_reward_source
    update_prompt: Count completed ticket rewards.
  auto_time_ratio:
    label: Autonomous time ratio
    product: cross_product_autonomy
    aggregation: point
    unit: ratio
    display: reading
    observation:
      id: autonomy_time_feedback
      route: local_runtime
      paths:
        events: .farplane/events/*.jsonl
        spawned_threads: .farplane/automation/spawned-threads.jsonl
        rewards: .farplane/automation/rewards.jsonl
    update_prompt: Read autonomy ledgers, not ticket reward attribution.
```
"""

RECIPE_GOALS = """---
kind: project-goals
---

# Goals

## Goals

```yaml
goals:
  validated_self_improvement:
    smart_goals:
      - id: recipe_goal
        target: Count accepted proof
        kpis:
          - accepted_harness_improvements
          - auto_completion_rate
```
"""

RECIPE_BINDINGS = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
project:
  id: farplane
  name: Farplane

metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: productization
    pinned: true
    aggregation: daily
    cumulative: true
    unit: improvements
    display: bar_plus_cumulative
    observation:
      id: ticket_reward_feedback
      route: local_files
      path: tickets/TASK-*/ticket.md
    update_prompt: Count proof-backed completed ticket rewards.
  auto_completion_rate:
    label: Auto completion rate
    product: productization
    aggregation: point
    unit: ratio
    display: reading
    observation:
      id: ticket_intervention_feedback
      route: local_runtime
      paths:
        associations: .farplane/state/ticket-thread-associations.jsonl
        events: .farplane/events/*.jsonl
    update_prompt: Count completed ticket threads with zero post-start human turns.
  intervention_free_ticket_count:
    label: Intervention-free tickets
    product: productization
    aggregation: daily
    cumulative: true
    unit: tickets
    display: bar_plus_cumulative
    observation:
      id: ticket_intervention_feedback
      route: local_runtime
      paths:
        associations: .farplane/state/ticket-thread-associations.jsonl
        events: .farplane/events/*.jsonl
    update_prompt: Count completed ticket threads with zero post-start human turns.
```
"""


class FarplaneMetricsTests(unittest.TestCase):
    def test_compile_metric_snapshots_reads_daily_metrics_without_fetching_sources(self) -> None:
        daily_bindings = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  x_views:
    label: X views
    product: distribution
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
    refresh: Use the x-account skill to write today's normalized reading.
```
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(daily_bindings, encoding="utf-8")
            daily_dir = root / ".farplane" / "metrics" / "daily"
            daily_dir.mkdir(parents=True)
            (daily_dir / "2026-06-30.json").write_text(
                json.dumps(
                    {
                        "date": "2026-06-30",
                        "metrics": {
                            "x_views": {"value": 4, "status": "available"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            (daily_dir / "2026-07-01.json").write_text(
                json.dumps(
                    {
                        "date": "2026-07-01",
                        "metrics": {
                            "x_views": {
                                "value": 9,
                                "status": "available",
                                "payload": {"posts": [{"id": "x:1", "value": 9}]},
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            with patch("farplane_metrics.fetch_source") as fetch_source:
                result = compile_metric_snapshots(root, "2026-07-01")
                fetch_source.assert_not_called()

            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(result.source_snapshot_paths, [])
        self.assertEqual(by_id["x_views"]["source_id"], "x_views")
        self.assertEqual(by_id["x_views"]["current"], 9)
        self.assertEqual(by_id["x_views"]["series"][-1]["daily_diff"], 5)
        self.assertEqual(by_id["x_views"]["series"][-1]["cumulative"], 13)
        self.assertEqual(by_id["x_views"]["best_daily"], 9)
        self.assertEqual(by_id["x_views"]["series"][-1]["payload"]["posts"][0]["id"], "x:1")

    def test_daily_metric_source_gap_is_not_counted_as_zero(self) -> None:
        daily_bindings = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  x_views:
    label: X views
    product: distribution
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
    refresh: Use the x-account skill to write today's normalized reading.
```
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(daily_bindings, encoding="utf-8")
            daily_dir = root / ".farplane" / "metrics" / "daily"
            daily_dir.mkdir(parents=True)
            (daily_dir / "2026-07-01.json").write_text(
                json.dumps(
                    {
                        "date": "2026-07-01",
                        "metrics": {
                            "x_views": {
                                "value": None,
                                "status": "source_gap",
                                "payload": {"reason": "missing X API token"},
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = compile_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertIsNone(by_id["x_views"]["current"])
        self.assertEqual(by_id["x_views"]["series"], [])
        self.assertEqual(by_id["x_views"]["status"], "source_gap")
        self.assertEqual(by_id["x_views"]["source_gaps"][0]["payload"]["reason"], "missing X API token")

    def test_compile_reads_kpi_targets_from_goals(self) -> None:
        target_goals = """---
kind: project-goals
---

# Goals

## Goals

```yaml
goals:
  project_control:
    smart_goals:
      - id: control_goal
        target: Keep ready tickets under 3
        kpis:
          - id: ready_unclaimed_ticket_count
            target: 3
            direction: below
          - id: accepted_harness_improvements
            target: 2
            direction: above
```
"""
        target_bindings = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  ready_unclaimed_ticket_count:
    label: Ready unclaimed tickets
    product: project_control
    kind: point
    unit: tickets
    display: reading
    refresh: Count ready tickets.
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: productization
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
    refresh: Count ticket rewards.
```
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(target_goals, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(target_bindings, encoding="utf-8")
            daily_dir = root / ".farplane" / "metrics" / "daily"
            daily_dir.mkdir(parents=True)
            (daily_dir / "2026-07-01.json").write_text(
                json.dumps(
                    {
                        "date": "2026-07-01",
                        "metrics": {
                            "ready_unclaimed_ticket_count": {"value": 2, "status": "available"},
                            "accepted_harness_improvements": {"value": 2, "status": "available"},
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = compile_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["ready_unclaimed_ticket_count"]["target"], 3)
        self.assertEqual(by_id["ready_unclaimed_ticket_count"]["target_direction"], "below")
        self.assertEqual(by_id["ready_unclaimed_ticket_count"]["target_hit"]["hit_value"], 2)
        self.assertEqual(by_id["accepted_harness_improvements"]["target"], 2)
        self.assertEqual(by_id["accepted_harness_improvements"]["target_direction"], "above")
        self.assertEqual(by_id["accepted_harness_improvements"]["target_hit"]["hit_value"], 2)

    def test_generates_point_daily_cumulative_and_target_hits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(BINDINGS, encoding="utf-8")
            (root / ".farplane" / "automation").mkdir(parents=True)
            (root / ".farplane" / "automation" / "rewards.jsonl").write_text(
                json.dumps(
                    {
                        "ts": "2026-06-29T23:00:00Z",
                        "outcome": "positive",
                        "evidence": ["tickets/TASK-0000/artifacts/proof.md"],
                    }
                )
                + "\n"
                + json.dumps(
                    {
                        "ts": "2026-06-30T01:00:00Z",
                        "outcome": "positive",
                        "evidence": ["tickets/TASK-0001/artifacts/proof.md"],
                    }
                )
                + "\n"
                + json.dumps(
                    {
                        "ts": "2026-06-30T02:00:00Z",
                        "outcome": "partial_positive",
                        "evidence": ["skills/example/SKILL.md"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (root / ".farplane" / "metrics" / "manual").mkdir(parents=True)
            (root / ".farplane" / "metrics" / "manual" / "x_account.json").write_text(
                json.dumps(
                    {
                        "observations": [
                            {"metric_id": "x_followers", "date": "2026-06-30", "value": 101, "status": "available"},
                            {"metric_id": "x_views", "date": "2026-06-30", "value": 4, "status": "available"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
title: Test
phase: building
status: todo
owner: codex
claimed_by:
ready: true
approval_required: false
updated_at: 2026-06-30T00:00:00Z
next_action: execute
---
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-06-30")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["x_followers"]["current"], 101)
        self.assertEqual(by_id["x_followers"]["target_hit"]["hit_at"], "2026-06-30")
        self.assertEqual(by_id["x_views"]["series"][0]["cumulative"], 4)
        self.assertEqual(by_id["accepted_output_events"]["current"], 3)
        self.assertEqual(by_id["accepted_output_events"]["target_hit"]["hit_value"], 3)
        self.assertEqual(by_id["ready_unclaimed_ticket_count"]["current"], 1)

    def test_missing_manual_source_is_source_gap_not_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(BINDINGS.replace("true | manual", "false | manual"), encoding="utf-8")
            (root / ".farplane" / "automation").mkdir(parents=True)
            (root / ".farplane" / "automation" / "rewards.jsonl").write_text("", encoding="utf-8")
            (root / "tickets").mkdir()

            result = generate_metric_snapshots(root, "2026-06-30")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["x_followers"]["status"], "source_gap")
        self.assertIsNone(by_id["x_followers"]["current"])
        self.assertIn("x_followers", {gap["metric_id"] for gap in payload["source_gaps"]})

    def test_reads_lean_goals_bindings_and_compact_metric_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(LEAN_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(LEAN_BINDINGS, encoding="utf-8")
            (root / ".farplane" / "metrics" / "manual").mkdir(parents=True)
            (root / ".farplane" / "metrics" / "manual" / "x_account.json").write_text(
                json.dumps(
                    {
                        "source": "x_account_metrics",
                        "date": "2026-07-01",
                        "status": "available",
                        "metrics": {
                            "x_views": {
                                "value": 206,
                                "items": [
                                    {
                                        "id": "x:2063623337851691167",
                                        "value": 206,
                                        "kind": "post",
                                    }
                                ],
                            },
                            "x_likes": {"value": 0},
                        },
                    }
                ),
                encoding="utf-8",
            )
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
title: Test
phase: building
status: todo
owner: codex
claimed_by:
ready: true
approval_required: false
updated_at: 2026-07-01T00:00:00Z
next_action: execute
---
""",
                encoding="utf-8",
            )

            generate_metric_snapshots(root, "2026-06-30")
            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["x_views"]["source_id"], "x_account_metrics")
        self.assertEqual(by_id["x_views"]["current"], 206)
        self.assertIsNone(by_id["x_views"]["series"][0]["daily_diff"])
        self.assertEqual(by_id["x_views"]["series"][-1]["daily_diff"], 0)
        self.assertEqual(by_id["x_views"]["series"][-1]["items"][0]["id"], "x:2063623337851691167")
        self.assertEqual(by_id["ready_unclaimed_ticket_count"]["current"], 1)
        self.assertEqual(by_id["weekly_runway_review_count"]["status"], "source_gap")

    def test_reads_budget_runway_review_from_weekly_interval_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(LEAN_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(LEAN_BINDINGS, encoding="utf-8")
            (root / ".farplane" / "metrics" / "manual").mkdir(parents=True)
            (root / ".farplane" / "metrics" / "manual" / "x_account.json").write_text(
                json.dumps({"status": "source_gap", "gaps": ["not_configured"]}),
                encoding="utf-8",
            )
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
title: Test
phase: building
status: todo
owner: codex
claimed_by:
ready: false
approval_required: false
updated_at: 2026-07-01T00:00:00Z
next_action: wait
---
""",
                encoding="utf-8",
            )
            report_dir = root / ".farplane" / "reports" / "interval" / "weekly_interval"
            report_dir.mkdir(parents=True)
            (report_dir / "2026-07-01T000000Z.md").write_text(
                """# Weekly

## Budget / Runway Review

| Active project | Contribution mode | Spend / attention used | Expected reward | Observed evidence | Decision | Next constraint |
| --- | --- | --- | --- | --- | --- | --- |
| Evidence loop | distribution | rough: one ticket | views | metric snapshot | continue | ship two posts |
| Adoption loop | learning | rough: one ticket | provider | source gap | instrument | add ledger |

## Next Window Plan
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["weekly_runway_review_count"]["current"], 1)
        self.assertEqual(by_id["projects_with_runway_decisions"]["current"], 2)

    def test_reads_autonomy_time_feedback_from_local_ledgers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(AUTONOMY_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(AUTONOMY_BINDINGS, encoding="utf-8")
            event_dir = root / ".farplane" / "events"
            event_dir.mkdir(parents=True)
            (event_dir / "codex.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"timestamp": "2026-07-01T10:00:00Z", "event_type": "turn_start", "session_id": "human-1"}),
                        json.dumps({"timestamp": "2026-07-01T10:20:00Z", "event_type": "turn_start", "session_id": "human-1"}),
                        json.dumps({"timestamp": "2026-07-01T12:00:00Z", "event_type": "turn_start", "session_id": "human-2"}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            automation_dir = root / ".farplane" / "automation"
            automation_dir.mkdir(parents=True)
            (automation_dir / "spawned-threads.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"timestamp": "2026-07-01T09:00:00Z", "status": "spawned", "thread_id": "auto-1"}),
                        json.dumps({"timestamp": "2026-07-01T09:45:00Z", "status": "rewarded_positive", "thread_id": "auto-1"}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (automation_dir / "rewards.jsonl").write_text(
                json.dumps(
                    {
                        "timestamp": "2026-07-01T09:45:00Z",
                        "outcome": "positive",
                        "evidence": ["tickets/TASK-0001/artifacts/proof.md"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["human_prompt_count"]["current"], 3)
        self.assertEqual(by_id["human_active_thread_count"]["current"], 2)
        self.assertEqual(by_id["human_attention_minutes_estimated"]["current"], 30)
        self.assertEqual(by_id["autonomous_thread_count"]["current"], 1)
        self.assertEqual(by_id["autonomous_worker_elapsed_minutes"]["current"], 45)
        self.assertEqual(by_id["rewarded_autonomous_thread_count"]["current"], 1)
        self.assertEqual(by_id["auto_time_ratio"]["current"], 1.5)
        self.assertAlmostEqual(by_id["output_per_human_prompt"]["current"], 0.3333)
        self.assertEqual(by_id["human_prompt_count"]["series"][0]["cumulative"], 3)

    def test_reads_github_repo_feedback_with_daily_traffic_rows(self) -> None:
        responses = {
            "repos/ZanarkandTechnologies/Farplane": (
                {"stargazers_count": 7, "forks_count": 2, "open_issues_count": 4},
                None,
            ),
            "repos/ZanarkandTechnologies/Farplane/issues?state=open&per_page=100": (
                [{"id": 10}, {"id": 11, "pull_request": {}}],
                None,
            ),
            "repos/ZanarkandTechnologies/Farplane/pulls?state=open&per_page=100": ([{"id": 1}, {"id": 2}], None),
            "repos/ZanarkandTechnologies/Farplane/pulls?state=closed&per_page=100": (
                [
                    {"id": 3, "merged_at": "2026-06-30T00:00:00Z"},
                    {"id": 4, "merged_at": "2026-07-01T00:00:00Z"},
                    {"id": 5, "merged_at": None},
                ],
                None,
            ),
            "repos/ZanarkandTechnologies/Farplane/traffic/views": (
                {"count": 99, "views": [{"timestamp": "2026-07-01T00:00:00Z", "count": 11}]},
                None,
            ),
            "repos/ZanarkandTechnologies/Farplane/traffic/clones": (
                {"uniques": 44, "clones": [{"timestamp": "2026-07-01T00:00:00Z", "uniques": 5}]},
                None,
            ),
        }

        def fake_run_gh_api(endpoint: str):
            return responses[endpoint]

        with tempfile.TemporaryDirectory() as tmp, patch("farplane_metrics.run_gh_api", side_effect=fake_run_gh_api):
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(AUTONOMY_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(AUTONOMY_BINDINGS, encoding="utf-8")
            (root / ".farplane" / "events").mkdir(parents=True)
            (root / ".farplane" / "automation").mkdir(parents=True)
            (root / ".farplane" / "automation" / "spawned-threads.jsonl").write_text("", encoding="utf-8")
            (root / ".farplane" / "automation" / "rewards.jsonl").write_text("", encoding="utf-8")

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["github_stars"]["current"], 7)
        self.assertEqual(by_id["github_forks"]["current"], 2)
        self.assertEqual(by_id["github_open_issues"]["current"], 1)
        self.assertEqual(by_id["github_open_prs"]["current"], 2)
        self.assertEqual(by_id["github_merged_prs"]["current"], 1)
        self.assertEqual(by_id["github_views"]["current"], 11)
        self.assertEqual(by_id["github_views"]["series"][0]["cumulative"], 11)
        self.assertEqual(by_id["github_unique_cloners"]["current"], 5)

    def test_missing_placeholder_source_gaps_without_reading_project_root(self) -> None:
        placeholder_bindings = """---
kind: project-bindings
---

# Bindings

## Project Config

```yaml
metrics:
  TODO_metric_name:
    label: TODO metric
    product: TODO
    aggregation: daily
    cumulative: true
    observation:
      id: TODO_source_id
      route: missing
      setup_hint: Configure a real source.
    update_prompt: Configure this before expecting readings.
```
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(RECIPE_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(placeholder_bindings, encoding="utf-8")

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))
            source_payload = json.loads(result.source_snapshot_paths[0].read_text(encoding="utf-8"))

        self.assertEqual(payload["metrics"][0]["status"], "source_gap")
        self.assertIn("source_not_configured:TODO_source_id", source_payload["gaps"])

    def test_reduces_completed_ticket_kpi_rewards_into_daily_observations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(REWARD_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(REWARD_BINDINGS, encoding="utf-8")
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
title: Rewarded
phase: complete
status: done
updated_at: 2026-07-01T09:00:00Z
---

# TASK-0001: Rewarded

## Reward

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "proof-backed harness improvement"
  - kpi_id: accepted_evidence_cycles
    expected_reward: "accepted experiment evidence"
  - kpi_id: auto_time_ratio
    expected_reward: "planning attribution only; runtime source owns the metric value"
guard: "count only after proof"
```

## Done / Proof
- Unit tests passed.
- Evidence: tickets/TASK-0001/artifacts/proof.md
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))
            reward_source_path = next(path for path in result.source_snapshot_paths if "ticket_reward_feedback" in str(path))
            reward_source = json.loads(reward_source_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["accepted_harness_improvements"]["current"], 1)
        self.assertEqual(by_id["accepted_harness_improvements"]["series"][0]["cumulative"], 1)
        self.assertNotEqual(by_id["auto_time_ratio"]["source_id"], "ticket_reward_feedback")
        self.assertNotEqual(by_id["auto_time_ratio"]["current"], 1)
        self.assertEqual(by_id["accepted_harness_improvements"]["series"][0]["items"][0]["ticket_id"], "TASK-0001")
        self.assertEqual(
            by_id["accepted_evidence_cycles"]["series"][0]["items"][0]["expected_reward"],
            "accepted experiment evidence",
        )
        self.assertIn(
            "tickets/TASK-0001/ticket.md:reward_attribution_not_metric_value:auto_time_ratio:autonomy_time_feedback",
            reward_source["gaps"],
        )

    def test_completed_archived_ticket_rewards_are_counted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(REWARD_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(REWARD_BINDINGS, encoding="utf-8")
            ticket_dir = root / "tickets" / "archive" / "TASK-0009"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0009
phase: complete
status: done
updated_at: 2026-07-01T09:00:00Z
---

# TASK-0009

## Reward

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "archived proof-backed harness improvement"
guard: "count only after proof"
```

## Done / Proof
- Evidence: tickets/archive/TASK-0009/artifacts/proof.md
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["accepted_harness_improvements"]["current"], 1)
        self.assertEqual(
            by_id["accepted_harness_improvements"]["series"][0]["items"][0]["ticket"],
            "tickets/archive/TASK-0009/ticket.md",
        )

    def test_ticket_kpi_rewards_require_completion_and_proof(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(REWARD_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(REWARD_BINDINGS, encoding="utf-8")
            building_dir = root / "tickets" / "TASK-0001"
            building_dir.mkdir(parents=True)
            (building_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
phase: building
status: todo
updated_at: 2026-07-01T09:00:00Z
---

# TASK-0001

## Reward

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "planned work must not count"
guard: "proof first"
```

## Done / Proof
- Evidence: planned only.
""",
                encoding="utf-8",
            )
            no_proof_dir = root / "tickets" / "TASK-0002"
            no_proof_dir.mkdir(parents=True)
            (no_proof_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0002
phase: complete
status: done
updated_at: 2026-07-01T10:00:00Z
---

# TASK-0002

## Reward

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "complete without proof must not count"
guard: "proof first"
```
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))
            source_path = next(path for path in result.source_snapshot_paths if "ticket_reward_feedback" in str(path))
            source_snapshot = json.loads(source_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["accepted_harness_improvements"]["status"], "source_gap")
        self.assertIn("tickets/TASK-0002/ticket.md:missing_completion_proof", source_snapshot["gaps"])

    def test_reads_metric_recipes_from_bindings_with_pinned_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(RECIPE_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(RECIPE_BINDINGS, encoding="utf-8")
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
phase: complete
status: done
updated_at: 2026-07-01T10:00:00Z
---

# TASK-0001

## Reward

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "recipe shape counts this"
guard: "proof first"
```

## Done / Proof
- Tests passed.
- Evidence: tickets/TASK-0001/artifacts/proof.md
""",
                encoding="utf-8",
            )
            (root / ".farplane" / "state").mkdir(parents=True)
            (root / ".farplane" / "state" / "ticket-thread-associations.jsonl").write_text("", encoding="utf-8")

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(
            set(by_id),
            {"accepted_harness_improvements", "auto_completion_rate", "intervention_free_ticket_count"},
        )
        self.assertTrue(by_id["accepted_harness_improvements"]["pinned"])
        self.assertEqual(by_id["accepted_harness_improvements"]["source_id"], "ticket_reward_feedback")
        self.assertEqual(by_id["accepted_harness_improvements"]["series"][0]["cumulative"], 1)
        self.assertEqual(by_id["auto_completion_rate"]["status"], "source_gap")

    def test_ticket_intervention_feedback_counts_post_start_human_turns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(RECIPE_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(RECIPE_BINDINGS, encoding="utf-8")
            ticket_a = root / "tickets" / "TASK-0001"
            ticket_b = root / "tickets" / "archive" / "TASK-0002"
            ticket_a.mkdir(parents=True)
            ticket_b.mkdir(parents=True)
            for ticket_dir, ticket_id, hour in [(ticket_a, "TASK-0001", "10"), (ticket_b, "TASK-0002", "11")]:
                (ticket_dir / "ticket.md").write_text(
                    f"""---
ticket_id: {ticket_id}
phase: complete
status: done
updated_at: 2026-07-01T{hour}:30:00Z
---

# {ticket_id}

## Reward

```yaml
kpi_rewards:
  - kpi_id: auto_completion_rate
    expected_reward: "complete without re-entry"
guard: "known association only"
```

## Done / Proof
- Evidence: proof.md
""",
                    encoding="utf-8",
                )
            state_dir = root / ".farplane" / "state"
            state_dir.mkdir(parents=True)
            (state_dir / "ticket-thread-associations.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"ticket_id": "TASK-0001", "thread_id": "thread-a", "execution_started_at": "2026-07-01T10:00:00Z"}),
                        json.dumps({"ticket_id": "TASK-0002", "thread_id": "thread-b", "execution_started_at": "2026-07-01T11:00:00Z"}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            event_dir = root / ".farplane" / "events"
            event_dir.mkdir(parents=True)
            (event_dir / "events.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"timestamp": "2026-07-01T10:00:00Z", "event_type": "turn_start", "thread_id": "thread-a", "actor": "user"}),
                        json.dumps({"timestamp": "2026-07-01T10:10:00Z", "event_type": "turn_start", "thread_id": "thread-a", "actor": "user"}),
                        json.dumps({"timestamp": "2026-07-01T11:10:00Z", "event_type": "turn_start", "thread_id": "thread-b", "actor": "assistant"}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))
            source_path = next(path for path in result.source_snapshot_paths if "ticket_intervention_feedback" in str(path))
            source_payload = json.loads(source_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["auto_completion_rate"]["current"], 0.5)
        self.assertEqual(by_id["intervention_free_ticket_count"]["current"], 1)
        self.assertEqual(by_id["intervention_free_ticket_count"]["series"][0]["cumulative"], 1)
        source_by_id = {obs["metric_id"]: obs for obs in source_payload["observations"]}
        self.assertEqual(source_by_id["ticket_intervention_turn_count"]["value"], 1)
        self.assertEqual(source_by_id["intervention_free_ticket_count"]["value"], 1)
        self.assertEqual(source_by_id["ticket_intervention_turn_count"]["items"][0]["intervention_turns"], 1)

    def test_ticket_intervention_feedback_source_gaps_missing_association(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(RECIPE_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(RECIPE_BINDINGS, encoding="utf-8")
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
phase: complete
status: done
updated_at: 2026-07-01T10:30:00Z
---

# TASK-0001

## Done / Proof
- Evidence: proof.md
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            source_path = next(path for path in result.source_snapshot_paths if "ticket_intervention_feedback" in str(path))
            source_payload = json.loads(source_path.read_text(encoding="utf-8"))

        self.assertEqual(source_payload["status"], "source_gap")
        self.assertIn("missing_ticket_thread_association_source", source_payload["gaps"])


if __name__ == "__main__":
    unittest.main()
