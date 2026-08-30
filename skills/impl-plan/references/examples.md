# Impl Plan Examples

## Good: localized backend change

````md
## Summary

Reject duplicate skill names through the existing registry validator and keep
all other behavior unchanged.

## Scope

- In: `src/validators/skill_registry.py`, focused validator tests.
- Out: new services, configuration, UI, unrelated cleanup.
- Constraints: preserve the current public function and error behavior except
  for the new duplicate-name case.

## Delta

> **Before:** duplicate names pass validation.
>
> **After:** the second occurrence raises the specified `ValueError`.
>
> **Example:** `[{name: "a"}, {name: "a"}]` raises
> `duplicate skill name: a`.

## Contract Diagram

```text
[S1] rows -> [S2] validate_rows -> [S3] valid rows
                  |
                  +-> [F1] repeated name -> ValueError
[F1] -> [P1] exact duplicate-name message
```

## Change Plan

### Change 1: enforce uniqueness in the existing validator

#### Implementation Preview

> **Current owner:** `src/validators/skill_registry.py:12` —
> `for row in rows: validate_row(row)` *(fictional fixture excerpt)*
>
> **Planned owner:** `src/validators/skill_registry.py` —
> `seen = set(); ...; if name in seen: raise ValueError(...)` *(illustrative)*
>
> **Expected example:** `[{name: "a"}, {name: "a"}]` ->
> `ValueError("duplicate skill name: a")`.

```yaml
diagram_nodes: [S2, F1, P1]
files:
  read:
    - src/validators/skill_registry.py
    - tests/test_skill_registry.py
  edit:
    - src/validators/skill_registry.py
    - tests/test_skill_registry.py
operation: Track names inside validate_rows and raise the required ValueError on the second occurrence; add focused duplicate and regression cases.
proof: python3 -m unittest tests.test_skill_registry
failure: Existing non-duplicate fixtures or public errors change.
```

## Done

- [ ] Duplicate names raise the exact required error.
- [ ] Existing validator tests still pass.

## QA Strategy

```yaml
proof_weight: mechanical
checks:
  - python3 -m unittest tests.test_skill_registry
delegated_lanes: []
evidence_paths: []
final_checkpoint: inline
residual_risk: none
```

## State

- Current: planned
- Next: human approval, then goal-advisor handoff
- Blockers: none
````

Why good:

- uses the canonical ticket shape instead of a skill-local template;
- reuses existing ownership and proof surfaces;
- distinguishes the feature-level Delta from the owner-level implementation
  transformation;
- contains one executable change unit without repeating global policy;
- uses the smallest required Contract Diagram without manufacturing advisors
  or a detailed visual companion.

## Good: when a visual companion earns its cost

A cross-service migration with multiple before/after ownership views may link
`diagrams.md`. The ticket remains canonical; the companion adds no scope and
must pass `validate_visual_companion.py`.

## Good: copy-complete UI baseline

```text
[DS3 — Evidence]
Reader question: Why should I believe this outcome?
Headline: Cut weekly account research from 6 hours to 45 minutes.
Proof: Four-week operated comparison; the chart caption says what changed.
Takeaway: The buyer can evaluate the time-saving claim without technical help.
Action: Review the comparison.
Assertion: Every visible string above appears verbatim in the capture.
```

Why good: the builder does not invent business copy, and QA can compare the
actual section with an observable baseline rather than a vague page label.

## Bad

```md
We should improve the plan and maybe add some tests later. Create diagrams.md
because every implementation plan needs one.
```

Why bad:

- no observable delta, file ownership, operation, failure boundary, or proof;
- tentative language leaves the builder to invent the implementation;
- the diagram is ceremony rather than a clearer representation.
