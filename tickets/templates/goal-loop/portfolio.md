---
kind: goal-portfolio
ticket_id: TASK-XXXX
status: draft
created_at: 2026-06-12
template_id: goal-loop-portfolio
template_version: "0.1.0"
---

# TASK-XXXX Goal Portfolio

## North Star

Describe the durable outcome this portfolio is trying to compound toward.

## Goal Writing Standard

Use evidence-bearing goals, not vague task labels.

```text
good_goal(intent, horizon, evidence_state)
  -> outcome + metric + timeframe + constraints + proof_surface
```

- `Outcome:`
- `Metric / Feedback:`
- `Timeframe:`
- `Scope In / Out:`
- `Proof Surface:`
- `Risk / Anti-metric:`

## Portfolio Rule

Only expand the first evidence-producing branch deeply. Keep future branches as
trajectory placeholders until the current timeframe review produces evidence.
The default smallest durable unit is a feedback-producing project. Use
`starting_tasks` inside a project for obvious first moves; create child tickets
only for real execution, unblock, approval, review, dependency, or proof
boundaries.

## Portfolio Map

- [ ] 5Y:
  - `metric:`
  - [ ] Y1:
    - `metric:`
    - [ ] Q1:
      - `metric:`
      - [ ] M1:
        - `type:` feedback_sized_project
        - `feedback_surface:`
        - `starting_tasks:`
        - [ ] W1:
          - `type:` feedback_sized_project
          - `feedback_surface:`
          - `starting_tasks:`
          - [ ] TASK-XXXX:
            - `trigger:`
            - `metric:`
            - `boundary_reason:`
            - `depends_on:`
            - `parallel:`
            - `amplifies:`
            - `hold:`
            - `state:`

## Metric Discovery

Define early metrics before starting the loop.

| Goal | Horizon | Metric Provider | Signal | Direction | Collection Plan |
| --- | --- | --- | --- | --- | --- |
|  |  | artifact_presence / mechanical / review / human_feedback / market / learning |  | higher / lower / pass-fail / accept-revise / learn |  |

## Current Milestone

Expand only the branch that can produce useful evidence now.

- ``

Hold:

- ``

## Overflow Edges

Use only when inline map annotations become too noisy.

| Source | Edge | Target | Reason |
| --- | --- | --- | --- |
|  | depends_on / parallel / amplifies / hold |  |  |

## Sync Targets

- `notion:` none
- `other:` none

## Replan Cadence

- Daily:
- Weekly:
- Monthly:
- Quarterly:
- Yearly:

## Continuation Policy

- `child_goal_complete:` update this map, append child completion progress, run
  proof/review, then start the next eligible sibling or wait for heartbeat
- `milestone_complete:` run heartbeat/replan before expanding the next branch
- `manual_replan:` allowed / not_allowed
- `heartbeat_replan:` cadence or none
- `no_op_policy:` log no-op when no useful action exists
- `parent_boundary:` parent portfolio uses heartbeat/manual resume, not native
  Goal
- `leaf_boundary:` native Goal executes only the selected child ticket or
  executable leaf task

## Next Goal Packet

- `ticket.md:`
- `program.md:`
- `progress.md:`

## Parent Heartbeat Prompt

```text
Inspect this portfolio as the parent heartbeat.
Task: Choose exactly one next action: start_child_goal, resume_child_goal,
request_feedback, replan, or no_op.
Logging: Append a heartbeat entry to progress.md.
Metric: Preserve this portfolio's current milestone, holds, and proof policy.
After each turn: If a leaf is selected, output/create its child Goal Packet and
native /goal prompt. Do not run the whole portfolio as a native Goal.
```
