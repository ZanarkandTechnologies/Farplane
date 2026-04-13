# Impl Plan

## Purpose

Guide agents to produce one clear per-ticket planning artifact, with a compact
diagram-first approval surface by default, a skimmable top `Human` lane, a
lower `Agent` execution lane, and optional consensus challenge for riskier
work.

For standalone diagram work or deeper diagram taste/pattern guidance, use
[`diagramming`](/Users/kenjipcx/coding-harness/Codexter/skills/diagramming/SKILL.md).

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `todos.md`: example natural-language todo template for approval-first planning
- `prompts/plan.md`: operator prompt
- `references/template.md`: merged plan template
- `references/examples.md`: good/bad examples
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read `SKILL.md`.
2. Read `todos.md` if using skill todos.
3. Decide `one commit` vs `split`.
4. Choose default mode or `--consensus`.
5. Output a top `Human` lane with decision, diagram, signature sketch,
   before/after, proof, and ask.
6. Output a lower `Agent` lane with delta, execution order, risk/rollback, and
   ticket move.

## How to Test

- Confirm `Human` appears before `Agent`.
- Confirm the diagram appears near the top for material work.
- Confirm a compact `Signature Sketch` appears near the top when interfaces
  matter.
- Confirm `B -> A` appears near the top.
- Confirm `todos.md` reinforces planning behaviors as plain natural-language checklist text without becoming a second template.
- Confirm the recommendation appears near the top.
- Confirm narrative sections are required only when the applicability rule says
  they should be.
- Confirm consensus mode still preserves Planner/Architect/Critic challenge inside the same public skill.
