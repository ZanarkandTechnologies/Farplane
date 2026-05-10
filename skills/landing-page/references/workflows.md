# Workflows

## Standard Landing Page

1. Enter Planner unless an approved `LANDING_SPEC.md` exists.
2. Define offer and audience.
3. Choose story arc.
4. Map sections.
5. Draft a low-fidelity ASCII flow.
6. Complete the section matrix: user job, narrative claim, visual carrier,
   asset plan, motion/effect, proof/copy payload, and QA assertion.
7. For product/device/equipment pages, complete the Product Demo Plan:
   realistic product shot, in-context use shot, assembly/disassembly or
   exploded-view sequence, highlighted parts/features, and meaningful
   scroll/video states.
8. Complete the asset evidence plan: generated/real media paths, provenance,
   poster, reduced-motion still, mobile variant, and asset manifest.
9. Set visual rules through `visual-design`.
10. Plan motion only where it strengthens the story.
11. Validate the spec with `scripts/landing_spec_lint.py`.
12. Hand off to `frontend-craft` only after approval.
13. Verify with asset-evidence QA, section-quality QA, and designer judgment
    after build.

## Cinematic Scrolltelling

1. Define narrative phases in `LANDING_SPEC.md`.
2. Choose pinned/sticky or native-scroll structure.
3. Plan media layers and fallback assets per section.
4. For product pages, make the pinned/scrubbed media reveal meaningful product
   states: context, product shot, parts/exploded or assembly view, feature
   callout, reassembled final state.
5. Route complex timelines to official GreenSock skills or docs.
6. Generate or collect the hero media asset before claiming final quality.
7. Require hero scroll scrub plus lower-section visual carriers.
8. Verify desktop/mobile/reduced-motion checkpoints.
9. Run asset-evidence QA so code-native placeholders fail premium claims.
10. Run section-quality QA so blank lower-page panels fail even when the hero
   passes.
11. Run designer judgment before claiming premium or Terminal-level quality.
