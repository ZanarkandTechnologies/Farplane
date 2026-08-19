---
skill: manage-wiki
date: 2026-08-19
change_type: behavior
owner: skill-creator
status: pass
review_route: reviewer
before_ref: retired-skill:ingest-world-data
after_ref: skills/manage-wiki/SKILL.md
reasoning_basis: reviewer
proof_artifacts:
  - tickets/TASK-0438/ticket.md
  - .farplane/evals/runs/20260819-055030-task0438-manage-wiki-final/summary.json
  - .farplane/evals/runs/20260819-055525-task0438-manage-wiki-source-gap/summary.json
  - .farplane/evals/runs/20260819-055905-task0438-retired-ingest-baseline-valid/summary.json
eval_required: yes
---

# Manage Wiki Migration Audit

## Change

- Before: a transcript-oriented ingestion skill searched a lean JSON catalogue
  in prose and rebuilt every projection after direct Markdown edits.
- After: one general Wiki skill stages page deltas, resolves mentions through
  exact plus candidate search, blocks ambiguity, then page-syncs projections.
- Why: make every research/ingestion caller use one safe Wiki mutation owner.
- Tradeoff accepted: generated SQLite adds local state but remains disposable;
  Markdown stays canonical and cross-project identity remains out of scope.

## First-Principles Reasoning

- Objective: preserve Wiki-quality narrative while generating reliable entity
  links and page-owned graph claims.
- Placement logic: judgment belongs in `manage-wiki`; deterministic search,
  validation, cache replacement, and exports belong in Core.
- Expected behavior delta: staged resolution outcomes replace ad hoc lookup and
  full-rebuild writeback; no compatibility skill alias survives.
- Proof needed: skill validation, four behavior evals, caller sweep, Wiki Core
  tests, and independent completion review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, five domain steps, gates, commands, and receipt are visible. |
| `reference_load_precision` | pass | Storage/notation are every-run; mixed example has a precise condition. |
| `missing_context_rate` | pass | Source, scope, staging, resolution, publish, sync, and failure paths are explicit. |
| `noisy_context_rate` | pass | Extended mixed scenario is outside first load. |
| `duplicated_instruction_count` | pass | Skill owns judgment; Core/docs own deterministic behavior and notation. |
| `prompt_size_tokens` | pass | `SKILL.md` is within the 200-line envelope. |
| `task_success_rate` | pass | Final full run passed link/create/ambiguity at A; the source-gap repair rerun passed A. Retired baseline passed 2/4. |
| `review_tas_rate` | pass | TASK-0438 completion review returned TAS-A with no blockers. |
| `maintenance_locality` | pass | One Wiki mutation owner replaces direct caller writeback. |
| `composition_clarity` | pass | Reads, writes, outcomes, gates, routes, failures, and output are explicit. |

## Proof Artifacts

- Skill-local evals: `evals/evals.json` covers link, create, ambiguity, and
  source-gap behavior.
- Structure evals: todo tiers, surface budget, Tier 0, checklist sync, JSON, and
  eval-query validation pass.
- Behavior baseline: `20260819-055905-task0438-retired-ingest-baseline-valid`
  passed 2/4 cases; it missed applicable replacement diffs, bounded page sync,
  and candidate-by-candidate ambiguity evidence.
- Candidate proof: `20260819-055030-task0438-manage-wiki-final` passed
  link/create/ambiguity at A. The only miss was an omitted explicit
  `skip_source_gap`; hardening then passed
  `20260819-055525-task0438-manage-wiki-source-gap` at A.
- Reviewer receipt:
  `tickets/TASK-0438/artifacts/review/completion-review.md` (`TAS-A`).
- Validator: integrated registry, surface-budget, capability, query-lint, and
  doc-reference checks pass.
- Eval required: yes; baseline and candidate evidence are complete.
- Evidence gaps: none.

## Before Behavior

- Callers directly edited entity Markdown and invoked the legacy full compiler.

## After Behavior

- Callers hand sourced deltas to `manage-wiki`, which publishes only a fully
  resolved, validated changeset and returns page-scoped projection evidence.

## Followups

- `no_self_improve_reason`: four focused cases are sufficient for launch;
  create an optimization loop only after real resolution failures accumulate.
