---
title: Goal Advisor Goal Shapes
owner: goal-advisor
status: active
created_at: 2026-06-13
---

# Goal Shapes

Load this reference when the one-line classifier in `SKILL.md` is not enough to
decide or explain the selected Goal shape.

## Active Goal

```text
active_goal(ticket, program, progress)
  -> chained_turns_until_complete_or_blocked
```

Use for implementation, skill improvement, research, or app-building work that
should continue inside the current uninterrupted time/budget window.

## Heartbeat

```text
heartbeat(ticket, program, progress, schedule)
  -> inspect_state + maybe_resume_goal + progress_entry
```

Use when useful work depends on time, external state, feedback arrival, board
drain, cron-like cadence, or other periodic operations. A heartbeat is a
trigger pattern over Goal Packet state, not a separate loop runtime.

## Feedback Loop

```text
feedback_loop(ticket, program, progress, provider)
  -> feedback_request + observation_or_score_or_decision + next_turn
```

Use `optimize-with-human` when Kenji's judgment is the fastest quality signal
and the operator wants an optimization loop rather than one-off feedback.

## Rollout

```text
rollout_goal(pattern, sample_proof, target_set)
  -> staged_batches + child_tickets? + rollout_progress
```

Use after one or a few examples prove the pattern. Promote to a reusable skill
only after repeated use proves the trigger and workflow.

## Batch Goal

```text
batch_goal(files[], budget, proof_policy)
  -> per_ticket_proof[] + batch_evidence + progress_updates
```

Use when one Goal should complete or advance several listed files in the same
time/budget window. The batch passes only when every listed ticket satisfies
its own `Done / Proof`; batch or integration proof is additional, not a
replacement.

Batch rules:

- list every ticket/program/progress file inline in the generated prompt;
- preserve each ticket's `Done / Proof`, blockers, and stop conditions;
- require one proof row per ticket;
- treat batch/integration proof as additional;
- stop or split when attribution becomes unclear.

## Board Drain Heartbeat

```text
board_drain_heartbeat(board_files[], cadence, budget)
  -> no_op | start_goal(files[]) | resume_goal(files[]) | replan | blocked
```

For a board-drain heartbeat:

- fetch proceedable tickets from the listed board or ticket index;
- skip blocked, claimed, human-gated, dependency-blocked, or missing-tool work;
- choose a time/budget-bounded file set;
- output or resume a native Goal prompt for that file set;
- log no-op when nothing useful can advance.

## Goal Portfolio

```text
goal_portfolio(north_star, horizon, resources, constraints)
  -> portfolio.md + parent_program.md + current_frontier + child_goal_packets?
```

Use when the operator wants to coordinate a business, product line, autonomous
store, skill-improvement program, or other multi-goal system. Load
`goal-portfolio.md` before designing this shape.

Portfolio orchestration boundary:

```text
parent_heartbeat(portfolio.md, program.md, progress.md)
  -> start_child_goal | resume_child_goal | request_feedback | replan | no_op

leaf_native_goal(ticket.md, program.md, progress.md)
  -> artifact + evidence + completion_entry
```

Do not generate a native `/goal` prompt that tries to run the whole portfolio
indefinitely. Generate a heartbeat prompt for the parent and a native Goal
prompt only for the current executable leaf.
