---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-feed-scout
name: Farplane Feed Scout
kind: cron
status: paused
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: "23:15"
---
Task record: GitHub Issues of each project's repo (tickets/README.md); this job never writes them.

Use $feed-scout.

Run the bounded daily Feed Scout from the configured sources. Write its dated
report, then update and validate the configured persistent Scout Brief
before bounded source-backed candidate interventions. Re-render canonical ICP
fields from `farplane/harness.yaml#areas`; update only source-backed concerns,
language, trends, notable things, and source gaps. Merge or replace current
synthesis in place—do not append daily snapshots or a monthly timeline. Report at
most one direct recovery candidate, only for an evidenced existing failure with
known fix, KPI/guard, proof, and no experiment debt; never create the issue.
Opportunities remain report candidates for the operator to pick. Create and execute no tickets.
Customer events: for each new `customer_event` in the report (an event on an entity with `kind: customer` or `kind: prospect`), open its own research thread on the office queue: `.agent-office/bin/office-queue add --floor <floor> --routine customer-event-<canonical key> --title "Research <entity>: <event>"`, with the brief on stdin: "Use $prospect with intake `event`: <entity>, <event>, <source link>, <date>. Return the OpportunityCase; send nothing." The routine id keeps a rerun from opening the same event twice. These queue tasks are the one exception to creating no tasks; never file issues for them.
Skip what the operator stopped: before proposing for a floor, run `.agent-office/bin/office-queue denied --floor <floor>` (from the Farplane checkout) and drop any proposal whose key it lists. A proposal's key is its `Proposal: <key>` line, else its title in lower-case words joined by hyphens; write a `Proposal:` line on anything you file.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
config_ref = "farplane/bindings.yaml#feed_scout"
window = "last_24h"
recovery_candidate_limit = 1
write_policy = "no task-record writes; recovery and opportunity candidates stay in the report"

Final response:
- Link the Feed Scout report path and summarize the strongest findings in 2-4 bullets.
- Link the Scout Brief path and include its changed headings, `updated_at`, source
  refs, and validation result.
- List the direct recovery candidate, or `none`.
- List candidate interventions and their admission result:
  `recovery_candidate`, `candidate`, `source_gap`, `blocked_by_gate`, or `not_actionable`.
- Name source gaps, external side-effect gates, and next owner.
- List each customer event and the queue task id it opened, or why none.
- Include the no-execution receipt.

Config source:
farplane/automations/steps/feed-scout.md id="farplane-feed-scout"
