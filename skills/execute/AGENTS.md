# Execute Maintenance

## Scope

- `SKILL.md`
- `SKILL.md` Todo List
- `README.md`
- `AGENTS.md`

## Boundaries

- Keep this as a Tier 2 interface, not a domain router.
- Do not move Farplane-specific implementation, QA-lane, or ticket-closeout
  details here.
- Domain skills should reference this interface from their `SKILL.md` Todo List when they
  implement generic execution.

## Checks

- The skill requires proof and durable writeback.
- `SKILL.md` Todo List links Tier 1 primitives using Markdown links.
- Examples do not imply `$impl` is universal outside coding.
