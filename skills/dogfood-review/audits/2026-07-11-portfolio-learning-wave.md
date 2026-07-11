---
skill: dogfood-review
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: parent-ticket-reviewer
before_ref: skills/dogfood-review/SKILL.md@173-lines
after_ref: skills/dogfood-review/SKILL.md@178-lines
reasoning_basis: deliberative-advice
proof_artifacts:
  - tickets/TASK-0320/ticket.md
  - skills/dogfood-review/SKILL.md
  - skills/dogfood-review/qa_checklist.md
  - skills/dogfood-review/eval_task.json
  - skills/dogfood-review/templates/dogfood-report.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Dogfood read current experiment packets and could create at most one
  new packet under a global WIP limit of one.
- After: Dogfood reads active and recent archived packets plus its prior report,
  derives a weekly portfolio ledger, and may create a bounded non-interfering
  wave with defaults of wave size 2, total WIP 3, and delayed-live WIP 1.
- Why: slow delayed pilots should not serialize unrelated immediate toy/eval
  proof, while Pulse remains the sole experiment executor and check-in owner.
- Tradeoff accepted: cross-surface transfer waits for a coherent weekly
  snapshot, so a terminal result may wait up to one week before portfolio
  rollout planning.

## First-Principles Reasoning

- Objective: increase useful self-improvement throughput without duplicate
  scoring, attribution interference, or a second execution loop.
- Placement logic: Dogfood owns cross-ticket learning and supply; each ticket
  owns experiment state and Check-In Program; Pulse owns dispatch.
- Expected behavior delta: archived results remain visible, due-but-unscored
  gaps cannot be silently promoted, immediate proofs use spare capacity, and
  delayed packets are self-contained for future check-in workers.
- Proof needed: six distinct eval cases, target QA checklist, JSON/query lint,
  skill-system validation, composed parent-ticket QA, and completion review.

## Structure Review

- `line_count_before:` 173
- `line_count_after:` 178
- `kept_in_skill:` portfolio inputs/outputs, cutoff and capacity rules,
  Check-In Program completeness, and the no-execution boundary because they
  are required on every invocation.
- `moved_to_reference:` none; detailed report fields remain in the existing
  report template.
- `deleted_as_duplicate_or_rationale:` single-packet/WIP-one wording and
  duplicated generic packet description.
- `extra_sections_kept_with_reason:` none beyond the current skill template.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature and todo bind archive/history, outcome views, capacity, packet shape, and owner boundaries. |
| `reference_load_precision` | pass | Every linked template, registry guide, and downstream skill has an explicit load condition. |
| `missing_context_rate` | pass | Cutoff, due-but-unscored, non-interference, transfer, and delayed Check-In Program behavior remain first-load. |
| `noisy_context_rate` | pass | Detailed report schema stays in `templates/dogfood-report.md`; first load remains 178 lines. |
| `duplicated_instruction_count` | pass | SKILL owns behavior, QA owns violation checks, report template owns rendered fields, and eval owns cases. |
| `prompt_size_tokens` | pass | First-load stays below the roughly 250-line review threshold. |
| `task_success_rate` | unknown | Parent ticket still needs composed six-case behavior QA. |
| `review_tas_rate` | unknown | Parent-ticket completion reviewer is pending. |
| `maintenance_locality` | pass | All executable portfolio-learning behavior is owner-local to `dogfood-review`. |
| `composition_clarity` | pass | Inputs, canonical state, outputs, capacity formula, routes, and handoff are explicit. |

## Eval And QA Sync

- Six evals cover cutoff/archive history, due-but-unscored state, monitoring plus
  concurrent immediate toys, bounded transfer, immediate no-debt packets, and
  delayed executable Check-In Programs.
- Reusable runtime guardrails are mirrored in `qa_checklist.md`; case-specific
  scenario details remain only in the evals.
- QA is useful both before execution (source/capacity/ownership gates) and after
  execution (packet count, program completeness, and no-execution receipts).

## Validation

- `python3 -m json.tool skills/dogfood-review/eval_task.json` - pass.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` - pass,
  including skill todo, registry, surface-budget, capability, eval-query, doc
  reference, and Python compile checks.

## Followups

- Parent TASK-0320 owns composed Goal Packet QA, cross-skill integration review,
  and live automation reconciliation.
