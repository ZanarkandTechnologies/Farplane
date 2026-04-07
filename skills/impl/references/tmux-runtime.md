# Impl Tmux Runtime

The `impl` skill may use `scripts/tmux_helper.py` when the operator wants
visible worker lanes in tmux.

Rules:

- tmux helper is plumbing only
- `impl` owns worker selection and orchestration
- worker lanes should receive inline instructions to run one tracked skill on
  one ticket
- Stop-hook follow-ups may reuse the same tmux/session metadata, but the helper
  must not contain queue-selection or review policy

Typical commands:

```bash
python3 skills/impl/scripts/tmux_helper.py launch \
  --ticket tickets/TASK-1234-example.md \
  --phase building

python3 skills/impl/scripts/tmux_helper.py status

python3 skills/impl/scripts/tmux_helper.py followup \
  --ticket tickets/TASK-1234-example.md \
  --phase documenting \
  --reason "hook-driven continuation"
```
