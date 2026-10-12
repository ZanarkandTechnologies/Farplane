# Visual Mode

Load this for `qa(target, mode: visual)`: judging already captured UI evidence
against the issue's `design.md`, `docs/TASTE.md`, and declared screens/states.
Visual mode is a judgment pass. Capture belongs to the functional run or
`qa-tester`; a capture is never its own visual approval.

```text
visual_judgment(issue, design_md, screenshots + DOM facts)
  -> four-part report per state + design coverage + best image + verdict
```

## Required Context

Read before judging any screen:

1. the GitHub issue body (scope, declared screens/states, evidence checklist);
2. the issue's `design.md` with copy-complete ASCII screen/state IDs;
3. the UI contract: key screens/states, taste refs, expected artifacts;
4. `docs/TASTE.md` when taste, density, or layout quality is in scope.

If the expected screens/states cannot be named, `design.md` is missing or
stale, the launch path is too vague to reproduce, or the feature needs
instrumentation the issue does not acknowledge: return `fail` as
underspecified. Do not invent target screens or accept route completion.

## Verdict Start

```text
Expected baseline: <design.md path | Agent Contract | issue state | missing>
Best image: <path | missing expected artifact .farplane/qa/<issue>/<run>/screens/<state>.png>
Verdict: pass | revise | fail | blocked
```

## The Four-Part Report

For each changed screen or state, output all four sections; a missing section
makes visual QA incomplete.

1. **Expected UI Spec** (before interactions)
2. **Observed Snapshot Report** (what the UI actually shows)
3. **Diff Report + Verdict** (`PASS` or `FAIL`)
4. **Fix Plan** (exact directives at component/class/CSS level)

Work screen-first, not route-first: name the `design.md` state ID, restate the
expected screen in one short block, capture or open its evidence, compare
layout and style, compare behavior and state, mark `PASS` or `FAIL`, move on.

### Expected UI Spec answers

Design language (one sentence from taste + issue intent); layout map
(header/body/sidebar/footer positions); primary CTA (location, label, size,
default state); visual hierarchy (first/second/third attention targets);
spacing rhythm; typography (scale, weight, line length, truncation); color and
contrast (enabled vs disabled); elevation; alignment; narrow-viewport behavior.

### Diff report fields

`Screen`, `Design intent`, `Evidence` (exact path), `Verdict`, `Top 3 visual
diffs`, `Top 3 behavior diffs` (trigger, observed, expected), `Severity`
(`blocker | major | minor`), `Fix directives`, `Artifacts`, `Best evidence
item`, and `Design coverage`: one row per declared state/section,
`<design.md ID> -> <evidence path> -> PASS|FAIL|not_provable`, with desktop,
mobile, and readable sectional evidence. Preserve each row until superseded.

## Geometry From DOM Facts

Most UI bugs are geometry. Every diff report carries layout assertions read
from DOM facts (`getBoundingClientRect`, computed style, accessibility
snapshot, or a `*.facts.json` capture), not eyeballed from pixels. Use
viewport-relative percentages:

```json
{
  "element": "primaryCta",
  "expected_bbox_pct": { "x": [85, 100], "y": [5, 20], "w": [8, 20], "h": [5, 12] },
  "observed_bbox_pct": { "x": 88, "y": 9, "w": 12, "h": 7 },
  "tolerance_pct": 2
}
```

Assert CTA region, header/footer bounds, main-content clipping/overflow, and
relative order (A above/left of B). Missing geometry assertions make the pass
incomplete. Then read the screenshot itself to confirm what the facts imply.

## The First Viewport Proves Only That Viewport

Scroll positions, hover/focus/open states, loading/empty/error states, mobile,
and themes each need their own capture. For long-form pages, operate a real
scroll to the bottom; capture desktop and mobile full-page images plus readable
top, middle, and bottom frames; check lazy content, sticky elements, clipping,
and overflow after the scroll. A compressed full-page image is not readable
section proof; any uncovered required section is non-pass.

## Artifact Over Summary

Screenshot and DOM facts outrank review scores, readiness prose, clean console
logs, and check counts. A TAS-A summary or "92/100 ready" never overrides a
failed veto visible in the artifact. Equally, judge only against the current
brief: do not import taste bans from an unrelated project.

## Checklist

- **Visual correctness:** regions in place; no overlap, clipping, broken
  centering, unexplained whitespace, missing icons/fonts, or default-skinned
  components; loading/empty/error states purposeful; affordance honest.
- **Taste:** dense and intentional, not bulky; no accidental scrollbar; no
  heavy padding; long help text belongs in a tooltip; not plain or default.
- **Interaction:** click/tap works; hover/focus/active visible; feedback within
  300 ms; keyboard reachable with visible focus; modals trap focus and close.
- **Responsive:** ~375 px phone without overlap or horizontal overflow;
  landscape/short height when fixed bars or large heroes exist; long labels and
  larger text; reduced motion; 44 px touch targets; theme contrast; registry
  components customized to the brief. If a relevant check is skipped, say why.

## Final Review Before Handoff

Fail the report if it does not judge declared screens/states, hand-waves
layout, ignores clutter, debug leftovers, wrong components or drift from a
shared library, accepts bulky or default-looking UI without comment, says
"looks good" without evidence, or would not help implementation fix it fast.
For buyer-facing pages, a reader must find outcome, proof, and action without
the report substituting jargon for the page.

## Capture Variants

- **Default bundle:** one Codex in-app Browser tab: initial state + `before.png`,
  exercise the change, final state + `after.png`.
- **Failing-state repro:** screenshot, console, network, and page errors from the
  same tab, tagged with the declared state ID.
- **Timing or flake:** start a trace with developer access, reproduce, save the
  trace beside the final screenshot.
- **Two roles:** Playwright isolated contexts in one browser; capture each role.
- **Authenticated state:** `@Chrome` only when the operator's login is
  required; never export cookies, storage, or profiles into the repository.
- **Hard-to-assert UI** (canvas, video, timeline): request a `data-testid` or a
  DOM state mirror instead of guessing from pixels.
- **Animation-heavy landing:** also load `landing-page` -> `references/qa.md`.

Save every capture under `.farplane/qa/<issue>/<run>/` and write the report to
`visual.md` there; post the best image and verdict on the issue.

## Boundaries

Product workflow decisions belong to `prd`, visual-system decisions
to `visual-design`, landing media and scroll gates to `landing-page`, and the
broader completion verdict to `review`.
