---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
source_template: automations/feed-scout.md
source_template_version: 1.0.0
id: farplane-feed-scout
name: Farplane Feed Scout
kind: cron
status: active
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
Opportunities remain candidates for the next-wave planner. Do not execute tickets.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
config_ref = "farplane/bindings.yaml#feed_scout"
window = "last_24h"
recovery_ticket_limit = 1
write_policy = "no task-record writes; recovery and opportunity candidates stay in the report"

Final response:
- Link the Feed Scout report path and summarize the strongest findings in 2-4 bullets.
- Link the Scout Brief path and include its changed headings, `updated_at`, source
  refs, and validation result.
- List the direct recovery candidate, or `none`.
- List candidate interventions and their admission result:
  `recovery_candidate`, `planner_candidate`, `source_gap`, `blocked_by_gate`, or `not_ticketable`.
- Name source gaps, external side-effect gates, and next owner.
- Include the no-execution receipt.

Config source:
farplane/automations/feed-scout.md id="farplane-feed-scout"
