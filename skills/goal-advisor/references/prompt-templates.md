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
Approval:
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
Set `approval: pending` for material packets unless the operator explicitly
pre-approved auto-run. Do not run the native Goal until the packet is approved.
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
the source of truth. Keep this Goal prompt compact: do not restate long ticket,
program, design, or progress content that is already in the listed files.

Logging: Before ending each turn, append a compact structured entry to every
listed `progress.md` whose ticket state changed. If the work coordinates
multiple files, also append a coordination note to the primary progress file.

Metric: Satisfy the Done / Proof and metric provider declared in the listed
`ticket.md` and `program.md` files. For multi-ticket goals, each ticket must
have its own proof result; batch or integration proof is additional. If a
ticket's proof weight includes `qa`, `visual_qa`, `agent_qa`, `review`, or
`demo`, use the delegated lane named by the ticket/program and do not count
self-certification as proof.

Final checkpoint: Before `stop_complete` on material ticket work, run or
request the QA evidence review and completion review required by the ticket's
`Done / Proof`, `Proof route`, or `program.md`. Write the strongest evidence,
review receipt, command checks, and any residual risk back to the ticket
`State`/`Links` and the relevant `progress.md`. If QA evidence review or
completion review is missing, stale, or below the required gate, stop blocked or
revise instead of claiming completion.

After each turn: Compare progress against the listed files, request <drift
reviewer> or the delegated QA/review lane when required, continue within the
current time/budget window if useful, otherwise stop complete, stop blocked, or
emit the next heartbeat action with attempted paths and one missing input. For
UI or user-visible changes, stop complete only after the final response can
include the strongest screenshot/image evidence as a Markdown image link plus
artifact links, or after recording a clear blocker for missing visual proof.
The final response must include `Ticket:`, `Verification:`, `Artifacts:`,
`Grounding:`, and `Residual risk:` lines for material feature work.

Approval: This prompt may be run only after the human has approved the current
Goal Packet. If the ticket plan changed after this packet was compiled, return
to `goal-advisor`, regenerate the packet, and ask for approval again.
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
