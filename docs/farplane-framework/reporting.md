---
kind: farplane-framework-reporting-standard
status: active
created_at: 2026-07-08
updated_at: 2026-08-19
framework_template_version: "0.1.3"
---

# Farplane Reporting

Farplane Core owns the report-card contract for project reports under
`.farplane/reports/`. Report-producing skills write Markdown reports with YAML
frontmatter. Farplane Core builds `.farplane/reports/index.json` from those
files so UI clients do not define their own report standard.

```text
farplane reports index --project-root <project> -> .farplane/reports/index.json
farplane reports repair-refs --project-root <project> -> add missing path refs + rebuild index
```

## Current System Status

The reporting system is in place at the Core registry layer:

- Implemented: `farplane reports index` scans report Markdown and writes
  `.farplane/reports/index.json`.
- Implemented: the project snapshot report cards consume the same Core registry
  builder.
- Implemented: Interval, Pulse, Feed Scout, and Dogfood report
  producer contracts require `ref`, `kind`, `created_at`, and `ui_summary`.
- Implemented: `farplane reports repair-refs` adds path-derived `ref`
  frontmatter to existing report Markdown when frontmatter is present, then
  rebuilds the registry.
- Historical reports missing other required card fields stay excluded until a
  producer or human supplies truthful `kind`, `created_at`, and `ui_summary`.
- Not included by default: CRM/customer research reports, ticket QA/review
  artifacts, review runs, mining runs, backfill jobs, and event-miner runs.

Skill-local memory reports use `.farplane/<skill-name>/reports/**/*.md`. They
may be discovered across skills with `.farplane/*/reports/**/*.md`, but they do
not require a compiled index or the Core report-card frontmatter contract.

## Human Reading Contract

Report metadata and report readability are separate contracts. UI-indexed
reports keep the Core frontmatter below. Analytical report bodies should use
the decision-first spine in
`docs/templates/HUMAN_REPORT_TEMPLATE.md` when their producer adopts it:

```text
decision -> situation map -> material findings -> risks -> next action -> supporting evidence
```

The human body owns the conclusion and the shortest honest path to action.
Supporting artifacts own exhaustive ledgers, raw observations, and machine
receipts. A canonical receipt should preserve authority, mutations, validation,
and stop state in structured form; the human report links it instead of
repeating it as prose. This boundary reduces reading cost without deleting
proof or changing downstream machine state.

Use one compact diagram only when it makes a relationship or state transition
materially easier to understand. Empty sections, workflow instructions,
repeated summaries, and duplicate evidence are not report content.

## Minimal Report Frontmatter

Every UI-indexed project report must include:

```yaml
ref: reports/interval/daily_interval/2026-07-08T053300+0800
kind: interval-report
created_at: "2026-07-08T05:33:00+08:00"
ui_summary: "One concise report-card summary under 100 words."
```

- `ref` is the single hierarchy field. Derive parents, children, and groups from
  slash-separated `ref` prefixes.
- `kind` remains explicit even when it can be inferred from `ref`, so reports
  survive path moves.
- `created_at` is the report creation timestamp.
- `ui_summary` is the compact card summary. Keep it under 100 words.

Do not add `parent_id`, `group_id`, or `role` to report frontmatter until a
ticket proves that prefix-derived hierarchy is insufficient.

## Canonical Refs

```text
reports/interval/daily_interval/<timestamp>
reports/interval/daily_interval/<timestamp>/feed-scout
reports/pulse/<timestamp>
reports/feed-scout/<timestamp>
reports/dogfood-review/<timestamp>
reports/interval/<interval_id>/context/<timestamp>
```

The physical Markdown path usually mirrors the `ref`, but `kind` and `ref` are
the canonical UI contract. Existing interval frontmatter such as `project`,
`automation_id`, `interval_id`, `report_workflows`, `status`, `review_window`,
`planning_window`, and `context_bundle` should stay in place as pass-through
metadata.

## Registry

Core scans:

```text
<project>/.farplane/reports/**/*.md
```

It includes only Markdown files whose frontmatter has non-empty `ref`, `kind`,
`created_at`, and `ui_summary`. Malformed or incomplete files are skipped and
listed in `issues`.

Each indexed report includes:

```json
{
  "ref": "reports/interval/daily_interval/2026-07-08T053300+0800/feed-scout",
  "kind": "feed-scout",
  "created_at": "2026-07-08T05:34:00+08:00",
  "ui_summary": "Feed Scout surfaced two reusable harness patterns.",
  "path": ".farplane/reports/interval/daily_interval/2026-07-08T053300+0800/feed-scout.md",
  "parent_ref": "reports/interval/daily_interval/2026-07-08T053300+0800",
  "children_refs": [],
  "frontmatter": {}
}
```

Customer research uses `.farplane/customer-research/reports/*` and links
canonical entities through `entity_refs`. Entity source state lives in flat
`.farplane/entities/*.md`; `manage-wiki` owns durable article mutation and
`farplane wiki sync` generates `.farplane/wiki/wiki.sqlite` plus
`.farplane/entities/index.json`, `graph.json`, and `crm.json`. Wiki articles
have no handwritten report backlinks. A
future ticket may opt selected skill-local reports into the main
project registry by adopting the Core report-card contract.
Ticket QA/review/mining/backfill artifacts stay outside this registry by
default.

## Interval Highlight Ledgers

Daily and Weekly Interval may append presentation highlights after the source
report is finalized:

```text
.farplane/highlights/wins.jsonl
.farplane/highlights/failures.jsonl
```

The canonical rows are deliberately smaller than report cards:

```json
{"team":"farplane","report":"reports/interval/daily/2026-07-24","summary":"Activation beat the prior record.","links":[".farplane/metrics/activation.jsonl"]}
{"team":"farplane","report":"reports/interval/daily/2026-07-24","summary":"A simple correction stalled in delegation.","lesson":"Do the bounded correction directly when delegation costs more than the work.","links":["tickets/TASK-0400/ticket.md"]}
```

Wins contain `{team, report, summary, links?}`. Failures add `lesson`.
Identity is the natural composite `(kind, team, report)`. Core resolves the
source report and derives card IDs, project, cadence, period, timestamp, and
display labels into the replaceable project UI snapshot. The UI must not parse
report prose or require Convex/team-board state to render these galleries.

## Repair

Use the explicit repair command when existing report Markdown has valid
frontmatter but lacks only the canonical path ref:

```text
farplane reports repair-refs --project-root <project>
```

The repair derives `ref` from the Markdown path under `.farplane/` without the
`.md` extension. For example,
`.farplane/reports/interval/daily_interval/2026-07-07T213501Z.md` becomes
`reports/interval/daily_interval/2026-07-07T213501Z`. The command does not
invent missing `kind`, `created_at`, or `ui_summary`; those files remain
reported as excluded issues after the index is rebuilt.
