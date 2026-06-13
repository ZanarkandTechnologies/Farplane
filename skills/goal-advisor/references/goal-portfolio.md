---
title: Goal Portfolio Reference
owner: goal-advisor
status: draft
created_at: 2026-06-12
---

# Goal Portfolio Reference

Use this reference when a request is bigger than one Goal Packet: running a
business, coordinating several agents, decomposing a multi-year objective,
planning a rollout program, or deciding which skill or workflow improvements
compound through the harness.

```text
goal_portfolio(north_star, horizon, resources, constraints)
  -> portfolio.md + goal_graph + current_frontier + child_goal_packets?
```

## First Principles

A goal portfolio is not a pile of goals or an incentive system. Farplane agents
are one party under the operator's control, so the portfolio exists to make
planning, memory, sequencing, sync, and progress visible. It is a visible
operating graph:

- one North Star or strategic intent
- time-scoped goals at different horizons
- sequential goals along a timeline
- parallelizable goals in the same timeframe
- dependencies where one goal must finish before another starts
- amplification edges where one goal improves another goal's return
- a decomposition frontier so only the first useful branch is expanded deeply
- a cadence for replanning at each timeframe boundary
- projects and tasks once the horizon becomes concrete enough to execute
- early metric candidates before the first loop starts

Keep the source of truth in the repo where the Goal starts. Sync to Notion or
other tools as a view, not as the canonical state, unless the operator explicitly
chooses Notion as the source of truth.

## File Model

```text
GoalPortfolio :=
  portfolio.md
+ ticket.md
+ program.md
+ progress.md
+ project[]
+ task[]
+ child_ticket[]
+ notion_sync?
```

Use `portfolio.md` for the long-horizon planning UI. Use child tickets for
execution units. Use `program.md` to define how the portfolio is reviewed,
expanded, synced, and pruned. Use `progress.md` for append-only observations.

## Markdown Planning UI

Prefer one compact Markdown map that an agent can edit safely. Do not split the
same information into separate horizon tree, project tree, active goal graph,
parallel branch table, amplification table, conflict table, and trigger plan
unless the single map becomes unreadable.

```markdown
## North Star

Build AGI Toy Shop into a profitable autonomous toy storefront.

## Portfolio Map

- [ ] 5Y goal: Build a compounding autonomous store
  - metric: revenue engine + durable capability evidence
  - [ ] Y1 goal: Launch first profitable revenue engine
    - metric: first repeatable offer/funnel/content loop
    - [ ] Q1 goal: Prove offer, funnel, content, and tracking
      - metric: review + artifact + first market/feedback baseline
      - [ ] M1 project: Create the first evidence loop
        - [ ] W1 project slice: Launch first offer test and tracking baseline
          - [ ] TASK-0001 Define first toy offer
            - trigger: native_goal
            - metric: review + artifact
            - parallel: TASK-0003, TASK-0004
            - amplifies: TASK-0002, TASK-0005
          - [ ] TASK-0002 Publish first landing page draft
            - trigger: native_goal
            - metric: review + artifact_presence
            - depends_on: TASK-0001
          - [ ] TASK-0003 Install funnel tracking baseline
            - trigger: native_goal
            - metric: mechanical
            - parallel: TASK-0001, TASK-0004
          - [ ] TASK-0004 Generate 10 short-form hooks
            - trigger: native_goal
            - metric: human_feedback
            - amplifies: TASK-0005
          - [ ] TASK-0005 Ask Kenji for content feedback
            - trigger: feedback_loop
            - metric: human_feedback
        - [ ] W2 project slice: Iterate offer from W1 evidence
          - hold: until W1 review
      - [ ] M2 project: Improve content and conversion loop
        - hold: until M1 review
    - [ ] Q2 goal: Scale winning channel
      - hold: until Q1 review

## Replan Cadence

- Weekly: update W-level tickets and current frontier.
- Quarterly: compare Q goal against evidence, create the next quarter branch.
- Yearly: revise annual strategy from market and capability evidence.
```

## Goal Quality

Do not write vague goals that are just high-level task labels. A portfolio goal
should be specific enough to guide planning and measurable enough to support
review, even when the metric is qualitative or early.

```text
good_goal(intent, horizon, evidence_state)
  -> outcome + metric + timeframe + constraints + proof_surface
```

A good goal should usually answer:

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

When no baseline exists, make the first goal about creating the baseline:

```text
Establish the first conversion baseline for AGI Toy Shop's offer funnel by W1,
measured by an installed tracking artifact, one review pass, and a first
captured sample, without spending money or publishing unreviewed changes.
```

Avoid goals like:

```text
Improve funnel.
Make better content.
Build the shop.
```

Rewrite them as:

```text
Produce 10 short-form hooks for the first AGI Toy Shop offer by W1, collect
Kenji's keep/reject labels, and extract at least 3 reusable content patterns
before updating the content skill.
```

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

For early portfolios, pair one leading metric with one proof surface:

```text
goal_metric(goal) -> provider + signal + direction + review_cadence
```

Examples:

- Offer goal: `review` + offer doc passes clarity/usefulness review.
- Content goal: `human_feedback` + 10 hooks labeled keep/reject.
- Funnel goal: `mechanical` + tracking event fires in a local smoke.
- Market goal: `market` + first real conversion or reply once publishing is
  allowed.

Do not fake precision. If the true goal is learning, use a learning metric and
state the next decision that the evidence will unlock.

## Projects And Tasks

Goals describe desired outcomes. Projects group work. Tasks are concrete
actions or tickets. Around the month level, the portfolio should usually start
introducing projects; around the week/day level, it should introduce tasks or
child tickets.

```text
goal -> project[] -> task[]
project(goal, timeframe, owner, deliverables) -> task[] + evidence
task(project, action, proof) -> artifact + state_delta
```

Suggested boundary:

- `5Y`: strategic ambition or identity.
- `1Y`: operating outcome.
- `Q`: measurable bet or capability package.
- `M`: project or campaign theme.
- `W`: project slice, active Goal Packet, or child-ticket batch.
- `D`: concrete task, feedback sample, review, or implementation ticket.

Projects can vary in size. A project may last a month, a week, or a few days,
but it should own a coherent bundle of tasks and one proof surface.

## Map Annotation Rules

Represent graph properties inline on the relevant node when possible:

- `trigger:` native_goal, heartbeat, feedback_loop, child_ticket, one_turn, or
  sync_only
- `metric:` provider and signal
- `depends_on:` blocking predecessor
- `parallel:` safe sibling work
- `amplifies:` downstream node that benefits
- `hold:` condition that prevents expansion or execution
- `state:` planned, active, blocked, complete_candidate, or complete

Use separate sections only for:

- `Open Questions`, when the operator must decide something.
- `Replan Cadence`, because cadence cuts across the whole map.
- `Sync Targets`, because external views are not goal nodes.
- `Overflow Edges`, when inline annotations make the map hard to scan.

## Decomposition Rules

Expand only the first branch that can produce useful evidence now.

```text
decompose(goal, horizon, evidence_state)
  -> current_frontier + child_goals + hold_list
```

Do not expand the entire five-year tree into tasks. Strategy farther away from
evidence should stay abstract.

Suggested horizons:

- `5Y`: identity, ambition, durable advantage
- `1Y`: operating model and revenue engine
- `Q`: measurable bet and capability package
- `M`: project, campaign, release, or improvement theme
- `W`: project slice, active Goal Packet, heartbeat packet, or ticket batch
- `D`: concrete ticket task, feedback sample, review, or implementation step

## Parallelism Rules

Two goals can run in parallel when they do not require the same exclusive input,
do not mutate the same owner surface in conflicting ways, and each can produce
evidence independently.

```text
parallelizable(goal_a, goal_b, resources)
  -> yes | no | needs_coordination
```

Common parallelizable branches for an autonomous store:

- funnel tracking and content-skill improvement
- product catalog research and customer-support workflow design
- analytics setup and first offer copy
- skill eval writing and market feedback collection

Common conflicts:

- two agents rewriting the same skill package
- one goal launching an offer while another changes the offer definition
- market-facing spend or publish actions without a shared approval gate
- several goals optimizing local proxy metrics with no shared North Star

Do not over-model coordination before compute or attention becomes scarce. When
there is no real resource conflict, spawn isolated Goal Packets and coordinate
through clear state surfaces rather than inventing agent-incentive machinery.

## Amplification Rules

Mark an amplification edge when the output of one goal improves the expected
return of another.

```text
amplifies(source_goal, target_goal)
  -> reason + expected_gain + evidence_needed
```

For Farplane, skill improvements can amplify many downstream goals. Prefer
optimizing a skill when it has high call frequency, high failure cost, or sits
upstream of many active tickets.

```text
priority(skill_improvement)
  ~= call_frequency * downstream_value * failure_cost * confidence
```

This is a heuristic, not a fake precision score. Use it to choose which
capability to improve first, then verify through real evals, review, human
feedback, or market data.

## Trigger Modes

Use native Goal for immediate chained work. Use heartbeat when time, market
data, feedback, or periodic review matters. Use child tickets for bounded work
that can be delegated. Use Notion sync only as an external view.

```text
choose_trigger(goal)
  -> native_goal | heartbeat | child_ticket | one_turn | sync_only
```

Examples:

- `native_goal`: implement first funnel tracker.
- `heartbeat`: weekly CEO strategy review.
- `child_ticket`: create landing page copy variants.
- `one_turn`: answer a small blocking question.
- `sync_only`: mirror portfolio state to Notion.

## Continuation After Goal Completion

Native Goals usually finish a concrete child ticket or project slice. They are
not the long-range memory by themselves. The portfolio heartbeat owns what
happens after a child Goal is done.

```text
complete_child_goal(child_packet, portfolio, parent_program)
  -> portfolio_state_delta + next_trigger

portfolio_heartbeat(portfolio, parent_program, progress)
  -> no_op | start_child_goal | resume_child_goal | request_feedback | replan
```

Default continuation rules:

- If a child Goal finishes, update its node in `portfolio.md`, append completion
  progress, and run the proof/review gate.
- If unfinished sibling nodes are eligible, start or resume the next child Goal.
- If the current frontier is complete, run the parent heartbeat or replan
  routine.
- If no useful action exists yet, log a no-op rather than silently forgetting
  the portfolio.
- Manual replans are allowed, but serious long-running portfolios should also
  define a heartbeat cadence.

## AGI Toy Shop Example

North Star:

```text
Build AGI Toy Shop into a profitable autonomous toy storefront whose content,
offer, funnel, and support loops improve from evidence.
```

First portfolio shape:

```markdown
- [ ] M1 project: Create the first evidence loop
  - [ ] W1 project slice: Launch first offer test and tracking baseline
    - [ ] TASK-0001 Define first toy offer
      - trigger: native_goal
      - metric: review + artifact
      - parallel: TASK-0003, TASK-0004
      - amplifies: landing page and content hooks
    - [ ] TASK-0003 Install funnel tracking baseline
      - trigger: native_goal
      - metric: mechanical
      - parallel: TASK-0001, TASK-0004
    - [ ] TASK-0005 Ask Kenji for content feedback
      - trigger: feedback_loop
      - metric: human_feedback
```

The first branch to expand is W1. Later branches stay as placeholders until W1
evidence changes the plan.

See `examples/agi-toy-shop-portfolio.md` for a fuller file-system-style
portfolio example.

## Output Contract

When designing a portfolio, return or write:

```text
Portfolio:
North Star:
Horizon:
Portfolio Map:
Current Frontier:
Overflow Edges:
State Surfaces:
Next Goal Packet:
```
