---
ticket_id: TASK-0028
title: require main artifact grounding for subagents
phase: planning
status: review
owner: codex
priority: high
depends_on:
  - TASK-0026
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-08T01:54:29Z
updated_at: 2026-04-08T01:54:29Z
next_action: review and approve the subagent-grounding slice before implementation starts
last_verification: backlog ticket created from cross-source harness gap analysis
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/specs/orchestrator-subagent-loop.md
  - tickets/README.md
---

# TASK-0028: require main artifact grounding for subagents

## Summary
Require worker lanes and delegated subagents to ground themselves on one main artifact, usually the selected ticket, before acting.

## Scope
- In: explicit grounding rules, artifact-first handoff shape, and lightweight checks that the subagent is acting on the same work object
- Out: broader dispatcher or mailbox runtime work

## Plan

### Pitch
- `Req:` fix the weakness where delegated workers can still drift or over-index on chat context instead of the canonical work artifact
- `Bet:` make “read the main artifact first” a first-class execution invariant
- `Win:` less context rot, cleaner handoffs, and fewer misunderstandings between orchestrator and workers

### B -> A
- `Before:` tickets are durable memory, but grounding on them is not always enforced as the strict first step
- `After:` subagents must anchor on the selected ticket or declared main artifact before implementation, QA, or review
- `Outcome:` coordination becomes artifact-led rather than transcript-led

### Delta
- `Touch:` `$impl` orchestration contract, worker prompts/skills, maybe ticket handoff packet shape
- `Keep:` ticket-first execution model
- `Change:` make one canonical artifact the required grounding surface for delegated work
- `Delete/Avoid:` loose handoffs that depend on ambient context memory

### Core Flow
```pseudo
orchestrator selects one ticket
worker reads and summarizes the ticket or delegated artifact
worker executes only after grounding is explicit
review and qa validate against the same artifact
```

### Proof
- `P1:` worker prompts or contracts require explicit ticket-artifact grounding
- `P2:` a replayable delegated run shows fewer ticket-context mismatches
- `Risk:` extra boilerplate without real enforcement
- `Rollback:` keep only the smallest grounding assertion that reduces drift

### Plan Review
- `Refs:` OpenAI repo-legibility/progressive-disclosure ideas, `orchestrator-subagent-loop.md`, `tickets/README.md`, `skills/impl`
- `Scope:` one grounding invariant, not a broader runtime overhaul
- `Proof:` replay one delegated build/review/QA cycle with ticket-summary assertions
- `Guardrails:` avoid a heavyweight artifact registry or second control plane
- `Fixes:` keep the ticket as default grounding object

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` move to building and enforce artifact-first grounding in the orchestration path

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and implement the grounding contract
- `Follow-ups:` may split out worker-specific prompt cleanups if the slice gets too wide
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: delegated workers have a documented required grounding step against the selected ticket or main artifact
- [ ] AC-2: orchestration surfaces make the main artifact explicit for build, QA, and review lanes
- [ ] AC-3: at least one replayable delegated flow demonstrates reduced drift from the selected ticket

## Working Notes
- Main weakness: ticket-first is true structurally but not yet a hard invariant in every delegated lane.
- Blog technique mapping: OpenAI’s progressive disclosure and repo-legibility framing.
- This complements `TASK-0026`, which binds worker identity to handoffs; this ticket makes those workers explicitly ground on the selected artifact before acting.

## Implementation Notes
- Touched areas: `$impl` contract, worker-lane prompts/skills, maybe ticket handoff format
- Reused patterns: ticket as durable task memory
- Guardrails: no extra hidden coordination artifact by default

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- `reviewed_at:` 2026-04-08 01:54 +0100
- `rubrics_used:` implementation-plan,evidence-quality
- `overall_score:` 92
- `overall_verdict:` pass
- `rerun_required:` false
- `blocking_findings:` none
- `next_action:` hold in review until approved for implementation

## Blockers
- none

## Handoff
- Current state: planning ticket created for stricter artifact-first subagent grounding.
- Resume from: `docs/specs/orchestrator-subagent-loop.md`

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
