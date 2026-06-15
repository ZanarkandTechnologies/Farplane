---
owner: learning-drain
purpose: weekly automation prompt wrapper
---

# Learning Drain Automation Prompt

Use this as the legacy automation body when a scheduler still calls
`learning-drain`. New weekly skill upkeep should call
`skill-maintenance(mode: harden_skill)` directly. This wrapper remains a thin
pointer for source intake: caps, dedupe, processed state, and hardening handoff
routing.

```text
Run the Farplane learning-drain compatibility wrapper for this project, then
return a skill-maintenance harden_skill handoff for actionable skill/package
issues.

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
- Route concrete skill/package prevention work to skill-maintenance mode
  harden_skill.
- Route non-skill harness/process behavior gaps to optimize-harness.
- Route testable durable regressions to eval.
- Write processed rows to .farplane/state/learning-drain/processed.jsonl.
- Return a Learning Drain Report with harden_skill handoff refs, other
  follow-up refs, and deferred rows.
```

If the automation surface supports a direct skill invocation, use the skill
name and parameters instead of this prose prompt:

```text
skill=learning-drain
mode=automation
project_root=/Users/kenjipcx/Zanarkand Technologies/projects/Farplane
cap=5
canonical_next=skill-maintenance:harden_skill
```
