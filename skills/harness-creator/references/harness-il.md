---
title: Harness Program Notation
owner: harness-creator
status: draft
created_at: 2026-06-14
updated_at: 2026-06-14
aliases:
  - HarnessIL
  - Harness DSL
---

# Harness Program Notation

Use **Harness Program** as the operator-facing name.

`HarnessIL` and `Harness DSL` are acceptable internal aliases, but avoid making
the operator choose or read those names. The useful artifact is the program:

```text
harness_creator(input) -> project-harness.md containing one harness-program block
```

The harness program is the compressed, executable-looking core of the project
or business harness. Markdown around it is only for evidence, assumptions,
notes, and review.

## Shape

````markdown
# Project Harness

```harness-program
project "Name" {
  values: [impact.high, loyal_users.high, trust.high, money.low]
  modes: [channel, academy]

  axis reach_acquire {
    bet: "Who should find this first?"
    kpi: review_metric("hook/title clarity")
    evidence: ref("research/channel-examples.md")
    heartbeat: weekly_strategy_refresh
  }

  system analytics {
    status: missing_instrumentation
    action: create_ticket("define first metrics")
  }

  heartbeat hourly_board_drain {
    first: drain_proceedable_tickets
    else: idle_gap_audit
    gates: [no_external_side_effects]
  }

  frontier {
    task: "Choose first pilot episode"
    route: goal_advisor
    metric: review_metric
    gates: [no_publish, no_spend]
  }
}
```

## Evidence

- `facts:`
- `assumptions:`
- `research_refs:`
- `open_questions:`
````

## Grammar

Keep the language tiny. It is a notation, not a real runtime.

```text
harness_program :=
  project_block

project_block :=
  project string "{" project_stmt* "}"

project_stmt :=
  values_stmt
| modes_stmt
| goal_stmt
| axis_block
| system_block
| skill_block
| heartbeat_block
| frontier_block
| gate_stmt

values_stmt := values ":" "[" weighted_value* "]"
modes_stmt := modes ":" "[" mode* "]"
goal_stmt := goal ident "{" outcome metric? horizon? "}"

axis_block :=
  axis ident "{"
    bet
    kpi
    evidence?
    anti_metric?
    heartbeat?
    gate_stmt?
  "}"

system_block :=
  system ident "{"
    status
    evidence?
    action
    owner?
  "}"

skill_block :=
  skill ident "{"
    status
    use?
    action?
  "}"

heartbeat_block :=
  heartbeat ident "{"
    trigger?
    first?
    else?
    skills?
    gates?
    output?
  "}"

frontier_block :=
  frontier "{"
    task
    route
    metric
    files?
    gates?
    stop_when?
  "}"
```

## Vocabulary

### Values

```text
impact.high
money.high
user_count.medium
loyal_users.high
learning.high
trust.high
quality.high
efficiency.medium
```

### Modes

```text
business | channel | academy | lab | research | community
| product | ecommerce | internal_ops
```

### Axes

```text
reach_acquire
activate_first_value
retain_loyalty
refer_share
monetize_resources
impact_mission
deliver_quality
efficiency_capability
learning_evidence
risk_trust
```

### Metric Providers

```text
live_metric("signal")
proxy_metric("signal")
review_metric("rubric_or_question")
human_feedback("label_or_question")
market_signal("signal")
learning_metric("hypothesis")
missing_instrumentation("system_needed")
```

Do not analyze data that does not exist. Use `missing_instrumentation(...)`
and create a system action.

### System Status

```text
ready
partial
missing
missing_instrumentation
needs_config
needs_reference
needs_eval
defer
```

### Actions

```text
use_existing("skill_or_system")
deep_init_project("missing_standard_systems")
create_ticket("task")
goal_advisor_handoff("frontier")
create_skill_candidate("stable_repeated_trigger")
add_reference("path_or_topic")
add_eval("claim")
defer_until_pilot("reason")
no_op("reason")
```

### Heartbeats

```text
hourly_board_drain
idle_gap_audit
daily_chief_of_staff
weekly_strategy_refresh
```

Default policy:

```text
heartbeat hourly_board_drain {
  first: drain_proceedable_tickets
  else: idle_gap_audit
}
```

### Gates

```text
no_publish
no_spend
no_account_changes
no_customer_contact
no_private_scraping
no_legal_or_brand_sensitive_action
review_before_external_side_effects
ticket_or_goal_required_for_edits
```

## Grounding Rules

- Put facts in `evidence: ref("path")`, not free-floating claims.
- Mark guesses as assumptions in the Markdown evidence wrapper.
- Use `missing_instrumentation(...)` for absent metrics.
- Use `deep_init_project(...)` for standard project systems instead of
  rediscovering docs, tickets, QA, runtime commands, feedback loops, or
  bootstrap files.
- Use `research:*` only when domain truth is uncertain and the research changes
  the first frontier.
- Keep publishing, spend, account edits, customer contact, gated scraping, and
  brand/legal-sensitive actions behind explicit gates.

## Output Rule

The harness program is the output. Sidecar Markdown sections explain the proof:

```text
project-harness.md :=
  YAML front matter
+ harness-program block
+ Evidence
+ Assumptions
+ Open Questions
+ Goal Advisor Handoff
```

Do not generate a giant table-first harness unless the operator asks for an
inventory view. Tables are sidecars; the program is the compact source.
