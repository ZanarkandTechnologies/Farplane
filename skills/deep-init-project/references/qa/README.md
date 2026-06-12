# QA

Reusable browser-QA guidance lives here.

This folder is for durable how-to surfaces that make UI verification fast,
deterministic, and easy to automate. It is not the place for per-ticket proof
artifacts. Those still belong under `tickets/TASK-XXXX/artifacts/`.

## Recommendation

Default to this flow:

1. prove or debug the workflow with `agent-browser` when the path is new,
   brittle, or not yet instrumented
2. capture the ticket evidence from `agent-browser`: snapshot, screenshots,
   console logs, page errors, and the tested route or state
3. codify the stable happy path in Playwright only when repeated regression
   coverage is worth the extra harness overhead

In practice, that means:

- **`agent-browser` first for browser proof:** use it for most ticket QA,
  exploratory UI checks, visual state capture, console/error inspection, and
  any workflow whose selectors or assertions are not already settled
- **Playwright for regression:** use Playwright when the task explicitly needs
  a durable automated UX regression, an existing Playwright suite is the
  acceptance surface, or a stable flow is ready to graduate into scripted
  coverage
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
- notes about when a flow deserves Playwright coverage instead of
  `agent-browser` proof alone

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
- Name the `agent-browser` evidence to capture for the normal QA path.
- Record the selectors and assertion surfaces Playwright should use only when
  the flow is ready for regression coverage.
- If the path is still painful, write down the missing instrumentation as a
  follow-up instead of normalizing brittle manual setup.

## Regression Graduation Rule

The final proof target for user-facing browser flows should usually be an
`agent-browser` evidence bundle unless the ticket asks for repeatable
regression coverage.

Playwright is still valuable, but mostly for:

- stable, already-understood flows
- critical paths that need repeated automated coverage
- failures in an existing scripted suite
