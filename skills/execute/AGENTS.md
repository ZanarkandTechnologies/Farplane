# Execute Maintenance

## Scope

- `SKILL.md`
- `todos.md`
- `README.md`
- `AGENTS.md`

## Boundaries

- Keep this as a Tier 2 interface, not a domain router.
- Do not move Codexter-specific implementation, QA-lane, or ticket-closeout
  details here.
- Domain skills should reference this interface from their `todos.md` when they
  implement generic execution.

## Checks

- The skill requires proof and durable writeback.
- `todos.md` links Tier 1 primitives using Markdown links.
- Examples do not imply `$impl` is universal outside coding.
