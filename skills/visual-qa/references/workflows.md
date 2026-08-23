# Visual QA workflow extensions

Canonical workflow and output contract live in `../SKILL.md`.
Use this file only for variants that are not needed every run.

<!-- Keep the top-level visual-qa skill focused on judgment and report shape. -->

## Baseline rule

Before any variant workflow:

- read the active ticket or delegated ticket section,
- extract the declared screens/states to cover,
- read `docs/TASTE.md` if UI taste is relevant,
- fail as underspecified if the target screens/states are not clear enough to compare.

## Default runbook

<!--
Standard before/after capture bundle.
Use this when no special repro mode is needed and the ticket already defines the target screens.
-->

Use this for standard visual QA when you need a compact before/after evidence bundle.

Use one Codex in-app Browser tab to capture the initial page state and
`before.png`, exercise the changed workflow, then capture the final page state
and `after.png`. Save the artifacts under the owning ticket rather than a
shared browser-state directory.

Use the ticket's declared screens/states to decide what to capture; do not rely on ad-hoc exploration alone.

## Variant: Snapshot-driven bug reproduction

<!--
Use this when you need a compact artifact pack for one failing state rather than a full screen-by-screen pass.
-->

Use this when you already know the failing state and need a compact repro bundle.

Use the Codex in-app Browser to capture the failing page state, screenshot,
console output, network evidence when relevant, and page errors from the same
tab.

Report repro steps plus artifact paths in `tickets/TASK-XXXX/artifacts/qa/<timestamp>/visual-qa.md`, and name which declared screen/state the bundle corresponds to.

## Variant: Trace capture

<!--
Timing and flake variant.
This should be opt-in because traces are heavier than the default artifact pack.
-->

Use this when timing or flake is part of the bug.

Use the Codex in-app Browser with developer access to start a trace, reproduce
the issue, capture the final screenshot, and save both artifacts under the
ticket QA directory.

## Variant: Multi-user flows with isolated contexts

<!--
Separate sessions keep role-dependent UI evidence from collapsing into one browser context.
-->

Use Playwright browser contexts when layout or state depends on two roles or
users. Keep both contexts inside one browser process when the test runner
supports it, capture each role separately, and close the contexts after the
run.

## Variant: Scroll-driven or animation-heavy pages

For long narrative pages, timeline scrubbing, and animation validation:

- Scroll the actual page to its bottom; do not infer lower-page behavior from
  browser dimensions or a first viewport.
- Capture desktop and mobile full-page images plus readable top, middle, and
  bottom frames. Check lazy-loaded content, sticky elements, clipping, and
  overflow after the scroll.
- Write `<design.md section ID> -> <evidence path> -> PASS|FAIL|not_provable`.
  An uncovered required section is a non-pass; a compressed full-page image is
  not readable section proof.
- Use `landing-page` -> `references/qa.md` for landing QA.
- Reuse the same `Expected UI Spec -> Observed Snapshot Report -> Diff Report -> Fix Plan` format from `../SKILL.md`
- Keep the ticket's design intent and `docs/TASTE.md` visible in the report even when the page is animation-heavy.
