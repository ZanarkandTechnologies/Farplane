---
skill: impl-plan
date: 2026-08-30
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/templates/ticket.md@0.3.1
after_ref: tickets/templates/ticket.md@0.3.2
reasoning_basis: first_principles
proof_artifacts:
  - skills/impl-plan/references/examples.md
  - skills/impl-plan/evals/evals.json
eval_required: yes
---

# Impl Plan Dual Change Preview Audit

## Change

- Before: `Delta` carried the feature-level Before / After / Example, while a
  Change Plan unit named files and a signature delta but did not consistently
  show the exact owner seam being transformed.
- After: `Delta` remains the feature/behavior preview, and each Change Plan
  unit adds a separate `Implementation Preview` with current owner evidence,
  the planned replacement, and one expected example.
- Why: reviewers need to verify both what changes experientially and what the
  implementation will change before approving execution.
- Tradeoff accepted: each change unit gains three compact preview rows; exact
  source is preferred, while illustrative syntax must be labeled.

## First-Principles Reasoning

- Objective: make implementation intent correctable at a glance without
  replacing the existing feature preview.
- Placement logic: the canonical ticket template owns both presentation
  shapes; the planner prompt fills them; examples and evals calibrate behavior.
- Expected behavior delta: planners preserve the feature-level Delta and add a
  distinct owner-level current -> planned -> expected preview per change unit.
- Proof needed: template registry sync, skill/eval lint, calibrated example,
  and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | The canonical ticket template visibly distinguishes both previews. |
| `reference_load_precision` | pass | The example is calibration-only and introduces no second schema. |
| `missing_context_rate` | pass | Current-owner evidence and the planned seam are explicit. |
| `noisy_context_rate` | pass | The preview is three rows inside each existing change unit. |
| `duplicated_instruction_count` | pass | Template owns shape; prompt states planner behavior; example demonstrates it. |
| `prompt_size_tokens` | unknown | No tokenizer comparison was required for the small prompt delta. |
| `task_success_rate` | unknown | Fresh judged planner execution has not been run. |
| `review_tas_rate` | pass | Independent re-review returned TAS-A with no blockers after grounding repairs. |
| `maintenance_locality` | pass | Source changes remain in the ticket template and `impl-plan` package; the generated template registry was synchronized. |
| `composition_clarity` | pass | Feature, implementation, and simulation views have distinct jobs. |

## Proof Artifacts

- Skill-local evals, when needed: the localized-backend row now asserts both
  previews and the smallest required Contract Diagram.
- Structure evals, when needed: `farplane lint evals --changed` and
  `skills/skill-maintenance/scripts/check_skills.py` pass.
- Reviewer receipt: TAS-A / pass; no blockers after the current-excerpt
  fallback and eval wording were reconciled.
- Validator: template registry regenerated through
  `bin/validators/sync_template_registry.py --write`.
- Eval required: yes; assertion coverage updated, fresh judged run pending.
- Evidence gaps: no fresh live planner output yet.

## Before Behavior

- A ticket could explain the feature delta but leave reviewers to infer the
  exact code, prompt, schema, config, or copy transformation.
- The localized-backend example and eval contradicted the required Contract
  Diagram by permitting its omission.

## After Behavior

- `Delta` answers “what changes for the user or system?”
- `Implementation Preview` answers “what exact owner seam will change?”
- `Contract Diagram` answers “how does the changed behavior execute and fail?”

## Followups

- Run the focused localized-backend judged eval when an external eval run is
  warranted; deterministic checks and independent contract review already pass.
