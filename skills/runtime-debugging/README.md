# Runtime Debugging Skill

## Purpose

Guide agents through hypothesis-driven runtime debugging for reproducible bugs, regressions, flaky failures, and other issues that need runtime evidence before a fix.

## Public API / Entrypoints

- `SKILL.md`: main entrypoint loaded by the agent.
- `AGENTS.md`: maintenance rules for keeping the skill boundary tight and stable.
- `references/*.md`: focused playbooks for specific debugging entry modes.

## Minimal Example

1. Read `SKILL.md`.
2. Pick the matching reference file for the bug type.
3. Capture the bug symptom and exact reproduction path.
4. Form a small hypothesis set and add the minimum instrumentation needed.
5. Reproduce, analyze the evidence, apply the smallest fix, and verify it.

## How to Test

- Confirm `SKILL.md` includes triggers, workflow, bug-type selector, decision branches, gotchas, and output contract.
- Confirm it routes UI-specific issues to `visual-qa`.
- Confirm it distinguishes obvious errors from evidence-heavy runtime investigations.
- Confirm every linked reference file exists and has a distinct scope.
