# <workflow name>

## Goal
- What user-visible behavior this workflow should prove.

## Fast Entry
- Route or deep link:
- Shortcut or debug control:
- Panel or mode to open directly:

## Setup
- Preferred launch path:
- Auth / fixture / seed:
- Reset path:
- Commands:
- Targets / ports:
- Required services:

## Stable Selectors
- `data-testid`:
- Roles / labels:
- Assertion targets:

## agent-browser Path
1. Open the same fast entry path.
2. Use the shortcut or debug control if needed.
3. Capture `snapshot.json`, screenshots, console, and errors on failure.
4. Record the user-visible result and any unresolved instrumentation gap.

## Playwright Path
1. Use only when the workflow needs repeatable regression coverage.
2. Navigate using the fast entry path.
3. Assert the screen or panel is ready.
4. Perform the stable happy path.
5. Assert the user-visible result.

## Observability
- Debug HUD:
- DOM mirrors:
- Event logs:
- Pause / step / inspect helpers:

## Known Gaps
- Missing shortcut:
- Missing deterministic helper:
- Missing selector or assertion surface:
