---
title: Goal Loop Contract
status: draft
owner: goal-advisor
created_at: 2026-06-12
feature_refs:
  - FEAT-0029
---

# Goal Loop Contract

## Purpose

Define how Farplane uses native Codex Goals for material multi-turn work without
creating hidden or competing loop systems.

Native Codex Goal mode is the only formal continuation loop. Farplane adds the
visible state, configuration, progress, feedback, and drift-review surfaces
around it.

```text
goal_loop(files[], trigger, budget?)
  -> next_turn + evidence + drift_verdict + state_delta
```

Long-running business, strategy, or multi-agent operating loops may add a
portfolio layer above file-list Goal Packets:

```text
goal_portfolio(portfolio.md, goal_packet[], child_ticket[])
  -> current_frontier + trigger_plan + conflict_checks + state_delta
```

## Ownership Model

```text
Goal = native continuation engine for one uninterrupted execution window
portfolio.md = long-horizon goal graph and planning view
ticket.md = task contract
program.md = loop configuration
progress.md = append-only observed execution
Goal prompt = generated execution prompt
heartbeat = delayed trigger
optimize-with-human = human-feedback optimization preset
skills = methods inside a turn
rollout = meta ticket pattern
drift checker = read-only alignment reviewer
impl = coding-ticket leaf executor
```

Do not make tickets, skills, human feedback, heartbeat automations, or rollout
patterns into alternate continuation runtimes.

Do not make Notion, a dashboard, or a generated prompt the canonical source of
truth for a Farplane Goal Portfolio unless the operator explicitly chooses that
external system. The repo-owned portfolio file should be the durable
intermediate language for agents; external tools are sync views by default.

## Goal Packet

A material Goal should create or attach to durable files and use a Goal Packet.
The generated prompt should list those files inline as `Files:` rather than
relying on transcript memory.

```text
GoalPacket :=
  files[]
+ generated_goal_prompt
+ drift_check_contract
```

`files[]` is usually one or more `ticket.md`, `program.md`, and `progress.md`
triples. It may also include specs, board indexes, QA artifacts, or other local
files the Goal must treat as source of truth.

Use a Goal Packet for work that is ambitious, long-running, likely to resume,
agentically hard, proof-sensitive, human-feedback-driven, heartbeat-driven, or
rollout-like.

Tiny one-turn work should not use native Goal mode.

## Goal Portfolio

Use a Goal Portfolio when the work is bigger than one Goal Packet, such as
running an autonomous store, coordinating multiple agents, decomposing a
multi-year objective, or deciding which skill and harness improvements compound
through downstream work.

```text
GoalPortfolio :=
  portfolio.md
+ parent GoalPacket
+ child GoalPacket[]
+ child_ticket[]
+ sync_targets
```

`portfolio.md` is a Markdown planning UI. It can be synced to Notion, but the
repo file remains the canonical state unless explicitly overridden.

Portfolio orchestration is a heartbeat/manual-resume workflow. Native Goal mode
is for the selected uninterrupted execution window, which may be one ticket or
a bounded batch of listed files.

The portfolio should show:

- North Star or strategic intent
- goal-writing standard with outcome, metric, timeframe, scope, and proof
- one portfolio map that combines horizon tree, project/task tree, trigger
  modes, metrics, holds, dependencies, parallel branches, and amplification
  edges
- metric discovery for early leading indicators when the map needs more detail
- current frontier, meaning the first branch expanded deeply enough to run now
- cadence for daily, weekly, monthly, quarterly, and yearly replanning

Do not expand the entire long-horizon tree into low-level tasks. Expand only the
first branch that can produce useful evidence now.

At month-level planning, start representing execution as projects. At week/day
resolution, use tasks or child tickets. Goals describe outcomes; projects group
work; tasks perform concrete actions.

```text
goal -> project[] -> task[]
good_goal(intent, horizon, evidence_state)
  -> outcome + metric + timeframe + constraints + proof_surface

heartbeat(files[])
  -> start_goal | resume_goal | request_feedback | replan | no_op

native_goal(files[], budget?)
  -> artifact + evidence + completion_entry
```

## File Contracts

### `ticket.md`

Owns the durable task contract:

- objective and summary
- scope in and out
- before/after delta and first-principles basis
- compact task program when the workflow fits in the ticket
- Done / Proof scoreboard
- current status and `next_action`
- human gates and safety boundaries
- sidecar and artifact links

Do not put long chronological logs, bulky evidence, or mutable loop strategy in
`ticket.md`.

### `portfolio.md`

Owns the long-horizon planning graph when one ticket coordinates multiple goals:

- North Star
- goal-writing standard
- portfolio map
- metric discovery
- current decomposition frontier
- dependencies and holds
- parallelizable branches
- amplification edges
- trigger modes for each goal
- sync targets such as Notion
- replan cadence

Do not put turn logs or execution transcripts in `portfolio.md`; use
`progress.md`. Do not put every speculative future task in `portfolio.md`;
future horizons should stay abstract until evidence justifies expansion.

### `program.md`

Owns the loop configuration:

- goal mode: `active_goal`, `heartbeat`, `rollout`, `skill_improvement`, or
  `feedback_loop`
- metric or feedback provider
- time, token/model/compute, subagent, review, QA, feedback, and spend budget
- after-each-turn routine
- drift-check policy
- progress logging policy
- heartbeat policy when time gaps matter
- stop conditions
- blocked report shape
- listed-file, board-drain, batch, or rollout policy when relevant

`program.md` is not a second `SKILL.md`. It is the configuration for this one
Goal loop. For short non-Goal work, the ticket `Program` section can hold the
task pseudocode directly. Use `program.md` when the program is long-running,
Goal-backed, heartbeat-based, rollout-like, skill-improvement oriented, or
likely to need multiple resumptions.

### `progress.md`

Owns append-only observed execution:

- turn timestamp
- trigger
- intent for the turn
- actions taken
- files or artifacts changed
- evidence collected
- metric or feedback sample
- drift verdict
- next action
- blocker or stop reason

Do not paste raw transcript. Keep each entry compact and reconstructable.

## Goal Prompt Shape

The generated native Goal prompt should list files inline, then use four
explicit sections:

```text
Files:
- <ticket.md>
- <program.md>
- <progress.md>
Task: <ticket objective, scope, Done / Proof, and current next_action>
Logging: <how to append progress.md before turn end>
Metric: <metric_provider or feedback_provider from program.md>
After each turn: <drift check, next-action choice, complete/blocked policy>
```

The Goal prompt is a runtime instruction derived from `ticket.md` and
`program.md`; it is not the canonical program.

## Drift Check

Use an independent read-only drift reviewer when work is material, strategic,
long-running, or easy to self-approve.

```text
drift_check(ticket, program, progress_tail, current_claim)
  -> aligned | drifting | blocked | complete_candidate
   + reason
   + evidence_refs
   + recovery_action
```

The drift checker compares observed progress against the contract. It does not
own implementation planning, edits, or final approval.

## Feedback Providers

Some loops optimize against mechanical commands. Others need human judgment or
agent review.

```text
feedback_provider(request, rubric, context)
  -> observation | score | decision
```

Provider examples:

- `mechanical`: command, test, script, benchmark, eval
- `review`: reviewer TAS verdict
- `agent_qa`: adversarial tester evidence
- `human_feedback`: human score, qualitative feedback, or approval decision
- `market`: external result such as clicks, replies, sales, or retention

Avoid fake numbers. Judgment-heavy work may use `review_verdict`,
`human_feedback`, or `artifact_presence` instead of a numeric metric.

## Goal Versus Heartbeat

Goals and heartbeats share the same file contract but differ by trigger and time
shape:

```text
trigger =
  immediate_goal_continuation
| scheduled_heartbeat
| human_feedback_received
| external_event
```

Use native Goal when work should continue inside the current uninterrupted
time/budget window. Use a heartbeat when the next useful check depends on time,
external state, human feedback, board drain, or periodic operations.

For portfolios or board drains, use heartbeat or manual resume at the parent
level. The heartbeat chooses the next file set; that file set may then run under
native Goal.

Heartbeat prompts should read the listed files, then either resume/start a
Goal, request feedback, log a no-op, replan, or report blocked.

## Continuation After Completion

A native Goal is a time/budget-bounded execution loop. It may complete a large
ticket or a bounded batch within a day. Work that requires pauses, periodic
checks, or waiting belongs in heartbeat policy rather than an ever-growing
native Goal.

```text
complete_goal_window(files[], program)
  -> progress_entry + file_state_delta + next_trigger
```

When a Goal window completes:

1. Append completion entries to every changed `progress.md`.
2. Update the relevant ticket, board, or portfolio state to `complete`,
   `complete_candidate`, `blocked`, or `waiting`.
3. Run the configured review, drift check, QA, or proof gate.
4. If a heartbeat policy still has proceedable work, start or resume the next
   eligible file set.
5. If the frontier is complete, run the heartbeat or replan routine.
6. Expand only the next evidence-justified branch.

Use this split:

- native Goal = work within the current uninterrupted time/budget window
- heartbeat = periodically inspect evidence and decide whether to start,
  resume, wait, or replan
- ticket/program/progress files = task contract, loop policy, and observed state
- portfolio = optional longer trajectory and current frontier
- replan = update the map after evidence, completion, blockers, or elapsed time

The operator may manually trigger a replan, but long-running portfolios should
not depend on memory or chat nudges alone. Their `program.md` should define a
heartbeat cadence and a replan routine.

```text
portfolio_heartbeat(portfolio, parent_program, progress)
  -> no_op | start_child_goal | resume_child_goal | request_feedback | replan
```

Use `no_op` when nothing useful can happen yet. Log the no-op so future agents
can tell the loop is alive rather than forgotten.

## Rollout Pattern

Rollout is a meta ticket pattern, not a daemon:

```text
rollout_goal(pattern, sample_results, target_set)
  -> child_ticket[] | staged_checkpoints + rollout_progress
```

Use rollout when:

1. one case has proven the pattern;
2. the procedure is captured in `program.md`, a checklist, or a temporary
   rollout prompt;
3. the target set is explicit;
4. each batch has proof and rollback or hold conditions.

Promote the rollout procedure into a reusable skill only after repeated use
proves the trigger and workflow are stable.

## Batch And Board Drain

Batch and board drain are Goal modes, not separate public runners.

```text
batch_goal(files[], budget, proof_policy)
  -> per_ticket_proof[] + batch_evidence + progress_updates

board_drain_heartbeat(board_files[], cadence, budget)
  -> no_op | start_goal(files[]) | resume_goal(files[]) | replan | blocked
```

For a batch Goal:

1. list every ticket/program/progress file inline in the generated prompt;
2. preserve each ticket's `Done / Proof`, blockers, and stop conditions;
3. require one proof row per ticket;
4. treat batch/integration proof as additional, not a replacement;
5. stop or split when attribution becomes unclear.

For a board-drain heartbeat:

1. fetch proceedable tickets from the listed board or ticket index;
2. skip blocked, claimed, human-gated, dependency-blocked, or missing-tool work;
3. choose a time/budget-bounded file set;
4. output or resume a native Goal prompt for that file set;
5. log no-op when nothing useful can advance.

`$work`, `$ralph`, and `batch-work` are retired as public orchestration
surfaces. Their remaining useful contracts are represented here as
Goal-advisor admission/profile, heartbeat board-drain, and batch proof policy.
`$impl` remains the coding-ticket leaf executor when the selected files describe
a build-ready coding ticket.

## AGI Toy Shop Example

Portfolio-level autonomous-store plan:

```text
portfolio.md:
  North Star: Build AGI Toy Shop into a profitable autonomous toy storefront.
  Current Frontier: Y1 > Q1 > W1.
  Portfolio Map:
    - Prove first offer: native_goal, review + artifact, parallel with content
      loop and analytics.
    - Improve short-form content skill: native_goal + human feedback, amplifies
      funnel testing.
    - Install funnel analytics: native_goal, mechanical evidence, amplifies
      offer iteration.
    - Weekly CEO review: heartbeat, hybrid evidence, depends on active evidence.
```

Autonomous-store strategy loop:

```text
ticket.md:
  Improve AGI Toy Shop's autonomous storefront conversion and customer-support
  reliability without publishing changes or spending money.

program.md:
  mode: heartbeat
  metric_provider: hybrid(review_verdict, human_feedback, artifact_presence)
  cadence: weekly
  after_each_turn: inspect sales/support artifacts, propose one highest-ROI
    ticket, append progress, request drift review.

progress.md:
  2026-06-12: inspected support logs, found repeated delivery-status confusion,
  created TASK-0142, drift=aligned, next=write ticket plan.
```

Content-skill improvement loop:

```text
program.md:
  mode: skill_improvement
  metric_provider: human_feedback
  feedback_preset: optimize-with-human
  feedback_request: show 10 TikTok hooks and ask Kenji to swipe keep/reject
  promotion_rule: update skill only when feedback finds a repeatable pattern
```

## Rollout Policy

1. Add Goal Packet files for one material ticket.
2. Prove a future agent can reconstruct state from files alone.
3. Run a read-only drift check against a real or synthetic mismatch.
4. Update `goal-advisor`.
5. Use heartbeat and rollout only after the basic packet works.
