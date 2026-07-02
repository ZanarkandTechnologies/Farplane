---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-07-02
framework_template_version: "0.2.2"
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.md
  - farplane/automations.toml
  - farplane/products.md
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
rows, thresholds, constraints, refs, and human-approved boundaries.

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
  goals.md
  products.md
  ops-memory.md
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

Use YAML front matter plus Markdown sections and stable tables. Do not put a
fenced `harness-program` DSL block in canonical project harness files. Product
pipelines belong in `products.md`, current strategy belongs in `goals.md`, and
full Codex automation configs belong in `automations.toml`.

### `farplane/goals.md`

Project strategy context: north star, value function, goal axes, inline SMART
goals, current bets, current milestone, and holds. Each goal axis may carry a
compact `smart_goals` list with `id`, `target`, `kpis`, and `interpretation`.
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

Metric refresh prompts, chart shape, units, and pinned status live in `farplane/bindings.yaml`
metric recipes. This file may evolve through evidence-backed goals deltas, but
it must stay inside the static charter in `farplane/harness.md`. Horizon and
Goal Advisor procedures live in their skills, not in this file.

### `farplane/products.md`

Project product catalog: team identity, product rows, work-lane weights, and
constraints. Products are not chores. Interval planners consume this data;
the planning/refill procedure lives in `interval-update`.

Use Markdown with YAML front matter and the standard headings `Team`,
`Products`, `Work Lanes`, and `Constraints`.

### `farplane/ops-memory.md`

Active operating memory: the compact, mutable place for what the autonomous
team is doing now. It records current focus, active projects, tracked feedback
refs, next frontier, constraints, parking lot, recent decisions, and Pulse
notes. Stable strategy stays in `farplane/goals.md`; product lanes stay in
`farplane/products.md`; executable work stays in `tickets/`; dated receipts
stay under `.farplane/reports/`.

Use the template in
`skills/init-advisor/references/OPS_MEMORY_TEMPLATE.md`. Keep the headings
stable enough that agents can skim and update them, but do not treat the file as
a deterministic database. The interval agent may semantically read active
project fields such as `lane`, `goal_axes`, `contribution_mode`,
`weekly_runway_decision`, `expected_reward`, `done_signal`, `critical_path`,
and `next_frontier`; missing or stale fields become observation gaps, planning
requests, or instrumentation tickets.

The recommended sections are:

| Section | Purpose | Update owner |
| --- | --- | --- |
| `Current Focus` | One compact statement of the active frontier. | Daily/Weekly Interval, Pulse when reporting stale focus. |
| `Active Projects` | Flexible project blocks with contribution mode, runway decision, expected reward, done signals, critical path, and next frontier. | Weekly Interval, with Pulse citing relevant blocks for tactical tickets. |
| `Tracked Feedback` | Content refs, customer/user feedback refs, runtime/product feedback refs, and observation gaps that help agents choose skill, CLI, or ticket searches. | Daily/Weekly Interval or explicit feedback-capture tickets. |
| `Next Frontier` | Primary and secondary next moves that should bias planning. | Daily/Weekly Interval. |
| `Constraints` | Local reminders that ops-memory cannot authorize goals/products, spend, publishing, accounts, deploys, or customer contact. | Human-approved policy or interval report. |
| `Parking Lot` | Real ideas that should not consume active budget this week. | Weekly Interval. |
| `Recent Decisions` | Compact decision notes that affect near-term planning. | Daily/Weekly Interval. |
| `Pulse Notes` | Instructions for how Pulse should cite, distrust, or use ops-memory. | Pulse/Interval contract updates. |

Do not store raw metric values here when the daily metrics file can own them.
Use `Tracked Feedback` for refs and tracking intent; store daily readings under
`.farplane/metrics/daily/` and render UI trends from
`.farplane/metrics/ui/latest.json`.

For autonomous growth and owned-content distribution, store posted/draft content
tracking rows in `.farplane/content/ledger.jsonl`, not in ops memory. Ops memory
may summarize the active campaign or next frontier; the content ledger owns
repeatable fetch targets for publishing skills, interval metric refresh, and
future UI distribution views.

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
surface as a `source_gap` reading in the daily metrics file. Agents may use
skills, local ledgers, CLI/API fetches, ticket searches, or manual notes, but
they should all normalize to one dated file:

```text
.farplane/metrics/daily/YYYY-MM-DD.json
  -> { date, metrics: { [metric_id]: { value, status, payload? } } }

.farplane/metrics/ui/latest.json
  -> {
       schema_version: 2,
       metrics: [...KPI chart series...],
       contents: [...content-centric metric series...]
     }
```

Goals own SMART targets. Bindings do not carry targets, provider routes, write
paths, or fetcher DSL fields. Do not store secrets or credentials here.

Feed Scout config in `feed_scout` declares non-secret watched sources, cadence,
report paths, UI feed paths, and local-first write policy. It must not store raw
fetched items or summaries; those rows belong under `.farplane/feed-scout/` and
`.farplane/reports/feed-scout/`.

### `farplane/hooks.json`

Declarative Farplane-native hook configuration. It may contain thresholds,
enabled flags, and hook-specific refs. Hook algorithms and post-action behavior
belong in hook scripts or skills.

### `.farplane/content/ledger.jsonl`

Ignored local runtime ledger for owned content created, approved, posted, and
measured by a project. Farplane Core owns the local schema and CLI write path;
Farplane UI may render it as a distribution tab, but does not own the file
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
`payload.items` into `.farplane/metrics/daily/YYYY-MM-DD.json`. The compiler
preserves those payloads in KPI series and also derives
`.farplane/metrics/ui/latest.json.contents[]`, where each content item has its
own per-KPI time series for distribution-tab drilldown.

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
workflows derived from `farplane/products.md`, such as
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

Ticket `Reward` blocks are the spend-justification and KPI-attribution
primitive for tactical work. Use parseable `kpi_rewards` pairs plus a `guard`:

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "one proof-backed shipped harness improvement"
guard: "count only after completion proof; stop before expanding scope"
```

Only KPI recipes whose source is `ticket_reward_feedback` become ticket-derived
metric values. Rewards for externally sourced KPIs are planning attribution
only; the metric value still comes from its configured source.

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

### `.farplane/reports/`

Generated reports. New framework reports should be date-stamped:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md
```

Consumers find newest interval reports by timestamp sorting or explicit links
from later reports. There is no tracked scheduler config just to store
`last_report`.

Interval reports expose UI report-card metadata in frontmatter under
`ui_summary`. Consumers should parse YAML frontmatter, not prose sections. The
stable card contract is:

```yaml
ui_summary:
  schema_version: 1
  title: Daily Interval Update
  date: "2026-07-02"
  report_type: interval
  interval_id: daily_interval
  deep_link_path: .farplane/reports/interval/daily_interval/2026-07-01T213611Z.md
  summary_bullets:
    - Refresh the active frontier after the KPI/autonomy metric chain completed.
    - Clear review-gated KPI/content/QA surfaces.
    - Protect the simplified metric loop.
  highlights: []
  metrics: []
  blockers:
    - Ops memory primary frontier points at completed TASK-0251.
  next_actions:
    - Refresh active ops-memory frontier.
```

`summary_bullets` should contain 3-5 compact outcomes. `highlights`,
`metrics`, `blockers`, and `next_actions` are optional arrays; emit an empty
array when no item applies. `deep_link_path` is the local report path to open for
the full Markdown report.

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
