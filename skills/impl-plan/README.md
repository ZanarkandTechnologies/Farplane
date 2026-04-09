# Impl Plan

## Purpose

Guide agents to produce one clear per-ticket planning artifact, with default
approval-first planning and optional consensus challenge for riskier work.

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `prompts/plan.md`: operator prompt
- `references/template.md`: merged plan template
- `references/examples.md`: good/bad examples
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read `SKILL.md`.
2. Decide `one commit` vs `split`.
3. Choose default mode or `--consensus`.
4. Output a concise approval surface plus richer sections when the work needs them.

## How to Test

- Confirm `B -> A` appears near the top.
- Confirm the recommendation appears near the top.
- Confirm `User Story` / `High-Fidelity Example` are required only when the applicability rule says they should be.
- Confirm consensus mode still preserves Planner/Architect/Critic challenge inside the same public skill.
