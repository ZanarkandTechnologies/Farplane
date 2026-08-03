# Visual debugging escalation recipes

Canonical debugging bundle and report requirements live in `../SKILL.md`.
Use this file for escalation patterns when the default bundle is not enough.

## Escalation: Trace capture for timing/flakes

Use the Codex in-app Browser with developer access to start a trace, reproduce
the issue in the existing tab, capture the final page state and screenshot,
then save the trace and image under the ticket QA artifact directory.

## Escalation: Headed mode for visual parity checks

Open the local route in the Codex in-app Browser, inspect the visible and
interactive page state, and capture the parity screenshot from that tab.

## Escalation: Auth/gated-flow state capture

Use `@Chrome` only when the flow requires the operator's existing authenticated
Chrome state. Never export cookies, local storage, credentials, or browser
profiles into the repository. Verify the active account before acting.

## Escalation notes

- Always include artifact paths in `tickets/TASK-XXXX/artifacts/qa/<timestamp>/visual-qa.md`.
- If the UI is hard to assert (canvas/video/timeline), add stable selectors (`data-testid`) or expose critical state text in DOM.
- Keep final report shape aligned with `../SKILL.md`: `Expected UI Spec -> Observed Snapshot Report -> Diff Report -> Fix Plan`.
- If the ticket does not declare the screens/states clearly enough to compare, stop and report underspecified QA before doing deeper browser exploration.
