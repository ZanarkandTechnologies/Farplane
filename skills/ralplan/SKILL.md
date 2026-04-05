---
name: ralplan
version: 0.1.0
description: "Plan one ticket into an executable slice before Ralph implementation."
---

# Ralphplan

Use this when a ticket exists but its implementation plan is still missing, stale, or untrusted.

## Job

1. Resolve the active ticket from the current run state or explicit ticket selector.
2. Inspect linked specs and the relevant code.
3. Write or repair the implementation plan inside the ticket.
4. Optionally use review/challenge `subagents` to tighten the plan.
5. Emit one `RALPH_RESULT`.
6. Stop and let the `Stop` `hook` judge whether the ticket can advance to `building`.

## Use When

- a ticket is in `review`
- the next step is planning, not implementation
- the implementation approach needs to be made explicit before coding starts

## Do Not Use When

- the user is still deciding what to build; use `brainstorm` or `deep-interview`
- the ticket is already approved for implementation; use `ralph`
- the user wants end-to-end freeform ideation instead of a bounded build plan

## Runtime Model

Ralphplan is the planning half of the same system:

- one ticket
- one bounded planning skill
- optional critic/challenge `subagents`
- one `Stop` `hook` judge

The ticket stores the plan.

## Required Reads

- current run state: `.ralph/state/current-run.json`
- active ticket
- linked specs / PRD
- relevant code only

## Required Write-Back

Update the ticket with:

- implementation plan
- touched areas / likely files
- constraints or blockers
- `next_action`

## Result Contract

Emit exactly one final line:

`RALPH_RESULT: status=<enum> next=<enum> reason=<optional>`

Supported statuses:

- `plan_ready`
- `continue_ralphplan`
- `blocked`

Typical next values:

- `building`
- `planning`
- `none`

## Important Boundary

Ralphplan creates the executable plan.
It does **not** implement the ticket.

After the plan is accepted, the next step is `ralph`.
