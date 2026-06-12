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
goal_loop(ticket.md, program.md, progress.md, trigger)
  -> next_turn + evidence + drift_verdict + state_delta
```

## Ownership Model

```text
Goal = native continuation engine
ticket.md = task contract
program.md = loop configuration
progress.md = append-only observed execution
Goal prompt = generated execution prompt
heartbeat = delayed trigger
optimize-with-human = human-feedback optimization preset
skills = methods inside a turn
rollout = meta ticket pattern
drift checker = read-only alignment reviewer
```

Do not make tickets, skills, human feedback, heartbeat automations, or rollout
patterns into alternate continuation runtimes.

## Goal Packet

A material Goal should create or attach to one ticket and use a Goal Packet:

```text
GoalPacket :=
  ticket.md
+ program.md
+ progress.md
+ generated_goal_prompt
+ drift_check_contract
```

Use a Goal Packet for work that is ambitious, long-running, likely to resume,
agentically hard, proof-sensitive, human-feedback-driven, heartbeat-driven, or
rollout-like.

Tiny one-turn work should not use native Goal mode.

## File Contracts

### `ticket.md`

Owns the durable task contract:

- objective
- scope in and out
- acceptance criteria
- proof contract
- current status and `next_action`
- human gates and safety boundaries
- evidence links

Do not put long chronological logs or mutable loop strategy in `ticket.md`.

### `program.md`

Owns the loop configuration:

- goal mode: `active_goal`, `heartbeat`, `rollout`, `skill_improvement`, or
  `feedback_loop`
- metric or feedback provider
- after-each-turn routine
- drift-check policy
- progress logging policy
- heartbeat policy when time gaps matter
- stop conditions
- blocked report shape
- child-ticket or rollout policy when relevant

`program.md` is not a second `SKILL.md`. It is the configuration for this one
Goal loop.

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

The generated native Goal prompt should use four explicit sections:

```text
Task: <ticket objective, scope, proof contract, and current next_action>
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

Goals and heartbeats share the same state contract but differ by trigger:

```text
trigger =
  immediate_goal_continuation
| scheduled_heartbeat
| human_feedback_received
| external_event
```

Use native Goal when turns should chain immediately. Use a heartbeat when the
next useful check depends on time, external state, human feedback, or periodic
operations.

Heartbeat prompts should read the same `ticket.md`, `program.md`, and
`progress.md`, then either resume/start a Goal, request feedback, log a no-op,
or report blocked.

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

## AGI Toy Shop Example

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
