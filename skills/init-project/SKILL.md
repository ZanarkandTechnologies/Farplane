---
name: init-project
version: 2.4.0
description: "One-time setup workflow for new projects. Scaffold docs-first operating files, shared taste doctrine, filesystem ticket board, and reusable plan/build prompts."
---

# Init Project Skill

One-time setup for new projects. This skill scaffolds a docs-first workflow and gives copy/paste prompts for planning and building sessions.

## What This Sets Up

- `PROJECT_RULES.md` (project-specific stack + commands + conventions)
- `AGENTS.md` (operational contract loaded every loop)
- `docs/` state (`prd.md`, `specs/`, `HISTORY.md`, `MEMORY.md`, `TASTE.md`, `TROUBLES.md`)
- `tickets/` board (`todo/`, `review/`, `building/`, `done/`, `templates/`, `INDEX.md`)

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
bash ~/.cursor/skills/init-project/scripts/bootstrap.sh
```

### Manual steps

1. Copy `references/PROJECT_RULES_TEMPLATE.md` -> `PROJECT_RULES.md`.
2. Copy `references/AGENTS_TEMPLATE.md` -> `AGENTS.md`.
3. Create docs state:
   - `mkdir -p docs/specs`
   - `touch docs/prd.md docs/HISTORY.md docs/MEMORY.md docs/TASTE.md docs/TROUBLES.md`
4. Create ticket board:
   - `mkdir -p tickets/todo tickets/review tickets/building tickets/done tickets/templates`
   - copy the ticket template into `tickets/templates/`
   - create `tickets/INDEX.md`
5. Use `prd` skill for requirements and PRD authoring (HITL loop).
6. Use `spec-to-ticket` skill to convert one SLC slice into raw tickets in `tickets/todo/`.

## Why This Structure

- `PROJECT_RULES.md` centralizes stack details and backpressure commands.
- `AGENTS.md` stays operational and lightweight because it is loaded every loop.
- `docs/` is the canonical project state for planning and execution.
- `docs/TASTE.md` is the canonical visual doctrine, so tickets and QA can reference one shared style source.
- `docs/TROUBLES.md` is the append-only operator feedback log for repeated misses, failed attempts, and correction patterns that should feed future system improvements.
- `tickets/` is the canonical execution board, so planning, build, and QA work from one file per ticket.
- `tickets/INDEX.md` gives one quick board view, but the ticket files remain canonical.
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

## Prompt Templates (Copy/Paste Ready)

- [prompts/plan.md](prompts/plan.md) - Planning session prompt.
- [prompts/build.md](prompts/build.md) - Build session prompt.

## Templates (Load On Demand)

- [PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md) - Project rules template.
- [AGENTS_TEMPLATE.md](references/AGENTS_TEMPLATE.md) - AGENTS template.
- [TASTE_TEMPLATE.md](references/TASTE_TEMPLATE.md) - Shared visual doctrine template.
- `tickets/templates/ticket.md` - Filesystem ticket template.
