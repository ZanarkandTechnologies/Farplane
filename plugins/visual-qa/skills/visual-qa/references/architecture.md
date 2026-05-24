# Architecture

`visual-qa` is a judgment layer for UI evidence. It does not own browser
orchestration, ticket state, or implementation changes.

## Inputs

- active ticket or delegated UI contract,
- expected screens, states, and taste references,
- screenshot, snapshot, trace, console, or geometry evidence,
- browser/QA runbook output when available.

## Outputs

- Expected UI Spec,
- Observed Snapshot Report,
- Diff Report and verdict,
- Fix Plan with component/CSS-level directives,
- best evidence item for ticket or handoff writeback.

## Boundaries

- Browser driving belongs to QA runbooks or `qa-tester`.
- Product workflow decisions belong to `functional-ui`.
- Visual-system decisions belong to `visual-design`.
- Landing-page media and scroll proof gates belong to `landing-page`.
