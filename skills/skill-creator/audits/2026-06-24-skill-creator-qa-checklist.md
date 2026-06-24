---
skill: skill-creator
date: 2026-06-24
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/SKILL.md
after_ref: skills/skill-creator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-creator/SKILL.md
  - skills/skill-creator/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: `skill-creator` relied on the generic skill-maintenance structure
  checklist but had no skill-local QA guardrails for authoring and scaffolding.
- After: `skill-creator` declares `qa_checklist.md`, loads it as preflight, and
  applies it again before completion.
- Why: Skill creation has recurring domain-specific risks: fake scaffolding,
  stale template metadata, hidden default behavior, and weak proof routing.
- Tradeoff accepted: Added one skill-local checklist file while trimming
  duplicate first-load gotcha/reference lines to keep `SKILL.md` near budget.

## First-Principles Reasoning

- Objective: Make every material skill-creator invocation check authoring,
  template, scaffolding, reference, and proof risks explicitly.
- Placement logic: First-load `SKILL.md` only names when to load the checklist;
  detailed checks live in `qa_checklist.md`.
- Expected behavior delta: Agents using skill-creator should read the checklist
  before skill work and record checklist verdicts before completion.
- Proof needed: quick validator, JSON/script checks, full skill-maintenance
  validation, and live install.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` tells agents to read `qa_checklist.md` as preflight. |
| `reference_load_precision` | pass | Checklist link states preflight and final-check use. |
| `missing_context_rate` | pass | Finish path requires applying `qa_checklist.md`. |
| `noisy_context_rate` | pass | Detailed QA items live in checklist, not `SKILL.md`. |
| `duplicated_instruction_count` | pass | Removed duplicate first-load lines while adding the checklist. |
| `prompt_size_tokens` | pass | `SKILL.md` is under the 250-line warning after trim. |
| `task_success_rate` | unknown | No behavior eval run; structure checks passed. |
| `review_tas_rate` | unknown | Self-check only. |
| `maintenance_locality` | pass | Skill-creator-specific QA now has one owner file. |
| `composition_clarity` | pass | Checklist covers authoring, scaffolding, references, templates, and proof. |

## Proof Artifacts

- Skill-local evals, when needed: not required
- Structure evals, when needed:
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/skill-creator`
  - `python3 -m py_compile skills/skill-creator/scripts/init_skill.py skills/skill-creator/scripts/quick_validate.py skills/skill-creator/scripts/package_skill.py`
  - `python3 scripts/check_skills.py --write` from `skills/skill-maintenance`
- Reviewer receipt: none
- Validator: passed on 2026-06-24
- Eval required: no
- Evidence gaps: no independent reviewer lane

## Before Behavior

- Skill creator could complete without checking skill-creator-specific QA risks.

## After Behavior

- Skill creator has a discoverable, skill-local checklist and first-load
  instructions to use it.

## Followups

- Promote repeated checklist misses into eval rows if future use shows agents
  still skip proof, source ownership, or scaffold hygiene.
