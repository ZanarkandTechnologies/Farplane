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

  heartbeat daily_interval {
    trigger: "Codex automation daily"
    bindings: "farplane/bindings.md"
    first: interval_update
    review_window: "last_24h"
    planning_window: "next_24h"
    output: ".farplane/reports/interval/daily_interval/<timestamp>.md"
  }

  heartbeat weekly_interval {
    trigger: "Codex automation weekly"
    bindings: "farplane/bindings.md"
    first: interval_update
    review_window: "last_week"
    planning_window: "next_week"
    output: ".farplane/reports/interval/weekly_interval/<timestamp>.md"
  }
}
```

## Notes

Fill this with `harness-creator` when the project needs richer strategy,
feedback loops, missing-system tickets, or business/product operating goals.
