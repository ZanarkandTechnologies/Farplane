# Metric Discovery

Use this when the user wants optimization but the metric is unknown.

## Metric Card

```text
Target user:
Job-to-be-done:
Artifact being improved:
Primary behavior to improve:
Primary metric:
Direction:
Guard metric:
Anti-metric:
Minimum meaningful delta:
Measurement method:
Judgement questions:
```

## Candidate Metric Types

- Mechanical numeric: errors, latency, size, cost, pass count, coverage.
- Binary eval pass rate: prompt, skill, workflow, or agent behavior cases.
- Evidence completeness: required proof artifacts present and fresh.
- Human judgement: only when quality is real but not mechanically measurable.
  Use `advise` and capture the judgement questions.

## Metric Selection Questions

Ask or infer:

- What user-visible behavior should get better?
- What failure would prove the workflow is worse even if the primary metric
  improves?
- Can a command, script, or binary eval produce the number?
- How noisy is the measurement?
- What minimum delta is worth keeping?
- What anti-metric prevents gaming?

## Recommendation Rule

Prefer the most mechanical metric that still represents the user's real goal.
When no mechanical metric is good enough, use binary evals. When even binary
evals are insufficient, use an explicit judgement call and log why.
