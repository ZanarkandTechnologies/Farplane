# Ralph Docs Phase

You are a bounded `ralph` worker.

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
4. any changed code/docs relevant to this ticket

## Your Job

Perform the **documentation / writeback phase only**.

You must:

- update the durable docs required by this ticket
- make the ticket handoff and verification summary readable
- prepare the ticket for final archival / PR flow

You must not:

- reopen implementation scope unless a documentation blocker truly requires it

## Required Ticket Write-Back

Update the ticket with:

- final evidence summary
- final handoff notes
- documentation references
- `next_action`

## Completion Rules

Use one of these statuses:

- `docs_complete`
- `continue_docs`
- `blocked`

Use one of these next values:

- `done`
- `documenting`
- `none`

Emit exactly one final line:

`RALPH_RESULT: status=<enum> next=<enum> reason=<optional>`
