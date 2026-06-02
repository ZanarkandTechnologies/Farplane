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
- `docs/bootstrap-brief.md` and its project profile when present
- Existing `docs/specs/*` (if any)
- Existing product constraints (if any)

### Outputs

- `docs/prd.md` (recommended for product work)
- Updated/created `docs/specs/*.md` with acceptance criteria

### PRD checklist (must be answerable)

- **First-principles basis**: objective, need, root cause, assumptions,
  constraints, first viable slice, proof/falsification, tradeoffs, and
  non-goals.
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
3. What is the **root cause** or underlying constraint creating this need?
4. What assumptions must be true for the chosen path to work?
5. What is the **first SLC slice** we should ship (small but valuable)?
6. What proof would validate or falsify the riskiest assumption?
7. What are the **non-goals** for this slice (things we will not build yet)?
8. What are the **inputs/outputs** (data shape, integrations, external services)?
9. What are the **must-have flows** (happy path steps) and the top **2-3 edge cases**?
10. What are the **failure modes** we must handle (auth, network, rate limits, payments, retries)?
11. What are the **constraints** (privacy/security, latency, offline, accessibility, budgets)?
12. What are the **success metrics** or acceptance tests (what will make you say "ship it")?
13. What existing system constraints do we inherit (stack, hosting, auth, conventions)?
14. What is the **rollout** expectation (internal only, beta, public; migration/backfill)?
15. What are you most worried we'll get wrong?
16. If a project profile exists, which component axes need divergent options
    before we choose a complete direction?
17. What smallest PoC would prove the riskiest assumption before full
    production ticketing?

### Writing `docs/prd.md` (recommended structure)

- **Problem / context**
- **First-principles basis**
- **Audience**
- **JTBD**
- **SLC slice (next release)**
- **Project profile / component matrix / explored options** when present
- **Prototype or PoC gates** when a risky assumption should be tested early
- **Non-goals**
- **Acceptance criteria (high level)**
- **Constraints**
- **Risks / unknowns**
- **Backpressure / evidence to ship**

### Acceptance criteria rules

- Specify **observable outcomes**, not implementation details.
- Include: happy path, error handling, and one performance/UX constraint where relevant.
