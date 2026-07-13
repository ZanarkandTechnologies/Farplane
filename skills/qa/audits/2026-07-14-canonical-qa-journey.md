---
skill: qa
date: 2026-07-14
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/qa/audits/2026-07-13-single-owner-qa-journey.md
after_ref: tickets/archive/TASK-0356/ticket.md
reasoning_basis: reviewer
proof_artifacts:
  - tickets/archive/TASK-0356/artifacts/qa/test-output.txt
  - tickets/archive/TASK-0356/artifacts/qa/eval-summary.md
  - tickets/archive/TASK-0356/artifacts/review/completion-review.md
eval_required: yes
---

# Canonical QA Journey

## Change

- Before: the single-owner five-gate journey was present, but `qa`,
  `qa-tester`, the cookbook, and receipt examples disagreed about current
  ticket fields, runtime binding, evidence branches, writeback, and learning.
- After: `qa` owns one current-schema contract and validated receipt;
  `qa-tester` loads that contract and focuses on operation/capture; the guide
  and cookbook describe the same journey and selective learning loop.
- Why: duplicated contracts allowed correct policy to drift into incorrect
  execution.
- Tradeoff accepted: the QA skill grows from 167 to 233 lines so the canonical
  schema and hard gates remain first-load visible, while the actor prompt drops
  from roughly 294 to 180 lines by routing detailed browser recipes to their
  owning skills and runbooks.

## First-Principles Reasoning

- Objective: make ticket proof repeatable, inspectable, and reusable without
  self-approval or browser-only assumptions.
- Placement logic: human guidance stays in `qa/`; reusable execution and
  receipt semantics stay in `skills/qa`; the isolated operator role stays in
  `agents/qa-tester.toml`; mechanical receipt checks stay skill-local.
- Expected behavior delta: current tickets are read correctly, runtime gaps
  block, UI and non-UI evidence branch honestly, receipts are validated,
  `Links` is canonical, `progress.md` is conditional, and learning is classified.
- Proof needed: validator unit tests, query-spoiler check, real Codex QA skill
  eval, skill/docs/ticket validation, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, todo, schema, invariants, routes, and stop behavior remain in `SKILL.md`. |
| `reference_load_precision` | pass | Browser detail routes explicitly through `agent-browser`; no required receipt behavior moved out of first load. |
| `missing_context_rate` | pass | Current ticket fields, effective proof policy, runtime gate, and writeback are explicit. |
| `noisy_context_rate` | pass | QA skill is 233 lines; actor recipes were compacted to 185 role-specific lines. |
| `duplicated_instruction_count` | pass | `qa` owns receipt semantics; actor reads it instead of repeating the full schema. |
| `prompt_size_tokens` | pass | QA skill remains below the approximate 250-line review threshold. |
| `task_success_rate` | pass | One fixture-backed run reached five TAS-A verdicts; every generated receipt also passed schema and artifact-honesty validation. |
| `review_tas_rate` | pass | Completion review reached TAS-A across all five required families. |
| `maintenance_locality` | pass | Guide, skill, actor, cookbook, validator, and eval ownership are named. |
| `composition_clarity` | pass | Inputs, state, outputs, gates, routes, evidence, and learning handoff are explicit. |

## Proof Artifacts

- Skill-local evals: five distinct QA cases backed by current-schema tickets
  and evidence under `skills/qa/evals/fixtures/`.
- Structure evals: query-spoiler scan and full skill-system check passed.
- Reviewer receipts: plan review TAS-A; completion review TAS-A with no
  blocking findings.
- Validators: twenty focused receipt, fixture-integrity, and eval-answer
  tests passed.
- Real harness: `.farplane/evals/runs/20260713-203845-task-0356-qa-final-reviewed/summary.json`
  records five TAS-A verdicts; `validate_eval_run.py` passed the same answers.
- Eval required: yes, because prompt-like behavior and routing changed.
- Evidence gaps: none for the claimed QA-contract behavior. Downstream app
  browser QA remains ticket-specific.

## Before Behavior

- Tester required retired ticket sections and universal screenshots.
- Result examples omitted fields required by the five-gate checklist.
- Evidence writeback targeted retired `Evidence`/`State` sections.
- Cookbook learning was recommended but not a required run decision.

## After Behavior

- Effective proof policy is `Done` + `QA Strategy` + optional `Agent Contract`
  + explicit tightening override.
- Evidence requirements branch by proof type and runtime ambiguity blocks.
- One validator enforces canonical receipt structure and conditional invariants.
- Every run selects ticket-only, cookbook-update, or instrumentation-ticket
  learning without forcing shared-doc churn.

## Followups

- Preserve the semantic no-answer-leak review and generated-receipt validator
  when future QA eval rows change.
