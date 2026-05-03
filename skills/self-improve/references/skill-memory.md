# Skill-Local Self-Improve Memory

Use skill-local memory when experiments teach reusable lessons about a target
skill. This is the Codexter version of Karpathy's `program.md` pattern: the
target skill carries a small durable program for future self-improvement runs.

## When To Store Inside The Skill

Store inside `skills/<target-skill>/self-improve/` when:

- the target is a Codex skill package
- the evals are reusable across future runs
- the lessons change how future agents should improve the skill
- the operator wants the skill to accumulate memory over time

Keep artifacts in `experiments/self-improve/` when:

- logs are bulky or one-off
- outputs may contain secrets, transcripts, customer data, or local paths that
  should not ship with the skill
- the eval suite has not caught a real failure yet
- the run is scratch research rather than durable skill development

## Directory Contract

```text
skills/<target-skill>/self-improve/
  program.md
  evals/test_cases.jsonl
  evals/assertions.md
  runs/<YYYYMMDD-HHMM-slug>/
    autoresearch.md
    autoresearch.sh
    autoresearch.jsonl
    scores.jsonl
    notes.md
```

The target skill's live behavior remains in `SKILL.md`, references, scripts, and
templates. The `self-improve/` directory is memory and eval infrastructure for
future improvement passes.

## Prompt-Like Skill Profile

Use this profile when the editable skill surface behaves like a prompt or
instruction program and variants need clean comparison:

```text
skills/<target-skill>/self-improve/
  prompts/current.txt
  prompts/candidates/
  prompts/history/
  evals/test_cases.jsonl
  evals/assertions.py
  evals/runner.py
  results/scores.jsonl
  results/latest_run.json
  results/failure_analysis.md
```

Rules:

- `prompts/current.txt` mirrors the active prompt-like instruction surface.
- `prompts/candidates/` stores variants under evaluation.
- `prompts/history/` stores promoted or rejected variants with score-bearing
  filenames such as `20260503-pass-083-summary.md`.
- `results/latest_run.json` is the first file an agent reads after a failed or
  partial eval run.
- `results/failure_analysis.md` captures failure themes and the next hypothesis.

## `program.md` Template

```markdown
# Self-Improve Program: <skill-name>

## Objective
<What this skill should become better at.>

## Current Contract
- Trigger:
- First-load workflow:
- Outcome:
- Validation:

## Eval Metric
- Primary: `skill_eval_pass_rate`
- Direction: higher
- Minimum meaningful delta:
- Simplicity guard:

## Rubric
- <quality dimension 1>
- <quality dimension 2>
- <quality dimension 3>

## Durable Evals
- `evals/test_cases.jsonl`
- `evals/assertions.md`

## Experiment Log
| Date | Run | Hypothesis | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- |

## Accepted Learnings
- <Reusable rule future agents should preserve.>

## Rejected Ideas
- <Idea and why it failed, so future runs do not repeat it.>

## Next Hypotheses
- <Small experiment to try next.>
```

Keep `program.md` compact. It should guide the next agent, not archive every
raw observation.

## Run Folder Rules

Each run folder gets its own autoresearch session files. Keep:

- `autoresearch.md` for the run-specific goal and scope
- `autoresearch.jsonl` for machine-readable run history
- `scores.jsonl` for eval-level pass/fail details
- `notes.md` for a short before/after debrief

After a run, copy only the durable lessons back into `program.md`.

## Promotion Rules

Promote evals when they:

- represent realistic operator prompts
- would catch a known regression
- can be checked mechanically
- are not tailored to one candidate answer

Promote lessons when they:

- change future hypotheses
- clarify a boundary or trigger
- prevent repeated failed edits
- explain why a tempting change was rejected

Do not promote raw LLM transcripts, large logs, secrets, or purely subjective
notes into the skill package.
