---
name: init-project
version: 2.8.0
description: "One-time setup workflow for new projects. Scaffold docs-first operating files, shared taste doctrine, flat ticket state with archival, and reusable plan/build prompts."
---

# Init Project Skill

One-time setup for new projects. This skill scaffolds a docs-first workflow and gives the project an explicit front-end funnel before execution starts.

## What This Sets Up

- `PROJECT_RULES.md` (project-specific stack + commands + conventions)
- `AGENTS.md` (operational contract loaded every loop)
- `ARCHITECTURE.md` (top-level system map for the repo)
- `docs/` state (`prd.md`, `specs/README.md`, `specs/`, `HISTORY.md`, `MEMORY.md`, `TASTE.md`, `TROUBLES.md`)
- `tickets/` state (`*.md`, `archive/`, `templates/`, optional `README.md`)
- optional `.githooks/` samples (`README.md`, `pre-commit`, `pre-push`) for
  local quality gates
- optional `scripts/pre_commit_check.sh` and `scripts/pre_push_check.sh`
  templates for repo-local validators
- discovery-to-execution funnel:
  - `brainstorm`
  - `deep-interview`
  - `prd`
  - `spec-to-ticket`
  - `impl-plan`
  - `impl`

## Common Stack Setup

### Convex + Next.js + Clerk (default)

```bash
pnpm create convex@latest . -- -t nextjs-clerk
```

- First `pnpm dlx convex@latest dev` cloud setup is interactive and must be run by a human.

### Plain Next.js

```bash
pnpm create next-app@latest . --ts --tailwind --eslint --app --src-dir
```

### Convex in an existing project

```bash
pnpm add convex
pnpm dlx convex@latest dev
```

## Bootstrap Workflow

### Fast path

```bash
bash ~/.codex/skills/init-project/scripts/bootstrap.sh
```

### Manual steps

1. Copy `references/PROJECT_RULES_TEMPLATE.md` -> `PROJECT_RULES.md`.
2. Copy `references/AGENTS_TEMPLATE.md` -> `AGENTS.md`.
3. Copy `references/ARCHITECTURE_TEMPLATE.md` -> `ARCHITECTURE.md`.
4. Create docs state:
   - `mkdir -p docs/specs`
   - copy `references/SPECS_README_TEMPLATE.md` -> `docs/specs/README.md`
   - `touch docs/prd.md docs/HISTORY.md docs/MEMORY.md docs/TASTE.md docs/TROUBLES.md`
5. Create tickets state:
   - `mkdir -p tickets tickets/archive tickets/templates`
   - copy the ticket template into `tickets/templates/`
6. Create optional git hook samples:
   - `mkdir -p .githooks`
   - copy the hook README and the sample `pre-commit` / `pre-push` scripts
   - do **not** activate them automatically
7. Create optional repo-local validation scripts:
   - `mkdir -p scripts`
   - copy `pre_commit_check.sh` and `pre_push_check.sh`
   - fill `pre_push_check.sh` with lint, typecheck, and test commands for the stack
8. If the idea is still open-ended, use `brainstorm`.
9. If the first slice is still too vague for a PRD, use `deep-interview`.
10. Use `prd` skill for requirements and PRD authoring (HITL loop).
11. Use `spec-to-ticket` skill to convert one SLC slice into raw tickets in `tickets/`.

### Existing-project migration

If the project already exists:

1. run the same bootstrap script in the repo root
2. do **not** convert the whole backlog
3. start with one PRD/spec and one ticket
4. prove one `impl-plan -> impl` cycle first

Migration guide:

- [README.md](README.md)

## Why This Structure

- `PROJECT_RULES.md` centralizes stack details and backpressure commands.
- `AGENTS.md` stays operational and lightweight because it is loaded every loop.
- `ARCHITECTURE.md` gives the repo one top-level system map instead of pushing all orientation into `README.md` or `AGENTS.md`.
- `docs/` is the canonical project state for planning and execution.
- `docs/TASTE.md` is the canonical visual doctrine, so tickets and QA can reference one shared style source.
- `docs/TROUBLES.md` is the append-only operator feedback log for repeated misses, failed attempts, and correction patterns that should feed future system improvements.
- `tickets/` is the canonical execution surface, so planning, build, and QA work from one file per active ticket, with completed tickets moved into `tickets/archive/`.
- `.githooks/` gives each repo one visible place for optional local gates
  without silently mutating git config during bootstrap.
- repo-local `scripts/pre_push_check.sh` keeps the actual validation contract in
  the project instead of burying lint/typecheck/test commands in the git hook.
- queue state should live in ticket frontmatter rather than folder lanes.
- `brainstorm` and `deep-interview` keep weak ideas from reaching tickets too early.
- Agents can find specs, plan, and validation commands without hunting through nested files.

## Planning Philosophy (Inherited Defaults)

The generated planning flow should follow these defaults:

- Context first before edits (specs, rules, related files, interfaces, memory state).
- Plan before build for feature/refactor work, with human confirmation before execution.
- Include a high-level change preview in plans (ASCII/mermaid + critical touchpoint stubs).
- Use conditional delegation only; avoid specialized QA delegation for docs-only/rule-text-only work.
- Add one debt/inefficiency insight for touched surfaces when planning implementation work.
- Keep prototype-first ramping explicit: 1 -> 10 -> 100, with dry-runs and checkpoints.

## Gotchas

- Do not hardcode stack specifics into `AGENTS.md`; put them in `PROJECT_RULES.md`.
- Keep progress notes out of `AGENTS.md`; put them in the active ticket file.
- Keep repeated failure feedback out of `docs/MEMORY.md`; log it in `docs/TROUBLES.md` first, then promote only durable lessons into `docs/MEMORY.md` or the relevant skill/contract.
- First Convex cloud setup is interactive; stop and ask the human to run it.
- Do not skip from a fuzzy idea directly to `prd`; use `brainstorm` or `deep-interview` first when the first slice is not obvious.
- Do not auto-enable the scaffolded git hooks; leave activation as an explicit
  `git config core.hooksPath .githooks` choice by the human.
- Put project-specific lint, typecheck, test, and build gates into
  `scripts/pre_push_check.sh`; treat CodeRabbit as optional after those local
  checks, not as the only pre-push gate.
- If the repo wants CodeRabbit in `pre-push`, call the standalone `coderabbit`
  CLI directly from the hook. Do not make the initialized project depend on a
  Codexter-owned global helper path.

## Prompt Templates (Copy/Paste Ready)

- [prompts/plan.md](prompts/plan.md) - Planning session prompt.
- [prompts/build.md](prompts/build.md) - Build session prompt.

## Templates (Load On Demand)

- [PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md) - Project rules template.
- [AGENTS_TEMPLATE.md](references/AGENTS_TEMPLATE.md) - AGENTS template.
- [ARCHITECTURE_TEMPLATE.md](references/ARCHITECTURE_TEMPLATE.md) - Architecture map template.
- [SPECS_README_TEMPLATE.md](references/SPECS_README_TEMPLATE.md) - Specs index template.
- [TASTE_TEMPLATE.md](references/TASTE_TEMPLATE.md) - Shared visual doctrine template.
- [GITHOOKS_README_TEMPLATE.md](references/GITHOOKS_README_TEMPLATE.md) - Optional local hook setup guide.
- [PRE_COMMIT_HOOK_TEMPLATE.sh](references/PRE_COMMIT_HOOK_TEMPLATE.sh) - Optional pre-commit sample.
- [PRE_PUSH_HOOK_TEMPLATE.sh](references/PRE_PUSH_HOOK_TEMPLATE.sh) - Optional pre-push sample.
- [PRE_COMMIT_CHECK_TEMPLATE.sh](references/PRE_COMMIT_CHECK_TEMPLATE.sh) - Repo-local pre-commit validator template.
- [PRE_PUSH_CHECK_TEMPLATE.sh](references/PRE_PUSH_CHECK_TEMPLATE.sh) - Repo-local pre-push validator template.
- `tickets/templates/ticket.md` - Filesystem ticket template.
