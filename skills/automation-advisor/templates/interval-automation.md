---
title: "Scheduled Codex Automation Template"
status: active
owner: automation-advisor
created_at: 2026-06-24
updated_at: 2026-07-11
template_version: "1.0.0"
---

# Scheduled Codex Automation Template

Use `kind = "cron"` for every scheduled workflow other than Work Pulse. Give
Feed Scout, Daily BAU review, Weekly BAU review, weekly self-improvement, and
optional loops separate records so their reports and ticket supply remain
attributable.

```toml
[[automations]]
id = "<automation-id>"
name = "<human name>"
kind = "cron"
status = "active"
prompt = '''
Use $<owning-skill>.

Run one bounded scheduled pass. Name only project-specific inputs, ticket
limits, side-effect gates, and the report-first or no-execution boundary that a
human needs to edit. Let the skill own its normal workflow and output shape.

Params:
project_root = "<project-root>"

Final response:
- Link the report path and summarize the report in 2-4 bullets.
- List tickets created or updated, or `none`.
- List each candidate/admission decision with the reason: `created`,
  `updated`, `already_owned`, `planner_candidate`, `source_gap`,
  `same_run_ledger`, `blocked_by_gate`, or `not_ticketable`.
- Name operator-needed items, source gaps, and the next owner.
- Include the no-execution receipt for report-only runs.

Config source:
farplane/automations.toml automation id="<automation-id>"
'''

[automations.target]
workspace = "<project-root>"

[automations.schedule]
type = "daily | weekly | monthly | active_hours_interval"
timezone = "<timezone>"
time = "05:33"
days = ["Mon"]
day_of_month = 1
```

Daily and Weekly BAU review call `$interval-update`; they write dated reports
with a Problems ledger and may only create bounded maintenance tickets for
problems evidenced before the current run. Feed Scout calls `$feed-scout` and
weekly self-improvement calls `$dogfood-review`. None of these records execute
their tickets; the single Work Pulse heartbeat does. The final response should
make the report useful in chat instead of merely saying that the report was
written.
