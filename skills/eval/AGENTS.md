# Eval Skill Module

## Purpose

This module owns the reusable local eval harness for Codex and Claude:

- scaffold `.farplane/evals`
- define the simple task JSON contract
- define shared eval config such as default fixture context
- run harness-native evals
- render local run artifacts through the bundled viewer

## Editing Rules

- Keep task JSON simple: `id`, `title`, optional `context`, `query`,
  `reference_points`, optional `tags`, optional `notes`.
- Put suite-wide fixture setup in `config.json` plus `contexts/*`; use task
  `context` only for overrides, and use `context: ""` to disable the default
  context for a real-repo task.
- Keep rubric policy in judge prompts, not task JSON.
- Prefer reusable templates under `templates/` over one-off runtime-only changes.
- If install-time behavior changes, update `scripts/run_evals.py`, the matching template files, and tests together.
- Keep the viewer standalone and local-first: it should work from a file picker without requiring a framework build.

## Verification

- `python3 skills/eval/tests/test_run_evals.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
