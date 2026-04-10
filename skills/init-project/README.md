# Init Project

Bootstrap or migrate a project into the docs-first, ticket-first harness model.

## Use Cases

- **Greenfield**: start a new repo with the full scaffold
- **Brownfield**: add the harness structure to an existing repo without rewriting the app

## Greenfield

Use the bootstrap script:

```bash
bash ~/.codex/skills/init-project/scripts/bootstrap.sh
```

Then follow the funnel:

```text
brainstorm -> deep-interview -> prd -> spec-to-ticket -> impl-plan -> ralph
```

## Brownfield Migration

If the repo already exists, do the smallest migration first.

### 1. Add the harness structure

```bash
mkdir -p docs/specs tickets tickets/archive tickets/templates
touch ARCHITECTURE.md docs/prd.md docs/HISTORY.md docs/MEMORY.md docs/TROUBLES.md docs/specs/README.md
```

Then copy in:

- `PROJECT_RULES.md`
- `AGENTS.md`
- `ARCHITECTURE.md`
- `docs/TASTE.md`
- `tickets/templates/ticket.md`

The bootstrap script can still help:

```bash
bash ~/.codex/skills/init-project/scripts/bootstrap.sh .
```

Use `--force` only if you want to overwrite files that already exist.

### 2. Do not ticketize the whole backlog

Start with:

- one PRD/spec
- one real ticket
- one `impl-plan -> ralph` cycle

Do not migrate every old issue into ticket files at once.

### 3. Front-end funnel first

For an existing repo:

- use `brainstorm` if you still need options
- use `deep-interview` if the first slice is unclear
- use `prd` once the first slice is coherent

Then:

- use `spec-to-ticket`
- set the chosen ticket to `status: review`
- run `impl-plan`
- set it to `status: building`
- run `ralph`

### 4. Keep migration scope small

The first migration slice should only prove:

- ticket structure works
- `Stop` hook works
- the project can produce one good ticket outcome

### 5. What not to migrate yet

Do not start with:

- full backlog conversion
- multi-ticket parallelism
- tmux worker farm
- cloud execution lanes

Those can come after one clean ticket run.

## Migration Checklist

- [ ] `PROJECT_RULES.md` exists
- [ ] `AGENTS.md` exists
- [ ] `ARCHITECTURE.md` exists
- [ ] `docs/prd.md`, `docs/specs/`, `docs/TROUBLES.md` exist
- [ ] `docs/specs/README.md` exists
- [ ] `tickets/` structure exists
- [ ] `tickets/archive/` exists for completed tickets
- [ ] one first ticket exists
- [ ] one first `impl-plan` run is successful
- [ ] one first `ralph` run is successful
- [ ] repeated failures get logged to `docs/TROUBLES.md`
