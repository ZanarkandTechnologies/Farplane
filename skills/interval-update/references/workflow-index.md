---
title: "Interval Workflow Index"
status: active
owner: interval-update
kind: reference
---

# Interval Workflow Index

Load this reference only when `report_workflows` enables optional interval
workflows. Each enabled workflow runs as its own isolated lane unless the
workflow ref names a deterministic helper script or bounded write exception.

## Reflection Workflows

```text
plan_progress(review_window)
  -> goal_movement + task_drag + plan_realism
  ref: references/workflows/plan-progress.md

codex_attention_drift(review_window)
  -> attention_map + drift_causes
  ref: references/workflows/codex-attention-drift.md

ticket_board_drift(review_window)
  -> stale_work + board_hygiene_deltas
  ref: references/workflows/ticket-board-drift.md

feedback_obligations(review_window, planning_window)
  -> commitments + followups
  ref: references/workflows/feedback-obligations.md

opportunity_signals(review_window, planning_window)
  -> candidates + defer_or_displace_decisions
  ref: references/workflows/opportunity-signals.md

goal_drift(review_window)
  -> goal_findings + goals_delta_candidates
  ref: references/workflows/goal-drift.md

metric_snapshot(review_window)
  -> metric_status + gaps
  ref: references/workflows/metric-snapshot.md
```

## Reward And Leverage

```text
reward_checkins(review_window, planning_window)
  -> due_reward_checkins + bad_predictions + retro_ticket_candidates
  ref: references/workflows/reward-checkins.md
  script: scripts/reward_checkins.py

compounding_leverage_review(review_window, planning_window)
  -> lever_inventory + top_experiment_candidates + reward_signals
  ref: references/workflows/compounding-leverage-review.md
```

## Maintenance And Refinement

```text
skill_hardening(review_window, planning_window)
  -> harden_skill_handoffs + eval_candidates + processed_state_delta
  ref: references/workflows/skill-hardening.md

skill_refinement(review_window, planning_window)
  -> consolidate_skill_handoffs + compaction_candidates + coverage_risks
  ref: references/workflows/skill-refinement.md

docs_consolidation(review_window, planning_window)
  -> consolidate_docs_handoffs + stale_doc_candidates + source_gaps
  ref: references/workflows/docs-consolidation.md

tracked_feature_review(review_window, planning_window)
  -> dogfood_report + tracked_item_findings + interval_summary
   + improvement_ticket_path_or_candidate?
  skill: dogfood-review
  scope: active generated feature/system registry rows with non-empty `track`,
    plus active feature rows with `experimental: true`; retired or superseded
    feature rows are historical evidence for successor rows, not review targets
  writeback: when write_policy enables dogfood improvement ticket creation,
    dogfood-review may create exactly one planning/review ticket for the run;
    otherwise it must emit one complete candidate in the report
```

## Final Planning

```text
priority_planning(review_window, planning_window)
  -> priorities + depriorities + proof_checks
  ref: references/workflows/priority-planning.md
```

## Metric Refresh Helpers

```text
count_ticket_kpi_rewards(ticket_dir, date, kpi_key)
  -> { value, status, payload? }
  script: scripts/metric_refresh.py ticket-reward-count

calculate_autonomy_time_ratio(runtime_dir, date)
  -> { value, status, payload? }
  script: scripts/metric_refresh.py autonomy-time-ratio

calculate_ticket_intervention_metrics(ticket_dir, runtime_dir, date)
  -> { auto_completion_rate, intervention_free_ticket_count,
       ticket_intervention_turn_count }
  script: scripts/metric_refresh.py ticket-intervention-metrics

select_content_metric_targets(content_ledger, platform, kpi_key, date, window_days?)
  -> { status, external_ids, items, payload.fetch_command }
  script: scripts/metric_refresh.py content-targets
```
