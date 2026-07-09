---
skill: ad-advisor
date: 2026-07-09
change_type: structure
owner: skill-creator
status: pass
review_route: self_check
before_ref: none
after_ref: skills/ad-advisor/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - skills/ad-advisor/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: paid-ad guidance had no dedicated skill owner; social/account skills
  covered organic content and account metrics/publishing.
- After: `ad-advisor` owns campaign config, policy/spend gates, dry-run CLI/API
  handoff, and measurement setup.
- Why: paid ads combine external spend, platform policy, account bindings, and
  measurement; those risks deserve a separate advisor skill.
- Tradeoff accepted: this skill advises and prepares configs but does not ship
  a live Meta CLI wrapper script yet.

## First-Principles Reasoning

- Objective: help configure ads without accidentally launching spend or hiding
  account/credential assumptions.
- Placement logic: sibling to `social-content`, `x-account`, and
  `instagram-account`; downstream from offer/creative work and upstream of live
  platform mutation.
- Expected behavior delta: agents should produce dry-run or paused/draft plans
  and block live spend until approval is explicit.
- Proof needed: registry validation plus eval smoke rows for Meta CLI dry-run
  gate and sensitive-targeting risk.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, todo list, gates, routes, and output are in `SKILL.md`. |
| `reference_load_precision` | pass | References are handoff owners, not hidden default workflow. |
| `missing_context_rate` | pass | Spend gates, bindings, policy risks, and docs grounding are first-load. |
| `noisy_context_rate` | pass | No provider-specific command manual is embedded. |
| `duplicated_instruction_count` | pass | Organic account skills remain separate. |
| `prompt_size_tokens` | pass | First-load file is below the structure review threshold. |
| `task_success_rate` | unknown | Requires future eval runner evidence. |
| `review_tas_rate` | unknown | No independent reviewer lane run in this pass. |
| `maintenance_locality` | pass | Future edits belong in `skills/ad-advisor/`. |
| `composition_clarity` | pass | Inputs, gates, routes, outputs, and blockers are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/ad-advisor/eval_task.json`
- Structure evals, when needed:
  `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Reviewer receipt: self-check; no reviewer lane used because this is a small
  initial package with no live mutation scripts.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed.
- Eval required: yes, but runner execution is a follow-up when eval suite is
  selected.
- Evidence gaps: no live Ads CLI command or account-readiness check performed.

## Before Behavior

- Agents could mix paid ads into organic posting/account skills or skip spend
  gates.

## After Behavior

- Agents should advise on campaign setup, require bindings and budget gates,
  prepare dry-run/paused handoffs, and route live spend to review/approval.

## Followups

- Add a Meta-specific reference after the first real dry-run or account setup.
