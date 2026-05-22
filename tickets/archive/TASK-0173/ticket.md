---
ticket_id: TASK-0173
title: add first-principles planning contract
phase: complete
status: done
owner: unassigned
claimed_by:
priority: high
depends_on:
  - TASK-0171
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-05-23T01:45:42+08:00
updated_at: 2026-05-23T01:45:42+08:00
next_action: none
last_verification: 2026-05-23 - skill, feature, ticket metadata, and whitespace checks passed
---

# TASK-0173: add first-principles planning contract

## Summary
Add a canonical first-principles planning contract for PRDs, specs, tickets,
and implementation plans. The goal is to make agents reduce product/build work
to objective, need, assumptions, root cause, constraints, first viable slice,
proof, tradeoffs, and non-goals before execution.

## Scope
- In:
  - add `docs/specs/first-principles-planning.md`
  - wire the contract into generated project `AGENTS.md`
  - update PRD skill, PRD template, and requirements discovery
  - update `spec-to-ticket` so ticket boundaries carry first-principles basis
  - update `impl-plan` so material plans preserve/challenge that basis
  - update the ticket template with `First-principles basis`
  - update policy index, spec index, feature registry, and history
- Out:
  - adding a standalone first-principles skill
  - adding deterministic validators for reasoning quality
  - changing runtime hooks or subagents

## Plan
- `Change:` introduce `FirstPrinciplesPlan` as a canonical planning/spec
  contract and wire it into the existing planning pipeline.
- `Why:` the behavior is a cross-planning invariant, not a domain-specific
  workflow. It should be detailed in a spec, lightly reminded in generated
  `AGENTS.md`, and operationalized by PRD/spec/ticket/impl-plan surfaces.
- `First-principles basis:`
  - `Objective:` make first-principles thinking visible in all material specs
    and plans.
  - `Need:` prevent agents from building from symptoms, implementation bias, or
    fake metrics.
  - `Assumptions:` PRD/spec/ticket/impl-plan are the right consuming surfaces.
  - `Root cause:` the existing system had partial prompts but no shared
    contract.
  - `Constraints:` avoid bloating always-loaded prompts and avoid a premature
    new skill.
  - `First viable slice:` docs/spec reference plus planning-skill/template
    wiring.
  - `Proof/falsification:` validators pass and changed surfaces reference the
    contract.
  - `Tradeoff accepted:` no mechanical reasoning validator in this slice.
  - `Non-goals:` no hooks, subagents, or new public skill.
- `Touch:`
  - `docs/specs/first-principles-planning.md`
  - `docs/specs/README.md`
  - `docs/policies/README.md`
  - `skills/deep-init-project/references/AGENTS_TEMPLATE.md`
  - `skills/prd/SKILL.md`
  - `skills/prd/todos.md`
  - `skills/prd/references/prd-template.md`
  - `skills/prd/references/requirements-discovery.md`
  - `skills/spec-to-ticket/SKILL.md`
  - `skills/spec-to-ticket/todos.md`
  - `skills/impl-plan/SKILL.md`
  - `skills/impl-plan/todos.md`
  - `tickets/templates/ticket.md`
  - `docs/features/registry.jsonl`
  - `docs/HISTORY.md`
- `Execution steps:`
  1. Add canonical first-principles planning spec.
  2. Add a compact generated-project `AGENTS.md` reminder.
  3. Wire PRD authoring and templates to capture the basis.
  4. Wire ticket slicing and implementation planning to preserve/challenge the
     basis.
  5. Update policy/spec indexes, feature row, history, and ticket evidence.
  6. Run validators and review.
- `Recommendation:` keep first-principles thinking as a planning contract, not
  as a new skill.

## Acceptance Criteria
- [x] `docs/specs/first-principles-planning.md` exists and defines the contract.
- [x] Generated project `AGENTS.md` template carries a compact reminder.
- [x] PRD skill/template/discovery preserve first-principles basis.
- [x] `spec-to-ticket` and `impl-plan` carry the basis into tickets/plans.
- [x] Ticket template includes first-principles basis in `Plan`.
- [x] Policy/spec indexes, feature registry, and history are updated.
- [x] Skill, feature, ticket metadata, and whitespace checks pass.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 docs/features/validate_features.py`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Manual checks:`
  - Confirm `AGENTS_TEMPLATE.md` stays compact.
  - Confirm detailed policy extraction guidance lives in the spec, not the
    always-loaded prompt.

## Proof Contract
- `Metrics:`
  - `Primary metric:` first_principles_planning_validation_passed
  - `Direction:` pass/fail
  - `Verify:` validators and manual surface check
  - `Guard:` no standalone first-principles skill and no root prompt bloat
  - `Min acceptable result:` canonical spec, planning-skill wiring, template
    wiring, indexes, feature row, checks pass
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
- `spec-contract:` 4.2 / 4.0, pass. The contract is scoped to planning/spec
  surfaces and avoids creating a redundant skill.
- `integration-readiness:` 4.1 / 4.0, pass. PRD, spec-to-ticket, impl-plan,
  generated project template, ticket template, policy/spec indexes, and feature
  registry agree on the contract.
- `evidence-quality:` 4.0 / 4.0, pass. Validators cover skill links, feature
  registry, ticket metadata, and whitespace.
- `Finding log:` no blocking findings. Low caveat: reasoning quality remains
  judgment-reviewed, not mechanically validated.

## Blockers
- none
