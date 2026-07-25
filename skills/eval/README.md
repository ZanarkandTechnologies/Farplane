# Eval

Purpose: scaffold and run harness-native evals for Codex and Claude.

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

Inspect project and framework runs in Farplane UI's first-class `Eval OS`
module. Core intentionally ships no second viewer; it owns the files under
`.farplane/evals`, while Farplane UI owns navigation, rendering, comparison,
history, and task drilldown.

## Test

```bash
python3 skills/eval/tests/test_run_evals.py
```
