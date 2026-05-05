# Handoff: Symphony-Compatible Codexter Invocation Contract

Date: 2026-05-05

## Adopt/Adapt Items

1. `WORKFLOW.md` control tower.
2. `WorkItem` and `BoardAdapter` contracts.
3. `ComputeSelector` and ticket-level compute override.
4. External `CodexterRunEnvelope` invocation contract.
5. `ProofPacket` output that external runners can parse.

## Implementation Handoff

Create a spec-level system design first:

- `docs/specs/symphony-compatible-codexter-runner.md`

Then ticket the first slice:

- filesystem adapter only,
- local Codex invocation only,
- no daemon,
- no Linear adapter,
- no background polling,
- no parallel queue.

## First Slice Acceptance

- A local Codex session can run one filesystem ticket through the existing
  Codexter skill route.
- The envelope can carry `computeTarget: "local_shared" | "local_worktree"`.
- The run writes a machine-readable `ProofPacket`.
- The same input/output contract is suitable for a future Symphony worker.
