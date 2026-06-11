---
skill: skill-creator
date: 2026-06-11
change_type: structure
owner: skill-maintenance
status: pass
review_route: deliberative_advice
before_ref: working-tree-before-audit-standard
after_ref: working-tree-after-audit-standard
reasoning_basis: deliberative_advice
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - git diff --check
eval_required: no
---

# Skill Audit

## Change

- Before: new skill creation reviewed structure, metrics, and proof, but did not
  require a durable audit artifact for material skill creation or structure
  changes.
- After: `skill-creator` points material creation and structural edits to the
  shared skill audit template and warns against `health_score` or `last_edited`
  frontmatter. It also tells authors that first-load sufficiency outranks
  modular neatness and to place content by access frequency and owner scope.
  It treats best-practices as authoring context and prefers anchored sections
  over full-file loading.
- Why: audits should be part of the skill package when a skill's reusable
  behavior changes, so future maintainers can compare before and after.
- Tradeoff accepted: creation should record first-principles placement and
  before/after behavior, while evals remain optional proof for uncertain or
  measurable claims.

## First-Principles Reasoning

- Objective: make durable audit writeback part of material skill creation.
- Placement logic: new-skill authors see the audit requirement in
  `skill-creator`, but the audit template remains owned by `skill-maintenance`;
  cross-skill standards stay in docs while one-skill conditional detail goes to
  references.
- Expected behavior delta: material new skills gain a package-local audit trail;
  mechanical edits can explicitly skip it; required first-load rules stay in
  `SKILL.md` instead of disappearing into references. Skill creation loads only
  the relevant best-practices section unless the whole contract is being shaped
  or reviewed.
- Proof needed: validators prove template consistency; evals are needed only
  when claiming improved behavior.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | The review todo now names the audit path and skip condition. |
| `reference_load_precision` | pass | The full audit body is in `skill-maintenance/templates/skill-audit.md`. |
| `missing_context_rate` | pass | New skills see the audit expectation in both creator todo and starter template. |
| `noisy_context_rate` | pass | The template receives only a short audit note, not the full rubric body. |
| `duplicated_instruction_count` | pass | Audit rules are referenced from the owner template rather than copied in full. |
| `prompt_size_tokens` | pass | First-load increase is small and attached to final review. |
| `task_success_rate` | unknown | No skill-creation eval run was executed for this audit standard yet. |
| `review_tas_rate` | unknown | No reviewer receipt was produced for this change yet. |
| `maintenance_locality` | pass | `skill-maintenance` remains the owner of the audit template and mechanics. |
| `composition_clarity` | pass | Creation now composes with maintenance audits without making every new skill own audit mechanics. |

## Proof Artifacts

- Skill-local evals, when needed: not run.
- Structure evals, when needed: not run.
- Reviewer receipt: not produced.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no; this change defines authoring policy and does not claim
  measured agent behavior improved.
- Evidence gaps: no task-success or review-TAS measurement exists yet.

## Before Behavior

- New skills could be created with no durable audit trail unless a ticket or
  chat summary happened to preserve the reasoning.

## After Behavior

- Material new-skill work has a standard audit artifact path.
- New skill scaffolds preserve required trigger, context, gates, routing, proof,
  and output contracts in first load.
- New skill scaffolds point cross-skill standards to `docs/*` and one-skill
  conditional detail to `references/*`.
- New skill authors use best-practices as an authoring standard, not as runtime
  context every skill must load.
- Audit evidence stays binary and file-backed instead of becoming stale
  frontmatter metadata.

## Followups

- Add skill-creator eval rows that confirm material new-skill creation writes
  or explicitly skips an audit record.
