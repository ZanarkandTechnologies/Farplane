# Code Quality

Use when reviewing code changes. This is the main code rubric; API/backend/type concerns live as explicit sub-lenses inside it rather than separate live skill trees.

Threshold: `4.0`

## Dimensions

- `modularity-reusability`
- `bloatability`
- `readability`
- `boundary-clarity`
- `error-handling`
- `maintainability`

## Anchors

### `modularity-reusability`

- `1`: the code is tangled, duplicated, or hard to reuse safely
- `3`: the main modular shape is okay, but some reuse/boundary opportunities are still weak
- `5`: the code is cleanly modular and reuses existing patterns where it should

### `bloatability`

- `1`: dead code, stale compatibility layers, or unnecessary legacy remain embedded in the change
- `3`: some avoidable weight remains, but not enough to block the work
- `5`: the implementation removes dead weight and does not add unearned surface area

### `readability`

- `1`: the code is hard to follow, under-explained, or misleading
- `3`: readable enough, though some sections still make the next engineer work too hard
- `5`: the code reads clearly, comments help where needed, and the intent makes sense quickly

### `boundary-clarity`

- `1`: responsibilities leak across modules and ownership is confusing
- `3`: boundaries are mostly understandable, but still somewhat muddy
- `5`: interfaces and responsibilities are localized and obvious

### `error-handling`

- `1`: failure paths are missing, silent, or unsafe
- `3`: major failures are handled, but some paths remain vague or weakly surfaced
- `5`: failures are explicit, contextualized, and operationally useful

### `maintainability`

- `1`: the change is brittle or high-risk to modify later
- `3`: workable to maintain, but with some friction from shape or duplication
- `5`: future modification is straightforward and low-risk

## Sub-Lenses

Use these lenses when relevant and include findings under this rubric:

- `api`: contract correctness, validation/error-path proof, backward safety
- `backend`: state/data correctness, mutation safety, regression exposure
- `types`: invariant strength, illegal-state prevention, mutation safety

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
