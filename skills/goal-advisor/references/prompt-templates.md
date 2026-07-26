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
Record the ticket `updated_at` used for compilation in `program.md` or the
prompt artifact, plus the approval state and generated prompt path. For
material native Goal packets, `generated_prompt:` should point to the compiled
prompt artifact or inline prompt location; use `none` only when the route is
explicitly direct execution rather than native Goal execution.
Set `approval: pending` for material packets unless the operator explicitly
pre-approved auto-run. Do not run the native Goal until the packet is approved.

For delayed Reward packets, replace the `Check-In Program` placeholders with
the experiment's executable evidence, scoring, decision, writeback,
idempotency, and source-gap procedure. For immediate feedback or packets with
no delayed Reward row, keep only `mode: not_applicable` plus a reason.
```

## Native Goal Prompt

```text
/goal Run the following files as one Goal Packet.
Files:
- <ticket.md>
- <program.md>
- <progress.md>
- <optional additional ticket/program/progress/spec/board/artifact files>

First read `program.md`; it is the executable loop policy for this Goal
Packet. Then read `ticket.md`; it is the scope, acceptance, and proof contract.
Use `progress.md` as the append-only state log. If `program.md` is missing,
stale, not listed here, or conflicts with the ticket's scope/proof policy, stop
blocked or return to `goal-advisor` to regenerate the packet.

Task: Complete only the primary ticket's `Scope: In` and `Done` conditions.
Obey `program.md` for trigger mode, budget, metric or feedback provider, proof
route, drift policy, after-turn routine, heartbeat or batch rules, and stop
conditions. Use specs, designs, boards, and artifacts as constraints, evidence,
and context; they do not expand executable scope unless `ticket.md` says so.
Preserve each ticket's Scope, Delta, Change Plan, Done, QA Strategy, Docs
Strategy, Agent Contract, Run Hints, budget, blocker policy, and stop
conditions. `Scope: Out` wins unless the ticket is updated and this packet is
regenerated. Do not flatten or rewrite requirements; keep this Goal prompt
compact and treat the listed files as the source of truth.

Logging: Before ending each turn, append a compact structured entry to every
listed `progress.md` whose ticket state changed. If the work coordinates
multiple files, also append a coordination note to the primary progress file.

Metric: Satisfy the Done conditions, QA Strategy, Docs Strategy, and metric
provider declared in the listed `ticket.md` and `program.md` files. For
multi-ticket goals, each ticket must have its own QA result; batch or
integration proof is additional. If ticket and program proof policies conflict,
the ticket `QA Strategy` wins and the packet should be revised. If a ticket's
QA Strategy proof weight includes `qa`, `visual_qa`, `agent_qa`, `review`, or
`demo`, use the delegated lane named by the ticket/program and do not count
self-certification as proof.

Final checkpoint: Before `stop_complete` on material ticket work, run or
request the QA evidence review and completion review required by the ticket's
`QA Strategy.goal_advisor_inputs`, or `program.md`. Write the strongest evidence,
review receipt, command checks, docs validation, and any residual risk back to
the ticket `Links` and the relevant `progress.md`. If QA evidence review,
completion review, docs validation, or packet freshness is missing, stale, or
below the required gate, stop blocked or revise instead of claiming completion.
For a material implementation Goal, after QA passes and before completion
review, run the `demo` skill to produce the default narrated lead-engineer recap
MP4. Do not add a ticket demo flag or apply this step to heartbeats, feedback
checks, planning-only Goals, or direct non-Goal work.
When every gate passes, run `farplane ticket close TASK-XXXX` and include its
receipt before `stop_complete`. Do not move the ticket by hand.

After each turn: Compare progress against the listed files, choose and execute
one bounded action, evaluate it with the ticket/program provider, then append a
compact observation, evidence link, learning, decision, and next action. When
a result materially misses a declared expectation, is implausibly strong, or
appears invalid, check evaluator/evidence integrity and allow bounded in-budget
repairs or reruns only while a concrete integrity concern remains; repeated
valid contrary evidence must update the next action. Request <drift reviewer>
or the delegated QA/review lane when required by `program.md`.
Continue within the current time/budget window if useful; otherwise stop
complete, stop blocked, or emit the next heartbeat action with attempted paths
and one missing input. For UI or user-visible changes, stop complete only after
the final response can include the strongest screenshot/image evidence as a
Markdown image link plus artifact links, or after recording a clear blocker for
missing visual proof. The final response must include `Ticket:`,
`Verification:`, `Artifacts:`, `Grounding:`, and `Residual risk:` lines for
material feature work.

Approval: This prompt may be run only after the human has approved the current
Goal Packet. If the ticket plan changed after this packet was compiled, return
to `goal-advisor`, regenerate `program.md` and this prompt, and ask for
approval again.
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
replan, blocked, or no_op. For board drain, fetch proceedable tickets, skip
blocked/gated/claimed/dependency-blocked work, and select the next
time/budget-bounded file set.

Logging: Append a compact heartbeat entry to the listed progress file before
ending, including no-op reasons when nothing useful can happen yet.

Metric: Preserve the listed files' Done, QA Strategy, budget, and stop policies.

After each turn: If an executable file set is selected, output its native Goal
prompt with an inline `Files:` list. Use `blocked` when required inputs,
approval, evidence, or tools are missing. Do not create hidden automation or a
competing scheduler.
```

## Delayed Check-In Resume Prompt

```text
Resume the original experiment Goal Packet for one due check-in.
Files:
- <original ticket.md>
- <original program.md>
- <original progress.md>
- <named evidence artifacts, when any>

Matured Reward IDs: <stable reward_id values derived by Work Pulse>
Evidence refs: <refs supplied by Work Pulse or named in program.md>
Current time: <pulse timestamp>

First read `program.md`, then execute its `Check-In Program` exactly. Update
only the supplied matured rows, preserve future and already-complete rows,
append the required observation and decision to `progress.md`, and return one
of `accept`, `kill`, or `monitor`. The ticket's scope and QA
Strategy win on conflict. If the program is missing, stale, not in
`delayed_reward` mode, or lacks a required evidence/decision rule, record the
source gap and return blocked for Goal Advisor repair; do not invent a check-in
algorithm in this prompt.
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

After each turn: Select and change one bounded part of the skill, run the
declared complete evaluator, append the observation, evidence, learning,
decision, and next action, then request drift review when required. Promote
only durable accepted rules. Use Goal mode as the durable loop runner,
`self-improve` only for eval/memory/prompt scaffolding, and `skill-maintenance`
for accepted writeback.
```
