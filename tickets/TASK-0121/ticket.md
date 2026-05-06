---
ticket_id: TASK-0121
title: define explicit Codexter invocation triggers
phase: planning
status: review
owner: codex
claimed_by:
priority: high
depends_on:
  - TASK-0120
blocked_by: []
ready: false
approval_required: true
requires_qa: false
requires_demo: false
created_at: 2026-05-06T17:18:41Z
updated_at: 2026-05-06T17:18:41Z
next_action: review the explicit invocation-trigger contract
last_verification: planned on 2026-05-06 after Codexter/Symphony scope reset
---

# TASK-0121: define explicit Codexter invocation triggers

## Summary
Define the small set of explicit triggers that mean "Codexter should act on
this ticket." The goal is to support local chat, ticket comments, Codex Cloud
payloads, and future Symphony payloads without introducing a polling daemon or
auto-running draft tickets.

## Scope
- In:
  - Define `InvocationTrigger` vocabulary for local chat, ticket comment,
    Codex Cloud task, and Symphony worker payloads.
  - Update `CodexterRunEnvelope` docs/examples so `requestedBy` and `mode`
    clearly represent invocation intent.
  - Add examples such as `@codexter plan TASK-0124`,
    `@codexter implement`, and "run this ticket locally".
  - Clarify that comment triggers are conventions for a caller to translate
    into an envelope; Codexter does not listen to comments by itself.
  - Add fixture tests or examples proving local `prepare` still routes one
    selected ticket without side effects.
- Out:
  - No webhook server.
  - No Notion/Linear comment listener.
  - No automatic transition from `ready: true` to running.
  - No new CLI product claim beyond the existing diagnostic helper.

## Plan
- `Change:` Add an invocation-trigger layer to the docs and helper examples so
  explicit human intent is the only start signal.
- `Why:` Ticket creation is often part of thinking. Codexter should wait until
  the user invokes the agent, even if the board later lives in Linear or Notion.
- `Before -> After:`
  - Before: `CodexterRunEnvelope` exists, but there is no crisp trigger
    vocabulary explaining who creates it and when.
  - After: each start path maps to a trigger and then to one envelope; comments
    or cloud tasks are just sources of invocation intent.
- `Touch:`
  - `docs/specs/board-compute-orchestration.md`
  - `docs/specs/symphony-compatible-codexter-runner.md`
  - `skills/codexter-invocation/SKILL.md`
  - `skills/codexter-invocation/README.md`
  - `skills/codexter-invocation/references/symphony.md`
  - `skills/codexter-invocation/templates/symphony-run-envelope.json`
  - `bin/codexter_invocation.py` only if a small `mode` or example validation
    update is needed.
  - `bin/test_codexter_invocation.py`
- `Inspect:`
  - `WORKFLOW.md`
  - `bin/codexter_boards.py`
  - `bin/codexter_compute.py`
  - `tickets/README.md`
  - `docs/MEMORY.md`
- `Signature delta:`
  - `docs/specs/... / InvocationTrigger`
  - `skills/codexter-invocation/SKILL.md / Workflow`
  - optional `bin/codexter_invocation.py / parse_run_envelope(source, root): CodexterRunEnvelope`
  - optional `bin/test_codexter_invocation.py / test_comment_style_trigger_fixture`
- `Type Sketch:`
  - `InvocationTrigger`:
    - `kind`: `local_chat | ticket_comment | codex_cloud | symphony_worker`
    - `command`: `plan | implement | qa | review | close`
    - `workItem`: ticket id/path/url reference
    - `actor`: human, service, or external runner label
  - `CodexterRunEnvelope`:
    - existing `mode`, `requestedBy`, `phase`, `workItemId`,
      `computeTarget`, `proofPacketPath`
    - no listener/session ids in ticket frontmatter.
- `Typed flow example:`
  1. User writes a Linear comment: `@codexter implement`.
  2. A future Linear adapter or Symphony workflow constructs:
     `{mode: "external_runner", workItemId: "...", phase: "building"}`.
  3. Codexter reads the envelope inside normal Codex.
  4. BoardAdapter normalizes the ticket.
  5. ComputeSelector admits or blocks the requested target.
  6. The routed skill runs and writes proof.
- `Execution steps:`
  1. Add the `InvocationTrigger` concept to the system specs.
  2. Update local and comment examples in the invocation skill docs.
  3. Keep the actual helper read-only and diagnostic.
  4. Add or update tests that show envelope preparation works for local chat
     and external/comment-shaped modes.
  5. Add grep checks for "ticket created => run" style wording and remove it.
- `Recommendation:` Land this after `TASK-0120`; it turns the mental model into
  a usable trigger contract without adding infrastructure.
- `Options considered:`
  - Local chat only: simplest, but loses future shared-board clarity.
  - Comment grammar plus envelope: recommended; explicit, extensible, and
    still no daemon.
  - Webhook listener: useful later, but premature and outside Codexter's core.
- `Blast radius:` invocation docs, examples, tests, future adapter tickets.
- `Risks:`
  - Accidentally implying Codexter reads comments itself. Containment: call
    comments a caller-side convention until an adapter ticket exists.
  - Making the envelope schema too broad. Containment: reuse existing fields
    unless one missing field blocks an example.

## Gap Analysis
- `Current state:` Envelopes exist, but trigger ownership is implicit.
- `Production expectation:` Multi-entry systems distinguish draft work, ready
  work, and explicit invocation.
- `Missing gaps:` no trigger grammar, no comment examples, and no source-to-
  envelope explanation for Codex Cloud/Symphony.
- `Comparable implementations:` GitHub slash commands, Linear agent comments,
  Codex Cloud task commands, Symphony workflow prompts.
- `Recommendation:` define the trigger vocabulary now; build listeners only
  when a real board adapter needs them.

## Acceptance Criteria
- [ ] Specs define explicit invocation as the start signal.
- [ ] Ticket comments are documented as an input convention, not an active
  listener.
- [ ] `CodexterRunEnvelope` examples cover local chat and future external
  caller flows.
- [ ] Existing local invocation tests still pass.

## Verification
- `Tests:`
  - `python3 -m unittest bin/test_codexter_invocation.py`
  - `python3 -m py_compile bin/codexter_invocation.py`
  - `python3 tickets/scripts/check_ticket_metadata.py`
- `Manual checks:`
  - `python3 bin/codexter_invocation.py prepare --ticket TASK-0085 --phase building --proof .harness/results/task-0085.proof.json`
  - Grep docs for stale auto-run or listener claims.
- `Evidence required:`
  - Prepared invocation JSON or test output showing one explicit trigger maps
    to one route.

## Autonomy Readiness
- `Human inputs/assets:` approval of trigger vocabulary.
- `Credentials / external access:` none.
- `Compute/runtime needs:` local Python only.
- `Tooling gaps:` none for docs/tests; external listeners deferred.
- `QA risks:` examples could overpromise external behavior; keep wording
  explicit.
- `Human gates:` approval required.
- `Agent decision boundaries:` may update docs/examples/tests; may not build a
  listener or daemon.

## Refs
- [Codexter invocation skill](/Users/kenjipcx/coding-harness/Codexter/skills/codexter-invocation/SKILL.md)
- [Symphony-compatible runner spec](/Users/kenjipcx/coding-harness/Codexter/docs/specs/symphony-compatible-codexter-runner.md)
- [WORKFLOW.md](/Users/kenjipcx/coding-harness/Codexter/WORKFLOW.md)

## Evidence
- `Artifacts:`
  - [next-batch plan review](/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-0120/artifacts/review/2026-05-06-next-batch-plan-review.json)
- `Commands:`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check -- tickets/TASK-0120/ticket.md tickets/TASK-0121/ticket.md tickets/TASK-0122/ticket.md tickets/TASK-0123/ticket.md`
  - `python3 skills/ralph/scripts/select_next_ticket.py --root . --json`
- `Result summary:`
  - Planning ticket created and approval-gated; depends on the terminology reset in `TASK-0120`.

## Blockers
- awaiting approval
