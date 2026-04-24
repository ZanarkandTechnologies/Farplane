# Impl Plan Template

## Summary
2-3 sentences on what changes and why it matters now.

## Scope

- In:
- Out:

## Plan

- `Change:`
- `Why:`
- `Before -> After:`
- `Touch:`
- `Inspect:`
- `Signature delta:`
  - `Format:` `module / symbol(input): output`
  - `Use:` 3-7 seams that prove codebase understanding
- `Type Sketch:`
  - `Format:` `TypeName { field: Type }` or `type Name = { field: Type }`
  - `Use:` only the fields that matter to the plan
  - `Avoid:` full dumps
- `Typed flow example:`
  - one golden-path dry run using the named types
- `Recommendation:`
- `Options considered:`
  - only when a material choice exists
- `Blast radius:`
- `Risks:`

## Gap Analysis

- `Required:` for missing, partial, parity-driven, or product-shaping feature
  work. Optional for tightly scoped bug fixes, internal refactors, or obvious
  one-surface changes.
- `Current state:`
- `Production expectation:`
- `Missing gaps:`
- `Comparable implementations:`
- `Recommendation:`

## Diagram

- `Required:` when material or cross-module work needs a diagram because the
  file map alone is not enough; optional for trivial localized fixes
- `Legend:` keep | change | add | remove

```mermaid
flowchart LR
  %% Keep this compact. Prefer one top-level delta map when it adds clarity.
```

## Applicability Rule

- `Diagram` is expected for material feature work, workflow/tooling changes,
  ambiguous implementation work, and any ticket where trust depends on seeing
  changed components or interfaces but the file map alone is not enough.
- `Type Sketch` plus `Typed flow example` are required for material,
  stateful, interface-heavy, or cross-boundary work where trust depends on
  seeing data-shape continuity.
- `Gap Analysis` is required only when the work is missing, partial,
  parity-driven, or otherwise under-specified.
- `Type Sketch`, `Typed flow example`, and `Diagram` may be short or omitted
  for trivial, narrowly localized fixes where the code context already anchors
  the expected behavior.

## Acceptance Criteria

- [ ] AC-1

## Verification

- `Tests:`
- `Manual checks:`
- `Evidence required:`
- `Artifacts path:` `tickets/artifacts/TASK-XXXX/`

## Refs

- optional durable links only

## Evidence

- `Artifacts:`
- `Commands:`
- `Plan review:`
  - `Refs used:`
  - `Checks:`
  - `Fixes:`
- `Result summary:`
- `Ready:` yes / no

## Blockers

- none
