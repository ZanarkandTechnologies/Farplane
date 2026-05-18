# Blockers

Generic blocker log for multi-ticket or `batch-work` passes.

## Active

- none

## Notes

- Keep ticket-specific blockers in `tickets/TASK-*/ticket.md`.
- Use this file for cross-ticket blockers that should not stop the rest of a
  batch.

## Resolved / Avoided

- `TASK-0110`: Existing unrelated dirty files are present in the workspace. I
  kept the source-registry implementation on clean/new surfaces and did not
  sweep unrelated dirty work into the ticket slice.
- `TASK-0118`: The Symphony/Codexter train had stale active ticket state after
  implementation. I archived `TASK-0107` and `TASK-0110` through `TASK-0116`,
  repaired registry/template references to the archive paths, and left
  unrelated frontend/video/delegate dirty work untouched.
