# Impl Plan

## Purpose

Guide agents to produce one clear per-ticket planning artifact, with a detailed
action-oriented ticket-body plan shape, conditional diagrams when the file map
alone is not enough, and optional consensus challenge for riskier work.
This is the Tier 3 coding-pipeline implementation of the generic
[`plan`](/Users/kenjipcx/coding-harness/Codexter/skills/plan/SKILL.md)
interface.
When an `Agent Testability Brief` exists, `impl-plan` should preserve that
doctrine in the resulting proof and execution plan.

For standalone diagram work or deeper diagram taste/pattern guidance, use
[`diagramming`](/Users/kenjipcx/coding-harness/Codexter/skills/diagramming/SKILL.md).

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `SKILL.md` Important Checklist: example natural-language todo template for detailed ticket planning
- `prompts/plan.md`: operator prompt
- `references/template.md`: merged plan template
- `references/examples.md`: good/bad examples
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read `SKILL.md`.
2. Use the `SKILL.md` Important Checklist near the start so the ordered
   checklist stays loaded during the pass.
3. Treat the selected ticket as the planning boundary by default, and split
   only if a real boundary justifies it.
4. Choose default mode or `--consensus`.
5. Output one detailed ticket plan with summary, scope, `Plan`, and only the
   optional sections the ticket actually needs.
6. Use `Signature delta` for callable seams and `Type Sketch` plus `Typed flow
   example` when typed data continuity matters.

## How to Test

- Confirm the output matches the canonical ticket-body shape.
- Confirm the plan targets the full selected ticket instead of inventing a
  smaller internal "first slice" without a real boundary.
- Confirm `Execution steps` make the next build steps explicit when sequencing
  matters.
- Confirm the diagram appears near the top when material work needs one to make
  flow, ownership, or typed data path legible.
- Confirm a compact `Signature delta` appears when interfaces matter.
- Confirm `Type Sketch` plus `Typed flow example` appear for material,
  stateful, or interface-heavy work.
- Confirm the `SKILL.md` Important Checklist reinforces planning behaviors as plain natural-language checklist text without becoming a second template.
- Confirm the recommendation appears near the top.
- Confirm optional sections are required only when the applicability rule says
  they should be.
- Confirm consensus mode still preserves Planner/Architect/Critic challenge inside the same public skill.
- Confirm any `Agent Testability Brief` is carried into the proof/testability shape instead of being ignored.
