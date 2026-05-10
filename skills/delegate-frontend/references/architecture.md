# Architecture

`delegate-frontend` is a Codexter orchestration skill, not a frontend framework.

- Codexter remains the owner of tickets, final QA, and completion claims.
- Pi/Kimi owns one bounded external-CLI phase at a time.
- `.harness/external-cli/profiles/frontend-pi-kimi` contains the mounted
  frontend, media, QA, and review skills.
- `.harness/external-cli/runs/<run-id>` contains prompts, command metadata,
  session logs, handoffs, and phase-owned outputs.

The skill should reduce direct unbounded frontend editing by turning vague UI
work into explicit `spec`, `assets`, `implementation`, `repair`, or
`visual-review` phases.
