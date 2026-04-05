---
ticket_id: TASK-0013
title: rewrite global ralph and ralplan skills
phase: building
status: active
owner: codex
priority: high
depends_on:
  - TASK-0011
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T20:35:00Z
next_action: add harness-native ralph and ralplan skills and reinstall them into ~/.codex so the $ skill surface matches the current runtime
last_verification: none
linked_docs:
  - README.md
  - prompts/ralphplan.md
  - prompts/ralph.md
  - tickets/building/TASK-0011-ralph-hook-integration-and-evals.md
---

# TASK-0013: rewrite global ralph and ralplan skills

## Summary
Replace the old globally installed OMX-shaped `$ralph` and `$ralplan` skill semantics with the harness-native ticket-first flow.

## Scope
- In: `skills/ralph/`, `skills/ralplan/`, small docs/index updates, and reinstall into `~/.codex`
- Out: changes to the underlying runtime logic beyond what the skill text invokes

## Plan

### Pitch
- `Req:` the user-facing `$ralph` and `$ralplan` surface is still the old OMX behavior even though the repo runtime has moved to a different model
- `Bet:` rewriting those two skills gives the highest UX payoff with minimal additional machinery
- `Win:` the `$` commands finally match the harness you actually built

### B -> A
- `Before:` installed `~/.codex/skills/ralph` and `~/.codex/skills/ralplan` still assume `.omx`, OMX state, and OMX execution patterns
- `After:` the repo ships harness-native versions and the live `~/.codex` install uses them
- `Outcome:` users can type `$ralph` and `$ralplan` without falling into the wrong runtime model

### Delta
- `Touch:` `skills/`, `README.md`, `tickets/INDEX.md`, this ticket
- `Keep:` `brainstorm`, `deep-interview`, `prd`, `spec-to-ticket`, and the existing runtime scripts/prompts
- `Change:` the user-facing skill semantics only
- `Delete/Avoid:` avoid inheriting `.omx`, `/cancel`, deslop, or other OMX-only assumptions

### Core Flow
```pseudo
$brainstorm -> $deep-interview -> $prd -> spec-to-ticket -> $ralplan -> $ralph
```

### Proof
- `P1:` repo-native `skills/ralph/SKILL.md` and `skills/ralplan/SKILL.md` exist
- `P2:` install.sh places them into ~/.codex/skills
- `P3:` installed skill text matches the ticket-first runtime rather than OMX

### Ask
- `Ready: yes`
- `Next:` write the two skills and reinstall them

## Acceptance Criteria
- [ ] AC-1: repo contains harness-native `ralph` and `ralplan` skills
- [ ] AC-2: installed `~/.codex/skills/ralph` and `~/.codex/skills/ralplan` point to the repo versions
- [ ] AC-3: the new skill text references ticket-first runtime behavior instead of `.omx` / OMX runtime behavior

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- none

## Handoff
- Current state: front-end `brainstorm` and `deep-interview` are ours; `ralph` and `ralplan` are still globally wrong.
- Resume from: this ticket plus `~/.codex/skills/ralph/SKILL.md` and `~/.codex/skills/ralplan/SKILL.md`.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
