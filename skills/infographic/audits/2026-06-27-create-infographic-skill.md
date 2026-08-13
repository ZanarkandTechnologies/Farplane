---
skill: infographic
date: 2026-06-27
change_type: structure
owner: skill-creator
status: pass
review_route: self_check
before_ref: none
after_ref: skills/infographic/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/infographic/eval_task.json
  - skills/infographic/qa_checklist.md
  - skills/infographic/examples/handdrawn-saas-wireframe/assets/reference.png
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
eval_required: yes
---

# Skill Audit

## Change

- Before: Farplane had `image-generation`, `visual-design`, a standalone data-visualization skill, and
  `social-content`, but no single owner for infographic packets or text-dense
  product-storyboard visuals.
- After: Added `infographic` as a Tier 3 content-visual skill with a
  `infographic:handdrawn-saas-wireframe` method reference, QA checklist,
  positive example, eval task, and durable reference asset.
- Why: The requested reference style needs message structure, exact copy,
  layout planning, and production-route choice before image generation.
- Tradeoff accepted: The first version emphasizes repeatable skill contract and
  prompt/render planning over shipping a renderer script immediately.

## First-Principles Reasoning

- Objective: Make agents reliably produce or hand off dense explanatory
  infographics like the provided hand-drawn dashboard storyboard.
- Placement logic: A new Tier 3 skill is justified because the trigger is
  reusable and spans several downstream production skills; the hand-drawn SaaS
  look is a method reference because it is one style branch, not the whole
  domain.
- Expected behavior delta: Agents build copy inventory, layout spec, style
  profile, and proof plan before rendering or image generation.
- Proof needed: Skill validation, checklist self-check, and a future behavior
  run that tries the skill on multiple briefs.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes trigger, signature, todos, gates, output, and references. |
| `reference_load_precision` | pass | The hand-drawn method reference has a specific load condition in Todo List and Reference Map. |
| `missing_context_rate` | pass | Default path keeps copy, layout, production, and proof rules in first load. |
| `noisy_context_rate` | pass | Long style recipe lives in `references/handdrawn-saas-wireframe.md`. |
| `duplicated_instruction_count` | pass | `qa_checklist.md` owns detailed checks; `SKILL.md` only names the preflight/final gate. |
| `prompt_size_tokens` | pass | First-load skill remains compact enough for normal invocation. |
| `task_success_rate` | unknown | Needs behavior run through the Goal Packet. |
| `review_tas_rate` | unknown | Reviewer lane not run in this creation pass. |
| `maintenance_locality` | pass | Infographic domain owns packet shape; method reference owns style branch. |
| `composition_clarity` | pass | Routes and downstream skill owners are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/infographic/eval_task.json`
- Structure evals, when needed:
  `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed
- Reviewer receipt: skipped for first scaffold; Goal Packet requires later review
- Validator: passed; `python3 bin/validators/sync_skill_registry.py --check`
  also passed
- Eval required: yes, but behavior execution is assigned to `tickets/TASK-0238`
- Evidence gaps: no rendered sample produced yet

## Before Behavior

- A user asking for a text-dense infographic could be routed directly to image
  generation, risking unreadable labels and missing source-truth checks.

## After Behavior

- The agent creates an `Infographic Packet`, chooses a method, preserves exact
  copy, and names deterministic rendering or visual QA when needed.

## Followups

- Run the TASK-0238 Goal loop to generate 2-3 sample artifacts and refine the
  style reference or add a renderer template if deterministic rendering proves
  necessary.
