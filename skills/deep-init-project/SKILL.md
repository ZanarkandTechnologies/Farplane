---
name: deep-init-project
version: 3.0.0
description: "Turn a new-project intake into a Farplane project with docs, tickets, runtime commands, QA gates, harness config, and reusable planning/build prompts."
tier: 3
group: coding
source: local
workflow: true
eval: eval_task.json
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
common repo types such as Convex, Next.js, Clerk, shadcn, React apps, and
optional quality tooling. Keep those recipes in this skill or its references;
do not delete the code-repo scaffolding branch while simplifying project
initialization.

Reusable project automation prompt templates live in
[AUTOMATION_TEMPLATE.md](references/AUTOMATION_TEMPLATE.md). New projects use
the Farplane Framework's recurring loops: `pulse-update` for frequent bounded
action selection and explicit `interval-update` automations for daily or weekly
reporting and planning.
Generated project config should include `farplane/automations.md` as the
reviewable prompt source copied into Codex automations.

## Skill Signature

```text
deep_init_project(project_root?, project_idea?, repo_shape?, stack_profile?, init_mode?, force?)
  -> project_substrate
   + farplane_config
   + readiness_audit
   + goals_delta?
   + optional_code_scaffold?
   + ticket_system
   + qa_surface
   + runtime_contract
   + starter_prd_ticket
   + automation_setup_handoff?
   + next_planning_handoff
state: reads(existing repo files, README/AGENTS/docs/tickets when present, bootstrap brief, project profile, operator context); writes AGENTS/PROJECT_RULES/ARCHITECTURE/docs/tickets/qa/farplane scaffolds, optional stack scaffold, and starter PRD ticket
gates: existing_files_preserved; spec_version_recorded; human_gates_named; secrets_not_written; no_hidden_automation; interactive_stack_steps_stop_for_human
routes: horizon-advisor | goal-advisor | deep-interview | prd | spec-to-ticket | research:official-docs | research:code-patterns | automation-advisor
fails: creates only code scaffolding with no Farplane project config; treats PRD authoring as required init completion; claims full project initialization when goals, success criteria, non-goals, or decision boundaries are still missing; deletes stack setup recipes; overwrites existing project state silently
```

## Phase Boundary

This skill follows Tier 0 phases inline. Use external research only when a stack
command or framework convention may be stale. PRD authoring is a downstream
ticketed handoff, not the default init phase.

`init_mode` controls completion semantics:

- `substrate`: create or preserve the Farplane project files, write any missing
  readiness gaps into `docs/bootstrap-brief.md`, and report
  `substrate_complete`.
- `full`: after substrate setup, run a project-goals readiness pass. Ask the
  first missing operator-owned goal question when the North Star, 3-month
  outcome, success criteria, non-goals, or decision boundaries are absent.
  Update or propose a `farplane/goals.md` delta before handing executable
  milestones to `goal-advisor`.

Do not treat `farplane/goals.md` existing as proof that goal setup is complete.
If it is placeholder, stale, or not grounded in the operator's stated intent,
the result is `needs_goal_intake`, not `project_initialized`.

```text
setup_project_goals(bootstrap_brief, project_context, existing_goals?)
  -> readiness_status
   + first_missing_question?
   + goals_delta?
   + current_milestone_candidate?
   + goal_advisor_handoff?
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the init target.
  - [ ] Resolve `project_root`, greenfield vs brownfield state, `force?`, and
    whether the user wants only Farplane substrate or also code/app scaffolding.
  - [ ] Resolve `init_mode := substrate | full`; use `full` only when the
    operator wants project-goals setup during initialization.
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
  - [ ] Keep `farplane/automations.md` as the exact prompt source that calls
    generic skills in plain project-specific operational language.
  - [ ] Ensure `farplane/manifest.json` records the Farplane project
    `spec_version` and standard tracked/ignored paths.
  - [ ] Preserve existing files unless `force == true` or explicit overwrite
    intent is present.
  - [ ] Keep `.farplane/` ignored runtime state and `farplane/` tracked project
    spec.
  - [ ] Do not auto-enable scaffolded git hooks.
- [ ] 4. Run readiness audit and full-mode project-goals setup.
  - [ ] Audit `docs/bootstrap-brief.md`, `farplane/harness.md`,
    `farplane/goals.md`, `farplane/automations.md`, `farplane/bindings.md`,
    `farplane/pm.json`, `PROJECT_RULES.md`, and QA surfaces for missing,
    placeholder, stale, or disabled state.
  - [ ] Write the audit result into `docs/bootstrap-brief.md` under
    Goal Intake Status and Initialization Readiness when those sections exist.
  - [ ] In `substrate` mode, report missing goal/setup questions as next
    handoff rather than asking the full interview now.
  - [ ] In `full` mode, ask the first missing project-goals question before
    claiming `project_initialized`: "What should this project reliably do for
    you over the next 3 months that it does not yet do reliably today?"
  - [ ] Use `horizon-advisor` when project goals, KPI tree, value function, or
    current milestone need to be written or improved.
  - [ ] Use `goal-advisor` only after `farplane/goals.md` has a current
    milestone concrete enough to compile into a ticket-backed Goal Packet.
- [ ] 5. Initialize the optional code scaffold.
  - [ ] Bind `code_scaffold(...)`; ask only for missing params needed to choose
    or skip the stack profile.
  - [ ] Run the selected stack command only when `include_code_scaffold == true`.
  - [ ] Stop for human action on interactive setup, credentials, billing,
    deploys, or cloud project creation.
  - [ ] Record canonical app-only and QA/evidence run commands in
    `PROJECT_RULES.md`, `docs/bootstrap-brief.md`, and the relevant `qa/`
    cookbook surface.
  - [ ] Record optional maintainability and hardening commands in
    `PROJECT_RULES.md` when the stack already has or explicitly adopts tools
    such as ESLint/Oxlint, Ruff/Radon, Semgrep, CodeQL, SonarQube, jscpd,
    dependency-cruiser/Madge, Knip/depcheck, dependency audit, or secret scan.
    Do not install these tools automatically unless setup scope explicitly
    includes code scaffold/tooling installation.
- [ ] 6. Create the starter planning handoff.
  - [ ] Create or preserve `tickets/TASK-0001/ticket.md` for drafting the
    initial PRD.
  - [ ] Leave `docs/prd.md` as a draft placeholder unless PRD work is
    explicitly requested now.
  - [ ] Route to the next planning skill after init; do not conduct the planning
    phase inside this skill.
- [ ] 7. Prepare automation activation.
  - [ ] Create `farplane/pm.json` as UI grouping glue with `threads.chats` and
        `threads.automations`.
  - [ ] Do not create live threads or automations unless the operator asked for
        live automation activation.
  - [ ] When live activation is requested, call `automation-advisor` after the
        substrate exists so it can create or update the Codex loops named in
        `farplane/automations.md`, commonly Pulse, Daily Interval, and Weekly
        Interval.
  - [ ] Record PM-visible thread IDs in `farplane/pm.json`; do not store
        automation runtime IDs there.
  - [ ] If activation is skipped or unavailable, report
        `needs_automation_setup` with the exact next owner:
        `automation-advisor`.
- [ ] 8. Verify and finish init.
  - [ ] Run focused scaffold checks such as
    `python3 bin/validators/check_farplane_project_files.py` when available.
  - [ ] Confirm the expected `farplane/`, `.farplane/`, and `tickets/` surfaces
    exist.
  - [ ] Report `substrate_complete`, `needs_goal_intake`, `needs_runtime_setup`,
    `needs_automation_setup`, or `project_initialized`; do not collapse these
    into a generic "done".
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
- Automation setup handoff: `automation-advisor` creates or updates the live
  Codex loops only when activation is requested.
- Full-mode project-goals setup: goal-intake readiness in
  `docs/bootstrap-brief.md`, a proposed or applied `farplane/goals.md` delta,
  a `horizon-advisor` pass when strategy needs shaping, and a `goal-advisor`
  handoff only after the current milestone is concrete.
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

### Optional Quality Tooling Slots

Record adopted commands in `PROJECT_RULES.md`; install only when the operator
or selected stack setup explicitly includes those tools.

- JavaScript / TypeScript: ESLint or Oxlint, TypeScript checks, jscpd,
  dependency-cruiser or Madge, Knip or depcheck, Semgrep, CodeQL, SonarQube, and
  dependency audit commands.
- Python: Ruff, Radon, mypy or pyright, vulture, pip-audit or uv audit,
  Semgrep, CodeQL, SonarQube, and mutation testing only for high-budget proof.
- Cross-stack hardening: secret scanning, config validation, dependency audit,
  and resilience/failure tests when the project owns the relevant runtime.

## Reference Map

- [references/project-profiles.md](references/project-profiles.md) - load when
  selecting project type, components, advice axes, prototype gates, and
  downstream handoff.
- [references/project-lifecycle.md](references/project-lifecycle.md) - load
  when recording the bootstrap route and next lifecycle phase.
- [references/MANIFEST_TEMPLATE.json](references/MANIFEST_TEMPLATE.json) -
  copied to `farplane/manifest.json` for the Farplane project spec instance.
- [references/AUTOMATION_TEMPLATE.md](references/AUTOMATION_TEMPLATE.md) -
  copied to `farplane/automations.md` for reviewable Codex automation prompts.
- [references/PRD_TICKET_TEMPLATE.md](references/PRD_TICKET_TEMPLATE.md) -
  copied to `tickets/TASK-0001/ticket.md` as the post-init PRD handoff.
- [references/PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md)
  - copied to `PROJECT_RULES.md` for project stack, runtime, and QA commands.
- [references/qa/](references/qa/) - copied when creating the QA cookbook
  surface.
- [../horizon-advisor/references/project-goals.md](../horizon-advisor/references/project-goals.md)
  - load in full mode when shaping or validating `farplane/goals.md` before
  compiling execution with `goal-advisor`.
- [../../docs/farplane-framework/project-files.md](../../docs/farplane-framework/project-files.md)
  - load when the user asks why a Farplane project has these files or how the
  spec should evolve.
- [README.md](README.md) - load only for skill-local manual bootstrap details.
- [prompts/plan.md](prompts/plan.md) and [prompts/build.md](prompts/build.md) -
  load only when the user asks for reusable planning/build prompts.
