# Impl Plan

## Purpose

Guide agents to produce one approval-ready ticket plan with a compact
before/after delta, task program, visual map when useful, concrete
`Done / Proof`, and a `plan_qa` readiness check.
This is the Tier 3 coding-pipeline implementation of the generic `plan`
interface.
When an `Agent Testability Brief` exists, `impl-plan` should preserve that
doctrine in the resulting proof and execution plan.

For standalone diagram work or deeper diagram taste/pattern guidance, use
`skills/diagramming/SKILL.md`.

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `SKILL.md` Todo List: first-load workflow and gates
- `prompts/plan.md`: operator prompt
- `references/template.md`: merged plan template
- `references/examples.md`: good/bad examples
- `qa_checklist.md`: material plan minimality and proof-route checks
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read `SKILL.md`.
2. Use the `SKILL.md` Todo List near the start so the ordered gates stay loaded.
3. Treat the selected ticket as the planning boundary by default, and split
   only if a real boundary justifies it.
4. Choose default mode or `--consensus`.
5. Output one detailed ticket plan with `Summary`, `Scope`, `Delta`, `Program`,
   `Map`, `Done / Proof`, `State`, `Links`, and sparse `Notes`.
6. Run `qa_checklist.md` before accepting a material plan.
7. Put callable seams and typed data movement in the map first; add fallback
   signature or type-flow detail only when the map would become crowded.

## How to Test

- Confirm the output matches the compact ticket-body shape.
- Confirm the plan targets the full selected ticket instead of inventing a
  smaller internal "first slice" without a real boundary.
- Confirm `Program` makes the next build steps explicit when sequencing
  matters.
- Confirm the map appears near the top when material work is easier to
  understand visually.
- Confirm callable seams appear in the map or a compact fallback list when
  interfaces matter.
- Confirm typed flow appears in the map or compact fallback flow for material,
  stateful, or interface-heavy work.
- Confirm the `SKILL.md` Todo List reinforces planning gates without becoming a
  second template.
- Confirm `plan_qa` records minimality, reuse, least-parameter, file/function,
  split-boundary, and proof-route results for material plans.
- Confirm the recommendation appears only when a real decision exists.
- Confirm optional sections are required only when the applicability rule says
  they should be.
- Confirm `Evidence` is not emitted as default planning boilerplate.
- Confirm consensus mode still preserves Planner/Architect/Critic challenge inside the same public skill.
- Confirm any `Agent Testability Brief` is carried into the proof/testability shape instead of being ignored.
