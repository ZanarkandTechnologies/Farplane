---
owner: learning-drain
purpose: weekly automation prompt wrapper
---

# Learning Drain Automation Prompt

Use this as the automation body when a scheduler should run the weekly learning
drain. The automation is only a pointer. The skill owns behavior, caps, dedupe,
processed state, and follow-up routing.

```text
Run the Farplane learning-drain skill for this project.

Project root:
/Users/kenjipcx/Zanarkand Technologies/projects/Farplane

Mode:
automation

Inputs:
- Read docs/TROUBLES.md.
- Read docs/LESSONS.md.
- Read .farplane/state/learning-drain/processed.jsonl if present.
- Read .farplane/state/self-improve/weekly-drain-processed.jsonl only as a
  legacy compatibility source if present.

Policy:
- Cap actionable follow-ups at 5.
- Do not delete or rewrite TROUBLES/LESSONS rows.
- Do not reprocess rows already present in processed state.
- Pair related trouble and lesson rows before creating follow-ups.
- Route concrete harness/process behavior gaps to optimize-harness.
- Route testable durable regressions to eval.
- Route skill-system maintenance to skill-maintenance.
- Write processed rows to .farplane/state/learning-drain/processed.jsonl.
- Return a Learning Drain Report with follow-up refs and deferred rows.
```

If the automation surface supports a direct skill invocation, use the skill
name and parameters instead of this prose prompt:

```text
skill=learning-drain
mode=automation
project_root=/Users/kenjipcx/Zanarkand Technologies/projects/Farplane
cap=5
```
