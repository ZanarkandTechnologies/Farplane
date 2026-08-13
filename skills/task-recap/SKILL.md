---
name: task-recap
description: "Turn a paused Codex task, durable artifacts, and available thread context into a source-linked resumption brief with decisions, problems, deltas, gaps, and a safe next action."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.4.0"
  skill-qa-checklist: "0.1.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash
---

# Task Recap

## Context

Use this when an operator returns to a paused Codex task and needs enough
grounded context to reply, decide, or hand off safely. It is a read-only
recovery workflow: it reconstructs context but never edits the task, sends a
message, or resumes execution.

Treat durable task state as primary: `ticket.md`, then `program.md`, the latest
80 lines of `progress.md`, linked evidence, and task-scoped source changes.
Use the accessible thread only as supplementary context. If a source is absent,
stale, or conflicts with another source, name that condition instead of filling
the gap from memory.

## Skill Signature

```text
task_recap(task_ref?, focus?) -> resumption_brief + source_ledger + next_action
state: reads(ticket, program, progress, artifacts, scoped diff/status, available thread context); writes(none)
owns: one source-linked resumption brief
gates: task_boundary_bound_or_source_gap; conflicts_labeled; claims_trace_to_sources; no_execution
routes: direct-answer | goal-advisor | review
fails: transcript-only certainty; fabricated task history; completion claim from stale state; unrelated worktree noise as task evidence
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one task boundary and source ledger.
  - [ ] Use an explicit ticket, task/thread reference, or supplied paths; otherwise bind the current task only when it is unambiguous.
  - [ ] If no durable task source is accessible, return a bounded source-gap recap that names the exact missing ticket, artifact, or thread reference.
- [ ] 2. Recover the most authoritative task state.
  - [ ] Read `ticket.md`, `program.md` when present, the latest 80 `progress.md` lines, declared artifacts, and only relevant diff/status evidence.
  - [ ] Read available thread context only to recover the latest user ask, decisions, and unresolved discussion that the durable sources do not cover.
- [ ] 3. Reconcile history before narrating it.
  - [ ] Separate observed facts, source-backed decisions, and clearly marked inferences.
  - [ ] Surface conflicts between ticket state, progress, evidence, and scoped worktree state; do not promote a checkbox or a transcript claim into proof.
- [ ] 4. Build the full recovery brief.
  - [ ] Trace every material delta as `Before`, `After`, and `Example`.
  - [ ] For each material problem, record `symptom -> attempt -> observed result -> disposition -> remaining impact`.
  - [ ] Preserve accepted and rejected decisions, the latest user ask, open questions, and response-ready context.
- [ ] 5. Finish with bounded evidence and routing.
  - [ ] Apply [runtime QA](qa_checklist.md) and list sources used, conflicts, and coverage gaps.
  - [ ] Return one safest next action or reply posture; route to `goal-advisor` only when the task is an active Goal and execution is explicitly requested.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Return this shape, collapsing empty sections but never hiding gaps:

```text
Now: <decision-complete current state>
Goal / success condition:
Latest user context:
Timeline and decisions:
Changes:
  - Before / After / Example
Problems and attempts:
  - symptom -> attempt -> result -> disposition -> impact
Evidence and conflicts:
Open loops and safe next action:
Source ledger and gaps:
```

Positive example: “The implementation exists, but the latest runtime receipt
failed; reply that it is not yet customer-ready and request the missing receipt
instead of confirming completion.”

## Gotchas

- A full recap is not a transcript dump: cite the smallest source set that
  supports each material claim.
- A task can be partially implemented and still blocked; distinguish code,
  check, review, and user-acceptance state.
- A captured `git status` is evidence only at its timestamp. Do not treat
  unrelated changes as task work or a past snapshot as current state.

## Reference Map

- [Ticket and Goal Packet resume contract](../../tickets/README.md) — read when
  a ticket or Goal Packet is available.
- [Runtime QA](qa_checklist.md) — read before returning the recap and reapply
  when the recap will support a material decision.
- [Behavior eval cases](evals/evals.json) — use to test source coverage,
  conflicts, problem history, gaps, and worktree scope.

## Output

- `resumption_brief`: a full, response-ready task recap.
- `source_ledger`: sources used, conflicts, freshness limits, and gaps.
- `next_action`: one safe reply posture, decision, or explicit source request.
