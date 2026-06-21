---
kind: project-automations
status: draft
project: TODO
created_at: TODO
updated_at: TODO
framework_template_version: "0.1.0"
owner: project-pm-automation
ledger: .farplane/state/run-ledger.json
bindings: farplane/bindings.md
---

# Project Automations

This file defines the project's recurring automation program.
Live Codex automation prompts should be compiled from this file, but each live
prompt should still carry its exact program and todo list.

This file is a cadence manifest, not a copy of every skill runbook. Skill
presets own their default reads, writes, output contract, and eval surface.
This manifest owns schedules, target threads, side-effect gates, grouped jobs,
freshness policy, report handles, and local overrides.

```project-automation
project {
  id: TODO
  root: "TODO"
  mission: "TODO"
  default_board_policy: local_first
  ledger: ".farplane/state/run-ledger.json"
  bindings: "farplane/bindings.md"
  ticket_sources {
    local {
      enabled: true
      path: "tickets/"
      priority: first
    }
    notion {
      enabled: false
      binding_ref: "notion"
      project_id: null
      project_name: "TODO"
      statuses: ["Not started", "In Progress"]
      use_when: "local has no proceedable ticket and notion.enabled is true"
    }
  }
  gates: [
    no_push,
    no_deploy,
    no_publish,
    no_spend,
    no_account_changes,
    no_destructive_cleanup
  ]
}

settings {
  pm_heartbeat {
    automation_id: TODO-pm-heartbeat
    kind: heartbeat
    schedule: "FREQ=MINUTELY;INTERVAL=30"
    target_thread_id: null
    enabled: false
    max_child_threads_per_beat: 1
    action_authority: "spawn_one_bounded_action"
  }
  daily_pm_plan {
    automation_id: TODO-daily-pm-plan
    kind: heartbeat
    schedule: "FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0"
    target_thread_id: null
    action_authority: "plan_and_rank"
  }
  weekly_pm_plan {
    automation_id: TODO-weekly-pm-update
    kind: heartbeat
    schedule: "FREQ=WEEKLY;BYDAY=MO;BYHOUR=9;BYMINUTE=0;BYSECOND=0"
    target_thread_id: null
    action_authority: "strategy_and_memory"
  }
  ticket_drainer {
    automation_id: TODO-ticket-update
    kind: heartbeat
    schedule: "FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0"
    target_thread_id: null
    enabled: false
    execution_limit: 1
  }
}

cadence_thread_contract {
  principle: "separate planning horizons into separate heartbeat threads; use files as shared memory and threads as working memory"
  shared_memory: [
    "farplane/goals.md",
    "farplane/automations.md",
    ".farplane/state/run-ledger.json",
    ".farplane/reports/**/latest.md",
    "tickets/**/ticket.md",
    "tickets/**/progress.md",
    "docs/MEMORY.md",
    "docs/LESSONS.md",
    "docs/TROUBLES.md"
  ]
  child_thread_spawning {
    owner: "parent cadence heartbeat"
    rule: "parent names and spawns child threads; child threads do not rely on title tools to rename themselves"
    name_template: "[Project] <ticket-id> <ticket name>"
    fallback: "if child thread creation is unavailable, write a handoff-ready prompt and report blocker instead of executing leaf work inside the parent cadence"
  }
}

reports {
  pm_heartbeat.latest: ".farplane/reports/pm-heartbeat/latest.md"
  pm_heartbeat.runs: ".farplane/reports/pm-heartbeat/runs/"
  daily_pm_plan.latest: ".farplane/reports/daily-pm-plan/latest.md"
  daily_pm_plan.runs: ".farplane/reports/daily-pm-plan/runs/"
  update_external_context.latest: ".farplane/reports/external-context/latest.md"
  update_external_context.runs: ".farplane/reports/external-context/runs/"
  update_memory.latest: ".farplane/reports/memory/latest.md"
  update_memory.runs: ".farplane/reports/memory/runs/"
  skill_hardening.latest: ".farplane/reports/skill-maintenance/harden-latest.md"
  skill_hardening.runs: ".farplane/reports/skill-maintenance/runs/"
  skill_refinement.latest: ".farplane/reports/skill-maintenance/refine-latest.md"
  skill_refinement.runs: ".farplane/reports/skill-maintenance/runs/"
  registry_drift.latest: ".farplane/reports/registry-drift/latest.md"
  registry_drift.runs: ".farplane/reports/registry-drift/runs/"
  update_strategy.latest: ".farplane/reports/strategy/latest.md"
  update_strategy.runs: ".farplane/reports/strategy/runs/"
  ticket_update.latest: ".farplane/reports/ticket-update/latest.md"
  ticket_update.runs: ".farplane/reports/ticket-update/runs/"
  weekly_pm.latest: ".farplane/reports/weekly-pm/latest.md"
  weekly_pm.runs: ".farplane/reports/weekly-pm/runs/"
  weekly_pm.context: ".farplane/reports/weekly-pm/context/"
}

job_catalog {
  rule: "job entries point to skill-owned presets; add local_overrides only when this project differs from the preset"

  pm_heartbeat: pm-heartbeat.bandit @30m -> reports.pm_heartbeat
  daily_pm_plan: daily-pm-plan.operating_plan @1d -> reports.daily_pm_plan
  weekly_pm_plan: weekly-pm-plan.strategy @7d -> reports.weekly_pm
  update_external_context: feed-scout.project_context @24h -> reports.update_external_context
  update_memory: update-memory.project_context @7d -> reports.update_memory
  skill_hardening: skill-maintenance.harden_skill @7d -> reports.skill_hardening
  skill_refinement: skill-maintenance.refine_skill @7d -> reports.skill_refinement
  registry_drift: skill-maintenance.registry_drift @7d -> reports.registry_drift
  update_strategy: update-strategy.weekly_pm @7d -> reports.update_strategy
  ticket_update: ticket-drainer.daily @none -> reports.ticket_update

  depends_on {
    update_strategy: [
      "update_external_context:max_age=24h",
      "update_memory:max_age=7d",
      "skill_hardening:max_age=7d",
      "registry_drift:max_age=7d"
    ],
    daily_pm_plan: [
      "weekly_pm_plan:max_age=7d"
    ],
    pm_heartbeat: [
      "daily_pm_plan:max_age=24h"
    ]
  }

  local_overrides {
    pm_heartbeat.action_arms: [
      ticket_execution,
      planning,
      growth_research,
      product_quality,
      skill_hardening,
      eval_writing,
      automation_building,
      reward_update,
      metric_snapshot,
      weekly_reflection
    ]
    ticket_update.skills: [impl-plan, goal-advisor]
  }
}

cadences {
  weekly_pm_plan {
    config_ref: settings.weekly_pm_plan
    preset: weekly-pm-plan.strategy
    reports: reports.weekly_pm
    depends_on: job_catalog.depends_on.update_strategy
    template_refs: [
      "skills/weekly-pm-plan/templates/report.md",
      "skills/weekly-pm-plan/templates/context-bundle.md"
    ]
    grouped_jobs: [
      update_external_context,
      update_memory,
      skill_hardening,
      skill_refinement,
      registry_drift,
      update_strategy
    ]
    context_refs {
      project_root: project.root
      review_window: "previous weekly cadence window"
      goals_ref: "farplane/goals.md"
      automation_ref: "farplane/automations.md"
      ledger_ref: project.ledger
      ticket_refs: ["tickets/"]
      memory_refs: ["docs/MEMORY.md", "docs/LESSONS.md", "docs/TROUBLES.md"]
      report_refs: [".farplane/reports/**/latest.md"]
      opportunity_sources: job_catalog.local_overrides.update_external_context.sources?
      output_bundle_dir: reports.weekly_pm.context
    }
    authority: "strategy and proposed goals/ticket deltas; no leaf execution"
    goals_delta_policy: "auto_apply minor evidence/current-signal updates; approval_required for north-star, KPI, axis, priority, hold, quarterly, or yearly changes"
  }

  daily_pm_plan {
    config_ref: settings.daily_pm_plan
    preset: daily-pm-plan.operating_plan
    reports: reports.daily_pm_plan
    depends_on: job_catalog.depends_on.daily_pm_plan
    context_refs: [
      ".farplane/reports/weekly-pm/latest.md",
      ".farplane/reports/pm-heartbeat/latest.md",
      ".farplane/state/run-ledger.json",
      "farplane/goals.md",
      "tickets/"
    ]
    authority: "rank today's lanes and optionally call ticket-drainer by policy"
  }

  pm_heartbeat {
    config_ref: settings.pm_heartbeat
    preset: pm-heartbeat.bandit
    reports: reports.pm_heartbeat
    depends_on: job_catalog.depends_on.pm_heartbeat
    context_refs: [
      ".farplane/reports/daily-pm-plan/latest.md",
      ".farplane/reports/weekly-pm/latest.md",
      ".farplane/automation/bandit-state.json",
      ".farplane/automation/spawned-threads.jsonl",
      ".farplane/automation/action-outcomes.jsonl"
    ]
    authority: "spawn at most one bounded child action per beat"
  }

  daily_ticket_drainer {
    config_ref: settings.ticket_drainer
    preset: ticket-drainer.daily
    reports: reports.ticket_update
    context_refs: [
      ".farplane/reports/weekly-pm/latest.md",
      ".farplane/reports/ticket-update/latest.md",
      ".farplane/state/run-ledger.json",
      "farplane/goals.md",
      "tickets/"
    ]
    authority: "select one safe ticket and create a named child-thread handoff"
  }
}
```

## Compiled Prompt Rule

Compile a live Codex automation by expanding:

```text
compile_automation(cadence, job_catalog, reports, gates)
  -> prompt(program, ordered_todo, side_effect_gates, final_output_fields)
```

Rules:

1. `automations.md` supplies cadence, freshness, reports, dependencies, target
   thread, and local overrides.
2. The referenced skill preset supplies default reads, writes, output contract,
   proof expectations, and eval surface.
3. The compiled prompt must inline enough ordered steps to run without guessing;
   it must not say only "read the manifest and decide."
4. Local overrides are explicit and project-specific; do not copy the entire
   skill runbook back into this file.

Each live automation prompt should include:

- `Program:` fenced as `automation-program`
- `Todo:` exact ordered steps
- explicit side-effect gates
- required final output fields

Do not leave the live prompt as only "read `farplane/automations.md` and decide."
