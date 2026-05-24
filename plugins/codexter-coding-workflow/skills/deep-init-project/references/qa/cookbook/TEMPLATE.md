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

## Playwright Path
1. Navigate using the fast entry path.
2. Assert the screen or panel is ready.
3. Perform the stable happy path.
4. Assert the user-visible result.

## agent-browser Path
1. Open the same fast entry path.
2. Use the shortcut or debug control if needed.
3. Capture `snapshot.json`, screenshots, console, and errors on failure.
4. Record anything Playwright could not prove yet.

## Observability
- Debug HUD:
- DOM mirrors:
- Event logs:
- Pause / step / inspect helpers:

## Known Gaps
- Missing shortcut:
- Missing deterministic helper:
- Missing selector or assertion surface:
