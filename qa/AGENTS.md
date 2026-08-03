# QA Module

This folder is the repo-owned home for reusable QA runbooks that help agents
and humans reach important app states quickly and deterministically.

## Purpose

- keep durable QA entry guidance out of chat transcripts
- store shortcuts, deep links, seeded fixtures, and debug hooks that make UI
  proof fast
- complement ticket-scoped artifacts instead of replacing them

## Rules

- use `qa/` for reusable guidance, not per-run evidence
- keep screenshots, logs, traces, and one-off reports under
  `tickets/TASK-XXXX/artifacts/`
- treat `skills/qa/SKILL.md` as the execution and receipt contract; this module
  owns readable guidance and reusable runbooks
- prefer the Codex in-app Browser for browser proof: page operation, snapshots,
  screenshots, console/network inspection, and page-error capture
- use Playwright only when stable UX regression coverage is explicitly needed,
  when an existing suite is the acceptance surface, or when a settled flow is
  ready to graduate into scripted coverage
- when a workflow is hard to automate, document the missing shortcut,
  deterministic setup, or instrumentation helper here so later tickets can land
  the fix intentionally
- after each run classify learning as `ticket_only`, `cookbook_update`, or
  `instrumentation_ticket`; do not force a cookbook edit for one-off facts

## Expected Contents

- `README.md`: the default browser-automation policy
- `cookbook/`: reusable app or feature guides

## Cookbook Standard

Each cookbook page should stay short and answer:

1. how QA reaches the target state quickly
2. which shortcuts, deep links, seeds, or fixtures make it deterministic
3. what the Codex in-app Browser should capture for the normal proof path
4. when the flow is worth graduating to Playwright regression coverage
5. the shortcut environment guard, expected state, cleanup, and last verified receipt
