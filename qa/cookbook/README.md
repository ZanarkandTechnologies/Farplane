---
title: QA Cookbook
status: active
owner: qa
updated_at: 2026-07-14
---

# QA Cookbook

Add one page per repeatable workflow. Cookbook pages make important states
fast and deterministic; they do not store per-run evidence.

## Page Contract

- Metadata: owner, lifecycle status, source ticket, last verification date,
  and last verified receipt.
- Goal: the behavior proved.
- Fast entry: route, deep link, shortcut, debug control, or command.
- Shortcut contract: trigger, environment guard, prerequisites, expected
  state, cleanup, verification, and proof receipt.
- Setup: seed, reset, auth, fixture, runtime handoff, or local command.
- Stable selectors/assertions: roles, labels, test IDs, outputs, or state probes.
- Capture path: normal `agent-browser`, command, API, or artifact evidence.
- Playwright path: only after stable regression graduation.
- Observability: logs, HUDs, DOM mirrors, debug panels, or traces.
- Known gaps: missing instrumentation that still needs implementation.

Use [TEMPLATE.md](TEMPLATE.md) when adding or materially updating a page.

## Learning Writeback

Update a page only after a QA receipt verifies a reusable improvement. Record
the source ticket and receipt. Keep one-off workarounds in the owning ticket;
turn missing implementation into a linked instrumentation ticket.

## Workflow Index

- Verified: [Core Hooks Runtime](core-hooks-runtime.md)
- Legacy/unverified metadata: [Framework Validation](framework-validation.md)
- Legacy/unverified metadata: [Skill Validation](skill-validation.md)
- Legacy/unverified metadata: [Ticket Metadata](ticket-metadata.md)
- Generic template path: [UI Browser Proof](ui-browser-proof.md)
