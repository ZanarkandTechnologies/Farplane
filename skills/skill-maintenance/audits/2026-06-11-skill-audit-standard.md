---
skill: skill-maintenance
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

- Before: skill maintenance validated structure and registry drift, but did not
  own a durable before/after audit record for material skill changes.
- After: skill maintenance owns `audit_skill_structure(...)`, the
  `templates/skill-audit.md` artifact, and skill-local audit writeback for
  material skill changes. It also states that first-load sufficiency outranks
  modular neatness when required every-invocation rules are at stake, and uses
  placement boundaries for `SKILL.md`, skill-local references, shared docs,
  templates, and evals. The best-practices doc is now scoped as an authoring
  standard, not runtime context for ordinary skill use.
- Why: skill structure quality compounds across future agents and needs binary
  evidence, not transcript memory or numeric health scores.
- Tradeoff accepted: first-principles review is sufficient for most structure
  changes; evals and reviewer receipts are reserved for uncertainty, regressions,
  disagreement, or measured claims.

## First-Principles Reasoning

- Objective: make material skill changes leave durable before/after evidence.
- Placement logic: `skill-maintenance` owns audit mechanics; the shared standard
  owns the policy; individual skill packages own their audit records and
  skill-local references.
- Expected behavior delta: future agents record reasoning and evidence gaps
  instead of writing stale health scores into front matter, and cleanup passes
  do not move required first-load rules into references just to shorten
  `SKILL.md`. Maintenance loads anchored best-practices sections by default and
  the full file only for broad audits or standard-setting changes.
- Proof needed: validators prove structural consistency; evals or reviewer
  receipts are needed only for measured behavior claims.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names the audit function, write path, and skip rule. |
| `reference_load_precision` | pass | The reusable audit body lives in `templates/skill-audit.md`; first-load text keeps only routing rules. |
| `missing_context_rate` | pass | Audit path, material-change boundary, and no-score rule are explicit. |
| `noisy_context_rate` | pass | Long audit checklist is in the template, not expanded repeatedly in first-load prose. |
| `duplicated_instruction_count` | pass | Shared standard lives in `docs/skills/best-practices.md`; skill-maintenance points to it and owns the template. |
| `prompt_size_tokens` | pass | Added first-load instructions are compact relative to the function they enable. |
| `task_success_rate` | unknown | No skill-local eval run was executed for this audit standard yet. |
| `review_tas_rate` | unknown | No reviewer receipt was produced for this change yet. |
| `maintenance_locality` | pass | Skill audit mechanics are owned by `skill-maintenance`. |
| `composition_clarity` | pass | `audit_skill_structure(skill, change, evidence?)` exposes inputs, output, state, gates, routes, and failure modes. |

## Proof Artifacts

- Skill-local evals, when needed: not run.
- Structure evals, when needed: not run.
- Reviewer receipt: not produced.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no; this change defines structure policy and does not claim
  measured agent behavior improved.
- Evidence gaps: no task-success or review-TAS measurement exists yet.

## Before Behavior

- Material skill changes could be summarized in chat or tickets without a
  skill-local before/after audit artifact.
- Numeric health-score thinking could drift into front matter.

## After Behavior

- Material skill changes create `skills/<skill>/audits/*.md` records or state a
  mechanical skip reason.
- First-load sufficiency is treated as higher priority than reference
  modularity.
- Content placement now depends on access frequency, owner scope, depth, and
  length rather than length alone.
- `docs/skills/best-practices.md` is treated as skill-authoring context, not
  always-on runtime context.
- Reviews use binary `pass` / `fail` / `unknown` rows and evidence-backed claims.
- `health_score` and `last_edited` do not belong in `SKILL.md` front matter.

## Followups

- Add focused eval rows for skill audit behavior before claiming improved
  `task_success_rate`.
- Produce reviewer receipts for future high-blast-radius audit-standard changes.
