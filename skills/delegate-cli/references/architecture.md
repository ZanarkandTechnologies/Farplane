# Delegate CLI Architecture

`delegate-cli` is a profile and adapter layer.

- `profile` says what work shape to run, which model to prefer, which skills to
  include, and which prompt template to render.
- `adapter` knows how to call one external CLI family.
- `skills/delegate-cli/scripts/delegate_cli_agent.py` owns deterministic setup, dry-run command
  rendering, prompt rendering, logs, and artifact copying.
- Farplane owns the ticket, QA, review, and integration result.

The bundled `frontend-pi-kimi` profile is a Pi/OpenRouter configuration, not a
public frontend workflow. Callers choose their bounded skill bundle with
`--skill`; future profiles should reuse the same launcher and artifact contract.
