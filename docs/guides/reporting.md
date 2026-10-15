---
title: "Reporting"
status: active
owner: harness
created_at: 2026-07-08
updated_at: 2026-10-15
framework_template_version: "0.2.0"
tags:
  - farplane
  - reports
refs:
  - bin/core/farplane_reports.py
  - skills/report-gen/templates/human-report.md
  - skills/feed-scout/templates/feed-scout-report.md
  - docs/guides/work-loop.md
---

# Reporting

Where reports live, which ones the UI indexes, and how a report reads. Farplane
Core owns the report-card contract for project reports under
`.farplane/reports/`: producers write Markdown with YAML frontmatter, and Core
builds `.farplane/reports/index.json` from those files so UI clients do not
define their own report standard.

```text
farplane reports index --project-root <project>       -> .farplane/reports/index.json
farplane reports repair-refs --project-root <project> -> add missing path refs + rebuild index
```

## Where Reports Live

| Report | Path | Indexed? |
| --- | --- | --- |
| Feed Scout source report (Intel Digest) | `.farplane/reports/feed-scout/<timestamp>.md` plus `latest.json` | yes; its template carries the four card fields |
| Thread Sweeper run log | `.farplane/reports/thread-sweeper/<YYYY-MM-DD>.md` | only if it carries the four card fields |
| Morning brief, Project Memory, weekly Project and company reports (`report-gen`) | `.farplane/company-os/daily/briefs/`, `.farplane/company-os/weeks/<week>/...` | no; read through the Morning and weekly records |
| Skill-local reports (prospect cases, research, calls, offers) | `.farplane/<skill>/reports/**/*.md` | no |
| Issue QA, review, mining, and backfill artifacts | linked from the issue | never |

Only reports under `.farplane/reports/` with all four card fields are indexed.
Skill-local reports live in `.farplane/<skill>/...`, can be discovered across
skills with `.farplane/*/reports/**/*.md`, and need no compiled index or card
frontmatter. A skill opts a report into the main registry only by adopting the
card contract below. The retired Interval and Work Pulse producers no longer
write reports; their older files under `.farplane/reports/interval/` and
`.farplane/reports/pulse/` stay readable.

## Card Frontmatter

Every UI-indexed report includes:

```yaml
ref: reports/feed-scout/2026-10-15T053300+0800
kind: feed-scout
created_at: "2026-10-15T05:33:00+08:00"
ui_summary: "One concise report-card summary under 100 words."
```

- `ref` is the single hierarchy field. Parents, children, and groups derive
  from slash-separated `ref` prefixes.
- `kind` stays explicit even when it can be inferred from `ref`, so reports
  survive path moves.
- `created_at` is the report creation timestamp.
- `ui_summary` is the compact card summary, under 100 words.

Do not add `parent_id`, `group_id`, or `role` until an issue proves that
prefix-derived hierarchy is insufficient. The physical Markdown path usually
mirrors `ref`, but `kind` and `ref` are the canonical UI contract. Other
producer frontmatter (`project`, `status`, `review_window`, and similar) stays
in place as pass-through metadata.

## Registry

Core scans `<project>/.farplane/reports/**/*.md` and includes only files whose
frontmatter has non-empty `ref`, `kind`, `created_at`, and `ui_summary`.
Malformed or incomplete files are skipped and listed in `issues`; historical
reports missing a field stay excluded until a producer or human supplies a
truthful value. The project snapshot report cards use the same Core builder.
Each indexed report looks like this (`parent_ref` is the nearest indexed ancestor ref, else null):

```json
{
  "ref": "reports/feed-scout/2026-10-15T053300+0800",
  "kind": "feed-scout",
  "created_at": "2026-10-15T05:33:00+08:00",
  "ui_summary": "Feed Scout surfaced two reusable harness patterns.",
  "path": ".farplane/reports/feed-scout/2026-10-15T053300+0800.md",
  "parent_ref": null,
  "children_refs": [],
  "frontmatter": {}
}
```

## Repair

`farplane reports repair-refs --project-root <project>` adds a path-derived
`ref` to existing report Markdown that has frontmatter but no `ref`, then
rebuilds the index. The ref is the path under `.farplane/` without `.md`:
`.farplane/reports/feed-scout/2026-10-15T053300+0800.md` becomes
`reports/feed-scout/2026-10-15T053300+0800`. It never invents `kind`,
`created_at`, or `ui_summary`; files missing those stay listed as excluded.

## How A Report Reads

Report metadata and readability are separate contracts. Analytical report
bodies use the decision-first spine in
`skills/report-gen/templates/human-report.md` when their producer adopts it:

```text
decision -> situation map -> material findings -> risks -> next action -> supporting evidence
```

The body owns the conclusion and the shortest honest path to action.
Supporting artifacts own exhaustive ledgers, raw observations, and machine
receipts. A canonical receipt keeps authority, mutations, validation, and stop
state in structured form; the report links it instead of repeating it as
prose. This cuts reading cost without deleting proof or changing downstream
machine state.

Use one compact diagram only when it makes a relationship or state transition
materially easier to understand. Empty sections, workflow instructions,
repeated summaries, and duplicate evidence are not report content.

## Entities In Reports

Skill-local reports link canonical Wiki pages through `entity_refs` (for
example prospect cases at `.farplane/prospect/reports/`). Pages under
`.farplane/entities/*.md` are the entity source; `manage-wiki` owns article
changes, and `farplane wiki sync` or `farplane wiki rebuild` regenerates the
Wiki database and JSON projections ([Wiki And Entities](wiki-and-entities.md)).
Wiki articles carry no handwritten report backlinks.

## Highlight Ledgers

The project snapshot still reads two optional presentation ledgers:

```text
.farplane/highlights/wins.jsonl
.farplane/highlights/failures.jsonl
```

```json
{"team":"farplane","report":"reports/feed-scout/2026-10-15T053300+0800","summary":"Activation beat the prior record.","links":[".farplane/metrics/activation.jsonl"]}
{"team":"farplane","report":"reports/feed-scout/2026-10-15T053300+0800","summary":"A simple correction stalled in delegation.","lesson":"Do the bounded correction directly when delegation costs more than the work."}
```

Wins contain `{team, report, summary, links?}`; failures add `lesson`. Identity
is the composite `(kind, team, report)`. Core resolves the source report and
derives card IDs, project, cadence, period, timestamp, and display labels into
the replaceable project UI snapshot; the UI never parses report prose or needs
board state to render them. Daily and Weekly Interval used to append these
rows; no live job writes them now, so the galleries stay empty until a
producer adopts the ledger.
