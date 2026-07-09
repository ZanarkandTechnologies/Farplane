---
title: Project Goals Reference
owner: horizon-advisor
status: draft
created_at: 2026-06-12
updated_at: 2026-07-08
---

# Project Goals Reference

Use this reference when a request is bigger than one Goal Packet: running a
business, coordinating several agents, decomposing a multi-year objective,
planning a rollout program, or deciding which skill or workflow improvements
compound through the harness.

Every long-horizon planning surface should be a Farplane project. The canonical
file for project-level strategy is always `farplane/goals.yaml`. If a business,
rollout, research program, or autonomous operating loop needs its own horizon,
make it a project with its own `farplane/goals.yaml` instead of adding a separate
parent strategy file beside a ticket.

Product-level strategy is split deliberately: stable product goals and product
KPI membership live in `farplane/products/<product>/product.md`; generated
`farplane/products.json` is the machine/UI index. Weekly or daily
bets are time-bounded hypotheses in interval reports or product `progress.md`,
not durable product goals.

```text
project_goals(north_star, horizon, resources, constraints)
  -> farplane/goals.yaml
   + goal_graph
   + current_milestone
   + child_goal_packets?
```

## First Principles

A project goals file is not a pile of aspirations or an incentive system.
Farplane agents are one party under the operator's control, so the file exists
to make planning, memory, sequencing, sync, and progress visible. It is a
visible operating graph:

- one North Star or strategic intent
- time-scoped goals at different horizons
- sequential goals along a timeline
- parallelizable goals in the same timeframe
- dependencies where one goal must finish before another starts
- amplification edges where one goal improves another goal's return
- a current milestone so only the first useful branch is expanded deeply
- a cadence for replanning at each timeframe boundary
- feedback-sized projects once the horizon becomes concrete enough to execute
- tickets only when execution, unblock, approval, review, or proof state needs a
  durable leaf
- early metric candidates before the first loop starts

Keep the source of truth in the repo where the project runs. Sync to Notion or
other tools as a view, not as the canonical state, unless the operator explicitly
chooses that external system as the source of truth.

## File Model

```text
ProjectGoals :=
  farplane/goals.yaml
+ farplane/harness.md
+ farplane/products/<product>/product.md
+ farplane/products.json
+ farplane/automations.toml
+ farplane/hooks.json
+ tickets/
+ memory_docs
```

Use Goal Packet `program.md` files to define how a selected leaf runs, and
`progress.md` files for append-only leaf observations. Use project reports
under `.farplane/reports/` for PM heartbeat summaries. Do not create standalone
parent strategy files.

## YAML Strategy Shape

Prefer one compact YAML object that an agent can edit safely and the UI can
parse directly. Do not split the same information into separate horizon tree,
project tree, active goal graph, parallel branch table, amplification table,
conflict table, and trigger plan unless the single object becomes unreadable.

```yaml
north_star:
  text: Build AGI Toy Shop into a profitable autonomous toy storefront.

goals:
  revenue_engine:
    name: Launch first profitable revenue engine
    horizon: quarterly
    objective: Prove offer, funnel, content, and tracking.
    smart_goals:
      - id: first_offer_feedback_loop
        target: Launch first offer test and tracking baseline by the next weekly review.
        kpis:
          - id: qualified_market_feedback_count
            target: 10
            direction: above
        interpretation: Feedback volume proves whether to iterate or pivot.

current_bets:
  - id: first_offer_test
    goal_id: revenue_engine
    thesis: A small reviewed offer test will produce better next tickets than broad storefront planning.
    status: active
    evidence_refs:
      - tickets/TASK-0001/ticket.md
    next_decision: Iterate or pivot after the weekly review.

current_milestone:
  id: launch_first_feedback_loop
  review_cadence: weekly
  next_action: Complete TASK-0001 and compare market feedback against the KPI.

holds:
  - id: w2_iteration_hold
    reason: Wait until W1 evidence is reviewed.
```

## Goal Quality

Do not write vague goals that are just high-level task labels. A project goal
should be specific enough to guide planning and measurable enough to support
review, even when the metric is qualitative or early.

```text
good_goal(intent, horizon, evidence_state)
  -> outcome + metric + timeframe + constraints + proof_surface
```

A good goal should answer:

- `Outcome:` what should be true at the end of the timeframe?
- `Metric:` how will we know it improved or passed?
- `Timeframe:` when will we review or replan it?
- `Scope:` what is included and excluded?
- `Proof:` what artifact, signal, review, feedback, or market data proves it?
- `Risk:` what would make the goal misleading or locally optimized?

Prefer this shape:

```text
Increase <target outcome> for <audience/system> from <baseline or unknown>
to <threshold, learning milestone, or reviewable state> by <timeframe>,
measured by <metric/provider>, without <constraint>.
```

When no baseline exists, make the first goal about creating the baseline.

## Metric Discovery

Define early metrics before spawning the loop. The metric does not need to be
perfect; it must be honest, cheap enough to collect, and aligned with the
current horizon.

```text
discover_metrics(goal, horizon, available_evidence)
  -> leading_metric + lagging_metric? + proof_surface + collection_plan
```

Useful early metric types:

- `artifact_presence`: the required file, page, tracker, or demo exists.
- `mechanical`: command, script, eval, scrape, or deterministic check passes.
- `review`: TAS verdict, rubric pass, or expert critique.
- `human_feedback`: labels, ranking, accept/revise decision, qualitative notes.
- `market`: clicks, signups, replies, purchases, retention, support volume.
- `learning`: baseline established, invalidated hypothesis, top failure modes.

Do not fake precision. If the true goal is learning, use a learning metric and
state the next decision that the evidence will unlock.

## Projects And Tickets

Goals describe desired outcomes. Projects group work. A project is the default
smallest durable unit: it should produce something that can be shown to a human,
reviewed by an agent, measured by a metric provider, or exposed to market/user
feedback. Starting tasks may live as hints inside a project, but they are not
the main strategy structure.

Only create child tickets below a project when the boundary is real: different
owner or agent, external access/setup, human approval, feedback collection,
blocking dependency, risky change, or durable proof/review state.

```text
goal -> project[]
project(goal, timeframe, owner, deliverables, feedback_surface)
  -> milestone + starting_tasks? + evidence + child_ticket[]?
ticket(project, action, proof, boundary_reason) -> artifact + state_delta
```

Suggested boundary:

- `5Y`: strategic ambition or identity.
- `1Y`: operating outcome.
- `Q`: measurable bet or capability package.
- `M`: project or campaign theme.
- `W`: feedback-producing project slice, active Goal Packet, or child-ticket
  batch.
- `D`: only when needed: concrete ticket, feedback sample, review, or
  implementation step.

## Horizon Advisor To Goal Advisor

`horizon-advisor` writes or proposes `farplane/goals.yaml` deltas. `goal-advisor`
compiles a selected frontier into executable Goal Packet state.

```text
horizon_advisor(project_root, intent, current_goals, evidence)
  -> farplane/goals.yaml delta + selected_frontier + goal_advisor_handoff

goal_advisor(files=[farplane/goals.yaml, ticket.md, program.md, progress.md])
  -> native_goal_prompt | heartbeat_prompt | direct_route
```

Do not generate a native Goal prompt that tries to run the whole goal graph
indefinitely. The project goals file selects and explains the frontier; native
Goal mode executes one uninterrupted window over listed files.
