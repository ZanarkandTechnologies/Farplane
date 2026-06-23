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
    trigger: "Codex automation every 30 minutes"
    bindings: "farplane/bindings.md"
    first: pulse_update
    output: ".farplane/reports/pulse/<timestamp>.md"
  }

  heartbeat steer_update {
    trigger: "Codex automation at the minimum planning cadence"
    bindings: "farplane/bindings.md"
    first: steer_update
    config: "farplane/steer.config.toml"
    state: ".farplane/state/steer-scheduler.json"
    jobs: [daily_report, weekly_steer]
    output: ".farplane/reports/steer/<job>/<timestamp>.md"
  }
}
```

## Notes

Fill this with `harness-creator` when the project needs richer strategy,
feedback loops, missing-system tickets, or business/product operating goals.
