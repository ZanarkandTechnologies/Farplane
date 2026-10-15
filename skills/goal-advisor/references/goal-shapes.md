---
title: Goal Advisor Goal Shapes
owner: goal-advisor
status: active
created_at: 2026-06-13
---

# Goal Shapes

Load this reference when the one-line classifier in `SKILL.md` is not enough to
decide or explain the selected Goal shape.

## What each shape evaluates against

- Active Goal: the issue's Done / Proof, tests, QA, and review.
- Skill improvement: the frozen skill eval plus behavior QA.
- ML autoresearch (a Goal Mode via its preset): the frozen metric; diagnose a
  surprising result before trusting it.
- Feedback: a structured human verdict.
- Delayed reward (Check-In Program): matured evidence against the acceptance rule.
- Rollout: sample evidence against the promotion and rollback rules.

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

Load [human-feedback](human-feedback.md) when Kenji's judgment is the fastest
quality signal and the operator wants an optimization loop rather than one-off
feedback.

## Rollout

```text
rollout_goal(pattern, sample_proof, target_set)
  -> staged_batches + child_tickets? + rollout_progress
```

Use after one or a few examples prove the pattern; the exemplar-first
procedure is the rollout preset in [loop presets](loop-presets.md).

## Batch Goal

```text
batch_goal(files[], budget, proof_policy)
  -> per_ticket_proof[] + batch_evidence + progress_updates
```

Use when one Goal should complete or advance several listed issues in the same
time/budget window. The batch passes only when every listed ticket satisfies
its own `Done` and `QA Strategy`; batch or integration proof is additional, not a
replacement.

Batch rules:

- list every issue (owner/repo#n) inline in the generated prompt;
- preserve each ticket's `Done`, `QA Strategy`, blockers, and stop conditions;
- require one proof row per ticket;
- treat batch/integration proof as additional;
- stop or split when attribution becomes unclear.

## Board Drain Heartbeat

```text
board_drain_heartbeat(board_files[], cadence, budget)
  -> no_op | start_goal(files[]) | resume_goal(files[]) | replan | blocked
```

A board-drain heartbeat runs only when the operator starts it; no automation
starts one. For a board-drain heartbeat:

- fetch proceedable issues from the listed repository or label query;
- skip blocked, claimed, human-gated, dependency-blocked, or missing-tool work;
- choose a time/budget-bounded issue set;
- output or resume a native Goal prompt for that issue set;
- log no-op when nothing useful can advance.

## Project Ticket Portfolio

```text
project_portfolio(harness, metric_objectives, metric_state, ticket_history)
  -> ranked_proposals + admitted_ticket_packets?
```

Use when the operator wants to coordinate a business, autonomous store,
skill-improvement program, or other long-running system. The next-wave planner
compares proposal trajectories from the charter, metric objectives, readings,
history, and reports. Goal Advisor only compiles an admitted ticket into leaf
Goal execution. There is no separate durable parent goal graph.

Project orchestration boundary:

```text
operator | operator_started_parent_heartbeat_goal(parent issue, harness, metric_state, reports)
  -> start_issue_goal | resume_issue_goal | request_feedback | replan | no_op

leaf_native_goal(issue body + Goal turn comments)
  -> artifact + evidence + proof comment
```

Work enters as a GitHub Issue. The operator, or a session they start, runs
Goal Advisor on it. The next admitted issue is picked by the operator or by a
parent heartbeat Goal over a parent issue (the Parent Heartbeat Prompt) that
the operator started; `report-gen` only proposes. Automations never start
agents or runs, and there is no execution heartbeat. Do not generate a native
`/goal` prompt that tries to run the proposal portfolio indefinitely; generate
a native Goal prompt only for the admitted executable issue.
