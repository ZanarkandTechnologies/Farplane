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

  heartbeat pulse_update {
    trigger: "compiled from farplane/automations.json lanes.pulse"
    bindings: "farplane/bindings.md"
    first: pulse_update
    output: ".farplane/reports/pulse/latest.md"
  }

  heartbeat rhythm_update {
    trigger: "compiled from farplane/automations.json lanes.rhythm"
    bindings: "farplane/bindings.md"
    first: rhythm_update
    jobs: [ticket_update]
    output: ".farplane/reports/rhythm/latest.md"
  }

  heartbeat horizon_update {
    trigger: "compiled from farplane/automations.json lanes.horizon"
    bindings: "farplane/bindings.md"
    first: grouped_jobs
    jobs: [update_external_context, update_memory, skill_hardening, skill_refinement, registry_drift, update_strategy, quarterly_plan, annual_review]
    output: ".farplane/reports/horizon/latest.md"
  }
}
```

## Notes

Fill this with `harness-creator` when the project needs richer strategy,
feedback loops, missing-system tickets, or business/product operating goals.
