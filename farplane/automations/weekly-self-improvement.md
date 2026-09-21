---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-weekly-self-improvement
name: Farplane Weekly Self-Improvement
kind: cron
status: active
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: weekly
  timezone: Asia/Kuala_Lumpur
  days:
  - Mon
  time: 06:00
---
Task storage override: follow tickets/README.md. Multica is dashboard-only;
resolve project bindings, keep issues unassigned, and use --no-start for updates.
Create/update task records through the existing Multica CLI, never ticket.md.
Do not invoke filesystem materializers, finalizers or dispatch based on local
migration snapshots. If a phase requires such a legacy adapter, report that
phase as unavailable; continue independent read-only reporting. Never start
Multica agents, squads, autopilots or runs.

Use $dogfood-review.

Run the weekly self-improvement review. Bind a cutoff, page through every exact
`self_improvement` admission receipt in the interval, include every still-live
earlier ticket, and read each packet's Reward rows, check-ins, progress,
artifacts, and review evidence. Write one dated portfolio checkpoint containing
all outcomes, live work, source gaps, portfolio-selection lessons, and
qualified/deprioritized opportunity signals.

Expose only the report path as `planner_context_ref` for normal global Plan Next
Wave. Do not create specs or tickets, reserve an area wave, choose a target
count, call Pulse materialization, execute, dispatch, check in Reward, or mutate
skills/policy. Missing receipts or ambiguous area derivation remain source gaps.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
window = "last_week"
planning_scope = "report_only_current_context"
write_policy = "dated Dogfood checkpoint only"

Reads:
- all exact self_improvement admission receipts through cutoff
- every still-live earlier self_improvement ticket packet
- previous dated Dogfood report when present
- farplane/harness.yaml planning.skill_refs plus passive areas.self_improvement context
- Core ticket history Reward receipts
- current harness metrics and skill/template/eval/QA rollout health

Final response:
- Link the retrospective report path and summarize the portfolio decision in 2-4 bullets.
- List all opportunity signals with `qualified`, `deprioritized`, `duplicate`,
  `conflict`, `source_gap`, or `not_ticketable` evidence.
- Name operator-needed items, source gaps, and next owner.
- Include the no-action receipt: no planning, spec/ticket creation,
  materialization, execution, dispatch, Reward decision/check-in, or mutation.

Config source:
farplane/automations/weekly-self-improvement.md id="farplane-weekly-self-improvement"
