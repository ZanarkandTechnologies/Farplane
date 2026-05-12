# Codex Cloud Codexter Task Prompt

You are running in Codex Cloud. This workspace must have Codexter installed.
Use normal Codex plus the installed Codexter skills; do not launch another
daemon, scheduler, cloud task, or board listener.

## Task

Run exactly one Codexter work item from the envelope below.

## CodexterRunEnvelope

```json
{
  "workflowPath": "WORKFLOW.md",
  "workItemId": "TASK-0123",
  "workItemPath": null,
  "computeTarget": "local_shared",
  "phase": "building",
  "mode": "external_runner",
  "requestedBy": "codex-cloud",
  "requestedAt": "2026-05-06T00:00:00Z",
  "proofPacketPath": ".harness/results/task-0123-cloud.proof.json"
}
```

## Required Flow

1. Use `codexter-invocation` to validate the envelope.
2. Load the selected work item through the configured board adapter.
3. Respect compute blockers. Do not silently fall back to a different target.
4. Route to the selected Codexter phase skill.
5. Keep ticket evidence updated when the filesystem ticket exists.
6. Run the relevant tests or explain the blocker.
7. Write the requested `ProofPacket`.

## Return Evidence

Leave the remote diff, ticket evidence, review result, command summary, and
`ProofPacket` inspectable by the local operator.

Do not mark the ticket done unless the proof packet verdict is trustworthy and
the local review requirements are satisfied.
