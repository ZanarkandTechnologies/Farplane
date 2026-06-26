---
title: "Interval Codex Automation Template"
status: active
owner: automation-advisor
created_at: 2026-06-24
updated_at: 2026-06-26
template_version: "0.4.1"
---

# Interval Codex Automation Template

Use this prompt for a project's scheduled interval automation.

```text
Use `$interval-update`.

Params:

project_root = "<project-root>"
interval_id = "<interval_id>"
review_window = "<bounded review window>"
planning_window = "<bounded planning window>"
timezone = "<timezone or UTC>"

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
