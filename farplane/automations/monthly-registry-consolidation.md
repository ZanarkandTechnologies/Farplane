---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
source_template: automations/monthly-registry-consolidation.md
source_template_version: 1.0.0
id: farplane-monthly-registry-consolidation
name: Farplane Monthly Registry Consolidation
kind: cron
status: paused
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: monthly
  timezone: Asia/Kuala_Lumpur
  day_of_month: 1
  time: 06:15
---
Task record: GitHub Issues of each project's repo (tickets/README.md); this job never writes them.

Use $consolidate.

Review the Farplane skill, feature, system, template, and source registries for
duplication, staleness, and wrong ownership. Write a dated consolidation report
without editing registries or creating tickets during this run.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
review_window = "last_month"
structure = "registry"

Final response:
- Link the consolidation report path and summarize the key duplicate/stale/wrong-owner findings.
- List registry edits or tickets created; this run should normally report `none`.
- List recommended follow-ups with owner surface and reason.
- Name source gaps and include the no-mutation receipt.

Config source:
farplane/automations/monthly-registry-consolidation.md id="farplane-monthly-registry-consolidation"
