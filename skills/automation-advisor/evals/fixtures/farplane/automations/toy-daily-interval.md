---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: toy-daily-interval
name: Toy Daily Interval
kind: cron
status: active
target:
  workspace: /tmp/toy-project
schedule:
  type: daily
  timezone: UTC
  time: 05:30
---
Use $interval-update.

Run the Daily reporting review over the last 24 hours and do not execute work.

Params:
project_root = "/tmp/toy-project"
interval_id = "daily"
review_window = "last_24h"
