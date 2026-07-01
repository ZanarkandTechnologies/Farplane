---
kind: project-bindings
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-07-02
framework_template_version: "0.3.2"
owner: project-pm-automation
---

# Farplane Bindings

Non-secret coordinates that bind generic skills, CLIs, and prompt-only metric
refresh recipes to this project. Secrets stay in the secure runtime environment.

## Project Config

```yaml
project:
  id: farplane
  name: Farplane
  root: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
integrations:
  github:
    repo: ZanarkandTechnologies/Farplane
    remote: git@github.com:ZanarkandTechnologies/Farplane.git
    default_branch: main
  notion:
    project_name: Farplane
    project_page_url: null
    task_database_alias: null
    write_policy: local_first
  posthog:
    project_id: null
    host: null
    dashboard_url: null
  vercel:
    project_id: null
    project_url: null
    production_url: null
  workos:
    tenant_alias: null
    dashboard_url: null
metrics:
  accepted_evidence_cycles:
    label: Accepted evidence cycles
    product: experiments
    pinned: true
    kind: daily_count
    unit: cycles
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.count_ticket_kpi_rewards(ticket_dir="tickets",
      date="<YYYY-MM-DD>", kpi_key="accepted_evidence_cycles") and store the
      returned value/status/payload in the daily metric file.
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: productization
    pinned: true
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.count_ticket_kpi_rewards(ticket_dir="tickets",
      date="<YYYY-MM-DD>", kpi_key="accepted_harness_improvements") and store
      the returned value/status/payload in the daily metric file.
  auto_time_ratio:
    label: Autonomous time ratio
    product: cross_product_autonomy
    pinned: true
    kind: point
    unit: ratio
    display: reading
    refresh: >-
      Call $interval-update.calculate_autonomy_time_ratio(runtime_dir=".farplane",
      date="<YYYY-MM-DD>") and store the returned value/status/payload for this
      metric.
  evidence_distribution_reach:
    label: Evidence distribution reach
    product: distribution
    pinned: true
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
    refresh: >-
      Sum available daily readings from x_views, instagram_views, github_views,
      and `.farplane/content/ledger.jsonl` in the same daily file; use source_gap when no
      component reading exists.
  latest_eval_pass_rate:
    label: Latest eval pass rate
    product: productization
    kind: point
    unit: ratio
    display: reading
    refresh: >-
      Read the latest eval summary pass_rate for the snapshot window and store
      value/status/payload in the daily metric file.
  github_views:
    label: GitHub views
    product: adoption
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
    refresh: >-
      Use gh api for ZanarkandTechnologies/Farplane traffic views on
      <YYYY-MM-DD>; store source_gap when traffic permissions are unavailable.
  auto_completion_rate:
    label: Auto completion rate
    product: cross_product_autonomy
    kind: point
    unit: ratio
    display: reading
    refresh: >-
      Call $interval-update.calculate_ticket_intervention_metrics(ticket_dir="tickets",
      runtime_dir=".farplane", date="<YYYY-MM-DD>") and store the
      auto_completion_rate reading.
  intervention_free_ticket_count:
    label: Intervention-free tickets
    product: cross_product_autonomy
    kind: daily_count
    unit: tickets
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.calculate_ticket_intervention_metrics(ticket_dir="tickets",
      runtime_dir=".farplane", date="<YYYY-MM-DD>") and store the
      intervention_free_ticket_count reading.
  ticket_intervention_turn_count:
    label: Ticket intervention turns
    product: cross_product_autonomy
    kind: daily_count
    unit: turns
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.calculate_ticket_intervention_metrics(ticket_dir="tickets",
      runtime_dir=".farplane", date="<YYYY-MM-DD>") and store the
      ticket_intervention_turn_count reading.
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
  x_followers:
    label: X followers
    product: distribution
    kind: point
    unit: followers
    display: line
    refresh: >-
      Call $x-account for the Farplane X account and record the current follower
      count; store source_gap if credentials or API access are unavailable.
  x_views:
    label: X views
    product: distribution
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.select_content_metric_targets(content_ledger=".farplane/content/ledger.jsonl",
      platform="x", kpi_key="x_views", date="<YYYY-MM-DD>", window_days=7),
      then call $x-account with the returned tweet IDs and store the aggregate
      x_views value plus per-post payload.items.
  x_likes:
    label: X likes
    product: distribution
    kind: daily_count
    unit: likes
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.select_content_metric_targets(content_ledger=".farplane/content/ledger.jsonl",
      platform="x", kpi_key="x_likes", date="<YYYY-MM-DD>", window_days=7),
      then call $x-account with the returned tweet IDs and store the aggregate
      x_likes value plus per-post payload.items.
  instagram_followers:
    label: Instagram followers
    product: distribution
    kind: point
    unit: followers
    display: line
    refresh: >-
      Call $instagram-account for the Farplane Instagram account and record the
      current follower count; store source_gap if unavailable.
  instagram_views:
    label: Instagram views
    product: distribution
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.select_content_metric_targets(content_ledger=".farplane/content/ledger.jsonl",
      platform="instagram", kpi_key="instagram_views", date="<YYYY-MM-DD>",
      window_days=7), then call $instagram-account with the returned media IDs
      and store the aggregate instagram_views value plus per-post payload.items.
  instagram_likes:
    label: Instagram likes
    product: distribution
    kind: daily_count
    unit: likes
    display: bar_plus_cumulative
    refresh: >-
      Call $interval-update.select_content_metric_targets(content_ledger=".farplane/content/ledger.jsonl",
      platform="instagram", kpi_key="instagram_likes", date="<YYYY-MM-DD>",
      window_days=7), then call $instagram-account with the returned media IDs
      and store the aggregate instagram_likes value plus per-post payload.items.
  posts_published:
    label: Posts published
    product: distribution
    kind: daily_count
    unit: posts
    display: bar_plus_cumulative
    refresh: >-
      Count rows in `.farplane/content/ledger.jsonl` with status=posted and
      published_at on <YYYY-MM-DD>; store source_gap if the ledger is missing.
```

## Policy

- Store only non-secret project coordinates here.
- Put credentials in environment variables, secret stores, or the runtime
  connector config.
- Metric recipes are the single owner for label, product, pinned status, unit,
  kind, display, and a prompt-only refresh instruction.
- Goals reference KPI IDs and interpret them; they do not duplicate refresh,
  source, provider, chart, or target mechanics.
- Goals own SMART targets; do not put metric targets here.
- If a metric reading is unavailable, the daily metric JSON records a source
  gap rather than an `enabled` toggle.
- The interval agent writes one daily metrics JSON file at
  `.farplane/metrics/daily/YYYY-MM-DD.json`; the UI compiler runs
  `farplane metrics compile` after daily readings exist.
