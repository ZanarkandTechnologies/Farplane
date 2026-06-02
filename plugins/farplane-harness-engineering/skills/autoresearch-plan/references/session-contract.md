# Autoresearch Session Contract

This contract is shared by `autoresearch-plan`, `autoresearch-exec`, and
`self-improve`.

## Artifacts

| File | Purpose |
| --- | --- |
| `autoresearch.md` | Human and agent-readable session program. A fresh agent can resume from this file plus the JSONL log. |
| `autoresearch.sh` | Metric runner. It must emit `METRIC name=value` lines. |
| `autoresearch.checks.sh` | Optional guard runner for tests, type checks, lint, or other correctness gates. |
| `autoresearch.jsonl` | Append-only machine-readable run history. |
| `autoresearch.ideas.md` | Optional backlog of promising hypotheses not tried yet. |

## Session Location

Generic sessions usually live at the project root or in a named experiment
directory. Skill self-improvement sessions may live under:

```text
skills/<target-skill>/self-improve/runs/<YYYYMMDD-HHMM-slug>/
```

When a session is nested under a target skill, `self-improve/program.md` is the
durable memory for future skill improvement runs. The nested `autoresearch.*`
files are the run-specific log.

## `autoresearch.md` Shape

```markdown
# Autoresearch: <goal>

## Objective
<What is being optimized and why.>

## Metric
- Primary: <metric_name> (<unit>, lower|higher is better)
- Verify: `./autoresearch.sh`
- Guard: `./autoresearch.checks.sh` or none

## Scope
- Editable:
- Read-only:
- Off limits:

## Constraints
- Hard constraints and simplification preferences.

## What's Been Tried
- Baseline not yet run.

## Next Ideas
- First hypotheses to try.
```

Keep this file short and periodically update "What's Been Tried" so session
resume does not depend on transcript memory.

## Metric Output

`autoresearch.sh` output must include one primary line:

```text
METRIC <metric_name>=<number>
```

Secondary metrics use the same format:

```text
METRIC duration_s=12.3
METRIC bundle_kb=181.0
```

Metric names may contain letters, digits, underscores, dots, dashes, and `µ`.
Values must be finite decimal numbers. Units belong in the metric name or
session metadata, not in the value.

## JSONL Schema

The first line should be a config entry:

```json
{"type":"config","goal":"reduce type errors","metric_name":"type_errors","metric_unit":"","direction":"lower","scope":["src/**/*.ts"],"verify_command":"./autoresearch.sh","guard_command":"./autoresearch.checks.sh","max_iterations":10,"created_at":"2026-05-03T00:00:00Z"}
```

Each run entry should include:

```json
{"type":"run","run":1,"commit":"abc1234","metric":12.0,"metrics":{"type_errors":12.0},"status":"keep","description":"narrow generic type in parser","asi":{"hypothesis":"parser type inference is source of error cluster","learned":"one helper overload removed 3 errors","next_action_hint":"check formatter types next"},"timestamp":"2026-05-03T00:00:00Z"}
```

Valid statuses:

- `baseline`
- `keep`
- `discard`
- `crash`
- `checks_failed`
- `metric_error`
- `no_op`

## ASI

`asi` means Actionable Side Information. Record what future iterations need:

- `hypothesis`
- `learned`
- `failure_reason`
- `rollback_reason`
- `next_action_hint`
- `noise_note`

Descriptions say what changed. ASI says what was learned.

## Boundaries With Existing Farplane Skills

- Use `autoresearch-plan` and `autoresearch-exec` for local metric loops.
- Use `self-improve` when the target is a skill and the metric is an eval pass
  rate.
- Use `self-improve/references/skill-memory.md` for the optional target-skill
  `program.md` memory format.
- Use native `/goal` for evidence-based continuation without git experiment
  memory.
- Use `impl-plan` and `$impl` for ticketed work needing QA, review, and evidence
  lanes.
