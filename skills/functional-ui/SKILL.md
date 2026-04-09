---
name: functional-ui
description: Use when planning product UI or UX flows. Grounds recommendations in user stories, comparable apps, and a clear best-path recommendation before visual styling work begins.
---

# Functional UI

Use this before visual implementation when the question is how the product should work, not just how it should look.

## Job

1. Identify the user and their top user stories.
2. Study similar apps and the workflows they already prove.
3. Compare 3 viable interaction models.
4. Recommend the best one.
5. Hand the chosen workflow to `frontend-design` for visual execution.

## Use When

- the user asks for UI or UX direction
- a screen or flow needs functional structure before styling
- product behavior, IA, or workflow is still open
- the team keeps redesigning common patterns from scratch

## Do Not Use When

- the workflow is already chosen and the task is purely visual polish
- the request is a landing page narrative; use `cinematic-landing`
- the task is a finished UI review; use `web-design-guidelines`

## Workflow

1. Capture the primary user/persona and the top jobs-to-be-done.
2. Read the PRD, spec, ticket, or request to extract the key states and constraints.
3. Inspect 2-4 comparable apps and focus on the overlapping workflow, not surface aesthetics.
4. Produce 3 grounded UI options with pros and cons.
5. Recommend one workflow and explain why it best fits the user stories.
6. Define the key screens, states, IA, and interaction rules for the chosen path.
7. Hand off to `frontend-design` once the functional shape is settled.

## Output

Produce a compact planning artifact with:

- `Users + stories`
- `Comparable apps`
- `Recommendation`
- `Key screens/states`
- `Options appendix`

## Guardrails

- start from the user story, not the component library
- borrow proven patterns before inventing new ones
- compare workflows, not just visual references
- always recommend one path; do not stop at inspiration
- if the user did not provide a take, assume they want guided product judgment
