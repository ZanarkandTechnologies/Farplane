---
kind: farplane-framework-reporting-standard
status: active
created_at: 2026-07-08
updated_at: 2026-07-08
framework_template_version: "0.1.0"
---

# Farplane Reporting

Farplane Core owns the report-card contract for project reports under
`.farplane/reports/`. Report-producing skills write Markdown reports with YAML
frontmatter. Farplane Core builds `.farplane/reports/index.json` from those
files so UI clients do not define their own report standard.

```text
farplane reports index --project-root <project> -> .farplane/reports/index.json
```

## Current System Status

The reporting system is in place at the Core registry layer:

- Implemented: `farplane reports index` scans report Markdown and writes
  `.farplane/reports/index.json`.
- Implemented: the project snapshot report cards consume the same Core registry
  builder.
- Implemented: Interval, Pulse, Feed Scout, Taste Loop, and Dogfood report
  producer contracts require `ref`, `kind`, `created_at`, and `ui_summary`.
- Not backfilled: historical ignored reports that lack `ref` are excluded until
  a future migration or new report production supplies the minimal frontmatter.
- Not included by default: CRM/customer research reports, ticket QA/review
  artifacts, review runs, mining runs, backfill jobs, and event-miner runs.

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
reports/taste-loop/<timestamp>/<workflow-or-ticket>
reports/dogfood-review/<timestamp>
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

Use `.farplane/crm/reports/*` and its own index for CRM/customer research unless
a future ticket explicitly opts those reports into the main project registry.
Ticket QA/review/mining/backfill artifacts stay outside this registry by
default.
