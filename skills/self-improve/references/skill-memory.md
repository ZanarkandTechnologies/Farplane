# Self Improve Goal Packet Ownership

Material self-improvement uses the standard ticket Goal Packet:

```text
tickets/TASK-XXXX/
  ticket.md
  program.md
  progress.md
  artifacts/native-goal-prompt.md
```

`goal-advisor` instantiates
[`goal-program-template.md`](goal-program-template.md) into `program.md` and
compiles the native prompt. The packet starts `approval: pending`; execution
begins only after the operator approves the current ticket, program, progress
scaffold, and prompt. `compiled_from_ticket_updated_at` makes stale packets
block and regenerate.

The target skill does not own lifecycle state. Pre-existing
`skills/<target>/self-improve/*` files are legacy experiment notes only unless
an explicit separate contract owns them; self-improve never reads, writes,
generates, parses, or migrates them as Goal state.

Use ticket `progress.md` for compact turn observations. Link generated Eval
runs rather than copying bulky output or creating a structured event schema.
