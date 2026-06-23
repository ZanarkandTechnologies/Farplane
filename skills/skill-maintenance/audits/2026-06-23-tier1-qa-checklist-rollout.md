---
skill: skill-maintenance
date: 2026-06-23
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: docs/skills/registry.jsonl
after_ref: skills/advise/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 skills/skill-maintenance/scripts/check_skills.py
  - reviewer: TAS-A source-scope pass
eval_required: no
---

# Tier 1 QA Checklist Rollout

## Change

- Before: Tier 1 skills had first-load todo lists but no skill-local
  `qa_checklist.md` runtime guardrails.
- After: `advise`, `prototyping`, `reference-grounding`, and
  `telegram-message` each declare `qa_checklist: qa_checklist.md`, read it as
  preflight guardrails, and apply it again at finish for material work.
- Why: Tier 1 primitives shape many downstream workflows, so their common
  failure modes should be prevented before execution and checked again before
  completion.
- Tradeoff accepted: Keep the canonical filename `qa_checklist.md` for tooling
  and registry discovery, while using human titles like `QA / Review Checklist`
  inside the file.

## First-Principles Reasoning

- Objective: Make all Tier 1 skills safer to invoke by turning recurring
  gotchas into preflight and final-review checks.
- Placement logic: `qa_checklist.md` is the existing Farplane special file for
  skill-local runtime guardrails; renaming would break convention and add a
  migration without improving behavior.
- Expected behavior delta: Agents load the checklist before material use of a
  Tier 1 skill, use it during execution, and apply it again before claiming
  readiness.
- Proof needed: Skill-system validation plus reviewer inspection of checklist
  usefulness and gotcha deduplication.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Each Tier 1 `SKILL.md` now has a preflight checklist todo. |
| `reference_load_precision` | pass | Each frontmatter points to `qa_checklist.md` at package root. |
| `missing_context_rate` | pass | Each checklist includes preflight and final review sections. |
| `noisy_context_rate` | pass | Checklists are outside first-load body and not copied wholesale into gotchas. |
| `duplicated_instruction_count` | pass | Checklist items focus on failure scans, not repeating every todo step. |
| `prompt_size_tokens` | pass | `SKILL.md` changes are compact pointers. |
| `task_success_rate` | unknown | No live invocation eval was run. |
| `review_tas_rate` | pass | Reviewer lane returned TAS-A for intended source scope. |
| `maintenance_locality` | pass | Owner remains each skill package plus `skill-maintenance` audit. |
| `composition_clarity` | pass | Checklists define `*_check(...) -> pass | violation | deferral`. |

## Proof Artifacts

- Skill-local evals, when needed: not needed for checklist artifact rollout.
- Structure evals, when needed: `check_skills.py --write`.
- Reviewer receipt: TAS-A for source scope; generated registry/graph output
  requires a separate clean generated-output pass before committing those files.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no.
- Evidence gaps: no live transcript proving agents always read the checklist on
  future skill calls; generated registry/graph files are dirty with unrelated
  workspace changes and should not be bundled into the Tier 1 source rollout.

## Before Behavior

- Tier 1 skills could be invoked without a dedicated preflight/final checklist
  that captures their most likely misuse modes.

## After Behavior

- Tier 1 skills have discoverable package-local QA/review checklists that guide
  both author execution and independent final review.

## Followups

- Consider a later bulk pass for Tier 2 skills after the Tier 1 pattern is
  reviewed and accepted.
- Regenerate and review generated registry/graph outputs from a clean or
  explicitly scoped workspace before committing those generated files.
