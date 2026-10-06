---
schema: farplane_automation_recipe
framework_template_version: 1.0.0
owner: automation-advisor
id: project-feed-scout
name: Project Feed Scout
kind: cron
status: paused
target:
  workspace: <project-root>
schedule:
  type: daily
  timezone: <timezone>
  time: 05:15
---
Task record: GitHub Issues of each project's repo (tickets/README.md); this job never writes them.

Use $feed-scout.

Run the bounded daily Feed Scout. Write its dated report, then update and
validate the configured Scout Brief in place with canonical ICPs, current
trends, notable things, and source gaps. Merge current synthesis rather than
creating daily/monthly snapshots. Then produce bounded source-backed candidate
interventions. Report at most one direct recovery candidate, only for an
evidenced existing failure with known fix and no experiment debt; never create
the issue. Opportunities remain planner candidates. Do not execute tickets.

Params:
project_root = "<project-root>"
config_ref = "farplane/bindings.yaml#feed_scout"
window = "last_24h"
recovery_ticket_limit = 1
write_policy = "no task-record writes; recovery and opportunity candidates stay in the report"

Final response:
- Link the Feed Scout report path and summarize the strongest findings in 2-4 bullets.
- Link the Scout Brief path and report changed headings, source refs, and validation.
- List the direct recovery candidate, or `none`.
- List candidate interventions and their admission result:
  `recovery_candidate`, `planner_candidate`, `source_gap`, `blocked_by_gate`, or `not_ticketable`.
- Name source gaps, external side-effect gates, and next owner.
- Include the no-execution receipt.

Config source:
farplane/automations/feed-scout.md id="project-feed-scout"
