---
ticket_id: TASK-0013
title: rewrite global ralph and ralplan skills
phase: building
status: building
owner: codex
priority: high
depends_on:
  - TASK-0011
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T22:50:00+0100
next_action: verify a live Ralph run now treats a coherent ticket as the execution unit instead of re-slicing it into micro-tasks
last_verification: 2026-04-05T22:50:00+0100 | verified prompts/ralph.md, skills/ralph/SKILL.md, and ~/.codex/skills/ralph/SKILL.md all treat the active ticket as the default execution unit
linked_docs:
  - README.md
  - prompts/ralphplan.md
  - prompts/ralph.md
  - tickets/TASK-0011-ralph-hook-integration-and-evals.md
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
- `Touch:` `skills/`, `README.md`, `tickets/README.md`, this ticket
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
- [x] AC-1: repo contains harness-native `ralph` and `ralplan` skills
- [x] AC-2: installed `~/.codex/skills/ralph` and `~/.codex/skills/ralplan` point to the repo versions
- [x] AC-3: the new skill text references ticket-first runtime behavior instead of `.omx` / OMX runtime behavior

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

Manual verification:
- `prompts/ralph.md` now says to treat the ticket as the execution unit for the pass
- `skills/ralph/SKILL.md` and `~/.codex/skills/ralph/SKILL.md` now say Ralph implements approved ticket scope, not a pre-shrunk micro-slice
- Ralphplan remains separate from this rule, so planning/ticket decomposition is not being disabled here

## Blockers
- none

## Handoff
- Current state: the live `$ralph` surface and runtime prompt now treat a coherent ticket as the unit of execution, while `$ralplan` remains free to do planning/ticket decomposition work.
- Resume from: this ticket plus `prompts/ralph.md`, `skills/ralph/SKILL.md`, and `~/.codex/skills/ralph/SKILL.md` if you want to tune the execution wording further after a live run.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
