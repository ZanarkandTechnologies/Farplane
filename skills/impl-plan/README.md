# Impl Plan

## Purpose

Guide agents to produce one clear per-ticket planning artifact, with a compact
before/after delta, a visual map that can carry changed seams and typed flow,
an ordered build plan, concrete verification, and optional consensus challenge
for riskier work.
This is the Tier 3 coding-pipeline implementation of the generic
[`plan`](/Users/kenjipcx/coding-harness/Farplane/skills/plan/SKILL.md)
interface.
When an `Agent Testability Brief` exists, `impl-plan` should preserve that
doctrine in the resulting proof and execution plan.

For standalone diagram work or deeper diagram taste/pattern guidance, use
[`diagramming`](/Users/kenjipcx/coding-harness/Farplane/skills/diagramming/SKILL.md).

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `SKILL.md` Todo List: example natural-language todo template for detailed ticket planning
- `prompts/plan.md`: operator prompt
- `references/template.md`: merged plan template
- `references/examples.md`: good/bad examples
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read `SKILL.md`.
2. Use the `SKILL.md` Todo List near the start so the ordered
   checklist stays loaded during the pass.
3. Treat the selected ticket as the planning boundary by default, and split
   only if a real boundary justifies it.
4. Choose default mode or `--consensus`.
5. Output one detailed ticket plan with `Summary`, `Scope`, `Delta`, `Map`,
   `Build Plan`, `Verification`, and sparse `Notes`.
6. Put callable seams and typed data movement in the map first; add fallback
   signature or type-flow detail only when the map would become crowded.

## How to Test

- Confirm the output matches the compact ticket-body shape.
- Confirm the plan targets the full selected ticket instead of inventing a
  smaller internal "first slice" without a real boundary.
- Confirm `Build Plan` makes the next build steps explicit when sequencing
  matters.
- Confirm the map appears near the top when material work is easier to
  understand visually.
- Confirm callable seams appear in the map or a compact fallback list when
  interfaces matter.
- Confirm typed flow appears in the map or compact fallback flow for material,
  stateful, or interface-heavy work.
- Confirm the `SKILL.md` Todo List reinforces planning behaviors as plain natural-language todo-list text without becoming a second template.
- Confirm the recommendation appears only when a real decision exists.
- Confirm optional sections are required only when the applicability rule says
  they should be.
- Confirm `Evidence` is not emitted as default planning boilerplate.
- Confirm consensus mode still preserves Planner/Architect/Critic challenge inside the same public skill.
- Confirm any `Agent Testability Brief` is carried into the proof/testability shape instead of being ignored.
