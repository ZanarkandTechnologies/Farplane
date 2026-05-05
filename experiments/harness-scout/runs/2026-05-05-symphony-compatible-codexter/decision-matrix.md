# Decision Matrix: Symphony-Compatible Codexter

Date: 2026-05-05

Scoring: `1` weak fit, `5` strong fit.

| Candidate | Decision | Value | Fit | Cost | Risk | Rationale |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `WORKFLOW.md` control tower | adapt | 5 | 5 | 3 | 2 | Best way to make agents start from one clear policy surface without replacing skills. |
| `WorkItem` + `BoardAdapter` | adapt | 5 | 5 | 3 | 2 | Makes filesystem tickets, Linear, and future boards share one shape. |
| External `CodexterRunEnvelope` contract | adopt | 5 | 5 | 4 | 3 | This is the key to "Symphony runs Codexter" through normal Codex execution. |
| `ComputeSelector` | adopt | 5 | 5 | 3 | 3 | Core user requirement: decide where a ticket runs. |
| External execution adapter | adapt | 4 | 4 | 4 | 3 | Needed after local invocation works; keep the first slice focused on normal Codex. |
| Claim/lease registry | defer/adapt | 4 | 4 | 4 | 4 | Required for parallelism and external runners, but should follow the v1 invocation contract. |
| Retry/reconciliation loop | defer/adapt | 4 | 3 | 4 | 4 | Trust Symphony for this when remote; local v1 can stay explicit/conversation-driven. |
| HTTP dashboard | defer | 3 | 2 | 4 | 3 | Useful later, not part of the first integration seam. |
| Raw Linear adapter | defer | 4 | 3 | 4 | 3 | Good later; filesystem-first proves the contract first. |

## Decision

Implement Codexter's Symphony-compatible seam in this order:

1. `WORKFLOW.md` schema.
2. `WorkItem` and filesystem `BoardAdapter`.
3. `ComputeTarget` / `ComputeSelector`.
4. External `CodexterRunEnvelope` invocation contract.
5. `ProofPacket` output schema.
6. Local Codex invocation through existing skills.
7. Only then add claims, leases, parallel dispatch, and external adapters.

## Anti-Decision

Do not build a Symphony clone inside Codexter. Build the interface that lets
Symphony run Codexter.
