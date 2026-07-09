---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-07-08
framework_template_version: "0.2.2"
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.yaml
  - farplane/automations.toml
  - farplane/products/*/product.md
  - farplane/products.json
  - docs/farplane-framework/reporting.md
  - farplane/bindings.yaml
  - farplane/hooks.json
  - .agents/skills/README.md
  - farplane/pm.json
  - .gitignore
---

# Project Files

Farplane projects separate tracked control files from local runtime state.

```text
farplane/        = tracked project framework config
.agents/skills/ = tracked project-local product skills
.farplane/       = ignored local runtime state, content ledgers, reports, eval runs, and logs
docs/            = tracked human-readable project memory and durable narrative
tickets/         = local visible work queue; README/templates are tracked
skills/          = tracked reusable cross-project or repo skills
```

## Project File Minimality Rule

Project files are declarative state. They may contain identity, goals, product
definitions, thresholds, constraints, refs, and human-approved boundaries.

Project files must not contain algorithms, ordered workflow steps, fallback
procedures, review procedures, learning procedures, or repeated agent
instructions. Extract that behavior into skills, hooks, validators, or ticket
programs where it can be tested.

## Tracked Framework Config

```text
farplane/
  manifest.json
  README.md
  harness.md
  goals.yaml
  products/
    <product>/product.md
    <product>/skill.md
  products.json
  automations.toml
  bindings.yaml
  hooks.json
  pm.json

.agents/
  skills/
    README.md
```

### `farplane/manifest.json`

Versioned project spec manifest. It records which files are standard tracked
project config and which ignored runtime paths should exist locally.

Use `template_uses.farplane-framework` in this JSON file so Farplane can count
which projects are current, stale, or missing for the framework template.

The manifest also carries a small UI-facing project identity block:
`project.name`, `project.description`, and `project.archetype`. Keep it short.
Do not turn the manifest into the product strategy document; detailed mission,
products, goals, and automation prompts live in the project files below.

### `farplane/harness.md`

Static human charter: mission, human thesis, operating principles,
non-tradeoffs, static leverage commitments, allocation guardrails, agent
authority, and change rule.

This file is the one owner for the durable human thesis. Products and goals may
evolve from evidence, but agents must not silently rewrite `harness.md`.
Interval reports may propose harness deltas; applying them requires explicit
human approval.

Allocation guardrails include the static runway rule: active work must justify
burn through revenue, validated learning, proof quality, distribution, reusable
harness leverage, or unblock value. The weekly interval applies that rule to
active projects; the detailed review procedure lives in `interval-update`.

Use YAML front matter plus Markdown sections and stable tables for the harness
charter. Do not put a fenced `harness-program` DSL block in canonical project
harness files. Product pipelines and current product strategy belong in
`farplane/products/<product>/product.md`, the generated product registry lives
at `products.json`, cross-product strategy belongs in structured `goals.yaml`,
and full Codex automation configs belong in `automations.toml`.

### `farplane/goals.yaml`

Project strategy context: north star, value function, goal axes, inline SMART
goals, current milestone, and holds. Each goal axis may carry a
compact `smart_goals` list with `id`, `target`, `kpis`, and `interpretation`.
SMART goals may name `product_refs`; those refs declare which product loops are
allowed to spend recurring attention on the goal. A product ref must resolve to
`farplane/products/<product>/product.md`. Products are subordinate execution
lanes for goals, not peers of the north star.
KPI entries are parseable target pairs:

```yaml
kpis:
  - id: accepted_harness_improvements
    target: 20
    direction: above
  - id: ready_unclaimed_ticket_count
    target: 3
    direction: below
```

Metric refresh prompts, chart shape, units, and pinned status live in
`farplane/bindings.yaml` metric recipes. Product KPI membership lives from the
product side in `farplane/products/<product>/product.md` and must validate
against `bindings.yaml#metrics`. This file may evolve through evidence-backed
goals deltas, but it must stay inside the static charter in
`farplane/harness.md`. Horizon and Goal Advisor procedures live in their
skills, not in this file.

### `farplane/products.json`

Generated machine product index for UI, snapshots, validators, and automation
context. It is generated from product-local `product.md` files and carries
product refs, lane weights, KPI membership, product goals, artifact workflows,
human gates, worker policy, and the goal-product matrix in JSON. Do not
hand-edit it.

```text
farplane/products/*/product.md
  -> farplane/products.json
```

Use the JSON when a tool, UI, automation, or validator needs structured product
data. Humans and agents should inspect the owning product-local `product.md`
files when they need prose strategy or loop context.

### `farplane/products/<product>/product.md`

Canonical product-loop definition and product loop program: product identity,
lane, default allocation, owner skill, local loop refs, human gates, KPI refs,
artifact workflows, product-level goals, current strategy, loop contract,
product loop, and progress-entry shape. The frontmatter is indexed into
`products.json`; the Markdown body is the interval-editable strategy/program
surface. Product goals are stable desired outcomes for the loop. Current
strategy and current hypothesis live in the `Current Strategy` section. Runtime
attempts and learning live in ignored product `progress.md`. Metric refresh
prompts stay in `farplane/bindings.yaml`.

`product.md` is the PM/team surface: what the product exists to move, which
goal and KPI evidence matters, what strategy is currently active, what gates
constrain the loop, and what learning shape the product should write.
`skill.md` is the repeatable execution process for the product's artifacts.
`progress.md` is a product learning notebook, not a Pulse event stream. Write
only entries that change what the product should try next: candidate moves,
selected moves, ticket/artifact refs, feedback results, learned rules, next
levers, blockers, or compact strategy-delta receipts. Beat-level accounting
belongs in Pulse reports and ledgers; strategy rationale belongs in interval
reports; current active strategy belongs in `product.md`.

### `farplane/automations.toml`

Human-reviewable Codex automation desired-state source. It stores full TOML
records for Pulse, Daily Interval, Weekly Interval, optional Monthly Registry
Consolidation, and optional Active-Hours Taste Loop.

Each `[[automations]]` record includes id, name, kind, status, schedule or
RRULE-equivalent fields, workspace/thread target, and the exact `prompt` copied
into the Codex app automation record. Skills stay generic and parameterized.
Prompts here should configure project root, interval windows, source refs,
side-effect gates, and project-specific extensions only. Generic loop behavior
belongs in `pulse-update`, `interval-update`, `consolidate`, and `taste-loop`.

The Active-Hours Taste Loop is the official optional framework heartbeat for
using human taste while the operator is online. It should read active-hours and
project-specific settings from `farplane/automations.toml`, rank candidate
skills with the official Skill Signals, emit a feedback card or Goal Advisor
handoff, and stop. It must not activate itself, create a local runner, edit
target skills directly, or invent fake benchmarks when the honest metric is
human feedback or review.

### Runtime Secrets And `farplane/bindings.yaml`

Secrets are runtime inputs, not tracked project files. Farplane Core resolves
runtime values in this order:

1. process env, including values injected by tools such as Doppler
2. private local fallback/cache `~/.farplane/config.toml`
3. rendered Codex adapter fallback `~/.codex/config.toml`

Use `farplane doctor` to check required key sources, private config file
permissions, optional Doppler availability, and obvious tracked secret
candidates without printing secret values.

### `farplane/bindings.yaml`

Non-secret project coordinates: URLs, handles, safe IDs, labels, aliases,
database names, dashboard links, notification channel labels, Feed Scout source
configuration, and metric recipes. The canonical YAML block contains `project`,
`integrations`, optional `feed_scout`, and `metrics`.

Metric recipes are the single owner for label, product, unit, chart display,
pinned status, metric kind, and one prompt-only refresh instruction:

```yaml
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: productization
    pinned: true
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
    refresh: Count completed tickets whose Reward.kpi_rewards names this KPI and whose proof shows shipped value.
```

Metric `refresh` prompts are inline with each KPI recipe so the reader can
inspect one KPI and see what the interval agent should do. A missing token,
missing file, unavailable API field, or unsupported feedback mechanism should
surface as a `source_gap` observation in the canonical metric observation
batch. Agents may use
skills, local ledgers, CLI/API fetches, ticket searches, or manual notes, but
they should all normalize to one dated batch shape:

```text
.farplane/metrics/observations/<source_id>/YYYY-MM-DD.json
  -> canonical MetricObservationBatch rows for one source run

.farplane/metrics/daily/YYYY-MM-DD.json
  -> optional debug/index snapshot for primitive groups

.farplane/project/ui/latest.json
  -> generated project/company snapshot for Overview, Goals, Products,
     Distribution, News, Cadence, Kanban, Proof, and Memory/Reports tabs,
     including KPI chart series and content-centric metric series
```

Metric-producing scripts should write one `MetricObservationBatch` per source
run:

```json
{
  "schema_version": 1,
  "date": "2026-07-03",
  "source_id": "instagram_account_metrics",
  "status": "available",
  "observations": [
    {
      "metric_id": "instagram_views",
      "date": "2026-07-03",
      "value": 2648,
      "status": "available",
      "payload": {}
    }
  ],
  "gaps": [],
  "payload": {}
}
```

Core owns the schema, writer, validator, Farplane-native reducers, and project
snapshot compiler. Platform skills own their API adapters, credentials, and
platform-specific metric extraction, but their output must validate against the
same `MetricObservationBatch` shape before snapshot compilation.

Goals own SMART targets. Bindings do not carry targets, provider routes, write
paths, or fetcher DSL fields. Do not store secrets or credentials here.

Core primitive reducers live in Farplane Core, not in every initialized
project and not in a skill package. `install.sh` links the global `farplane`
CLI; projects select their data root with `--project-root` or by running from
the project directory:

```bash
farplane metrics primitives --project-root /path/to/project --date <YYYY-MM-DD> --json
farplane metrics primitives --project-root /path/to/project --date <YYYY-MM-DD> --ticket-status rejected --json
farplane project snapshot --project-root /path/to/project --date <YYYY-MM-DD> --json
```

The first-wave primitives are mechanical reducers over Farplane files and local
Codex stores:

```text
fetch_tickets(window, kpi_reward?, status?)
kpis_for_product(product_id, product_md, metric_recipes)
ticket_count_by_kpi(window, kpi_id, status?)
ticket_count_by_product(window, product_id, status?)
kpi_attributed_ticket_ratio(window)
fetch_codex_thread_usage(window, cwd=project_root)
estimate_ai_burn(window, thread_usage, spend_model)
backfill_ticket_thread_associations(mine_runs_root, output_path)
```

Tickets do not carry `product_id` or `created_by`. Product ticket views are
transitive: product -> KPI IDs in `farplane/products/<product>/product.md` ->
tickets whose `Reward.kpi_rewards` include those KPI IDs. Metric mechanics and
source-gap prompts still live in `bindings.yaml`. KPI-attributed ticket ratio
means rewarded tickets divided by touched tickets; it is not proof of who
created or executed the ticket.

AI-planned ticket identity is frontmatter-owned with `rewards.kpi`.
`skills/pulse-update/scripts/list_pulse_board.py` accepts active ticket paths or
a project root, parses that frontmatter marker, and separates
AI-generated/reward-bearing tickets from manual/operator tickets. The body
`## Reward` block remains the expected-reward and guard contract. Manual active
tickets do not block Pulse refill and should not be mechanically repaired by
Pulse unless they are explicitly opted into AI planning with valid
`rewards.kpi` frontmatter plus a matching body reward block.
`.farplane/automation/spawned-threads.jsonl` remains worker/handoff state; it
is not the source of truth for ticket origin.

`.farplane/state/ticket-thread-associations.jsonl` is an ignored support index.
Mine backfill rows use `confidence=completion_only`; they can support completed
ticket drilldowns and rough burn attribution, but they must not satisfy
post-start intervention metrics. A future hook writer can add
`confidence=execution_start_candidate` rows.

Feed Scout config in `feed_scout` declares non-secret watched sources, cadence,
report paths, UI feed paths, and local-first write policy. It must not store raw
fetched items or summaries; those rows belong under `.farplane/feed-scout/` and
`.farplane/reports/feed-scout/`.

The project snapshot joins Feed Scout's daily output into the News tab. Feed
Scout remains the owner of fetching, ranking, and writing daily feed artifacts;
`farplane project snapshot` only reads those artifacts and exposes a stable
`tabs.news` payload for UI rendering.

### `farplane/hooks.json`

Declarative Farplane-native hook configuration. It may contain thresholds,
enabled flags, and hook-specific refs. Hook algorithms and post-action behavior
belong in hook scripts or skills.

### `.farplane/content/ledger.jsonl`

Ignored local runtime ledger for owned content created, approved, posted, and
measured by a project. Farplane Core owns the local schema and CLI write path;
Farplane UI renders it in the Distribution tab, but does not own the file
contract.

Each row is one content item:

```json
{
  "content_id": "instagram:reel-123",
  "platform": "instagram",
  "external_id": "reel-123",
  "url": "https://...",
  "status": "posted",
  "approval": "approved",
  "published_at": "2026-07-02T10:00:00Z",
  "campaign": "evidence_distribution",
  "kpis": ["instagram_views", "evidence_distribution_reach"],
  "approval_ref": "tickets/TASK-0001/ticket.md"
}
```

Allowed statuses are `idea`, `draft`, `approved`, `posted`, `measured`, and
`archived`. Allowed approval values are `not_required`, `requested`,
`approved`, and `rejected`.

Publishing skills must append or update a row after confirmed account mutation
using `farplane content add`. Metric refresh uses this ledger to select posted
content for platform metric fetches and writes aggregate values plus
`payload.items` into `.farplane/metrics/daily/YYYY-MM-DD.json`. The project
snapshot preserves those payloads in `metrics.series[]` and also derives
`metrics.contents[]`, where each content item has its own per-KPI time series
for distribution-tab drilldown.

Supported local commands:

```bash
python3 bin/farplane.py content add --platform instagram --external-id <media_id> --status posted --approval approved --published-at <iso> --kpis instagram_views,instagram_likes,evidence_distribution_reach
python3 bin/farplane.py content validate
python3 bin/farplane.py content select --platform instagram --kpi instagram_views --date <YYYY-MM-DD> --window-days 7
```

`content validate` reports malformed JSONL, invalid statuses, invalid approval
values, missing KPI lists, duplicate `content_id` rows, and invalid timestamps.
`content select` returns exact external IDs plus a platform-specific fetch
command hint, or `status=source_gap` when the ledger or matching posted rows are
missing. It does not call external accounts.

### `.agents/skills/`

Project-local product skills. Use this for monetizable or company-specific
workflows derived from `farplane/products/<product>/product.md` and the
generated `farplane/products.json` registry, such as
`.agents/skills/<product-skill>/SKILL.md`.

These local skills are referenced by tickets, interval reports, or automation
prompts by path. Promote a local product skill to root `skills/` only after
repeated runs show that it is reusable across projects.

### `farplane/pm.json`

Optional UI glue for grouping multiple Codex threads under one persistent
employee/PM agent in the Farplane UI. It is not loop state, scheduler state, or
an automation registry.

```json
{
  "version": 1,
  "name": "Project PM",
  "role": "founder_operator",
  "threads": {
    "chats": [],
    "automations": []
  }
}
```

Use `threads.chats` for persistent chat or worker threads that should render
under the same employee agent. Use `threads.automations` for automation-owned
threads that should also render under that employee. Threads not listed here
may appear as ephemeral agents in the UI.

## Local Work State

InitAdvisor owns the generated `.gitignore` block for Farplane local work in
`skills/init-advisor/references/GITIGNORE_TEMPLATE`:

```gitignore
# Farplane local runtime and work state
.farplane/
tickets/**
!tickets/README.md
!tickets/templates/
!tickets/templates/**
.agents/*
!.agents/skills/
!.agents/skills/**
```

Active tickets such as `tickets/TASK-0001/ticket.md` are local execution state
by default. Commit shared ticket scaffolding such as `tickets/README.md` and
`tickets/templates/`, but keep project-specific active work, reports, logs,
eval runs, and non-skill agent state out of normal commits unless the repo has
an explicit reason to version them.

Ticket reward metadata is split between a small frontmatter identity marker and
the human-readable spend-justification block. AI-planned tickets use
frontmatter `rewards.kpi`:

```yaml
rewards.kpi:
  - accepted_harness_improvements
```

Then the body `## Reward` block carries expected reward and guard detail:

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "one proof-backed shipped harness improvement"
    check_in_at: "2026-07-15T09:00:00+08:00"
    actual_result:
    reward_score:
    reward_score_reason:
guard: "count only after completion proof; stop before expanding scope"
```

Only KPI recipes whose source is `ticket_reward_feedback` become ticket-derived
metric values. Rewards for externally sourced KPIs are planning attribution
only; the metric value still comes from its configured source. `check_in_at`
marks when interval update should compare the expected reward against observed
reality. `actual_result`, `reward_score`, and `reward_score_reason` are filled
by the reward-checkin analyzer. `reward_score` is a scalar from `-1` to `1`,
where `1` means the actual result strongly matched or exceeded the expectation,
`0` means unclear or weakly related, and `-1` means the actual contradicted the
expectation or created negative value.

## Ignored Runtime State

```text
.farplane/
  README.md
  state/run-ledger.json
  automation/
  reports/
  evals/runs/
  logs/
```

### `.farplane/automation/`

Mutable Pulse automation state:

- Pulse decision rows
- reward observations
- spawned worker thread rows
- normalized action outcomes

### Report Standard

The Core-owned report standard lives in [Reporting](reporting.md). It defines
the minimal Markdown frontmatter required for UI indexing:

```yaml
ref: reports/interval/daily_interval/2026-07-08T053300+0800
kind: interval-report
created_at: "2026-07-08T05:33:00+08:00"
ui_summary: "One concise report-card summary under 100 words."
```

`ref` is the only hierarchy field. Consumers derive parent/child/group
relationships from slash-separated `ref` prefixes. The standard is not a
project primitive file; it is framework documentation plus the Core registry
builder.

### `.farplane/reports/`

Generated reports. New framework reports should be date-stamped:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/context/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/dogfood-review/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/index.json
```

Consumers find newest interval reports by timestamp sorting or explicit links
from later reports. There is no tracked scheduler config just to store
`last_report`.

Reports expose UI report-card fields in YAML frontmatter. Consumers should read
`.farplane/reports/index.json` when present, or parse Markdown frontmatter with
the same minimal contract:

```yaml
ref: reports/interval/daily_interval/2026-07-08T053300+0800
kind: interval-report
created_at: "2026-07-08T05:33:00+08:00"
ui_summary: "Refresh the active frontier after the KPI/autonomy metric chain completed; clear review-gated KPI/content/QA surfaces; protect the simplified metric loop."
```

Run `farplane reports index --project-root <project>` to rebuild the registry.
Run `farplane reports repair-refs --project-root <project>` when existing
report Markdown has valid frontmatter but lacks the canonical path-derived
`ref`.
The index scans `<project>/.farplane/reports/**/*.md`, includes only reports
with non-empty `ref`, `kind`, `created_at`, and `ui_summary`, derives
`parent_ref` and `children_refs` from `ref`, and preserves pass-through
frontmatter such as `project`, `automation_id`, `interval_id`,
`report_workflows`, `status`, `review_window`, `planning_window`, and
`context_bundle`.

Keep `ui_summary` under 100 words. CRM/customer research reports under
`.farplane/crm/reports/*`, ticket QA/review artifacts, `.farplane/reviews/*`,
mining runs, backfill jobs, and event-miner runs are not part of the main
reports registry unless explicitly opted in by a future ticket.

## Validation

Run:

```bash
python3 bin/validators/check_farplane_project_files.py
```

The validator checks the current manifest shape, retired file names, required
`harness.md` static-charter headings, absence of fenced harness-program DSL in
canonical harness files, duplicate active charter files such as
`farplane/project.md`, product-catalog headings, hooks JSON shape, bindings
front matter, and obvious secret leakage.
