---
skill: interval-update
date: 2026-08-20
change_type: behavior
owner: interval-update
status: pass
review_route: reviewer
before_ref: installed-skill-baseline
after_ref: working-tree
reasoning_basis: operator_direction
proof_artifacts:
  - .farplane/evals/runs/20260820T122550Z-weekly-draft-daily-candidate-v2/summary.json
  - .farplane/evals/runs/20260820T122705Z-weekly-draft-weekly-candidate/summary.json
  - .farplane/evals/runs/20260820T123930Z-weekly-draft-cadence-candidate/summary.json
eval_required: yes
---

# Weekly Draft And Promotion Lifecycle Audit

## Change

- Before: Daily could apply patch-sized skill, project-doc, and Wiki deltas;
  Weekly consolidated receipts for changes already made.
- After: Daily writes its immutable report, upserts source-fingerprinted
  candidates into one current weekly draft, and records zero canonical
  promotions. Weekly dispositions every candidate, freezes the report, promotes
  authorized records, receipts observed results, and opens the next draft.
- Why: current project context should accumulate without treating every daily
  observation as durable knowledge.
- Tradeoff accepted: durable knowledge may wait until the weekly review.

## Ownership

`farplane/harness.yaml` remains stable project identity. The ignored weekly
draft is current operating context, canonical tickets/skills/docs/Wiki own
promoted records, and finalized weekly reports preserve history. No new skill,
database, scheduler, hook, or mutable global ledger was added.

## Proof

| Case | Installed baseline | Candidate |
| --- | --- | --- |
| Daily stages three owner-routed candidates | fail, 0.65 | pass, 1.0 |
| Weekly dispositions and selectively promotes | fail, 0.675 | pass, 1.0 |
| Cadence keeps shared evidence quality but distinct authority | fail, 0.675 | pass, 1.0 |

All comparisons used the same GPT-5.6 Luna low-reasoning Promptfoo profile,
task, judge, sandbox, approvals, and network policy.

Independent reviewer verdict: `TAS-A`, pass, with no blocking findings or hard
gate failures after the superseded predecessor receipt was made explicit.
