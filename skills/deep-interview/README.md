# Deep Interview Skill

## Purpose

`deep-interview` turns a vague request into a clarified requirements brief
before `prd`, `impl-plan`, bootstrap scaffolding, or execution.

## Public Entrypoints

- `SKILL.md` - live interview contract and handoff rules

## Minimal Example

```text
$deep-interview --quick "clarify the first acceptable slice for TASK-0048"
```

```text
$deep-interview --bootstrap "clarify repo topology, stack, and push gates for a new project"
```

## How To Test

- `rg -n '\.omx|\bomx\b' skills/deep-interview/SKILL.md`
- re-read `skills/deep-interview/SKILL.md` against `tickets/README.md` and `docs/specs/context-and-handoff-policy.md`
