---
skill: social-content
date: 2026-06-29
change_type: structure | behavior | reference | eval
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/social-content/SKILL.md before 2026-06-29 local edit
after_ref: skills/social-content/SKILL.md + qa_checklist.md + eval_task.json
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-maintenance/scripts/check_skills.py --write
eval_required: yes
---

# Skill Audit

## Change

- Before: `social-content` had no `template_uses`, no skill-local QA checklist,
  no eval task, and `social-content:twitter-thread` guidance allowed vague
  premises or angle labels to pass as thread plans.
- After: `social-content` declares `skill-template: "0.3.6"`,
  `skill-qa-checklist: "0.1.0"`, and `skill-eval-task: "0.1.0"`; it has a
  first-load signature, phase boundary, concrete Twitter/X thread gate,
  `qa_checklist.md`, and an eval regression for thread options with real tweet
  stacks.
- Why: User feedback showed the skill produced high-level Twitter/X thread
  starting points instead of reviewable, value-bearing thread plans.
- Tradeoff accepted: The first-load skill grew from 152 to 206 lines to keep
  the concrete-structure gate and QA preflight visible on every invocation.

## First-Principles Reasoning

- Objective: Make `social-content:twitter-thread` produce reviewable thread
  plans with hook, reader value, tweet-by-tweet stack, evidence, payoff, and
  CTA before asking for approval.
- Placement logic: First-load behavior changed, so `SKILL.md` owns the gate.
  Detailed Twitter/X examples stay in `references/upstream-twitter.md`.
  Runtime guardrails live in `qa_checklist.md`. Regression proof lives in
  `eval_task.json`.
- Expected behavior delta: Future Taste Loop or Telegram review requests should
  not ask Kenji to approve vague options such as "Last 5 Percent Problem"
  unless the actual tweet progression is shown.
- Proof needed: JSON validity, skill-system validation, registry sync, and
  structure checklist review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` has context, signature, todo gates, gotchas, reference map, and output contract. |
| `reference_load_precision` | pass | `SKILL.md` names each reference and its load condition. |
| `missing_context_rate` | pass | Concrete thread planning gate remains in first load. |
| `noisy_context_rate` | pass | Long Twitter examples remain in `references/upstream-twitter.md`. |
| `duplicated_instruction_count` | pass | `SKILL.md` owns gates, checklist owns review checks, reference owns examples. |
| `prompt_size_tokens` | pass | `SKILL.md` is 206 lines, under the 250-line review budget. |
| `task_success_rate` | unknown | No live eval run was executed in this pass. |
| `review_tas_rate` | unknown | No independent reviewer receipt was produced. |
| `maintenance_locality` | pass | Future edits have clear owner surfaces. |
| `composition_clarity` | pass | Signature lists inputs, outputs, reads, writes, gates, routes, and fails. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/social-content/eval_task.json`
- Structure evals, when needed: `skills/social-content/qa_checklist.md`
- Reviewer receipt: skipped; self-check used because change is narrow and
  validator passed.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed on 2026-06-29.
- Eval required: yes, regression case added; not run in this pass.
- Evidence gaps: no live content-generation eval run or independent review.

## Before Behavior

- Twitter/X thread planning could present high-level premises or value labels
  without the actual tweet stack.
- Review requests could ask for approval of options that were not judgeable
  from Telegram.

## After Behavior

- Twitter/X thread options must include hook tweet, reader value promise,
  tweet-by-tweet stack, evidence/examples, payoff, CTA, and optional media.
- The checklist blocks product premises, positioning statements, or vague
  angles from being treated as concrete thread plans.

## Followups

- Run the new eval through the owning eval harness when a broader
  social-content hardening pass is scheduled.
