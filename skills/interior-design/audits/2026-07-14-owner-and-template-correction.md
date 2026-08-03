---
skill: interior-design
date: 2026-07-14
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: interior behavior misplaced in visual-design
after_ref: interior-design template 0.3.8 package
reasoning_basis: operator_correction
proof_artifacts:
  - skills/interior-design/evals/evals.json
  - skills/interior-design/examples/isometric-office-reset/example.md
  - skills/interior-design/audits/evidence/2026-07-14-release-v2-summary.json
eval_required: yes
---

# Interior Design Owner And Template Correction

## Change

- Before: room program, adjacency, circulation, furniture grammar, negative
  space, and blockout acceptance were added to `visual-design`.
- After: those behaviors live in a dedicated `interior-design` skill using
  `skill-template` 0.3.8; `visual-design` returns to interface aesthetics.
- Why: the operator correctly identified the domain as interior design.
- Tradeoff accepted: one additional Tier 3 skill and registry entry in exchange
  for a clear trigger, domain-specific workflow, and clean downstream handoff.

## First-Principles Reasoning

- Objective: produce interiors the operator can judge before implementation.
- Placement logic: room-scale program and composition are reusable and distinct
  from screen-level visual design.
- Expected behavior delta: spatial requests invoke interior design; UI-only
  requests route to visual design; real construction compliance remains out of
  scope.
- Proof needed: five skill-local behavior cases, template and surface-budget
  validation, installed-copy parity, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `ownership_explicit` | pass | `SKILL.md` separates interior, UI, implementation, and construction-compliance owners. |
| `latest_template_truthful` | pass | Frontmatter declares `skill-template: 0.3.8`; `check_skills.py --write` passes. |
| `first_load_sufficiency` | pass | Trigger, signature, phases, seven-step workflow, gates, and output are first-load visible. |
| `reference_load_precision` | pass | Todo and Reference Map name when to load composition, example, template, and QA surfaces. |
| `domain_specificity` | pass | Program, adjacency, circulation, shell, furniture scale, negative space, lighting, and blockout gates are interior-specific. |
| `surface_budget` | pass | 7 top-level todos, 5 QA items, and 5 eval cases. |
| `positive_example` | pass | `examples/isometric-office-reset/example.md` provides a transferable accepted shape. |
| `task_success_rate` | pass | Release-v2 behavior suite: 5/5 A, pass rate 1.0. |
| `review_tas_rate` | pass | Independent re-review passed after aligning the brief/example contract and making the eval receipt portable. |

## Proof Artifacts

- `evals/evals.json`
- `qa_checklist.md`
- `examples/isometric-office-reset/example.md`
- `audits/evidence/2026-07-14-release-v2-summary.json` (portable receipt copied
  from the Farplane-UI local eval run)
- `check_skills.py --write`: 121 registered skills; template, todo-tier,
  surface-budget, capability, query, and doc-reference checks pass.
- Reviewer receipt: pass; repaired artifact contract, portable proof receipt,
  and installed-copy parity all verified with no blocking findings.

An earlier run using the configured `gpt-5.6-sol` model was invalid because
the installed Codex CLI did not support that model. Behavioral proof uses the
explicitly supported `gpt-5.4` agent and judge.

## Before Behavior

- Visual design had to reason about interiors beyond its screen-level owner
  boundary.

## After Behavior

- Interior composition has a stable domain owner and hands only remaining UI
  aesthetics to visual design after the blockout is accepted.

## Followups

- Apply the skill to the actual Office3D screenshot and obtain an operator
  verdict on a blockout before changing production layout code.
