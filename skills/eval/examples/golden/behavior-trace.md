---
title: Golden Eval behavior trace
owner: skills/eval
status: active
kind: golden-example
updated_at: 2026-07-16
---

# Prove one agent workflow from visible evidence

## Input and context

- Request: prove that a fresh CLI agent follows one workflow checkpoint and
  creates its declared artifact.
- Source context: a natural eval task, observable reference points, optional
  output schema, and an equal-budget baseline profile.
- Branch: use this golden when tool events, file changes, or artifacts matter
  beyond the final prose answer.

## Accepted output

1. Write one natural task whose expected behavior lives in reference points,
   not leaked instructions.
2. Run Eval with `--behavior-trace --max-parallel-tasks 1`; add the standard
   schema only when structured child output is required.
3. Preserve exact prompt, raw JSONL events, stdout/stderr, final output,
   commands, usage, checkpoints, schema result when requested, and declared
   plus observed artifacts.
4. Use the same task and budget for candidate/baseline comparison and have a
   fresh reviewer inspect `summary.json`, `behavior_trace.json`, and QA.

## Why it passes QA

- Isolation -> one worker and ephemeral, hook-disabled CLI execution keep file
  deltas attributable.
- Evidence completeness -> raw events and artifact existence are preserved
  before summary or judgment.
- Honest schema behavior -> arbitrary nonempty JSON/text may be traced without
  a schema; explicit schemas are validated.
- Comparison fairness -> candidate and baseline use the same task and budget.

## Tempting negative

Accept the child's prose verdict without events or artifact existence checks,
or require every schema-less planner JSON to imitate a behavior-report object.

Why it fails: the first self-certifies behavior; the second confuses evidence
capture with one optional output contract and rejects valid traced workflows.

## Transferable invariants

- Score visible behavior only; never hidden reasoning.
- Preserve raw evidence before summarizing it.
- Keep candidate and baseline budgets equal.
- Route native-subagent-only capture to Agent QA; Eval behavior traces own
  stable CLI JSON events.

## Non-copyable facts and wording

- The named checkpoint, artifact, task, model/profile, schema choice, paths,
  and expected events are fixture-specific.
- Generate the task and evidence expectations from the current claim.

## Proof receipt

```yaml
golden_case: eval/behavior-trace
source_refs:
  - skills/eval/tests/test_run_evals.py
qa_refs:
  - skills/eval/qa_checklist.md
accepted_because:
  - visible_evidence_preserved
  - schema_is_optional
  - equal_budget_comparison
heldout_required: true
review_input: candidate + transferable_invariants + qa + heldout_context
review_excludes: planner_scratch_reasoning
```
