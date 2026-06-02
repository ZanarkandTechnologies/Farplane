# Eval Quality Review

Use this family when eval tasks, task fixtures, judge prompts, runner scripts,
artifact schemas, or eval onboarding guidance changed.

## TAS Guide

- `TAS-A`: eval tasks are realistic, reference points are clear text strings,
  judge rubrics are outside task JSON, execution uses the target harness, and
  artifacts make failures actionable.
- `TAS-B`: the eval is useful but has weak fixtures, vague reference points,
  overbroad judge instructions, thin failure analysis, or incomplete artifact
  traceability.
- `TAS-C`: the eval is misleading, promptfoo-shaped when the intended fixture is
  simpler, judges the wrong behavior, simulates the harness instead of running
  it, or produces results that cannot guide improvement.
- `TAS-D`: task fixtures, judge prompt, runner command, or output artifacts are
  missing enough that the eval cannot be judged.

## Dimensions

### Task Fixture Quality

- Does each task have a stable `id`, clear `title` or task name, user-facing
  prompt/query, and `reference_points` as plain strings?
- Are reference points expected observable outcomes rather than rubric policy?
- Are tags or notes useful without becoming the judge?

### Rubric Separation

- Is rubric policy in the judge prompt or review handoff rather than task JSON?
- Are TAS/boolean/tier judgments used instead of fake-precise 1-100 scoring?
- Are required pass conditions easy for another judge run to apply?

### Harness Fidelity

- Does the runner execute the user's real harness or agent CLI when validating
  behavior?
- Are command templates explicit for Codex, Claude, or custom harnesses?
- Are concurrency, labels, task limits, and temp-key friendliness handled?

### Artifact Usefulness

- Does each run produce aggregate and per-task details?
- Can a failed task show prompt, answer, judge result, command output, and
  likely cause?
- Is the summary useful enough to decide what to fix next?

### Improvement Signal

- Would adding or changing a skill/workflow move a visible eval result?
- Are individual skill checks and multi-skill workflow checks both possible
  without separate fixture formats?
- Do failures point to missing reference points, weak tool use, bad grounding,
  or poor output shape?

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
