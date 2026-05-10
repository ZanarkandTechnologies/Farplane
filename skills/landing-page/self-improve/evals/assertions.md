# Landing Page Self-Improve Assertions

Durable smoke assertions for known landing-page failures.

## Asset Evidence Regression

Given a premium or cinematic landing-page build:

- `assets/asset-manifest.json` exists.
- At least one primary media asset is real/generated and filesystem-backed.
- The primary media asset has provenance.
- The primary media asset has poster or reduced-motion fallback evidence.
- A manifest containing only `code-rendered-canvas`, `inline-svg`,
  `html-css-visual`, `three-js`, `webgl`, or `procedural` fails.

## Video Generation Regression

Given a premium cinematic hero that promises generated video:

- `generated-video` assets require video-generation provenance such as a
  `videoModel`, `videoProvider`, `sourceVideo`, or recognized video-generation
  app/model.
- A local `ffmpeg` transcode from generated still images or an image sequence
  fails as `generated-video`.
- Still-frame assembly must be declared as `frame-sequence` or downgraded to
  prototype unless the plan explicitly accepts frame-sequence quality.
- `Seedream`/image-generation provenance alone is not valid video-generation
  provenance.

## Planner / Executor Regression

Given a premium landing-page request:

- no approved `LANDING_SPEC.md` means no build handoff,
- approved specs include section matrix, asset plan, motion plan, QA gates, and
  executor handoff,
- final claims require asset-evidence QA plus section-quality QA.
