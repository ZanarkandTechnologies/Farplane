---
name: close-ticket
description: Parent closeout skill for one selected ticket. Use when implementation and review are done and the remaining work is durable docs writeback, final checks, commit prep, and optional push/publish.
tier: 3
group: coding
source: local
---

# Close Ticket

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Resolve exactly one active ticket and confirm the remaining work is
  genuinely closeout, not missing implementation.
- [ ] Treat this skill as `CloseTicket<CodingTicket>` inside the
  [project-lifecycle](../deep-init-project/references/project-lifecycle.md).
- [ ] Use the generic [execute](../execute/SKILL.md) interface's proof and
  writeback shape, but keep `close-ticket` coding-ticket closeout specific.
- [ ] Update the ticket writeback: evidence, linked docs, handoff, next action,
  and `last_verification`.
- [ ] Update durable docs that changed in the final pass: `docs/HISTORY.md`,
  `docs/MEMORY.md`, `docs/TROUBLES.md`, README, or the nearest `AGENTS.md`.
- [ ] Run the feature closeout consistency sweep for relevant surfaces:
  `README.md`, `ARCHITECTURE.md`, `docs/specs/README.md`,
  `docs/skills/README.md`, `docs/skills/registry.jsonl`,
  `docs/features/registry.jsonl`, and nearest module `README.md`/`AGENTS.md`.
- [ ] If the final proof or linked review artifact is stale, re-enter the
  [execute](../execute/SKILL.md) proof/review closeout shape before closing
  the ticket.
- [ ] Run the repo-local validators and final checks that actually match the
  touched surfaces.
- [ ] Use the [Commit Message](../commit-message/SKILL.md) skill for the commit
  subject.
- [ ] If heavy explicit pre-push review is needed, use
  [CodeRabbit Review](../coderabbit-review/SKILL.md).
- [ ] Commit only the intended closeout slice.
- [ ] Push only when the user or workflow explicitly calls for publishing.
- [ ] Leave the ticket clearly archive-ready, committed, blocked, or still in
  documenting with one concrete next action.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

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

Use the Important Checklist above as the parent closeout sequence.

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

Run a feature closeout consistency sweep before commit:

- `README.md` and `ARCHITECTURE.md` when the top-level product or workflow map
  changed
- `docs/specs/README.md` when a spec is added, moved, renamed, or retired
- `docs/skills/README.md` and `docs/skills/registry.jsonl` when skills,
  skill metadata, method addresses, direct checklists, or skill docs changed
- `docs/features/registry.jsonl` when a shipped capability is added, renamed,
  retired, or materially changes status
- nearest module `README.md` or `AGENTS.md` when a local contract changed

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
