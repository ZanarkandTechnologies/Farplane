---
skill: frontend-craft
date: 2026-06-15
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/frontend-craft/SKILL.md
after_ref: skills/frontend-craft/qa_checklist.md
reasoning_basis: user_observed_ui_copy_leak
proof_artifacts:
  - skills/frontend-craft/SKILL.md
  - skills/frontend-craft/qa_checklist.md
  - skills/frontend-craft/references/qa.md
eval_required: no
---

# Frontend Copy QA Checklist Audit

## Change

- Before: frontend QA mentioned long explanatory text only as a visual-quality
  cue, so developer-facing implementation prose could still leak into normal
  product screens.
- After: `frontend-craft` has a first-class `qa_checklist.md` with explicit
  checks for audience-facing copy, developer explainer paragraphs, help
  affordance routing, tooltip accessibility, copy density, rendered-copy
  evidence, and source-copy searches.
- Why: the operator observed UI text explaining Telegram routing, local gateway
  commands, env vars, and app-server plumbing directly in the UI. That is a
  reusable runtime guardrail, so it belongs in the skill-local QA checklist.
- Tradeoff accepted: the checklist does not ban technical copy. It requires the
  copy to live on an explicit settings, setup, diagnostics, logs, docs, or
  developer-console surface, and to use tooltips/popovers/docs links when the
  explanation is optional.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `owner_surface` | pass | `skills/frontend-craft/qa_checklist.md` is the skill-local checklist surface named by `docs/skills/system.md`. |
| `runtime_guardrail` | pass | The checklist applies after material UI/copy/help changes and before readiness claims. |
| `not_todo_duplicate` | pass | `SKILL.md` only routes when to use the checklist; detailed checks live in `qa_checklist.md`. |
| `audience_copy_specificity` | pass | Checks distinguish normal product screens from settings/setup/diagnostics/developer surfaces. |
| `tooltip_accessibility` | pass | Tooltip checks require visible trigger, keyboard/focus access, and no essential hover-only instructions. |
| `rendered_evidence` | pass | Checklist requires rendered copy inspection and source-copy search. |

## Proof

- Validation: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed and regenerated the skill registry with `frontend-craft` counted in
  the skill-local checklist set.
- Reviewer lane: skipped; this is a narrow owner-local checklist addition with
  self-check audit.
- Eval required: no; no eval reference point changed.
