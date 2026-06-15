---
kind: project-automations
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-15
framework_template_version: "0.1.0"
owner: project-pm-automation
ledger: .farplane/state/run-ledger.json
bindings: farplane/bindings.md
---

# Farplane Project Automations

This file is the source of truth for Farplane's recurring automation program.
Codex automation TOML files are compiled entrypoints from the cadences below.
They may read this file for config values, but each live automation prompt
should carry its exact program and todo list.

```project-automation
project {
  id: farplane
  root: "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
  mission: "compound Farplane's harness, skills, tickets, docs, feedback loops, and proof surfaces"
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
      project_name: "Farplane"
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
  weekly_pm {
    automation_id: farplane-weekly-pm-update
    kind: heartbeat
    schedule: "FREQ=WEEKLY;BYDAY=MO;BYHOUR=9;BYMINUTE=0;BYSECOND=0"
    target_thread_id: "019eca0d-d392-7db1-9b10-8916021a86d0"
  }
  ticket_drainer {
    automation_id: farplane-ticket-update
    kind: cron
    schedule: "FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0"
    execution_limit: 1
  }
}

reports {
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
}

job update_external_context {
  intent: "ground Farplane planning in new external harness patterns, creator/source changes, and scoutable ideas"
  skill: feed-scout
  freshness: 24h
  reads: [
    "skills/feed-scout/config/tracked-profiles.jsonl",
    "skills/feed-scout/config/tracked-entities.jsonl",
    "skills/feed-scout/config/tracked-harness-resources.jsonl",
    "docs/sources/registry.jsonl",
    "docs/features/registry.jsonl"
  ]
  writes: [
    ".farplane/reports/external-context/latest.md",
    ".farplane/reports/external-context/runs/YYYY-MM-DD.md"
  ]
  output: "external context report with checked sources, new items, scout decisions, proposal candidates, evidence paths, and blockers"
}

job update_memory {
  intent: "consolidate durable project context and docs without mixing in skill hardening"
  skill: update-memory
  freshness: 7d
  reads: [
    "docs/HISTORY.md",
    "docs/MEMORY.md",
    "docs/LESSONS.md",
    "docs/TROUBLES.md",
    "relevant docs/**/*.md",
    "README.md",
    "recent tickets and artifacts"
  ]
  writes: [
    ".farplane/reports/memory/latest.md",
    ".farplane/reports/memory/runs/YYYY-MM-DD.md",
    "proposed README/docs/MEMORY/HISTORY/LESSONS/TROUBLES deltas when justified",
    "docs consolidation tickets when justified"
  ]
  output: "context report with accepted deltas, proposed doc deltas, docs consolidation plan, stale context, and blockers"
}

job skill_hardening {
  intent: "turn fresh lessons and troubles into immediate evals, gotchas, QA guardrails, or tickets"
  skill: "skill-maintenance(mode: harden_skill)"
  freshness: 7d
  reads: [
    "docs/LESSONS.md",
    "docs/TROUBLES.md",
    "skills/*/SKILL.md",
    "docs/skills/registry.jsonl"
  ]
  writes: [
    ".farplane/reports/skill-maintenance/harden-latest.md",
    ".farplane/reports/skill-maintenance/runs/YYYY-MM-DD-harden.md",
    "skill evals/gotchas/checklists or local tickets when justified"
  ]
  output: "hardening report with touched skills, new protections, skipped items, and blockers"
}

job skill_refinement {
  intent: "compact older accumulated evals and gotchas after hardening exists"
  skill: "skill-maintenance(mode: refine_skill)"
  freshness: 7d
  reads: [
    "skills/*/SKILL.md",
    "skill evals",
    "skill gotchas",
    ".farplane/reports/skill-maintenance/harden-latest.md"
  ]
  writes: [
    ".farplane/reports/skill-maintenance/refine-latest.md",
    ".farplane/reports/skill-maintenance/runs/YYYY-MM-DD-refine.md",
    "skill compaction patches or local tickets when justified"
  ]
  output: "refinement report with consolidations, rejected compactions, and review notes"
}

job registry_drift {
  intent: "keep skill/source/feature registries aligned with current repo state"
  skill: skill-maintenance
  freshness: 7d
  reads: [
    "docs/skills/registry.jsonl",
    "docs/features/registry.jsonl",
    "docs/sources/registry.jsonl",
    "skills/*/SKILL.md"
  ]
  writes: [
    ".farplane/reports/registry-drift/latest.md",
    ".farplane/reports/registry-drift/runs/YYYY-MM-DD.md",
    "registry patches or follow-up tickets"
  ]
  output: "registry drift report with validation commands, fixes, and ambiguous gaps"
}

job update_strategy {
  intent: "refresh Farplane strategy, current milestone, tickets, and system gaps"
  skill: update-strategy
  freshness: 7d
  depends_on: [
    "update_external_context:max_age=24h",
    "update_memory:max_age=7d",
    "skill_hardening:max_age=7d",
    "registry_drift:max_age=7d"
  ]
  reads: [
    "AGENTS.md",
    "farplane/automations.md",
    "farplane/bindings.md",
    "docs/MEMORY.md",
    "docs/HISTORY.md",
    "active tickets",
    ".farplane/reports/*/latest.md"
  ]
  writes: [
    ".farplane/reports/strategy/latest.md",
    ".farplane/reports/strategy/runs/YYYY-MM-DD.md",
    "local ticket deltas"
  ]
  output: "strategy report with priorities, depriorities, system gaps, ticket changes, and Goal Advisor handoffs"
}

job ticket_update {
  intent: "pick and advance the highest-value autonomous ticket"
  skills: [impl-plan, goal-advisor]
  freshness: none
  reads: [
    "tickets/README.md",
    "tickets/TASK-*/ticket.md",
    "notion tasks only when ticket_sources.notion.enabled is true, local has no proceedable ticket, and farplane/bindings.md has a usable notion binding"
  ]
  writes: [
    ".farplane/reports/ticket-update/latest.md",
    ".farplane/reports/ticket-update/runs/YYYY-MM-DD-HHMM.md",
    "selected ticket progress/evidence/blockers"
  ]
  output: "selected ticket, ranking reason, impl-plan result, Goal Advisor execution handoff, evidence paths, or blocker"
}

cadence daily_ticket_drainer {
  automation_id: farplane-ticket-update
  config_ref: settings.ticket_drainer
  thread_context: "daily Farplane ticket execution"
  todo: [
    "fetch local tickets from ticket_sources.local.path",
    "if no proceedable local tickets and ticket_sources.notion.enabled, fetch Notion using farplane/bindings.md notion coordinates",
    "filter ready, unblocked, direct, autonomous tickets",
    "rank by priority, compounding ROI, project value, and low need for Kenji judgment",
    "select one ticket",
    "run impl-plan if planning is missing or stale",
    "call goal-advisor to create or activate the execution goal",
    "execute as far as possible until done, blocked, or ready for review",
    "write ticket_update report",
    "update ledger"
  ]
  fallback: "if no safe ticket can advance, write a no-op ticket_update report with blocker categories"
}

cadence weekly_pm_update {
  automation_id: farplane-weekly-pm-update
  config_ref: settings.weekly_pm
  thread_context: "weekly Farplane PM strategy, context, memory, and maintenance"
  grouped_jobs: [
    update_external_context,
    update_memory,
    skill_hardening,
    skill_refinement,
    registry_drift,
    update_strategy
  ]
  todo: [
    "ensure update_external_context max_age=24h reuse_report_if_fresh",
    "ensure update_memory max_age=7d reuse_report_if_fresh",
    "ensure skill_hardening max_age=7d reuse_report_if_fresh",
    "ensure skill_refinement max_age=7d reuse_report_if_fresh",
    "ensure registry_drift max_age=7d reuse_report_if_fresh",
    "run update_strategy using all report refs",
    "create_or_update_local_tickets",
    "write weekly_pm report",
    "update ledger"
  ]
}
```

## Run Ledger Contract

Each job writes a ledger row before and after execution:

```text
ledger[job_id] = {
  status: fresh | running | blocked | failed | stale,
  started_at?,
  finished_at?,
  freshness_until?,
  latest_report?,
  latest_error?,
  owner_cadence?
}
```

Before running a job, a cadence must:

1. Check `.farplane/state/run-ledger.json`.
2. Reuse `latest_report` when the job is fresh enough for the caller.
3. Mark the job `running` before doing work.
4. Write the job report.
5. Mark the job `fresh`, `blocked`, or `failed` with the report path.

If a required job is already `running`, the caller should read the most recent
fresh report if one exists; otherwise it should record a blocked dependency
rather than duplicating the job in a separate thread.
