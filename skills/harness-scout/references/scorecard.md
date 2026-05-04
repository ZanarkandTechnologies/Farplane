# Manual Benchmark Scorecard

Use this before building async benchmark infrastructure.

## Comparison Modes

- `missing-feature`: Codexter has no meaningful local match. The scorecard can
  be lighter; focus on source credibility, local fit, cost, and risk before
  opening an `impl-plan` handoff.
- `competing-implementation`: Codexter already has a local version and the
  source claims a better approach. Pick one small representative task and
  compare `current-codexter`, `source-proposed`, and `best-of-worlds` before
  recommending replacement or expansion.

Compare three variants on one small task:

1. `current-codexter`: use the existing Codexter workflow.
2. `source-proposed`: emulate the external source's proposed technique as
   instructions or a manual process, without changing repo contracts.
3. `best-of-worlds`: combine the source idea with Codexter conventions.

## Dimensions

Score each dimension `1-10`.

- `task-completion`: did the variant finish the task?
- `evidence-quality`: can a reviewer trust the proof?
- `operator-trust`: would the operator understand what happened and why?
- `autonomy-resume-quality`: does the variant survive handoff or compaction?
- `overhead-cost`: lower time, token, and file churn scores higher.
- `maintainability`: does the result fit Codexter's docs/tickets/skills split?

## Required Output

```text
Task:
Variants:
Scores:
Winner:
Confidence:
Anti-metrics:
Notes:
```

## Anti-Metrics

Record when a variant wins by cheating:

- hides state in transcript instead of visible artifacts
- produces weak evidence
- creates duplicate features or tickets
- requires unapproved background agents
- optimizes score at the cost of maintainability

The scorecard is a judgment aid, not a scientific benchmark.
