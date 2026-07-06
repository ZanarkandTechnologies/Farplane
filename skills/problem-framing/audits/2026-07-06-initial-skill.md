---
skill: problem-framing
date: 2026-07-06
change_type: structure
owner: skill-creator
status: pass
review_route: self_check
before_ref: none
after_ref: skills/problem-framing/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/problem-framing/eval_task.json
  - skills/problem-framing/examples/static-calculator-problem-frame/example.md
eval_required: yes
---

# Skill Audit

## Change

- Before: No skill owned turning complaints or feature requests into a problem
  frame before MVP, PRD, or ticket work.
- After: `problem-framing` owns complaint/request to problem frame, boundary
  options, constraints, and next-owner routing.
- Why: Existing skills cover brainstorming, interviews, PRDs, system design,
  UI workflow, and implementation planning, but not the symptom/problem split
  and product-boundary restraint.
- Tradeoff accepted: Adds one Tier 2 workflow, but keeps the agency-level MVP
  workflow out of this primitive.

## First-Principles Reasoning

- Objective: prevent agents from building the first requested artifact before
  the real problem, actor, stakes, and boundary are clear.
- Placement logic: Tier 2 because many product and execution workflows can use
  it as a medium-compounding framing interface.
- Expected behavior delta: agents preserve uncertainty and recommend the next
  owner instead of jumping to implementation.
- Proof needed: skill-local eval cases for feature-request drift, unknowns, and
  overbuild restraint.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes trigger, signature, todo path, routes, gates, and output template. |
| `reference_load_precision` | pass | Only example reference is linked as a quality reference. |
| `missing_context_rate` | pass | Required actor, current workflow, constraints, boundary, and unknown handling are in first load. |
| `noisy_context_rate` | pass | Long rationale is avoided; example is in fixture. |
| `duplicated_instruction_count` | pass | Distinct from `solution-shaping`, `brainstorm`, `prd`, and `impl-plan`. |
| `prompt_size_tokens` | pass | First load is below the review pressure threshold. |
| `task_success_rate` | unknown | Eval cases added; runner not executed in this audit. |
| `review_tas_rate` | unknown | No independent reviewer lane run. |
| `maintenance_locality` | pass | Problem framing behavior has one package owner. |
| `composition_clarity` | pass | Signature names outputs, gates, routes, and fails. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/problem-framing/eval_task.json`
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: not run; self-check only for initial package creation.
- Validator: registry/skill validation command noted above.
- Eval required: yes.
- Evidence gaps: no live agent-behavior test yet.

## Before Behavior

- Agents had to choose between broad `brainstorm`, `deep-interview`, `prd`, or
  downstream execution skills when the real job was symptom/problem framing.

## After Behavior

- Agents can call `problem-framing` to produce a problem frame and route to
  `solution-shaping`, `research:*`, `prd`, `deep-system-design`,
  `functional-ui`, or `impl-plan`.

## Followups

- Run a behavior eval or `agent-behavior-test` after registry validation.
