## Requirements Discovery (Audience + JTBD)

**One-liner**: Convert a fuzzy request into clear outcomes and acceptance criteria before writing specs or tickets.

### Hard rule (prevents "starts building")

- If `docs/prd.md` is missing or does not answer the checklist below, stop and ask questions. Do not write tickets. Do not build.

### Brainstorm-first rule (keeps the human engaged)

- Do a snappy brainstorm/interview first (no tools) before writing `docs/prd.md`.
- Default: 60-120 seconds of back-and-forth, 6-10 questions, and 2-3 options to pick from.
- Only after the user answers: write/update `docs/prd.md`.

### Inputs

- User request / context
- Existing `docs/specs/*` (if any)
- Existing product constraints (if any)

### Outputs

- `docs/prd.md` (recommended for product work)
- Updated/created `docs/specs/*.md` with acceptance criteria

### PRD checklist (must be answerable)

- **Audience**: Who is this for? Primary vs secondary users?
- **JTBD / outcome**: What are they trying to accomplish?
- **Scope**: What is in-scope for the next SLC slice?
- **Non-goals**: What is explicitly out of scope?
- **Success**: What does success look like (observable + measurable if possible)?
- **Constraints**: Security/privacy, performance/latency, platforms, budget/time, legal/compliance.
- **Risks**: Top 1-3 unknowns that could change the approach.
- **Backpressure**: What evidence is required to ship (tests, QA, perf checks, demos)?

### Interview prompts (ask these before writing specs/tickets)

Ask only what changes implementation decisions; default to 8-12 questions total:

1. Who is the **primary user** and what is their context (team, workflow, device)?
2. What is the **core JTBD** in one sentence? ("When ___, I want to ___, so I can ___.")
3. What is the **first SLC slice** we should ship (small but valuable)?
4. What are the **non-goals** for this slice (things we will not build yet)?
5. What are the **inputs/outputs** (data shape, integrations, external services)?
6. What are the **must-have flows** (happy path steps) and the top **2-3 edge cases**?
7. What are the **failure modes** we must handle (auth, network, rate limits, payments, retries)?
8. What are the **constraints** (privacy/security, latency, offline, accessibility, budgets)?
9. What are the **success metrics** or acceptance tests (what will make you say "ship it")?
10. What existing system constraints do we inherit (stack, hosting, auth, conventions)?
11. What is the **rollout** expectation (internal only, beta, public; migration/backfill)?
12. What are you most worried we'll get wrong?

### Writing `docs/prd.md` (recommended structure)

- **Problem / context**
- **Audience**
- **JTBD**
- **SLC slice (next release)**
- **Non-goals**
- **Acceptance criteria (high level)**
- **Constraints**
- **Risks / unknowns**
- **Backpressure / evidence to ship**

### Acceptance criteria rules

- Specify **observable outcomes**, not implementation details.
- Include: happy path, error handling, and one performance/UX constraint where relevant.
