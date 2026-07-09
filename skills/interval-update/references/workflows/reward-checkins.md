---
title: "Reward Check-ins Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Reward Check-ins Workflow

## Context

Use this workflow when an interval update should compare ticket planning
expectations against observed reality. It is a calibration loop, not a new
reward database. The ticket `## Reward` block stores the expected reward,
check-in time, actual result, and scalar similarity score.

The workflow answers:

```text
Did the actual result match what the planner expected?
If not, what should the next planning loop learn or investigate?
```

## Workflow Signature

```text
reward_checkins(project_root, now, review_window, planning_window,
                bad_threshold = 0.5)
  -> due_reward_items
   + legacy_missing_check_in
   + ticket_reward_patches?
   + bad_predictions
   + retro_ticket_candidates?
   + interval_report_section

state: reads(tickets/**/ticket.md, farplane/bindings.yaml, product files,
             metrics/reports/artifacts available in the review window);
       writes(parent_interval_update_report_section,
              proposed ticket_reward_patches,
              optional ticket delta when a low score needs follow-up)
gates: due_query_run; actual_result_grounded; reward_score_between_minus1_and1;
       low_scores_reported; retro_ticket_only_when_followup_needed
fails: scoring not-due tickets; creating a daily retro ticket without a miss;
       using reward_score as a KPI value; adding a separate reward ledger
```

## Score Contract

`reward_score` is a scalar from `-1` to `1` measuring similarity between
`expected_reward` and `actual_result`.

```text
 1.0  actual strongly matched or exceeded expected reward
 0.0  unclear, unrelated, or weakly related
-1.0  actual contradicted expected reward or created negative value
```

The analyzer owns the judgment. The script only finds due and already-scored
items.

## Phase Boundary

`reward_checkins` is the explicit interval workflow exception. The parent may
run the due-item helper inline because it is mechanical discovery. The analyzer
should run as a bounded lane over due items and cited evidence; unlike other
workflow lanes, it may propose only ticket
`Reward.kpi_rewards[].actual_result`, `reward_score`, and
`reward_score_reason` after grounding actuals. The parent writes those patches
only after the interval report records them as allowed post-report deltas. The
analyzer must not edit expected reward, goals, products, automation state, or
unrelated ticket fields.

## Todo List

- [ ] 1. Find due items.
  - [ ] Run:
        `python3 skills/interval-update/scripts/reward_checkins.py --ticket-dir tickets --now <now> --lookback-days 14`.
  - [ ] Treat `check_in_at <= now` plus missing `actual_result` or
        `reward_score` as due.
  - [ ] Treat `check_in_at > now` as not due.
  - [ ] Treat reward items without `check_in_at` as legacy missing-check-in
        items, not actionable source gaps, unless the ticket was created after
        this schema became required.
- [ ] 2. Ground actuals.
  - [ ] For each due item, read the ticket proof, artifacts, metrics, interval
        reports, review receipts, and product context needed to summarize the
        actual result.
  - [ ] If evidence is missing, set `actual_result` to the source gap and score
        the prediction according to how much reality can be compared.
- [ ] 3. Score predictions.
  - [ ] Propose `ticket_reward_patches` containing `actual_result`,
        `reward_score`, and `reward_score_reason`.
  - [ ] Keep `reward_score` within `-1..1`.
  - [ ] Do not edit `expected_reward` while scoring; preserve the original
        planning claim.
- [ ] 4. Report learning.
  - [ ] Include due, scored, low-scoring, source-gap, and not-due counts in the
        interval report.
  - [ ] Include proposed `ticket_reward_patches` in the interval report before
        the parent applies them as post-report deltas.
  - [ ] Name bad predictions with `reward_score < bad_threshold`.
  - [ ] Create a retro ticket only when a miss reveals a real investigation,
        strategy, instrumentation, or product-learning task. Do not create a
        daily retro ticket just because the workflow ran.
- [ ] 5. Preserve ownership.
  - [ ] Ticket `Reward` owns expected-vs-actual check-in fields.
  - [ ] Interval report owns the dated summary and next planning implication.
  - [ ] Product `product.md` changes only when the score changes current
        strategy.

## Output

```yaml
reward_checkins:
  due_count:
  scored_count:
  bad_prediction_count:
  source_gap_count:
  legacy_missing_check_in_count:
  due_items:
    - ticket:
      kpi_id:
      expected_reward:
      check_in_at:
      actual_result:
      reward_score:
      reward_score_reason:
  bad_predictions:
    - ticket:
      reward_score:
      why_prediction_failed:
      next_action:
  retro_ticket_candidates:
    - title:
      reason:
      reward:
      guard:
```
