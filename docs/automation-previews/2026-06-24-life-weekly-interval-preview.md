---
title: "Life Weekly Interval Automation Preview"
owner: automation-advisor
status: active
created_at: 2026-06-24
automation_id: weekly-opportunity-deep-research
skill_ref: skills/interval-update/SKILL.md
---

# Life Weekly Interval Automation Preview

This is the reviewable prompt shape for Kenji's weekly life strategy
automation. The live Codex automation calls the generic `interval-update`
skill; this file exists so the prompt can be reviewed without opening the
Codex app.

Reusable logic lives in:

- `skills/interval-update/SKILL.md`
- `skills/interval-update/references/workflows/plan-progress.md`
- `skills/interval-update/references/workflows/codex-attention-drift.md`
- `skills/interval-update/references/workflows/ticket-board-drift.md`
- `skills/interval-update/references/workflows/feedback-obligations.md`
- `skills/interval-update/references/workflows/opportunity-signals.md`
- `skills/interval-update/references/workflows/goal-drift.md`
- `skills/interval-update/references/workflows/metric-snapshot.md`
- `skills/interval-update/references/workflows/priority-planning.md`

Project-specific configuration stays here and in the live automation prompt.

```text
Run Kenji's weekly life strategy interval.

Call:
- `interval_update(project_root="/Users/kenjipcx/life", interval_id="weekly_life_strategy", review_window="last_week", planning_window="next_week", timezone="Asia/Kuala_Lumpur")`

Reads:
- `docs/MEMORY.md` as the goals and durable memory source.
- `docs/HISTORY.md`, `docs/LESSONS.md`, and `docs/TROUBLES.md` as durable
  context.
- Prior weekly strategy run artifacts under `docs/strategy-automation/runs/`.
- `docs/strategy-automation/daily-strategy-alignment-impl-plan.md` as extra
  planning context when present.
- `.farplane/events/` and `.farplane/state/message-windows/` as Codex attention
  telemetry.
- `.farplane/state/notion-context/` as status context when present.
- `docs/strategy-automation/` as opportunity and planning artifact context.

Writes:
- A dated weekly run artifact under `docs/strategy-automation/runs/`.
- Next-week priorities, depriorities, follow-ups, source gaps, and Goal Advisor
  handoffs.
- Compact durable updates to `docs/MEMORY.md`, `docs/TROUBLES.md`,
  `docs/LESSONS.md`, or `docs/HISTORY.md` only when the report evidence
  warrants them.

Runs:
- `plan_progress`: true.
- `codex_attention_drift`: true.
- `ticket_board_drift`: light.
- `feedback_obligations`: when sources exist.
- `opportunity_signals`: true.
- `goal_drift`: true.
- `metric_snapshot`: when sources exist.
- `priority_planning`: true.

Gates:
- Report before memory updates.
- Approval required for durable strategy changes that go beyond compact memory
  maintenance.
- Source gaps instead of guessed private refs.

Use the skill's default interval workflow standard, but treat absent Farplane
project files such as `tickets/`, Pulse reports, or `farplane/pm.json` as
source gaps for this life project unless they exist locally.

Before final synthesis, run only the configured report workflows above. Keep
every workflow evidence-backed: cite memory files, weekly strategy run
artifacts, local `.farplane` event/message-window summaries, Notion/status
context refs when available, opportunity docs, or source gaps. Do not import
hidden assumptions from the old `weekly-strategy-analysis` skill; reusable
logic now lives in `interval-update` workflow refs, and this automation
provides only project-specific configuration.

This interval owns weekly reporting, done-vs-not-done retro, Codex attention
drift, opportunity review, priority/depriority planning, and next-week guidance
for the life planning loop. Write a dated weekly run artifact under
`docs/strategy-automation/runs/` before updating durable memory. Update
`docs/MEMORY.md` only with compact durable weekly priorities, depriorities,
blockers, or planning signals that should affect other life automations. Put
repeated misses, failed attempts, blockers, and correction pain in
`docs/TROUBLES.md`; put fixed reusable prevention lessons in
`docs/LESSONS.md`; put meaningful timeline events in `docs/HISTORY.md`.

Do not mutate Notion task status, publish, deploy, spend money, scrape private
contact details, commit, push, perform destructive cleanup, or spawn unbounded
worker threads.

Final output: report path, source gaps, drift findings, top next-week
priorities, depriorities, follow-ups, memory updates made or intentionally
skipped, and any Goal Advisor handoffs.
```
