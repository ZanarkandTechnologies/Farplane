# Eval Skill Module

## Purpose

This module owns Farplane's reusable eval boundary:

- scaffold `.farplane/evals`
- keep skill behavior suites in Agent Skills `evals/evals.json`
- define shared eval config such as default fixture context
- project skill comparisons into Promptfoo without a second authored suite
- retain the existing harness-native runner for project suites and behavior traces
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
- For skill comparisons, let Promptfoo own execution, skill-use assertions,
  rubric grading, and raw export; keep the adapter deterministic.
- Author string IDs and one `assertions` list only. `farplane lint evals`
  rejects legacy aliases and unknown fields before the adapter creates a run.
- Stage candidate, baseline, and grader outside the source checkout; copy only
  evidence back into the run artifact.
- Prefer reusable templates under `templates/` over one-off runtime-only changes.
- If install-time behavior changes, update `scripts/run_evals.py`, the matching template files, and tests together.
- Keep UI implementation out of this package. Farplane UI owns Eval OS;
  this package owns only the artifact contract it consumes.

## Verification

- `python3 skills/eval/tests/test_run_evals.py`
- `python3 skills/eval/tests/test_run_promptfoo.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
