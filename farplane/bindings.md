---
kind: project-bindings
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-15
framework_template_version: "0.1.0"
owner: project-pm-automation
---

# Farplane Bindings

Non-secret coordinates that bind generic skills to this project.

Skills own capabilities.
Bindings provide project-specific IDs, URLs, labels, and aliases.
Secrets stay in the secure runtime environment.

```project-bindings
project {
  id: farplane
  name: "Farplane"
  root: "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
}

github {
  enabled: true
  repo: "ZanarkandTechnologies/Farplane"
  remote: "git@github.com:ZanarkandTechnologies/Farplane.git"
  default_branch: "main"
}

notion {
  enabled: false
  project_name: "Farplane"
  project_page_url: null
  task_database_alias: null
  write_policy: local_first
}

posthog {
  enabled: false
  project_id: null
  host: null
  dashboard_url: null
}

vercel {
  enabled: false
  project_id: null
  project_url: null
  production_url: null
}

workos {
  enabled: false
  tenant_alias: null
  dashboard_url: null
}
```

## Social Account Bindings

These bindings are non-secret account coordinates. Credentials live in
`~/.codex/private/social.env` or the runtime environment; private setup notes
live in `~/.codex/private/docs/social.md`.

| Account | Enabled | Skill | Alias | Username | Metrics Mode | Publish Policy | Secret Env Prefix |
| --- | --- | --- | --- | --- | --- | --- | --- |
| x | false | x-account | farplane_x | null | api_or_export | explicit_approval_only | FARPLANE_X |
| instagram | false | instagram-account | farplane_instagram | null | api_or_export | explicit_approval_only | FARPLANE_INSTAGRAM |

## Metric Source Bindings

Metric sources are non-secret fetch coordinates used by `interval-update` and
`farplane metrics snapshot`. Missing external or manual sources must surface as
`source_gap`; they must not be rendered as zero.

| Source | Enabled | Type | Fetch | Path Or Account | Raw Snapshot Dir |
| --- | --- | --- | --- | --- | --- |
| pulse_reward_ledger | true | local_jsonl | farplane_metrics | .farplane/automation/rewards.jsonl | .farplane/metrics/source-snapshots/pulse_reward_ledger |
| pulse_decision_ledger | true | local_jsonl | farplane_metrics | .farplane/automation/decisions.jsonl | .farplane/metrics/source-snapshots/pulse_decision_ledger |
| ticket_board | true | local_files | farplane_metrics | tickets/TASK-*/ticket.md | .farplane/metrics/source-snapshots/ticket_board |
| eval_summary_index | true | local_json | farplane_metrics | .farplane/evals/runs/index.json | .farplane/metrics/source-snapshots/eval_summary_index |
| manual_x_account | false | manual | manual_snapshot | .farplane/metrics/manual/x_account.json | .farplane/metrics/source-snapshots/manual_x_account |
| manual_instagram_account | false | manual | manual_snapshot | .farplane/metrics/manual/instagram_account.json | .farplane/metrics/source-snapshots/manual_instagram_account |
| manual_social_posts | false | manual | manual_snapshot | .farplane/metrics/manual/social_posts.json | .farplane/metrics/source-snapshots/manual_social_posts |

## Policy

- Store only non-secret project coordinates here.
- Put credentials in environment variables, secret stores, or the runtime
  connector config.
- If a skill needs a binding that is missing, create a ticket to add the
  binding or create the data-access skill.
