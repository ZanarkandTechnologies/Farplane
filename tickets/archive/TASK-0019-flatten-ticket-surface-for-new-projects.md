---
ticket_id: TASK-0019
title: flatten ticket surface for new projects
phase: building
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T22:45:00Z
next_action: write durable notes for the flat tickets cutover and keep the runtime on root-level ticket paths only
last_verification: ticket metadata validator passes on 19 root tickets; orchestrator dry-run advances from a root ticket path; tmux-backed smoke suite passes with root ticket paths and follow-up lane spawning
linked_docs:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/init-project/SKILL.md
  - skills/init-project/README.md
---

# TASK-0019: flatten ticket surface for new projects

## Summary
Make the canonical model a single `tickets/` folder with task state in the ticket itself and remove lane-subfolder assumptions from the harness.

## Scope
- In: move the repo to `tickets/*.md`, remove `tickets/INDEX.md`, delete lane folders, and patch runtime/skills/docs to use frontmatter state only
- Out: redesigning the ticket schema beyond the flat status/phase model

## Acceptance Criteria
- [x] AC-1: `init-project` scaffolds a single `tickets/` folder for new projects
- [x] AC-2: ticket docs/templates describe `tickets/*.md` plus frontmatter state as canonical
- [x] AC-3: runtime selectors can resolve tickets from the flattened layout
- [x] AC-4: `tickets/INDEX.md` is removed from the canonical workflow

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 Codexter/bin/check_ticket_metadata.py`
  - `python3 -m py_compile Codexter/bin/check_ticket_metadata.py Codexter/bin/stop_hook.py Codexter/bin/ralph_orchestrate.py Codexter/bin/ralph_tmux.py Codexter/experiments/run_ralph_smoke_evals.py`
  - `python3 Codexter/bin/ralph_orchestrate.py --ticket Codexter/tickets/TASK-0011-ralph-hook-integration-and-evals.md --phase planning --dry-run --json`
  - `python3 Codexter/experiments/run_ralph_smoke_evals.py`

## Blockers
- none

## Handoff
- Current state: repo is on the flat `tickets/*.md` model and the runtime validated against root ticket paths.
- Resume from: this ticket, `tickets/README.md`, `AGENTS.md`, `bin/stop_hook.py`, and `experiments/latest-runs.json`.
