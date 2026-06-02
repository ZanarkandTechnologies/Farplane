# Architecture

`delegate-frontend` is a Farplane orchestration skill, not a frontend framework.

- Farplane remains the owner of tickets, final QA, and completion claims.
- Pi/Kimi owns one bounded external-CLI phase at a time.
- `.harness/external-cli/profiles/frontend-pi-kimi` contains the mounted
  frontend, media, QA, and review skills.
- `.harness/external-cli/runs/<run-id>` contains prompts, command metadata,
  session logs, handoffs, and phase-owned outputs.

The skill should reduce direct unbounded frontend editing by turning vague UI
work into explicit `spec`, `assets`, `implementation`, `repair`, or
`visual-review` phases.
# Delegate Frontend Architecture

`delegate-frontend` is a profile entrypoint over `delegate-cli`.

It does not own a separate launcher or artifact contract. It selects
`frontend-pi-kimi` and keeps frontend-specific readiness checks close to the
frontend skill topology.
