# Eval Skill Module

## Purpose

This module owns the reusable local eval harness for Codex and Claude:

- scaffold `.farplane/evals`
- define the simple task JSON contract
- define shared eval config such as default fixture context
- run harness-native evals
- emit stable local run artifacts for Farplane UI Eval OS

## Editing Rules

- Keep task JSON simple: `id`, `title`, optional `context`, `query`,
  `reference_points`, optional `tags`, optional `notes`.
- Put suite-wide fixture setup in `config.json` plus `contexts/*`; use task
  `context` only for overrides, and use `context: ""` to disable the default
  context for a real-repo task.
- Keep AGI Toy Shop as the default fictional fixture for generic harness evals;
  extend it instead of creating one-off toy companies.
- Use Codex profiles for harness launch settings such as model, sandbox,
  approvals, MCP, and skill enable/disable. Do not put fixture facts or
  expected answers in profiles.
- Keep rubric policy in judge prompts, not task JSON.
- Prefer reusable templates under `templates/` over one-off runtime-only changes.
- If install-time behavior changes, update `scripts/run_evals.py`, the matching template files, and tests together.
- Keep UI implementation out of this package. Farplane UI owns Eval OS;
  this package owns only the artifact contract it consumes.

## Verification

- `python3 skills/eval/tests/test_run_evals.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
