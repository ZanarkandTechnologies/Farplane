# UI Quality

Use when reviewing UI, interaction, layout, routing, or other visible product behavior.

Threshold: `4.0`

For UI source review, pair this with
[`frontend-guidelines.md`](frontend-guidelines.md). `ui-quality` judges product
intent, taste, cohesion, and visible behavior; `frontend-guidelines` records the
source-fresh Web Interface Guidelines audit score.

## Family Score Guide

- `1`: the interface is broken, generic in damaging ways, or misses the product
  intent badly enough to fail review
- `2`: some useful UI work exists, but the result still feels weak, under-baked,
  or too generic to trust as a strong product surface
- `3`: functional and directionally aligned, but still ordinary, uneven, or
  underpowered against the intended quality bar
- `4`: strong, intentional, and pass-worthy with only minor rough edges
- `5`: distinctive, polished, and hard to improve materially within the stated
  intent

## Dimensions

- `originality`
- `design-quality`
- `craft`
- `functionality`
- `fidelity-to-intent`

### `originality`

Inspect: evidence of deliberate design choices versus stock layouts, library
defaults, or recognizable AI slop patterns.

Ask:

- Does a human designer's taste show up here, or just safe defaults?
- What choices make this feel specific rather than templated?

### `design-quality`

Inspect: cohesion of layout, mood, hierarchy, typography, color, and imagery.

Ask:

- Does the interface feel like one product, or a pile of parts?
- Is there a clear aesthetic direction, or just acceptable UI?

### `craft`

Inspect: spacing, hierarchy, color harmony, contrast, responsive behavior, and
state polish.

Ask:

- Are the fundamentals solid across states and breakpoints?
- Do rough edges distract from otherwise good ideas?

### `functionality`

Inspect: interaction clarity, task completion, state communication, and obvious
usability traps.

Ask:

- Can users complete the core flow without guessing?
- Are broken states, missing affordances, or unclear transitions hurting trust?

### `fidelity-to-intent`

Inspect: whether the result actually matches the ticket, taste target, and
surrounding product quality bar.

Ask:

- Does the visible output match the requested direction?
- What is still missing from the intended feel, emphasis, or interaction model?

## Evidence and Finding Cues

- Weak evidence usually looks like a working interface that is still obviously
  generic, visually inconsistent, or too rough to trust.
- Ordinary evidence usually covers the task but lacks distinctiveness, polish,
  or tight alignment to the intended feel.
- Strong evidence shows deliberate design choices, clean execution, and clear
  usability.
- Exceptional evidence feels authored, cohesive, and hard to confuse with stock
  output.
- Findings should name the generic pattern, broken hierarchy, missing affordance,
  or fidelity miss instead of praising the page for merely being functional.

## Example Judgments

- `2.0` example:
  the screen technically works, but it still looks like stock components with
  default spacing and weak hierarchy, so the result feels under-baked and generic.
- `3.0` example:
  the interface is usable and broadly aligned to the brief, but the visual
  direction is still ordinary and some states or interactions feel uneven.
- `4.0` example:
  the UI has a clear aesthetic direction, strong hierarchy, and reliable task
  completion, with only minor rough edges in polish or responsiveness.
- `5.0` example:
  the result feels authored rather than templated, compares well against strong
  references, and shows both taste and execution strength across states.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`

When `frontend-guidelines` also runs, include both scores in the review artifact
so later evaluation can compare taste/intent judgment against the external
guideline metric.
