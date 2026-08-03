---
title: Dogfood self-improvement portfolio checkpoints
status: implemented
owner: feature-registry
created_at: 2026-07-07
updated_at: 2026-07-16
tags: [farplane, feature, sys-0007]
feature_id: FEAT-0070
system_id: SYS-0007
category: improvement-loop
public: true
surfaces:
  - farplane/harness.yaml
  - skills/dogfood-review/SKILL.md
  - skills/dogfood-review/templates/dogfood-report.md
  - farplane/automations.toml
source_refs:
  - docs/systems/self-improvement-learning.md
  - farplane/harness.yaml
  - docs/prd.md
external_refs: []
evidence_refs:
  - skills/dogfood-review/evals/evals.json
  - tickets/archive/TASK-0384/ticket.md
known_limits: "Normal weekly materialization remains disabled until TASK-0384's frozen bootstrap eval, real shadow path, and independent TAS-A completion review pass."
metrics:
  - experimental_feature_decision_quality
  - experiment_ticket_quality
last_verified: 2026-07-16
experimental: true
superseded_by: false
track: >-
  Review the latest Dogfood checkpoint, exact admission-query receipts, every
  live self-improvement packet, Reward/check-in evidence, portfolio lessons,
  source gaps, and planner-context receipt. Judge completeness, attribution,
  state ownership, leanness, and proof that Dogfood performed no planning,
  ticket creation, materialization, execution, or check-in. Return continue,
  adjust, pause, graduate, rollback, or source_gap.
---

# Dogfood self-improvement portfolio checkpoints

Dogfood is SYS-0007's weekly reducer. It reconstructs the complete
`self_improvement` ticket history through a cutoff and writes a dated portfolio
checkpoint for the one normal next-wave planner.

```text
dogfood_review(cutoff, exact_area_receipts, live_earlier_packets,
               previous_checkpoint?, metrics?, evidence?)
  -> dated_checkpoint + outcome_ledger + portfolio_lessons
   + opportunity_signals + planner_context_ref + source_gaps
```

## Contract

- Page through every exact `self_improvement` admission receipt through the
  cutoff and include every still-live earlier packet.
- Read ticket `program.md`, `progress.md`, Reward rows, check-ins, artifacts,
  and review/QA evidence. Ticket packets remain canonical.
- Treat ambiguous area derivation, missing receipts, and unavailable outcome
  providers as source gaps rather than inferred membership or zero.
- Count revenue, reach, or subscription movement only from external ultimate-
  metric evidence; local enabler/guard completion remains leading/protective.
- Keep portfolio-selection lessons in the checkpoint and target-specific
  optimization policy/evidence in the owning ticket Goal Packet, joined by
  stable refs. Target-local self-improve files are legacy notes, not live state.
- Record every qualified, deprioritized, duplicate, conflicting, source-gap,
  and unticketable opportunity signal without a target count.
- Pass only the dated report as bounded `current_context`. Plan Next Wave owns
  generation, cross-horizon ranking, and capacity-derived `0..wave_size`
  admission. Pulse alone materializes and executes.

## Non-Goals

Dogfood does not create specs or tickets, reserve an area wave, execute work,
dispatch workers, perform check-ins, decide Reward, or mutate skills or policy.

## Proof

- Natural evals cover uncapped exhausted history retrieval, ambiguous membership, ultimate-
  outcome attribution, quota-free context handoff, and due check-ins.
- Every report includes reconstruction plus no-action receipts.
- `python3 docs/features/validate_features.py`
- `python3 bin/validators/check_doc_refs.py`

## Change History

- 2026-07-07: Created experimental feature-evaluation reporting.
- 2026-07-13: Added target-five reserved allocation.
- 2026-07-16: Removed declared-experiment and target-five planning; Dogfood now
  checkpoints all exact-area ticket evidence for normal planner context.
