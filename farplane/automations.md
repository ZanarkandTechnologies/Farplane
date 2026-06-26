---
kind: project-automations
framework_template_version: "0.4.0"
updated_at: 2026-06-26
owner: automation-advisor
source_of_truth:
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/taste-loop/SKILL.md
  - farplane/pm.json
---

# Farplane Automations

This file stores the exact prompt blocks copied into Codex automation records.
Prompts should configure cadence, project root, thread IDs, and project-specific
extensions only. The reusable loop behavior lives in `pulse-update`,
`interval-update`, and `taste-loop`.

## Pulse

| Field | Value |
| --- | --- |
| Automation id | `farplane-ticket-update` |
| Name | `Farplane Pulse` |
| Kind | `heartbeat` |
| RRULE | `FREQ=MINUTELY;INTERVAL=30` |
| Target thread | `019ed47a-3182-73f3-879f-a53797759b2a` |

```text
Run one Farplane Pulse beat.

Call:
- `pulse_update(project_root="/Users/kenjipcx/Zanarkand Technologies/projects/Farplane")`

Project extensions: none.

Project gates:
- no push, deploy, publish, spend, account changes, or destructive cleanup.
- no drift review, scrum reflection, or strategy replanning.

Final output:
- execution mode
- reward updates
- child thread IDs or planning request
- report/state paths
- evidence that will decide the next reward update
```

## Daily Interval

| Field | Value |
| --- | --- |
| Automation id | `farplane-daily-interval` |
| Name | `Farplane Daily Interval` |
| Kind | `cron` |
| RRULE | `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0` |
| Workspace | `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane` |

```text
Run the Farplane Daily Interval.

Call:
- `interval_update(project_root="/Users/kenjipcx/Zanarkand Technologies/projects/Farplane", interval_id="daily_interval", review_window="last_24h", planning_window="next_24h", timezone="Asia/Kuala_Lumpur")`

Project context:
- read the latest `weekly_interval` report when it exists.

Project workflows:
- `plan_progress`: light.
- `goal_drift`: light.
- `ticket_board_drift`: light.

Project gates:
- report before mutation.
- source gaps instead of guessed refs.
- no scheduler state writes.
- no push, deploy, publish, spend, external mutation, commit, unbounded worker
  spawning, or destructive cleanup.

Final output:
- dated report path
- next-24-hour plan
- Pulse guidance
- proposed ticket deltas or Goal Advisor handoffs
- approval-required goals delta, if any
```

## Weekly Interval

| Field | Value |
| --- | --- |
| Automation id | `farplane-weekly-interval` |
| Name | `Farplane Weekly Interval` |
| Kind | `cron` |
| RRULE | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=5;BYMINUTE=45;BYSECOND=0` |
| Workspace | `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane` |

```text
Run the Farplane Weekly Interval.

Call:
- `interval_update(project_root="/Users/kenjipcx/Zanarkand Technologies/projects/Farplane", interval_id="weekly_interval", review_window="last_week", planning_window="next_week", timezone="Asia/Kuala_Lumpur")`

Project context:
- read all `daily_interval` reports inside `last_week`.

Project workflows:
- `plan_progress`: true.
- `codex_attention_drift`: true.
- `ticket_board_drift`: true.
- `feedback_obligations`: when sources exist.
- `opportunity_signals`: when sources exist.
- `goal_drift`: true.
- `metric_snapshot`: when sources exist.
- `compounding_leverage_review`: true.
- `skill_hardening`: true.
- `skill_refinement`: when sources exist.
- `docs_consolidation`: when sources exist.
- `priority_planning`: true.

Project gates:
- report before mutation.
- approval required for static charter, north-star, KPI, strategy-axis,
  quarterly/yearly, durable milestone, and hold changes.
- urgent leverage escalation requires high confidence, explicit loss term,
  evidence refs, review-by date, and owner route.
- source gaps instead of guessed refs.
- no scheduler state writes.
- no push, deploy, publish, spend, external mutation, commit, unbounded worker
  spawning, or destructive cleanup.

Final output:
- dated report path
- next-week plan
- lane distribution and ticket budget
- Pulse guidance
- proposed ticket deltas or Goal Advisor handoffs
- approval-required goals delta, if any
- leverage decisions and reward closure
```

## Active-Hours Taste Loop

| Field | Value |
| --- | --- |
| Automation id | `farplane-active-hours-taste-loop` |
| Name | `Farplane Active-Hours Taste Loop` |
| Kind | `cron` |
| RRULE | `FREQ=HOURLY;INTERVAL=1` |
| Workspace | `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane` |
| Status | `prompt-ready; activation requires explicit operator action` |

```text
Run one Farplane active-hours taste-loop beat.

Call:
- `taste_loop(project_root="/Users/kenjipcx/Zanarkand Technologies/projects/Farplane")`

Project context:
- use `skills/taste-loop/templates/heartbeat-prompt.md` as the reusable prompt
  body and this block as the Farplane-specific automation wrapper.
- use `FARPLANE_TASTE_LOOP_*` config from the rendered Codex config.
- Daily and Weekly Interval may influence priorities through goals/products and
  reports, but this heartbeat owns only the active-hours feedback opportunity.

Project gates:
- no hidden daemon, unbounded worker spawning, publish, deploy, spend,
  account changes, or external mutation.
- no local runner or script is the primary execution surface; this is a
  Codex-native heartbeat prompt.
- no live target skill edits from this heartbeat; emit a feedback card or Goal
  Advisor handoff instead.
- no legacy autoresearch route unless a future approved config explicitly
  enables a safe mechanical METRIC loop.
- respect active-hours, max-open-feedback, max-actions-per-beat, cooldown, and
  convergence config.

Final output:
- status: no_op, feedback_card, goal_handoff, or blocked
- report path under `.farplane/reports/taste-loop/`
- selected target IDs and scores
- feedback card path or Goal handoff path when emitted
- reason for no-op or blocked result
```
