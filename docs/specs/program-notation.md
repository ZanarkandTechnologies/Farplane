---
title: Program Notation
status: draft
owner: harness-creator
created_at: 2026-06-14
updated_at: 2026-06-14
tags:
  - farplane
  - programs
  - harness
refs:
  - docs/specs/goal-loop-contract.md
  - tickets/templates/ticket.md
  - tickets/templates/goal-loop/program.md
  - tickets/templates/goal-loop/portfolio.md
  - skills/harness-creator/SKILL.md
---

# Program Notation

## Purpose

Standardize the vocabulary Farplane uses for executable plans, skill workflows,
Goal loop configs, portfolio maps, and project harness programs.

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
- Goal Portfolio `portfolio.md` uses horizon and frontier maps.
- harness-creator `project-harness.md` combines values, goals, KPIs, strategy
  axes, heartbeat previews, skill gaps, and Goal Advisor handoffs.

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
| `frontier` | First evidence-producing branch expanded enough to run | portfolio and harness programs |
| `params` | Operator, environment, data, budget, or account variables required | intake, harness, automation, Goal launch |
| `steps` | Ordered actions or workflow blocks | skills, tickets, harness programs |
| `bindings` | Skills, tools, subagents, files, and state surfaces used | all agentic programs |
| `state` | Durable files read or written | ticket, Goal, portfolio, harness |
| `gates` | Approval, safety, human, legal, spend, data, and brand boundaries | all external-facing programs |
| `metrics` | Mechanical, review, human, market, learning, or hybrid signals | Goal, portfolio, experiment programs |
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

### Goal Portfolio `portfolio.md`

Portfolio remains the long-horizon planning graph.

Projection:

```text
PortfolioProgram := north_star + horizon_map + metrics + frontier
                  + holds + replan_cadence + next_goal_packet
```

Use this above Goal Packets, not as a native Goal execution loop.

### Harness Program

Project, business, content, academy, lab, ecommerce, product, and internal-ops
harnesses should lead with a program-first operator view.

Projection:

```text
HarnessProgram := values + goal_weights + mode_presets + goals + axes
                + strategy_state + kpi_map + heartbeat_preview
                + skill_gap_map + missing_systems + current_frontier
                + goal_advisor_handoff
```

Use this when a user wants to understand how an agent could run or improve a
business, content engine, funnel, project, research program, or recurring
strategy loop.

Default storage is one Markdown file with YAML front matter and one fenced
`harness-program` block. Use Markdown around the block for evidence,
assumptions, open questions, review, and optional inventory tables. Split to
Goal Packet files only when a current frontier is ready to run.

`HarnessIL` and `Harness DSL` are internal aliases. Prefer **Harness Program**
in operator-facing docs.

## Project Harness Backbone

Project harnesses should express the backbone as callable steps with explicit
params. The agent can then infer which params are missing before each step and
ask, inspect local state, use a template, or research only where useful.

```text
project_harness_creator(
  project_idea,        // required: initial operator idea
  values?,             // operator-supplied or inferred with confidence marker
  goal_weights?,       // money, users, loyalty, impact, learning, trust, etc.
  mode_presets?,       // business, channel, academy, lab, ecommerce, ...
  known_context?,
  constraints?
) -> harness_program + evidence_wrapper + current_frontier + goal_advisor_handoff

bind_values(project_idea, values?, constraints?)
  -> values + non_tradeoffs + anti_values + missing_operator_params

select_mode_presets(project_idea, goal_weights?, mode_presets?)
  -> presets + default_axes + default_kpis + default_heartbeats

ground_domain_if_needed(project_idea, presets, known_context)
  -> domain_model + method_brief + evidence_refs + skipped_research_reason?

build_strategy_state(values, goal_weights, presets, domain_model)
  -> axes + strategy_state[] + kpi_map + metric_providers

map_systems_and_skills(strategy_state, local_repo, available_skills)
  -> missing_systems + skill_gap_map + deep_init_project_routes

define_scrum_heartbeats(project_harness, active_tickets?, goal_packets?)
  -> hourly_board_drain + idle_gap_audit + daily_chief_of_staff
   + weekly_strategy_refresh

select_goal_advisor_frontier(project_harness, budget?, gates?)
  -> current_frontier + goal_advisor_handoff + stop_conditions

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

Mark absent metrics as `missing_instrumentation` and route to a missing-system
ticket or Goal Advisor handoff instead of analyzing absent data.

### Scrum Heartbeat Shape

```text
hourly_board_drain(active_tickets, goal_packets, gates)
  -> resume_leaf | start_leaf | request_feedback | no_op

idle_gap_audit(project_harness, current_state)
  -> missing_system_ticket | prep_artifact | review_request | no_op

daily_chief_of_staff(project_harness, progress, signals)
  -> opportunities + risks + blockers + recommended_next_actions

weekly_strategy_refresh(last_strategy, findings, metrics_or_feedback)
  -> updated_strategy_state + experiments + holds + goal_advisor_handoffs
```

The hourly heartbeat drains proceedable tickets first. If no safe ticket or
Goal Packet can advance, it may run the proactive gap workflow. Live scheduling
requires explicit automation approval.

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

### Minimal Syntax Example

```harness-program
project "Faceless AI Engineering Channel" {
  values: [impact.high, loyal_users.high, trust.high, money.low]
  modes: [channel, academy, lab]

  axis reach_acquire {
    bet: "Find high-signal AI engineering learners"
    kpi: review_metric("hook/title clarity")
    evidence: ref("research/channel-examples.md")
    heartbeat: weekly_strategy_refresh
  }

  system analytics {
    status: missing_instrumentation
    action: create_ticket("define first content metrics")
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

## Blast Radius

Standardizing notation affects these surfaces:

| Surface | Current Shape | Change Needed | Risk |
| --- | --- | --- | --- |
| `skills/*/SKILL.md` | checklist plus signatures | Add optional params/state/gate clarity to relevant skills only | Low if optional |
| `tickets/templates/ticket.md` | compact task program | Rename `vars` guidance toward `params` and align field names | Medium; many tickets follow this |
| `tickets/templates/goal-loop/program.md` | loop config | Add cross-reference to this spec; keep field shape | Low |
| `tickets/templates/goal-loop/portfolio.md` | horizon map | Add cross-reference and field vocabulary | Low |
| `skills/harness-creator/templates/*` | portfolio/capability/handoff templates | Add `project-harness.md` with a fenced `harness-program` block | Medium; direct user-facing impact |
| `impl-plan` skill | ticket planning guidance | Reference common notation but keep coding-ticket projection | Low |
| `goal-advisor` skill | Goal architecture guidance | Clarify that it compiles selected blocks, not whole parent programs | Low |
| validators | mostly unrelated today | Optional future check for required sections in templates | Medium if enforced |
| existing tickets | mixed legacy formats | Do not rewrite historical tickets | Low if forward-only |

## Migration Plan

1. Adopt this spec as a draft vocabulary.
2. Add `project-harness.md` template to `harness-creator`.
3. Update `harness-creator` first-load checklist to require values, goal
   weights, metric-provider honesty, Scrum heartbeats, and Goal Advisor
   frontiers for project/business/content harnesses.
4. Update `tickets/templates/ticket.md` to mention `params` as the preferred
   name while preserving `vars` compatibility.
5. Add short links from Goal loop templates to this spec.
6. Update `impl-plan` and `goal-advisor` docs to use the projection terms.
7. After two pilots, decide whether to add a validator for required
   `harness-program` nodes.

## Non-Goals

- No new runtime scheduler.
- No hidden automation.
- No immediate rewrite of all existing skills or tickets.
- No requirement that every small skill use a heavy program table.
- No replacement for `goal-loop-contract.md`; this spec complements it.

## Open Questions

- Should `set_automation(...)` remain pseudocode, or become a typed schema only
  after the Codex automation tool is used repeatedly?

Resolved for now:

- Primary harness output is `project-harness.md`, not `program-preview.md` or
  `harness-program.md`.
- The compact source is a fenced `harness-program` block. Markdown tables are
  optional audit views, not the main program.
