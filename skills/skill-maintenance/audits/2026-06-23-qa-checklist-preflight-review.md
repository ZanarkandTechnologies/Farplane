---
skill: skill-maintenance
date: 2026-06-23
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-maintenance/SKILL.md
after_ref: skills/skill-maintenance/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py
  - python3 -m py_compile skills/skill-maintenance/scripts/sync_skill_checklists.py
eval_required: no
---

# Skill Audit

## Change

- Before: Skill-local `qa_checklist.md` was described mostly as a final
  readiness or material-change checklist.
- After: Skill-local `qa_checklist.md` is a preflight-plus-final-review
  contract: invoking agents read it before execution, apply it again before
  completion, and route independent reviewer/subagent verification for material
  changes.
- Why: Checklists that are only loaded at the end catch failures after the agent
  has already made them. Loading the same checklist early prevents common
  gotchas, while a separate reviewer pass reduces self-certification risk.
- Tradeoff accepted: `SKILL.md` gets a compact pointer to `qa_checklist.md`
  rather than duplicating the whole checklist into `## Gotchas`.

## First-Principles Reasoning

- Objective: Make skill QA checklists prevent repeat mistakes and still provide
  finish-gate evidence.
- Placement logic: `skill-maintenance` owns skill structure, checklist sync,
  audits, and reviewer routing; `skill-creator` owns the template hook; docs
  explain the shared standard.
- Expected behavior delta: Skills with `qa_checklist.md` should load it on
  start, use it during execution, and apply it at finish with independent review
  for material work.
- Proof needed: Skill-system validation plus file inspection of the changed
  owner surfaces.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skills/skill-creator/references/SKILL_TEMPLATE.md` now tells agents to read `qa_checklist.md` during context loading. |
| `reference_load_precision` | pass | The checklist remains at the skill package root and is named directly. |
| `missing_context_rate` | pass | `skills/skill-maintenance/SKILL.md` adds `qa_checklist_design` and final reviewer routing. |
| `noisy_context_rate` | pass | The pattern avoids copying full checklist bodies into `## Gotchas`. |
| `duplicated_instruction_count` | pass | `skills/skill-maintenance/qa_checklist.md` adds `qa_gotcha_deduplication`. |
| `prompt_size_tokens` | pass | The template adds compact pointers, not long embedded checklists. |
| `task_success_rate` | unknown | No live skill invocation eval was run. |
| `review_tas_rate` | unknown | No reviewer receipt was requested for this narrow docs/contract edit. |
| `maintenance_locality` | pass | Owner remains `skill-maintenance`; no new skill was created. |
| `composition_clarity` | pass | The new invocation pattern is expressed as `skill_invocation_with_checklist(...)`. |

## Proof Artifacts

- Skill-local evals, when needed: not needed for this docs/contract change.
- Structure evals, when needed: not needed.
- Reviewer receipt: skipped; self-check is sufficient for a narrow wording and
  template contract update.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py`.
- Eval required: no.
- Evidence gaps: no live subagent run proving independent final review behavior.

## Before Behavior

- Agents could reasonably treat `qa_checklist.md` as a final inspection surface
  and miss checklist guardrails during execution.

## After Behavior

- Agents should read `qa_checklist.md` before execution, apply it again before
  completion, and use a reviewer/subagent for material checklist conformance.

## Followups

- Prototype the pattern on one high-traffic skill with an existing
  `qa_checklist.md` before bulk-updating older skills.
