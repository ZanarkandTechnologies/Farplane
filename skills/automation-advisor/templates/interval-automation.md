---
title: "Interval Codex Automation Template"
status: active
owner: automation-advisor
created_at: 2026-06-24
updated_at: 2026-06-27
template_version: "0.5.0"
---

# Interval Codex Automation Template

Use these marker-delimited blocks for a project's scheduled interval automation
in `farplane/automations.md`. The TOML block is Codex automation metadata; the
prompt block carries the skill call and skill params copied into the live Codex
automation.

````markdown
<!-- farplane:automation-config id="<automation-id>" format="toml" -->
```toml
id = "<automation-id>"
name = "<human name>"
kind = "cron"
status = "active"
workspace = "<project-root>"

[schedule]
type = "daily | weekly | monthly"
timezone = "<timezone>"
time = "05:33"
days = ["Mon"]
day_of_month = 1
```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="<automation-id>" -->
```text
Use $interval-update.

Run the configured Farplane interval. Review the bounded window, write the
date-stamped interval report, and emit Pulse or Goal Advisor guidance rather
than doing ticket implementation directly.

Params:
project_root = "<project-root>"
interval_id = "<interval_id>"
review_window = "<bounded review window>"
planning_window = "<bounded planning window>"
timezone = "<timezone or UTC>"

Config source:
farplane/automations.md automation-config id="<automation-id>"

Overrides:
read_parent_interval = "<latest longer-interval report, when present>"
read_child_intervals = "<shorter-interval reports inside review window, when relevant>"
plan_progress = <false | "light" | true>
codex_attention_drift = <false | "light" | true>
ticket_board_drift = <false | "light" | true>
feedback_obligations = <false | "when sources exist" | true>
opportunity_signals = <false | "when sources exist" | true>
goal_drift = <false | "light" | true>
metric_snapshot = <false | "when sources exist" | true>
compounding_leverage_review = <false | "light" | true>
skill_hardening = <false | "when sources exist" | true>
skill_refinement = <false | "when sources exist" | true>
docs_consolidation = <false | "when sources exist" | true>
priority_planning = <false | "light" | true>
```
<!-- /farplane:automation-prompt -->
````

Monthly registry consolidation example:

````markdown
<!-- farplane:automation-config id="<project-monthly-registry-consolidation-id>" format="toml" -->
```toml
id = "<project-monthly-registry-consolidation-id>"
name = "Project Monthly Registry Consolidation"
kind = "cron"
status = "active"
workspace = "<project-root>"

[schedule]
type = "monthly"
timezone = "<timezone>"
day_of_month = 1
time = "06:15"
```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="<project-monthly-registry-consolidation-id>" -->
```text
Use $consolidate.

Run the monthly registry consolidation review. This is a report-only registry
truth and ownership compression pass, not a weekly self-learning loop and not
a direct artifact rewrite.

Scope:
target = [
  "docs/skills/registry.jsonl",
  "docs/features/registry.jsonl",
  "docs/systems/registry.jsonl",
  "docs/templates/registry.jsonl",
  "docs/sources/registry.jsonl"
]
structure = "registry"

Constraints:
preserve_ids = true
preserve_evidence = true
no_delete = true
owner_boundary = "registry rows only; route underlying artifact edits to owners"

Output:
Write a dated report under:
.farplane/reports/consolidation/registry/<YYYY-MM-DDTHHMMSSZ>.md

Do not edit registries or underlying artifacts during this automation run.

Params:
project_root = "<project-root>"
review_window = "last_month"
planning_window = "next_month"
timezone = "<timezone>"

Config source:
farplane/automations.md automation-config id="<project-monthly-registry-consolidation-id>"
```
<!-- /farplane:automation-prompt -->
````
