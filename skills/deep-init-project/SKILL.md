---
name: deep-init-project
version: 3.0.0
description: "Turn a new-project intake into a Farplane project with docs, tickets, runtime commands, QA gates, harness config, and reusable planning/build prompts."
tier: 3
group: coding
source: local
---

# Deep Init Project Skill

## Context

One-time setup for new or migrated projects. Every initialized project is a
Farplane project by default: it gets tracked `farplane/` config, ignored
`.farplane/` runtime state, visible tickets, docs, QA guidance, and optional
app-stack scaffolding.

The skill's completion point is initialization, not product discovery. It may
create a starter planning ticket, but it should not try to finish product
discovery during init unless the user explicitly asks for that separate phase.

This skill also owns the place where reusable stack setup recipes live for
common repo types such as Convex, Next.js, Clerk, shadcn, and React apps. Keep
those recipes in this skill or its references; do not delete the code-repo
scaffolding branch while simplifying project initialization.

## Skill Signature

```text
deep_init_project(project_root?, project_idea?, repo_shape?, stack_profile?, force?)
  -> project_substrate
   + farplane_config
   + optional_code_scaffold?
   + ticket_system
   + qa_surface
   + runtime_contract
   + starter_prd_ticket
   + next_planning_handoff
state: reads(existing repo files, README/AGENTS/docs/tickets when present, bootstrap brief, project profile, operator context); writes AGENTS/PROJECT_RULES/ARCHITECTURE/docs/tickets/qa/farplane scaffolds, optional stack scaffold, and starter PRD ticket
gates: existing_files_preserved; spec_version_recorded; human_gates_named; secrets_not_written; no_hidden_automation; interactive_stack_steps_stop_for_human
routes: deep-interview | prd | spec-to-ticket | research:official-docs | research:code-patterns
fails: creates only code scaffolding with no Farplane project config; treats PRD authoring as required init completion; deletes stack setup recipes; overwrites existing project state silently
```

## Phase Boundary

This skill follows Tier 0 phases inline. Use external research only when a stack
command or framework convention may be stale. PRD authoring is a downstream
ticketed handoff, not the default init phase.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the init target.
  - [ ] Resolve `project_root`, greenfield vs brownfield state, `force?`, and
    whether the user wants only Farplane substrate or also code/app scaffolding.
  - [ ] Inspect existing README, AGENTS, docs, tickets, package files, and app
    structure before writing.
- [ ] 2. Select the project and stack profile.
  - [ ] Select or preserve the project profile from
    [project-profiles](./references/project-profiles.md).
  - [ ] Select a stack profile such as Convex + Next.js + Clerk, plain Next.js
    + shadcn, Convex in an existing app, React-only, or no code scaffold.
  - [ ] Use [research:official-docs](../research/SKILL.md#researchofficial-docs)
    when stack setup commands or framework conventions may be stale.
  - [ ] Use [research:code-patterns](../research/SKILL.md#researchcode-patterns)
    when peer or local repo scaffolding patterns should shape the code
    scaffold.
- [ ] 3. Initialize the Farplane project substrate.
  - [ ] Run or mirror `scripts/bootstrap.sh` to create tracked `farplane/`
    config, ignored `.farplane/` runtime state, `tickets/`, docs, QA, optional
    hooks, validation scripts, and review helper surfaces.
  - [ ] Ensure `farplane/manifest.json` records the Farplane project
    `spec_version` and surface list.
  - [ ] Preserve existing files unless `force == true` or explicit overwrite
    intent is present.
  - [ ] Keep `.farplane/` ignored runtime state and `farplane/` tracked project
    spec.
  - [ ] Do not auto-enable scaffolded git hooks.
- [ ] 4. Initialize the optional code scaffold.
  - [ ] Bind `code_scaffold(...)`; ask only for missing params needed to choose
    or skip the stack profile.
  - [ ] Run the selected stack command only when `include_code_scaffold == true`.
  - [ ] Stop for human action on interactive setup, credentials, billing,
    deploys, or cloud project creation.
  - [ ] Record canonical app-only and QA/evidence run commands in
    `PROJECT_RULES.md`, `docs/bootstrap-brief.md`, and the relevant `qa/`
    cookbook surface.
- [ ] 5. Create the starter planning handoff.
  - [ ] Create or preserve `tickets/TASK-0001/ticket.md` for drafting the
    initial PRD.
  - [ ] Leave `docs/prd.md` as a draft placeholder unless PRD work is
    explicitly requested now.
  - [ ] Route to the next planning skill after init; do not conduct the planning
    phase inside this skill.
- [ ] 6. Verify and finish init.
  - [ ] Run focused scaffold checks such as
    `python3 bin/validators/check_farplane_project_files.py` when available.
  - [ ] Confirm the expected `farplane/`, `.farplane/`, and `tickets/` surfaces
    exist.
  - [ ] Report the initialized stack profile, any skipped human-gated steps,
    the starter PRD ticket, and the next command or skill.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## What This Sets Up

- Farplane substrate: `farplane/manifest.json`, `farplane/README.md`,
  `farplane/*.md`, `.farplane/` runtime state, and `tickets/`.
- Project operating docs: `AGENTS.md`, `PROJECT_RULES.md`, `ARCHITECTURE.md`,
  `docs/bootstrap-brief.md`, `docs/prd.md`, `docs/specs/`, and memory logs.
- QA and proof surface: `qa/`, optional `.githooks/`, repo-local validation
  scripts, and optional local Codex SDK review-loop files.
- Starter handoff: `tickets/TASK-0001/ticket.md` for the post-init
  `deep-interview -> prd` phase.
- Optional code scaffold selected from the stack recipes below.

## Code Scaffold Recipes

```text
code_scaffold(project_root, stack_profile?, package_manager?, ui?, backend?,
              auth?, theme?, existing_app?, include_code_scaffold?)
  -> stack_command? + skipped_reason? + human_gates + runtime_command_notes
```

### Convex + Next.js + Clerk (default)

```bash
pnpm create convex@latest . -- -t nextjs-clerk
```

- First `pnpm dlx convex@latest dev` cloud setup is interactive and must be run by a human.

### Plain Next.js + shadcn UI baseline

```bash
pnpm create next-app@latest . --ts --tailwind --eslint --app --src-dir
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json
```

### Convex in an existing project

```bash
pnpm add convex
pnpm dlx convex@latest dev
```

## Reference Map

- [references/project-profiles.md](references/project-profiles.md) - load when
  selecting project type, components, advice axes, prototype gates, and
  downstream handoff.
- [references/project-lifecycle.md](references/project-lifecycle.md) - load
  when recording the bootstrap route and next lifecycle phase.
- [references/MANIFEST_TEMPLATE.json](references/MANIFEST_TEMPLATE.json) -
  copied to `farplane/manifest.json` for the Farplane project spec instance.
- [references/PRD_TICKET_TEMPLATE.md](references/PRD_TICKET_TEMPLATE.md) -
  copied to `tickets/TASK-0001/ticket.md` as the post-init PRD handoff.
- [references/PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md)
  - copied to `PROJECT_RULES.md` for project stack, runtime, and QA commands.
- [references/qa/](references/qa/) - copied when creating the QA cookbook
  surface.
- [../../docs/farplane-framework/project-files.md](../../docs/farplane-framework/project-files.md)
  - load when the user asks why a Farplane project has these files or how the
  spec should evolve.
- [README.md](README.md) - load only for skill-local manual bootstrap details.
- [prompts/plan.md](prompts/plan.md) and [prompts/build.md](prompts/build.md) -
  load only when the user asks for reusable planning/build prompts.
