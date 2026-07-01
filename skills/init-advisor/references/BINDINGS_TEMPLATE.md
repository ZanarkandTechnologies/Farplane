---
kind: project-bindings
status: draft
project: TODO
created_at: TODO
updated_at: TODO
framework_template_version: "0.3.2"
owner: project-pm-automation
---

# Project Bindings

Non-secret coordinates that bind generic skills, CLIs, and prompt-only metric
refresh recipes to this project. Secrets stay in the secure runtime environment.

## Project Config

```yaml
project:
  id: TODO
  name: TODO
  root: TODO
integrations:
  github:
    repo: null
    remote: null
    default_branch: main
  notion:
    project_name: null
    project_page_url: null
    task_database_alias: null
    write_policy: local_first
  kanban:
    provider: filesystem_tickets
    tickets_dir: tickets
    archive_dir: tickets/archive
    write_policy: read_only_ui
    poll_seconds: 60
  posthog:
    project_id: null
    host: null
    dashboard_url: null
  vercel:
    project_id: null
    project_url: null
    production_url: null
metrics:
  TODO_metric_name:
    label: TODO metric label
    product: TODO_product_id
    pinned: false
    kind: daily_count
    unit: TODO_unit
    display: bar_plus_cumulative
    refresh: >-
      TODO call $skill-name or
      $interval-update.helper_name(param="value", date="<YYYY-MM-DD>") to
      prepare this daily reading. Record source_gap when the reading cannot be
      collected.
  ready_unclaimed_ticket_count:
    label: Ready unclaimed tickets
    product: project_control
    kind: point
    unit: tickets
    display: reading
    refresh: >-
      Count ready, approval-free, unclaimed tickets under tickets/ that are not
      complete or human-gated; store value/status/payload in the daily metric
      file.
  accepted_output_events:
    label: Accepted output events
    product: productization
    kind: daily_count
    unit: events
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.count_ticket_kpi_rewards(ticket_dir="tickets",
      date="<YYYY-MM-DD>", kpi_key="accepted_output_events") when this KPI is
      ticket-derived, or read the accepted reward ledger when configured.
  auto_time_ratio:
    label: Autonomous time ratio
    product: cross_product_autonomy
    kind: point
    unit: ratio
    display: reading
    refresh: >-
      Call $interval-update.calculate_autonomy_time_ratio(runtime_dir=".farplane",
      date="<YYYY-MM-DD>") and store the returned value/status/payload.
```

## Policy

- Store only non-secret project coordinates here.
- Put credentials in environment variables, secret stores, or runtime connector
  config.
- Metric recipes are the single owner for label, product, pinned status, unit,
  kind, display, and a prompt-only refresh instruction.
- When refresh uses a skill, write it as `$skill-name`; when refresh uses an
  interval-owned helper, include the helper signature and parameters.
- Goals reference KPI IDs and interpret them; they do not duplicate provider or
  chart mechanics.
- Goals own SMART targets; do not put metric targets here.
- Missing access, missing files, unavailable API fields, and unbuilt feedback
  mechanisms become daily source gaps, not `enabled` switches.
- The interval agent writes one daily metrics JSON file at
  `.farplane/metrics/daily/YYYY-MM-DD.json`; the UI compiler only runs
  `farplane metrics compile` after daily readings exist.
