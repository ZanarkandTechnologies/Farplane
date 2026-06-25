# Skill Eval Design

## Eval Philosophy

Self-improvement needs explicit assertions. Rubrics are useful for setup and
debrief; metric-advisor decides whether the honest provider is a mechanical
metric, eval result, review verdict, human feedback, hybrid signal, or
`none mechanical`.

Good evals answer: "Did this skill make the agent behave correctly on this
representative task?"

## Case Shape

Use JSONL for cases:

```json
{"id":"metric-card-setup","prompt":"Choose how to measure whether this skill's planning output got easier to approve","expected_behavior":["uses metric-advisor or an equivalent metric card","names provider and guard metrics","uses none mechanical when no command exists"],"assertions":["does not invent a fake numeric score","names review or human feedback when qualitative","does not start execution"]}
```

Store durable cases at `self-improve/evals/test_cases.jsonl`. Older
`cases.jsonl` files are acceptable for scratch runs, but new durable suites
should use `test_cases.jsonl`.

Fields:

- `id`
- `prompt` or `input`
- `expected_behavior`
- `assertions`
- optional `fixtures`
- optional `must_not`

## Assertion Types

Prefer assertions that can be checked with text, file, or command predicates:

- output contains required section
- output does not contain forbidden phrase
- expected file exists
- expected file contains text
- command exits 0
- JSON field equals value

Use a judge only as a secondary note, not the primary metric.

## Runner Contract

Prompt-like skill profiles should include:

```text
self-improve/evals/assertions.py
self-improve/evals/runner.py
self-improve/results/scores.jsonl
self-improve/results/latest_run.json
self-improve/results/failure_analysis.md
```

The runner consumes:

- `evals/test_cases.jsonl`: one test case per line
- `results/candidate_outputs.jsonl`: one candidate output per line with `id`
  and `output`
- `prompts/current.txt` or a candidate prompt path for metadata

The runner writes:

- `results/latest_run.json`: detailed case/assertion results
- `results/scores.jsonl`: append-only pass-rate history
- `results/failure_analysis.md`: failure themes and next hypothesis

## Baseline Before Mutation

Always run the eval suite before editing the target skill. Record:

- total cases
- passed assertions
- failed assertions
- failure themes
- suspected skill sections responsible

The first improvement hypothesis should target the largest failure theme.

When durable skill memory exists, also update
`self-improve/program.md` with:

- the baseline score
- the largest failure theme
- the first hypothesis
- any known rejected ideas from previous runs

## Anti-Overfitting Rules

- Use 3-5 cases only for smoke validation.
- Use 20-100 diverse cases before trusting durable or overnight optimization.
- Include one case outside the original user story.
- Include one "should not trigger" or boundary case when the skill trigger is
  broad.
- Add cases for failures discovered during real use.
- Do not make eval prompts copy the skill text.

## Debrief Shape

Use:

- `Before:` what failed in baseline
- `After:` what now passes
- `Example:` one concrete prompt that behaves better
- `Remaining risk:` where eval coverage is still thin
