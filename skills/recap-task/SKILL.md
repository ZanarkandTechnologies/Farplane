---
name: recap-task
description: "Turn a paused Codex task and its durable records into a source-linked recap that supports a safe reply, decision, or handoff."
tier: 3
group: operations
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep, Bash
---

# Recap Task

## Context

Use this when an operator returns to a paused task. Reconstruct enough context
to reply, decide, or hand off safely. This is read-only: do not edit the task,
send a message, or resume execution.

## Skill Signature

```text
recap_task(task_ref?, focus?) -> quick_recap + full_context? + next_action
reads: ticket, Goal Packet, evidence, task-scoped changes, and available thread context
does: reconciles the task record and fills the smallest safe recap template
writes: none
returns: source-linked recap, conflicts and gaps, and one safe next posture
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Resolve the task packet.**
  `task_ref + supplied paths -> source_packet | source_gap`

  Rule: Prefer `ticket.md`, then `program.md`, recent `progress.md`, linked
  evidence, task-owned changes, and finally available thread context. Read every
  supplied path before calling it missing. When no task boundary is reliable,
  stop with the `source-gap` template.

  Assert:
  - The task boundary and every source actually read are explicit.
  - Missing, unreadable, or stale context is named rather than reconstructed from memory.

- [ ] **N2 — Reconcile what is true now.**
  `source_packet -> current_state + delta + attempts + conflicts + freshness`

  Rule: Keep implementation, verification, review, and user acceptance
  separate. A checked box or changed file is not runtime proof. For worktree
  captures, name task-owned paths, excluded noise, the capture time, and that
  the snapshot is historical.

  Example: `fix implemented + unit pass + missing operated receipt -> partial`,
  never “fixed.”

  Assert:
  - Before, After, and one supported Example describe any material delta.
  - Each important attempt keeps its symptom, action, observed result, disposition, and remaining impact.

- [ ] **N3 — Choose the smallest safe recap template.**
  `current_state + caller_need -> quick | full | source-gap`

  Rule: Load [recap templates](references/templates.md). Use `quick` only when
  the packet is coherent. A requested full recap, proof conflict, or material
  failed attempt must select `full`; never stop after the quick card in those
  cases. Use `source-gap` when N1 cannot bind reliable task evidence.

  Assert:
  - The response begins with `Now`, `Delta`, and `Risks & action`.
  - Full mode includes every template section and lists each literal source path on its own ledger bullet before `Safe next`.

- [ ] **N4 — Render a response-ready recap.**
  `selected_template + reconciled_state -> grounded_recap + safe_next`

  Rule: Fill the template with task facts, not template instructions. Preserve
  the latest user question, accepted and rejected decisions, conflicts, and
  freshness limits. End with one safe reply posture, decision, or source request.

  Assert:
  - Every material claim traces to a source and uncertainty stays visible.
  - The recap does not execute work or claim evidence that the packet does not contain.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A timeline shows order; an attempt trace shows why a path worked, failed, or was rejected. Full mode may need both.
- Do not treat an old `git status` capture as live state or unrelated changes as task evidence.
- Do not compress a proof conflict into a reassuring summary.

## Reference Map

- [Recap templates](references/templates.md) — load after N2 reconciles the task state.
- [Ticket and Goal Packet contract](../../tickets/README.md) — load when a ticket or Goal Packet is present.

## Output

Return a filled quick, full, or source-gap template followed by one safe next
posture. Keep literal source paths in full mode. Write nothing.
