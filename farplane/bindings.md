---
kind: project-bindings
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-07-01
framework_template_version: "0.2.0"
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

## Metric Providers

Metric providers are non-secret coordinates that an interval agent or metric
snapshot command can try. Provider availability is observed at fetch time: a
missing token, missing file, or unavailable API metric becomes a source gap in
the daily snapshot rather than an `enabled` switch here.

```yaml
metric_providers:
  pulse_reward_ledger:
    provider: local_jsonl
    path: .farplane/automation/rewards.jsonl
    provides:
      - accepted_output_events
      - accepted_harness_improvements
      - proof_closure_events

  pulse_decision_ledger:
    provider: local_jsonl
    path: .farplane/automation/decisions.jsonl
    provides:
      - pulse_execute_count
      - pulse_request_planning_count

  ticket_board:
    provider: local_files
    path: tickets/TASK-*/ticket.md
    provides:
      - ready_unclaimed_ticket_count
      - stale_claim_count

  eval_summary_index:
    provider: local_json
    path: .farplane/evals/runs/index.json
    provides:
      - latest_eval_pass_rate

  x_account_metrics:
    provider: skill_snapshot
    skill: x-account
    alias: farplane_x
    credentials: FARPLANE_X
    writes: .farplane/metrics/manual/x_account.json
    provides:
      - x_followers
      - x_views
      - x_likes
      - x_retention_score

  instagram_account_metrics:
    provider: skill_snapshot
    skill: instagram-account
    alias: farplane_instagram
    credentials: FARPLANE_INSTAGRAM
    writes: .farplane/metrics/manual/instagram_account.json
    provides:
      - instagram_followers
      - instagram_views
      - instagram_likes
      - instagram_retention_score

  social_posts:
    provider: agent_snapshot
    skill: social-content
    writes: .farplane/metrics/manual/social_posts.json
    provides:
      - posts_published

  framework_adoption_events:
    provider: missing
    setup_hint: add an init-advisor/project-registry event source
    writes: .farplane/metrics/manual/framework_adoption.json
    provides:
      - initialized_project_count
      - first_goal_handoff_count

  runway_review_notes:
    provider: interval_report
    path: .farplane/reports/interval/weekly_interval
    setup_hint: weekly interval writes Budget / Runway Review rows before this is mechanically derivable
    provides:
      - weekly_runway_review_count
      - projects_with_runway_decisions
```

## Policy

- Store only non-secret project coordinates here.
- Put credentials in environment variables, secret stores, or the runtime
  connector config.
- If a skill needs a binding that is missing, create a ticket to add the
  binding or create the data-access skill.
