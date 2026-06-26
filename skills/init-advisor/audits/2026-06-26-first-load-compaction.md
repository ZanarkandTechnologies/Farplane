---
skill: init-advisor
date: 2026-06-26
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/init-advisor/SKILL.md
after_ref: skills/init-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - wc -l skills/init-advisor/SKILL.md skills/init-advisor/qa_checklist.md skills/init-advisor/references/CODE_SCAFFOLD_RECIPES.md
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - bash -n skills/init-advisor/scripts/bootstrap.sh
  - temp bootstrap fixture with exact GITIGNORE_TEMPLATE diff and git check-ignore probes
  - python3 bin/validators/check_farplane_project_files.py
  - python3 bin/validators/check_farplane_project_files.py --root "$tmpdir"
eval_required: no
---

# Skill Audit

## Change

- Before: `SKILL.md` was 533 lines and carried generated-surface answer
  scripts, adaptive-intake detail, full-mode readiness prose, stack commands,
  quality-tooling slots, automation activation detail, and a generated-file
  inventory in first load.
- After: `SKILL.md` is 239 lines. First load keeps the trigger boundary,
  signature, phase boundary, executable todo path, gates, and precise reference
  map.
- Why: agents need InitAdvisor's execution contract before acting, but branch
  detail should load only after substrate, full-mode, automation, or code
  scaffold branches are selected.
- Tradeoff accepted: some explanatory detail now requires loading README,
  `qa_checklist.md`, `AUTOMATION_TEMPLATE.md`, or
  `CODE_SCAFFOLD_RECIPES.md` explicitly.

## First-Principles Reasoning

- Objective: reduce first-load context while preserving scaffold behavior,
  readiness gates, and proof requirements.
- Placement logic: `SKILL.md` owns every-invocation routing and gates;
  `qa_checklist.md` owns readiness and adaptive-intake review; README owns the
  "what this sets up" explainer; `CODE_SCAFFOLD_RECIPES.md` owns stack setup
  commands; `AUTOMATION_TEMPLATE.md` owns automation prompt content.
- Expected behavior delta: an invoking agent loads less default context and
  loads branch-specific detail only when that branch is chosen.
- Proof needed: skill line budget, skill-system validation, bootstrap fixture,
  and project-file validator.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, gates, phase boundary, todo path, and reference load conditions remain in `SKILL.md`. |
| `reference_load_precision` | pass | README, QA checklist, automation template, gitignore template, and code scaffold recipes have branch-specific load conditions. |
| `missing_context_rate` | pass | Readiness/adaptive-intake gates moved to `qa_checklist.md`, which `SKILL.md` says to load before dogfood/final readiness/material behavior changes. |
| `noisy_context_rate` | pass | Stack commands and "what this sets up" inventory are no longer first-load content. |
| `duplicated_instruction_count` | pass | Automation detail now relies on `AUTOMATION_TEMPLATE.md`; inventory detail relies on README/manifest. |
| `prompt_size_tokens` | pass | `SKILL.md` reduced from 533 lines to 239 lines. |
| `task_success_rate` | pass | Bootstrap fixture and project-file validator still pass. |
| `review_tas_rate` | unknown | No independent reviewer was run for this self-contained structure pass. |
| `maintenance_locality` | pass | Future edits have clear owners by branch surface. |
| `composition_clarity` | pass | Skill-system validation passed. |

## Proof Artifacts

- Skill-local evals, when needed: not needed; no eval case changed.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: skipped; self-check used for this scoped compaction.
- Validator: `python3 bin/validators/check_farplane_project_files.py`.
- Eval required: no.
- Evidence gaps: no independent reviewer.

## Before Behavior

Agents loaded a long InitAdvisor file before knowing whether the task needed
substrate setup, full-mode readiness, automation activation, or stack scaffold.

## After Behavior

Agents load a compact InitAdvisor execution contract first, then pull:

- `README.md` for generated-file inventory and manual bootstrap explanation.
- `qa_checklist.md` for adaptive-intake and full-mode readiness review.
- `AUTOMATION_TEMPLATE.md` for automation prompt content.
- `CODE_SCAFFOLD_RECIPES.md` for optional stack commands and quality-tooling
  slots.

## Followups

- Consider a focused eval that asks "what does init create?" and checks whether
  the agent loads README/manifest instead of answering from stale first-load
  memory.
