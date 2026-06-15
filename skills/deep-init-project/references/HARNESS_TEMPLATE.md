---
kind: project-harness
status: draft
project: TODO
created_at: TODO
updated_at: TODO
framework_template_version: "0.1.0"
owner: harness
---

# Project Harness

```harness-program
project "TODO" {
  values {
    mission: "TODO"
    operating_principles: [
      "TODO"
    ]
    priorities: [
      trust.high,
      usefulness.high,
      speed.medium
    ]
    non_tradeoffs: [
      "TODO"
    ]
  }

  modes: [project]

  system ticket_loop {
    status: ready
    evidence: ref("tickets/")
    action: use_existing("local ticket workflow")
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

Fill this with `harness-creator` when the project needs richer strategy,
feedback loops, missing-system tickets, or business/product operating goals.
