# LLM Council Model

Use this reference when a deliberative-advice pass needs the council mechanics,
not only the simpler `advise` recommendation shape.

## Source Pattern

Karpathy's `llm-council` project is a local multi-model deliberation app. Its
core shape is:

1. Ask several models for independent first-pass responses.
2. Anonymize those responses and ask the models to evaluate or rank them.
3. Give a chairman model the first-pass responses and rankings so it can
   synthesize one final answer.
4. Keep intermediate responses, critique, rankings, and synthesis visible.

Primary source:

- https://github.com/karpathy/llm-council

Additional architecture summary:

- https://deepwiki.com/karpathy/llm-council/1-overview

## Farplane Adaptation

Farplane usually has specialized skills and subagents rather than a fixed pool
of external LLM providers. Adapt the council as a workflow pattern:

- `context packet`: write or identify one durable decision packet before
  spawning council lanes when prior discussion, options, evidence, or
  constraints matter
- `independent answers`: perspective briefs are collected before cross-reading
- `anonymized critique`: use neutral labels where feasible to reduce status,
  model, author, or role bias
- `ranking`: score argument quality against the decision criteria, not only
  popularity
- `chair synthesis`: one final owner chooses a path, preserves dissent, and
  states confidence
- `visible artifacts`: keep enough intermediate output to audit why the final
  answer won

## When To Use

Use council mechanics when one of these is true:

- the cost of a bad recommendation is high
- the decision affects multiple surfaces, teams, users, or future workflows
- there are credible opposing arguments
- the missing evidence could change the answer
- self-agreement or premature certainty is the main risk

Use plain `advise` when the decision is local, reversible, already grounded, or
only needs a concise 3-option recommendation.

## Council Context Packet

Use a context packet to prevent thin prompts from losing the real decision
frame.

```text
council_context_packet(decision, prior_discussion, evidence_refs, options)
  -> context_ref + lane_briefs
```

Default location:

```text
ticketed decision:
  tickets/TASK-XXXX/artifacts/subagents/<YYYYMMDD-HHMM>-council-context.md

non-ticket ephemeral decision:
  .farplane/context/<YYYYMMDD-HHMM>-<slug>-council-context.md

repo-worthy reusable decision:
  experiments/decisions/<YYYY-MM-DD>-<slug>/context.md
```

Default packet fields:

```text
Decision:
Why this matters:
Prior discussion summary:
Current behavior:
Expected behavior:
Options under consideration:
Known evidence:
Relevant files:
Constraints and non-goals:
Lane briefs:
Output shape:
Critique and ranking plan:
Proof or next owner:
```

Lane prompt template:

```text
Read context_ref: <path>.

Perspective:
Decision focus:
Criteria to apply:
Return:
- recommendation
- strongest opposing point
- evidence that would change your mind
- concrete implementation constraints

If the context_ref is missing or insufficient for this material judgment, say
so instead of guessing.
```

## Perspective Brief Shape

```text
Perspective:
Decision:
Criteria used:
Recommendation:
Strongest reason:
Biggest risk:
Evidence needed:
What would change my mind:
```

## Critique Shape

```text
Reviewer perspective:
Responses reviewed: A, B, C
Best argument:
Most dangerous assumption:
Ranking:
Missing evidence:
What the chair should preserve:
```
