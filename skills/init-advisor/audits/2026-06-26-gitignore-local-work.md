---
skill: init-advisor
date: 2026-06-26
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/init-advisor/scripts/bootstrap.sh
after_ref: skills/init-advisor/scripts/bootstrap.sh
reasoning_basis: first_principles
proof_artifacts:
  - bash -n skills/init-advisor/scripts/bootstrap.sh
  - temp bootstrap fixture with git check-ignore probes
  - python3 bin/validators/check_farplane_project_files.py --root "$tmpdir"
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
eval_required: no
---

# Skill Audit

## Change

- Before: InitAdvisor bootstrap only appended `.farplane/reviews/` and
  `.farplane/` to generated `.gitignore` files, leaving active ticket work
  such as `tickets/TASK-0001/ticket.md` visible to Git by default.
- After: InitAdvisor owns `references/GITIGNORE_TEMPLATE` and bootstrap appends
  it as one named Farplane `.gitignore` block that ignores `.farplane/`, active
  `tickets/**`, and non-skill `.agents/*`, while preserving
  `tickets/README.md`, `tickets/templates/**`, and `.agents/skills/**` as
  trackable scaffold.
- Why: new repos should inherit the same clean worktree boundary that Farplane
  already uses locally, instead of requiring repeated operator correction.
- Tradeoff accepted: active ticket files become local execution state by
  default; teams that want to version project-specific tickets can override the
  generated `.gitignore` intentionally.

## First-Principles Reasoning

- Objective: reduce repeated noisy Git status in newly initialized Farplane
  projects without hiding canonical framework config.
- Placement logic: `skills/init-advisor/references/GITIGNORE_TEMPLATE` owns the
  reusable ignore policy, `scripts/bootstrap.sh` applies generated project
  scaffolding, and `docs/farplane-framework/project-files.md` owns the
  framework file boundary.
- Expected behavior delta: fresh bootstrap emits a reusable ignore policy for
  local Farplane work state.
- Proof needed: shell syntax, fixture bootstrap, Git ignore probes, project
  validator, and skill-system check.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` now says active ticket work is ignored and ticket templates are tracked. |
| `reference_load_precision` | pass | README, SKILL.md, and project-files docs point to `references/GITIGNORE_TEMPLATE`. |
| `missing_context_rate` | pass | QA checklist names the runtime/ticket boundary as a finish gate. |
| `noisy_context_rate` | pass | No broad skill references were added. |
| `duplicated_instruction_count` | pass | The full ignore pattern lives in bootstrap and the framework doc; SKILL.md keeps a concise rule. |
| `prompt_size_tokens` | pass | Small first-load wording change only. |
| `task_success_rate` | pass | Temp fixture showed active ticket files ignored and scaffold files unignored. |
| `review_tas_rate` | unknown | No independent reviewer was run for this small owner-local change. |
| `maintenance_locality` | pass | Edits stayed in InitAdvisor source, QA checklist, and framework file-boundary doc. |
| `composition_clarity` | pass | Skill-maintenance validation passed after the edit. |

## Proof Artifacts

- Skill-local evals, when needed: not needed; no eval contract changed.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: skipped; self-check is sufficient for this small bootstrap
  behavior correction.
- Validator: `python3 bin/validators/check_farplane_project_files.py --root "$tmpdir"`.
- Eval required: no.
- Evidence gaps: none for bootstrap ignore behavior; no install sync was run.

## Before Behavior

Fresh bootstrap left active `tickets/TASK-*` files unignored unless a repo or
operator added that rule later.

## After Behavior

Fresh bootstrap appends `references/GITIGNORE_TEMPLATE`:

```gitignore
# Farplane local runtime and work state
.farplane/
tickets/**
!tickets/README.md
!tickets/templates/
!tickets/templates/**
.agents/*
!.agents/skills/
!.agents/skills/**
```

## Followups

- Consider an explicit validator check for generated `.gitignore` content if
  future init dogfood finds this drifting again.
