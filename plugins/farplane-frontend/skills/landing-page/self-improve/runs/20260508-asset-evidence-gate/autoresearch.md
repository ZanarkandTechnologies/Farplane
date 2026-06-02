# Autoresearch: landing-page asset evidence gate

## Objective
Prevent `landing-page` from approving premium/cinematic pages that contain only
code-rendered or inline visuals when generated or real media was expected.

## Metric
- Primary: `skill_eval_pass_rate`
- Verify: `python3 skills/landing-page/scripts/test_asset_evidence_lint.py`
- Guard: `python3 skills/landing-page/scripts/test_landing_spec_lint.py && python3 skills/skill-creator/scripts/quick_validate.py skills/landing-page`

## Scope
- Editable:
  - `skills/landing-page/SKILL.md`
  - `skills/landing-page/references/*`
  - `skills/landing-page/scripts/*`
  - `skills/landing-page/self-improve/*`
- Read-only:
  - `.harness/xr-medical-glasses-site/*` as the observed failed prototype.
- Off limits:
  - unrelated skills and ticket metadata.

## Constraints
- Do not require media generation for simple landing pages.
- Do not ban canvas/SVG/WebGL as support visuals.
- Do fail premium/cinematic final claims when no generated or real
  filesystem-backed media exists.

## What's Been Tried
- The previous planner/executor and section-quality gates passed the XR medical
  prototype despite no generated media assets.

## Next Ideas
- Add asset-evidence lint for manifest provenance and existing media paths.
- Add a delegated-Pi eval that requires generated media path handoff.
