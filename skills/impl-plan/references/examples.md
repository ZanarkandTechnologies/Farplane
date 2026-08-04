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

## Change Plan

### Change 1: enforce uniqueness in the existing validator

```yaml
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
- contains one executable change unit without repeating global policy;
- does not manufacture advisor calls, architecture maps, or diagrams.

## Good: when a visual companion earns its cost

A cross-service migration with multiple before/after ownership views may link
`diagrams.md`. The ticket remains canonical; the companion adds no scope and
must pass `validate_visual_companion.py`.

## Bad

```md
We should improve the plan and maybe add some tests later. Create diagrams.md
because every implementation plan needs one.
```

Why bad:

- no observable delta, file ownership, operation, failure boundary, or proof;
- tentative language leaves the builder to invent the implementation;
- the diagram is ceremony rather than a clearer representation.
