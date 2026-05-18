---
name: batch-work
description: Execute a user-specified range or list of tickets in one unattended pass. Load one ticket at a time, expand its todos into an external batch todo file, keep moving when a ticket blocks, and summarize completed work plus blockers at the end.
tier: 2
source: local
---

# Batch Work

Use this when the operator types `batch-work` or asks to process a range/list of
tickets without stopping after every ticket.

## Job

1. Parse the ticket range or explicit ticket list from the user.
2. Use the repo-level batch todo file outside the chat transcript.
3. Expand only the current ticket into the active todo list.
4. Implement the current ticket using its owning skills and checks.
5. If blocked, write the blocker to `blockers.md` and continue to the next
   ticket.
6. Review the batch after the range is exhausted.
7. Present per-ticket results and blockers.

## Use When

- The user says `batch-work`.
- The user gives a ticket range such as `TASK-0143 to TASK-0147`.
- The user says they will be away and wants progress across several known
  tickets.
- The tickets already exist and carry enough scope to attempt one at a time.

## Do Not Use When

- No ticket range or list is supplied.
- The work requires publish/deploy/spend/destructive actions that the user did
  not explicitly authorize.
- A ticket's target is ambiguous enough that continuing would risk unrelated
  work; record the blocker and continue.

## Workflow

1. Read the batch context surfaces:
   - `tickets/README.md` for ticket state and evidence rules
   - `docs/skills/README.md` and `docs/skills/registry.jsonl` for skill
     ownership, tier, source, and todos presence
   - `docs/features/README.md` and `docs/features/registry.jsonl` for harness
     capability names and shipped/implemented feature context
   - `docs/specs/README.md` for canonical spec surfaces when the tickets point
     at specs
   - `docs/MEMORY.md` and `docs/TROUBLES.md` for durable constraints and
     repeated misses
2. Use root `todos.md` as the active batch todo file. Create it if missing.
3. Use root `blockers.md` as the blocker log. Create it if missing.
4. Add the top-level ticket range to `todos.md`:

```markdown
# Batch Todos

- [ ] TASK-0143
- [ ] TASK-0144
- [ ] TASK-0145
```

5. For the current ticket only, replace that ticket line in `todos.md` with the
   ticket's concrete todo/checklist items. Do not expand the whole range at
   once.
6. Load the ticket's relevant skill todos into the active checklist only for the
   current ticket.
7. Implement the ticket and run its proof checks.
8. If blocked:
   - record ticket id, blocker, evidence, attempted actions, and recommended
     next action in `blockers.md`
   - mark that ticket blocked in the batch todo file
   - continue with the next ticket
9. Use [advise](../advise/SKILL.md) when stuck on a ticket and a bounded
   recommendation could unblock or classify the blocker.
10. After the final ticket, run the batch-level checks and [review](../review/SKILL.md).
11. Return a per-ticket summary: done, changed, proof, blocked, and follow-up.

## Reference Surfaces

- [tickets/README.md](../../tickets/README.md): ticket state machine,
  metadata, evidence, and artifact conventions.
- [docs/skills/README.md](../../docs/skills/README.md): skill registry
  contract and skill-system validation commands.
- [docs/skills/registry.jsonl](../../docs/skills/registry.jsonl): generated
  skill tier/source/todos/link map.
- [docs/features/README.md](../../docs/features/README.md): harness feature
  registry contract.
- [docs/features/registry.jsonl](../../docs/features/registry.jsonl):
  implemented/planned harness capabilities and feature names.
- [docs/specs/README.md](../../docs/specs/README.md): canonical spec index.
- [docs/MEMORY.md](../../docs/MEMORY.md): durable constraints.
- [docs/TROUBLES.md](../../docs/TROUBLES.md): repeated misses and prevention
  notes.

## Decision Branches

- **Ticket passes:** mark it done in `todos.md` and continue.
- **Ticket blocks:** write `blockers.md`, use advice if useful, then continue.
- **Ticket requires forbidden external side effect:** block it and continue.
- **Batch-level validation fails:** record whether the failure belongs to a
  specific ticket or the batch infrastructure.

## Outcome Contract

Return or write:

- batch run folder path
- root `todos.md`
- root `blockers.md`
- per-ticket changed files and proof
- batch-level review result
- final summary of completed tickets and blocked tickets
