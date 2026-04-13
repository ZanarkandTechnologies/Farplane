# Close Ticket Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `todos.md`

## Boundaries

- Keep this skill focused on end-of-ticket closeout, not fresh implementation.
- Keep `close-ticket` as the canonical live name.
- Keep `$docs-closeout` as compatibility-only wording in runtime-facing surfaces
  that still need to accept older prompts.
- Keep push/publish explicit; do not imply automatic external side effects.

## Conventions

- The parent flow should stay ordered: ticket writeback, durable docs, checks,
  commit prep, commit, optional push.
- Related skills should be linked from `todos.md` instead of re-embedding their
  full contracts.
- Closeout should return to build work when checks or review uncover a real
  same-ticket blocker.

## Checks

- Trigger conditions, workflow, guardrails, writeback, and result contract exist.
- `todos.md` is plain checklist text with Markdown links.
- The skill names commit and push as closeout steps without violating the repo's
  explicit-publish boundary.

## Testing

- Re-read `SKILL.md` once and confirm it is executable without opening other files.
- Compare the canonical name and alias wording against `bin/user_turn.py`,
  `bin/stop_hook.py`, and `skills/impl/scripts/tmux_helper.py` when the runtime
  control-skill contract changes.
