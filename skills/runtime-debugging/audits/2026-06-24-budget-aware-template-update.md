---
skill: runtime-debugging
date: 2026-06-24
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/runtime-debugging/SKILL.md
after_ref: skills/runtime-debugging/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/runtime-debugging/SKILL.md
eval_required: no
---

# Skill Audit

## Change

- Before: `runtime-debugging` used the older first-load shape, had no skill
  signature, no template metadata, and no budget-aware execution contract.
- After: `runtime-debugging` declares `template_uses.skill-template: "0.3.2"`,
  adds a callable signature, keeps branch routing in the todo list, and routes
  budgeted runs through `budget-advisor` with concrete debugging personas.
- Why: Runtime debugging benefits from parallel perspectives, but expanded
  effort needs guardrails so lanes preserve the same evidence-first output
  contract instead of becoming vague extra review.
- Tradeoff accepted: The skill grows from 108 to 171 lines while moving full
  persona prompts to `references/budget-personas.md` so normal debugging does
  not pay the full ensemble context cost.

## First-Principles Reasoning

- Objective: Make runtime debugging current with the skill template standard and
  safely budget-aware.
- Placement logic: Always-needed budget contract stays in `SKILL.md`;
  bug-class playbooks and full persona prompts remain in `references/*`.
- Expected behavior delta: A caller can pass `budget` and get bounded
  same-skill expansion via `budget-advisor`, including multiple codebase
  exploration perspectives, while preserving root-cause and proof requirements.
- Proof needed: Structure checklist pass, link/reference sanity, and skill
  registry sync.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, todo list, budget route, persona reference, and output contract are in `SKILL.md`. |
| `reference_load_precision` | pass | Each reference is named with a branch condition in the todo list and Reference Map. |
| `missing_context_rate` | pass | Required gates, routes, and proof expectations remain first-load. |
| `noisy_context_rate` | pass | Bug-class details and full persona prompts remain in references. |
| `duplicated_instruction_count` | pass | Workflow prose was folded into the numbered todo list and output contract. |
| `prompt_size_tokens` | pass | `SKILL.md` is 171 lines, under the 250-line review threshold. |
| `task_success_rate` | unknown | No live runtime-debugging invocation was run. |
| `review_tas_rate` | unknown | No independent reviewer receipt was requested for this single-skill structure update. |
| `maintenance_locality` | pass | Budget contract lives in `SKILL.md`; conditional bug playbooks and personas stay in `references/*`. |
| `composition_clarity` | pass | Inputs, state reads/writes, gates, routes, fails, and output are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: not required; this is a structure and routing
  update, not a new runnable behavior benchmark.
- Structure evals, when needed: self-check against
  `skills/skill-maintenance/qa_checklist.md`.
- Reviewer receipt: skipped; materiality is bounded to one Tier 2 skill and the
  standard checker is the primary proof.
- Validator: pass, `python3 scripts/check_skills.py --write`.
- Eval required: no.
- Evidence gaps: no live debug session proves the new budget path in practice.

## Before Behavior

- Agents loaded a thin debugging workflow but had to infer composition inputs,
  budget expansion, and lane prompts on their own.

## After Behavior

- Agents load a current-template debugging workflow with an explicit
  `runtime_debugging(symptom, repro?, context?, budget?)` contract and a
  conditional persona reference for repro, codepath, evidence, concurrency,
  performance, and fix verification perspectives.

## Followups

- Add an eval case only after observing a budgeted runtime-debugging failure or
  repeated misuse in live work.
