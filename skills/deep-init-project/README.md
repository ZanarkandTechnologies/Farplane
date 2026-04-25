# Deep Init Project

Bootstrap or migrate a project into the docs-first, ticket-first harness model.
This setup should start with a deep-interview-quality bootstrap intake, then
scaffold optional `.githooks/` samples plus project-local `scripts/pre_*_check.sh`
files for local quality gates, plus a repo-owned `qa/` cookbook surface for
agent-efficient verification guidance, without enabling hooks automatically.

## Use Cases

- **Greenfield**: start a new repo with the full scaffold
- **Brownfield**: add the harness structure to an existing repo without rewriting the app

## Greenfield

Use the bootstrap script:

```bash
bash ~/.codex/skills/deep-init-project/scripts/bootstrap.sh
```

Before finalizing the scaffold, run a bootstrap intake with the same discipline
as `deep-interview` and keep the answers in `docs/bootstrap-brief.md`.
That intake should explicitly answer whether local hooks should be enabled, what
belongs in `pre-push` or `pre-commit`, which heavy local checks such as
`desloppify` or `CodeRabbit` are desired, and whether a separate CI/deployment
gate exists.

That also writes `docs/bootstrap-brief.md`, `qa/README.md`,
`qa/cookbook/TEMPLATE.md`, `.githooks/README.md`,
`.githooks/pre-commit`, `.githooks/pre-push`, `scripts/pre_commit_check.sh`,
and `scripts/pre_push_check.sh` as opt-in samples. The recommended default is
to keep the large-file scan, fill in lint/typecheck/test/build commands, and
activate only `pre-push` unless the repo wants an extra pre-commit gate.

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
- `qa/`
- `tickets/templates/ticket.md`

The bootstrap script can still help:

```bash
bash ~/.codex/skills/deep-init-project/scripts/bootstrap.sh .
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
local validators and only when authenticated. Override the review base branch if
needed:

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
- use `deep-interview --bootstrap` if stack, topology, or quality-gate shape is
  still unclear
- use `deep-interview` if the first feature slice is unclear
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
- qa cookbook structure exists for future agent-facing shortcuts and probes
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

- [ ] `docs/bootstrap-brief.md` exists and captures stack/topology/gate decisions
- [ ] `docs/bootstrap-brief.md` captures local-hook, heavy-check, and CI/deploy-gate decisions
- [ ] `docs/bootstrap-brief.md` captures agent-experience/testability decisions
- [ ] `PROJECT_RULES.md` exists
- [ ] `AGENTS.md` exists
- [ ] `ARCHITECTURE.md` exists
- [ ] `docs/prd.md`, `docs/specs/`, `docs/TROUBLES.md` exist
- [ ] `qa/README.md` and `qa/cookbook/TEMPLATE.md` exist
- [ ] `docs/specs/README.md` exists
- [ ] `tickets/` structure exists
- [ ] `tickets/archive/` exists for completed tickets
- [ ] one first ticket exists
- [ ] one first `impl-plan` run is successful
- [ ] one first `impl` run is successful
- [ ] repeated failures get logged to `docs/TROUBLES.md`
