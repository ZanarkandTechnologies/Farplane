# Delegate CLI Architecture

`delegate-cli` is a profile and adapter layer.

- `profile` says what work shape to run, which model to prefer, which skills to
  include, and which prompt template to render.
- `adapter` knows how to call one external CLI family.
- `bin/delegate_cli_agent.py` owns deterministic setup, dry-run command
  rendering, prompt rendering, logs, and artifact copying.
- Codexter owns the ticket, QA, review, and integration result.

The first profile is `frontend-pi-kimi`. Future profiles should reuse the same
launcher and artifact contract.
