# Workflows

## Standard Landing Page

1. Enter Planner unless an approved `LANDING_SPEC.md` exists.
2. Define offer and audience.
3. Choose story arc.
4. Map sections.
5. Draft a low-fidelity ASCII flow.
6. Complete the section matrix: user job, narrative claim, visual carrier,
   asset plan, motion/effect, proof/copy payload, and QA assertion.
7. Set visual rules through `visual-design`.
8. Plan motion only where it strengthens the story.
9. Validate the spec with `scripts/landing_spec_lint.py`.
10. Hand off to `frontend-craft` only after approval.
11. Verify with section-quality QA and designer judgment after build.

## Cinematic Scrolltelling

1. Define narrative phases in `LANDING_SPEC.md`.
2. Choose pinned/sticky or native-scroll structure.
3. Plan media layers and fallback assets per section.
4. Route complex timelines to official GreenSock skills or docs.
5. Require hero scroll scrub plus lower-section visual carriers.
6. Verify desktop/mobile/reduced-motion checkpoints.
7. Run section-quality QA so blank lower-page panels fail even when the hero
   passes.
8. Run designer judgment before claiming premium or Terminal-level quality.
