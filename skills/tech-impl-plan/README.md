# Tech Impl Plan

## Purpose

Guide agents to produce compact approval-first implementation plans.

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `prompts/plan.md`: operator prompt
- `references/template.md`: compact plan template
- `references/examples.md`: good/bad examples
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read `SKILL.md`.
2. Decide `one commit` vs `split`.
3. Output `Pitch`, `B -> A`, `Delta`, `Core Flow`, `Proof`, `Ask`.

## How to Test

- Confirm `B -> A` appears near the top.
- Confirm pseudocode is the default teaching tool.
- Confirm appendix detail is optional.
