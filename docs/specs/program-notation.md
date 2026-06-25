---
title: Program Notation
status: draft
owner: harness-creator
created_at: 2026-06-14
updated_at: 2026-06-15
tags:
  - farplane
  - programs
  - harness
refs:
  - docs/specs/goal-loop-contract.md
  - tickets/templates/ticket.md
  - tickets/templates/goal-loop/program.md
  - farplane/goals.md
  - skills/harness-creator/SKILL.md
---

# Program Notation

## Purpose

Standardize the vocabulary Farplane uses for executable plans, skill workflows,
Goal loop configs, project goal maps, and project harness programs.

This spec does not require every surface to use the same Markdown shape. It
defines a common intermediate notation that each surface projects into its own
role.

```text
ProgramNotation := Params + Steps + Bindings + State + Gates + Metrics
                 + Evidence + Automation + Review + Next
```

## Why This Exists

Farplane currently has several related program dialects:

- `SKILL.md` uses a checklist-driven `Todo List`.
- ticket `Program` uses compact function/pseudocode.
- Goal Packet `program.md` uses loop configuration.
- Project `farplane/goals.md` uses horizon and milestone maps.
- `harness-creator` may use transient worksheets to review split-file deltas
  before writing `farplane/harness.md`, `farplane/products.md`,
  `farplane/goals.md`, `farplane/automations.md`, or `farplane/bindings.md`.

They are not wrong, but they make it hard to see which variables are required,
which skills are bound, which actions are automatable, and which proof gates
apply.

## Core Fields

Use these field names when a program needs structured clarity.

| Field | Meaning | Required For |
| --- | --- | --- |
| `id` | Stable program, workflow, step, or automation identifier | all reusable programs |
| `intent` | Why this program exists | material programs |
| `outcome` | Desired end state | material programs |
| `milestone` | Current concrete outcome expanded enough to run | project-goals and harness programs |
| `params` | Operator, environment, data, budget, or account variables required | intake, harness, automation, Goal launch |
| `steps` | Ordered actions or workflow blocks | skills, tickets, harness programs |
| `bindings` | Skills, tools, subagents, files, and state surfaces used | all agentic programs |
| `state` | Durable files read or written | ticket, Goal, project goals, harness |
| `gates` | Approval, safety, human, legal, spend, data, and brand boundaries | all external-facing programs |
| `metrics` | Mechanical, review, human, market, learning, or hybrid signals | Goal, project-goals, experiment programs |
| `evidence` | Source refs, confidence, validation method, proof artifacts | research, review, business programs |
| `automation` | Trigger, schedule, status, prompt program, delegate, and output | heartbeat, business, recurring programs |
| `review` | QA, reviewer, drift, or human feedback policy | material programs |
| `next` | Next owner, handoff, stop, block, or replan rule | all programs |

## Canonical Block Shape

Use this for detailed program rows or generated JSON/YAML later:

```text
program_block(
  id,
  intent,
  outcome,
  params?,
  trigger?,
  steps[],
  bindings{skills?, tools?, subagents?, files?},
  state{reads[], writes[]},
  gates[],
  metrics?,
  evidence?,
  automation_status?,
  review?,
  stop_conditions?,
  next
) -> artifact + evidence + state_delta
```

## Param Shape

Params make user input transparent. Ask questions to fill params; do not treat
questions as the durable schema.

```text
param(
  name,
  type,
  required_when,
  source,
  question?,
  default?,
  validation?,
  updates[]
)
```

Recommended sources:

- `operator`
- `local_repo`
- `external_research`
- `tool_config`
- `account_or_secret`
- `market_data`
- `generated`

## Automation Shape

Automation notation is declarative unless an actual scheduler has been created.

```text
set_automation(
  id,
  status,
  trigger,
  prompt_program,
  skills[],
  delegate_to_subagent?,
  gates[],
  state{reads[], writes[]},
  output,
  metric?,
  stop_conditions?
)
```

Valid `status` values:

- `preview`: design only, not scheduled
- `ready_for_goal_advisor`: can be compiled into a Goal Packet or prompt
- `ready_after_reference`: needs a reference/rubric first
- `blocked`: missing tool, approval, account, spend, or data
- `scheduled`: live automation exists
- `future_runtime`: credible later, not useful until external state exists

## Surface Projections

### `SKILL.md`

Skill files should keep their checklist-first shape for first-load usability.
When a skill owns a reusable workflow, its `Todo List` items can be read as
`steps[]`, and its `Skill Signature` can expose params, state, routes, gates,
and fails.

Projection:

```text
SkillProgram := signature + params? + TodoList(steps) + gates + routes + fails
```

Do not force every skill into a heavy program table. Add params only when a
skill repeatedly needs user or environment variables.

### Ticket `Program`

Ticket `Program` remains the compact build plan.

Projection:

```text
TicketProgram := signature + vars(params) + program(steps) + verify(proof)
```

Use this when the work is bounded and does not need multi-turn Goal loop
configuration.

### Goal Packet `program.md`

Goal `program.md` remains loop configuration, not the task plan itself.

Projection:

```text
GoalProgram := mode + files + budget + metric_provider + after_each_turn
             + drift_policy + heartbeat_or_batch_policy + stop_conditions
```

Use this when native Goal, heartbeat, rollout, feedback, or long-running work
needs resumable loop state.

### Project `farplane/goals.md`

Project goals remain the long-horizon planning graph.

Projection:

```text
ProjectGoalsProgram := north_star + horizon_map + metrics + current_milestone
                     + holds + replan_cadence + next_goal_packet
```

Use this above Goal Packets, not as a native Goal execution loop.

Project goal branches should be feedback-sized by default:

```text
feedback_sized_project(goal, available_feedback)
  -> smallest durable project whose output can be reviewed, measured, shown, or
     exposed to user/market feedback
```

Use `starting_tasks` inside a project for obvious first moves. Create child
tickets only for real boundaries: external access/setup, human approval,
feedback collection, different owner/agent, dependency risk, proof/review state,
or an executable Goal Packet. Do not pre-split a goal map into day-level tasks
just because the next steps are imaginable.

### Project Harness Split

Project, business, content, academy, lab, ecommerce, product, and internal-ops
harnesses should lead with a program-first operator view.

Projection:

```text
ProjectHarness := static_charter + product_catalog + strategy_state
                + automation_prompts + safe_bindings + hook_config
                + tickets_or_goal_handoffs
```

Use this when a user wants to understand how an agent could run or improve a
business, content engine, funnel, project, research program, or recurring
strategy loop.

Default project harness storage is split across standard Farplane files:

- `farplane/harness.md`: YAML front matter plus Markdown static-charter
  sections.
- `farplane/products.md`: product catalog and work-lane weights.
- `farplane/goals.md`: strategy, KPIs, milestones, and current bets.
- `farplane/automations.md`: recurring Codex automation prompts.
- `farplane/bindings.md`: non-secret project coordinates.
- `farplane/hooks.json`: declarative project hook config.
- `tickets/`: missing systems, blockers, and executable work.

Canonical `farplane/harness.md` files should not use fenced
`harness-program` blocks. Use Markdown headings and tables for human review and
simple UI parsing. A transient worksheet may still use compact pseudocode when
it helps review a proposed split-file delta, but the standard files are the
source of truth. Split to Goal Packet files only when a current milestone is
ready to run.

`HarnessIL` and `Harness DSL` are legacy internal aliases. Prefer **project
harness** or **split-file harness** in operator-facing docs.

The `values` block is the project constitution:

```text
values {
  mission: string
  operating_principles: string[]
  priorities: weighted_value[]
  non_tradeoffs: string[]
}
```

Goals, KPIs, strategy axes, tickets, and heartbeats should be derived from
these values, but they belong in the split files that own them rather than in a
single charter program block.

## Project Harness Backbone

Project harnesses should express the backbone as callable steps with explicit
params. The agent can then infer which params are missing before each step and
ask, inspect local state, use a template, or research only where useful.

```text
project_harness_creator(
  project_idea,        // required: initial operator idea
  values?,             // mission, operating principles, priorities, non-tradeoffs
  priorities?,         // money, users, loyalty, impact, learning, trust, etc.
  mode_presets?,       // business, channel, academy, lab, ecommerce, ...
  known_context?,
  constraints?
) -> harness_program + evidence_wrapper + proposed_tickets + current_milestone + goal_advisor_handoff

bind_values(project_idea, values?, constraints?)
  -> mission + operating_principles + priorities + non_tradeoffs
   + missing_operator_params

select_mode_presets(project_idea, priorities?, mode_presets?)
  -> presets + default_axes + default_kpis + default_heartbeats

ground_domain_if_needed(project_idea, presets, known_context)
  -> domain_model + method_brief + evidence_refs + skipped_research_reason?

build_strategy_state(values, priorities, presets, domain_model)
  -> axes + strategy_state[] + kpi_map + metric_providers

define_feedback_loop_skills(axes, kpi_map, metric_providers, available_skills)
  -> feedback_skills + required_inputs + unblock_or_build_tickets

map_systems_skills_and_tickets(strategy_state, local_repo, available_skills)
  -> skills + missing_systems + tickets + init_advisor_routes

define_scrum_heartbeats(project_harness, active_tickets?, goal_packets?)
  -> ticket_update + weekly_pm_update + update_system_gaps
   + daily_chief_of_staff

select_current_milestone(project_harness, budget?, gates?)
  -> current_milestone + goal_advisor_handoff + stop_conditions

review_and_improve(project_harness, evidence_refs, operator_feedback?)
  -> pass_revise_block + next_program_delta + next_missing_param
```

This backbone should be adapted per domain, but it should not reinvent standard
systems. Use templates for ticket loops, docs, QA/evidence paths, feedback
collection, analytics/instrumentation, and strategy review unless the project
is genuinely doing R&D.

### Strategy State Shape

```text
strategy_state(
  axis,
  value_weight,
  current_bet,
  KPI,
  metric_provider,
  metric_confidence,
  evidence,
  anti_metric,
  heartbeat,
  update_rule,
  approval_gates
)
```

Metric providers:

```text
live_metric | proxy_metric | review_metric | human_feedback
| market_signal | learning_metric | missing_instrumentation
```

Mark absent metrics as `missing_instrumentation` and route to a concrete
feedback skill plus an unblock/configure/build ticket instead of analyzing
absent data.

### Feedback Loop Skills

Every project harness must define at least one honest init-time feedback loop.
The loop can be primitive, such as operator labels or review metrics, but it
must be explicit before strategy refinement claims begin.

Model feedback loops as concrete skills with required inputs:

```text
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
}
```

Rule:

```text
feedback_needed
  -> skill(specific_feedback_capability, requires)
  -> ticket(type: unblock | type: build_skill | type: configure)
```

Avoid vague tasks like "create feedback loop". Name the capability first:
`instagram_attention_graph`, `youtube_retention_metrics`,
`posthog_activation_funnel`, `operator_usefulness_labels`,
`customer_interview_pattern_reader`, or `sales_call_objection_miner`.

### Skills, Required Inputs, And Operator Unblocks

Standardize external data, notifications, shared team systems, and account
access as `skill` capabilities with required inputs inside the relevant skill,
binding, product, or strategy surface. Do not add another top-level abstraction
unless pilots prove that skills cannot express the need.

```text
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
```

Rule:

```text
external_need
  -> skill(capability, requires)
  -> ticket(type: unblock)
```

The harness program stays structured. Human setup work lives in tickets.

### Scrum Heartbeat Shape

```text
daily_ticket_drainer(ticket_sources, bindings, gates, ranking_policy)
  -> selected_ticket | no_op_report
  -> impl_plan_result + goal_advisor_execution + evidence_or_blocker

weekly_pm_update(grouped_jobs, reports, ledger, goals, tickets, metrics, memory)
  -> weekly_pm_report + ticket_board_delta + memory_delta
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

update_system_gaps(project_files, current_state)
  -> missing_system_ticket | prep_artifact | review_request | no_op

daily_chief_of_staff(project_files, progress, signals)
  -> opportunities + risks + blockers + recommended_next_actions
```

Default to explicit Pulse and Interval automations first:

```text
automation pulse {
  schedule: every 30 minutes by default
  first: reconcile_outcomes
  then: select_one_bounded_action_or_refill_ticket
  reads: farplane/harness.md + farplane/products.md + farplane/goals.md + tickets
}

automation interval {
  schedule: daily or weekly by project prompt
  first: report(review_window)
  then: plan(planning_window)
  reads: farplane/harness.md + farplane/products.md + farplane/goals.md + reports
  writes: dated interval report + proposed deltas + tickets or Goal handoffs
}
```

Pulse executes one proceedable action or creates one grounded refill ticket.
Interval reports on a bounded review window, checks drift against the static
charter and goals, and plans the next bounded window. Live scheduling requires
explicit automation approval in the Codex app.

Use `delegate(context_ref, task_prompt, skills?, output?)` when a PM heartbeat
can split work into a bounded subagent lane. `context_ref` must point to a
file, ticket, Goal Packet, or artifact; the task prompt should name the skills
the lane may use and the output path it must write.

### Missing Param Backpropagation

```text
required_params(next_step)
  -> missing_params
  -> fill_from_context | fill_from_local_repo | fill_from_research | ask_operator
  -> updated_params
  -> run(next_step)
```

Ask the operator only for taste, intent, risk, private context, permissions,
budgets, and success definitions. Use local search or research for discoverable
facts such as methods, competitors, peer workflows, and available repo assets.

### Split-File Example

```text
farplane/harness.md:
  mission: "Teach practical AI and harness engineering so serious builders become more capable."
  human thesis: "The channel teaches from real work and preserves trust over shallow reach."
  non-tradeoffs: ["do not publish unreviewed claims", "do not optimize revenue before usefulness"]

farplane/products.md:
  team: "AI engineering education lab"
  products: ["episodes", "case studies", "tooling walkthroughs"]
  work_lanes: ["episode_experiments", "proof_and_quality", "distribution"]

farplane/goals.md:
  axis reach_acquire:
    question: "Can high-signal AI engineering learners find this?"
    kpi: review_metric("hook/title clarity")
    missing_signal: instagram_attention_graph
  current_milestone:
    output: "Choose first pilot episode"
    metric: review_metric
    gates: [no_publish, no_spend]

farplane/bindings.md:
  safe coordinates: channel URLs, dashboard labels, non-secret account aliases

tickets/:
  instagram_insights_export:
    type: unblock
    human_step: "Connect read-only metrics access or provide a CSV export"
    fallback: "operator ranks recent posts manually"
```

## Blast Radius

Standardizing notation affects these surfaces:

| Surface | Current Shape | Change Needed | Risk |
| --- | --- | --- | --- |
| `skills/*/SKILL.md` | checklist plus signatures | Add optional params/state/gate clarity to relevant skills only | Low if optional |
| `tickets/templates/ticket.md` | compact task program | Rename `vars` guidance toward `params` and align field names | Medium; many tickets follow this |
| `tickets/templates/goal-loop/program.md` | loop config | Add cross-reference to this spec; keep field shape | Low |
| `farplane/goals.md` | horizon map | Add cross-reference and field vocabulary | Low |
| `skills/harness-creator/templates/*` | harness/capability/handoff templates | Keep worksheets split-file oriented; do not make fenced DSL canonical | Medium; direct user-facing impact |
| `impl-plan` skill | ticket planning guidance | Reference common notation but keep coding-ticket projection | Low |
| `goal-advisor` skill | Goal architecture guidance | Clarify that it compiles selected blocks, not whole parent programs | Low |
| validators | mostly unrelated today | Optional future check for required sections in templates | Medium if enforced |
| existing tickets | mixed legacy formats | Do not rewrite historical tickets | Low if forward-only |

## Migration Plan

1. Adopt this spec as a draft vocabulary.
2. Keep `project-harness.md` as an optional transient worksheet, not a
   canonical project file.
3. Update `harness-creator` first-load checklist to require values,
   priorities, metric-provider honesty, Scrum heartbeats, and Goal Advisor
   milestones for project/business/content harnesses.
4. Update `tickets/templates/ticket.md` to mention `params` as the preferred
   name while preserving `vars` compatibility.
5. Add short links from Goal loop templates to this spec.
6. Update `impl-plan` and `goal-advisor` docs to use the projection terms.
7. After two pilots, decide whether to add more validators for required
   Markdown sections or table columns in split files.

## Non-Goals

- No new runtime scheduler.
- No hidden automation.
- No new top-level external-IO abstraction for v1; use skill capabilities plus
  required inputs and tickets.
- No immediate rewrite of all existing skills or tickets.
- No requirement that every small skill use a heavy program table.
- No replacement for `goal-loop-contract.md`; this spec complements it.

## Open Questions

- Should `set_automation(...)` remain pseudocode, or become a typed schema only
  after the Codex automation tool is used repeatedly?

Resolved for now:

- Primary harness output is the standard split-file set:
  `farplane/harness.md`, `farplane/products.md`, `farplane/goals.md`,
  `farplane/automations.md`, `farplane/bindings.md`, `farplane/hooks.json`, and
  tickets.
- Canonical `farplane/harness.md` uses YAML front matter plus Markdown
  sections. Fenced `harness-program` DSL is retired for canonical project
  harness files.
- Markdown tables are acceptable source views when their columns are stable and
  validator-backed.
