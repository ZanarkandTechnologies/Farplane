# Farplane Invocation

Use this skill when a normal Codex session receives a `FarplaneRunEnvelope` and
needs to route one work item through the existing Farplane skills.

## Public Entrypoints

- `SKILL.md` - invocation workflow for Codex
- `templates/run-envelope.json` - minimal envelope shape for local or future
  Symphony callers
- `templates/symphony-run-envelope.json` - file-envelope fixture for a future
  Symphony worker that launches normal Codex with Farplane installed
- `templates/codex-cloud-task-prompt.md` - prompt template for intentionally
  submitting one ticket to Codex Cloud
- `references/symphony.md` - responsibility split between Symphony and
  Farplane plus smoke command expectations
- `references/codex-cloud.md` - manual Codex Cloud handoff flow and
  review-before-apply guardrails
- `bin/farplane_invocation.py` - helper that validates workflow, ticket,
  compute, routing, and proof shape

## Minimal Example

```bash
python3 bin/farplane_invocation.py prepare \
  --ticket TASK-0107 \
  --phase planning \
  --proof .harness/results/task-0107-plan.proof.json
```

The helper prints a route such as `impl-plan`; Codex still performs the actual
skill invocation. The helper does not launch Codex.

## Symphony Shim

For future Symphony integration, use
`templates/symphony-run-envelope.json` as the request-file shape and
`references/symphony.md` as the ownership contract. Symphony owns polling,
claims, retries, workspaces, Codex launch, and tracker writeback. Farplane owns
the envelope, board normalization, compute admission, skill route, ticket
evidence, and `ProofPacket`.

## Codex Cloud Handoff

Use `references/codex-cloud.md` when a human explicitly decides to send one
ticket to Codex Cloud. Codex Cloud owns remote execution. Farplane owns the
prompt contract, local review, ticket evidence, and `ProofPacket` expectation.

Do not make Farplane submit, poll, or apply cloud tasks. Use `codex cloud diff`
for review before `codex cloud apply`.

## How To Test

- `python3 -m unittest bin/test_farplane_invocation.py`
- `python3 -m unittest bin/test_farplane_compute.py`
- `python3 -m py_compile bin/farplane_invocation.py`
