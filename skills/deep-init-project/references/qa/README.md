# QA

Reusable browser-QA guidance lives here.

This folder is for durable how-to surfaces that make UI verification fast,
deterministic, and easy to automate. It is not the place for per-ticket proof
artifacts. Those still belong under `tickets/TASK-XXXX/artifacts/`.

## Recommendation

Default to this flow:

1. prove or debug the workflow with `agent-browser` when the path is new,
   brittle, or not yet instrumented
2. codify the stable happy path in Playwright once the flow is understood
3. keep `agent-browser` as the debugging lane when the Playwright test breaks

In practice, that means:

- **Playwright first for regression:** use Playwright for stable end-to-end UX
  checks after UI changes so the proof is programmatic, repeatable, and easy to
  run in parallel
- **`agent-browser` first for discovery:** use it when you still need to prove
  that a workflow can work end to end, when selectors are not obvious yet, or
  when a Playwright failure needs browser-level debugging
- **instrumentation over wandering:** if QA has to click through too much UI,
  add a shortcut, deep link, seed/reset path, debug HUD, or test-only toggle
  and record it in the cookbook

Before any browser evidence run, the repo should also document:

- the preferred launch path for ordinary app work versus QA/evidence capture
- whether the workflow expects app-only, app plus DB, or a fuller orchestrated stack
- which URLs, ports, or env vars QA should trust after launch

## What Belongs Here

- deep links to the relevant route or screen
- auth bypass or seeded-state notes for local/test environments
- the canonical launch command or profile for evidence capture
- required supporting services and how they are started
- expected local targets such as frontend/backend URLs
- keyboard shortcuts, debug buttons, and quick-open panels
- deterministic setup flows such as reset, seed, pause, resume, or step
- stable selector expectations such as `data-testid` contracts
- notes about when a flow is ready to graduate from `agent-browser` to
  Playwright

## Suggested Layout

```text
qa/
  AGENTS.md
  README.md
  cookbook/
    README.md
    TEMPLATE.md
    <app-or-feature>.md
```

## Cookbook Workflow

Use a cookbook page when a feature needs repeated QA access.

- Start with the fastest deterministic entry path.
- Name the launch command or runtime profile that should already be running.
- Name the selectors and assertion surfaces Playwright should use.
- Record the debug hooks `agent-browser` can use when Playwright fails.
- If the path is still painful, write down the missing instrumentation as a
  follow-up instead of normalizing brittle manual setup.

## Last-Step Rule

The final proof target for user-facing browser flows should usually be a
Playwright test, not a transcript of agentic clicking.

`agent-browser` is still valuable, but mostly for:

- proving the first working path
- capturing evidence while a feature is in flux
- debugging why a scripted test is failing
