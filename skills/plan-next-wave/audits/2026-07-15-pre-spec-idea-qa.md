---
skill: plan-next-wave
date: 2026-07-15
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/plan-next-wave/SKILL.md@HEAD-820-lines-plus-concurrent-dirty-base
after_ref: skills/plan-next-wave/SKILL.md@749-lines-plus-owner-local-references
reasoning_basis: reviewer
proof_artifacts:
  - tickets/TASK-0380/artifacts/evals/baseline.md
  - tickets/TASK-0380/artifacts/agent-qa/plan.md
  - tickets/TASK-0380/artifacts/review/plan-readiness.md
eval_required: yes
---

# Pre-Spec Idea QA Audit

## Change

- Before: structurally valid candidates could reach full ticket expansion
  without a ten-second-comprehensible idea card or causal evidence receipt.
- After: every candidate exposes an Idea Card and evidenced Idea QA receipt;
  only cards whose five required families are all `TAS-A` and whose novelty
  and preference hard gates pass may enter comparison. Only selected survivors
  expand into full specs.
- Why: ticket structure, KPI fit, and citation presence did not prove that a
  human could understand or want the proposed result.
- Tradeoff accepted: a larger mandatory planner receipt in exchange for cheap
  rejection before expensive spec expansion.

## First-Principles Reasoning

- Objective: spend autonomous capacity only on ideas the ICP can understand,
  experience, and use to change a decision.
- Placement logic: admission belongs in `plan-next-wave`; detailed anchors and
  examples live in `references/idea-qa.md`; mechanical shape belongs in the
  existing validator.
- Expected behavior delta: opaque, self-referential, weakly grounded, repeated,
  or preference-incompatible ideas remain visible but cannot become specs.
- Proof needed: deterministic schema tests, natural variable-behavior cases,
  adversarial agent QA, and independent completion review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Required response order, gate, signature, todo, and spec receipt remain in `SKILL.md`. |
| `reference_load_precision` | pass | The reference map names `references/idea-qa.md` as the card/anchor/example owner. |
| `missing_context_rate` | pass | Threshold, hard gates, source-gap rule, and purity boundary are first-load behavior. |
| `noisy_context_rate` | pass | Detailed anchors and examples moved to the new reference instead of being duplicated inline. |
| `duplicated_instruction_count` | pass | Skill owns execution, reference owns calibration, checklist owns preflight, validator owns shape, evals own variable behavior. |
| `prompt_size_tokens` | pass | First-load skill is now 749 lines versus 820 at HEAD; the 144-line executable-spec schema moved intact to an owner-local reference. |
| `task_success_rate` | pass | Live GPT-5.6 invalid and admitted paths are semantic TAS-A plus zero lifecycle errors; 47 deterministic tests pass. |
| `review_tas_rate` | pass | Independent tester passes; evidence and completion reviews are TAS-A. |
| `maintenance_locality` | pass | New calibration detail is owner-local under `skills/plan-next-wave/`. |
| `composition_clarity` | pass | Inputs include World Memory and preference memory; outputs separate cards, comparison, rejections, and specs. |

## First-Load Review

```text
first_load_review:
  line_count_before: 820 (HEAD; concurrent dirty base already existed)
  line_count_after: 749
  kept_in_skill: response seam, hard gates, signature, todo, compact spec receipt
  moved_to_reference: TAS family rubrics, named checks, evidence definitions, preference normalization, examples, and the always-linked executable ticket-spec schema
  deleted_as_duplicate_or_rationale: none attributable safely across concurrent dirty edits
  extra_sections_kept_with_reason: response/spec contracts are consumed on every planner invocation
  remaining_sections_over_budget: none identified by the skill surface budget check
  proof_surface_fit: deterministic validator + natural evals + agent QA + reviewer
  task_case_quality: five distinct observed failure classes; queries do not name expected rubric results
  anti_cheat_case_design: pass via check_eval_queries.py and independent review
  qa_preflight_loaded: pass
  qa_finish_independence: pass; tester, evidence reviewer, and completion reviewer are independent lanes
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass; eval fixture uses clean-room toy project
  low_value_prose_scan: pass; duplicated ticket-spec field prose was consolidated without removing fields
  verdict: pass
```

## Proof Artifacts

- Skill-local evals: five TASK-0380 rows in `evals/evals.json`.
- Validator: `scripts/test_validate_ticket_specs.py`.
- Reviewer receipts: `tickets/TASK-0380/artifacts/review/plan-readiness.md` and
  `tickets/TASK-0380/artifacts/review/completion-review.md` (TAS-A).
- Prior blocked attempts remain historical evidence. Codex CLI `0.144.4` now
  accepts `gpt-5.6-sol`; a direct exact-output probe passed on 2026-07-15.

## Before Behavior

- Lane candidates could be fully compared and expanded before cheap human
  comprehension, novelty, experiential output, or preference checks.

## After Behavior

- Idea cards and receipts precede comparison; rejected cards remain auditable;
  admitted specs carry the originating receipt and deterministic validation.

## Followups

- Run the delayed five-round human experiment before any dogfood-review rollout.
- Change rubric families or named checks only from human experiment evidence;
  never replace them with an aggregate score.
