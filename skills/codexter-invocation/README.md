# Codexter Invocation

Use this skill when a normal Codex session receives a `CodexterRunEnvelope` and
needs to route one work item through the existing Codexter skills.

## Public Entrypoints

- `SKILL.md` - invocation workflow for Codex
- `templates/run-envelope.json` - minimal envelope shape for local or future
  Symphony callers
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

## How To Test

- `python3 -m unittest bin/test_codexter_invocation.py`
- `python3 -m py_compile bin/codexter_invocation.py`
