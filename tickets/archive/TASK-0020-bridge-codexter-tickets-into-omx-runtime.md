---
ticket_id: TASK-0020
title: bridge codexter tickets into omx runtime
phase: documenting
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-06T00:00:00Z
updated_at: 2026-04-06T06:38:00Z
next_action: decide whether the next slice should add an actual OMX launch wrapper or a writeback bridge from OMX task results into Markdown tickets
last_verification: python3 -m py_compile bin/export_omx_team_input.py plus python3 bin/export_omx_team_input.py --team-name codexter-omx-bridge --limit 3 and python3 bin/check_ticket_metadata.py
linked_docs:
  - docs/specs/omx-execution-bridge.md
  - /Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime-cli.ts
  - tickets/templates/ticket.md
---

# TASK-0020: bridge codexter tickets into omx runtime

## Summary
Use the pulled OMX codebase as the execution backend by exporting ready
Codexter Markdown tickets into OMX team-runtime input.

## Scope
- In: export ready tickets, map ticket metadata into OMX task descriptions, and verify the payload matches OMX runtime-cli expectations
- Out: full worker writeback, ticket claims, or replacing OMX runtime state

## Acceptance Criteria
- [x] AC-1: one script can export ready tickets into OMX team-runtime JSON
- [x] AC-2: the exported payload includes enough ticket context for OMX workers to identify the source Markdown ticket
- [x] AC-3: verification proves the payload matches the current OMX runtime-cli input contract

## Implementation Notes
- Touched areas: `docs/specs/omx-execution-bridge.md`, `bin/export_omx_team_input.py`, `bin/README.md`, `docs/specs/README.md`, `README.md`, and this ticket
- Reused patterns: Codexter ticket frontmatter parsing and OMX `runtime-cli.ts` input shape (`teamName`, `workerCount`, `agentTypes`, `tasks`, `cwd`)
- Guardrails: keep the bridge one-way for now, preserve Markdown tickets as visible truth, and do not rewrite OMX runtime state

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 -m py_compile bin/export_omx_team_input.py`
  - `python3 bin/export_omx_team_input.py --team-name codexter-omx-bridge --limit 3`
  - verified payload fields align with `/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime-cli.ts`
  - `python3 bin/check_ticket_metadata.py`

## Blockers
- none

## Handoff
- Current state: latest OMX was pulled fast-forward to `origin/main`, the bridge direction is canonicalized, and `bin/export_omx_team_input.py` can export ready Markdown tickets into OMX runtime-cli JSON.
- Resume from: `docs/specs/omx-execution-bridge.md`, `bin/export_omx_team_input.py`, `/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime-cli.ts`, and the next launch/writeback bridge slice.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
