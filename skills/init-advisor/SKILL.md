---
name: init-advisor
version: 3.0.0
description: "Turn a new-project intake into a Farplane substrate, readiness audit, optional code scaffold, and harness-creator handoff."
tier: 3
group: coding
source: local
eval: eval_task.json
qa_checklist: qa_checklist.md
---

# Init Advisor Skill

## Context

One-time setup for new or migrated projects. Every initialized project is a
Farplane project by default: it gets tracked `farplane/` config, ignored
`.farplane/` runtime state, visible tickets, docs, QA guidance, and optional
app-stack scaffolding.

The skill's completion point is initialization, not full product discovery. It
scaffolds `farplane/harness.md` as the static human charter and
`farplane/products.md` as the team archetype and product-catalog surface. In
`full` mode, route the operating-model setup through `harness-creator` after
the substrate exists. `harness-creator` owns the real-world-equivalent
grounding and composes downstream advisors such as `horizon-advisor`,
`harness-advisor`, `skill-creator`, and `goal-advisor` when they are needed.
Init advisor should not separately orchestrate those advisor calls.

This skill also owns the place where reusable stack setup recipes live for
common repo types such as Convex, Next.js, Clerk, shadcn, React apps, and
optional quality tooling. Keep those recipes in this skill or its references;
do not delete the code-repo scaffolding branch while simplifying project
initialization.

Reusable project automation prompt templates live in
[AUTOMATION_TEMPLATE.md](references/AUTOMATION_TEMPLATE.md). New projects use
the Farplane Framework's recurring loops: `pulse-update` for frequent bounded
ticket execution and explicit `interval-update` automations for daily or weekly
reporting and planning.
Generated project config should include `farplane/automations.md` as the
reviewable prompt source copied into Codex automations.

When answering "what does init create?", "what should the automation template
say?", or "what should generated automation surfaces contain?", do not answer
with `farplane/automations.md` alone. Lead with the core generated substrate and
then describe the recurring-loop prompts:

- `farplane/harness.md`: static human charter with human thesis, static
  leverage commitments, non-tradeoffs, agent authority, and change rule.
- `farplane/products.md`: product catalog for primary/supporting products and
  work lanes.
- Grounding step: before finalizing `farplane/harness.md`,
  `farplane/products.md`, or `farplane/goals.md`, ground the team archetype
  against real-world equivalents so the static charter and product catalog are
  not invented from file names alone.
- `farplane/automations.md`: reviewable Pulse, Daily Interval, and Weekly
  Interval prompt source. It does not create legacy `farplane/steer.config.toml`
  or `.farplane/state/steer-scheduler.json`; interval reports are date-stamped
  artifacts, not `latest.md` as canonical state.

Required sentence for generated-surface answers: "Before finalizing
`farplane/harness.md`, `farplane/products.md`, or `farplane/goals.md`, ground
the team archetype against real-world equivalents."

When the operator asks how init or migration should decide what to ask before
filling `farplane/harness.md`, `farplane/products.md`, or `farplane/goals.md`,
answer with this adaptive intake shape:

```text
1. Resolve `human_intake := skip | offer | required`; default to `offer` for
   new or migrated meaning-heavy files.
2. Use destination skill signatures as the question inventory.
3. Route `harness.md`, `products.md`, feedback loops, missing systems, and
   milestone-shape params to `harness-creator`.
4. Route `goals.md`, North Star, value function, KPI tree, holds, and milestone
   deltas to `horizon-advisor`.
5. Ask direct signature questions for factual or narrow missing params.
6. Escalate to `deep-interview --quick` only for intent-heavy, contradictory,
   or risky canonical-file gaps.
7. Constrain `deep-interview --quick` to the missing signature params plus
   intent, outcome, non-goals, decision boundaries, and success criteria.
8. Write the human intake decision, missing answers, and any
   `deep-interview` summary into `docs/bootstrap-brief.md`.
9. Do not embed or duplicate Deep Interview inside `init-advisor`,
   `harness-creator`, or `horizon-advisor`.
10. Do not claim `project_initialized` until required operator-owned params are
    answered or recorded as blocked.
```

Always include these two closeout lines in adaptive-intake answers:

```text
Record: write `human_intake`, missing answers, and any `deep-interview`
summary to `docs/bootstrap-brief.md`.
Boundary: do not embed or duplicate the Deep Interview loop inside
`init-advisor`, `harness-creator`, or `horizon-advisor`.
```

## Skill Signature

```text
init_advisor(project_root?, project_idea?, repo_shape?, stack_profile?, init_mode?, human_intake?, force?)
  -> project_substrate
   + farplane_config
   + readiness_audit
   + project_identity
   + static_harness_charter
   + operating_model_handoff_or_result?
   + goals_delta?
   + products_catalog_stub
   + optional_code_scaffold?
   + ticket_system
   + qa_surface
   + runtime_contract
   + starter_prd_ticket
   + automation_setup_handoff?
   + next_planning_handoff
state: reads(existing repo files, README/AGENTS/docs/tickets when present, bootstrap brief, project profile, operator context); writes AGENTS/PROJECT_RULES/ARCHITECTURE/docs/tickets/qa/farplane scaffolds, optional stack scaffold, and starter PRD ticket
gates: existing_files_preserved; spec_version_recorded; human_gates_named; human_intake_decision_recorded; secrets_not_written; no_hidden_automation; interactive_stack_steps_stop_for_human
routes: harness-creator | automation-advisor | deep-interview | prd | spec-to-ticket | research:official-docs | research:code-patterns
fails: creates only code scaffolding with no Farplane project config; treats PRD authoring as required init completion; claims full project initialization when the operating model, goals, success criteria, non-goals, or decision boundaries are still missing; deletes stack setup recipes; overwrites existing project state silently
```

## Phase Boundary

This skill follows Tier 0 phases inline. Use compact external research for
real-world equivalents before finalizing project archetype, static charter,
products, or goals; use deeper research only when a stack command, framework
convention, or market assumption may be stale. PRD authoring is a downstream
ticketed handoff, not the default init phase.

`init_mode` controls completion semantics:

- `substrate`: create or preserve the Farplane project files, write any missing
  readiness gaps into `docs/bootstrap-brief.md`, and report
  `substrate_complete`.
- `full`: after substrate setup, call `harness-creator` for the operating-model
  pass. It should ground the team archetype, static charter, products, goals,
  feedback loops, missing systems, current milestone, and any Goal Advisor
  handoff. Ask the first missing operator-owned harness-creator parameter
  instead of running separate goal, product, or advisor interviews from
  init-advisor.

`human_intake` controls how init/migration fills human-meaning files:

- `skip`: scaffold or migrate files mechanically and write missing intent as
  readiness gaps in `docs/bootstrap-brief.md`.
- `offer` (default): when missing, placeholder, stale, or newly introduced
  files depend on human intent, offer a short intake before filling them.
- `required`: do not finalize meaning-heavy file content until the missing
  operator-owned params have been answered or recorded as blocked.

Use direct signature questions first. Derive the question inventory from the
destination skill signatures instead of inventing a generic interview:
`harness-creator` for `farplane/harness.md`, `farplane/products.md`,
feedback loops, missing systems, and current milestone shape;
`horizon-advisor` for `farplane/goals.md`, value function, KPIs, holds, and
milestone deltas. Escalate to `deep-interview --quick` only when the missing
params are intent-heavy, contradictory, or risky enough that one direct
question would produce a shallow or misleading file fill. Intent-heavy params
include mission, human thesis, priorities, non-goals, decision boundaries,
success criteria, North Star, value function, KPI meaning, and current
milestone.

Do not embed the Deep Interview loop in `init-advisor`, `harness-creator`, or
`horizon-advisor`. `deep-interview` supplies the questioning method when
signature questions are not enough; the destination skill still owns the file
delta and handoff.

Do not treat `farplane/goals.md` existing as proof that goal setup is complete.
If the split project files are placeholder, stale, or not grounded in the
operator's stated intent, the result is `needs_operating_model_intake`, not
`project_initialized`.
Keep `farplane/goals.md` as Markdown with a fenced `goal-program` block for
parseable goals, value function, axes, projects, and milestones. Propose or
apply split-file deltas only after operator intent is known, and use
`goal-advisor` only after a current milestone is concrete enough to compile
into a ticket-backed Goal Packet.

Every material setup stage should be expressible as a function signature.
Resolve missing params from local files, operator context, and real-world
equivalent research first; if a required param remains unknown, ask the smallest
blocking question and record the readiness gap instead of inventing the value.

```text
setup_project_operating_model(bootstrap_brief, project_context,
                              existing_harness?, existing_products?,
                              existing_goals?, human_intake?)
  -> readiness_status
   + human_intake_decision
   + first_missing_question?
   + deep_interview_quick_handoff?
   + harness_delta?
   + products_delta?
   + goals_delta?
   + current_milestone_candidate?
   + goal_advisor_handoff?
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the init target.
  - [ ] Resolve `project_root`, greenfield vs brownfield state, `force?`, and
    whether the user wants only Farplane substrate or also code/app scaffolding.
  - [ ] Resolve the project identity for `farplane/manifest.json`:
        `project.name`, `project.description`, and `project.archetype`.
  - [ ] Resolve `init_mode := substrate | full`; use `full` only when the
    operator wants project-goals setup during initialization.
  - [ ] Resolve `human_intake := skip | offer | required`; default to `offer`
        for new or migrated meaning-heavy files and record the decision in
        `docs/bootstrap-brief.md` when readiness gaps remain.
  - [ ] Inspect existing README, AGENTS, docs, tickets, package files, and app
    structure before writing.
- [ ] 2. Select the project and stack profile.
  - [ ] Select or preserve the project profile from
    [project-profiles](./references/project-profiles.md).
  - [ ] Select a stack profile such as Convex + Next.js + Clerk, plain Next.js
    + shadcn, Convex in an existing app, React-only, or no code scaffold.
  - [ ] Capture enough project identity to scaffold the manifest. In `full`
    mode, let `harness-creator` perform the real-world-equivalent grounding
    before finalizing `farplane/harness.md`, `farplane/products.md`, or
    `farplane/goals.md`.
  - [ ] Use [research:official-docs](../research/SKILL.md#researchofficial-docs)
    when stack setup commands or framework conventions may be stale.
  - [ ] Use [research:code-patterns](../research/SKILL.md#researchcode-patterns)
    when peer or local repo scaffolding patterns should shape the code
    scaffold.
- [ ] 3. Initialize the Farplane project substrate.
  - [ ] Run or mirror `scripts/bootstrap.sh` to create tracked `farplane/`
    config, ignored `.farplane/` runtime state, `tickets/`, docs, QA, optional
    hooks, validation scripts, and review helper surfaces.
  - [ ] Create `farplane/harness.md` as the tracked static human charter:
        mission, human thesis, operating principles, priorities,
        non-tradeoffs, static leverage commitments, allocation guardrails,
        agent authority, and change rule. Do not place dynamic product
        direction or current strategy here.
  - [ ] Create `farplane/products.md` as the tracked project product catalog:
        team table, product table, work-lane table, and constraints. Do not
        treat chores as products, and do not put planning algorithms here.
  - [ ] Create `farplane/hooks.json` as declarative hook configuration. Do not
        put hook algorithms, eval runners, or post-action procedures in project
        files; those belong in skills, hooks, validators, or ticket programs.
  - [ ] Create `.agents/skills/README.md` as the local product-skill home.
        Project-specific product workflows live under
        `.agents/skills/<product-skill>/SKILL.md`; promote only stable
        cross-project workflows to root `skills/`.
  - [ ] Keep `farplane/automations.md` as the exact prompt source that calls
    generic skills in plain project-specific operational language.
  - [ ] Include Pulse, Daily Interval, and Weekly Interval prompt blocks:
        Pulse selects fast bounded actions; Daily Interval reviews the last 24
        hours and plans the next 24 hours; Weekly Interval checks goals drift
        and plans the next week.
  - [ ] In the Pulse prompt, say Pulse selects at most one bounded action per
        beat, prefers local ready/unblocked tickets, and does not require a
        separate ticket-drainer automation.
  - [ ] In the Pulse prompt, say it reads `farplane/harness.md` to preserve the
        static human thesis and `farplane/products.md` when shaping product
        refill tickets.
  - [ ] Product refill tickets name the project type, baseline or comparison
        point, expected artifact, and proof signal.
  - [ ] Substantial implementation routes through `harness-creator` first when
        the operating model is missing, then `goal-advisor` only after a
        concrete milestone exists.
  - [ ] Do not create legacy Steer scheduler files such as
        `farplane/steer.config.toml` or
        `.farplane/state/steer-scheduler.json`.
  - [ ] Use date-stamped interval report paths as canonical evidence; do not
        make `latest.md` the canonical interval state.
  - [ ] Ensure `farplane/manifest.json` records the Farplane project
    `spec_version` and standard tracked/ignored paths.
  - [ ] Preserve existing files unless `force == true` or explicit overwrite
    intent is present.
  - [ ] Keep `.farplane/` ignored runtime state and `farplane/` tracked project
    spec.
  - [ ] Do not auto-enable scaffolded git hooks.
- [ ] 4. Run readiness audit and full-mode operating-model setup.
  - [ ] When doing a dogfood, final readiness review, or material init
        behavior change, read [qa_checklist.md](qa_checklist.md) and apply it
        as preflight plus finish-gate checks.
  - [ ] Audit `docs/bootstrap-brief.md`, `farplane/harness.md`,
    `farplane/goals.md`, `farplane/products.md`, `farplane/automations.md`,
    `farplane/bindings.md`, `.agents/skills/README.md`, `farplane/pm.json`,
    `PROJECT_RULES.md`, and QA surfaces for missing,
    placeholder, stale, or disabled state.
  - [ ] Treat missing human thesis, static leverage commitments, non-tradeoffs,
        agent authority, or change rule in `farplane/harness.md` as a readiness
        gap. The first useful question is: "What is the durable human thesis
        this project must preserve while its products and goals evolve?"
  - [ ] Treat missing or placeholder team archetype as a readiness gap. The
        first useful question is: "What kind of team is this project supposed to
        be, and what should it repeatedly produce?"
  - [ ] Audit `docs/bootstrap-brief.md`, `farplane/products.md`, and
        `farplane/goals.md` for team archetype, product outputs, North Star,
        3-month outcome, success criteria, non-goals, and decision boundaries.
  - [ ] Use the destination skill signatures as the question inventory:
        `harness-creator` params for static charter, product catalog, feedback
        loops, missing systems, and current milestone shape; `horizon-advisor`
        params for North Star, value function, KPI tree, goals, holds, and
        milestone deltas.
  - [ ] Ask direct signature questions for factual or narrow missing params.
        Escalate to `deep-interview --quick` only when missing params are
        intent-heavy, contradictory, or likely to produce shallow canonical
        files without a Socratic pass.
  - [ ] When using `deep-interview --quick`, constrain it to the missing
        signature params and readiness gates: intent, outcome, non-goals,
        decision boundaries, and success criteria. Write the summary into
        `docs/bootstrap-brief.md`; do not duplicate the interview loop inside
        `init-advisor`.
  - [ ] Write the audit result into `docs/bootstrap-brief.md` under
        Goal Intake Status and Initialization Readiness when those sections
        exist, including readiness state, human intake decision, missing
        answers, and any `deep-interview` summary or handoff.
  - [ ] Keep `farplane/goals.md` as Markdown with a fenced `goal-program` block
        for parseable goals, value function, axes, projects, and milestones.
  - [ ] Propose or apply split-file deltas only after operator intent is known.
  - [ ] In `substrate` mode, report missing operating-model questions as next
    handoff rather than asking the full interview now.
  - [ ] In `full` mode, call `harness-creator` after substrate setup when the
    static charter, products, goals, feedback loops, missing systems, or
    current milestone need to be written or improved, including any Goal Advisor
    handoff after the milestone is concrete.
  - [ ] Ask only the first missing direct `harness-creator` or
        `horizon-advisor` parameter before claiming `project_initialized`,
        unless the adaptive intake rule escalates to `deep-interview --quick`.
        Common first questions are: "What is the durable human thesis this
        project must preserve?" or "What should this project reliably do for
        you over the next 3 months that it does not yet do reliably today?"
  - [ ] Let `harness-creator` decide whether to use `horizon-advisor`,
    `harness-advisor`, `skill-creator`, or `goal-advisor`; do not duplicate
    those advisor calls in init-advisor.
  - [ ] Use `goal-advisor` only after the current milestone is concrete enough
        to compile into a ticket-backed Goal Packet.
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
    dependency-cruiser/Madge, Knip/depcheck, static analysis dashboard,
    mutation testing, dependency audit, secret scan, config validation, or
    resilience/failure tests.
    Do not install these tools automatically unless setup scope explicitly
    includes code scaffold/tooling installation.
  - [ ] Route behavior-preserving cleanup to `refactoring` and risk-reduction
        work to `hardening`.
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
        automation runtime IDs there. Runtime automation IDs stay in the Codex
        app automation store.
  - [ ] If activation is skipped or unavailable, report
        `needs_operating_model_intake` or `needs_automation_setup` with the
        exact next owner: `harness-creator` or `automation-advisor`.
- [ ] 8. Verify and finish init.
  - [ ] Run focused scaffold checks such as
    `python3 bin/validators/check_farplane_project_files.py` when available.
  - [ ] Confirm the expected `farplane/`, `.farplane/`, and `tickets/` surfaces
    exist.
  - [ ] Report a plain human status such as "Ready", "Filesystem ready,
    operating model still missing", "Runtime setup missing", or "Automation
    setup missing"; include the snake_case internal status only when writing a
    machine-readable field or validator-facing note.
  - [ ] Report the initialized stack profile, any skipped human-gated steps,
    the starter PRD ticket, and the next command or skill.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## What This Sets Up

- Farplane substrate: `farplane/manifest.json`, `farplane/README.md`,
  `farplane/harness.md`, `farplane/products.md`, `farplane/hooks.json`,
  `.agents/skills/README.md`, `farplane/*.md`,
  `.farplane/` runtime state, and `tickets/`.
- Project operating docs: `AGENTS.md`, `PROJECT_RULES.md`, `ARCHITECTURE.md`,
  `docs/bootstrap-brief.md`, `docs/prd.md`, `docs/specs/`, and memory logs.
- QA and proof surface: `qa/`, optional `.githooks/`, repo-local validation
  scripts, and optional local Codex SDK review-loop files.
- Starter handoff: `tickets/TASK-0001/ticket.md` for the post-init
  `deep-interview -> prd` phase.
- Automation setup handoff: `automation-advisor` creates or updates the live
  Codex loops only when activation is requested; `farplane/pm.json` keeps
  PM-visible thread IDs while runtime automation IDs stay in the Codex app
  automation store.
- Full-mode operating-model setup: `harness-creator` receives the initialized
  substrate and owns proposed or applied deltas for `farplane/harness.md`,
  `farplane/products.md`, `farplane/goals.md`, `farplane/automations.md`,
  `farplane/bindings.md`, missing-system tickets, and any Goal Advisor handoff
  after the current milestone is concrete. `human_intake` controls whether
  missing operator-owned params are skipped as readiness gaps, offered as a
  short intake, or required before file finalization.
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
  dependency-cruiser or Madge, Knip or depcheck, static analysis dashboard,
  mutation testing for high-budget proof, Semgrep, CodeQL, SonarQube, and
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
- [references/FARPLANE_PRODUCTS_TEMPLATE.md](references/FARPLANE_PRODUCTS_TEMPLATE.md)
  - copied to `farplane/products.md` for the project product catalog.
- [references/AUTOMATION_TEMPLATE.md](references/AUTOMATION_TEMPLATE.md) -
  copied to `farplane/automations.md` for reviewable Codex automation prompts.
- [references/PRD_TICKET_TEMPLATE.md](references/PRD_TICKET_TEMPLATE.md) -
  copied to `tickets/TASK-0001/ticket.md` as the post-init PRD handoff.
- [references/PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md)
  - copied to `PROJECT_RULES.md` for project stack, runtime, and QA commands.
- [references/qa/](references/qa/) - copied when creating the QA cookbook
  surface.
- [../harness-creator/SKILL.md](../harness-creator/SKILL.md) - call in full
  mode after substrate setup when static charter, products, goals, feedback
  loops, missing systems, automation/binding deltas, or the current milestone
  need project-specific setup.
- [../../docs/farplane-framework/project-files.md](../../docs/farplane-framework/project-files.md)
  - load when the user asks why a Farplane project has these files or how the
  spec should evolve.
- [README.md](README.md) - load only for skill-local manual bootstrap details.
- [prompts/plan.md](prompts/plan.md) and [prompts/build.md](prompts/build.md) -
  load only when the user asks for reusable planning/build prompts.
