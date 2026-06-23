---
title: Task Case Design QA Checklist
owner: skills/task-case-design
status: active
kind: qa-checklist
updated_at: 2026-06-23
---

# Task Case Design QA Checklist

Use this checklist after creating or materially revising task cases for tests,
evals, QA, or agent behavior proof.

```text
task_case_qa(case_matrix, selected_cases, target_behavior)
  -> pass | revise | fail + fixes + remaining_risk
```

## Checks

1. `behavior_named`
   - Pass: every selected case maps to a specific behavior and failure risk.
   - Fail: cases test vague quality, taste, or "overall skill behavior."

2. `source_traceable`
   - Pass: each case names a source such as failure, trace, ticket, spec,
     existing test, or synthetic gap.
   - Fail: cases exist only because a large number was requested.

3. `dimension_coverage`
   - Pass: selected cases cover distinct dimensions such as ordinary path,
     failure mode, boundary, persona/caller, fixture state, or anti-cheat.
   - Fail: the suite is mostly happy-path variants.

4. `proof_surface_fit`
   - Pass: deterministic behavior uses mechanical checks when possible, and
     variable behavior has explicit judge criteria.
   - Fail: parseable outputs are judged by an LLM, or subjective behavior is
     forced into brittle exact-match assertions.

5. `oracle_visible`
   - Pass: each case has visible success criteria, failure signal, evidence,
     and owner-if-fails.
   - Fail: a maintainer cannot tell why the case passed or what to fix.

6. `query_not_spoiled`
   - Pass: eval or agent-task inputs sound natural and do not reveal the
     expected answer, skill name, checklist, or reference points.
   - Fail: the case teaches the behavior it is supposed to test.

7. `fixture_safe`
   - Pass: fixture state is available, inspect-only or sandboxed, and stable
     enough to rerun.
   - Fail: the case needs live secrets, deploys, pushes, private user paths, or
     unsandboxed mutation without explicit runner ownership.

8. `diagnostic_value`
   - Pass: a failure routes to a likely owner such as skill contract, fixture,
     prompt, judge, validator, UI, backend, or docs.
   - Fail: failure only indicates generic badness.

9. `batch_size_disciplined`
   - Pass: first batches are small and high signal; extra cases are justified
     by distinct failures or boundaries.
   - Fail: the suite optimizes for count rather than learning.

10. `maintenance_loop`
    - Pass: the artifact names how future real failures will be added, noisy
      cases retired, and judge criteria calibrated.
    - Fail: the suite is treated as one-and-done.

## Common Fixes

- Replace a vague case with a concrete behavior and failure signal.
- Merge near-duplicates and keep the case with better source quality.
- Move expected behavior from eval query text into reference points, fixture
  context, or judge criteria.
- Downgrade an LLM-judge case to a deterministic assertion when possible.
- Add one negative control to catch answer leakage or overfitting.

## Finish Note

```text
task_case_qa:
  changed_files:
  reviewed_cases:
  verdict: pass | revise | fail | unknown
  fixes_applied:
  deferrals:
  remaining_risk:
```
