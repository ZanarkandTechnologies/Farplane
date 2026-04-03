---
ticket_id: TASK-0001
title: bootstrap codex harness repo
phase: building
status: active
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T02:06:03Z
next_action: add the remote repository URL and push the verified harness scaffold
last_verification: reviewed git status plus bash -n install.sh and python3 -m py_compile bin/notify.py
linked_docs: []
---

# TASK-0001: bootstrap codex harness repo

## Summary
Create the minimum repo harness needed to version reusable Codex configuration from this live `~/.codex` directory without leaking machine-local state.

## Scope
- In: `.gitignore`, repo docs, ticket board, sanitized config example, installer, Git init
- Out: remote hosting setup, secret management beyond local placeholders, changing the live `config.toml`

## Plan

### Pitch
- `Req:` make this directory easy to publish and clone as a Codex config harness repo
- `Bet:` version the live directory in place, but ignore runtime state and keep the real `config.toml` local
- `Win:` smallest path that keeps current skills/agents reusable without leaking secrets or machine-local artifacts

### B -> A
- `Before:` live `.codex` home with reusable config mixed together with auth, logs, sessions, sqlite files, and secret-bearing config
- `After:` Git-ready harness scaffold with safe ignore rules, bootstrap docs, installer, sanitized config example, and a ticket/docs workflow for future changes
- `Outcome:` easy to clone directly into `~/.codex` or install from a separate repo checkout

### Delta
- `Touch:` root docs, `AGENTS.md`, `.gitignore`, `config.toml.example`, `install.sh`, `docs/*`, `tickets/*`
- `Keep:` existing `agents/`, `skills/`, `rules/`, `bin/notify.py`, live `config.toml`
- `Change:` add repo structure and safety boundaries around the existing live config
- `Delete/Avoid:` avoid committing live `config.toml`, auth/session history, logs, sqlite files, caches, or shell snapshots

### Core Flow
```pseudo
inspect ~/.codex contents
classify reusable config vs live machine state
write .gitignore for machine-local state
add docs/tickets/README for the harness workflow
add config.toml.example with placeholders
add install.sh to symlink tracked config into ~/.codex
init git and verify tracked file set
```

### Proof
- `P1:` `git status --short` shows only reusable harness files as untracked/tracked changes
- `P2:` `bash -n install.sh` and `python3 -m py_compile bin/notify.py` pass
- `Risk:` a future tracked file could still contain a secret if added carelessly
- `Rollback:` remove `.git/` or revert the scaffold files; live ignored state stays untouched

### Plan Review
- `Refs:` `docs/prd.md`, `tickets/building/TASK-0001-codex-harness-bootstrap.md`, `docs/MEMORY.md`, `AGENTS.md`, local code/config inspection
- `Scope:` pass
- `Proof:` pass
- `Guardrails:` pass
- `Fixes:` kept the change to one bootstrap slice and left live `config.toml` unmodified

### Delegation
- `Need:` `Not needed`
- `Why:` small local repo scaffold with no UI/runtime debugging path
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` initialize Git locally, then add a remote and push when the repo URL exists

## Acceptance Criteria
- [x] AC-1: the repo clearly versions reusable Codex config while ignoring live runtime state and secrets
- [x] AC-2: there is a documented bootstrap path for cloning directly into `~/.codex` or linking from another checkout
- [x] AC-3: the harness has minimal docs and ticket scaffolding so future changes can follow repo contract

## Working Notes
- The ticket remains in `tickets/building/` until the repository can be pushed and the bootstrap work is fully closed out.

## Implementation Notes
- Touched areas: root repo scaffold plus docs/tickets only
- Reused patterns: local `AGENTS.md` contract and ticket template shape already used in nearby repos
- Guardrails: left `config.toml` ignored and live; no auth/session/log/sqlite state added to Git

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification

## Blockers
- none

## Handoff
- Current state: scaffold is implemented and locally verified; remote publication is the remaining explicit next step.
- Resume from: this ticket, `git status --short`, and the bootstrap docs/install surfaces.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
