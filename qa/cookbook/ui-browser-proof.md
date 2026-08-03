# UI Browser Proof

## Goal
- Capture browser evidence when a ticket changes Farplane UI or another
  user-visible app surface.

## Fast Entry
- Route or deep link: use the app-specific route from the active ticket or
  downstream project `PROJECT_RULES.md`.
- Shortcut or debug control: prefer the documented QA shortcut for the target
  app.
- Panel or mode to open directly: use the smallest page that exposes the
  changed behavior.

## Setup
- Auth / fixture / seed: use the active ticket's setup notes.
- Reset path: use only app-owned safe reset helpers.
- Commands:
  - Use the active repo's authoritative QA / evidence command from
    `PROJECT_RULES.md`.

## Stable Selectors
- `data-testid`: prefer existing app selectors.
- Roles / labels: use accessible roles and labels before brittle CSS selectors.
- Assertion targets: visible changed behavior, loading/error states, and
  absence of console/page errors.

## Codex Browser Path
1. Start the app with the authoritative QA path.
2. Open the fast-entry route.
3. Exercise the user-visible workflow.
4. Capture screenshot, page snapshot, console logs, and page errors.
5. Save evidence under the owning ticket's `artifacts/` directory.

## Playwright Path
1. Use when the workflow has graduated to stable regression coverage.
2. Reuse the same fast-entry route and selectors.
3. Assert both the happy path and the ticket's most important failure state.

## Observability
- Screenshot.
- DOM or accessibility snapshot.
- Console logs and page errors.
- Ticket proof notes.

## Known Gaps
- This repo is not itself a UI app. Farplane UI proof normally runs in the
  Farplane UI project, then links evidence back to the owning ticket when
  needed.
