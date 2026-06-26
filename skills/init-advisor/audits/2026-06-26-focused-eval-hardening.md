---
skill: init-advisor
date: 2026-06-26
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: .farplane/evals/runs/20260625-192452-20260626-init-advisor-focused/summary.json
after_ref: .farplane/evals/runs/20260626-064248-20260626-init-advisor-focused-final/summary.json
reasoning_basis: eval
proof_artifacts:
  - .farplane/evals/runs/20260625-192452-20260626-init-advisor-focused/summary.json
  - .farplane/evals/runs/20260625-193814-20260626-init-advisor-pulse-single-v4/summary.json
  - .farplane/evals/runs/20260626-064248-20260626-init-advisor-focused-final/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Focused `init-advisor` eval returned `3 C`, `2 B`, `0 A`.
- After: First-load todo and QA checklist now name the missing generated
  surfaces, automation constraints, full-mode readiness fields, Pulse ticket
  selection contract, activation ID split, and quality-tooling routing.
- Why: The behavior existed partly in scattered prose but was not reliably
  surfaced when answering direct init lifecycle questions.
- Tradeoff accepted: Slightly more first-load text in exchange for fewer hidden
  lifecycle assumptions.

## First-Principles Reasoning

- Objective: Make `init-advisor` reliably answer current lifecycle evals without
  rerouting through a broad suite.
- Placement logic: The missed behavior belongs to the owner skill's first-load
  checklist and QA checklist because it is required every time init describes
  generated surfaces or readiness gates.
- Expected behavior delta: Answers should explicitly name `farplane/harness.md`,
  `farplane/products.md`, `farplane/automations.md`, Pulse/Interval contracts,
  full-mode operating-model gates, and blocked statuses.
- Proof needed: Focused `init-advisor` eval rerun plus skill validator.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `init_advisor_pulse_interval_01` rerun reached A after required generated-surface sentence. |
| `reference_load_precision` | pass | Patch stays in `SKILL.md` and `qa_checklist.md`; no broad reference chase added. |
| `missing_context_rate` | pass | Final focused suite reached 6/6 A. |
| `noisy_context_rate` | pass | Final focused suite reached 6/6 A without judge complaints about bloat. |
| `duplicated_instruction_count` | unknown | Manual pass kept repeated points scoped to execution and QA gates. |
| `prompt_size_tokens` | unknown | Not measured. |
| `task_success_rate` | pass | Focused suite changed from 3 C / 2 B to 6 A. |
| `review_tas_rate` | unknown | No reviewer receipt yet. |
| `maintenance_locality` | pass | Only `skills/init-advisor/*` changed. |
| `composition_clarity` | unknown | Pending focused eval. |

## Proof Artifacts

- Skill-local evals, when needed:
  `.farplane/evals/runs/20260625-193814-20260626-init-advisor-pulse-single-v4/summary.json`
  and `.farplane/evals/runs/20260626-064248-20260626-init-advisor-focused-final/summary.json`.
- Structure evals, when needed: not required for this behavior-only hardening.
- Reviewer receipt: not yet run.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: yes.
- Evidence gaps: No focused `init-advisor` gaps remain from this eval cluster.

## Before Behavior

- Direct init lifecycle answers omitted several required surfaces and gates even
  when the source skill contained related concepts elsewhere.

## After Behavior

- Required lifecycle details are present in first-load execution bullets and QA
  checks where future maintainers can find them.

## Followups

- Continue the lifecycle repair queue with remaining owner clusters.
