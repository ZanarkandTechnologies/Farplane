---
skill: proposal-pricing
date: 2026-08-02
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: d21ba7bc505b6dce1f8ef41630ac23e7e42a74c7
after_ref: working-tree
reasoning_basis: reviewer
proof_artifacts:
  - .farplane/evals/runs/20260801-204749-proposal-pricing-transcript-matrix/summary.json
  - .farplane/evals/runs/20260801-213006-proposal-pricing-final-branches/summary.json
  - .farplane/evals/runs/20260801-213122-proposal-pricing-full-postfix/summary.json
  - .farplane/evals/runs/20260801-224511-proposal-pricing-body-only-regression/summary.json
eval_required: yes
---

# Proposal Pricing Transcript Sufficiency Matrix

## Change

- Before: complete anchors, one-missing-number calls, and missing outcomes had
  routes, but transcripts needing several numbers or containing conflicting
  evidence did not have a deterministic next action.
- After: the skill requires a proposed outcome, recognizes three complete
  annual-value anchors, asks one prioritized economic question per turn when
  value is incomplete, resolves explicit corrections, and asks one
  clarification when complete estimates remain in conflict.
- Why: real call transcripts vary in completeness and noise; the skill must
  make the same sufficiency decision without inventing inputs or returning a
  discovery questionnaire.
- Tradeoff accepted: one-question-per-turn can take more exchanges than a
  bundled intake, but each question is easier to answer and prevents broad,
  low-signal proposal discovery.

## First-Principles Reasoning

- Objective: produce a concise price-backed proposal only when one value anchor
  and the proposed customer outcome are defensible.
- Placement logic: first-load routing lives in `SKILL.md`; reusable prevention
  lives in `qa_checklist.md`; variable transcript behavior lives in evals.
- Expected behavior delta: all transcript shapes resolve to one of three
  outputs: a concise proposal, one next-best economic question, or a
  one-sentence `not_ready` result.
- Proof needed: deterministic checks plus held-out transcript cases covering
  every decision branch and independent review of the skill/eval contract.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Outcome gate, anchor completeness, question priority, conflict handling, and outputs are in `SKILL.md`. |
| `reference_load_precision` | pass | No new mandatory reference was introduced. |
| `missing_context_rate` | pass | Eleven cases cover sufficient, recoverable, conflicting, overlapping, noisy, and not-ready transcript states. |
| `noisy_context_rate` | pass | The normal path gained only the decision rules required at invocation time. |
| `duplicated_instruction_count` | pass | Runtime route is owned by `SKILL.md`; QA verifies rather than re-explains it. |
| `prompt_size_tokens` | pass | The delta is a compact decision branch rather than an external intake schema. |
| `task_success_rate` | pass | Consolidated run: 11/11 TAS-A. |
| `review_tas_rate` | pass | Independent final review returned TAS-A across skill contract, eval quality, evidence quality, and integration readiness. |
| `maintenance_locality` | pass | All behavior, prevention, and proof remain inside `skills/proposal-pricing/`. |
| `composition_clarity` | pass | Inputs and the three exclusive outputs are explicit. |

## Proof Artifacts

- Baseline/comparison run: `20260801-204749-proposal-pricing-transcript-matrix`
  returned 9/9 TAS-A, 100% skill triggering, three candidate wins and six ties.
- Focused final branches: `20260801-213006-proposal-pricing-final-branches`
  returned 2/2 TAS-A.
- Consolidated post-fix suite: `20260801-213122-proposal-pricing-full-postfix`
  returned 11/11 TAS-A.
- Body-only regression: `20260801-224511-proposal-pricing-body-only-regression`
  returned TAS-A and the proposal had no chat-status preamble or `Grounding:`
  footer.
- Deterministic checks: calculator tests 4/4; JSON parsing passed; eval-query
  lint passed; `git diff --check` passed; capability fixtures passed.
- Registry validation: registry, templates, todo tiers, and Tier 0 checks
  passed. The aggregate skill check remains nonzero only because of unrelated
  pre-existing `content-impl-plan` QA/eval surface-budget violations.
- Reviewer receipt: TAS-A, no hard gates or blockers. The reviewer identified
  chat-status and `Grounding:` wrappers as low-risk proposal slop; the output
  contract, QA checklist, and happy-path regression assertion now reject them.

## Before Behavior

- Outcome plus a complete anchor produced a proposal.
- An anchor missing exactly one number produced one question.
- No outcome produced `not_ready`.
- Two-or-more missing numbers and conflicting complete estimates were
  underspecified.

## After Behavior

- No outcome always produces one-sentence `not_ready`, even when value exists.
- Any complete non-overlapping anchor produces one concise proposal.
- Incomplete evidence produces one next-best question per turn, starting with
  the nearest partial anchor or typical monthly/annual cost.
- Later explicit corrections or authoritative estimates supersede earlier
  numbers; unresolved conflicts produce one clarification and no price.

## Followups

- None required for the covered decision matrix. Real customer transcripts
  should remain private and can be converted into sanitized regression cases
  only when they reveal a distinct failure mode.
