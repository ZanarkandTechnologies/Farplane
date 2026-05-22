---
ticket_id: TASK-0172
title: add harness advisor placement axes
phase: complete
status: done
owner: unassigned
claimed_by:
priority: medium
depends_on:
  - TASK-0171
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-05-22T18:12:00+08:00
updated_at: 2026-05-22T18:12:00+08:00
next_action: none
last_verification: 2026-05-22 - skill, feature, ticket metadata, and whitespace checks passed
---

# TASK-0172: add harness advisor placement axes

## Summary
`harness-advisor` already knew to compare Codexter placement surfaces, but it
did not make the context-management axes explicit for harder placement calls.
This ticket adds a compact placement model so material or ambiguous advisor
decisions can score always-loaded prompt cost, progressive skill/docs
disclosure, subagent context isolation, tool/MCP capability, hook determinism,
registry dedupe, and ticket proof ownership.

## Scope
- In:
  - add `skills/harness-advisor/references/placement-axes.md`
  - update `skills/harness-advisor/SKILL.md` to require placement-axis scoring
  - update `skills/harness-advisor/todos.md`
  - update `FEAT-0023` surfaces and known limits
  - update history
- Out:
  - changing root `AGENTS.md`
  - changing global template policy
  - adding hooks, validators, MCP tools, or new subagents

## Plan
- `Change:` give `harness-advisor` an optional reusable axes reference with
  algebra, OOP-style surface interfaces, questions, and compact scoring.
- `Why:` context management is a first-class harness optimization problem.
  Advisor should decide whether a request belongs in always-loaded prompt,
  progressive skill/docs, isolated subagent, durable files, MCP/tool, hook,
  registry, or ticket contract.
- `Before -> After:`
  - Before: advisor compared surfaces but did not explicitly score context
    budget, duplication risk, determinism, or ownership fit.
  - After: advisor reads placement axes for material or ambiguous placement
    decisions and can include an `Axes` section when useful.
- `Touch:`
  - `skills/harness-advisor/SKILL.md`
  - `skills/harness-advisor/todos.md`
  - `skills/harness-advisor/references/placement-axes.md`
  - `docs/features/registry.jsonl`
  - `docs/HISTORY.md`
- `Signature delta:`
  - `PlacementDecision := FailureMode + ContextBudget + ReuseFrequency + OwnershipBoundary + Determinism + EvidenceSurface + DuplicationRisk + Discoverability + MaintenanceCost`
  - `SurfaceScore := context_cost + reuse_frequency + determinism + ownership_fit + duplication_risk + recommended`
- `Acceptance Criteria:`
  - [x] Advisor has an axes reference for context and placement scoring.
  - [x] Advisor workflow and todos require reading/scoring that reference only
        for material or ambiguous placement decisions.
  - [x] Feature registry reflects the added advisor surface.
  - [x] Skill, feature, ticket metadata, and whitespace checks pass.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 docs/features/validate_features.py`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Manual checks:`
  - Confirm local `AGENTS.md` already references `harness-advisor` and
    `skill-maintenance`.
  - Confirm the axes model lives in advisor reference docs, not root prompt.

## Proof Contract
- `Metrics:`
  - `Primary metric:` harness_advisor_axes_validation_passed
  - `Direction:` pass/fail
  - `Verify:` validators and manual surface check
  - `Guard:` no root prompt bloat
  - `Min acceptable result:` axes reference, advisor workflow/todo updates,
    feature registry update, checks pass
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `spec-contract >= 4.0`
  - `integration-readiness >= 4.0`
  - `evidence-quality >= 4.0`
- `Required Evidence:`
  - validation logs
  - final review summary

## Evidence
- `Commands:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 docs/features/validate_features.py`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Result summary:` all checks passed

## Review
- `spec-contract:` 4.1 / 4.0, pass. The change targets one clear missing
  advisor behavior: optional context-aware placement scoring for harder calls.
- `integration-readiness:` 4.1 / 4.0, pass. Root policy already points to
  advisor and skill-maintenance; the new detail lives in progressive advisor
  docs instead of always-loaded prompt.
- `evidence-quality:` 4.0 / 4.0, pass. Checks cover skill registry, feature
  registry, ticket metadata, and whitespace.
- `Finding log:` no blocking findings.

## Blockers
- none
