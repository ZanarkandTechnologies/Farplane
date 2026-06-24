---
kind: project-goals
status: draft
project: TODO
created_at: TODO
updated_at: TODO
framework_template_version: "0.2.0"
owner: project-pm-automation
---

# Project Goals

## Intake Required

This file is not ready until the operator has answered:

- What should this project reliably do over the next 3 months?
- What would prove that it is working?
- What should agents not do autonomously?
- What is the first milestone worth executing?

Until those answers are captured, report `needs_goal_intake` rather than
`project_initialized`.

## North Star

TODO

## Goal Program

The fenced `goal-program` block is the parseable source for graphing goals,
metrics, project frontiers, and milestones. Keep explanatory prose in Markdown;
keep machine-readable goal structure in this block.

```goal-program
values_ref: farplane/harness.md
automation_ref: farplane/automations.md
bindings_ref: farplane/bindings.md

goal project_north_star {
  horizon: "quarter"
  outcome: "TODO: durable outcome this project should create."
  metric: review_metric("TODO: what would prove the outcome is working")
  anti_metric: "TODO: behavior that would look productive but violates the goal"
  proof: [farplane/goals.md, tickets/, .farplane/reports/interval/]
}

value_function project_value {
  maximize: [
    accepted_output,
    validated_learning,
    user_or_operator_value
  ]
  minimize: [
    human_intervention_minutes,
    false_completion_incidents,
    source_gap_rate,
    context_loss
  ]
  hold_constant: [
    safety,
    operator_control,
    proof_quality,
    privacy
  ]
}

axis value_delivery {
  question: "What valuable outcome should compound?"
  kpi: review_metric("TODO: accepted evidence of value")
  current_signal: missing("goal intake required")
}

axis quality_and_proof {
  question: "How do we know the project is doing good work?"
  kpi: review_metric("TODO: proof bundle or acceptance signal")
  current_signal: missing("proof surface not configured")
}

project first_frontier {
  parent: project_north_star
  output: "TODO: first feedback-sized project frontier."
  feedback_surface: review_metric("TODO: review, eval, usage, or operator signal")
  gates: [
    no_secrets_in_tracked_files,
    approval_required_for_spend_deploy_publish_account_changes
  ]
}

milestone first_milestone {
  task: "TODO: first milestone worth executing."
  metric: review_metric("TODO: done/proof signal")
  route: goal-advisor
  gates: [operator_approval_if_material]
}
```

## Operating Priorities

1. TODO

## Current Milestone

TODO

## Holds

- Do not store secrets in tracked config.
- Do not deploy, spend, publish, or change accounts without approval.

## Goal Advisor Handoff

Use `goal-advisor` when the current milestone becomes executable enough to run
as a ticket-backed Goal Packet.
