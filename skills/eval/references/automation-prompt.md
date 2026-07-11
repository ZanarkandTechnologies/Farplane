---
title: Eval Drain Automation Prompt
owner: skills/eval
status: active
created_at: 2026-06-13
updated_at: 2026-06-13
---

# Eval Drain Automation Prompt

Use this as the automation body when a scheduler should run the weekly eval
drain. The automation is only a pointer. The eval skill owns discovery,
subagent consolidation, processed state, proof, and review routing.

```text
Run the Farplane eval skill in consolidation mode for this project.

Project root:
/Users/kenjipcx/Zanarkand Technologies/projects/Farplane

Mode:
automation

Inputs:
- Read skills/eval/SKILL.md.
- Read skills/eval/references/eval-consolidation.md.
- Run fetch_evals_edited_since_last_run against skills/*/evals/evals.json.
- Read .farplane/state/eval-drain/processed.jsonl if present.

Policy:
- Do not delay or remove immediate lesson/trouble-derived eval creation.
- Fetch eval files edited since the last accepted eval drain using content
  hashes, not filesystem mtimes alone.
- For each changed eval file, run `consolidate(..., structure = eval_suite)`
  directly or through one isolated review lane with the eval file,
  consolidation guide, and eval-writing rubric as context.
- Each subagent returns keep, merge, rewrite, archive notes, lost coverage
  risks, and apply/revise/defer recommendation.
- Apply only consolidations that make evals less noisy without losing distinct
  failure modes.
- Keep hardcases unless a stronger replacement explicitly preserves their
  benchmark value.
- Append processed rows to .farplane/state/eval-drain/processed.jsonl only
  after accepted consolidation or explicit no-op/defer disposition.
- Return an Eval Drain Report with changed files, per-eval recommendations,
  applied changes, deferred risks, processed-state path, and proof commands.
```

If the automation surface supports a direct skill invocation, use the skill
name and parameters instead of this prose prompt:

```text
skill=eval
mode=consolidate
project_root=/Users/kenjipcx/Zanarkand Technologies/projects/Farplane
state=.farplane/state/eval-drain/processed.jsonl
```
