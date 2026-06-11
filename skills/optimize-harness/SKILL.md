---
name: optimize-harness
description: "Turn observed Farplane behavior gaps into placement decisions, proof or eval, accepted changes, and review."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0053
allowed-tools: Read, Glob, Grep, Bash
---

# Optimize Harness

## Context

Use this when the operator says Farplane should behave differently and wants
the harness changed, not just explained. This is the high-level entrypoint for
"fix this behavior" requests: diagnose the gap, choose the owning surface,
create proof, route the change, and review the result.

This skill orchestrates existing surfaces. It should not absorb their jobs:
`gap-analysis` diagnoses, `harness-advisor` places the fix, `eval` creates or
runs proof including hardcase-marked cases, `self-improve` runs metric-driven
experiments, `skill-maintenance` applies skill-system migrations, and `review`
judges readiness.

## Skill Signature

```text
optimize_harness(observed_behavior, expected_behavior?, metric?, evidence?) -> accepted_change | experiment_plan | blocked_report
state: reads(gap reports, harness doctrine, registries, evals, target surfaces); writes(ticket?, eval_case?, experiment_artifact?, applied_change?, review_receipt?)
gates: gap_named; owner_surface_named; proof_exists; review_passes_or_blocked
routes: gap-analysis | harness-advisor | eval | self-improve | skill-maintenance | impl | review
fails: changes without proof; optimizes vague taste; creates new skill before checking registry; hides blocked state
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Normalize the request into observed behavior, expected behavior,
  candidate metric when present, and evidence already available.
- [ ] 2. Diagnose the gap with [gap-analysis](../gap-analysis/SKILL.md).
  - [ ] If the gap is already obvious and well grounded, state it explicitly
    and keep moving.
  - [ ] If expected behavior is underspecified, mark the uncertainty instead of
    inventing a target.
- [ ] 3. Place the fix with [harness-advisor](../harness-advisor/SKILL.md).
  - [ ] Name one primary owner surface.
  - [ ] Name rejected surfaces and why they should not own this change now.
- [ ] 4. Design proof with [eval](../eval/SKILL.md) or the appropriate QA path.
  - [ ] Create or update an eval case when the expected behavior is durable.
  - [ ] Mark the case as `hardcase` only when it is unusually difficult,
    reusable, benchmark-worthy, or saleable after sanitization.
- [ ] 5. Choose direct change versus experiment.
  - [ ] 1. Use direct implementation when the owner and proof are clear.
  - [ ] 2. Use [self-improve](../self-improve/SKILL.md) when a target skill or
    harness surface needs metric-driven candidate search.
  - [ ] 3. Use [skill-maintenance](../skill-maintenance/SKILL.md) for
    skill-template, registry, bulk rollout, or skill-contract migrations.
- [ ] 6. Apply the accepted change through the owning implementation workflow
  and keep evidence in the active ticket or proof artifact.
- [ ] 7. Use the native execution phase for final proof, writeback, and
  review routing before claiming the harness behavior is improved.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Workflow spine:

```text
observe -> expected -> gap_report -> placement_decision -> eval_or_proof -> change_or_experiment -> review
```

Minimal handoff:

```text
Observed:
Expected:
Gap:
Primary owner:
Proof:
Route:
Review gate:
```

## Gotchas

- Do not skip diagnosis just because the operator used a confident phrase like
  "obviously." Name the concrete gap before changing the harness.
- Do not use `self-improve` for ordinary implementation. Use it only when there
  is a metric, target surface, search space, baseline, and candidate comparison.
- Do not keep hard cases in a separate capture backlog. Hardcase is eval
  metadata for a runnable proof case.
- Do not add a new skill before checking the generated skill registry for an
  existing owner or consolidation target.
- Do not let this skill become a hidden autonomous loop. Visible artifacts,
  tickets, evals, and review receipts carry state.

## Reference Map

- [gap-analysis](../gap-analysis/SKILL.md) - diagnose current versus expected
  behavior and name the next owner.
- [harness-advisor](../harness-advisor/SKILL.md) - choose the primary harness
  placement surface.
- [eval](../eval/SKILL.md) - create, tag, and run proof cases including
  hardcase mode.
- [self-improve](../self-improve/SKILL.md) - run metric-driven experiments for
  skill or harness-surface optimization.
- [skill-maintenance](../skill-maintenance/SKILL.md) - apply skill-system
  template, registry, contract, and bulk maintenance changes.
- [review](../review/SKILL.md) - judge plans, skill changes, evals, proof, and
  completion claims.
- the native execution phase - final proof, writeback, and review routing
  for applied changes.
- [docs/specs/harness-engineering-doctrine.md](../../docs/specs/harness-engineering-doctrine.md) -
  Farplane placement doctrine.
- [docs/specs/self-improvement-contracts.md](../../docs/specs/self-improvement-contracts.md) -
  compact signatures and target self-improvement workflow.

## Output

Return or write:

- `Observed`
- `Expected`
- `Gap report`
- `Placement decision`
- `Proof or eval case`
- `Direct change or experiment route`
- `Review result`
- `Next concrete action`
