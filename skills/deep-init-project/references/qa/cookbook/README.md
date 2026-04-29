# QA Cookbook

Add one page per app area or repeatable workflow.

Keep each page short and biased toward deterministic access.

## Page Checklist

- `Goal:` what the workflow proves
- `Fast entry:` route, deep link, shortcut, or debug control
- `Setup:` seed, reset, auth, fixture, local command, or runtime profile
- `Targets:` frontend/backend URLs, ports, or supporting services QA should trust
- `Stable selectors:` the roles, labels, or `data-testid` values that should
  stay reliable
- `Playwright path:` the canonical automated happy path
- `agent-browser path:` the fallback or debugging sequence
- `Observability:` logs, HUDs, DOM mirrors, or debug panels that make failures
  understandable
- `Known gaps:` missing shortcuts or helpers that still need implementation
