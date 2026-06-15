---
skill: harness-creator
date: 2026-06-15
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/harness-creator/references/harness-il.md
after_ref: skills/harness-creator/references/harness-il.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/harness-creator/SKILL.md
  - skills/harness-creator/references/harness-il.md
  - skills/harness-creator/templates/project-harness.md
  - docs/specs/program-notation.md
eval_required: no
---

# Skill Audit

## Change

- Before: External data, account, notification, and shared-team access needs
  risked becoming a separate external-IO abstraction or loose Markdown notes.
- After: The harness program represents those needs as `skill` capabilities
  with `requires` inputs, then emits `ticket` nodes with `type: unblock`.
- Why: The harness should stay structured while human setup work moves into the
  ticket system.
- Tradeoff accepted: The notation reuses the existing ticket primitive for
  human setup, avoiding another top-level model.

## First-Principles Reasoning

- Objective: Keep `project-harness.md` compact and executable-looking while
  making human access/setup blockers visible and actionable.
- Placement logic: `skill` owns capabilities; `ticket type: unblock` owns
  human setup inputs and the actual work item.
- Expected behavior delta: Agents create/propose unblock tickets for metrics,
  memory sync, notifications, accounts, and approvals instead of burying them
  in notes.
- Proof needed: Skill and doc validators plus manual inspection of the grammar
  and template.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` requires operator unblocks to be ticketed. |
| `reference_load_precision` | pass | `harness-il.md` owns `skill requires` and `ticket type: unblock` notation. |
| `missing_context_rate` | pass | Output contract names unblock tickets. |
| `noisy_context_rate` | pass | Detailed examples stay in reference/template. |
| `duplicated_instruction_count` | pass | No separate external-IO abstraction added. |
| `prompt_size_tokens` | pass | First-load change is small. |
| `task_success_rate` | unknown | Needs pilot. |
| `review_tas_rate` | unknown | No independent reviewer lane run. |
| `maintenance_locality` | pass | Future changes belong in notation reference and template. |
| `composition_clarity` | pass | Skill capability, required input, unblock ticket, and fallback loop are distinct. |

## Proof Artifacts

- Skill-local evals, when needed: not required.
- Structure evals, when needed: standard skill validators.
- Reviewer receipt: local self-check only.
- Validator: final command output belongs in implementation closeout.
- Eval required: no.
- Evidence gaps: pilot should test whether unblock tickets reduce operator
  confusion.

## Before Behavior

- Human setup and data-access blockers could remain in Markdown evidence notes.

## After Behavior

- Human setup and data-access blockers become explicit `ticket` program nodes
  with `type: unblock`.

## Followups

- Add an unblock-ticket template only after the first pilot shows repeated
  ticket fields.
