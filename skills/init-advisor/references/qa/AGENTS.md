# QA Module

This folder is the repo-owned home for reusable QA runbooks that help agents
and humans reach important app states quickly and deterministically.

## Purpose

- keep durable browser-test entry guidance out of chat transcripts
- store shortcuts, deep links, seeded fixtures, and debug hooks that make UI
  proof fast
- complement ticket-local `tickets/TASK-XXXX/artifacts/` instead of replacing it

## Rules

- use `qa/` for reusable guidance, not per-run evidence
- keep screenshots, logs, traces, and one-off reports under
  `tickets/TASK-XXXX/artifacts/`
- keep the canonical evidence-capture launch path, required services, and
  expected targets visible here rather than in chat memory
- prefer `agent-browser` for browser proof: page operation, snapshots,
  screenshots, console logs, and page-error capture
- use Playwright only when stable UX regression coverage is explicitly needed,
  when an existing suite is the acceptance surface, or when a settled flow is
  ready to graduate into scripted coverage
- when a workflow is hard to automate, document the missing shortcut,
  deterministic setup, or instrumentation helper here so later tickets can land
  the fix intentionally

## Expected Contents

- `README.md`: the default browser-automation policy
- `cookbook/`: reusable app or feature guides

## Cookbook Standard

Each cookbook page should stay short and answer:

1. how QA reaches the target state quickly
2. which shortcuts, deep links, seeds, or fixtures make it deterministic
3. which launch path, services, targets, or ports QA should trust
4. what `agent-browser` should capture for the normal proof path
5. when the flow is worth graduating to Playwright regression coverage
