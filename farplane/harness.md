---
kind: project-harness
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-15
framework_template_version: "0.1.0"
owner: harness
---

# Farplane Harness

```harness-program
project "Farplane" {
  values {
    mission: "Make autonomous Codex work visible, reviewable, repeatable, and useful through files, tickets, skills, goals, and proof."
    operating_principles: [
      "prefer visible artifacts over hidden runtime state",
      "keep reusable behavior in skills and project-specific coordinates in bindings",
      "shape work through tickets before long autonomous execution",
      "prove behavior with validators, reviews, evals, or artifact evidence"
    ]
    priorities: [
      trust.high,
      reliability.high,
      operator_leverage.high,
      clarity.high,
      speed.medium
    ]
    non_tradeoffs: [
      "do not hide orchestration state in chat",
      "do not create a scheduler or daemon when a visible automation prompt is enough",
      "do not store secrets in tracked project config"
    ]
  }

  modes: [harness, project_ops, skill_system, agent_workbench]

  system ticket_loop {
    status: ready
    evidence: ref("tickets/")
    action: use_existing("local ticket workflow")
  }

  system project_framework {
    status: ready
    evidence: ref("farplane/")
    action: use_existing("Farplane framework config")
  }

  system recurring_pm {
    status: ready
    evidence: ref("farplane/automations.md")
    action: use_existing("weekly PM and daily ticket drainer automations")
  }

  skill update_strategy {
    status: ready
    use: "refresh priorities, current milestone, gaps, experiments, and tickets"
  }

  skill update_memory {
    status: ready
    use: "consolidate README, docs, memory, history, lessons, and troubles into context deltas"
  }

  skill skill_maintenance {
    status: ready
    use: "harden and refine skills from lessons, troubles, evals, and gotchas"
  }

  skill goal_advisor {
    status: ready
    use: "compile milestone or ticket execution into Goal, heartbeat, or direct route"
  }

  heartbeat ticket_update {
    trigger: "compiled from farplane/automations.md settings.ticket_drainer"
    bindings: "farplane/bindings.md"
    first: daily_ticket_drainer
    output: ".farplane/reports/ticket-update/latest.md"
  }

  heartbeat weekly_pm_update {
    trigger: "compiled from farplane/automations.md settings.weekly_pm"
    bindings: "farplane/bindings.md"
    first: grouped_jobs
    jobs: [update_external_context, update_memory, skill_hardening, skill_refinement, registry_drift, update_strategy]
    output: ".farplane/reports/weekly-pm/latest.md"
  }
}
```

## Notes

Farplane is dogfooding the framework while the framework is still draft.
Keep this file compact and move detailed operating rules into docs, skills, or
tickets.
