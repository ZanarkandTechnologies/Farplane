---
ticket_id: TASK-0012
title: add deep interview and brainstorm skills
phase: building
status: active
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T18:45:00Z
next_action: add Codexter-native front-end skills for ambiguity-gated requirements and early option exploration
last_verification: none
linked_docs:
  - README.md
  - skills/prd/SKILL.md
  - skills/spec-to-ticket/SKILL.md
---

# TASK-0012: add deep interview and brainstorm skills

## Summary
Add the front-end skills that make the Ralph flow usable before ticket execution starts: a deep-interview skill for requirements clarification and a brainstorm skill for open-ended exploration.

## Scope
- In: new `skills/deep-interview/` and `skills/brainstorm/` contracts plus small docs/index updates
- Out: hook/runtime changes, new tmux orchestration, or ticket execution semantics

## Plan

### Pitch
- `Req:` the current harness has `prd`, but it lacks the stronger ambiguity-gating/front-end discovery surfaces that make the Ralph flow practical for messy client inputs
- `Bet:` a Codexter-native `deep-interview` plus `brainstorm` pair will reduce bad starts more than adding more execution machinery
- `Win:` users can sharpen product direction before specs and tickets without borrowing OMX's runtime assumptions

### B -> A
- `Before:` the repo has `prd`, but not a one-question-at-a-time discovery skill or a lightweight ideation skill
- `After:` the repo has one skill for converging on requirements and one for exploring options before commitment
- `Outcome:` the front of the Ralph funnel becomes more usable and less dependent on ad-hoc chat

### Delta
- `Touch:` `skills/`, `README.md`, `docs/HISTORY.md`, `tickets/INDEX.md`
- `Keep:` `prd` as the spec-writing step and `spec-to-ticket` as the ticketization step
- `Change:` add a discovery layer in front of `prd`
- `Delete/Avoid:` avoid importing OMX-specific `.omx` assumptions into these skills

### Core Flow
```pseudo
brainstorm when the idea is open-ended
deep-interview when the idea is still too vague for PRD/spec writing
prd after the key constraints and first SLC slice are clear
spec-to-ticket after PRD/specs are accepted
```

### Proof
- `P1:` the new skills describe when to stop and hand off instead of trying to do the whole workflow themselves
- `P2:` the skills are Codexter-native and reference tickets/specs/docs instead of OMX state
- `Risk:` too much overlap with `prd`
- `Rollback:` remove the skills and keep the older `prd`-only front end

### Ask
- `Ready: yes`
- `Next:` implement the two skills and keep them narrowly scoped

## Acceptance Criteria
- [ ] AC-1: `deep-interview` exists and is clearly positioned before `prd`
- [ ] AC-2: `brainstorm` exists and is clearly positioned before commitment/spec writing
- [ ] AC-3: both skills reference Codexter artifacts rather than OMX runtime/state

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- none

## Handoff
- Current state: front-end discovery is the missing skill layer.
- Resume from: this ticket plus `skills/prd/SKILL.md` and `skills/spec-to-ticket/SKILL.md`.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
