# Loop Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`

## Boundaries

- Keep `$loop` lightweight, same-session, and deterministic.
- Keep ticket orchestration, QA lanes, review packets, and tmux helpers out of
  the core `$loop` story.
- Keep the skill grounded in the shipped parser and stop-hook behavior.

## Conventions

- The prompt must include an explicit completion contract.
- Supported v1 predicates are only `completion_marker_seen`, `path_exists`, and
  `file_contains`.
- Stop wording should name explicit same-session stop commands.
- The skill should tell operators to hand off to `impl-plan` or `$impl` when
  work stops being a bounded local loop.

## Checks

- Trigger conditions, invocation shape, supported predicates, stop contract, and
  guardrails exist.
- Examples use the real parser surface: `$loop`, `done_when=`,
  `completion_marker=`, and `retry_message=`.
- No wording implies hidden background orchestration or ticket ownership.

## Testing

- Re-read `SKILL.md` once and confirm it is usable without opening runtime code.
- Compare examples against `bin/user_turn.py` and `bin/stop_hook.py` when the
  runtime contract changes.
