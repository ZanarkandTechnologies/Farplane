---
skill: landing-page
date: 2026-08-04
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: git:HEAD:skills/landing-page/SKILL.md
after_ref: working-tree:skills/landing-page/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/landing-page/evals/evals.json
  - tickets/TASK-9015/artifacts/qa/validation.md
  - tickets/TASK-9015/artifacts/review/completion-review.md
eval_required: yes
---

# Landing Page Plan-Only Handoff Audit

## Change

- Before: The skill combined landing strategy, specification, implementation
  handoff, frontend execution, and post-build proof in one workflow.
- After: The skill terminates at an approved `LANDING_SPEC.md` or blocked
  specification and returns it to `impl-plan`; the specification carries the
  downstream implementation and QA contract.
- Why: Landing expertise is a domain input to software planning, not a second
  implementation planner or executor.
- Tradeoff accepted: A build request crosses an explicit approval handoff, but
  the premium story, reference, asset, motion, and proof requirements remain
  available to the implementation plan.

## First-Principles Reasoning

- Objective: Preserve landing-page judgment while keeping one owner for the
  final software Change Plan and one later Goal execution path.
- Placement logic: Offer, story, sections, media intent, motion intent, and
  proof requirements belong in the landing specification; code and deployment
  belong after the calling implementation plan is approved.
- Expected behavior delta: The skill can no longer recurse into another
  planner or claim build completion; it produces a reusable, inspectable input.
- Proof needed: A conditional-asset eval, contradiction scan, landing linters,
  structure validation, and reviewer inspection of the handoff boundary.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Todo 5 and Core Workflow state the terminal artifact and prohibited execution actions. |
| `reference_load_precision` | pass | Premium methods and asset evidence remain deferred to the existing references. |
| `missing_context_rate` | pass | The selected live case preserved page-specific blockers and produced complete named spec handoffs from sparse inputs. |
| `noisy_context_rate` | pass | Complete licensed assets skipped discovery while reference-led assets alone triggered Asset Advisor. |
| `duplicated_instruction_count` | pass | The duplicated legacy nine-step workflow was removed; Planning Contract is canonical. |
| `prompt_size_tokens` | unknown | No before/candidate token measurement was run. |
| `task_success_rate` | pass | Conditional asset/spec handoff live receipt reached A with pass rate 1.0. |
| `review_tas_rate` | pass | TASK-9015 completion review passed TAS-A with no hard-gate failures. |
| `maintenance_locality` | pass | Changes remain inside landing-page surfaces plus generated registry and ticket evidence. |
| `composition_clarity` | pass | Landing-page returns the spec; impl-plan integrates it; Goal execution implements it. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/landing-page/evals/evals.json`.
- Structure evals, when needed: quick validation, landing linters, todo-tier,
  surface-budget, eval-query, registry, JSON, and diff checks.
- Reviewer receipt: `tickets/TASK-9015/artifacts/review/completion-review.md`.
- Validator: `tickets/TASK-9015/artifacts/qa/validation.md`.
- Eval required: yes; behavior changed.
- Evidence gaps: One selected landing-page behavior case was run; the owning
  eval file remains the broader regression surface.

## Before Behavior

- The skill could continue from approved spec into frontend build and runtime
  proof.
- Executor-stage language blurred ownership with the general implementation
  planner.

## After Behavior

- The skill approves or blocks `LANDING_SPEC.md` and stops.
- The spec carries asset, motion, accessibility, browser, mobile, and visual QA
  requirements to one later implementation plan.
- Asset Advisor remains conditional on missing, reference-led, generated, or
  rights-sensitive media.

## Followups

- Rerun the owning behavior case after future asset-routing or handoff changes.
