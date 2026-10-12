# Proof Cases

Load this when the proof surface or the cases are not settled yet: a behavior
claim needs cases before rows are written, or a suite needs pruning. Folded
from `proof-advisor` (#41).

```text
proof_cases(claim, sources) -> case_matrix + selected_cases + proof_surface_map + gaps
```

## Sources first

1. Mine real regressions, user corrections, traces, logs, tickets, and existing
   tests before inventing anything.
2. Use synthetic cases only to fill a named coverage gap, never to replace
   failure analysis. Say which real source would strengthen the suite.

## Dimensions, then small batches

- Name the dimensions that make cases distinct first: caller intent, scenario,
  input shape, fixture state, boundary, tool/state transition, oracle, proof
  surface. A request for "30 ideas" gets dimensions plus a starter batch.
- Generate 3-7 candidates per batch, then select fewer high-signal ones.
- For prompt-like or skill-like behavior, each batch holds one ordinary success,
  one known or likely failure, one boundary, and one anti-cheat control: a case
  that passes only if the skill does the work, not if the query leaks it.

## Select

Reject a candidate when it is a near-duplicate (same failure, same owner), a
vague goodness check, needs a hidden oracle, needs an impossible or live-risky
fixture, or would fail without naming which owner to fix. Prefer one case with
a strong oracle over five with blurry criteria.

## Choose the proof surface per case

| Behavior | Surface |
| --- | --- |
| Parseable, schema, fixture diff, file state | Unit, contract, or validator check; never an LLM judge |
| Variable output with explicit criteria | Eval row with assertions or a judge |
| Tool use, multi-turn state, artifacts | `behavior_trace` or [qa adversarial mode](../../qa/SKILL.md) |
| Running app or user-visible UI | [qa](../../qa/SKILL.md), then [qa visual mode](../../qa/SKILL.md) |
| Unclear metric or reward signal | [goal-advisor metric card](../../goal-advisor/references/metrics.md) first |

When an agent cannot reach or assert the behavior, plan the test hook in
[impl-plan's agent testability reference](../../impl-plan/references/agent-testability.md).

## Case row

```text
case_id; source: real_failure | trace | ticket | spec | existing_test | synthetic_gap
input; fixture_state; expected_oracle; failure_signal
proof_surface; evidence_required; owner_if_fails
```
