# Reference Grounding

## Purpose

Ground decisions, plans, and claims in the smallest useful set of local or
external references before another workflow consumes them.

## Public API / Entrypoints

- `SKILL.md`: Tier 1 grounding contract
- `SKILL.md` Todo List: anti-forgetting checklist
- `AGENTS.md`: maintenance rules

## Minimal Example

1. State the claim that needs evidence.
2. Check the local baseline and one fitting source class.
3. Return evidence, confidence, and local impact.
4. Escalate to `research:*` only when a broader brief is needed.

## How To Test

- Confirm the skill produces a compact grounding note, not a research dump.
- Confirm it names source confidence and local impact.
- Confirm broad parity/gap/source-synthesis work is routed to `research:*`.
