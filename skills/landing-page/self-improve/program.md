# Self-Improve Program: landing-page

## Objective
Make `landing-page` reliably produce premium/cinematic landing pages with real
or generated asset evidence, not only code-native visual placeholders.

## Current Contract
- Trigger: one-page marketing, launch, homepage, portfolio, hero-heavy,
  cinematic, or scrolltelling surfaces.
- First-load workflow: Planner writes and approves `LANDING_SPEC.md`; Executor
  builds only after spec validation.
- Outcome: landing brief, implementation handoff, generated/real asset plan,
  motion plan, QA plan, and final evidence pack.
- Validation: spec lint, asset-evidence lint, section-quality QA,
  designer-judgment review, mobile/reduced-motion/browser checks.

## Eval Metric
- Primary: `skill_eval_pass_rate`
- Direction: higher
- Minimum meaningful delta: one known real failure mode becomes mechanically
  caught.
- Simplicity guard: prefer references and scripts over bloating `SKILL.md`.

## Rubric
- Spec-first planning before build.
- Generated or real media provenance for premium/cinematic pages.
- Explicit downgrade when media generation is unavailable.
- Scroll/motion QA proves behavior.
- Section-quality QA catches blank lower sections.
- Designer judgment catches under-authored pages.

## Durable Evals
- `scripts/test_landing_spec_lint.py`
- `scripts/test_asset_evidence_lint.py`
- `self-improve/evals/test_cases.jsonl`
- `self-improve/evals/assertions.md`

## Experiment Log
| Date | Run | Hypothesis | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- |
| 2026-05-08 | asset-evidence-gate | Add a post-build manifest linter so code-rendered/SVG-only premium pages fail | Added `asset_evidence_lint.py`, tests, QA docs, and live skill routing | yes | The XR glasses prototype passed section QA without generated media; premium claims require filesystem-backed generated or real media evidence. |
| 2026-05-08 | video-generation-provenance | Require `generated-video` assets to prove actual video-generation provenance instead of accepting image stills plus `ffmpeg` | Added a failing regression fixture, video provenance validation, delegate handoff rule, and live XR failure proof | yes | Seedream/image-generation plus local `ffmpeg` is a frame sequence, not generated video. |

## Accepted Learnings
- Section-quality QA proves visible section substance, not generated asset
  provenance.
- Canvas, SVG, Three.js, WebGL, and HTML/CSS visuals can support a premium page,
  but cannot be the only evidence when the brief promises generated/real media.
- If media generation cannot run, downgrade to `prototype` and record the asset
  blocker instead of claiming premium/cinematic quality.
- `generated-video` must come from a video model/app or source video. If the
  run only has image-generator stills assembled with `ffmpeg`, declare the
  asset as `frame-sequence` or downgrade to prototype.

## Rejected Ideas
- Do not solve this with stronger wording alone; the XR failure showed prose
  was insufficient without a mechanical asset-evidence gate.

## Next Hypotheses
- Add real generated-media fixtures once local image/video generation is
  available in the tracked repo.
- Extend asset lint to validate frame sequence manifests and first-frame
  dimensions.
- Add a delegated-Pi eval that fails if a generated-video handoff lacks
  `skillsActuallyUsed: video-generation` and video model/source provenance.
- Add a video-quality eval that judges whether real generated video has
  meaningful motion after the provenance gate passes.
