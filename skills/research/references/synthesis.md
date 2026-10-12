---
title: Source Synthesis
owner: research
status: active
kind: workflow-reference
---

# Source Synthesis

Load for the `synthesis` branch in N5: several projects, repos, products, or
articles feed one target workflow, page, or skill. A single external source
mined for Farplane features belongs to `harness-scout`.

## Order

1. Name the target user, job, artifact to change, and local constraints.
2. Catalogue each source with type, credibility, recency, and relevance.
   Prefer maintained code, then official docs, then detailed write-ups;
   screenshots and marketing claims are weak signals.
3. Extract concrete features, workflows, guardrails, and failure modes, each
   with its evidence location.
4. Cluster overlapping features across sources before scoring. A pattern that
   several sources converge on outranks one impressive source.
5. If the success metric is fuzzy, get a metric card from `goal-advisor`
   (`references/metrics.md`)
   before scoring.
6. Score and decide each cluster.

## Scoring

Score each 1-5: `user-value`, `evidence-strength`, `transferability`,
`implementation-cost` (lower cost scores higher), `risk` (lower risk scores
higher), and `synergy` with the other adopted features.

- `adopt`: high value, strong evidence, good fit, low-to-medium cost.
- `adapt`: the principle is strong but the source's shape does not fit local
  conventions; import the principle only.
- `reject`: weak fit, weak evidence, high risk, or parity bait that does not
  serve the target job.
- `defer`: valuable but too large for the current slice. Use it instead of
  "maybe" when timing is the only reason.

External skills and repos are research inputs, not live dependencies: never
score "sync upstream" as `adopt`.

## Output

| Feature | Sources | Evidence | Scores | Decision | Reason |
| --- | --- | --- | --- | --- | --- |

Follow the table with the combined workflow, the tradeoff accepted, and the
next owner.
