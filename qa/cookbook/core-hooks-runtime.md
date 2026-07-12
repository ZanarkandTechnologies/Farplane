---
template_id: qa-cookbook-workflow
template_version: "0.1.0"
ticket_refs:
  - TASK-0333
status: planned
updated_at: 2026-07-12
---

# Core Hooks Runtime

Use this workflow to prove Farplane Core hook installation, health reporting,
local typed-event capture, and event-to-program routing without relying on
Farplane UI or mutating the operator's live tickets.

## Open

```bash
python3 bin/farplane.py hooks list --json
python3 bin/farplane.py hooks doctor --json
```

## Stabilize

- Create a temporary Codex home with a rendered `hooks.json`.
- Create a temporary Farplane project fixture with `farplane/hooks.json`,
  `farplane/bindings.yaml`, and two routes for one supported typed event.
- Use fixture payloads for the observed Codex hook variants.
- Do not edit the real `~/.codex/hooks.json` for negative cases.

## Inspect

- Doctor's complete managed-command inventory and issue/hint rows.
- `.farplane/` typed event/outbox and nonfatal hook error receipts.
- `.farplane/hooks/drain-launches/*.json` local child-process launch receipts.
- Each matched mining run's `run.json`, frozen program/input, and report.
- Repeated payload behavior: the same event/route/program/input identity must
  not create an unintended duplicate run.

## Fast Proof

```bash
python3 bin/farplane.py hooks test --project-root <fixture> --json
```

If the final command name differs, keep one equivalent deterministic Core CLI
entrypoint and update this cookbook atomically.

## Required Cases

1. Healthy Core-local install: all managed commands resolve without UI/Node.
2. Broken command: Doctor returns nonzero/`ok: false` and an exact repair hint.
3. One typed event, two routes: two immutable mining runs appear exactly once.
4. Retry: pending local routes drain without duplicate logical runs.
5. Processor failure: Codex hook exits safely while a local error receipt makes
   the failure inspectable.
6. Process boundary: event record/outbox exists before drain launch, the drain
   has a distinct child PID/process receipt, and the hook process does not run
   mining inline.
7. Failed launch: a broken fixed drain command leaves the event pending, and a
   later local drain completes the same event exactly once.

## Evidence

Write compact receipts and logs under:

- `tickets/TASK-0333/artifacts/smoke/`
- `tickets/TASK-0333/artifacts/qa/`

The final reviewer must compare the healthy and deliberately broken Doctor
results and inspect the two-route run identities.
