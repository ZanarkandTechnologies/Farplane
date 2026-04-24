---
name: init-project
version: 2.9.0
description: "One-time setup workflow for new projects. Use a deep-interview-quality bootstrap intake, then scaffold docs-first operating files, visible quality gates, and reusable plan/build prompts."
---

# Init Project Skill

One-time setup for new projects. This skill should not feel like a shallow
scaffold dump. Start with a deep-interview-quality bootstrap intake, capture a
visible `docs/bootstrap-brief.md`, then scaffold a docs-first workflow and the
project's initial quality gates.

## What This Sets Up

- `PROJECT_RULES.md` (project-specific stack + commands + conventions)
- `AGENTS.md` (operational contract loaded every loop)
- `ARCHITECTURE.md` (top-level system map for the repo)
- `docs/` state (`bootstrap-brief.md`, `prd.md`, `specs/README.md`, `specs/`, `HISTORY.md`, `MEMORY.md`, `TASTE.md`, `TROUBLES.md`)
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

### Intake first

Before scaffolding decisions harden, run a bootstrap intake with the same
quality bar as `deep-interview`.

Recommended contract:

```text
deep-interview --bootstrap "<repo idea or migration target>"
```

Keep the clarified answers in `docs/bootstrap-brief.md`. That brief is the
bootstrap source of truth for:

- project goal and audience
- recommended topology (`single app` vs `monorepo` / `microservices`)
- stack choices and defaults
- required local validators (`lint`, `typecheck`, `test`, optional `build`)
- optional heavy gates (`desloppify`, `CodeRabbit`)
- large-file policy (`500` warn, `1000` block by default)
- shared utility placement convention
- decision boundaries for what the scaffold may choose automatically

### Fast path

```bash
bash ~/.codex/skills/init-project/scripts/bootstrap.sh
```

The bootstrap script writes the visible brief template plus the scaffold files.
It does not auto-enable git hooks or guess final validator commands for the
repo.

### Manual steps

1. Run a deep-interview-quality bootstrap intake and write the answers into
   `docs/bootstrap-brief.md`.
2. Copy `references/PROJECT_RULES_TEMPLATE.md` -> `PROJECT_RULES.md`.
3. Copy `references/AGENTS_TEMPLATE.md` -> `AGENTS.md`.
4. Copy `references/ARCHITECTURE_TEMPLATE.md` -> `ARCHITECTURE.md`.
5. Create docs state:
   - `mkdir -p docs/specs`
   - copy `references/BOOTSTRAP_BRIEF_TEMPLATE.md` -> `docs/bootstrap-brief.md`
   - copy `references/SPECS_README_TEMPLATE.md` -> `docs/specs/README.md`
   - `touch docs/prd.md docs/HISTORY.md docs/MEMORY.md docs/TASTE.md docs/TROUBLES.md`
6. Create tickets state:
   - `mkdir -p tickets tickets/archive tickets/templates`
   - copy the ticket template into `tickets/templates/`
7. Create optional git hook samples:
   - `mkdir -p .githooks`
   - copy the hook README and the sample `pre-commit` / `pre-push` scripts
   - do **not** activate them automatically
8. Create optional repo-local validation scripts:
   - `mkdir -p scripts`
   - copy `pre_commit_check.sh` and `pre_push_check.sh`
   - keep the file-size scan as-is
   - fill the project commands for `lint`, `typecheck`, `test`, optional
     `build`, and optional `desloppify`
9. If the idea is still open-ended, use `brainstorm`.
10. If the first slice or bootstrap shape is still vague, use `deep-interview`.
11. Use `prd` skill for requirements and PRD authoring (HITL loop).
12. Use `spec-to-ticket` skill to convert one SLC slice into raw tickets in `tickets/`.

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
- `docs/bootstrap-brief.md` keeps bootstrap decisions on a visible project
  surface instead of burying them in chat.
- `docs/TASTE.md` is the canonical visual doctrine, so tickets and QA can reference one shared style source.
- `docs/TROUBLES.md` is the append-only operator feedback log for repeated misses, failed attempts, and correction patterns that should feed future system improvements.
- `tickets/` is the canonical execution surface, so planning, build, and QA work from one file per active ticket, with completed tickets moved into `tickets/archive/`.
- `.githooks/` gives each repo one visible place for optional local gates
  without silently mutating git config during bootstrap.
- repo-local `scripts/pre_push_check.sh` keeps the actual validation contract in
  the project instead of burying lint/typecheck/test commands in the git hook.
- queue state should live in ticket frontmatter rather than folder lanes.
- `brainstorm` and `deep-interview` keep weak ideas from reaching tickets too early.
- `deep-interview` owns the interview loop quality. `init-project` should reuse
  that discipline, not fork it into a second shallow intake.
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
- Put project-specific lint, typecheck, test, and optional build gates into
  `scripts/pre_push_check.sh`; keep the large-file scan intact and treat
  CodeRabbit as optional after those local checks, not as the only pre-push
  gate.
- The default large-file policy is `500` raw lines = warn, `1000` raw lines =
  block for tracked source files. Keep duplicate-helper or shared-utility
  heuristics advisory unless the project explicitly tightens them.
- If the repo wants CodeRabbit in `pre-push`, call the standalone `coderabbit`
  CLI directly from the hook. Do not make the initialized project depend on a
  Codexter-owned global helper path.
- Put the project's shared utility convention in `PROJECT_RULES.md` and keep
  `AGENTS.md` limited to the operational reminder to reuse/extract helpers.

## Prompt Templates (Copy/Paste Ready)

- [prompts/plan.md](prompts/plan.md) - Planning session prompt.
- [prompts/build.md](prompts/build.md) - Build session prompt.

## Templates (Load On Demand)

- [PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md) - Project rules template.
- [AGENTS_TEMPLATE.md](references/AGENTS_TEMPLATE.md) - AGENTS template.
- [ARCHITECTURE_TEMPLATE.md](references/ARCHITECTURE_TEMPLATE.md) - Architecture map template.
- [BOOTSTRAP_BRIEF_TEMPLATE.md](references/BOOTSTRAP_BRIEF_TEMPLATE.md) - Bootstrap intake brief template.
- [SPECS_README_TEMPLATE.md](references/SPECS_README_TEMPLATE.md) - Specs index template.
- [TASTE_TEMPLATE.md](references/TASTE_TEMPLATE.md) - Shared visual doctrine template.
- [GITHOOKS_README_TEMPLATE.md](references/GITHOOKS_README_TEMPLATE.md) - Optional local hook setup guide.
- [PRE_COMMIT_HOOK_TEMPLATE.sh](references/PRE_COMMIT_HOOK_TEMPLATE.sh) - Optional pre-commit sample.
- [PRE_PUSH_HOOK_TEMPLATE.sh](references/PRE_PUSH_HOOK_TEMPLATE.sh) - Optional pre-push sample.
- [PRE_COMMIT_CHECK_TEMPLATE.sh](references/PRE_COMMIT_CHECK_TEMPLATE.sh) - Repo-local pre-commit validator template.
- [PRE_PUSH_CHECK_TEMPLATE.sh](references/PRE_PUSH_CHECK_TEMPLATE.sh) - Repo-local pre-push validator template.
- `tickets/templates/ticket.md` - Filesystem ticket template.
