---
ticket_id: TASK-0030
title: encode mechanical harness invariants
phase: planning
status: review
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-08T01:54:29Z
updated_at: 2026-04-08T01:54:29Z
next_action: review and approve the invariant-enforcement slice before implementation starts
last_verification: backlog ticket created from cross-source harness gap analysis
linked_docs:
  - docs/specs/harness-techniques.md
  - AGENTS.md
  - docs/MEMORY.md
---

# TASK-0030: encode mechanical harness invariants

## Summary
Turn a few high-value harness rules from prompt guidance into real validators or lints so the system relies less on instruction-following alone.

## Scope
- In: selecting a small set of invariants, encoding them mechanically, and surfacing remediation-grade failures
- Out: broad policy rewrite or heavy static analysis infrastructure

## Plan

### Pitch
- `Req:` fix the weakness where key harness rules are stated in prompts and docs but not mechanically enforced
- `Bet:` encode a small number of high-value invariants instead of trying to lint everything
- `Win:` less drift, more reliable harness behavior, and clearer failure messages

### B -> A
- `Before:` many harness invariants live in `AGENTS.md`, `MEMORY`, and skill text only
- `After:` the most important invariants are checked by code, not only remembered by the agent
- `Outcome:` faster feedback and less silent drift

### Delta
- `Touch:` validators/scripts/rules plus the canonical docs that define the invariants
- `Keep:` human-readable rules as the policy source
- `Change:` add machine-checkable enforcement for selected invariants
- `Delete/Avoid:` sprawling lint coverage with low-signal failures

### Core Flow
```pseudo
select 1-3 high-value invariants
encode them as validators with clear remediation messages
run them in the normal ticket/docs workflow
use failures to prevent drift
```

### Proof
- `P1:` at least one existing or simulated drift case fails the new invariant check
- `P2:` failure output tells the agent or operator exactly how to repair the issue
- `Risk:` too many low-value rules create noise
- `Rollback:` keep only the few invariants that catch real mistakes

### Plan Review
- `Refs:` OpenAI mechanical-invariant emphasis, `harness-techniques.md`, root `AGENTS.md`, `docs/MEMORY.md`, existing ticket validator patterns
- `Scope:` a narrow first set of invariants
- `Proof:` validator tests or representative fixture failures
- `Guardrails:` do not replace docs with validators; use validators to backstop them
- `Fixes:` start with the most common drift paths only

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` move to building and implement the first small invariant set

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and implement the initial validators
- `Follow-ups:` may split doc invariants from runtime or ticket invariants if scope grows
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: 1-3 high-value harness invariants are encoded mechanically
- [ ] AC-2: failures provide clear remediation guidance
- [ ] AC-3: at least one representative drift case proves the validators catch a real problem

## Working Notes
- Main weakness: prompt-only rules are too easy for fast-moving agents to violate.
- Blog technique mapping: OpenAI’s recommendation to encode knowledge and constraints mechanically where possible.

## Implementation Notes
- Touched areas: validators/rules, maybe bin scripts, canonical doc references
- Reused patterns: existing ticket metadata checking and explicit invariant logging
- Guardrails: prefer high-value invariants over coverage breadth

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- `reviewed_at:` 2026-04-08 01:54 +0100
- `rubrics_used:` implementation-plan,evidence-quality
- `overall_score:` 94
- `overall_verdict:` pass
- `rerun_required:` false
- `blocking_findings:` none
- `next_action:` hold in review until approved for implementation

## Blockers
- none

## Handoff
- Current state: planning ticket created for mechanical invariant enforcement.
- Resume from: `docs/specs/harness-techniques.md` and `docs/MEMORY.md`

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
