---
title: V1 typed charter, Reward, Pulse, and Dogfood contract cutover
status: accepted
owner: skill-maintenance
created_at: 2026-07-12
kind: skill-maintenance-audit
ticket_ref: tickets/TASK-0330/ticket.md
skills:
  - pulse-update
  - ticket-opportunity-generator
  - dogfood-review
  - harness-creator
  - goal-advisor
  - init-advisor
  - metric-advisor
---

# V1 contract cutover audit

## Behavior Delta

```text
before:
  Markdown charter paths, duplicated metric optimization state, score-shaped
  Reward completion, row-index check-ins, and interval-era setup language
after:
  typed harness.yaml selection, definition-owned metric semantics, stable
  Reward IDs and decisions, ticket-local check-ins, weekly Dogfood aggregation,
  one Pulse heartbeat, and Core-owned file-event mining
```

Operational rules stayed in their owner skills; project coordinates stayed in
`harness.yaml`, `metrics.yaml`, `bindings.yaml`, and `automations.toml`. No new
router, heartbeat, planner-score loop, compatibility reader, or scalar mining
score was added.

## Eval And QA Sync

- Pulse, Dogfood, Harness Creator, Goal Advisor, Ticket Opportunity Generator,
  and Init Advisor eval wording now tests the typed charter and stable Reward
  contract.
- Goal Packet templates use `reward_id`, `decision`, evaluation keys, evidence
  refs, and `accept | kill | monitor`.
- Project validators reject the retired Markdown charter, duplicated objective
  refs/priorities, selected metrics without definition-owned direction or
  freshness, and unselected hard-guard definitions.
- `check_skills.py --write` passed todo, registry, template, tier, surface
  budget, capability, eval-query, and doc-reference checks.

## First-Load Review

| Skill | Lines before | Lines after | Result |
| --- | ---: | ---: | --- |
| `pulse-update` | 284 | 285 | stable-ID check-in and typed context made explicit |
| `ticket-opportunity-generator` | 224 | 250 | accepted prior planner trajectory contract plus typed selection |
| `dogfood-review` | 190 | 202 | two-horizon portfolio boundary made explicit |
| `harness-creator` | 399 | 388 | stale interval/goal language removed despite new typed contract |
| `goal-advisor` | 462 | 463 | stable Reward IDs replace row-index/iterate semantics |
| `init-advisor` | 254 | 255 | typed bootstrap owner named |
| `metric-advisor` | 192 | 194 | selection owner split made explicit |

```yaml
first_load_review:
  kept_in_skill: normal-path state ownership, gates, routing, and proof
  moved_to_reference: none; conditional detail remained in existing references
  deleted_as_duplicate_or_rationale: stale goal, optimization, and interval-planning language
  extra_sections_kept_with_reason: existing sections preserve callable contracts and templates
  remaining_sections_over_budget: harness-creator and goal-advisor predate this change; both shrank or remained effectively flat
  proof_surface_fit: deterministic validators/tests plus behavior eval contracts
  task_case_quality: realistic empty-board, due-check-in, delayed experiment, and bootstrap cases
  anti_cheat_case_design: prompts do not disclose exact required answer strings beyond task state
  qa_preflight_loaded: pass
  qa_finish_independence: parent ticket requires independent completion review
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: stale ownership prose removed; no tutorial section added
  verdict: pass
```

## Residual Risk

The new contracts have deterministic and focused behavior proof, but scheduled
operation still needs observation after the next Pulse and Dogfood runs.
Farplane UI has unrelated baseline type errors outside the mining adapter
paths; the touched UI paths pass their focused checks.
