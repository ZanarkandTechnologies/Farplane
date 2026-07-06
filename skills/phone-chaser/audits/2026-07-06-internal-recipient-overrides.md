---
skill: phone-chaser
date: 2026-07-06
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/phone-chaser/SKILL.md
after_ref: skills/phone-chaser/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
eval_required: no
---

# Skill Audit

## Change

- Before: `phone-chaser` described its scope as Kenji-facing reminders and
  explicit test calls.
- After: `phone-chaser` defaults to Kenji but allows a supplied phone-number
  override for named internal organization recipients or explicit test numbers
  with a legitimate reminder/escalation purpose.
- Why: The dispatch helper already supports `--phone-number`; the skill
  contract was narrower than the intended reminder workflow.
- Tradeoff accepted: The skill allows internal reminder flexibility while still
  blocking prospects, customers, public numbers, unknown recipients, and cold
  outreach.

## First-Principles Reasoning

- Objective: Make phone reminders useful for internal escalation without
  turning the skill into an outreach or robocall surface.
- Placement logic: The behavior boundary belongs in `SKILL.md`; the reusable
  dispatch guardrail belongs in `qa_checklist.md`.
- Expected behavior delta: Agents may pass `--phone-number` for approved
  internal/test recipients and must block unclear external recipients.
- Proof needed: Skill checker pass plus self-check that first-load and QA
  guardrails name the new allowed and blocked recipient classes.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` context, todo, gotcha, and template now state the override boundary. |
| `reference_load_precision` | pass | No new references were added. |
| `missing_context_rate` | pass | Allowed/blocked recipient rules remain in first-load context and QA. |
| `noisy_context_rate` | pass | The change added only compact operational guardrails. |
| `duplicated_instruction_count` | pass | `SKILL.md` owns execution boundary; `qa_checklist.md` owns reusable dispatch checks. |
| `prompt_size_tokens` | pass | `SKILL.md` remains under 150 lines. |
| `task_success_rate` | unknown | No live dispatch was run. |
| `review_tas_rate` | unknown | No independent reviewer was run for this small contract edit. |
| `maintenance_locality` | pass | Future edits have clear owners: skill contract and skill-local QA checklist. |
| `composition_clarity` | pass | Signature, gates, fails, todo, and output contract remain explicit. |

## Proof Artifacts

- Skill-local evals, when needed: not needed; no variable behavior or eval
  judge changed.
- Structure evals, when needed: not needed; no structure rewrite.
- Reviewer receipt: skipped; small owner-local contract edit.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed on 2026-07-06.
- Eval required: no.
- Evidence gaps: No live call was placed.

## Before Behavior

- Default call target was Kenji's configured reminder number.
- Override behavior existed in `dispatch_call.py` but was framed only as user
  supplied/approved without the internal-recipient policy in the guardrails.
- QA allowed only Kenji or explicit test numbers.

## After Behavior

- Default call target remains Kenji's configured reminder number.
- Overrides are allowed for named internal organization recipients and explicit
  test numbers when the request has a legitimate reminder/escalation purpose.
- QA blocks prospects, customers, public numbers, unknown recipients, guessed
  contacts, and unclear reminder relationships.

## Followups

- Done: the deployable worker's internal LiveKit participant name is now
  recipient-neutral.
