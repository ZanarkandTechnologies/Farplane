---
skill: skill-template
date: 2026-08-20
change_type: template
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: docs/skills/templates/SKILL_TEMPLATE.md@0.4.1
after_ref: docs/skills/templates/SKILL_TEMPLATE.md@0.4.4
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-maintenance/scripts/test_check_skills.py
  - skills/skill-maintenance/scripts/test_generate_template_intelligence.py
  - bin/validators/test_check_skill_surface_budget.py
eval_required: no
---

# Skill template 0.4.4 audit

## Change

- Before: the template used checkbox-shaped ordered todos and generic action
  placeholders; the golden pattern was only linked.
- After: the template uses a plain numbered stage contract and embeds the
  golden pattern's key moves: bind, inspect, show a failure example, preserve,
  optionally assert, and self-audit. Budget-specific routing is omitted from
  the universal template.
- Why: `SKILL.md` defines reusable behavior, not mutable task state. The useful
  information is the ordered transformation and expected stage result.
- Tradeoff accepted: older template versions keep their checkbox syntax until
  migrated on contact; the surface-budget counter accepts both recorded forms.

## First-Principles Reasoning

- Objective: make a newly created skill executable from its first load without
  encouraging generic checkbox scaffolding.
- Placement logic: the template owns new-skill structure; best practices own
  the shared authoring rule; validators own enforcement.
- Expected behavior delta: authors begin from a small proven trajectory and
  replace its prompts with domain-specific actions rather than inventing a
  checklist from scratch.
- Proof needed: parser tests, template-intelligence checks, scaffolder syntax,
  surface-budget counting, and the complete skill-system validator.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Golden stage moves are inline in the template. |
| `reference_load_precision` | pass | No external golden reference is required. |
| `missing_context_rate` | pass | Input, signals, preservation, optional gate, and finish are visible. |
| `noisy_context_rate` | pass | Five short stages; no long example or rubric added. |
| `duplicated_instruction_count` | pass | Template, best-practice rule, and validator have distinct owners. |
| `prompt_size_tokens` | pass | The template remains below its existing 200-line envelope. |
| `task_success_rate` | unknown | No agent-behavior rollout was requested. |
| `review_tas_rate` | unknown | Independent reviewer was not invoked for this direct edit. |
| `maintenance_locality` | pass | New structure is owned by template 0.4.4. |
| `composition_clarity` | pass | Ordered stages name input, transformation, gate, and return. |

## Proof Artifacts

- Structure evals: focused parser, template-intelligence, and surface-budget
  unit tests passed.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed with 125 registry rows and zero surface-budget failures.
- Eval required: no; the change is a deterministic Markdown structure and
  validation contract, not a claim of improved domain-task performance.
- Evidence gaps: no bulk migration or candidate/baseline agent eval.

## Before Behavior

- New skills were prompted with `- [ ] 1.` items and generic action labels.

## After Behavior

- New skills start with plain `1.` stages and see the compact golden trajectory
  directly in the template.

## Followups

- Migrate existing skills only when they adopt template 0.4.4; do not rewrite
  the portfolio mechanically.
