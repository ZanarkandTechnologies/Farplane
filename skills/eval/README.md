# Eval

Purpose: run Agent Skills comparisons through Promptfoo and retain the existing
harness-native path for project suites and behavior traces.

## Skill comparison

`evals/evals.json` remains the only authored behavior suite. The adapter creates
fresh candidate, baseline, and grader workspaces outside the checkout, generates
temporary Promptfoo JSON, runs the pinned packages through `npx`, and writes raw
plus normalized evidence under the selected runs directory.

First create this project's non-secret Codex profile, then run an owning skill's
manifest. The CLI defaults to the project-local Eval OS directory, so successful
runs appear in Farplane Office without copying artifacts.

```bash
farplane eval init
farplane eval promptfoo --skill <skill-name> --label <skill-name>-baseline --dry-run
farplane eval promptfoo --skill <skill-name> --label <skill-name>-baseline
```

`--skill` resolves `skills/<skill-name>/evals/evals.json`. Use `--eval-file` for
an explicit manifest, `--baseline-skill` to compare two versions, or
`--provider-profile` to use a non-default local profile. The default baseline is
the same fixture without the target skill installed.

The lower-level adapter remains available when a script needs direct control:

```bash
python3 skills/eval/scripts/run_promptfoo.py \
  --eval-file skills/<skill>/evals/evals.json \
  --provider-profile path/to/promptfoo-profile.json \
  --label candidate-vs-baseline
```

The profile owns shared provider settings and must set `enable_streaming: true`.
The adapter accepts stable string or integer IDs and one `expectations` or
`assertions` list. Promptfoo exit `100` is a completed comparison; the adapter
returns success only when every candidate row passes, irrespective of expected
baseline failures.

ChatGPT-login runs inherit the configured Codex home, including its harness
context. For repeated or CI runs, point profile `config.cli_env.CODEX_HOME` at
an already authenticated isolated home or use an API-key-backed environment.
The adapter deliberately does not copy credentials.

## Layout

```text
.farplane/evals/
├── run_evals.py
├── config.json
├── contexts/
│   └── agi-toy-shop.md
├── prompts/
│   ├── agent.md
│   └── judge.md
├── schemas/
│   └── behavior-report.schema.json
├── tasks/
│   ├── harness_tasks.json
│   └── agents_md_tasks.json
└── runs/
```

Codex and Claude runs use this same project-local sidecar; select the runner
with `--harness codex` or `--harness claude`.

Skill-specific eval tasks can also live beside the owning skill:

```text
skills/<skill-name>/evals/evals.json
```

Reusable global-prompt regressions live under
`skills/eval/examples/farplane-global-harness/`. The focused
`personality-concision-tasks.json` suite covers operator perspective,
framework-restraint guards, information-value compression, hard response
bands, and the safety/requested-detail exception.

## Example

```bash
python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .farplane/evals/run_evals.py run --harness codex --label baseline --limit 1
python3 .farplane/evals/run_evals.py run --harness codex --harness-evals --label harness-only
python3 .farplane/evals/run_evals.py run --harness codex --agents-md --label agents-md
python3 .farplane/evals/run_evals.py run --harness codex --skills --label skill-baseline
python3 .farplane/evals/run_evals.py run --harness codex --skill qa --label qa-skill
python3 .farplane/evals/run_evals.py run --harness codex --skill qa --compare-baseline --agent-profile farplane-eval-skill --baseline-agent-profile farplane-eval-base --label qa-compare
python3 .farplane/evals/run_evals.py run --harness codex --skill qa --behavior-trace --behavior-output-schema .farplane/evals/schemas/behavior-report.schema.json --max-parallel-tasks 1 --label qa-trace
python3 .farplane/evals/run_evals.py run --harness codex --tasks skills/eval/examples/farplane-global-harness/personality-concision-tasks.json --label personality-concision
python3 skills/eval/scripts/run_evals.py reliability path/to/run-1/summary.json path/to/run-2/summary.json --eval-file skills/qa/evals/evals.json --output path/to/reliability.json
```

No-scope `run` executes every known available family: harness tasks,
AGENTS.md/system-prompt tasks, and skill-local evals. Scope flags narrow the
run. File location defines the eval family; task JSON stays intentionally
small and does not carry `surface`, `target`, budget, or isolation fields.

`--compare-baseline` keeps existing skill-local eval JSON unchanged. The runner
uses native skill context, records whether the target skill triggered, and runs
the baseline profile only after the target skill triggers. For trigger-sensitive
cases, write natural user requests in `prompt`; do not name the skill unless the
case is explicitly testing direct invocation.

`--behavior-trace` adds the exact agent prompt, raw `events.jsonl`, stdout and
stderr, final output, command/usage summary, checkpoint score, artifact
inventory, and optional schema result to each task detail. It composes with
`--compare-baseline`. Use one worker so filesystem deltas are attributable.
Use Agent QA instead when the proof requires native-subagent-only roles or
Desktop tools rather than stable Codex CLI JSON events.

## Promotion reliability

Use `reliability` before promoting a material skill or prompt change from
stochastic eval evidence. Pass two or more explicit, unchanged-run
`summary.json` paths. The reducer fails closed when task IDs/titles, harness
metadata, trace mode, source task files, or recorded comparison metadata differ.

The report keeps three signals separate:

- `strict_grade`: tier-judge grades across every case and repetition
- `behavior`: behavior-trace pass/fail/blocked outcomes
- `exact_suite`: repetitions where every case received strict A

`stable_pass` requires strict A and behavior pass for every case in every
repetition. `unstable` means behavior remained passing but at least one strict
grade varied. Any behavior failure returns `fail`. The command exits `0` only
for `stable_pass`; `unstable` and `fail` exit `1`, while malformed or
incompatible inputs exit `2`.

New run summaries record profiles, prompt/task hashes, parallelism, output
schema, and extra arguments in `comparison_metadata`. Older summaries can
still be reduced when their recorded legacy fields match, but the report emits
`legacy_comparison_metadata_gap` because unrecorded model/budget equality is an
operator assertion rather than machine proof.

Optional `--eval-file` inspection identifies image/screenshot expectations
that have no image fixture. It separates intentional missing-evidence controls
from potential fixture/evaluator tension and never changes the promotion
verdict or rewrites eval truth.

For claims such as “the agent ran both validators,” add hidden
`metadata.farplane.behavior_requirements.required_successful_command_regexes`
to the eval row. Behavior trace matches those regexes only against completed
zero-exit commands and does not include them in the child or judge prompt.

Inspect project and framework runs in Farplane UI's first-class `Eval OS`
module. Core intentionally ships no second viewer; it owns the files under
`.farplane/evals`, while Farplane UI owns navigation, rendering, comparison,
history, and task drilldown.

## Test

```bash
python3 skills/eval/tests/test_run_evals.py
python3 skills/eval/tests/test_run_promptfoo.py
```
