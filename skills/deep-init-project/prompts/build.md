# Build Prompt

Copy and paste this into a new session to start a build pass.

<!--
Keep this prompt execution-only.
High-frequency build actions stay here; rationale and policy stay in AGENTS.md and skills.
-->

---

0a. Read the active ticket in `@tickets/*.md`, preferring `status: building`.
0b. Read `@docs/MEMORY.md`, `@docs/TROUBLES.md`, and `@docs/LESSONS.md` if present.
0c. If UI is in scope, read `@docs/TASTE.md`.
0d. Search the code before assuming missing work.

Build rules:

<!--
This block is the build closeout loop:
finish implementation, validate it, write back into the ticket, then move board state.
-->

- complete one active ticket by default
- validate with the project backpressure commands: tests, lint, typecheck, build
- if the ticket changes user-visible behavior, delegate to `qa-tester`
- update the ticket with:
  - what changed
  - blockers
  - artifact links
  - user evidence
- update project records when applicable:
  - `docs/HISTORY.md`
  - `docs/MEMORY.md`
  - `docs/TROUBLES.md`
  - `docs/LESSONS.md`
- if new scope is discovered, create a linked follow-up ticket in `tickets/`
- if blocked by execution, keep `status: building` and record blockers
- if blocked by planning ambiguity, set `status: review`
- when implementation, QA, evidence, and human confirmation are complete, set `phase: documenting`, finish durable writeback, then archive/delete the ticket or set `status: done`
