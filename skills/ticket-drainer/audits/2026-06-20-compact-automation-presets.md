---
skill: ticket-drainer
date: 2026-06-20
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: farplane/automations.md detailed job blocks
after_ref: skills/ticket-drainer/SKILL.md and compact job_catalog presets
reasoning_basis: deliberative_advice
proof_artifacts:
  - skills/ticket-drainer/eval_task.json
  - skills/deep-init-project/eval_task.json
  - experiments/decisions/2026-06-20-automation-manifest-compactness/context.md
eval_required: yes
---

# Skill Audit

## Change

- Before: `farplane/automations.md` repeated job intent, reads, writes, and
  output details for recurring work.
- After: `farplane/automations.md` is a compact cadence manifest; reusable job
  behavior lives in skill-owned automation presets.
- Why: cadence config should be readable and project-local, while skills own
  reusable behavior and eval surfaces.
- Tradeoff accepted: compiled live automation prompts must expand skill presets
  carefully instead of copying full runbooks into the manifest.

## First-Principles Reasoning

- Objective: keep automation configuration readable without making live prompts
  vague or unevaluable.
- Placement logic: schedules, gates, report handles, target threads, freshness,
  and local overrides stay in the manifest; reads/writes/output defaults move to
  skills.
- Expected behavior delta: new project templates and Farplane's live manifest
  reference skill presets such as `ticket-drainer.daily` and
  `skill-maintenance.harden_skill`.
- Proof needed: skill registry recognizes the new skill, eval task files parse,
  and eval runner infrastructure can discover skill evals.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skills/ticket-drainer/SKILL.md` includes context, preset, signature, gates, todo, and output. |
| `reference_load_precision` | pass | No extra reference files required for the first slice. |
| `missing_context_rate` | pass | Child-thread handoff fields and report/ledger writeback are explicit. |
| `noisy_context_rate` | pass | Manifest job details were compressed to preset references. |
| `duplicated_instruction_count` | pass | Repeated reads/writes/output blocks removed from live/template manifests. |
| `prompt_size_tokens` | unknown | No token measurement run. |
| `task_success_rate` | unknown | New eval cases were added but not run through a model harness. |
| `review_tas_rate` | unknown | No independent reviewer receipt in this turn. |
| `maintenance_locality` | pass | Reusable behavior moved to skill packages; manifest keeps project-local wiring. |
| `composition_clarity` | pass | `job_catalog` names skill preset, freshness, report handle, dependencies, and overrides. |

## Proof Artifacts

- Skill-local evals, when needed:
  - `skills/ticket-drainer/eval_task.json`
  - `skills/deep-init-project/eval_task.json`
- Structure evals, when needed:
  - `python3 skills/eval/tests/test_run_evals.py`
- Reviewer receipt: not run; self-check only.
- Validator:
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 -m json.tool skills/ticket-drainer/eval_task.json`
  - `python3 -m json.tool skills/deep-init-project/eval_task.json`
- Eval required: yes; eval tasks now exist, but no model harness run was
  executed.
- Evidence gaps: independent review and model eval run.

## Before Behavior

Automation manifests duplicated skill runbook details, which made the manifest
large and made behavior changes harder to eval at the owning skill surface.

## After Behavior

Automation manifests point to skill-owned presets. `ticket-drainer` owns the
daily parent heartbeat contract and can be evaluated directly.

## Followups

- Add a deterministic validator for `job_catalog` preset names if compact
  notation becomes a shared contract.
- Recompile live automation prompts after any future preset schema change.
