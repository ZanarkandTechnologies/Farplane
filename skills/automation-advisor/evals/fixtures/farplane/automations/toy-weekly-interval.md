---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: toy-weekly-interval
name: Toy Weekly Interval
kind: cron
status: active
target:
  workspace: /tmp/toy-project
schedule:
  type: weekly
  timezone: UTC
  days:
  - Mon
  time: 05:45
---
Use $interval-update.

Run the Weekly reporting review over the previous completed week and do not
execute work.

Params:
project_root = "/tmp/toy-project"
interval_id = "weekly"
review_window = "previous_completed_week"
