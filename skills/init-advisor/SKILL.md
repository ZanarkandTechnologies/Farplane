---
name: init-advisor
version: 3.1.0
description: "Turn a new-project intake into a Farplane substrate, readiness audit, optional code scaffold, and harness-creator handoff."
tier: 3
group: operations
source: local
eval: evals/evals.json
qa_checklist: qa_checklist.md
---

# Init Advisor Skill

## Context

One-time setup for new or migrated projects. Every initialized project is a
Farplane project by default: it gets tracked `farplane/` config, ignored
`.farplane/` runtime state, ignored active ticket work with tracked ticket
templates, docs, QA guidance, and optional app-stack scaffolding.

The skill's completion point is initialization, not full operating-model
discovery. It scaffolds `farplane/harness.yaml` as the typed human charter,
descriptive-product, capability-reference, and metric-selection surface, and
`farplane/metrics.yaml` as the measurable
objective, guard, and metric-definition contract. In `full` mode, route the operating-model setup through
`harness-creator` after the substrate exists. `harness-creator` owns the
real-world-equivalent
grounding and composes downstream advisors such as `metric-advisor`,
`harness-advisor`, `skill-creator`, and `goal-advisor` when they are needed.
Init advisor should not separately orchestrate those advisor calls.

This skill also owns the place where reusable stack setup recipes live for
common repo types such as Convex, Next.js, Clerk, shadcn, React apps, and
optional quality tooling. Keep those recipes in this skill or its references;
do not delete the code-repo scaffolding branch while simplifying project
initialization.

For an existing project framework upgrade, run
`scripts/migrate_framework.py --project-root <project> --force`. This is the
only safe force path: it updates versioned framework fields and deterministic
metric `kind -> type` mappings while preserving human-authored charter,
descriptions, refresh prompts, bindings, tickets, and docs. Do not use
`bootstrap.sh --force` as a general project upgrade because bootstrap owns
whole-file scaffolding.

Reusable project automation config templates live in
[AUTOMATION_TEMPLATE.toml](references/AUTOMATION_TEMPLATE.toml). Generated
project config includes `farplane/automations.toml` as the reviewable desired
state copied into Codex automations; live activation belongs to
`automation-advisor`.

For "what does init create?" answers, load [README.md](README.md) or the
manifest template rather than duplicating the generated-file inventory here.
For readiness and adaptive human-intake gates, load
[qa_checklist.md](qa_checklist.md) and apply it as preflight plus finish check.

## Skill Signature

```text
init_advisor(project_root?, project_idea?, repo_shape?, stack_profile?, init_mode?, human_intake?, force?)
  -> project_substrate
   + farplane_config
   + readiness_audit
   + project_identity
   + static_harness_charter
   + operating_model_handoff_or_result?
  + metric_objective_delta?
   + metric_contract
   + capability_workflow_handoff?
   + optional_code_scaffold?
   + ticket_system
   + qa_surface
   + runtime_contract
   + business_foundation_tickets
   + automation_setup_handoff?
   + next_planning_handoff
state: reads(existing repo files, README/AGENTS/docs/tickets when present, bootstrap brief, project profile, operator context); writes AGENTS/PROJECT_RULES/ARCHITECTURE/docs/tickets/qa/farplane scaffolds, optional stack scaffold, and three dependent business-foundation tickets
gates: existing_files_preserved; spec_version_recorded; human_gates_named; human_intake_decision_recorded; secrets_not_written; no_hidden_automation; interactive_stack_steps_stop_for_human
routes: harness-creator | automation-advisor | deep-interview | prd | spec-to-ticket | research:official-docs | research:code-patterns
fails: creates only code scaffolding with no Farplane project config; treats PRD authoring as required init completion; claims full project initialization when human intent, measurable objectives, success criteria, non-goals, or decision boundaries are still missing; deletes stack setup recipes; overwrites existing project state silently
```

## Phase Boundary

This skill follows Tier 0 phases inline. Use compact grounding before
finalizing project archetype, static charter, capability workflows, or metric objectives; use deeper
research only when stack commands, framework conventions, or market assumptions
may be stale. PRD authoring is downstream of the three-ticket business
foundation, not init completion.

`init_mode` controls completion semantics:

- `substrate`: create or preserve the Farplane project files, write any missing
  readiness gaps into `docs/bootstrap-brief.md`, and report
  `substrate_complete`.
- `full`: after substrate setup, call `harness-creator` for the operating-model
  pass. It owns the static charter, capability workflows, metric objectives, feedback loops, missing
  systems, metric objectives, and any later Goal Advisor handoff.

`human_intake` controls how init/migration fills human-meaning files:

- `skip`: scaffold or migrate files mechanically and write missing intent as
  readiness gaps in `docs/bootstrap-brief.md`.
- `offer` (default): when missing, placeholder, stale, or newly introduced
  files depend on human intent, offer a short intake before filling them.
- `required`: do not finalize meaning-heavy file content until the missing
  operator-owned params have been answered or recorded as blocked.

Use destination skill signatures as the question inventory. Route static
charter, capability workflow references, feedback loops, missing systems, and
objective shape to `harness-creator`; route metric meaning, directions, guards,
and proof providers to `metric-advisor`. Escalate to
`deep-interview --quick` only when direct signature questions would produce
shallow or misleading answers. Record the intake choice and missing answers in
`docs/bootstrap-brief.md`; do not embed the Deep Interview loop here.

Do not treat file existence as readiness. Placeholder or stale split project
files mean "operating model still missing", not "initialized". Keep human
meaning, hard constraints, planning areas, and selected metric refs in
`farplane/harness.yaml`; keep reusable metric direction, freshness, and guard
rules in `farplane/metrics.yaml`; use
`goal-advisor` only after a ticket is concrete enough for a Goal Packet.

```text
setup_project_operating_model(bootstrap_brief, project_context,
                              existing_harness?, existing_capability_skills?,
                              existing_metrics?, human_intake?)
  -> readiness_status
   + human_intake_decision
   + first_missing_question?
   + deep_interview_quick_handoff?
   + harness_delta?
   + capability_skill_delta?
   + metric_objective_delta?
  + initial_metric_objectives?
   + goal_advisor_handoff?
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the init target.
  - [ ] Resolve `project_root`, greenfield vs brownfield, `force?`,
        `init_mode := substrate | full`, `human_intake := skip | offer |
        required`, and whether code/app scaffold is included.
  - [ ] Resolve manifest identity: `project.name`, `project.description`, and
        `project.archetype`.
  - [ ] Inspect existing README, AGENTS, docs, tickets, package files, and app
    structure before writing.
- [ ] 2. Select the project and stack profile.
  - [ ] Select or preserve the project profile from
    [project-profiles](./references/project-profiles.md).
  - [ ] If code scaffold is included, load
        [CODE_SCAFFOLD_RECIPES.md](references/CODE_SCAFFOLD_RECIPES.md) and
        use official-docs or code-pattern research when commands or conventions
        may be stale.
- [ ] 3. Initialize the Farplane project substrate.
  - [ ] Run or mirror `scripts/bootstrap.sh` to create tracked `farplane/`
    config, ignored `.farplane/` runtime state, flat authored
    `.farplane/entities/*.md`, authored `.farplane/views.yaml`, skill-owned
    report directories, ignored active ticket work with tracked ticket
    templates, docs, QA, optional hooks, validation scripts, and review helper
    surfaces.
  - [ ] Use [GITIGNORE_TEMPLATE](references/GITIGNORE_TEMPLATE) as the
        canonical generated `.gitignore` block for Farplane local runtime and
        work state.
  - [ ] Use [AUTOMATION_TEMPLATE.toml](references/AUTOMATION_TEMPLATE.toml) as
        the `farplane/automations.toml` source; do not duplicate automation
        config rules in this skill.
  - [ ] Create or preserve `farplane/metrics.yaml` as the metric-definition and
        grouped-refresh contract; keep only non-secret connector/provider
        coordinates in `farplane/bindings.yaml`.
  - [ ] Do not create legacy Steer scheduler files such as
        `farplane/steer.config.toml` or
        `.farplane/state/steer-scheduler.json`.
  - [ ] Preserve existing files unless `force == true` or explicit overwrite
        intent is present.
  - [ ] Do not auto-enable scaffolded git hooks.
- [ ] 4. Run readiness audit and full-mode operating-model setup.
  - [ ] Read [qa_checklist.md](qa_checklist.md) before dogfood, final readiness
        review, or material init behavior changes; apply it again before finish.
  - [ ] In `substrate` mode, record missing operating-model answers in
        `docs/bootstrap-brief.md` and report them as the next handoff.
  - [ ] In `full` mode, call `harness-creator` after substrate setup when the
        static charter, capability workflows, metric objectives,
        feedback loops, or missing systems need
        project-specific setup.
  - [ ] Let `harness-creator` decide whether to route to `metric-advisor`,
        `harness-advisor`, `skill-creator`, or `goal-advisor`.
- [ ] 5. Create the business foundation.
  - [ ] Create or preserve exactly three ordinary ticket paths:
    `TASK-0001` finds the first customer, `TASK-0002` delivers the first value,
    and `TASK-0003` collects the first revenue.
  - [ ] Give each ticket its scalar `foundation_step`, numbered
    `foundation_sequence`, and the ordinary dependency on the preceding ticket
    where applicable. Keep any external-action approval instructions in the
    ticket program rather than retired ticket metadata.
  - [ ] Preserve every existing ticket path independently unless explicit
    scaffold replacement was requested; report partial collisions honestly.
  - [ ] Leave `docs/prd.md` as a draft placeholder unless PRD work is
    explicitly requested now.
  - [ ] Do not create live work or automation. Complete the foundation in
    order, then route to PRD/spec planning for the next product slice.
- [ ] 6. Prepare automation activation.
  - [ ] Create `farplane/pm.json` as UI grouping glue with `threads.chats` and
        `threads.automations`.
  - [ ] Do not create live threads or automations unless the operator asked for
        live automation activation.
  - [ ] When live activation is requested, call `automation-advisor` after the
        substrate exists so it can create or update the loops named in
        `farplane/automations.toml`.
  - [ ] Write PM-visible thread IDs to `farplane/pm.json`; keep runtime
        automation IDs in the Codex app automation store.
  - [ ] If activation is skipped or unavailable, report
        `needs_operating_model_intake` or `needs_automation_setup` with the
        exact next owner: `harness-creator` or `automation-advisor`.
- [ ] 7. Verify and finish init.
  - [ ] Run focused scaffold checks such as
    `python3 bin/validators/check_farplane_project_files.py` when available.
  - [ ] Confirm the expected `farplane/`, `.farplane/`, and `tickets/` surfaces
    exist.
  - [ ] Report a plain human status such as "Ready", "Filesystem ready,
    operating model still missing", "Runtime setup missing", or "Automation
    setup missing"; include the snake_case internal status only when writing a
    machine-readable field or validator-facing note.
  - [ ] Report the initialized stack profile, any skipped human-gated steps,
    the three business-foundation tickets, and the next command or skill.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Reference Map

- [README.md](README.md) - load when the user asks what InitAdvisor sets up,
  how to run bootstrap manually, or how brownfield migration works.
- [references/project-profiles.md](references/project-profiles.md) - load when
  selecting project type, components, advice axes, prototype gates, and
  downstream handoff.
- [references/project-lifecycle.md](references/project-lifecycle.md) - load
  when recording the bootstrap route and next lifecycle phase.
- [references/MANIFEST_TEMPLATE.json](references/MANIFEST_TEMPLATE.json) -
  copied to `farplane/manifest.json` for the Farplane project spec instance.
- [references/FRAMEWORK_CHANGELOG.md](references/FRAMEWORK_CHANGELOG.md) -
  load before bumping `farplane-framework` versions or migrating projects
  between framework spec versions.
- [references/GITIGNORE_TEMPLATE](references/GITIGNORE_TEMPLATE) - appended to
  `.gitignore` so generated local runtime state and active ticket work stay out
  of commits while shared ticket and local-skill scaffold remains trackable.
- [references/FEATURES_README_TEMPLATE.md](references/FEATURES_README_TEMPLATE.md)
  - copied to `docs/features/README.md` for feature-spec guidance.
- [references/SYSTEMS_README_TEMPLATE.md](references/SYSTEMS_README_TEMPLATE.md)
  - copied to `docs/systems/README.md` for system/product grouping guidance.
- [references/AUTOMATION_TEMPLATE.toml](references/AUTOMATION_TEMPLATE.toml) -
  copied to `farplane/automations.toml` for reviewable Codex automation
  configs.
- [references/CODE_SCAFFOLD_RECIPES.md](references/CODE_SCAFFOLD_RECIPES.md) -
  load only when `include_code_scaffold == true`, the user asks which stack can
  be scaffolded, or stack setup commands need review.
- [references/FOUNDATION_FIND_CUSTOMER_TICKET_TEMPLATE.md](references/FOUNDATION_FIND_CUSTOMER_TICKET_TEMPLATE.md),
  [references/FOUNDATION_DELIVER_VALUE_TICKET_TEMPLATE.md](references/FOUNDATION_DELIVER_VALUE_TICKET_TEMPLATE.md),
  and [references/FOUNDATION_COLLECT_REVENUE_TICKET_TEMPLATE.md](references/FOUNDATION_COLLECT_REVENUE_TICKET_TEMPLATE.md)
  - copied to `TASK-0001` through `TASK-0003` as the dependency-ordered
    business foundation.
- [references/PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md)
  - copied to `PROJECT_RULES.md` for project stack, runtime, and QA commands.
- [references/TICKETS_README_TEMPLATE.md](references/TICKETS_README_TEMPLATE.md)
  and [references/TICKET_TEMPLATE.md](references/TICKET_TEMPLATE.md) - packaged
  ticket lifecycle/template scaffolds used by both source and installed runs.
- [references/qa/](references/qa/) - copied when creating the QA cookbook
  surface.
- [../harness-creator/SKILL.md](../harness-creator/SKILL.md) - call in full
  mode after substrate setup when static charter, capability workflows, metric objectives, feedback
  loops, missing systems, automation/binding deltas, or metric objectives
  need project-specific setup.
- [../../docs/farplane-framework/project-files.md](../../docs/farplane-framework/project-files.md)
  - load when the user asks why a Farplane project has these files or how the
  spec should evolve.
- [prompts/plan.md](prompts/plan.md) and [prompts/build.md](prompts/build.md) -
  load only when the user asks for reusable planning/build prompts.
