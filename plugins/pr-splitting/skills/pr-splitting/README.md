# PR Splitting

## Purpose

Help agents turn one finished working branch into smaller non-stacked PR plans,
preferring feature-first slices and falling back to layer-based buckets when
feature seams are too entangled.

## Public API / Entrypoints

- `SKILL.md`: main PR-splitting contract
- `todos.md`: compact anti-forgetting checklist
- [`references/decision-rules.md`](/Users/kenjipcx/coding-harness/Codexter/skills/pr-splitting/references/decision-rules.md)
- [`references/output-template.md`](/Users/kenjipcx/coding-harness/Codexter/skills/pr-splitting/references/output-template.md)
- `AGENTS.md`: maintenance notes

## Minimal Example

1. Pick the base branch.
2. Inspect the final diff and identify candidate feature stories.
3. Keep feature slices end to end when they can merge cleanly.
4. Fall back to layer buckets only when feature seams are too entangled.
5. Return PR buckets with exact file lists, size, blockers, and branch steps.

## How to Test

- Confirm `SKILL.md` makes feature-first the default.
- Confirm `SKILL.md` explicitly discourages hunk-based splitting.
- Confirm the references add decision depth and output shape instead of
  replacing the core workflow.
- Confirm the output contract always includes exact files and a refusal path.
