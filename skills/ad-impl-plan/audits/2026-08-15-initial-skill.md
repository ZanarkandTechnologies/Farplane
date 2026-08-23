---
skill: ad-impl-plan
date: 2026-08-15
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/ad-advisor/SKILL.md + skills/content-impl-plan/SKILL.md
after_ref: skills/ad-impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0420/artifacts/validation.md
  - .farplane/evals/runs/20260815-091648-task-0420-ad-impl-plan-goal-telegram-repair/summary.json
  - .farplane/evals/runs/20260815-092251-task-0420-ad-impl-plan-telegram-review/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Paid-ad strategy, asset production, Goal looping, and Meta reporting
  had no paid-ad campaign ticket planner.
- After: `ad-impl-plan` owns the canonical paid-ad campaign ticket and routes
  existing specialists conditionally.
- Why: Ticket creation is planner work; adding it to `ad-advisor` would merge
  strategy with orchestration, while `content-impl-plan` would make every ad
  a media-production workflow.
- Tradeoff accepted: The initial surface delegates Goal Packet creation to
  `goal-advisor` instead of adding campaign-specific runtime state.

## First-Principles Reasoning

- Objective: One reviewable campaign directive must keep its tests, approvals,
  evidence, and delayed learning loop together.
- Placement logic: The trigger is repeated, judgment-heavy, and progressively
  loaded; a Tier 3 marketing skill is the smallest owner.
- Expected behavior delta: Campaign planning creates one canonical ticket,
  admits only required child routes, and treats every delivery change as an
  explicit approval boundary.
- Proof needed: Structure validation, normal/blocker/permission eval rows,
  generated registry/index checks, installation, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Trigger, phase boundary, ownership, output, and safety gates are in the first-load contract. |
| `reference_load_precision` | pass | The planner loads only conditional campaign routes and lets their owners do domain work. |
| `missing_context_rate` | pass | Required unknowns become named ticket-row blockers rather than guessed campaign facts. |
| `noisy_context_rate` | pass | Existing-creative tests omit production routes; reference-led routes remain conditional. |
| `duplicated_instruction_count` | pass | Strategy, copy, assets, Goal Packet, Meta reporting, and Telegram delivery retain their existing owners. |
| `prompt_size_tokens` | not_measured | No project threshold is defined; structural surface-budget validation passed. |
| `task_success_rate` | pass | Core campaign suite: 5/5 A; visual Telegram review case: 1/1 A. |
| `review_tas_rate` | pass | Independent reviewer returned TAS-A with no hard-gate failures. |
| `maintenance_locality` | pass | Skill package owns its contract, QA, evals, example, and audit; registry is generated. |
| `composition_clarity` | pass | Independent reviewer confirmed that existing specialists retain strategy, production, operations, reporting, and notification ownership. |

## Proof Artifacts

- Skill-local evals: `skills/ad-impl-plan/evals/evals.json`
- Structure evals: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: `tickets/TASK-0420/artifacts/review.md`
- Validation receipt: `tickets/TASK-0420/artifacts/validation.md`
- Core behavior result: 5/5 A at `.farplane/evals/runs/20260815-091648-task-0420-ad-impl-plan-goal-telegram-repair/summary.json`
- Visual Telegram result: 1/1 A at `.farplane/evals/runs/20260815-092251-task-0420-ad-impl-plan-telegram-review/summary.json`
- Installed-copy parity: source and `~/.codex/skills/ad-impl-plan` match after selected install.
- Final independent review: TAS-A at `tickets/TASK-0420/artifacts/review.md`.
- Eval required: yes
- Evidence gaps: No live Meta mutation, spend, campaign launch, or Telegram
  message is in scope; those require a separately approved campaign ticket.

## Optimization Deferral

`self-improve` is not invoked: this new, safety-critical planner has no
real approved-campaign corpus or stable human-quality metric yet. Its six
initial behavior cases form a regression floor; future optimization should use
approved campaign-ticket and creative-review outcomes rather than synthetic
scores alone.

## Before Behavior

- No planner creates the canonical ticket for a paid-ad operating loop.

## After Behavior

- One planner creates the ticket, preserves existing ownership, and makes
  operation-specific approvals visible.

## Followups

- Add an approved write-capable Meta adapter only under a separate ticket with
  dedicated authorization and mutation proof.
