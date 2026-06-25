---
kind: harness-creator-worksheet
status: draft
created_at: TODO
updated_at: TODO
template_id: project-harness
template_version: "0.3.0"
feature_refs:
  - FEAT-0027
  - FEAT-0048
project_id: TODO
automation_status: preview
framework_template_version: "0.2.0"
canonical_targets:
  - farplane/harness.md
  - farplane/products.md
  - farplane/goals.md
  - farplane/automations.md
  - farplane/bindings.md
---

# Harness Creator Worksheet

This is a transient planning worksheet. It is not a canonical project charter
and must not replace `farplane/harness.md`.

Use it to review proposed split-surface deltas before writing the standard
Farplane files:

- `farplane/harness.md` owns the static human charter: mission, human thesis,
  operating principles, non-tradeoffs, static leverage commitments, agent
  authority, systems, and change rule.
- `farplane/products.md` owns the dynamic product catalog and Pulse refill
  context.
- `farplane/goals.md` owns dynamic strategy, KPIs, current frontier, and Goal
  Advisor handoffs.
- `farplane/automations.md` owns reviewable automation prompt text.
- `farplane/bindings.md` owns non-secret project coordinates.

## Static Charter Delta

Target: `farplane/harness.md`

Approval required before applying changes to the human thesis, durable leverage
commitments, non-tradeoffs, agent authority, or change rule.

## Mission

TODO: why this project or business exists.

## Human Thesis

TODO: durable human thesis the agents must preserve.

## Operating Principles

- TODO: principle that should guide repeated decisions.

## Static Leverage Commitments

| Commitment | Why It Compounds | Evidence To Seek | Pivot Signal |
| --- | --- | --- | --- |
| TODO | TODO | TODO | TODO |

## Non-Tradeoffs

- TODO: what cannot be sacrificed for local wins.

## Agent Authority

- Agents may evolve products, audiences, tickets, and goals through
  evidence-backed deltas.
- Agents may challenge the static thesis with evidence.
- Agents may propose a charter delta in a dated interval report.
- Agents may not silently rewrite the static thesis or durable leverage
  commitments.

## Change Rule

Static charter changes require an explicit human-approved harness delta.
Interval reports may propose the delta, but cannot apply it silently.

## Charter-Level Operating Loop

```text
TODO signal
  -> TODO investigation or experiment
  -> TODO evidence artifact
  -> TODO product or process update
  -> TODO feedback signal
  -> TODO next selection rule
```

## Product Catalog Delta

Target: `farplane/products.md`

Use this section for the team archetype, operating flywheel, primary products,
supporting products, autonomous project types, selection notes, and Pulse refill
guidance. Do not put these dynamic product decisions in `farplane/harness.md`.

| Product | Audience | Artifact Examples | Reward Signals | Owner Skills |
| --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO |

## Strategy Delta

Target: `farplane/goals.md`

Use this section for goals, axes, KPIs, current frontier, holds, strategy
deltas, and Goal Advisor handoffs. Strategy must stay inside the static charter
but is not itself the charter.

```goal-program
goal north_star {
  outcome: "TODO"
  metric: learning_metric("first honest baseline")
  horizon: "TODO"
}

axis TODO {
  question: "TODO"
  kpi: missing_instrumentation("TODO")
  current_signal: ref("TODO")
}

project current_frontier {
  output: "TODO: first evidence-producing milestone"
  feedback_surface: review_metric("TODO")
  route: goal_advisor
  gates: [no_publish, no_spend, no_account_changes]
}
```

## Automation And Binding Delta

Targets: `farplane/automations.md`, `farplane/bindings.md`

- `automation_delta:`
- `safe_binding_delta:`
- `activation_status:` preview / needs_operator_setup / ready_for_automation_advisor
- `side_effect_gates:`

## Evidence

- `facts:`
- `research_refs:`
- `local_refs:`
- `operator_inputs:`
- `metric_sources:`

## Assumptions

- `inferred_values:`
- `inferred_products:`
- `inferred_goals:`
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
|  |  |  | use_existing / init_advisor / create_ticket / goal_advisor_handoff / defer |  |
