---
kind: skill-maintenance-audit
skill: feed-scout
date: 2026-07-24
ticket_id: TASK-0403
---

# Feed Scout Source Instructions Audit

## Expected

One inherited/refining `instructions` field should describe what Feed Scout
does with an entity/source while fixed policy owns proposal routing and safety.

## Previous

`interest_prompt` described extraction/ranking and the design proposed a second
`source_discovery_prompt`. Owned-source records also repeated their key's type
in `kind`.

## Change

- replaced the prompt contract with `instructions` and `instructions_ref`;
- removed redundant source `kind`;
- added fixed proposal routing and one-hop source nomination;
- separated canonical item dedupe from semantic source redundancy;
- added validator tests, behavior evals, QA guards, and framework docs.

## Validation

See `tickets/TASK-0403/artifacts/qa/verification.md`.
