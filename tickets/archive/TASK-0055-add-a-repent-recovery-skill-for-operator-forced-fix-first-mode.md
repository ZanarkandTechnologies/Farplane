---
ticket_id: TASK-0055
title: add a repent recovery skill for operator-forced fix-first mode
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-10T16:28:20Z
updated_at: 2026-04-10T17:31:00Z
next_action: none; ticket archived after the `repent` skill landed, manual validation replaced the unavailable packaged validator, and ticket/docs checks passed
last_verification: python3 tickets/scripts/check_ticket_metadata.py; git diff --check; rg -n "TODO|\\[TODO" skills/repent -S; manual skill validation completed after `quick_validate.py` failed due missing PyYAML in the local environment
linked_docs:
  - AGENTS.md
  - templates/global/AGENTS.md
  - docs/HISTORY.md
  - docs/MEMORY.md
  - skills/repent/SKILL.md
  - skills/repent/references/fixtures.md
---

# TASK-0055: add a repent recovery skill for operator-forced fix-first mode

## Summary
Create a small operator-facing recovery skill named `repent` that can be invoked when the assistant missed something obvious and needs to switch into audit-then-fix behavior immediately.

## Scope
- In:
  - defining the `repent` skill contract
  - adding a few concrete recovery fixtures/examples
  - wiring skill metadata so it is discoverable and usable
  - durable writeback for the new skill decision
- Out:
  - replacing the default proactive contract with the skill
  - adding runtime hooks or hidden orchestration
  - building a broad correction-analysis framework

## User Story
- `Actor:` Codexter operator who thinks the agent is being stubborn, passive, or explanation-first
- `Need:` a short explicit recovery command that forces the agent to verify the complaint and then fix the issue immediately if it is real
- `Outcome:` the operator has an escape hatch when the default contract is not enough

## Non-Goals
- `Do not solve:` all miss-recovery behavior through the skill alone; the default contract remains primary

## Acceptance Criteria
- [x] AC-1: a new `skills/repent/` skill exists with a concrete recovery workflow and no scaffold TODOs
- [x] AC-2: the skill clearly distinguishes true miss, false alarm, and ambiguous complaint cases
- [x] AC-3: the skill tells the agent to audit first, then fix first when the complaint is real, instead of leading with explanation
- [x] AC-4: the skill includes concrete operator-facing examples/fixtures
- [x] AC-5: skill validation or equivalent manual validation passes and durable docs reflect the new escape-hatch surface

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification
- `python3 tickets/scripts/check_ticket_metadata.py`
- `git diff --check`
- `rg -n "TODO|\\[TODO" skills/repent -S`
- Manual verification:
  - inspected `skills/repent/SKILL.md` for concrete trigger conditions, recovery workflow, and safety boundaries
  - inspected `skills/repent/references/fixtures.md` for deterministic operator-facing recovery cases
  - inspected `skills/repent/agents/openai.yaml` for usable UI metadata
- Validator note:
  - `python3 /Users/kenjipcx/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/repent` could not run here because `PyYAML` is not installed in the environment; replaced with explicit manual validation instead of claiming a false pass

## Implementation Notes
- Touched areas: `skills/repent/SKILL.md`, `skills/repent/references/fixtures.md`, `skills/repent/agents/openai.yaml`, `skills/repent/AGENTS.md`, `skills/repent/README.md`, `templates/global/AGENTS.md`, `AGENTS.md`, `docs/MEMORY.md`, and `docs/HISTORY.md`
- Reused patterns: contract-first behavior tuning, deterministic fixtures from the proactive-contract ticket, and operator-explicit override semantics rather than hidden runtime behavior
- Guardrails: kept `repent` same-scope, recovery-only, and non-destructive; it complements the default proactive contract rather than widening approval boundaries

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `work_type:` `["skills","docs-update"]`
- `search_scope:` `{changed_files: ["skills/repent/SKILL.md", "skills/repent/references/fixtures.md", "skills/repent/agents/openai.yaml", "skills/repent/AGENTS.md", "skills/repent/README.md", "templates/global/AGENTS.md", "AGENTS.md", "docs/MEMORY.md", "docs/HISTORY.md", "tickets/TASK-0055-add-a-repent-recovery-skill-for-operator-forced-fix-first-mode.md"], related_files: ["tickets/archive/TASK-0054-make-the-agent-more-proactive-on-corrections-and-obvious-next-actions.md"], invariants_checked: ["repent remains an explicit operator override only", "repent does not widen approval boundaries", "default proactive contract remains primary"], docs_checked: ["templates/global/AGENTS.md", "docs/MEMORY.md", "docs/HISTORY.md"]}`
- `reviewed_at:` `2026-04-10 17:31 +0100`
- `rubrics_used:` `["integration-readiness","evidence-quality"]`
- `overall_score:` `4.3`
- `overall_threshold:` `4.0`
- `overall_verdict:` `pass`
- `rerun_required:` `false`
- `evidence_quality:` `pass`
- `integration_readiness:` `pass`
- `traceability:` `pass`
- `freshness:` `pass`
- `hard_gate_failures:` `[]`
- `finding_log:` `[]`
- `blocking_findings:` `[]`
- `next_action:` `none; escape-hatch skill is implemented`

## Blockers
- none

## Handoff
- Current state: the `repent` skill is implemented as a small operator-facing audit-then-fix escape hatch and documented as an explicit override rather than a replacement for the default proactive contract.
- Resume from: if a follow-up is needed, inspect `skills/repent/SKILL.md`, `skills/repent/references/fixtures.md`, and `templates/global/AGENTS.md` together.
