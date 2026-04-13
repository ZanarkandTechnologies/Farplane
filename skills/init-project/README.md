# Init Project

Bootstrap or migrate a project into the docs-first, ticket-first harness model.
This setup now also scaffolds optional `.githooks/` samples plus project-local
`scripts/pre_*_check.sh` files for local quality gates, without enabling them
automatically.

## Use Cases

- **Greenfield**: start a new repo with the full scaffold
- **Brownfield**: add the harness structure to an existing repo without rewriting the app

## Greenfield

Use the bootstrap script:

```bash
bash ~/.codex/skills/init-project/scripts/bootstrap.sh
```

That also writes `.githooks/README.md`, `.githooks/pre-commit`,
`.githooks/pre-push`, `scripts/pre_commit_check.sh`, and
`scripts/pre_push_check.sh` as opt-in samples. The recommended default is to
put lint, typecheck, and tests into `scripts/pre_push_check.sh`, then activate
only `pre-push` unless the repo wants an extra pre-commit gate.

Then follow the funnel:

```text
brainstorm -> deep-interview -> prd -> spec-to-ticket -> impl-plan -> impl
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

If you want optional local hooks after bootstrap:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-push
```

Leave `pre-commit` disabled unless the project explicitly wants the heavier
local gate on every commit.

If `coderabbit` is installed, the scaffolded `pre-push` hook will run it after
local validators. Override the review base branch if needed:

```bash
CODERABBIT_BASE_BRANCH=develop
```

### 2. Do not ticketize the whole backlog

Start with:

- one PRD/spec
- one real ticket
- one `impl-plan -> impl` cycle

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
- run `impl`

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
- [ ] one first `impl` run is successful
- [ ] repeated failures get logged to `docs/TROUBLES.md`
