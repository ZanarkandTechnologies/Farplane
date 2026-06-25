# Init Advisor

Bootstrap or migrate a project into the Farplane docs-first, ticket-first
harness model. Init sets up the project substrate first, can optionally run a
code/app scaffold such as Next.js, React, or Convex, and then leaves a starter
PRD ticket for the next phase.

This setup should scaffold optional `.githooks` samples plus project-local
`scripts/pre_*_check.sh` files for local quality gates, a Codex SDK pre-push
diff-review loop, plus repo-owned runtime and `qa/` guidance so agents can
launch the app and capture evidence without guessing, all without enabling
hooks automatically.

Every initialized project is a Farplane project by default. Use
`init_mode=substrate` for substrate-only migrations, and `init_mode=full` when
the operator also wants the project operating model shaped during setup.

## Use Cases

- **Greenfield**: start a new repo with the full scaffold
- **Brownfield**: add the harness structure to an existing repo without rewriting the app

## Greenfield

Use the bootstrap script:

```bash
bash ~/.codex/skills/init-advisor/scripts/bootstrap.sh
```

Before finalizing the scaffold, run a bootstrap intake with the same discipline
as `deep-interview` and keep the answers in `docs/bootstrap-brief.md`.
That intake should explicitly answer whether local hooks should be enabled, what
belongs in `pre-push` or `pre-commit`, whether the Codex SDK diff reviewer
should be advisory or strict, which heavy local checks such as `desloppify` or
CodeRabbit are desired, and whether a separate CI/deployment gate exists. It
should also name the canonical app-only run path, canonical full QA or
evidence-capture path, required services such as DB or orchestration tools, and
any port or environment-variable assumptions. When the user wants app code
created during init, select the stack scaffold before running commands.

That also writes `farplane/README.md`, `farplane/manifest.json`, `farplane/harness.md`,
`farplane/goals.md`, `farplane/automations.md`, `farplane/bindings.md`,
`farplane/hooks.json`, `farplane/skills/README.md`, `farplane/pm.json`, `docs/bootstrap-brief.md`, `qa/README.md`,
`qa/cookbook/TEMPLATE.md`, `.githooks/README.md`,
`.githooks/pre-commit`, `.githooks/pre-push`, `scripts/pre_commit_check.sh`,
`scripts/pre_push_check.sh`, review docs, and review-agent helper scripts as
opt-in samples. The recommended default is to keep the large-file scan, fill in
lint/typecheck/test/build commands, run advisory Codex SDK diff review during
pre-push, and activate only `pre-push` unless the repo wants an extra
pre-commit gate. The other required follow-through is to fill
`PROJECT_RULES.md` and `qa/` with the authoritative launch path agents should
use for ordinary app work versus QA. It also creates
`tickets/TASK-0001/ticket.md` as the starter PRD handoff.

The script also creates ignored `.farplane/` runtime folders:
`.farplane/state/run-ledger.json`, `.farplane/reports/`,
`.farplane/evals/runs/`, and `.farplane/logs/`. Keep canonical framework
config in tracked `farplane/`; use `.farplane/` for generated local state only.

Bootstrap does not create live Codex automations by itself. After the substrate
exists, use `harness-creator` in full mode to shape the static charter,
products, goals, feedback loops, and current milestone. `harness-creator`
routes to `horizon-advisor` or `goal-advisor` only when those narrower advisor
calls are needed. When live loops are explicitly requested, use
`automation-advisor` to activate Pulse, Daily Interval, and Weekly Interval.
Activation creates or reuses the dedicated loop threads, creates or updates the
Codex automations, and appends PM-visible thread IDs to `farplane/pm.json`.

Optional code scaffold recipes live in `SKILL.md` under `Code Scaffold Recipes`.
Use the selected recipe during init when requested, but stop for interactive
cloud setup, credentials, billing, deploys, and destructive actions.

After init, follow the planning funnel:

```text
brainstorm -> deep-interview -> horizon-advisor -> goal-advisor
prd -> spec-to-ticket -> impl-plan -> goal-advisor
```

## Brownfield Migration

If the repo already exists, do the smallest migration first.

### 1. Add the harness structure

```bash
mkdir -p docs/specs tickets tickets/archive tickets/templates
touch ARCHITECTURE.md docs/prd.md docs/HISTORY.md docs/MEMORY.md docs/TROUBLES.md docs/LESSONS.md docs/specs/README.md
```

Then copy in:

- `PROJECT_RULES.md`
- `AGENTS.md`
- `ARCHITECTURE.md`
- `farplane/README.md`
- `farplane/manifest.json`
- `farplane/harness.md`
- `farplane/goals.md`
- `farplane/automations.md`
- `farplane/bindings.md`
- `farplane/hooks.json`
- `farplane/skills/README.md`
- `farplane/pm.json`
- `docs/TASTE.md`
- `qa/`
- `tickets/templates/ticket.md`

The bootstrap script can still help:

```bash
bash ~/.codex/skills/init-advisor/scripts/bootstrap.sh .
```

Use `--force` only if you want to overwrite files that already exist.

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
has linked the skill package. CodeRabbit remains an optional heavier external
review pass when installed and explicitly configured.

### 2. Do not ticketize the whole backlog

Start with:

- one PRD/spec
- one real ticket
- one `impl-plan -> goal-advisor` cycle

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

- [ ] `docs/bootstrap-brief.md` exists and captures stack/topology/gate decisions
- [ ] `docs/bootstrap-brief.md` captures local-hook, heavy-check, and CI/deploy-gate decisions
- [ ] `docs/bootstrap-brief.md` captures Codex SDK diff-review policy and code-review skill linkage
- [ ] `docs/bootstrap-brief.md` captures canonical app/QA run paths plus required services and port/env assumptions
- [ ] `docs/bootstrap-brief.md` captures agent-experience/testability decisions
- [ ] `PROJECT_RULES.md` exists
- [ ] `PROJECT_RULES.md` names the authoritative app-only and QA/evidence launch commands
- [ ] `AGENTS.md` exists
- [ ] `ARCHITECTURE.md` exists
- [ ] `farplane/README.md` exists
- [ ] `farplane/manifest.json` records the Farplane project spec version and standard tracked/ignored paths
- [ ] `farplane/harness.md` exists or `init_mode=substrate` has a recorded readiness gap
- [ ] `farplane/goals.md` exists or `init_mode=substrate` has a recorded readiness gap
- [ ] `farplane/automations.md` exists and contains the exact Pulse, Daily Interval, and Weekly Interval prompt blocks to copy into Codex automations
- [ ] `farplane/bindings.md` exists and names non-secret project IDs, URLs, labels, and aliases needed by reusable skills
- [ ] `farplane/hooks.json` exists or `init_mode=substrate` has a recorded readiness gap
- [ ] `farplane/skills/README.md` exists as the local product-skill home
- [ ] `farplane/pm.json` exists when the UI should fold chat and automation thread IDs into one visual project PM
- [ ] Live automation activation, when requested, is handled by
      `automation-advisor` and appends PM-visible thread IDs to `farplane/pm.json`
- [ ] `.farplane/state/run-ledger.json`, `.farplane/reports/`, `.farplane/evals/runs/`, and `.farplane/logs/` exist as ignored local runtime state
- [ ] `python3 bin/validators/check_farplane_project_files.py` passes when the repo has Farplane validators
- [ ] `docs/prd.md`, `docs/specs/`, `docs/TROUBLES.md`, `docs/LESSONS.md` exist
- [ ] `qa/README.md` and `qa/cookbook/TEMPLATE.md` exist
- [ ] `docs/code_review.md`, `docs/review-agent.md`, and review helper scripts exist
- [ ] one QA cookbook page records the evidence-capture launch path and expected targets
- [ ] `docs/specs/README.md` exists
- [ ] `tickets/` structure exists
- [ ] `tickets/archive/` exists for completed tickets
- [ ] `tickets/TASK-0001/ticket.md` exists as the initial PRD handoff
- [ ] one first ticket exists
- [ ] one first `impl-plan` run is successful
- [ ] one first `goal-advisor` run is successful
- [ ] repeated failures get logged to `docs/TROUBLES.md`
- [ ] reusable post-fix lessons get distilled into `docs/LESSONS.md`
