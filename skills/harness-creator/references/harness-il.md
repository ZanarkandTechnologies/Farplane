---
title: Harness Program Notation
owner: harness-creator
status: legacy
created_at: 2026-06-14
updated_at: 2026-06-14
aliases:
  - HarnessIL
  - Harness DSL
---

# Harness Program Notation

This file documents the legacy compact Harness Program notation. Do not use it
as the default authoring shape for canonical Farplane project files.

The canonical project state is split across standard Farplane files:

```text
harness_creator(input)
  -> farplane/harness.md static-charter delta
   + farplane/harness.md stable capability-ref delta
   + farplane/goals.yaml strategy delta
   + optional project-harness.md transient worksheet
```

Use YAML front matter plus Markdown sections for canonical files. Use this
legacy notation only when reading older worksheets, migrating old examples, or
capturing a quick transient review sketch that will be projected back into the
standard files. Do not treat `project-harness.md` as a canonical replacement for
`farplane/harness.md`.

## Shape

````markdown
# Project Harness

```harness-program
project "Name" {
  values {
    mission: "Help a specific audience reach a meaningful outcome"
    operating_principles: [
      "teach from real work, not recycled theory",
      "make claims auditable"
    ]
    priorities: [impact.high, loyal_users.high, trust.high, money.low]
    non_tradeoffs: [
      "do not publish unreviewed claims",
      "do not optimize revenue before usefulness"
    ]
  }

  modes: [channel, academy]

  axis reach_acquire {
    bet: "Who should find this first?"
    kpi: review_metric("hook/title clarity")
    evidence: ref("research/channel-examples.md")
    heartbeat: weekly_interval
  }

  system analytics {
    status: missing_instrumentation
    action: ticket(instagram_insights_export)
  }

  skill instagram_attention_graph {
    status: needs_access
    requires: [instagram_insights_export]
    use: "read attention graph, retention, replay, save, share, and comment signals"
  }

  ticket instagram_insights_export {
    type: unblock
    human_step: "Connect read-only metrics access or provide a CSV export"
    enables: [instagram_attention_graph]
    fallback: human_feedback("rank recent posts manually")
  }

  heartbeat pulse_update {
    first: reconcile_outcomes
    else: select_one_bounded_action
    gates: [no_external_side_effects]
  }

  heartbeat rhythm_update {
    first: update_day_range_plan
    else: ticket_drainer
    gates: [no_external_side_effects]
  }

  heartbeat weekly_interval {
    first: update_strategy
    skills: [weekly_strategy_analysis, skill_maintenance, goal_advisor, review]
    delegate: delegate(ref("farplane/goals.yaml"), "refresh strategy and skill upkeep", skills=[interval_update, skill_maintenance])
    output: "artifacts/strategy/interval-update.md"
  }

  milestone first_episode_selection {
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
  values_block
| modes_stmt
| goal_stmt
| axis_block
| system_block
| skill_block
| ticket_block
| heartbeat_block
| milestone_block
| gate_stmt

values_block :=
  values "{"
    mission
    operating_principles?
    priorities
    non_tradeoffs?
  "}"
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
    requires?
    use?
    action?
  "}"

ticket_block :=
  ticket ident "{"
    type
    task?
    human_step?
    why?
    enables?
    acceptable_alternatives?
    fallback?
    gates?
  "}"

heartbeat_block :=
  heartbeat ident "{"
    trigger?
    first?
    else?
    skills?
    delegate?
    gates?
    output?
  "}"

milestone_block :=
  milestone ident "{"
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

Values are the project constitution. They sit above goals, KPIs, tickets, and
heartbeats. Use them to encode why the project exists, how it should behave,
what it optimizes for, and what it refuses to trade away.

```text
mission: string
operating_principles: string[]
priorities: weighted_value[]
non_tradeoffs: string[]
```

Priority atoms:

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

### Feedback-Sized Projects

When a harness produces or updates project goals, use projects as the
default durable unit.

```text
feedback_sized_project(goal, available_feedback)
  -> smallest durable project whose output can be reviewed, measured, shown, or
     exposed to user/market feedback
```

Use `starting_tasks` for obvious local moves inside the project. Create child
tickets only when a real boundary needs durable state: execution, unblock,
human approval, review, dependency, external access/setup, or proof.

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

### Metric Recipes

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

### Feedback Loops

Every initialized project needs at least one honest feedback loop before it can
claim refinement. Model feedback loops as concrete skills, not vague tasks.

```harness-program
skill instagram_attention_graph {
  status: needs_access
  requires: [instagram_insights_export]
  use: "read attention graph, retention, replay, save, share, and comment signals"
}

ticket instagram_insights_export {
  type: unblock
  human_step: "Connect read-only metrics access or provide a CSV export"
  why: "Strategy cannot improve against Instagram feedback until the signal exists"
  enables: [instagram_attention_graph]
  fallback: human_feedback("operator ranks recent posts manually")
  gates: [no_account_changes]
}
```

Rule:

```text
feedback_needed
  -> skill(specific_feedback_capability, requires)
  -> ticket(type: unblock | type: build_skill | type: configure)
```

Good feedback skills are concrete: `instagram_attention_graph`,
`youtube_retention_metrics`, `posthog_activation_funnel`,
`operator_usefulness_labels`, `customer_interview_pattern_reader`, or
`sales_call_objection_miner`.

### System Status

```text
ready
partial
missing
missing_instrumentation
needs_config
needs_access
needs_operator_setup
needs_reference
needs_eval
defer
```

### Actions

```text
use_existing("skill_or_system")
init_advisor("missing_standard_systems")
create_ticket("task")
ticket(identifier)
delegate(context_ref, task_prompt, skills?, output?)
goal_advisor_handoff("milestone")
create_skill_candidate("stable_repeated_trigger")
add_reference("path_or_topic")
add_eval("claim")
defer_until_pilot("reason")
no_op("reason")
```

### Skills As Capability Bindings

Use `skill` for capabilities, including access to external tools or data. Do
not add a separate external-IO block unless pilots prove a real need.

```harness-program
skill notion_memory_sync {
  status: needs_operator_setup
  requires: [notion_database_access]
  use: "sync shared project memory and ticket state"
}
```

The required input may be a credential, export, account connection, permission,
approval, data file, or human feedback source.

### Tickets

Use `ticket` for one-time work, setup, access, approval, and unblock tasks.
The program should propose tickets rather than inventing extra sidecar files.

```harness-program
ticket notion_database_access {
  type: unblock
  human_step: "Kenji grants access or links the shared Notion database"
  why: "The project PM cannot sync shared memory or ticket state without it"
  enables: [notion_memory_sync]
  acceptable_alternatives: ["manual export", "local-only memory until setup"]
  gates: [no_account_changes]
}
```

Default rule:

```text
blocker
  -> ticket(type: unblock)
   + fallback_until_unblocked
```

### Heartbeats

```text
pulse_update
rhythm_update
weekly_interval
ticket_drainer
update_system_gaps
update_strategy
update_memory
skill_maintenance.harden_skill
skill_maintenance.refine_skill
delegate
```

Default policy:

```text
heartbeat pulse_update {
  first: reconcile_outcomes
  then: check_drift_against_active_task_and_rhythm_plan
  then: select_one_bounded_action
}

heartbeat rhythm_update {
  first: check_drift_against_horizon_plan
  then: rank_day_range_lanes
  optional: ticket_drainer
}

heartbeat ticket_drainer {
  first: fetch_local_tickets
  bindings: "farplane/bindings.yaml"
  optional: fetch_notion_when_enabled_bound_and_local_empty
  then: rank_one_ticket -> impl-plan -> goal-advisor
}

heartbeat weekly_interval {
  first: grouped_jobs_with_report_cache
  bindings: "farplane/bindings.yaml"
  skills: [feed_scout, update_memory, update_strategy, skill_maintenance, goal_advisor, review]
  delegate: delegate(ref("farplane/goals.yaml"), "refresh strategy and skill upkeep", skills=[interval_update, skill_maintenance])
}
```

Default project automation standard:

```text
ticket_drainer(ticket_sources, gates, ranking_policy)
  -> selected_ticket | no_op_report
  -> impl_plan_result + goal_advisor_execution + evidence_or_blocker

weekly_interval(grouped_jobs, reports, ledger, goals, tickets, metrics, memory)
  -> drift_check + horizon_report + scheduled_action_results + ticket_board_delta + memory_delta
   + skill_improvement_delta + blockers

update_strategy(project_goals, tickets, progress, metrics_or_feedback)
  -> strategy_delta + system_gaps + experiments + ticket_deltas

update_memory(history, memory, readme, docs, recent_progress)
  -> consolidated_memory + readme_delta + docs_delta
   + docs_consolidation_plan? + stale_context_notes

skill_maintenance.harden_skill(skill, lessons, troubles)
  -> new_evals + gotchas + regression_cases + improvement_tickets

skill_maintenance.refine_skill(skill, evals, gotchas, usage_results)
  -> skill_delta + consolidated_evals + consolidated_gotchas + review_notes

delegate(context_ref, task_prompt, skills?, output?)
  -> subagent_handoff + evidence_ref
```

Use `delegate(...)` when a heartbeat can safely split bounded work into a
subagent lane. The `context_ref` must be a file or ticket path, not hidden chat
memory; the task prompt names required skills and expected output.

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
- Define one concrete feedback skill at init time. If it cannot run yet, add
  the precise unblock/configure/build ticket that would make it usable.
- Use `skill` nodes for external systems and data access requirements; the
  skill describes the capability, and `requires` names the missing human or
  environment input.
- Use `ticket { type: unblock }` for human setup, credentials, data exports,
  approval, account linking, and shared-system access.
- Use `init_advisor(...)` for standard project systems instead of
  rediscovering docs, tickets, QA, runtime commands, feedback loops, or
  bootstrap files.
- Use `research:*` only when domain truth is uncertain and the research changes
  the current milestone.
- Keep publishing, spend, account edits, customer contact, gated scraping, and
  brand/legal-sensitive actions behind explicit gates.

## Output Rule

Write durable output to the split Farplane files. A worksheet may explain the
proof before those deltas are accepted:

```text
farplane/harness.md :=
  static human charter sections + stable capability refs

farplane/goals.yaml :=
  strategy, KPIs, current bets, milestone, and holds

project-harness.md :=
  optional transient worksheet
+ target file deltas
+ evidence
+ assumptions
+ open questions
+ Goal Advisor handoff
```

Do not generate a giant table-first harness unless the operator asks for an
inventory view. Tables are sidecars; the program is the compact source.
