---
example: visual-camera-control
method: ai-video-advisor:visual-camera-control
status: evidence-backed
source_ticket: TASK-0424
---

# Visual camera control example

## Request

Animate one coastal-pier location through high aerial, corkscrew dive, low
fly-by, 270-degree landmark orbit, and exact top-down crane-out perspectives.

## Before

One control diagram and one ten-second prompt contained all five timed states.
The generated clip preserved the location and achieved multiple perspectives,
but strict QA marked only high oblique and low fly-by clear. The helix, orbit,
and final top-down view were partial.

Evidence: `tickets/TASK-0424/artifacts/experiment-evidence.md`.

## After

```text
method: ai-video-advisor:visual-camera-control
topology: chained_maneuvers
selection_reason:
  - five independently scored camera states
  - landmark-locked orbit greater than 120 degrees
  - high and low perspectives plus exact terminal view
  - prior single-shot adherence failure

clips:
  - 01_approach_dive: high aerial -> aligned low pier entrance
  - 02_low_flyby: low entrance -> Ferris-wheel approach
  - 03_orbit: gaze-locked orbit start -> translated 270-degree end anchor
  - 04_crane_out: orbit exit -> designed near-vertical top-down anchor
```

Each clip receives clean identity references, explicit start/end frame roles,
one geometric movement prompt, and one observable acceptance condition. Clip N
must pass and supply the start frame for clip N+1 before later generation spend.

## What this proves

- Visual primitives remain useful as a human direction layer.
- The executable unit is the compiled semantic maneuver, not the drawn arrow.
- Multiple perspective anchors improve spatial intent, but complex movements
  require topology and handoff control.
- Resource Bank can retain the source and golden examples; AI Video Advisor
  owns execution and adherence.
