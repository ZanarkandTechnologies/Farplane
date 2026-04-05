---
name: ralph
version: 0.1.0
description: "Run one ticket through the bounded Ralph execution skill and let the Stop hook judge whether to repeat or advance."
---

# Ralph

Use this when a ticket is already in `tickets/building/` and the next step is implementation with evidence gathering.

## Job

1. Resolve the active ticket from the current run state or explicit ticket selector.
2. Implement the current approved slice for that ticket.
3. Gather evidence, using QA `subagents` when useful.
4. Update the ticket.
5. Emit one `RALPH_RESULT`.
6. Stop and let the `Stop` `hook` judge whether to repeat, advance, block, or complete.

## Use When

- a ticket is in `building`
- the implementation plan already exists
- the user wants the system to keep working the same ticket until the evidence is good enough
- a small or medium ticket should move through one bounded execution pass

## Do Not Use When

- the ticket still needs planning; use `ralplan`
- the idea is still vague; use `brainstorm`, `deep-interview`, or `prd`
- the user only wants explanation or review, not execution

## Runtime Model

Ralph is not an infinite chat.

It is:

- one ticket
- one bounded execution skill
- optional QA `subagents`
- one `Stop` `hook` judge

The ticket is the durable memory.
The transcript is disposable.

## Required Reads

- current run state: `.ralph/state/current-run.json`
- active ticket
- linked docs referenced by the ticket
- relevant code only

## Required Write-Back

Update the ticket with:

- implementation notes
- changed surfaces
- evidence
- blockers
- `next_action`
- `last_verification`

## Result Contract

Emit exactly one final line:

`RALPH_RESULT: status=<enum> next=<enum> reason=<optional>`

Supported statuses:

- `build_complete`
- `continue_ralph`
- `done`
- `blocked`

Typical next values:

- `building`
- `documenting`
- `done`
- `none`

## Important Boundary

Ralph gathers evidence.
Ralph does **not** decide whether that evidence is sufficient.

That decision belongs to the `Stop` `hook` judge.
