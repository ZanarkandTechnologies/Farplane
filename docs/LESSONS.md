# Lessons

Append distilled lessons here after a trouble, repent pass, review failure, or
hardcase has been fixed or classified.

`docs/TROUBLES.md` is the raw pain-point log. This file is the smaller,
actionable learning log used to improve prompts, skills, policies, evals, and
review gates.

## When To Write Here

- `repent lesson` produced a reusable prevention rule after the fix.
- a `docs/TROUBLES.md` row recurred or revealed a stable prompt/skill gap.
- review or QA found a repeatable agent failure worth encoding.
- a hardcase should inform future evals, prompt guidance, or skill behavior.

## Format

```text
YYYY-MM-DD HH:mm Z | area,tags | source | lesson | owner | next_prompt_or_skill_change
```

## Promotion Rule

Promote durable rules from this file into `docs/MEMORY.md`, `AGENTS.md`, the
owning skill, a validator, or an eval only after the lesson is stable enough to
guide future work.
