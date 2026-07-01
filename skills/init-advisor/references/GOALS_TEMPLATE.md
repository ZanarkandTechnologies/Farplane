---
kind: project-goals
status: draft
project: TODO
created_at: TODO
updated_at: TODO
framework_template_version: "0.4.3"
owner: horizon-advisor
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

## Value Function

| Direction | Variables |
| --- | --- |
| Maximize | TODO |
| Minimize | TODO |
| Preserve | TODO |

## Goals

Goal axes own strategic targets and interpretation. Start with honest metric
candidates even when feedback mechanisms are missing; missing mechanisms become
setup or instrumentation tickets, not reasons to omit the goal. KPI entries are
parseable target pairs with stable IDs. Metric units, chart shape, pinned
status, source, skills, commands, and update hints live in
`farplane/bindings.md` metric recipes.

```yaml
goals:
  value_delivery:
    question: What valuable outcome should compound?
    evidence_hints:
      - TODO
    smart_goals:
      - id: first_value_goal
        target: TODO measurable outcome and date
        kpis:
          - id: TODO_metric_name
            target: TODO_number
            direction: above
        interpretation: >
          TODO explain how to read this KPI for the goal. The metric recipe in
          bindings.md owns how to fetch and render it.

  quality_and_proof:
    question: How do we know the project is doing good work?
    evidence_hints:
      - proof quality
      - review results
      - regression checks
    smart_goals:
      - id: first_quality_goal
        target: TODO quality/proof threshold and date
        kpis:
          - id: TODO_quality_metric
            target: TODO_number
            direction: above
        interpretation: >
          TODO explain how this KPI prevents false progress. Record missing
          provider gaps rather than inventing metrics.
```

## Current Bets

| Bet | Horizon | Output | Proof Signal | Owner |
| --- | --- | --- | --- | --- |
| first_frontier | TODO | TODO | TODO | goal-advisor |

## Current Milestone

TODO

## Holds

- Do not store secrets in tracked config.
- Do not deploy, spend, publish, or change accounts without approval.
