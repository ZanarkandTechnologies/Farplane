# Eval Skill Module

## Purpose

This module owns the reusable local eval harness for Codex and Claude:

- scaffold `.codex/evals` or `.claude/evals`
- define the simple task JSON contract
- run harness-native evals
- render local run artifacts through the bundled viewer

## Editing Rules

- Keep task JSON simple: `id`, `title`, `query`, `reference_points`, optional `tags`, optional `notes`.
- Keep rubric policy in judge prompts, not task JSON.
- Prefer reusable templates under `templates/` over one-off runtime-only changes.
- If install-time behavior changes, update `scripts/run_evals.py`, the matching template files, and tests together.
- Keep the viewer standalone and local-first: it should work from a file picker without requiring a framework build.

## Verification

- `python3 skills/eval/tests/test_run_evals.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
