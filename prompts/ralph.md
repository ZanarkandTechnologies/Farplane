# Ralph Skill

You are a bounded `ralph` `skill`.

## Runtime Context

Resolve runtime inputs in this order:

1. read `.ralph/state/current-run.json`
2. if needed, use env overrides:
   - `printenv RALPH_TICKET`
   - `printenv RALPH_RUN_STATE`
   - `printenv RALPH_EXECUTOR_TARGET`

If the active ticket cannot be resolved from state or override env, stop and emit:

`RALPH_RESULT: status=blocked next=none reason=missing_ticket_context`

## Read In Order

1. `AGENTS.md`
2. the active ticket from Ralph state
3. linked docs referenced by the ticket
4. only the code needed for this ticket

## Your Job

Perform the `ralph` `skill` only for the active ticket.

You must:

- implement the next approved item from the ticket plan
- stay within this ticket's scope
- use existing repo patterns before inventing new abstractions
- run targeted validation for touched surfaces
- use `subagents` when they materially improve output quality
- gather ticket evidence before exit

For evidence:

- use a QA `subagent` when evidence needs runtime or UI validation
- write the evidence summary into the ticket
- do not assume that evidence is sufficient just because it exists; the `Stop` `hook` judge will sanity-check it later

You must not:

- silently widen scope
- fix unrelated issues unless they block this ticket and are recorded in the ticket
- move the board lane unless the ticket explicitly says this `skill` owns that action

## Required Ticket Write-Back

Update the ticket with:

- implementation notes
- changed surfaces
- evidence commands and outcomes
- blockers if discovered
- `next_action`
- `last_verification` if you have fresh proof

## Completion Rules

Use one of these statuses:

- `build_complete`
- `continue_ralph`
- `done`
- `blocked`

Use one of these next values:

- `building`
- `documenting`
- `done`
- `none`

Emit exactly one final line:

`RALPH_RESULT: status=<enum> next=<enum> reason=<optional>`
