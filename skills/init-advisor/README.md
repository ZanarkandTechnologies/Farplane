# Init Advisor

Bootstrap or migrate a project into the Farplane docs-first, ticket-first
harness model. Init sets up the project substrate first, can optionally run a
code/app scaffold such as Next.js, React, or Convex, and then leaves three
dependent business-foundation tickets: find the first customer, deliver the
first value, and collect the first revenue.

This setup should scaffold optional `.githooks` samples plus project-local
`scripts/pre_*_check.sh` files for local quality gates, a Codex SDK pre-push
diff-review loop, plus repo-owned runtime and `qa/` guidance so agents can
launch the app and capture evidence without guessing, all without enabling
hooks automatically.

Every initialized project is a Farplane project by default. Use
`init_mode=substrate` for substrate-only migrations, and `init_mode=full` when
the operator also wants the project operating model shaped during setup.

Framework manifest changes are tracked in
[FRAMEWORK_CHANGELOG.md](references/FRAMEWORK_CHANGELOG.md). Read it before
bumping `farplane/manifest.json` or migrating a project between
`farplane-framework` versions.

## Use Cases

- **Greenfield**: start a new repo with the full scaffold
- **Brownfield**: add the harness structure to an existing repo without rewriting the app

## Greenfield

Use the bootstrap script:

```bash
bash ~/.codex/skills/init-advisor/scripts/bootstrap.sh
```

Before finalizing the scaffold, run a structured bootstrap intake and keep the
answers in `docs/bootstrap-brief.md`.
That intake should explicitly answer what belongs in `pre-push` or `pre-commit`,
whether the Codex SDK diff reviewer should be advisory or strict and whether a
separate CI/deployment gate exists. It
should also name the canonical app-only run path, canonical full QA or
evidence-capture path, required services such as DB or orchestration tools, and
any port or environment-variable assumptions. When the user wants app code
created during init, select the stack scaffold before running commands.

That also writes `farplane/README.md`, `farplane/manifest.json`, `farplane/harness.yaml`,
`farplane/metrics.yaml`, `farplane/automations.toml`, `farplane/bindings.yaml`,
`.agents/skills/README.md`, `farplane/pm.json`, `docs/bootstrap-brief.md`, `qa/README.md`,
`qa/cookbook/TEMPLATE.md`, `.githooks/README.md`,
`.githooks/pre-commit`, `.githooks/pre-push`, `scripts/pre_commit_check.sh`,
`scripts/pre_push_check.sh`, review docs, and review-agent helper scripts as
opt-in samples. The recommended default is to keep the large-file scan, fill in
lint/typecheck/test/build commands, run advisory Codex SDK diff review during
pre-push, and activate only `pre-push` unless the repo wants an extra
pre-commit gate. The other required follow-through is to fill
`PROJECT_RULES.md` and `qa/` with the authoritative launch path agents should
use for ordinary app work versus QA. It also creates exactly three ordinary
foundation tickets at `tickets/TASK-0001` through
`tickets/TASK-0003`. They use normal dependencies to enforce customer -> value
-> revenue order. Existing ticket paths are preserved independently unless
`--force` was explicitly requested, so brownfield partial collisions are
reported and left untouched.

The script also creates ignored, owner-named `.farplane/` folders:
`.farplane/reports/`, `.farplane/metrics/daily/`,
`.farplane/evals/runs/`, `.farplane/logs/`, `.farplane/entities/`, `.farplane/wiki/`,
`.farplane/views.yaml`, and skill-owned report folders such as
`.farplane/customer-research/reports/`.
The flat Wiki article directory is the single source of truth. `wiki.sqlite`,
`index.json`, `graph.json`, and `crm.json` are generated views, while reports link entities
through `entity_refs` and remain owned by their producing skills. Keep shared
canonical framework config in tracked `farplane/`; Wiki article Markdown and
`views.yaml` are the explicit authored local exceptions under `.farplane/`. It also
appends [GITIGNORE_TEMPLATE](references/GITIGNORE_TEMPLATE) to `.gitignore` so
active `tickets/TASK-*` work stays local by default while `tickets/README.md`
and `tickets/templates/` remain available as tracked scaffold.

Bootstrap does not create live Codex automations by itself. After the substrate
exists, use `harness-creator` in full mode to shape the static charter,
capability workflows, metric objectives, guards, and feedback loops. `harness-creator`
routes to `metric-advisor` or `goal-advisor` only when those narrower advisor
calls are needed. When live loops are explicitly requested, use
`automation-advisor` to activate the single Work Pulse heartbeat plus separate
Feed Scout, Daily BAU, Weekly BAU, self-improvement, and optional cron records.
Activation creates or reuses the dedicated loop threads, creates or updates the
Codex automations, and appends PM-visible thread IDs to `farplane/pm.json`.

Optional code scaffold recipes live in
[CODE_SCAFFOLD_RECIPES.md](references/CODE_SCAFFOLD_RECIPES.md). Use the
selected recipe during init when requested, but stop for interactive cloud
setup, credentials, billing, deploys, and destructive actions.

After the business foundation closes, follow the planning funnel:

```text
brainstorm -> direct clarification -> metric-advisor -> goal-advisor
prd -> spec-to-ticket -> impl-plan -> goal-advisor
```

## Brownfield Migration

If the repo already exists, do the smallest migration first.

### Choose the versioned migration

Read the project's current `farplane/manifest.json` and compare
`spec_version` plus `template_uses.farplane-framework` with
[FRAMEWORK_CHANGELOG.md](references/FRAMEWORK_CHANGELOG.md). Apply each newer
migration entry in order. The changelog is the canonical version-to-version
migration guide; this section is the operational checklist.

For the V1 `2.0.4` contract, the important boundary is:

```text
tracked owners:
  harness.yaml + metrics.yaml + bindings.yaml + automations.toml

ignored projections:
  .farplane/metrics/** + .farplane/project/ui/latest.json + reports/evals/logs

execution and proof:
  tickets/TASK-XXXX/{ticket.md,program.md,progress.md,artifacts/**}
```

Remove product registries/controllers and detached review/evidence stores only
after their active readers have been migrated. Define planning `areas` in
`harness.yaml`; scheduled jobs supply reports/candidates while one Work Pulse
planner owns proactive admission. Preserve reusable artifact workflows as
skills. Do not keep compatibility aliases unless an explicit external contract
requires them.

Ticket completion is the bounded event exception: the read-only learning
program writes a report, then deterministic Core may project one deduped
KPI-linked direct-fix or prove-or-reject ticket. Dogfood consumes the receipt
and does not recreate that ticket.

### 1. Add the harness structure

```bash
mkdir -p docs/features docs/systems tickets tickets/archive tickets/templates
touch ARCHITECTURE.md docs/prd.md docs/HISTORY.md docs/MEMORY.md docs/features/README.md docs/systems/README.md
```

Then copy in:

- `PROJECT_RULES.md`
- `AGENTS.md`
- `ARCHITECTURE.md`
- `farplane/README.md`
- `farplane/manifest.json`
- `farplane/harness.yaml`
- `farplane/metrics.yaml`
- `farplane/automations.toml`
- `farplane/bindings.yaml`
- `.agents/skills/README.md`
- `farplane/pm.json`
- `docs/TASTE.md`
- `qa/`
- `tickets/templates/ticket.md`

Use the versioned, field-preserving migration for an existing project:

```bash
python3 ~/.codex/skills/init-advisor/scripts/migrate_framework.py \
  --project-root . --force
```

This `--force` applies only known framework deltas. It preserves human-authored
charter, metric definitions, refresh prompts, bindings, docs, and tickets.
Do not use `bootstrap.sh --force` for framework upgrades; bootstrap owns
whole-file scaffolding and is reserved for explicit scaffold replacement.

When a migration changes generated Wiki schemas, verify runtime support and
validate canonical Markdown before replacing disposable read models:

```bash
farplane wiki doctor --project-root . --json
farplane wiki rebuild --project-root . --no-write --json
farplane wiki rebuild --project-root .
```

Doctor verifies SQLite FTS5/trigram readiness. The dry run returns source and
typed-view diagnostics without writing; the final command atomically rebuilds
Wiki search state, `index.json`, `graph.json`, `crm.json`, and typed views.
Never migrate those generated files by hand; update current consumers for the
new schema first and regenerate from `.farplane/entities/*.md` plus
`.farplane/views.yaml`.

After merging human-owned charter and strategy content, regenerate the runtime
read models and validate the project:

```bash
farplane metrics primitives --project-root . --date <YYYY-MM-DD> --json
farplane project snapshot --project-root . --date <YYYY-MM-DD> --json
python3 bin/validators/check_farplane_project_files.py --root .
```

The primitive command writes Core-owned daily readings under
`.farplane/metrics/daily/`. Provider skills and interval workflows write
validated observation batches under `.farplane/metrics/observations/`. The
project snapshot then joins those readings with the tracked project files for
Farplane UI; it is a projection, not a source of truth.

If you want optional local hooks after bootstrap:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-push
```

Leave `pre-commit` disabled unless the project explicitly wants the heavier
local gate on every commit.

For Node projects, add the Codex SDK reviewer dependencies and scripts:

```bash
npm install --save-dev @openai/codex-sdk tsx
```

Then add package scripts:

```json
{
  "review:agent": "tsx scripts/codex_review_agent.ts",
  "review:prepush": "bash scripts/run_pre_push_review.sh"
}
```

The local diff reviewer reads the installed
`~/.codex/skills/code-review/SKILL.md` contract when the Farplane install script
has linked the skill package. Material review should route through Farplane
reviewer agents and the `review` skill.

### 2. Do not ticketize the whole backlog

Start with:

- one PRD/spec
- one real ticket
- one `impl-plan -> goal-advisor` cycle

Do not migrate every old issue into ticket files at once.

### 3. Front-end funnel first

For an existing repo:

- use `brainstorm` if you still need options
- use direct bootstrap clarification if stack, topology, or quality-gate shape
  is still unclear
- ask focused clarification questions if the first feature slice is unclear
- use `prd` once the first slice is coherent

Then:

- use `spec-to-ticket`
- set the chosen ticket to `status: awaiting_review`
- run `impl-plan`
- after approval set it to `status: todo`; the executing session claims it as `active`
- run `goal-advisor`

### 4. Keep migration scope small

The first migration slice should only prove:

- ticket structure works
- qa cookbook structure exists for future agent-facing shortcuts and probes
- canonical app and QA launch commands are documented on visible repo surfaces
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

- [ ] `farplane/manifest.json` was compared with the versioned migration entries in `references/FRAMEWORK_CHANGELOG.md`
- [ ] V1 migrations removed product controllers/registries and detached review/evidence stores after migrating active readers
- [ ] `docs/bootstrap-brief.md` exists and captures stack/topology/gate decisions
- [ ] `docs/bootstrap-brief.md` captures local-gate, heavy-check, and CI/deploy-gate decisions
- [ ] `docs/bootstrap-brief.md` captures Codex SDK diff-review policy and code-review skill linkage
- [ ] `docs/bootstrap-brief.md` captures canonical app/QA run paths plus required services and port/env assumptions
- [ ] `docs/bootstrap-brief.md` captures agent-experience/testability decisions
- [ ] `PROJECT_RULES.md` exists
- [ ] `PROJECT_RULES.md` names the authoritative app-only and QA/evidence launch commands
- [ ] `AGENTS.md` exists
- [ ] `ARCHITECTURE.md` exists
- [ ] `docs/features/README.md` exists as the feature-spec home
- [ ] `docs/systems/README.md` exists as the cross-feature system grouping home
- [ ] `farplane/README.md` exists
- [ ] `farplane/manifest.json` records the Farplane project spec version and standard tracked/ignored paths
- [ ] `farplane/harness.yaml` exists or `init_mode=substrate` has a recorded readiness gap
- [ ] `farplane/metrics.yaml` declares at least one measurable objective and defines every objective/guard metric ID
- [ ] every metric definition has exactly one inline `refresh` or valid `refresh_ref` in `farplane/metrics.yaml`, with an explicit source-gap route
- [ ] `farplane/automations.toml` contains exactly one Work Pulse heartbeat plus separate cron records for Feed Scout, Daily BAU, Weekly BAU, self-improvement, and optional scheduled workflows
- [ ] `farplane/bindings.yaml` exists and names non-secret project IDs, URLs, labels, and aliases needed by reusable skills
- [ ] `.agents/skills/README.md` exists as the local capability-skill home
- [ ] `farplane/pm.json` exists when the UI should fold chat and automation thread IDs into one visual project PM
- [ ] Live automation activation, when requested, is handled by
      `automation-advisor` and appends PM-visible thread IDs to `farplane/pm.json`
- [ ] owner-named `.farplane/reports/`, `.farplane/<skill-name>/reports/`, `.farplane/entities/`, `.farplane/wiki/`, `.farplane/views.yaml`, `.farplane/metrics/daily/`, `.farplane/evals/runs/`, and `.farplane/logs/` exist as ignored local state; `views.yaml` starts as `views: {}` and generated Wiki/search/JSON projections exist after the first `farplane wiki rebuild`
- [ ] framework migrations that change Wiki/entity schemas pass `farplane wiki doctor` and `farplane wiki rebuild --no-write --json` before regeneration, and generated schema versions match the current changelog
- [ ] primitive metrics and `.farplane/project/ui/latest.json` were regenerated after canonical project-file migration
- [ ] `python3 bin/validators/check_farplane_project_files.py` passes when the repo has Farplane validators
- [ ] `docs/prd.md`, `docs/features/`, and `docs/MEMORY.md` exist
- [ ] `qa/README.md` and `qa/cookbook/TEMPLATE.md` exist
- [ ] `docs/code_review.md`, `docs/review-agent.md`, and review helper scripts exist
- [ ] one QA cookbook page records the evidence-capture launch path and expected targets
- [ ] `docs/features/README.md` exists
- [ ] `tickets/` structure exists
- [ ] `tickets/archive/` exists for completed tickets
- [ ] `tickets/TASK-0001/ticket.md` exists for `find_customer` with
      `foundation_sequence: 1`
- [ ] `tickets/TASK-0002/ticket.md` exists for `deliver_value`, depends on
      `TASK-0001`
- [ ] `tickets/TASK-0003/ticket.md` exists for `collect_revenue`, depends on
      `TASK-0002`
- [ ] existing foundation ticket paths were preserved individually and any
      partial collision was reported
- [ ] one first ticket exists
- [ ] one first `impl-plan` run is successful
- [ ] one first `goal-advisor` run is successful
- [ ] repeated failures route to ticket evidence, an owner-local guard, or a durable invariant in `docs/MEMORY.md`
