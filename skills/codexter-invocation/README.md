# Codexter Invocation

Use this skill when a normal Codex session receives a `CodexterRunEnvelope` and
needs to route one work item through the existing Codexter skills.

## Public Entrypoints

- `SKILL.md` - invocation workflow for Codex
- `templates/run-envelope.json` - minimal envelope shape for local or future
  Symphony callers
- `templates/symphony-run-envelope.json` - file-envelope fixture for a future
  Symphony worker that launches normal Codex with Codexter installed
- `references/symphony.md` - responsibility split between Symphony and
  Codexter plus smoke command expectations
- `bin/codexter_invocation.py` - helper that validates workflow, ticket,
  compute, routing, and proof shape

## Minimal Example

```bash
python3 bin/codexter_invocation.py prepare \
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
claims, retries, workspaces, Codex launch, and tracker writeback. Codexter owns
the envelope, board normalization, compute admission, skill route, ticket
evidence, and `ProofPacket`.

## How To Test

- `python3 -m unittest bin/test_codexter_invocation.py`
- `python3 -m py_compile bin/codexter_invocation.py`
