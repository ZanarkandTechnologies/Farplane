# Eval Quality Review

Use this family when eval tasks, task fixtures, judge prompts, runner scripts,
artifact schemas, or eval onboarding guidance changed.

## TAS Guide

- `TAS-A`: eval tasks are realistic, reference points are clear text strings,
  judge rubrics are outside task JSON, execution uses the target harness, and
  artifacts make failures actionable.
- `TAS-B`: the eval is useful, but one or more required checks fail in a
  repairable way.
- `TAS-C`: a blocker check fails, the eval judges the wrong behavior, the
  runner simulates the harness instead of running it, or the output cannot
  guide improvement.
- `TAS-D`: task fixtures, judge prompt, runner command, or output artifacts are
  missing enough that the eval cannot be judged.

## Checklist Modules

### Required Checks

- [ ] `fixture-stable`: Each task has a stable `id`, clear title or task name,
  user-facing prompt/query, and `reference_points` as plain strings.
- [ ] `reference-points-observable`: Reference points describe expected
  observable outcomes rather than rubric policy.
- [ ] `judge-separated`: Rubric policy lives in the judge prompt or review
  handoff rather than task JSON.
- [ ] `binary-or-tiered`: Judge verdicts use boolean or TAS/tier judgments
  instead of fake-precise numeric scores.
- [ ] `real-harness`: The runner executes the user's real harness or agent CLI
  when validating behavior.
- [ ] `explicit-commands`: Command templates are explicit for Codex, Claude, or
  custom harnesses.
- [ ] `actionable-artifacts`: Each run produces aggregate and per-task details
  that show prompt, answer, judge result, command output, and likely cause.

### Blocker Checks

- [ ] `wrong-behavior`: The eval judges behavior other than the task or skill
  claim it is supposed to validate.
- [ ] `simulated-harness`: The runner uses a simulated answer path where a real
  harness run is required.
- [ ] `misleading-result`: The eval can produce a passing result that would not
  guide a real improvement decision.

### Improvement-Signal Checks

- [ ] `visible-delta`: Adding or changing the relevant skill/workflow would
  move a visible eval result.
- [ ] `workflow-compatible`: Individual skill checks and multi-skill workflow
  checks are possible without separate fixture formats.
- [ ] `failure-diagnostic`: Failures point to missing reference points, weak
  tool use, bad grounding, or poor output shape.

## Evidence Cues

- Task JSON files
- Judge prompt templates
- Runner script and command output
- `summary.json` and per-task run artifacts
- Eval onboarding and best-practice references

## Finding Cues

- Task JSON contains scoring rubric instead of reference points
- Runner uses a simulated answer path for a real harness eval
- Judge gives uncalibrated numeric scores
- Output has a pass rate but no per-task failure detail
- Fixture tests only toy prompts and misses the real skill/workflow behavior
