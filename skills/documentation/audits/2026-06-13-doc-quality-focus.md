---
skill: documentation
date: 2026-06-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: advise
before_ref: skills/documentation/SKILL.md
after_ref: skills/documentation/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - skills/documentation/SKILL.md
  - skills/documentation/references/doc-quality-checklist.md
  - docs/skills/README.md
  - docs/skills/registry.jsonl
eval_required: no
---

# Skill Audit

## Change

- Before: `documentation` mixed official-doc fetching, source synthesis, durable
  doc writing, and review checks in one workflow.
- After: `documentation` owns durable doc writing and doc-quality review;
  compact official-doc lookup and evidence gathering route through
  `reference-grounding`, and detailed finish-pass checks live in a lazy-loaded
  reference.
- Why: Doc search is already a Tier 1 grounding primitive. The compounding skill
  value is making durable docs clearer, more consistent, and easier to review.
- Tradeoff accepted: The skill is less useful as a standalone API-doc fetcher,
  but routing becomes cleaner and the detailed writing checklist no longer
  pollutes first-load context.

## First-Principles Reasoning

- Objective: Prevent noisy docs with duplicate definitions, stale sections, and
  agent-facing commentary.
- Placement logic: `documentation` is Tier 2 because it composes grounding,
  writing, check passes, advice, and review. The Tier 1 evidence move remains
  `reference-grounding`.
- Expected behavior delta: Agents use `reference-grounding` to gather evidence,
  then use `documentation` to write or revise durable docs with reader-contract,
  consistency, and review checks.
- Proof needed: Registry sync, doc-reference validation, and targeted content
  inspection.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Todo list names reader contract, grounding, draft pass, finish-pass checklist, advice, and review. |
| `reference_load_precision` | pass | Detailed checks are in `references/doc-quality-checklist.md`, loaded only for the finish pass. |
| `missing_context_rate` | pass | Skill states doc search boundary and durable-doc owner surface. |
| `noisy_context_rate` | pass | Removed API-doc template, tool examples, and bulky review checklist from first-load body. |
| `duplicated_instruction_count` | pass | Official-doc lookup no longer duplicates `reference-grounding` as a full workflow. |
| `prompt_size_tokens` | pass | Skill body is focused on doc-quality workflow rather than mixed docs-fetch guide. |
| `task_success_rate` | unknown | No behavioral eval run. |
| `review_tas_rate` | unknown | No reviewer lane used for this local skill rewrite. |
| `maintenance_locality` | pass | Changes stayed in `skills/documentation`, generated registry, and selection guide. |
| `composition_clarity` | pass | Boundary is explicit: grounding first, documentation second, review for material docs. |

## Proof Artifacts

- Skill-local evals, when needed: not required for this boundary rewrite.
- Structure evals, when needed: standard skill maintenance check plus doc-ref
  validation.
- Reviewer receipt: not requested; `advise`-level decision was enough.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no.
- Evidence gaps: no live transcript eval proving future invocations route doc
  search through `reference-grounding`.

## Before Behavior

- The skill could be selected for both official-doc lookup and durable doc
  writing, causing overlap with `reference-grounding`.

## After Behavior

- The skill is selected for durable doc-writing quality and check passes, while
  source lookup is an input gathered through `reference-grounding`.

## Followups

- Add a small skill eval if future agents keep routing simple docs lookup to
  `documentation` instead of `reference-grounding`.
