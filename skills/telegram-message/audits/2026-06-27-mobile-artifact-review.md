---
skill: telegram-message
date: 2026-06-27
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/telegram-message/SKILL.md
after_ref: skills/telegram-message/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/telegram-message/qa_checklist.md
  - skills/telegram-message/eval_task.json
  - docs/skills/registry.jsonl
eval_required: yes
---

# Skill Audit

## Change

- Before: `telegram-message` allowed artifact-ready messages to send local
  paths plus a short question, which fails when Kenji reads Telegram from a
  phone.
- After: `telegram-message` requires artifact-review messages to include inline
  decision content, a phone-openable URL, or a fallback/blocker instead of
  sending local-path-only review requests.
- Why: Human feedback loops only work when the notification itself is
  actionable from the channel where the human receives it.
- Tradeoff accepted: Telegram messages may be slightly longer for artifact
  review, but they should remain compact and decision-shaped rather than giant
  dumps.

## First-Principles Reasoning

- Objective: Make Telegram feedback requests viewable and answerable on a phone.
- Placement logic: This is a reusable notification guardrail, so it belongs in
  `telegram-message` first load and `qa_checklist.md`, with an eval regression
  case.
- Expected behavior delta: Callers should no longer send local filesystem paths
  as the only way to inspect a requested artifact.
- Proof needed: Skill-system validator passes, registry sync includes the new
  eval/checklist metadata, and the checklist directly blocks the observed
  failure.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` states the phone-viewability gate, view modes, and todo checks. |
| `reference_load_precision` | pass | Only `references/configuration.md` is listed, with a credential-fallback load condition. |
| `missing_context_rate` | pass | Required routing, gates, failure modes, command shape, and output contract are first-load. |
| `noisy_context_rate` | pass | Detailed review checks live in `qa_checklist.md`; first load stays under the line budget. |
| `duplicated_instruction_count` | pass | `SKILL.md` names the hard gate; checklist owns detailed pass/fail review. |
| `prompt_size_tokens` | pass | `SKILL.md` is compact enough for first-load use. |
| `task_success_rate` | unknown | No post-change Telegram worker run has been captured yet. |
| `review_tas_rate` | unknown | No independent reviewer receipt was requested for this same-scope hardening. |
| `maintenance_locality` | pass | Future notification viewability edits belong in this skill and checklist. |
| `composition_clarity` | pass | Signature names inputs, outputs, state, gates, routes, and fails. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/telegram-message/eval_task.json`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: skipped; focused Tier 1 hardening with direct observed
  failure and validator proof.
- Validator: `check_skills.py --write` passed on 2026-06-27.
- Eval required: yes, added as a regression case; not executed as a scored eval
  in this turn.
- Evidence gaps: Next Taste Loop notification should be observed to confirm the
  caller includes the actual concept-card content in Telegram.

## Before Behavior

- A valid-looking feedback request could say only:
  `Artifact: tickets/TASK-0240/artifacts/concept-cards-TL-EXP-001.md`.

## After Behavior

- Artifact feedback requests must include the options, excerpt, compact summary,
  or a phone-openable URL. Local paths are desktop refs only.

## Followups

- Update `optimize-with-human` and Taste Loop callers if they still generate
  local-path-only Telegram request bodies despite the primitive guardrail.
