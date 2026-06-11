---
name: functional-ui
version: 1.1.0
description: "Turn broken or unclear product workflows into user stories, UI-state diagnosis, comparable examples, and implementation handoff."
tier: 3
group: frontend
source: local
common_chains:
  after: ["visual-design"]
---

# Functional UI

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] State the UI/workflow decision and the artifact being produced:
  diagnosis, UX plan, redesign recommendation, or implementation handoff.
- [ ] Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
  when users, jobs, contexts, friction, or success signals are not already
  settled.
- [ ] Use [research:competitor](../research/SKILL.md#researchcompetitor) or
  [research:parity](../research/SKILL.md#researchparity) when comparable app
  workflows or established product patterns should shape the options.
- [ ] Diagnose the current UI or planned workflow before proposing visual or
  component changes.
- [ ] Use the native planning phase to compare the strongest interaction models
  and choose one recommended workflow.
- [ ] Define screens, states, IA, interaction rules, data/content ranges, and
  edge cases.
- [ ] Hand off to [visual-design](../visual-design/SKILL.md) when look/taste is
  still open, or [frontend-craft](../frontend-craft/SKILL.md) when the workflow
  is ready to build.
- [ ] Use the native execution phase for proof/writeback shape before
  claiming the functional UI plan is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this before visual implementation when the question is how the product should work, why a current UI feels wrong, or how a component/flow should be redesigned from proven examples.

## Job

1. Identify the user, context, and top jobs-to-be-done.
2. Diagnose the current UI or planned workflow.
3. Study comparable/latest examples and the workflows they prove.
4. Compare 3 viable interaction models or redesign paths.
5. Recommend one path clearly.
6. Define states, IA, interaction rules, and implementation handoff.

## Use When

- the user asks for UI or UX direction
- the user says "this UI sucks", "functional-ui this", "redesign this component", or asks why a screen/flow feels wrong
- a screen or flow needs functional structure before styling
- product behavior, IA, or workflow is still open
- the team keeps redesigning common patterns from scratch
- `frontend-craft` is implementing a frontend and no current UX brief settles users, states, and interactions

## Do Not Use When

- the workflow is already chosen and the task is purely visual polish
- the request is a landing page narrative; use `landing-page`
- the task is a finished UI review; use `web-design-guidelines`

## Workflow

1. Capture the primary user/persona and the top jobs-to-be-done.
2. Read the PRD, spec, ticket, request, screenshot, or current component to extract states, constraints, and failure modes.
3. Diagnose the current UI using [redesign-diagnosis.md](references/redesign-diagnosis.md) when a broken UI exists.
4. Inspect 2-4 comparable apps, examples, or established patterns using [comparable-patterns.md](references/comparable-patterns.md). Focus on workflow and behavior, not surface aesthetics.
5. Produce 3 grounded UI options with pros and cons.
6. Recommend one workflow and explain why it best fits the user stories.
7. Define screens, states, IA, interaction rules, data/content ranges, and edge cases.
8. Hand off with [implementation-handoff.md](references/implementation-handoff.md) to `visual-design` or `frontend-craft`.

## Decision Branches

| Situation | Output emphasis |
| --- | --- |
| Broken existing component | diagnosis, comparable examples, recommended redesign, implementation handoff |
| New app screen | users, jobs, IA, states, interaction model |
| Repeated workflow | speed, defaults, keyboard/touch paths, empty/error/success states |
| Dense dashboard/tool | scan paths, prioritization, filters, table/list behavior |
| AI/chat/workflow UI | conversation states, tool progress, sources, retry/failure recovery |

## Output

Produce a compact planning artifact with:

- `Users + stories`
- `Current UI diagnosis` when redesigning an existing surface
- `Comparable apps`
- `Recommendation`
- `Key screens/states`
- `Interaction rules`
- `Implementation handoff`
- `Options appendix`

## Guardrails

- start from the user story, not the component library
- borrow proven patterns before inventing new ones
- compare workflows, not just visual references
- always recommend one path; do not stop at inspiration
- if the user did not provide a take, assume they want guided product judgment
- do not solve functional failures with visual-only advice
- do not specify final typography/color/motion taste beyond what the interaction model requires; hand that to `visual-design`

## Reference Files

- [redesign-diagnosis.md](references/redesign-diagnosis.md) - diagnose why a current UI fails.
- [comparable-patterns.md](references/comparable-patterns.md) - inspect adjacent products and extract reusable workflow patterns.
- [implementation-handoff.md](references/implementation-handoff.md) - package UX decisions for `frontend-craft`.
- [architecture.md](references/architecture.md) - ownership boundary and downstream handoff model.
- [workflows.md](references/workflows.md) - broken UI and new screen/flow paths.
- [gotchas.md](references/gotchas.md) - common functional-UI failure modes.
