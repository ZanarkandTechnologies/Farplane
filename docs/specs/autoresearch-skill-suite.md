# Autoresearch Skill Suite

Date: 2026-05-03

## Goal

Add a Codexter-native measured-improvement workflow split into three skills:

- `autoresearch-plan`
- `autoresearch-exec`
- `self-improve`

The first two skills ship the v1 SLC: generic metric-driven planning and
execution. `self-improve` uses the same artifact contract for skills, with
binary eval pass rate as the metric.

## Product Context

Codexter already has a strong spec -> ticket -> plan -> implementation ->
review loop. It did not have a reusable way to repeatedly improve code, docs,
prompts, or skills against a mechanical metric while preserving run memory
across compaction and fresh sessions.

The ticket loop uses a `Proof Contract` as the bridge between measured
optimization and review judgment. Tickets carry metric handles, rubric gates,
and required evidence. `autoresearch` owns the metric experiment session only
when the ticket contract says repeated measured improvement is warranted.

The suite combines:

- Karpathy's `program.md` idea: the human programs the research org through a
  durable instruction artifact
- pi-autoresearch's artifact model: `autoresearch.md`, runner, JSONL log,
  checks, and ideas backlog
- Udit Goenka's planning gates: metric validation, guards, noise handling, and
  atomic iteration
- skill-improvement blog patterns: binary eval assertions before mutating skills

## JTBD

When an operator has a target and a metric, they want Codexter to set up and run
an autonomous improvement loop so measured gains can accumulate without manual
supervision of every experiment.

## User Groups And Use Modes

- **Optimization novices:** need metricable defaults, guard suggestions, and
  refusal of subjective keep/discard metrics before execution starts.
- **Power operators:** need a compact artifact contract they can edit directly,
  branch safely, and resume after compaction or handoff.
- **Skill authors:** need binary evals plus skill-local memory so repeated
  improvement passes learn from prior experiments.
- **Safety-sensitive repo owners:** need dirty-tree checks, off-limits scopes,
  secret hygiene, and reversible git behavior.
- **Long-running agents:** need JSONL history, ASI, plateau/noise notes, and
  enough context in files to continue without chat memory.

## Skill Boundaries

### `autoresearch-plan`

Owns setup:

- infer or ask for Goal, Scope, Metric, Direction, Verify, Guard, and Iterations
- screen dangerous Verify commands
- dry-run Verify and prove a numeric metric exists
- scaffold session artifacts
- hand off to `autoresearch-exec`
- when used from ticketed work, write or update the ticket `Proof Contract`
  with the metric name, direction, verify command, guard command, and session path

### `autoresearch-exec`

Owns execution:

- resume from session artifacts
- establish baseline
- make one atomic change per iteration
- commit before verification
- run metric and checks
- keep improved changes and revert failed changes
- append JSONL entries with useful ASI

### `self-improve`

Owns skill-specific optimization:

- inspect target skill maturity
- read or create target-skill `self-improve/program.md` when durable skill
  memory is desired
- define human rubric
- build binary eval cases
- baseline eval pass rate
- route measured execution through the autoresearch artifact contract
- debrief before/after behavior

## Non-Goals

- no full dashboard or Pi extension
- no broad subcommand family such as security/debug/ship
- no hidden dispatcher or recurring automation
- no subjective metric as the default keep/discard function
- no destructive rollback as the normal path

## Shared Artifact Contract

The canonical session files are:

```text
autoresearch.md
autoresearch.sh
autoresearch.checks.sh
autoresearch.jsonl
autoresearch.ideas.md
```

`autoresearch.sh` must emit:

```text
METRIC <metric_name>=<number>
```

`autoresearch.jsonl` starts with a config entry and appends one run entry for
each baseline, keep, discard, crash, check failure, metric error, or no-op.

For ticketed work, the ticket `Proof Contract` is the shared scoreboard:
metrics point to autoresearch sessions, rubrics point to `review`, and evidence
links prove both. The session files stay in the autoresearch artifact contract;
the ticket stores only the metric handle, commands, threshold, and session path.

## Skill-Local Memory Contract

For skill targets, `self-improve` can keep durable memory inside the target
skill package:

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

`program.md` is not a second usage contract. `SKILL.md` remains the live skill
surface. `program.md` is memory for future improvement runs: objective, eval
metric, rubric, experiment log, accepted learnings, rejected ideas, and next
hypotheses.

Scratch runs, bulky raw logs, sensitive transcripts, and unproven evals stay in
`experiments/self-improve/` until they are worth promoting.

Prompt-like skills can also use:

```text
self-improve/prompts/current.txt
self-improve/prompts/candidates/
self-improve/prompts/history/
self-improve/evals/assertions.py
self-improve/evals/runner.py
self-improve/results/latest_run.json
self-improve/results/scores.jsonl
self-improve/results/failure_analysis.md
```

## Implementation Plan Shape

- `Change:` add a reusable measured-improvement workflow split into planning,
  execution, and skill self-improvement.
- `Why:` Codexter needs an artifact-backed loop for "given a metric, keep
  improving."
- `Before -> After:` before, improvement loops were ad hoc; after, each run has
  a session spec, metric runner, JSONL memory, guard checks, and resumable loop.
- `Touch:` `skills/autoresearch-plan/`, `skills/autoresearch-exec/`,
  `skills/self-improve/`, and canonical docs inventory.
- `Signature delta:`
  - `autoresearch-plan / create_session(goal, scope, metric, verify, guard?): AutoresearchSession`
  - `autoresearch-plan / validate_metric(command): MetricValidation`
  - `autoresearch-exec / run_iteration(session): RunEntry`
  - `autoresearch-exec / decide(run, best, guard): KeepDiscardDecision`
  - `self-improve / build_eval_suite(skill_path, rubric): SkillEvalSuite`
  - `self-improve / score_candidate(candidate_skill, eval_suite): SkillScore`
- `Type Sketch:`
  - `AutoresearchSession { goal, scope, metricName, direction, verifyCommand, guardCommand?, maxIterations? }`
  - `RunEntry { run, commit, metric, status, description, asi, timestamp }`
  - `MetricValidation { command, exitCode, extractedValue, numeric, baseline }`
  - `SkillEvalCase { prompt, expectedBehavior, assertions[] }`
  - `SkillScore { passRate, failedAssertions[], notes }`

## Acceptance Criteria

- `autoresearch-plan` can infer or ask for session primitives and scaffold the
  session files.
- Verify dry-run must prove one numeric metric before execution starts.
- `autoresearch-exec` can establish a baseline, run bounded iterations, keep
  improved changes, revert/log failed changes, and distinguish guard failures
  from metric failures.
- JSONL entries preserve run number, commit, metric, status, description,
  timestamp, and ASI.
- `self-improve` defines binary eval-based skill optimization without requiring
  the generic v1 loop to depend on skill-specific logic.
- `self-improve` defines the optional target-skill `self-improve/program.md`
  memory format for durable skill experiments.

## Verification

Use:

- `python3 -m py_compile` for helper scripts
- script-level smoke tests for metric parsing and JSONL summary
- a temporary fixture run for `init_session.py`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/check_doc_parity.py`
- `python3 bin/check_harness_invariants.py`
