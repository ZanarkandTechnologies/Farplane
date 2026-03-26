# Visual debugging escalation recipes

Canonical debugging bundle and report requirements live in `../SKILL.md`.
Use this file for escalation patterns when the default bundle is not enough.

## Escalation: Trace capture for timing/flakes

```bash
mkdir -p test-results
agent-browser trace start test-results/trace.zip
# Reproduce issue
agent-browser snapshot -i -c --json
agent-browser trace stop test-results/trace.zip
agent-browser screenshot test-results/after.png
```

## Escalation: Headed mode for visual parity checks

```bash
agent-browser open http://localhost:3000 --headed
agent-browser snapshot -i -c --json
```

## Escalation: Auth/gated-flow state capture

```bash
mkdir -p test-results
agent-browser state save test-results/auth.json
# Later
agent-browser state load test-results/auth.json
```

## Escalation notes

- Always include artifact paths in `docs/research/qa-testing/YYYY-MM-DD_visual-qa.md`.
- If the UI is hard to assert (canvas/video/timeline), add stable selectors (`data-testid`) or expose critical state text in DOM.
- Keep final report shape aligned with `../SKILL.md`: `Expected UI Spec -> Observed Snapshot Report -> Diff Report -> Fix Plan`.
- If the ticket does not declare the screens/states clearly enough to compare, stop and report underspecified QA before doing deeper browser exploration.
