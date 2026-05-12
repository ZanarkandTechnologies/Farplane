# Scorecard: Symphony-Compatible Codexter

Date: 2026-05-05

Scores are manual 1-10 estimates for whether each source idea should influence
Codexter now.

| Idea | Value | Codexter fit | Implementation cost | Risk | Confidence | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `WORKFLOW.md` as invocation control tower | 9 | 9 | 5 | 4 | 8 | adapt now |
| `WorkItem` / board adapter | 9 | 9 | 6 | 4 | 8 | adapt now |
| `CodexterRunEnvelope` external invocation contract | 10 | 10 | 7 | 5 | 8 | adopt now |
| `ProofPacket` output schema | 9 | 10 | 5 | 3 | 8 | adopt now |
| Symphony-style retry/reconciliation | 7 | 6 | 7 | 6 | 6 | defer until invocation contract exists |
| Linear adapter | 8 | 7 | 7 | 5 | 6 | defer until filesystem adapter proves contract |
| Full daemon | 6 | 5 | 9 | 8 | 6 | reject for first slice |

## Anti-Metrics

Do not optimize for:

- number of remote runners supported before local contract works;
- number of board adapters before filesystem adapter proves the model;
- amount of copied Symphony behavior;
- background autonomy without proof packet parseability.

## Winning Metric

The first strong proof is:

> A future Symphony worker could launch Codex with the same
> `CodexterRunEnvelope` a local operator relies on, and parse the resulting
> `ProofPacket` without reading the transcript.
