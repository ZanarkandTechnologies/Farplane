# Code Quality

Use when reviewing code changes. This is the main code rubric; API/backend/type concerns live as explicit sub-lenses inside it rather than separate live skill trees.

Required TAS: `TAS-A`

## Family TAS Guide

- `TAS-C`: the change is unsafe, tangled, misleading, or obviously not ready to land
- `TAS-B`: some useful implementation exists, but trust is low because defects,
  boundary leaks, or maintainability problems are still material
- `TAS-B`: workable and directionally correct, but ordinary enough that a focused
  cleanup or hardening pass is still warranted
- `TAS-A`: strong, maintainable, and pass-worthy with only minor caveats
- `TAS-A`: unusually clean, economical, and robust within scope

## Dimensions

- `modularity-reusability`
- `bloatability`
- `readability`
- `boundary-clarity`
- `error-handling`
- `maintainability`

### `modularity-reusability`

Inspect: duplication, composability, and whether existing patterns are reused
when they should be.

Ask:

- Did this change reuse the right local abstractions?
- Is there new duplication or coupling that the next change will pay for?

### `bloatability`

Inspect: dead surface, speculative abstraction, and unnecessary compatibility
weight.

Ask:

- What code was added that is not earning its keep?
- Did this change remove any dead weight, or at least avoid adding more?

### `readability`

Inspect: local clarity, naming, comments, and cognitive load for the next
engineer.

Ask:

- Can a new reader explain the intent of the changed code quickly?
- Are comments clarifying hard parts, or covering for confusing structure?

### `boundary-clarity`

Inspect: ownership, module seams, and leakiness across layers or files.

Ask:

- Are responsibilities localized where a future fix would naturally look?
- Did the change quietly move policy into the wrong layer?
- Did a rename, rule, or invariant change in one file but not its neighboring ownership surfaces?

### `error-handling`

Inspect: failure paths, recovery behavior, surfacing, and operator usefulness.

Ask:

- What happens when the happy path breaks?
- Are failures explicit and actionable, or silent and ambiguous?

### `maintainability`

Inspect: brittleness, testability, change cost, and future modification risk.

Ask:

- Would the next engineer be comfortable modifying this without fear?
- Does this implementation create hidden rules or one-off behavior?

## Sub-Lenses

Use these lenses when relevant and include findings under this rubric:

- `api`: contract correctness, validation/error-path proof, backward safety
- `backend`: state/data correctness, mutation safety, regression exposure
- `types`: invariant strength, illegal-state prevention, mutation safety

## Evidence and Finding Cues

- Weak evidence usually looks like working happy-path code with unclear
  boundaries or unexamined failure behavior.
- Ordinary evidence usually covers the main path but leaves some duplication,
  awkwardness, or risk debt.
- Strong evidence shows clear local structure, explicit failure handling, and
  low surprise for future maintainers.
- Exceptional evidence not only avoids defects, but also improves the shape of
  the surrounding code.
- Findings should name the specific leak, duplication, brittle branch,
  neighboring-surface inconsistency, or failure-path miss with file context when
  possible.

## Desloppify Cues

When using the anti-slop playbook, search for:

- a duplicated constant, helper, or policy that should have changed too
- a rename that stopped at the primary file
- a stale caller or export contract
- comments/docstrings that now lie about the implementation
- dead compatibility branches or debug residue that no longer earn their keep

## Example Judgments

- `TAS-B` example:
  the bug is mostly fixed, but the patch duplicates logic in a second location,
  leaves one failure path silent, and quietly increases coupling across modules.
- `TAS-B` example:
  the code works and the structure is mostly sane, but some awkward branching,
  weak naming, or lightly handled errors still make a cleanup pass worthwhile.
- `TAS-A` example:
  the change is localized, reuses the right local pattern, handles failures
  explicitly, and leaves only minor readability or polish concerns.
- `TAS-A` example:
  the code solves the ticket and also improves the surrounding module shape by
  removing dead weight, clarifying ownership, or making future changes obviously easier.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `tas`
- `required_tas`
- `pass`
- `checks`
- `failed_checks`
- `findings`
- `next_action`
