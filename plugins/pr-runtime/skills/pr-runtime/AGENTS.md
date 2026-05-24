# PR Runtime Maintenance

## Scope

- `SKILL.md`
- `README.md`

## Boundaries

- Keep this skill about isolated checkout and ticket runtime procedure, not full
  GitHub review-thread handling or generic runtime orchestration.
- Keep the helper contract narrow: runtime record persistence, optional
  worktree creation, port reservation, explicit local runtime launch/stop, and
  QA target publication.
- Do not turn this skill into a second public execution surface beside `$impl`.

## Conventions

- Lead with when isolation is required, not with raw git commands.
- Keep runtime state under `.harness/state/`, not tracked repo files.
- Treat existing PR branch follow-up and multiple live writers as the primary
  triggers for isolated checkout use.

## Checks

- Trigger conditions, workflow, guardrails, and output contract exist.
- The skill says where runtime records live and how QA finds targets.
- The README shows the helper command surface and one minimal example.

## Testing

- Re-read `SKILL.md` once and confirm it works without opening extra refs.
- Confirm the helper commands named in the README exist.
- Confirm the skill still reads as a workflow contract, not a shell tutorial.
