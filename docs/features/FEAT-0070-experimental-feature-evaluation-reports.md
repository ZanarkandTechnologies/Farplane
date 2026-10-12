---
title: Retired Dogfood self-improvement portfolio checkpoints
status: retired
owner: feature-registry
created_at: 2026-07-07
updated_at: 2026-10-12
tags: [farplane, feature, sys-0007, retired]
feature_id: FEAT-0070
system_id: SYS-0007
category: improvement-loop
public: true
surfaces:
  - docs/features/FEAT-0070-experimental-feature-evaluation-reports.md
source_refs:
  - docs/systems/self-improvement-learning.md
  - farplane/harness.yaml
  - docs/prd.md
external_refs: []
evidence_refs: []
known_limits: "Retired in #41 when the `dogfood-review` skill was deleted. Self-improvement campaigns keep their evidence in their own GitHub-issue Goal Packets; no portfolio checkpoint skill remains."
metrics:
  - experimental_feature_decision_quality
  - experiment_ticket_quality
last_verified: 2026-10-12
experimental: false
superseded_by: false
track: false
---

# Retired Dogfood self-improvement portfolio checkpoints

Dogfood portfolio checkpoints are retired. The feature was retired in #41 when
its `dogfood-review` skill was deleted. Self-improvement campaigns keep their
evidence in their own GitHub-issue Goal Packets; see
[Self-Improvement And Learning](../systems/self-improvement-learning.md).

## Historical Behavior

The retired feature was SYS-0007's weekly reducer. It:

- reconstructed the complete `self_improvement` ticket history through a
  cutoff from exact admission receipts and still-live earlier packets;
- read ticket `program.md`, `progress.md`, Reward rows, check-ins, and
  review/QA evidence, treating missing receipts as source gaps;
- wrote one dated portfolio checkpoint with an outcome ledger, portfolio
  lessons, and opportunity signals; and
- passed only that report as bounded planner context. It never created tickets,
  executed work, or decided Reward.

## Change History

- 2026-07-07: Created experimental feature-evaluation reporting.
- 2026-07-13: Added target-five reserved allocation.
- 2026-07-16: Removed declared-experiment and target-five planning; Dogfood now
  checkpoints all exact-area ticket evidence for normal planner context.
- 2026-10-12: Retired in #41 when `dogfood-review` was deleted.
