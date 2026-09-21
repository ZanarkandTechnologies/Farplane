---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-feed-scout
name: Farplane Feed Scout
kind: cron
status: active
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: 05:15
---
Task storage override: follow tickets/README.md. Multica is dashboard-only;
resolve project bindings, keep issues unassigned, and use --no-start for updates.
Create/update task records through the existing Multica CLI, never ticket.md.
Do not invoke filesystem materializers, finalizers or dispatch based on local
migration snapshots. If a phase requires such a legacy adapter, report that
phase as unavailable; continue independent read-only reporting. Never start
Multica agents, squads, autopilots or runs.

Use $feed-scout.

Run the bounded daily Feed Scout from the configured sources. Write its dated
report, then update and validate the configured persistent Scout Brief
before bounded source-backed candidate interventions. Re-render canonical ICP
fields from `farplane/harness.yaml#areas`; update only source-backed concerns,
language, trends, notable things, and source gaps. Merge or replace current
synthesis in place—do not append daily snapshots or a monthly timeline. You may create one
direct recovery ticket only for an evidenced existing failure with known fix,
KPI/guard, proof, and no experiment debt. Opportunities remain candidates for
the next-wave planner. Do not execute tickets.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
config_ref = "farplane/bindings.yaml#feed_scout"
window = "last_24h"
recovery_ticket_limit = 1
write_policy = "unassigned Multica recovery issues only; no opportunity or experiment tickets"

Final response:
- Link the Feed Scout report path and summarize the strongest findings in 2-4 bullets.
- Link the Scout Brief path and include its changed headings, `updated_at`, source
  refs, and validation result.
- List direct recovery tickets created or updated, or `none`.
- List candidate interventions and their admission result: `created`,
  `planner_candidate`, `source_gap`, `blocked_by_gate`, or `not_ticketable`.
- Name source gaps, external side-effect gates, and next owner.
- Include the no-execution receipt.

Config source:
farplane/automations/feed-scout.md id="farplane-feed-scout"
