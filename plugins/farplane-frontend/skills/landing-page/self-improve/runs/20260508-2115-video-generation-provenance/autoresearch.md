# Autoresearch: landing-page video-generation provenance gate

## Objective

Prevent premium cinematic landing pages from accepting image-generator stills
assembled with `ffmpeg` as true generated video.

## Metric

- Primary: `skill_eval_pass_rate`
- Verify: `python3 skills/landing-page/scripts/test_asset_evidence_lint.py`
- Guard: `python3 skills/landing-page/scripts/test_landing_spec_lint.py && python3 skills/skill-creator/scripts/quick_validate.py skills/landing-page`

## Scope

- Editable:
  - `skills/landing-page/SKILL.md`
  - `skills/landing-page/references/*`
  - `skills/landing-page/scripts/asset_evidence_lint.py`
  - `skills/landing-page/scripts/test_asset_evidence_lint.py`
  - `skills/delegate-frontend/SKILL.md`
- Read-only observed failure:
  - `.harness/xr-medical-glasses-site/assets/asset-manifest.json`

## Baseline

The XR site manifest labeled
`assets/generated/product-ai/disassembly-v3/hero-teardown-scrub-keyframe.mp4`
as `generated-video`, but provenance showed local `ffmpeg` assembly from
Seedream/generated still frames. The old asset evidence gate passed.

## Keep Criteria

- A fixture with real video provenance passes.
- A fixture with `ffmpeg` plus generated still/image sequence provenance fails.
- The current XR site fails until it records true video-generation provenance or
  downgrades the asset to frame-sequence/prototype.
