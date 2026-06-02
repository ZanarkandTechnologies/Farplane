# Ralph Skill Maintenance

- Keep `$ralph` as a serial dispatcher over existing phase skills.
- Keep selector helpers read-only; they may report eligibility, but must not
  mutate tickets, create claims, launch agents, or manage worktrees.
- Keep parallel dispatch, external board adapters, leases, and merge policy out
  of this package until a later ticket explicitly opens that scope.
- Do not reintroduce `.ralph/`, `docs/progress.md`, `ralph_orchestrate.py`, or
  `ralph_worker.sh` as active surfaces.
