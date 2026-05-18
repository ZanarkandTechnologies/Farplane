---
name: close-ticket
description: Parent closeout skill for one selected ticket. Use when implementation and review are done and the remaining work is durable docs writeback, final checks, commit prep, and optional push/publish.
tier: 3
group: coding
---

# Close Ticket

Use this skill when one ticket is functionally done and the remaining work is
to close it cleanly instead of doing more implementation.

`close-ticket` is a Tier 3 Codexter coding-pipeline closeout skill. It consumes
the generic [execute](../execute/SKILL.md) interface's proof/writeback shape but
keeps Codexter-specific ticket, docs, commit, and archive rules here.

This is the canonical public closeout surface. `$docs-closeout` is a backward
compatible alias, not the preferred live name.

## Contract

- resolve exactly one active ticket
- assume implementation is already complete or explicitly paused
- perform closeout work in order: writeback, checks, commit prep, optional push
- keep the ticket as the durable progress surface
- do not reopen implementation scope unless a real blocker or failing check
  forces a same-ticket return to build work

## First-Load Checklist

Ensure an agent can execute the core path after only reading this file.

- Trigger conditions:
  - the ticket is in `phase: documenting` or otherwise in final closeout
  - implementation and verification are already done enough that the remaining
    work is docs, proof cleanup, commit, and publication
  - the user asks to close out, archive, document, commit, or push a finished
    ticket
- Workflow:
  1. resolve one ticket and confirm it is really in closeout, not missing
     implementation or review
  2. update the ticket writeback fields and any durable docs that changed
  3. run the repo-local checks appropriate to the touched files
  4. rerun [review](../review/SKILL.md) only if the review packet or proof is
     stale or missing for the final state
  5. use [commit-message](../commit-message/SKILL.md) to pick the commit
     subject
  6. make the commit when the repo state is ready
  7. push only when the user or workflow explicitly calls for publishing
  8. leave the ticket archive-ready with clear handoff state
- Core decision branches:
  - docs/proof only -> write back, validate, close
  - missing final review/proof -> refresh review before commit
  - failing checks or discovered blocker -> return `continue_impl` or `blocked`
- Top 3 gotchas:
  - do not treat unfinished implementation as closeout
  - do not push automatically unless the user or workflow explicitly called for it
  - do not let commit prep hide missing ticket or doc writeback
- Outcome contract:
  - ticket evidence, handoff, linked docs, next action, and verification are updated
  - durable docs such as `docs/HISTORY.md`, `docs/MEMORY.md`, and `docs/TROUBLES.md`
    are updated when needed
  - the repo has run the appropriate closeout checks
  - commit and push state are explicit in the ticket and final result

## Ordered Flow

Use the checklist in [todos.md](./todos.md) as the parent closeout sequence.

Related skills:

- [review](../review/SKILL.md) for final scored review when the packet is stale,
  missing, or invalidated by the closeout delta
- [commit-message](../commit-message/SKILL.md) for the final subject line
- [coderabbit-review](../coderabbit-review/SKILL.md) only when a heavy explicit
  pre-push or PR review is warranted

## Required Write-Back

Update the selected ticket with:

- final evidence summary
- linked durable docs
- final handoff notes
- next action
- last verification
- clear closeout outcome: archived, ready to archive, committed, or blocked

Update durable docs when the closeout pass changes durable repo truth:

- `docs/HISTORY.md`
- `docs/MEMORY.md`
- `docs/TROUBLES.md`
- nearest README or AGENTS surface when the user-visible contract changed

## Checks

Run the smallest truthful final checks for the touched surfaces.

Prefer repo-local validator scripts or ticket-specific commands first:

- ticket metadata validator when ticket fields changed
- doc parity or harness invariants when canonical docs/runtime contracts changed
- tests, lint, typecheck, or pre-push checks when the underlying code changed

Do not claim closeout is done if the final ticket state and final verification
summary are stale.

## Commit And Push

- commit only the intended closeout slice
- keep unrelated dirty work out of the closeout commit
- push only when the user or workflow explicitly wants publishing
- if publishing is out of scope, state that clearly instead of implying it happened

## Completion

Emit exactly one final line:

`IMPL_RESULT: status=<enum> next=<enum> reason=<optional>`

Allowed statuses:

- `close_ticket_complete`
- `continue_impl`
- `blocked`

Allowed next values:

- `done`
- `documenting`
- `none`
