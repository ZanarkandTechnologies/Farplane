---
ticket_id: TASK-0171
title: add project lifecycle reference and template wiring
phase: complete
status: done
owner: unassigned
claimed_by:
priority: high
depends_on:
  - TASK-0170
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-05-22T17:57:36+08:00
updated_at: 2026-05-22T17:57:36+08:00
next_action: none
last_verification: 2026-05-22 - skill maintenance, ticket metadata, and whitespace checks passed
---

# TASK-0171: add project lifecycle reference and template wiring

## Summary
Codexter needed a clearer representation of the shared project lifecycle
without prematurely creating a public `project-pipeline` skill. This ticket
adds a lifecycle reference under `deep-init-project`, wires the compact
lifecycle rule into generated project `AGENTS.md`, and clarifies that
`PROJECT_RULES.md` owns technical commands and runtime standards.

## Scope
- In:
  - add `skills/deep-init-project/references/project-lifecycle.md`
  - update generated project `AGENTS.md` template with the compact lifecycle
    invariant
  - update `PROJECT_RULES_TEMPLATE.md` with a pointer back to `AGENTS.md` for
    agent lifecycle/workflow rules
  - add `Lifecycle route` to the bootstrap brief template
  - update relevant skill todos to name lifecycle phase ownership
  - update `harness-advisor` so placement decisions consider the generated
    project `AGENTS.md` and `PROJECT_RULES.md` templates
  - update feature/skill docs and history
- Out:
  - creating a new top-level `project-pipeline` skill
  - changing runtime orchestration, hooks, validators, or ticket state machine

## Plan
- `Change:` encode `ProjectLifecycle` as a deep-init reference and wire the
  generated project templates plus downstream todos to that lifecycle.
- `Why:` the true abstraction is the project lifecycle, not reusable base-class
  implementations of `plan` or `execute`.
- `Before -> After:`
  - Before: generated projects had discovery/planning/build modes, but no
    compact always-loaded lifecycle invariant.
  - After: generated project `AGENTS.md` states the lifecycle, bootstrap brief
    captures the route, and downstream skill todos declare which lifecycle
    phase they implement.
- `Touch:`
  - `skills/deep-init-project/references/project-lifecycle.md`
  - `skills/deep-init-project/references/AGENTS_TEMPLATE.md`
  - `skills/deep-init-project/references/PROJECT_RULES_TEMPLATE.md`
  - `skills/deep-init-project/references/BOOTSTRAP_BRIEF_TEMPLATE.md`
  - `skills/deep-init-project/todos.md`
  - `skills/prd/todos.md`
  - `skills/spec-to-ticket/todos.md`
  - `skills/impl-plan/todos.md`
  - `skills/impl/todos.md`
  - `skills/close-ticket/todos.md`
  - `skills/harness-advisor/SKILL.md`
  - `docs/skills/README.md`
  - `docs/features/registry.jsonl`
  - `docs/HISTORY.md`
- `Signature delta:`
  - `ProjectLifecycle := Bootstrap + DeepInterview + PRD + TicketBreakdown + TicketLoop*`
  - `TicketLoop := PlanTicket + ExecuteTicket + VerifyTicket + ReviewTicket + CloseTicket`
- `Type Sketch:`
  - `ProjectLifecycle`: lifecycle phases and phase owners
  - `TicketLoop`: planner owner, executor owner, proof owner, review owner,
    closeout owner
  - `GeneratedProjectAgents`: always-loaded lifecycle invariant plus pointers
    to bootstrap brief, PRD, tickets, and `PROJECT_RULES.md`
- `Execution steps:`
  1. Add lifecycle reference and OOP pattern map.
  2. Update generated project templates with lifecycle ownership split.
  3. Update skill todos to reference lifecycle phase ownership.
  4. Update `harness-advisor` placement grounding to include generated project
     templates.
  5. Update registry docs, feature row, history, and ticket evidence.
- `Recommendation:` keep lifecycle as a reference until multiple higher-tier
  skills need to actively call a public `project-pipeline` skill.
- `Risks:`
  - over-linking Tier 3 todos to peer Tier 3 skills
  - bloating generated `AGENTS.md` with theory instead of operational rules

## Acceptance Criteria
- [x] Project lifecycle reference exists under `deep-init-project`.
- [x] Generated project `AGENTS.md` template includes the compact lifecycle
      invariant.
- [x] `PROJECT_RULES_TEMPLATE.md` clarifies that agent workflow lives in
      `AGENTS.md`.
- [x] Bootstrap brief template captures lifecycle route.
- [x] Relevant todos name lifecycle phase ownership.
- [x] `harness-advisor` considers generated project templates as placement
      surfaces.
- [x] Skill registry, todo-tier, capability, ticket metadata, and whitespace
      checks pass.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Manual checks:`
  - Confirm generated `AGENTS.md` stays compact and operational.
  - Confirm lifecycle theory lives in a reference, not the always-loaded prompt.
- `Evidence required:`
  - changed lifecycle/template/todo files
  - generated registry validation output
  - ticket metadata output

## Proof Contract
- `Metrics:`
  - `Primary metric:` project_lifecycle_template_validation_passed
  - `Direction:` pass/fail
  - `Verify:` skill and ticket validators
  - `Guard:` no new top-level abstract skill created
  - `Min acceptable result:` lifecycle reference, template wiring, todo updates,
    and validation pass
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
- `Artifacts:` none
- `Commands:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Result summary:` all checks passed

## Review
- `spec-contract:` 4.2 / 4.0, pass. The change has one clear lifecycle
  placement decision and preserves the no-new-abstract-skill boundary.
- `integration-readiness:` 4.1 / 4.0, pass. Generated project `AGENTS.md`,
  `PROJECT_RULES.md`, bootstrap brief, downstream todos, and harness-advisor
  now agree on the ownership split.
- `evidence-quality:` 4.0 / 4.0, pass. Mechanical checks cover skill registry,
  todo-tier links, capability fixtures, ticket metadata, and whitespace.
- `Finding log:` no blocking findings. Low caveat: lifecycle semantics remain
  prose/reference-level guidance, not deterministic validation.

## Blockers
- none
