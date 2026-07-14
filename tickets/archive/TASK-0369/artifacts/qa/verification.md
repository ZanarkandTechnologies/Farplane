---
title: TASK-0369 verification
status: complete
ticket_id: TASK-0369
updated_at: 2026-07-14
---

# Verification

## Critical Path

```text
harness area ICP
  -> Feed Scout update-in-place memory
  -> memory validation
  -> Pulse semantic planning input
  -> Plan Next Wave audience_context gate
  -> ticket execution inputs
  -> Farplane artifact skill retrieval
```

## Checks

- `python3 -m unittest skills/feed-scout/scripts/test_validate_memory.py skills/plan-next-wave/scripts/test_validate_ticket_specs.py skills/plan-next-wave/scripts/test_eval_fixtures.py bin/tests/test_farplane_project_file_validator.py`
  - Result: pass, 45 tests, including hostile extra-timeline, per-entry
    provenance, configured-ICP completeness, canonical-field drift, and
    delayed-check-in cases, plus full Feed Scout contract validation for the
    planner's clean-room memory fixture.
- `python3 skills/feed-scout/scripts/validate_memory.py .farplane/feed-scout/memory.md --harness farplane/harness.yaml`
  - Result: pass for the seeded live memory.
- `python3 skills/feed-scout/scripts/validate_memory.py skills/feed-scout/templates/memory.md --allow-template-placeholders`
  - Result: pass for the shipped template.
- `python3 skills/feed-scout/scripts/validate_memory.py skills/plan-next-wave/evals/fixtures/icp-world-memory.md --harness farplane/harness.yaml`
  - Result: pass; the planner hardcase now stages a complete valid Feed Scout
    memory rather than a partial or placeholder artifact.
- `python3 bin/validators/check_farplane_project_files.py --root .`
  - Result: pass after regenerating `.farplane/project/ui/latest.json`.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - Result: skill todo, registry, templates, tiers, surface budgets,
    capabilities, eval-query lint, doc refs, and Python compile checks pass.
- Live install:
  - `feed-scout`, `plan-next-wave`, and `pulse-update` installed successfully.
  - Live `farplane-ticket-update` and `farplane-feed-scout` automations updated
    in place and read back with the memory/ICP contract present.

## Behavioral Evals

- Feed Scout memory update hardcase:
  - Initial run: B; it updated/validated memory correctly but did not explicitly
    reject incomplete candidate handoff.
  - Repair: added a hard candidate audience-context gate and QA check.
  - Retest: A, 1/1 pass.
  - Evidence: `.farplane/evals/runs/20260714-115544-task-0369-feed-retest/summary.json`.
- Pulse memory materialization case:
  - Result: A, all five reference points passed.
  - Evidence: `.farplane/evals/runs/20260714-115439-task-0369-world-memory/tasks/pulse_passes_icp_world_memory_into_ticket_context.json`.
- Plan Next Wave shallow-vs-grounded case:
  - First trace returned A but its admitted spec failed deterministic replay
    because a delayed signal omitted `check_in_at`; this was not accepted as
    completion proof.
  - Repair: tightened planner semantics and validator coverage, then replaced
    the blank memory template in the hardcase with a populated clean-room
    current-memory fixture.
  - Intermediate retest returned B because it cited caller context rather than
    a concrete memory entry and did not evidence the validator receipt.
  - A subsequent review rejected that proof because the repaired query taught
    the validator/check-in answer and the fixture was only a partial memory.
    The query was restored to natural operator facts, the full four-ICP fixture
    was made contract-valid, and the validation receipt was added to the real
    planner return contract instead of the user query.
  - Final unspoiled retest: A, 1/1 pass, with concrete memory refs, a valid
    delayed check-in, publication outside unattended execution, and an explicit
    deterministic validation receipt.
  - Independent post-eval replay extracted the admitted spec and ran the real
    validator against `farplane/harness.yaml` and `farplane/metrics.yaml`:
    `ok: true`, zero errors.
  - Evidence: `.farplane/evals/runs/20260714-121825-task-0369-planner-unspoiled-final/summary.json`
    and `tickets/archive/TASK-0369/artifacts/qa/planner-eval-spec-validation.json`.

## Eval Query Review

```text
eval_query_review:
  changed_files:
    - skills/feed-scout/evals/evals.json
    - skills/plan-next-wave/evals/evals.json
    - skills/pulse-update/evals/evals.json
  reviewed_rows:
    - feed_scout_updates_persistent_icp_world_memory
    - planner_rejects_shallow_icp_trend_repetition
    - pulse_passes_icp_world_memory_into_ticket_context
  reviewer: self + final independent reviewer lane
  query_spoiler_verdict: pass
  fixes_applied: strengthened Feed Scout runtime gate; added a full contract-valid clean-room memory fixture and regression test; aligned planner signal semantics and return receipt with deterministic validation; removed repair instructions from the natural query
  deferrals: none for the changed behavior
  remaining_risk: observe a real later Pulse wave and its eventual Reward outcome
```

## Residual Risk

The implementation proves structure, provenance enforcement, handoff,
materialization, and all three focused agent behaviors. It does not yet prove
that later real Pulse waves earn better human
Reward outcomes; FEAT-0072 tracking and the next scheduled runs own that signal.
