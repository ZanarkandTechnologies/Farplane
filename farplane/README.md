---
kind: farplane-config-index
status: active
created_at: 2026-06-15
updated_at: 2026-07-11
framework_template_version: "0.3.0"
---

# Farplane Config

Tracked project framework config lives here.

This folder is the project-local declaration that Farplane UI should be able to
summarize as one autonomous company inside the broader harness cockpit.

`manifest.json` owns the compact UI identity card. Richer project meaning lives
in tracked project files: `harness.yaml` is the typed human charter,
descriptive-product/capability map, and active metric selection;
`metrics.yaml` owns reusable metric meaning, direction, freshness, and guard
rules. Skills own recurring workflows; tickets own execution and proof.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.yaml     # typed charter, planning areas, capability refs, metric selection
  metrics.yaml     # metric definitions, direction, freshness, guard rules
  automations.toml # one Work Pulse heartbeat plus separate scheduled sources
  bindings.yaml    # non-secret project IDs and provider coordinates
  pm.json          # optional UI thread manifest for one visual project PM
  capability-profiles.yaml # optional restriction-only Project PM access policy

.agents/
  skills/          # project-local capability skills
    README.md
```

Runtime state lives under `.farplane/` and is intentionally ignored by git.

```text
.farplane/
  README.md
  views.yaml
  entities/
  state/ticket-thread-associations.jsonl
  automation/
  content/ledger.jsonl
  metrics/daily/
  metrics/observations/
  project/ui/latest.json
  reports/
  evals/runs/
  logs/
  capability-profiles/sessions/
```

The manifest names only stable owner paths; it does not require a generic run
ledger, evidence bucket, or review directory. QA and review receipts belong to
the ticket they judge.

Farplane Core is installed once and invoked through the global `farplane` CLI.
Other projects do not copy metric scripts; they pass a project root:

```bash
farplane metrics primitives --project-root /path/to/project --date <YYYY-MM-DD> --json
farplane project snapshot --project-root /path/to/project --date <YYYY-MM-DD> --json
farplane reports index --project-root /path/to/project --json
farplane reports repair-refs --project-root /path/to/project --json
farplane mining routes validate --project-root /path/to/project --json
farplane mining runs list --project-root /path/to/project --json
farplane mining drain --project-root /path/to/project --json
farplane capability-profiles read --project-root /path/to/project
```

`pm.json` groups visible Project PM threads; it never grants runtime access.
When a Project PM needs restriction, `capability-profiles.yaml` selects an
allowlist of skills and MCP servers. The selected runtime adapter compiles that
portable policy against its live capability inventory for fresh work; Codex
stores an immutable local launch receipt under
`.farplane/capability-profiles/sessions/`. Without an active profile, the PM
has full access.

Primitive metrics are Core-owned reducers over tickets, `bindings.yaml`, local
Codex stores, and ignored Farplane runtime state. Farplane UI should render the
generated project snapshot and deep-link back to the source files; canonical
writes still belong to the tracked project files and ignored runtime ledgers.

Metric producers persist canonical observation batches at
`.farplane/metrics/observations/<source_id>/<YYYY-MM-DD>.json`. Farplane Core
owns the Pydantic schema, writer, validator, native reducers, and snapshot
compiler. Platform skills such as Instagram or X own API fetching, but their
outputs must validate against the same `MetricObservationBatch` shape.

Report producers persist Markdown under `.farplane/reports/` with `ref`,
`kind`, `created_at`, and `ui_summary` frontmatter. Farplane Core owns
`.farplane/reports/index.json`; UI clients should read that registry instead of
defining report hierarchy locally. Use `farplane reports repair-refs` to add
path-derived `ref` frontmatter to existing report Markdown before rebuilding
the index. The standard lives in
[docs/farplane-framework/reporting.md](../docs/farplane-framework/reporting.md).

`farplane ticket finalize TASK-XXXX` completes and archives a ticket, then writes
its explicit completion event. `farplane/bindings.yaml#event_routes` maps that
event to an immutable mining program. Events, outbox state, frozen run inputs,
machine receipts, and verdicts remain ignored under `.farplane/`. Farplane UI
may edit routes and render runs through the Core CLI but does not own mining
semantics.

See [docs/farplane-framework/project-files.md](../docs/farplane-framework/project-files.md).

## Official Automation Presets

- `Work Pulse`: the only heartbeat; reconciles, dispatches, handles due
  check-ins, and refills an empty BAU board.
- `Feed Scout`: separate source report and bounded opportunity-ticket job.
- `Daily/Weekly BAU`: problem reports and bounded already-evidenced
  maintenance, not new-direction planning.
- `Dogfood Improvement`: portfolio learning and bounded experiment packets;
  Work Pulse executes the selected tickets.
- `Monthly Registry Consolidation`: optional report-only pass over registry
  truth, duplicate rows, owner drift, and generated-output freshness.
- Human-feedback improvements are ordinary Dogfood-created Goal Packets;
  Work Pulse executes them and ticket review state waits without a worker.
