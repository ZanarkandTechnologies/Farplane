# Judgement Questions For Skills

Judgement questions tell agents when a skill needs an `advise`-style decision
instead of a mechanical command.

## When To Add Them

Add 3-7 judgement questions when a skill regularly needs choices about:

- user segment or job-to-be-done
- metric or success signal
- guard metric or anti-metric
- scope boundary
- source credibility
- adoption versus rejection
- simplicity versus completeness

For external skill or repo imports, the default judgement question is:

- Should this external idea be adopted, adapted, rejected, or deferred for the
  stable local Codexter contract?

## Good Questions

Good questions are reusable and decision-shaped:

- Which metric best reflects the user's real goal?
- What guard prevents this metric from being gamed?
- Which source should set the standard for this workflow?
- Should this source be treated as a stable dependency or only as research
  input?
- What should be rejected even if it looks impressive?
- What is the smallest credible slice?

## Bad Questions

Avoid questions that are just hidden checklist items:

- Did you read the file?
- Did tests pass?
- Did you update docs?

Those belong in workflow or validation, not judgement.

## Output Shape

When a judgement question is used, record:

```text
Decision:
Options:
Recommended option:
Why it wins:
Tradeoff accepted:
Metric or evidence to revisit later:
```
