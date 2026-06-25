---
skill: harness-creator
date: 2026-06-26
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/harness-creator/SKILL.md
after_ref: skills/harness-creator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 bin/validators/check_farplane_project_files.py
  - python3 tickets/scripts/check_ticket_metadata.py
  - python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py --check
  - python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-framework-core --check
eval_required: no
---

# Local Product Skills

## Change

- Before: `harness-creator` defined products and inventoried skills, but did
  not explicitly derive local product workflow skills.
- After: it must map existing root and local skills first, then propose
  `farplane/skills/<product-skill>/SKILL.md` stubs or one refinement ticket for
  immature product workflows.
- Why: core product workflows are the company's monetizable production
  capabilities and need a durable feedback/hardening home.
- Tradeoff accepted: init is slightly more structured, but product execution
  gains a clear local skill owner and promotion path.

## First-Principles Reasoning

- Objective: connect product lines to executable, improvable workflows.
- Placement logic: product-specific workflows belong under `farplane/skills/`
  until repeated proof shows cross-project reuse.
- Expected behavior delta: PM activation waits until each core product line has
  an existing route, local product skill, or refinement ticket.
- Proof needed: skill checks, project-file validator, and ticket metadata.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `check_skills.py --write` passed |
| `reference_load_precision` | pass | no new mandatory deep reference added |
| `missing_context_rate` | unknown | no behavior run yet |
| `noisy_context_rate` | pass | product skill detail is one checklist phase plus template section |
| `duplicated_instruction_count` | pass | local/global promotion rule appears in skill and template where needed |
| `prompt_size_tokens` | unknown | not measured |
| `task_success_rate` | unknown | no behavior run yet |
| `review_tas_rate` | unknown | no reviewer run |
| `maintenance_locality` | pass | changes stay in harness-creator, init templates, project-file docs, and validators |
| `composition_clarity` | pass | lifecycle and framework graph checks passed |

## Proof Artifacts

- Skill-local evals, when needed: not required; behavior contract update only.
- Structure evals, when needed: `check_skills.py --write` passed.
- Reviewer receipt: not run.
- Validator: project-file validator, ticket metadata, lifecycle graph check,
  and framework-core graph check passed.
- Eval required: no.
- Evidence gaps: no live init run yet.

## Before Behavior

- Product lines could imply workflows, but there was no explicit place to store
  local product skills before promotion.

## After Behavior

- `harness-creator` derives local product skills under `farplane/skills/`,
  maps existing skill reuse first, and creates refinement tickets when a stub is
  premature.

## Followups

- Dogfood by deriving Farplane's first local product skills for experiment
  reports, trust ablations, and evidence distribution.
