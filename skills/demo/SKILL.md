---
name: demo
description: Run the demo phase for one selected ticket by turning passing QA artifacts into demo-ready outputs and producing a structured demo result artifact for Stop-hook gating.
tier: 3
group: coding
source: local
---

# Demo

`$demo` is the demo-packaging phase for a selected ticket.

Use it when:

- the ticket requires demo output
- QA has already passed and produced reusable artifacts
- `$impl` or the operator needs to rerun demo generation without redoing QA

Do not use it when:

- QA has not passed yet
- the ticket does not require a demo artifact

## Contract

- Read the selected ticket plus linked docs/specs.
- Reuse QA artifacts from `tickets/TASK-XXXX/artifacts/qa/`.
- If QA evidence is missing, weak, or not presentation-ready, request a QA rerun
  or use [agent-browser](../agent-browser/SKILL.md) only for a narrow missing
  browser capture.
- Write demo outputs under `tickets/TASK-XXXX/artifacts/demo/`.
- Update the ticket `Evidence` section with demo artifact links.
- Write `result.json` under the demo artifact root and finish with:
  - `IMPL_RESULT: status=demo_complete next=building reason=...`

## Required artifacts

- `result.json`
- at least one demo-ready output such as HTML, slides, clip, or storyboard pack

## `result.json` shape

```json
{
  "ticket_id": "TASK-0000",
  "phase": "demo",
  "verdict": "pass",
  "summary": "demo artifacts are ready",
  "artifacts": [
    "tickets/TASK-0000/artifacts/demo/2026-04-24T211500Z/demo.html"
  ]
}
```

The final Stop-hook reviewer may still fail completion even when demo `verdict`
is `pass` if the output is not presentation-ready enough to show upward to a PM
or CEO.
