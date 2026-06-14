---
kind: project-harness
status: draft
created_at: TODO
project_id: TODO
automation_status: preview
---

# Project Harness

## Harness Program

```harness-program
project "TODO" {
  values: [
    impact.medium,
    loyal_users.medium,
    trust.high,
    money.medium,
    efficiency.medium
  ]

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
    heartbeat: weekly_strategy_refresh
  }

  axis activate_first_value {
    bet: "TODO: what is first value?"
    kpi: review_metric("first-value clarity")
    evidence: ref("TODO")
    heartbeat: weekly_strategy_refresh
  }

  axis retain_loyalty {
    bet: "TODO: why would they return?"
    kpi: human_feedback("would return / would not return")
    evidence: ref("TODO")
    heartbeat: weekly_strategy_refresh
  }

  axis efficiency_capability {
    bet: "TODO: what can be made easier or more repeatable?"
    kpi: learning_metric("cycle-time or effort baseline")
    evidence: ref("TODO")
    heartbeat: weekly_strategy_refresh
  }

  system ticket_loop {
    status: ready
    evidence: ref("tickets/")
    action: use_existing("ticket workflow")
  }

  system feedback_collection {
    status: missing_instrumentation
    evidence: ref("TODO")
    action: create_ticket("define first feedback loop")
  }

  system analytics {
    status: missing_instrumentation
    evidence: ref("TODO")
    action: create_ticket("define first analytics baseline")
  }

  skill goal_advisor {
    status: ready
    use: "compile the current frontier or heartbeat"
  }

  skill deep_init_project {
    status: defer
    use: "create standard project systems only if missing"
  }

  heartbeat hourly_board_drain {
    trigger: "hourly or when operator is inactive"
    first: drain_proceedable_tickets
    else: idle_gap_audit
    skills: [goal_advisor, review]
    gates: [no_external_side_effects, ticket_or_goal_required_for_edits]
    output: "artifacts/heartbeat/hourly-board-drain.md"
  }

  heartbeat daily_chief_of_staff {
    trigger: "daily"
    first: summarize_opportunities_risks_blockers
    skills: [weekly_strategy_analysis, goal_advisor, review]
    gates: [no_external_side_effects]
    output: "artifacts/strategy/daily-chief-of-staff.md"
  }

  heartbeat weekly_strategy_refresh {
    trigger: "weekly"
    first: refresh_strategy_from_findings_metrics_feedback
    skills: [weekly_strategy_analysis, goal_advisor, review]
    gates: [review_before_external_side_effects]
    output: "artifacts/strategy/weekly-strategy-refresh.md"
  }

  frontier {
    task: "TODO: first evidence-producing frontier"
    route: goal_advisor
    metric: review_metric("frontier produces useful evidence")
    files: ["project-harness.md"]
    gates: [no_publish, no_spend, no_account_changes]
    stop_when: "frontier handoff is ready or blocked by missing approval/data"
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

| Capability | Program Node | Existing Skill / Tool | Status | Decision |
| --- | --- | --- | --- | --- |
|  |  |  | ready / needs_config / needs_reference / needs_eval / needs_wrapper / missing / defer |  |

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
