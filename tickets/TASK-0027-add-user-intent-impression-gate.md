---
ticket_id: TASK-0027
title: add user intent impression gate
phase: planning
status: review
owner: codex
priority: high
depends_on:
  - TASK-0025
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-08T01:54:29Z
updated_at: 2026-04-08T01:54:29Z
next_action: review and approve the user-intent gate slice before implementation starts
last_verification: backlog ticket created from cross-source harness gap analysis
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/review-gates.md
---

# TASK-0027: add user intent impression gate

## Summary
Add a final review layer that checks whether the finished output would actually satisfy or impress the original user request, not just the internal ticket story.

## Scope
- In: preserving the original request as a durable artifact, adding a final user-intent comparison step, and routing failures back into the same ticket loop
- Out: product-analytics or post-deploy satisfaction measurement

## Plan

### Pitch
- `Req:` fix the current weakness where the harness can satisfy the ticket mechanically but still miss the actual user ask
- `Bet:` add one explicit final gate that compares output, evidence, and ticket against the original user intent
- `Win:` better alignment with what the user actually wanted, not just what the implementor built

### B -> A
- `Before:` the original ask mostly lives in chat memory or diffuse ticket prose
- `After:` the original ask becomes a durable review input and a final judge step
- `Outcome:` the system can reject outputs that are internally coherent but unconvincing to the user

### Delta
- `Touch:` ticket or run artifact shape, review/QA contract, Stop-hook or closeout gating
- `Keep:` ticket as the main execution object
- `Change:` add a final “does this satisfy the original ask?” check
- `Delete/Avoid:` assuming ticket completion automatically implies user satisfaction

### Core Flow
```pseudo
store original ask in the durable work artifact
build and gather evidence normally
compare final output and evidence against the original ask
if misaligned, repeat the same ticket with the gap called out explicitly
```

### Proof
- `P1:` a replay case catches a ticket that is internally coherent but weak against the original user request
- `P2:` the final gate produces concrete mismatch reasons, not vague taste commentary
- `Risk:` this becomes a duplicate of general review
- `Rollback:` constrain it to final user-alignment checks only

### Plan Review
- `Refs:` OpenAI’s user-centered harness framing, Anthropic’s evaluator contract, `harness-techniques.md`, `review-gates.md`, `tickets/templates/ticket.md`
- `Scope:` one final-gate addition, not a full intake/runtime redesign
- `Proof:` replay a ticket where “done” and “impressive to the user” diverge
- `Guardrails:` do not add hidden chat scraping or opaque heuristics
- `Fixes:` keep the comparison explicit and artifact-backed

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` move to building and add the user-intent gate to the durable work artifact plus final review path

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and implement the durable original-ask capture plus final gate
- `Follow-ups:` may split into one artifact-shape ticket and one review-loop ticket if the slice expands
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: the original user ask is captured in a durable artifact used during final review
- [ ] AC-2: the review loop can fail a ticket for user-intent mismatch even when lower-level checks pass
- [ ] AC-3: at least one replayable case demonstrates the gate catching a misaligned output

## Working Notes
- Main weakness: the system can be internally correct and still not feel impressive to the user.
- Blog technique mapping: OpenAI’s user-centered harness emphasis plus Anthropic’s explicit evaluator contract.
- This complements `TASK-0025`, which captures turn-start intent for stop-hook alignment; this ticket adds the later final-review gate against that durable intent.

## Implementation Notes
- Touched areas: ticket or run artifact contract, final review packet, Stop-hook or closeout routing
- Reused patterns: current review packet and ticket writeback model
- Guardrails: keep the original ask visible and explicit

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- `reviewed_at:` 2026-04-08 01:54 +0100
- `rubrics_used:` implementation-plan,evidence-quality
- `overall_score:` 93
- `overall_verdict:` pass
- `rerun_required:` false
- `blocking_findings:` none
- `next_action:` hold in review until approved for implementation

## Blockers
- none

## Handoff
- Current state: planning ticket created for the explicit user-intent final gate.
- Resume from: `docs/specs/harness-techniques.md`

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
