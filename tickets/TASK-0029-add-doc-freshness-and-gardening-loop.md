---
ticket_id: TASK-0029
title: add doc freshness and gardening loop
phase: planning
status: review
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-08T01:54:29Z
updated_at: 2026-04-08T01:54:29Z
next_action: review and approve the docs-freshness slice before implementation starts
last_verification: backlog ticket created from cross-source harness gap analysis
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/specs/README.md
  - AGENTS.md
---

# TASK-0029: add doc freshness and gardening loop

## Summary
Make the repo’s docs-as-system-of-record claim more trustworthy by adding freshness checks and a recurring doc-gardening workflow.

## Scope
- In: doc link/freshness validation, canonical-surface checks, and a repeatable documentation-maintenance pass
- Out: content-heavy documentation rewrites unrelated to the harness

## Plan

### Pitch
- `Req:` fix the weakness where canonical docs exist, but nothing mechanical prevents drift or stale cross-links
- `Bet:` add a small validator plus a recurring maintenance loop instead of relying on memory
- `Win:` the harness docs become dependable enough to serve as actual agent grounding

### B -> A
- `Before:` docs are canonical by convention, but not mechanically freshness-checked
- `After:` stale or drifting canonical surfaces are easier to detect and clean up
- `Outcome:` repo legibility becomes more trustworthy over time

### Delta
- `Touch:` doc validation scripts/rules, documentation-maintainer workflow, maybe README/spec index enforcement
- `Keep:` docs-first structure and progressive disclosure
- `Change:` add freshness enforcement and recurring cleanup
- `Delete/Avoid:` assuming canonical docs stay fresh on their own

### Core Flow
```pseudo
define what canonical docs must stay in sync
validate links and required references mechanically
run a recurring doc-gardening pass
surface drift as explicit findings instead of silent rot
```

### Proof
- `P1:` the validator catches at least one realistic stale-doc or missing-link case
- `P2:` the maintenance pass has a bounded, repeatable output shape
- `Risk:` overbuilt doc tooling for a lightweight problem
- `Rollback:` keep the validator narrow and only cover canonical harness docs

### Plan Review
- `Refs:` OpenAI docs-as-system-of-record and cleanup emphasis, `harness-techniques.md`, `docs/specs/README.md`, root `AGENTS.md`
- `Scope:` canonical harness docs only
- `Proof:` run the validator and exercise one maintenance pass
- `Guardrails:` do not turn this into a full docs site generator
- `Fixes:` start with a narrow validator over high-value docs only

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` move to building and implement the validator plus maintenance loop

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and implement the freshness checks
- `Follow-ups:` may split validator and maintainer-pass work if needed
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: a narrow validator checks key canonical harness docs for freshness or required cross-links
- [ ] AC-2: one repeatable doc-gardening workflow exists for maintaining canonical harness docs
- [ ] AC-3: the new checks catch at least one representative drift case in development or tests

## Working Notes
- Main weakness: docs are good, but still depend on human memory to stay trustworthy.
- Blog technique mapping: OpenAI’s docs-as-system-of-record and cleanup/gardening posture.

## Implementation Notes
- Touched areas: doc validation surface, documentation maintenance workflow, canonical doc references
- Reused patterns: docs/specs as source of truth
- Guardrails: stay narrow and high-signal

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- `reviewed_at:` 2026-04-08 01:54 +0100
- `rubrics_used:` implementation-plan,evidence-quality
- `overall_score:` 91
- `overall_verdict:` pass
- `rerun_required:` false
- `blocking_findings:` none
- `next_action:` hold in review until approved for implementation

## Blockers
- none

## Handoff
- Current state: planning ticket created for canonical docs freshness and maintenance.
- Resume from: `docs/specs/harness-techniques.md`

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
