---
artifact: source-output-eval
ticket: TASK-0419
status: frozen
frozen_before_candidate_generation: true
date: 2026-07-28
---

# Source-Output Eval

- Source: `https://www.youtube.com/watch?v=7wuYBfE131U`
- Learning goal: transfer the script-led, layered, narration-timed production
  workflow with rights-safe content.
- Target: 1080p Remotion MP4 plus replayable manifests/proof.

## Source Anchors

| ID | Timestamp/frame | Evidence class | Observation |
| --- | --- | --- | --- |
| A-01 | 01:13–01:44; frame-95s | transcript + frame | narration beats map to visual/asset rows |
| A-02 | 02:04–02:24; frame-130s | transcript + frame | shared background/type/accent remain locked |
| A-03 | 04:35–05:13; frame-590s | transcript + frame | background, halftone midground, structural foreground |
| A-04 | 06:15–07:03; frame-390s | transcript + frame | spring/interpolate have distinct jobs and major elements stagger |
| A-05 | 07:50–09:46; frames 470s/520s/590s | transcript + frames | generated scene is tuned via saved controls before acceptance |
| A-06 | 10:55–12:04; frames 680s/720s | transcript + frames | master scene bounds follow narration |
| A-07 | 12:06–12:49; frame-765s | transcript + frame | final MP4 contains mixed audio |

## Frozen Eval

```yaml
frozen_before_candidate_review: true
must_match:
  - six narration beats are explicitly mapped to three scene/visual contracts
  - shared background, type, and accent remain stable across scene boundaries
  - each scene separates background, monochrome/halftone midground, and structural/data foreground
  - foreground arrives before staggered midground using distinct spring/interpolate roles
  - major element x/y/scale values are persisted outside operator memory
  - at least one scene contains an animated data claim
  - master scene boundaries follow declared narration beat ranges
  - final candidate is a real 1920x1080 MP4 with narration and original audio
may_vary:
  - toy-repair subject, wording, number of assets, precise layout, palette values, system voice, music
reject:
  - source people, politics, script, prompts, frames, music, voice, logos, proprietary assets, or affiliation
  - generic montage without narration-to-visual mapping
  - scenes that merely swap backgrounds without the three-layer contract
  - all elements moving simultaneously
  - layout tuning that exists only as an undocumented manual state
  - technical render success presented as workflow proof
source_anchor_checks:
  - S-01 beat table and narration timing
  - S-02 stable visual system
  - S-03 three-layer scene architecture
  - S-04 staggered motion roles
  - S-05 persisted controls
  - S-06 data-bearing scene
  - S-07 mixed master render
```

## Proof Methods

| ID | Observable check | Proof |
| --- | --- | --- |
| S-01 | six beats map to three scene bounds and visual rows | beat manifest + audio probe |
| S-02 | background/type/accent identifiers do not change | manifest + boundary frames |
| S-03 | every scene declares all three layers | manifest + representative holds |
| S-04 | foreground onset precedes midground onsets | timing probe + frames |
| S-05 | x/y/scale controls exist for major elements | typed constants + manifest |
| S-06 | animated value resolves to 72% and holds | final scene frame + probe |
| S-07 | 1080p/30fps MP4 contains video and audio | ffprobe + final candidate |
| R-01 | protected source expression absent | source scan + manifest |

## Pass Rule

All must-match, integrity, and rights gates pass; visual/reviewer judgment is
TAS-A. A failed row must retain the exact eight-field replay schema and the
rubric must remain unchanged after candidate inspection.
