# Impl Plan

## Purpose

Guide agents to produce one approval-ready ticket plan with a compact
before/after delta, modular `Change Plan`, concrete `Done`, `QA Strategy`,
`Docs Strategy`, and a `plan_qa` readiness check.
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
- `qa_checklist.md`: material plan minimality, architecture-signature,
  reviewer-gate, and proof-route checks
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read `SKILL.md`.
2. Use the `SKILL.md` Todo List near the start so the ordered gates stay loaded.
3. Treat the selected ticket as the planning boundary by default, and split
   only if a real boundary justifies it.
4. Choose default mode or `--consensus`.
5. Output one detailed ticket plan with `Summary`, `Scope`, `Delta`,
   `Change Plan`, `Done`, `QA Strategy`, `Docs Strategy`, `Links`, and sparse
   `Notes`, plus optional `Agent Contract` or `Run Hints` when warranted.
6. For material plans, put compact `architecture_signatures` at the top of
   `Change Plan`; use `signature_or_type_impact` inside units only for local
   deltas.
7. Run `qa_checklist.md` before accepting a material plan.
8. Request a native reviewer lane for material plan readiness and reconcile its
   verdict before calling the plan approval-ready.
9. Add an optional visual map only when topology or ownership is clearer that
   way.

## How to Test

- Confirm the output matches the compact ticket-body shape.
- Confirm the plan targets the full selected ticket instead of inventing a
  smaller internal "first slice" without a real boundary.
- Confirm `Change Plan` makes the next build steps, file surfaces, routes, and
  unit-level QA expectations explicit when sequencing matters.
- Confirm material plans expose top-level `architecture_signatures` or a
  concrete localized-fix exemption.
- Confirm optional maps appear only when material work is easier to understand
  visually.
- Confirm callable seams appear in `architecture_signatures` for the top-level
  architecture and in the relevant Change Plan unit for local deltas.
- Confirm typed flow appears in the relevant Change Plan unit for material,
  stateful, or interface-heavy work.
- Confirm the `SKILL.md` Todo List reinforces planning gates without becoming a
  second template.
- Confirm `plan_qa` records minimality, reuse, least-parameter, file/function,
  split-boundary, architecture-signature, reviewer-gate, and proof-route
  results for material plans.
- Confirm the recommendation appears only when a real decision exists.
- Confirm optional sections are required only when the applicability rule says
  they should be.
- Confirm `Evidence` is not emitted as default planning boilerplate.
- Confirm consensus mode still preserves Planner/Architect/Critic challenge inside the same public skill.
- Confirm any `Agent Testability Brief` is carried into `QA Strategy` instead
  of being ignored.
