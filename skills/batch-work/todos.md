# Todos

- [ ] Parse the user-specified ticket range or explicit ticket list.
- [ ] Read the relevant context surfaces:
  `tickets/README.md`, `docs/skills/README.md`,
  `docs/skills/registry.jsonl`, `docs/features/README.md`,
  `docs/features/registry.jsonl`, `docs/specs/README.md`,
  `docs/MEMORY.md`, and `docs/TROUBLES.md`.
- [ ] Use root `todos.md` for the batch todo list and root `blockers.md` for
  blockers, creating either file only if missing.
- [ ] Add the ticket ids as top-level todos in `todos.md`; do not expand every
  ticket at the start.
- [ ] Expand only the current ticket into concrete todos, including the ticket's
  own checklist and relevant skill todos.
- [ ] Use `$work` admission policy to decide whether the next
  item stays single-ticket or can safely join a related tiny-ticket group.
- [ ] Implement the current ticket and run its proof checks.
- [ ] For grouped tiny tickets, maintain one proof row per ticket plus one
  batch-level regression row.
- [ ] When stuck, use [advise](../advise/SKILL.md) to classify the blocker or
  recommend the next bounded move.
- [ ] If still blocked, write the blocker to `blockers.md`, mark the ticket
  blocked in the batch todo file, and continue to the next ticket.
- [ ] After the range is exhausted, run batch-level checks and
  [review](../review/SKILL.md).
- [ ] Present completed tickets, blocked tickets, proof, and next actions.
