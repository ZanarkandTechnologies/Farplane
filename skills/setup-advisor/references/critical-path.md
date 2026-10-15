# Setup Advisor Critical Path

The end-to-end path for creating or migrating a Farplane project, from target
binding to verified readiness. Load it to sequence `init`/`migrate` with
`charter` and automation handoff; the file inventory lives in
[reference-map.md](reference-map.md) and the upgrade steps in
[migration.md](migration.md).

Initialization creates the substrate; it does not pretend that file creation is
the same as grounded goals or useful autonomous work.

```text
setup_advisor(project_root, idea, init_mode, human_intake)
  -> project substrate
   + static charter
   + goals contract
   + capability-skill home
   + one-board ticket and proof surfaces
   + desired automation config
   + operating-model or activation handoff
```

## 1. Bind The Target

Resolve the project root, greenfield/brownfield state, project identity, stack
profile, `init_mode := substrate | full`, human-intake policy, and overwrite
authority. Inspect existing files before writing and preserve them unless
explicit overwrite intent exists.

Stop for credentials, spend, deploys, destructive actions, or genuinely
branching project decisions. Missing human-owned meaning becomes one compact
question or a readiness gap, not invented content.

## 2. Create The Substrate

Create or preserve:

```text
AGENTS.md
README.md
ARCHITECTURE.md
docs/bootstrap-brief.md
docs/prd.md
docs/{HISTORY,MEMORY,TASTE}.md
qa/
tickets/README.md
tickets/templates/
tickets/TASK-0001/ticket.md
```

The result has local policy, durable memory, a visible ticket workflow, QA
entrypoints, and a starter planning handoff. PRD authoring remains downstream
unless explicitly requested.

## 3. Create Framework Config

Tracked project config:

```text
farplane/README.md
farplane/manifest.json
farplane/harness.yaml
farplane/metrics.yaml
farplane/automations/
farplane/bindings.yaml
farplane/pm.json
.agents/skills/README.md
```

Ignored runtime state:

```text
.farplane/reports/
.farplane/metrics/
.farplane/project/ui/
.farplane/automation/
.farplane/state/
.farplane/evals/runs/
.farplane/logs/
```

Key ownership:

- `manifest.json`: versioned paths and compact project identity;
- `harness.yaml`: typed human charter, configured planning skill allowlist,
  passive area/ICP context, authority, capability refs, and selected metric refs;
- `metrics.yaml`: provider-independent metric definitions with direction,
  freshness, and optional guard rules;
- `.agents/skills/`: project-local recurring capability workflows;
- `automations/`: one record per live scheduled job, added by automation-advisor;
- `bindings.yaml`: non-secret connector/provider coordinates;
- tickets: executable commitments and all QA/review evidence;
- `.farplane/**`: generated/local observations and reports, not strategy.

Do not scaffold a product catalog, per-category strategy files, per-category
worker policy, or a generated controller index. A recurring output should map
to a callable capability skill; the metric objective explains its measurable contribution and a
ticket owns the current execution.

## 4. Run Readiness Audit

Audit the bootstrap brief, charter, metric selection, bindings, capability ownership,
automation desired state, local skill home, PM grouping config, project rules,
ticket templates, and QA surfaces.

Human-facing results:

```text
Ready
Filesystem ready, operating model still missing
Runtime setup missing
Automation setup missing
```

`project_initialized` requires a grounded operating model, current goals, an
owned route for required recurring outputs, and enough ticket/proof context to
start useful work. Placeholder files are not readiness proof.

## 5. Shape The Operating Model

In `full` mode, `setup-advisor` owns the project-specific pass:

```text
harness_creator(idea, values, priorities, current_files, capabilities)
  -> harness delta
   + goals delta
   + capability reuse map
   + local capability stubs or refinement tickets
   + feedback and missing-system tickets
   + initial metric objectives
   + goal_advisor handoff?
```

It checks existing reusable and project-local skills before creating a new
workflow. The `goal-advisor` metric card handles material objective/guard depth;
`goal-advisor` compiles a selected material ticket only after the ticket contract is concrete.

## 6. Prepare Automation

The desired project topology has no execution heartbeat. Work Pulse, the
former heartbeat, is retired; work enters as a GitHub issue in the project's
own repository and runs when the operator, or a session they start, runs
`goal-advisor` on it (native Goal), or directly when small.

```text
Feed Scout            cron/manual
Dogfood Improvement   cron/manual
Maintenance           cron/manual

AI Office root:
Company OS Daily      cron
Company OS Weekly     cron
```

Bootstrap writes `farplane/automations/`; `automation-advisor` owns live
Codex automation activation. Runtime IDs remain in the Codex automation store,
while `pm.json` contains only UI-visible grouping refs.
The AI Office root owns the single global Daily/Weekly pair; bootstrap does not
copy those records into managed projects.

Scheduled sources may write reports and bounded tickets of their own class.
They do not execute tickets, run due check-ins, or create additional worker
controllers. Automations are cron records that collect, report and propose;
they never create, close, label, assign or edit issues and never start agents
or runs.

## 7. Verify

Run the project-file validator, focused scaffold checks, YAML/TOML/JSON parses,
and an old-reference sweep. A clean bootstrap must not create retired project
files or require them to validate.

When live activation was requested, compare desired and live automation state:
no execution heartbeat, expected cron/manual jobs, correct project target,
and no duplicate executor.

Report the initialized stack, human-gated omissions, current readiness, starter
ticket, and exact next owner. Do not claim full initialization while a required
charter, goal, capability, proof, or runtime input is still a placeholder.
