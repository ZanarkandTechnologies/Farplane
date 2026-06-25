---
title: "Refactoring Workflow"
status: active
owner: refactoring
created_at: 2026-06-25
updated_at: 2026-06-25
tags:
  - refactoring
  - maintainability
refs:
  - skills/refactoring/SKILL.md
---

# Refactoring Workflow

Use this reference after `SKILL.md` selects a normal refactoring branch.

```text
refactor_loop(target, metric_profile, proof)
  -> behavior_lock + transformations + proof + smell_delta + residual_risk
```

## Loop

1. Define the behavior boundary.
   - public API, route, UI state, CLI output, data shape, or side effect
   - callers that must keep working
   - non-goals and intentionally untouched debt
2. Lock behavior.
   - use existing tests first
   - add characterization tests only around behavior being preserved
   - use snapshots or golden fixtures when tests are missing and behavior is
     stable enough to capture
3. Identify the smallest high-value target.
   - changed or high-churn files first
   - high complexity plus low coverage beats cosmetic style issues
   - duplication that has already caused or is likely to cause divergent fixes
4. Choose transformations.
   - extract pure logic from side effects
   - split mixed responsibilities by caller need, not by arbitrary line count
   - replace duplicated logic with one owner module
   - improve names only when they reduce ambiguity at call sites
   - tighten types or schemas when doing so makes behavior easier to prove
5. Change in small steps.
   - run the proof after risky moves
   - keep behavior changes out unless the caller explicitly expands scope
   - prefer local ownership over new global utility buckets
6. Verify.
   - behavior proof passes
   - selected smell metrics improve or the tradeoff is explained
   - no new boundary violations or hidden dependencies
7. Report.
   - before/after structure
   - exact checks
   - metric delta
   - residual risks and follow-ups

## Stop Conditions

- The behavior boundary cannot be proven.
- The requested cleanup would change public behavior without approval.
- The highest-scoring target belongs to a different owner or ticket.
- Metrics improve only by making code less readable or harder to test.
