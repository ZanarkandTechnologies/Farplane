---
title: Goal Advisor Prompt Templates
owner: goal-advisor
status: active
created_at: 2026-06-13
---

# Goal Advisor Prompt Templates

Load this reference only after `goal-advisor` has chosen a Goal or heartbeat
branch and needs to emit prompt text.

## Goal Architecture

```text
Goal Architecture:
Ticket:
Program:
Progress:
Files:
Trigger:
Budget:
Metric / Feedback Provider:
Drift Policy:
Heartbeat Prompt:
Native Goal Prompt:
Next Action:
```

## Goal Packet Setup

```text
Create or update:
- tickets/TASK-XXXX/ticket.md
- tickets/TASK-XXXX/program.md from tickets/templates/goal-loop/program.md
- tickets/TASK-XXXX/progress.md from tickets/templates/goal-loop/progress.md

Then generate the native `/goal` prompt from the same packet.
```

## Native Goal Prompt

```text
/goal Run the following files as one Goal Packet.
Files:
- <ticket.md>
- <program.md>
- <progress.md>
- <optional additional ticket/program/progress/spec/board/artifact files>

Task: Complete the desired outcomes defined across the listed files. Preserve
each ticket's scope, constraints, Done / Proof, budget, blocker policy, and stop
conditions. Do not flatten or rewrite requirements; treat the listed files as
the source of truth.

Logging: Before ending each turn, append a compact structured entry to every
listed `progress.md` whose ticket state changed. If the work coordinates
multiple files, also append a coordination note to the primary progress file.

Metric: Satisfy the Done / Proof and metric provider declared in the listed
`ticket.md` and `program.md` files. For multi-ticket goals, each ticket must
have its own proof result; batch or integration proof is additional.

After each turn: Compare progress against the listed files, request <drift
reviewer> when required, continue within the current time/budget window if
useful, otherwise stop complete, stop blocked, or emit the next heartbeat
action with attempted paths and one missing input.
```

## Parent Heartbeat Prompt

```text
Inspect the following files as a heartbeat Goal.
Files:
- <board.md or ticket index>
- <program.md>
- <progress.md>
- <optional ticket/program/progress files>

Task: Choose exactly one next action: start_goal, resume_goal, request_feedback,
replan, no_op, or stop_complete. For board drain, fetch proceedable tickets,
skip blocked/gated/claimed/dependency-blocked work, and select the next
time/budget-bounded file set.

Logging: Append a compact heartbeat entry to the listed progress file before
ending, including no-op reasons when nothing useful can happen yet.

Metric: Preserve the listed files' Done / Proof, budget, and stop policies.

After each turn: If an executable file set is selected, output its native Goal
prompt with an inline `Files:` list. Do not create hidden automation or a
competing scheduler.
```

## Skill Improvement Goal

```text
/goal Run <ticket path> as a native Goal-backed skill-improvement loop for
<target skill>, verified by <eval command/artifact, metric, or human-reviewed
artifact> while preserving <skill contract constraints>.

Files:
- <ticket.md>
- <program.md>
- <progress.md>
- <target skill SKILL.md>
- <optional references/scripts/evals/self-improve files>

Task: Improve the target skill toward the metric, rubric, or feedback schema
defined in the listed program. If no metric exists, first define the cheapest
honest feedback surface before mutating the skill.

Logging: Use `progress.md` as the turn log. Append progress, changed files,
verification, metric sample, drift verdict, next action, and blockers.

Metric: Use the listed eval, review, or human feedback provider. Do not promote
unverified changes as accepted rules.

After each turn: Change one bounded part of the skill, verify it, request drift
review when required, and promote only durable accepted rules. Use Goal mode as
the durable loop runner, `self-improve` only for eval/memory/prompt scaffolding,
and `skill-maintenance` for accepted writeback.
```
