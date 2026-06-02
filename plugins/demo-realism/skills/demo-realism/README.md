# Demo Realism

## Purpose

`demo-realism` helps agents turn a vague MVP or client-demo idea into a
believable realism pack: operating hypothesis, workflow ladder, screen/state
ladder, realistic demo data, and a presentation-worthiness rubric.

## Public API / Entrypoints

- [`SKILL.md`](/Users/kenjipcx/coding-harness/Farplane/skills/demo-realism/SKILL.md)
- [`references/architecture.md`](/Users/kenjipcx/coding-harness/Farplane/skills/demo-realism/references/architecture.md)
- [`references/workflows.md`](/Users/kenjipcx/coding-harness/Farplane/skills/demo-realism/references/workflows.md)
- [`references/gotchas.md`](/Users/kenjipcx/coding-harness/Farplane/skills/demo-realism/references/gotchas.md)
- [`references/rubric.md`](/Users/kenjipcx/coding-harness/Farplane/skills/demo-realism/references/rubric.md)

## Minimal Example

Use `demo-realism` when a prototype feels fake and needs believable workflow and
data assumptions before design/build.

Example ask:

```text
Use demo-realism for a warehouse operations demo aimed at regional directors.
We need believable workflows, realistic exceptions, and demo data that feels
presentable to a real client.
```

## How To Test

- Read [`SKILL.md`](/Users/kenjipcx/coding-harness/Farplane/skills/demo-realism/SKILL.md) and confirm the first-load workflow is executable without references.
- Run:

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/demo-realism
```

- Manually verify the skill output contract includes:
  - client operating hypothesis
  - pitch-worthy MVP slice
  - workflow ladder
  - screen/state ladder
  - demo-data pack
  - realism rubric
