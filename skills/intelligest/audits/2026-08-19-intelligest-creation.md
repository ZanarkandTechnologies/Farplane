---
skill: intelligest
date: 2026-08-19
change_type: behavior
owner: skill-creator
status: pass
review_route: self_check
before_ref: apps/youtube-shortcut:summarize-direct
after_ref: skills/intelligest/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/intelligest/evals/evals.json
  - apps/youtube-shortcut/scripts/local-agent.test.ts
  - .farplane/evals/runs/20260819-065944-20260819-intelligest-v1/summary.json
  - .farplane/evals/runs/20260819-070300-20260819-intelligest-media-repair/summary.json
  - skills/intelligest/audits/2026-08-19-intelligest-review.md
eval_required: yes
---

# Intelligest Creation Audit

## Change

- Before: the YouTube caller invoked `summarize` directly and embedded Content
  Intelligence product judgment in one app prompt; broad Topic overlap could
  appear as Related coverage.
- After: `intelligest` owns one durable Intelligence Receipt and calls narrow
  extraction, grounding, Wiki, and Resource Bank specialists conditionally.
- Why: give the operator one memorable verb while keeping persistence and
  specialist ownership explicit.
- Tradeoff accepted: true related coverage returns empty when no recent-catalog
  search adapter or comparable source evidence is available.

## First-Principles Reasoning

- Objective: make every source produce visible intelligence state without
  silently saving inspiration or confusing topic similarity with comparable
  reporting.
- Placement logic: the repeated judgment belongs in a Tier 3 skill; canonical
  job writes remain in Content Intelligence, source extraction remains in
  `summarize`/`media-ingest`, Wiki writes remain in `manage-wiki`, and Resource
  Bank writes remain in `ingest-content`.
- Expected behavior delta: callers invoke one verb, dedupe before analysis,
  compare only recent evidence-backed takes, and expose every optional branch.
- Proof needed: skill structure/registry checks, eval-query lint, focused
  shortcut tests, installer retirement proof, and contract review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, comparison rule, branch gates, five domain steps, and output are present in 178 lines. |
| `reference_load_precision` | pass | Only the quality-dependent related-coverage calibration loads a golden example. |
| `missing_context_rate` | pass | Canonical intake, extraction, comparison, News, Wiki, Resource Bank, progress, and blocker paths are explicit. |
| `noisy_context_rate` | pass | Provider mechanics and product schema internals remain with their existing owners. |
| `duplicated_instruction_count` | pass | Intelligest owns judgment; linked skills retain extraction and write ownership. |
| `prompt_size_tokens` | pass | `SKILL.md` remains below the 200-line envelope. |
| `task_success_rate` | pass | Four cases earned A initially; the only B was hardened and its focused rerun earned A, covering all five cases. |
| `review_tas_rate` | pass | The scoped self-review returned TAS-A for all four required families. |
| `maintenance_locality` | pass | One new skill, one existing caller, one installer retirement set, and generated registry sync. |
| `composition_clarity` | pass | The receipt owner and each conditional child write are explicit. |

## Proof Artifacts

- Skill-local evals: initial run passed four of five at A; the media blocker was
  hardened and its focused rerun passed A.
- Structure evals, when needed: skill-system validator and registry sync.
- Reviewer receipt: `2026-08-19-intelligest-review.md` (`TAS-A`, scoped
  self-check).
- Validator: `check_skills.py --write`, eval-query lint, installer unit tests,
  31 YouTube tests, and shortcut type-check pass.
- Eval required: yes.
- Evidence gaps: no live production video was re-analyzed in this change; the
  current Topics transport is a narrow comparison-key adapter rather than a
  dedicated source-ID similarity relation.

## Before Behavior

- Direct `summarize` invocation mixed extraction with app-specific intelligence
  policy and let broad recurring Topics drive Related coverage.

## After Behavior

- `intelligest` owns the complete analysis receipt and fails closed when recent
  comparable-source evidence is unavailable.

## Followups

- None until real invocation evidence reveals a narrower repair.
