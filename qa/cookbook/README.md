# QA Cookbook

Add one page per app area or repeatable workflow.

Keep each page short and biased toward deterministic access.

## Page Checklist

- `Goal:` what the workflow proves
- `Fast entry:` route, deep link, shortcut, or debug control
- `Setup:` seed, reset, auth, fixture, or local command
- `Stable selectors:` the roles, labels, or `data-testid` values that should
  stay reliable
- `agent-browser path:` the normal page-operation and evidence-capture path
- `Playwright path:` only when the workflow has graduated to scripted
  regression coverage
- `Observability:` logs, HUDs, DOM mirrors, or debug panels that make failures
  understandable
- `Known gaps:` missing shortcuts or helpers that still need implementation

Use [TEMPLATE.md](/Users/kenjipcx/coding-harness/Farplane/qa/cookbook/TEMPLATE.md)
when adding a new page.
