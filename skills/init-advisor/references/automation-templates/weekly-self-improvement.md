---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: project-weekly-self-improvement
name: Project Weekly Self-Improvement
kind: cron
status: paused
target:
  workspace: <project-root>
schedule:
  type: weekly
  timezone: <timezone>
  days:
  - Mon
  time: 06:00
---
Use $dogfood-review.

Bind a cutoff, page through all exact `self_improvement` admission receipts in
the interval, include every still-live earlier packet, and read ticket Reward,
check-in, progress, artifact, and review evidence. Write one dated checkpoint
with the complete outcome ledger, live work, source gaps, portfolio-selection
lessons, and qualified/deprioritized opportunity signals. Expose only the
report as `planner_context_ref` for normal global planning. Do not create specs
or tickets, reserve a wave, materialize, execute, dispatch, decide Reward, run
check-ins, or mutate skills/policy.

Params:
project_root = "<project-root>"
window = "last_week"
planning_scope = "report_only_current_context"
write_policy = "dated Dogfood checkpoint only"

Reads:
- all exact self_improvement admission receipts through cutoff
- every still-live earlier self_improvement packet
- previous dated Dogfood report when present
- farplane/harness.yaml areas.self_improvement complete record and planner_instruction
- Core active/archive ticket history with expected and actual Reward
- harness health, template rollout, skill eval, and feature/system evidence

Final response:
- Link the retrospective report path and summarize the portfolio decision in 2-4 bullets.
- List all opportunity signals with `qualified`, `deprioritized`, `duplicate`,
  `conflict`, `source_gap`, or `not_ticketable` evidence.
- Name operator-needed items, source gaps, and next owner.
- Include the no-action receipt: no planning, ticket/spec creation,
  materialization, execution, dispatch, check-in, Reward decision, or mutation.

Config source:
farplane/automations/weekly-self-improvement.md id="project-weekly-self-improvement"
