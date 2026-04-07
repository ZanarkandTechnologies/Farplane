---
name: docs-closeout
description: Documentation and archive-prep pass for one selected ticket.
---

# Docs Closeout

Use this skill when a ticket has finished implementation and verification and
only documenting/writeback/archive preparation remains.

## Contract

- resolve exactly one active ticket
- perform documentation and handoff work only
- update ticket evidence, handoff, linked docs, next action, and verification summary
- prepare the ticket for archive-ready state
- do not reopen implementation scope unless a real documentation blocker requires it

## Required Write-Back

Update the ticket with:

- final evidence summary
- linked durable docs
- final handoff notes
- next action
- last verification

## Completion

Emit exactly one final line:

`RALPH_RESULT: status=<enum> next=<enum> reason=<optional>`

Allowed statuses:

- `docs_complete`
- `continue_ralph`
- `blocked`

Allowed next values:

- `done`
- `documenting`
- `none`
