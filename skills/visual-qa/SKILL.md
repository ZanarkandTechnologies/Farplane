---
name: visual-qa
version: 0.2.0
description: "UI verification and visual debugging skill for agents. Enforces ticket-first, taste-aware screen comparison with Expected UI Spec -> Observed Snapshot Report -> Diff Report -> Fix Plan, plus geometry/layout assertions and evidence artifacts."
---

# Visual QA Skill

<!--
Judgment-only layer.
Do not let this file expand back into a browser-orchestration prompt; runbooks belong in references.
-->

Use this when:

- captured UI evidence already exists or is being gathered
- you need a visual judgment against ticket intent and `docs/TASTE.md`
- you are debugging visual regressions, layout drift, or state/render mismatches

This skill does not own browser orchestration or ticket write-back.
It owns screen judgment only.

## Core principle

Visual truth beats "it compiles." Always produce artifacts and a structured diff report.

## Required context before QA

<!--
Visual QA should read ticket intent and taste before looking at evidence.
If the ticket is underspecified, fail early instead of reward-hacking a route.
-->

Before judging any screen, read:

1. the active ticket in `tickets/building/` or the delegated ticket file/section,
2. the ticket's UI contract (`Key screens/states`, `Taste refs`, `Expected artifacts`),
3. the ticket `Evidence checklist`, if present,
4. `docs/TASTE.md` when UI taste or layout quality is in scope.

If the ticket does not define the expected screens/states well enough to compare against reality, stop and mark QA as underspecified instead of improvising a vague check.

## Non-negotiable output contract

For each changed screen, output all four sections:

1. **Expected UI Spec** (before interactions)
2. **Observed Snapshot Report** (what the UI actually shows)
3. **Diff Report + Verdict** (`PASS` or `FAIL`)
4. **Fix Plan** (exact directives at component/class/CSS level)

If any section is missing, QA is incomplete.

## Screen-by-screen workflow

QA is screen-first, not route-first.

For each declared screen or state in the ticket:

1. restate the expected screen in one short block,
2. capture the declared evidence for that screen/state,
3. compare layout and style,
4. compare behavior and state,
5. mark `PASS` or `FAIL`,
6. move to the next declared screen/state.

The goal is to find as many declared screens/states as possible, not merely to reach the end of a happy path.

## Expected UI Spec (must answer explicitly)

- **Design language**: one-sentence restatement of taste and local ticket intent.
- **Layout map**: Header / Body / Sidebar / Footer and relative positions.
- **Primary CTA**: location, label, size, default state.
- **Visual hierarchy**: first/second/third attention targets.
- **Spacing rhythm**: consistent paddings/margins, no cramped or floaty zones.
- **Typography**: heading/body scale, weights, line-length, truncation behavior.
- **Color and contrast**: readable text/icons, clear enabled vs disabled states.
- **Elevation**: shadow/hover-lift consistency.
- **Alignment**: pixel edge alignment and baseline consistency.
- **Responsiveness**: expected behavior at narrow viewport.

## Mandatory layout assertions

Layout assertions are required in every QA diff report. Most UI bugs are geometry.

Use percentage-based checks (viewport-relative):

- CTA region: expected `x/y` range and width/height range.
- Header/footer bounds: pinned to top/bottom with clear boundaries.
- Main content bounds: no unexpected clipping or overflow.
- Relative order: region A above/below or left/right of region B.

Example assertion format:

```json
{
  "element": "primaryCta",
  "expected_bbox_pct": { "x": [85, 100], "y": [5, 20], "w": [8, 20], "h": [5, 12] },
  "tolerance_pct": 2
}
```

## Verification checklist (snapshot-first, not click-first)

### A) Visual correctness

- Regions exist and are in expected positions.
- No overlap, clipping, broken centering, or unexplained whitespace.
- No broken UI signals: missing icons/fonts, unstyled defaults, wrong component skin.
- State rendering is valid: loading, empty, and error states are purposeful and readable.
- Affordance is honest: clickable items look clickable; static items do not.

### A2) Taste alignment

- The screen feels dense and intentional rather than bulky.
- No accidental scrollbar is present without a clear reason.
- Panels, cards, and containers are not overly padded or visually heavy.
- Long explanatory text is not substituting for tooltip/help affordances.
- The screen does not look plain, generic, or default-styled.
- Component quality aligns with the project's stated taste reference (`shadcn`-quality where applicable).

### B) Interaction and state

For each interactive element (CTA, tabs, menus, inputs):

- Click/tap works reliably.
- Hover/focus/active states are visible.
- Action gives visible feedback within 300ms (spinner/toast/nav/state change).
- Keyboard tab reachability works and focus is visible.
- Modals/drawers trap focus and close properly (Esc/outside click when intended).

### C) Responsive behavior

- Narrow viewport keeps core task usable.
- No horizontal overflow, hidden CTA, or scroll traps.
- Sticky/fixed elements do not cover required controls.

## Failure mode: underspecified QA

Treat QA as incomplete and return `FAIL` when any of these are true:

- the ticket does not identify the key screens/states to compare,
- the expected design language is missing and cannot be inferred from `docs/TASTE.md`,
- the route or launch path is too vague to reproduce reliably,
- the feature needs extra instrumentation and the ticket does not acknowledge it.

Do not reward-hack by inventing your own target screens or by treating route completion as sufficient proof.

## Evidence capture

<!--
Evidence capture is intentionally referenced out to keep this file compact.
The top-level skill should explain what to judge, not every browser command needed to gather input.
-->

Evidence capture should follow the visual QA runbooks in `references/workflows.md`.
Use the ticket's declared screens/states to decide what to capture; do not rely on ad-hoc exploration alone.

## Diff report format (required)

<!--
This report format is the handoff boundary between visual judgment and ticket write-back.
qa-tester should surface the best evidence item into the ticket's User Evidence block.
-->

Use this exact structure:

- `Screen`: which declared screen/state this report covers
- `Design intent`: one-sentence restatement from ticket + `docs/TASTE.md`
- `Evidence`: exact screenshot/snapshot/log path used for this judgment
- `Verdict`: `PASS` or `FAIL`
- `Top 3 visual diffs`: what, where, why it matters
- `Top 3 behavior diffs`: trigger, observed behavior, expected behavior
- `Severity`: `blocker | major | minor`
- `Fix directives`: exact implementation changes (component/class/CSS-level)
- `Artifacts`: paths to snapshots/screenshots/logs/traces
- `Best evidence item`: the screenshot/artifact `qa-tester` should surface in the ticket `User Evidence` section

Write the report to:

- `docs/research/qa-testing/YYYY-MM-DD_visual-qa.md`

## PR enforcement guidance

- No screenshot + no diff report = QA incomplete.
- If geometry assertions are absent, treat QA as incomplete.
- For risky UI changes, include both baseline and after artifacts.
- If ticket context or taste context is missing, treat QA as incomplete instead of inventing a target.
- If declared evidence was not captured, treat the affected screen judgment as incomplete.
- If the report does not identify the best user-facing evidence item, QA is incomplete.

## Token-efficiency rules

- Prefer one canonical checklist over repeating variants.
- Use compact bullets and concrete diffs, not long narrative.
- Store raw evidence in `test-results/*`; summarize only high-signal findings.
- Escalate to references only for edge cases.

## Final Check

Before handoff, read `references/review.md` and tighten the QA verdict until it passes those checks.

## References

- `visual-qa` -> `references/review.md` (final review questions before handoff)
- `agent-browser` -> `references/qa-workflows.md` (advanced refs, sessions, JSON outputs)
- `visual-qa` -> `references/workflows.md` (extended workflow variants)
- `visual-qa` -> `references/debugging.md` (debug escalation recipes)
- For animation-heavy landings: `cinematic-landing` -> `references/testing.md`
