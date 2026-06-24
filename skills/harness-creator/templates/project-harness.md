---
kind: project-harness
status: draft
created_at: TODO
updated_at: TODO
template_id: project-harness
template_version: "0.2.0"
feature_refs:
  - FEAT-0027
  - FEAT-0048
project_id: TODO
automation_status: preview
framework_template_version: "0.1.0"
---

# Project Harness

## Harness Program

```harness-program
project "TODO" {
  values {
    mission: "TODO: why this project or business exists"
    operating_principles: [
      "TODO: principle that should guide repeated decisions"
    ]
    priorities: [
      impact.medium,
      loyal_users.medium,
      trust.high,
      money.medium,
      efficiency.medium
    ]
    non_tradeoffs: [
      "TODO: what cannot be sacrificed for local wins"
    ]
  }

  modes: [business]

  goal north_star {
    outcome: "TODO"
    metric: learning_metric("first honest baseline")
    horizon: "TODO"
  }

  axis reach_acquire {
    bet: "TODO: who finds this first?"
    kpi: missing_instrumentation("reach/acquisition baseline")
    evidence: ref("TODO")
    heartbeat: weekly_interval
  }

  axis activate_first_value {
    bet: "TODO: what is first value?"
    kpi: review_metric("first-value clarity")
    evidence: ref("TODO")
    heartbeat: weekly_interval
  }

  axis retain_loyalty {
    bet: "TODO: why would they return?"
    kpi: human_feedback("would return / would not return")
    evidence: ref("TODO")
    heartbeat: weekly_interval
  }

  axis efficiency_capability {
    bet: "TODO: what can be made easier or more repeatable?"
    kpi: learning_metric("cycle-time or effort baseline")
    evidence: ref("TODO")
    heartbeat: weekly_interval
  }

  system ticket_loop {
    status: ready
    evidence: ref("tickets/")
    action: use_existing("ticket workflow")
  }

  system feedback_collection {
    status: missing_instrumentation
    evidence: ref("TODO")
    action: ticket(first_feedback_signal_access)
  }

  system analytics {
    status: missing_instrumentation
    evidence: ref("TODO")
    action: ticket(metrics_source_access)
  }

  skill goal_advisor {
    status: ready
    use: "compile the current milestone or heartbeat"
  }

  skill deep_init_project {
    status: defer
    use: "create standard project systems only if missing"
  }

  skill notion_memory_sync {
    status: needs_operator_setup
    requires: [notion_project_access]
    use: "sync shared project memory and ticket state"
    action: ticket(notion_project_access)
  }

  skill telegram_notifications {
    status: needs_operator_setup
    requires: [telegram_notification_target]
    use: "send review, blocker, and feedback requests"
    action: ticket(telegram_notification_target)
  }

  skill metrics_ingest {
    status: needs_access
    requires: [metrics_source_access]
    use: "read product, content, or business metrics"
    action: ticket(metrics_source_access)
  }

  skill first_feedback_signal {
    status: needs_access
    requires: [first_feedback_signal_access]
    use: "TODO: read the first concrete feedback signal, such as Instagram attention graph, YouTube retention, PostHog activation funnel, sales-call objections, customer interviews, or operator usefulness labels"
    action: ticket(first_feedback_signal_access)
  }

  ticket notion_project_access {
    type: unblock
    human_step: "Grant access or provide the shared Notion project/database link"
    why: "Shared team memory and ticket state cannot sync without access"
    enables: [notion_memory_sync]
    fallback: use_existing("local filesystem memory only")
    gates: [no_account_changes]
  }

  ticket metrics_source_access {
    type: unblock
    human_step: "Connect read-only analytics access or provide a recurring export"
    why: "The harness cannot optimize KPIs from metrics that do not exist"
    enables: [metrics_ingest]
    fallback: human_feedback("operator labels examples until metrics exist")
    gates: [no_account_changes, no_private_scraping]
  }

  ticket first_feedback_signal_access {
    type: unblock
    human_step: "TODO: connect read-only access, provide recurring export, approve connector setup, or define operator labels for the first feedback signal"
    why: "The project cannot refine strategy until at least one honest feedback loop exists"
    enables: [first_feedback_signal, weekly_interval]
    fallback: human_feedback("operator labels outputs manually until the concrete signal exists")
    gates: [no_account_changes, no_private_scraping]
  }

  heartbeat pulse_update {
    trigger: "Codex automation every 30 minutes"
    bindings: "farplane/bindings.md"
    first: pulse_update
    skills: [pulse_update, goal_advisor, review]
    gates: [no_external_side_effects, ticket_or_goal_required_for_edits]
    output: ".farplane/reports/pulse/<timestamp>.md"
  }

  heartbeat daily_interval {
    trigger: "Codex automation daily"
    bindings: "farplane/bindings.md"
    first: interval_update
    review_window: "last_24h"
    planning_window: "next_24h"
    skills: [interval_update, update_memory, update_strategy, goal_advisor, review]
    delegate: delegate(ref("project-harness.md"), "refresh daily report and next-day plan", skills=[interval_update])
    gates: [review_before_external_side_effects]
    output: ".farplane/reports/interval/daily_interval/<timestamp>.md"
  }

  heartbeat weekly_interval {
    trigger: "Codex automation weekly"
    bindings: "farplane/bindings.md"
    first: interval_update
    review_window: "last_week"
    planning_window: "next_week"
    skills: [interval_update, feed_scout, update_memory, update_strategy, skill_maintenance, goal_advisor, review]
    delegate: delegate(ref("project-harness.md"), "refresh weekly strategy, memory, and skill upkeep", skills=[interval_update, skill_maintenance])
    gates: [review_before_external_side_effects]
    output: ".farplane/reports/interval/weekly_interval/<timestamp>.md"
  }

  milestone first_evidence_loop {
    task: "TODO: first evidence-producing milestone"
    route: goal_advisor
    metric: review_metric("milestone produces useful evidence")
    files: ["project-harness.md"]
    gates: [no_publish, no_spend, no_account_changes]
    done_when: "milestone handoff is ready or blocked by missing approval/data"
  }
}
```

## Evidence

- `facts:`
- `research_refs:`
- `local_refs:`
- `operator_inputs:`
- `metric_sources:`

## Assumptions

- `inferred_values:`
- `inferred_modes:`
- `unverified_domain_claims:`
- `why_research_was_or_was_not_needed:`

## Open Questions

- `operator_decisions:`
- `permissions_or_accounts:`
- `budgets:`
- `taste_or_strategy_questions:`

## Unblock Tickets

Create tickets for each unblock/setup task that blocks the milestone,
instrumentation, memory sync, notifications, or feedback loops.

| Ticket | Type | Human Step | Enables | Fallback |
| --- | --- | --- | --- | --- |
| `tickets/TASK-XXXX-unblock-*.md` | unblock |  |  |  |

## Goal Advisor Handoff

- `files:`
- `task:`
- `trigger:` active_goal / heartbeat / feedback_loop / rollout / batch_goal / direct
- `budget:`
- `metric_provider:`
- `drift_policy:`
- `side_effect_gates:`
- `stop_conditions:`
- `prompt_or_next_action:`

## Optional Inventory Views

Use these only when the program becomes hard to audit.

### Capability Map

| Capability | Program Node | Existing Skill / Tool | Required Input | Status | Decision |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | ready / needs_config / needs_access / needs_operator_setup / needs_reference / needs_eval / needs_wrapper / missing / defer |  |

### Missing Systems

| System | Program Node | Evidence | Action | Owner |
| --- | --- | --- | --- | --- |
|  |  |  | use_existing / deep_init_project / create_ticket / goal_advisor_handoff / defer |  |

## Review

- `metric_honesty_check:`
- `grounding_check:`
- `hidden_autonomy_check:`
- `next_strategy_refresh:`
- `next_action:`
