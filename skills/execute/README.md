# Execute

## Purpose

Define the Tier 2 execution interface that domain-specific skills implement.

## Public API / Entrypoints

- `SKILL.md`: generic execution interface
- `SKILL.md` Todo List: execution checklist
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read the plan and proof contract.
2. Do the scoped work.
3. Run proof.
4. Write evidence and handoff state.
5. Review before completion.

## How To Test

- Confirm the skill stays domain-neutral.
- Confirm coding-specific execution still belongs to `$impl` and closeout to
  `close-ticket`.
- Confirm completion claims require durable evidence.
