# Visual QA workflow extensions

Canonical workflow and output contract live in `../SKILL.md`.
Use this file only for variants that are not needed every run.

<!--
Command-heavy browser workflows live here on purpose.
Keep the top-level visual-qa skill focused on judgment and report shape.
-->

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

```bash
mkdir -p test-results
agent-browser snapshot -i -c --json > test-results/before.snapshot.json
agent-browser screenshot test-results/before.png

# Exercise changed UI using snapshot refs (prefer @e1 over CSS selectors)
agent-browser snapshot -i -c --json

agent-browser snapshot -i -c --json > test-results/after.snapshot.json
agent-browser screenshot test-results/after.png
```

Use the ticket's declared screens/states to decide what to capture; do not rely on ad-hoc exploration alone.

## Variant: Snapshot-driven bug reproduction

<!--
Use this when you need a compact artifact pack for one failing state rather than a full screen-by-screen pass.
-->

Use this when you already know the failing state and need a compact repro bundle.

```bash
mkdir -p test-results
agent-browser snapshot -i -c --json > test-results/repro.snapshot.json
agent-browser screenshot test-results/repro.png
agent-browser console > test-results/console.txt || true
agent-browser errors > test-results/errors.txt || true
```

Report repro steps plus artifact paths in `docs/research/qa-testing/YYYY-MM-DD_visual-qa.md`, and name which declared screen/state the bundle corresponds to.

## Variant: Trace capture

<!--
Timing and flake variant.
This should be opt-in because traces are heavier than the default artifact pack.
-->

Use this when timing or flake is part of the bug.

```bash
mkdir -p test-results
agent-browser trace start test-results/trace.zip

# Reproduce issue
agent-browser snapshot -i -c --json

agent-browser trace stop test-results/trace.zip
agent-browser screenshot test-results/after.png
```

## Variant: Multi-user flows with sessions

<!--
Separate sessions keep role-dependent UI evidence from collapsing into one browser context.
-->

Use separate browser sessions when layout/state depends on two roles or users.

```bash
agent-browser --session A open http://localhost:3000
agent-browser --session B open http://localhost:3000
agent-browser --session A snapshot -i -c --json
agent-browser --session B snapshot -i -c --json
# ...drive both sides...
agent-browser --session A screenshot test-results/sessionA.png
agent-browser --session B screenshot test-results/sessionB.png
agent-browser --session A close
agent-browser --session B close
```

## Variant: Scroll-driven or animation-heavy pages

For long narrative pages, timeline scrubbing, and animation validation:

- Use `cinematic-landing` -> `references/testing.md`
- Reuse the same `Expected UI Spec -> Observed Snapshot Report -> Diff Report -> Fix Plan` format from `../SKILL.md`
- Keep the ticket's design intent and `docs/TASTE.md` visible in the report even when the page is animation-heavy.
