---
skill: recap-task
date: 2026-08-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/recap-task/audits/2026-08-13-initial-recap-task.md
after_ref: skills/recap-task/SKILL.md
reasoning_basis: operator feedback + first-principles review
proof_artifacts:
  - .farplane/evals/runs/20260813-173654-task-0434-recap-task-grouped-quick-card-release-final/summary.json
  - tickets/TASK-0434/artifacts/review/2026-08-14-grouped-quick-card-rereview.md
eval_required: yes
---

# Grouped Quick-Card Audit

## Change

- Before: a recap led with a full topical briefing, forcing an operator to scan
  several sections before finding the reply posture, delta, and open loop.
- After: every recap leads with three visually grouped sections: `Now`,
  `Delta`, and `Risks & action`. `Before`, `After`, and an indented `Example`
  remain visible together; full context follows only when requested or required
  for a safe response.
- Why: a delayed reply needs a decision at a glance without losing the causal
  change and evidence basis that make the decision trustworthy.
- Tradeoff accepted: the first screen carries a compact source summary plus
  source-linked deltas, while the full timeline remains a deliberate detail
  layer instead of always competing for attention.

## First-Principles Review

- Objective: reduce rereading time without producing a shallow status update.
- Placement: the default response shape is needed on every invocation, so it
  belongs in `SKILL.md`, with the behavior expectations mirrored in local QA
  and eval assertions.
- Non-goals: no new task fields, no transcript storage, no automatic thread
  replies, and no omission of source gaps or failed attempts.
- Proof: validate package structure, run all five behavior cases, install the
  targeted package, compare source to installed copy, and obtain independent
  review. Repair any failed case before readiness.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names the governing-header placement, grouped card, full-detail trigger, source rules, and read-only limit. |
| `reference_load_precision` | pass | Existing ticket, QA, and eval references retain explicit load conditions. |
| `missing_context_rate` | pass | The release suite returned A for the explicit source-gap route and all bound-source routes. |
| `noisy_context_rate` | pass | The compact card is first load; detailed chronology remains conditional. |
| `duplicated_instruction_count` | pass | Output layout is owned by `SKILL.md`; QA and evals state only verifiable behavior. |
| `task_success_rate` | pass | Release suite: 5/5 A at `.farplane/evals/runs/20260813-173654-task-0434-recap-task-grouped-quick-card-release-final/summary.json`. |
| `review_tas_rate` | pass | Native reviewer returned TAS-A; receipt: `tickets/TASK-0434/artifacts/review/2026-08-14-grouped-quick-card-rereview.md`. |
| `maintenance_locality` | pass | `check_skills.py --write`, eval-query lint, ticket metadata, whitespace, targeted install, and source/installed diff all passed. |
| `composition_clarity` | pass | Independent review found the layered card, full-detail trigger, and source boundaries coherent. |

## Before Behavior

- Operators had all supported detail, but no enforced visual hierarchy for the
  immediate reply, change delta, or remaining action.

## After Behavior

- Operators receive a scannable decision card first, then source-linked detail
  when full recovery context is requested or safety requires it.

## Repair Log

- The initial grouped-card suite returned 3/5 A: the full-context case treated
  readable staged paths as a source gap, and the worktree case did not call its
  dated capture explicitly historical rather than live. The contract, QA, and
  affected eval assertions now require both behaviors; rerun the two failed
  cases before the final five-case suite.
- The focused repair run then passed full context but still described the
  worktree only as “scoped.” The contract now requires task-owned and excluded
  file paths so this boundary is inspectable and repeatable.
- The next full run exposed a detail-layer regression: some full recaps omitted
  the latest customer question, collapsed several dated events, or listed only
  source basenames. Full mode now requires the question or decision, one
  source-labeled entry per material event, and task-relative or supplied paths
  in its ledger; rerun the affected full-context and attempt-history cases.
- The focused detail rerun then showed that the project's governing response
  ledger must precede the card and that a full recap needs a final safe-next
  line after its source ledger. The output contract and assertions now make
  both positions explicit.
- The following targeted run still abbreviated dates, reduced source paths to
  basenames, and shifted `Goal` from the operator's immediate response need to
  the underlying implementation. Full-mode fields now prohibit those
  abbreviations and order the goal correctly.
- A final full-suite rerun exposed a remaining branch ambiguity: a material
  proof conflict could return only the card, and literal source paths could be
  grouped. The full layer is now mandatory for proof conflicts and every
  concrete path has its own ledger bullet.
- The conflict-ledger repair then left one full-history issue: rejected and
  incomplete attempts could be listed without their causal outcome. Full mode
  now requires a separate `Problems and attempts` chain so every disposition
  and remaining impact stays recoverable.
- The release rerun passed four cases and showed one remaining freshness issue:
  a worktree snapshot named its date but not its exact capture time. Worktree
  sources now require that timestamp alongside the historical-state warning.

## Proof To Date

- Release behavior suite: 5/5 A across full context, conflicting completion,
  failed attempts, missing durable context, and worktree-noise scope at
  `.farplane/evals/runs/20260813-173654-task-0434-recap-task-grouped-quick-card-release-final/summary.json`.

## Final Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write`, ticket
  metadata, eval-query lint, and whitespace checks passed.
- `bash install.sh --skills-only --skills recap-task --target
  /Users/kenjipcx/.codex` completed; `diff -ru skills/recap-task
  /Users/kenjipcx/.codex/skills/recap-task` had no output.
- Native review returned TAS-A with no hard gates; receipt:
  `tickets/TASK-0434/artifacts/review/2026-08-14-grouped-quick-card-rereview.md`.

## Followups

- `no_self_improve_reason`: this is a targeted output-shape correction; retain
  the five-case suite as the regression guard before considering further
  optimization.
