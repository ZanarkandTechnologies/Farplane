---
ticket_id: TASK-0015
title: purge live omx instruction surfaces
phase: building
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T21:20:00Z
updated_at: 2026-04-05T22:14:24+0100
next_action: decide whether to purge the remaining shared ~/.codex prompt and skill surfaces that still carry OMX-era guidance, or leave the repo-owned Codexter set in place for now
last_verification: 2026-04-05T22:14:24+0100 | installed_only_agents=0 and installed_only_skills=0 after deleting every ~/.codex entry not present in Codexter
linked_docs:
  - docs/prd.md
  - docs/MEMORY.md
  - tickets/TASK-0013-rewrite-ralph-skills.md
---

# TASK-0015: purge live omx instruction surfaces

## Summary
Remove the remaining OMX-specific guidance from the live user-level Codex surfaces that still shape current sessions.

## Scope
- In: `~/.codex/prompts/`, `~/.codex/agents/`, selected `~/.codex/skills/`, and the small Codexter rule/ticket writeback needed to track the purge
- Out: historical research docs, archived backups, and the `oh-my-codex` repo itself

## Plan

### Pitch
- `Req:` OMX was supposed to be purged from the active system, but current live instruction surfaces still tell agents to use `omx ...` commands and `.omx/...` paths
- `Bet:` fix the active user-level prompts/agents/skills first, because those keep reintroducing OMX behavior into day-to-day sessions
- `Win:` current Codex sessions stop inheriting obsolete OMX commands and state assumptions even before the old repo is archived or deleted

### B -> A
- `Before:` live `~/.codex` prompts, agents, and skills still mention `OMX`, `omx ...`, and `.omx/...`
- `After:` the active instruction surfaces become harness-native or generic, and the known live Codexter residue stops pointing at `.omx`
- `Outcome:` the active system no longer nudges users or agents back into the retired OMX model

### Delta
- `Touch:` `~/.codex/prompts/`, `~/.codex/agents/`, `~/.codex/skills/`, `rules/default.rules`, `tickets/README.md`, this ticket
- `Keep:` ticket-first Codexter flow, non-OMX research history, and `oh-my-codex` as a separate archive/delete decision
- `Change:` live planning/execution guidance and obvious obsolete OMX-branded utility skills
- `Delete/Avoid:` avoid broad historical doc churn or large repo renames in this slice

### Core Flow
```pseudo
identify live instruction files that still inject omx behavior
rewrite or remove the smallest set that changes active behavior
verify the edited surfaces no longer mention omx or .omx
record remaining out-of-scope residue for later archive/delete work
```

### Proof
- `P1:` edited live `~/.codex` prompts/agents/skills no longer instruct `omx ...` usage or `.omx/...` plan/state paths
- `P2:` Codexter live residue tied to the retired runtime is removed or rewritten
- `Risk:` over-broad text churn could delete useful non-OMX guidance
- `Rollback:` keep the patch small and scoped to the instruction surfaces that currently steer sessions

### Plan Review
- `Refs:` `docs/prd.md`, `docs/MEMORY.md`, `AGENTS.md`, `tickets/TASK-0013-rewrite-ralph-skills.md`, live `~/.codex` prompt/agent/skill files
- `Scope:` one cleanup slice focused on active guidance, not historical archive cleanup
- `Proof:` direct grep over edited surfaces plus targeted file inspection
- `Guardrails:` delete or rewrite only the live instructions that still enforce OMX behavior
- `Fixes:` split the old broad “purge OMX” idea into this explicit live-surface slice

### Delegation
- `Need:` Not needed
- `Why:` the slice is local, bounded, and faster to patch directly
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` patch the live instruction surfaces and verify the remaining residue

### Ticket Move
- `Now:` `tickets/`
- `On approval:` already approved by user request to continue the purge
- `Follow-ups:` likely separate archive/delete ticket for the `oh-my-codex` repo and optional history/cache cleanup
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: the installed-only `~/.codex` agents and skills have been deleted so the live directories now contain only entries present in Codexter
- [x] AC-2: Codexter no longer carries the live `.omx/` exclude rule
- [x] AC-3: this ticket records the intentionally deferred shared OMX residue that still lives inside repo-owned prompt and skill surfaces

## Working Notes
- Focus on active behavior first.
- Historical research documents can still mention OMX without blocking this slice.
- Avoid stepping on the dedicated `TASK-0013` `ralph` / `ralplan` rewrite unless a line is directly necessary for the purge.
- User redirected the slice from broad text cleanup to a direct installed-only diff and delete pass.
- Deferred residue remains in shared repo-owned prompt and skill surfaces such as `plan`, `team`, `help`, `doctor`, `cancel`, and several prompt-agent metadata markers.

## Implementation Notes
- Touched areas:
  - `~/.codex/agents/`
  - `~/.codex/skills/`
  - `rules/default.rules`
  - `tickets/README.md`
  - this ticket
- Reused patterns:
  - used direct installed-vs-repo set diffs against `Codexter/agents` and `Codexter/skills`
- Guardrails:
  - deleted only entries present in `~/.codex` and absent from the Codexter repo copy
  - left all shared repo-owned surfaces intact

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

Manual verification:
- Pre-delete diff showed `31` installed-only agent files and `46` installed-only skill directories under `~/.codex`.
- Deleted every installed-only entry from `~/.codex/agents` and `~/.codex/skills`.
- Post-delete verification:
  - `installed_only_agents=0`
  - `installed_only_skills=0`
- Remaining installed directories now match the Codexter repo set exactly for names:
  - agents: `asset-generator`, `bash-operator`, `code-reviewer`, `convex-builder`, `deep-researcher`, `documentation-maintainer`, `documentation-searcher`, `explore`, `frontend-designer`, `librarian`, `memory`, `planner-agent`, `qa-tester`
  - skills: `agent-browser`, `apify`, `bash-efficiency`, `brainstorm`, `cinematic-landing`, `code-review`, `codebase-analysis`, `commit-message`, `convex`, `data-viz`, `deep-interview`, `documentation`, `external-patterns`, `find-skills`, `frontend-design`, `init-project`, `prd`, `ralph`, `ralplan`, `react-flow`, `runtime-debugging`, `skill-creator`, `spec-to-ticket`, `tech-impl-plan`, `testing`, `three-js`, `vercel-react-best-practices`, `visual-qa`, `web-design-guidelines`

## Blockers
- none

## Handoff
- Current state: installed-only `~/.codex` agents and skills are gone; the remaining `~/.codex` names now mirror the Codexter repo copy.
- Resume from: this ticket plus the remaining shared-surface OMX grep inventory if the user wants the repo-owned prompt and skill text scrubbed next.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes board state, move the file and update `tickets/README.md` as a human summary.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then archive/delete the ticket or move it out of active lanes.
