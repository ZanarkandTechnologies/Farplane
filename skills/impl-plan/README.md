# Impl Plan

## Purpose

Guide agents to produce one clear per-ticket planning artifact, with a compact
diagram-first approval surface by default and optional consensus challenge for
riskier work.

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
5. Output a concise diagram-first approval surface plus richer sections when the work needs them.

## How to Test

- Confirm `Diagram Summary` appears near the top for material work.
- Confirm `B -> A` appears near the top.
- Confirm `todos.md` reinforces planning behaviors as plain natural-language checklist text without becoming a second template.
- Confirm the recommendation appears near the top.
- Confirm `User Story` / `High-Fidelity Example` are required only when the applicability rule says they should be.
- Confirm consensus mode still preserves Planner/Architect/Critic challenge inside the same public skill.
