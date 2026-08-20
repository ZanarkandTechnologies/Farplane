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

Run one bounded scheduled pass. For Interval, use one evidence window and the
current weekly working draft. Daily stages candidate upserts with zero durable
promotions. Weekly dispositions every candidate, freezes the report, promotes
authorized records, writes the receipt, and opens the next draft. Name only
project-specific inputs, promotion policy, external side-effect gates, and the
no-ticket-execution boundary. Let the skill own routing and validation.

Params:
project_root = "<project-root>"

Final response:
- Link the report, weekly draft, and knowledge receipt.
- List candidate upserts or Weekly dispositions and promoted owners.
- List tickets created or updated, or `none`.
- List each candidate/admission decision with the reason: `created`,
  `updated`, `already_owned`, `planner_candidate`, `source_gap`,
  `same_run_ledger`, `blocked_by_gate`, or `not_ticketable`.
- Name operator-needed items, source gaps, and the next owner.
- Include the no-ticket-execution receipt and any knowledge blockers.

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

Daily and Weekly call `$interval-update`; one bounded evidence window produces
the dated report, weekly-draft delta, and receipt. Daily promotes nothing.
Weekly consolidates completed Daily receipts, dispositions candidates, promotes
authorized records, and opens the next draft. Feed Scout calls `$feed-scout`
and weekly self-improvement calls `$dogfood-review`. None execute tickets; the
single Work Pulse heartbeat does.
