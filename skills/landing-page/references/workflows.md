# Workflows

## Standard Landing Page

1. Create or validate `LANDING_SPEC.md`; keep the handoff blocked until the
   specification is approved.
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
12. Return the approved spec to the calling `impl-plan`.
13. Require asset-evidence QA, section-quality QA, and designer judgment in the
    downstream proof contract.

## Cinematic Scrolltelling

1. Define narrative phases in `LANDING_SPEC.md`.
2. Choose pinned/sticky or native-scroll structure.
3. Plan media layers and fallback assets per section.
4. For product pages, make the pinned/scrubbed media reveal meaningful product
   states: context, product shot, parts/exploded or assembly view, feature
   callout, reassembled final state.
5. Route complex timelines to official GreenSock skills or docs.
6. Resolve the hero media source/generation packet or preserve its blocker.
7. Require hero scroll scrub plus lower-section visual carriers.
8. Put desktop/mobile/reduced-motion checkpoints in the proof plan.
9. Require asset-evidence QA so code-native placeholders fail premium claims.
10. Require section-quality QA so blank lower-page panels fail even when the
    hero passes.
11. Require designer judgment before a downstream premium or Terminal-level
    completion claim.

## Modern Scroll-Scrub Recipe

For Terminal/Terminus-inspired, premium industrial, generated-media, or
asset-heavy pages, use the parent skill `SKILL.md` Todo List as the active todo list. The required
order is:

1. competitor/inspiration analysis,
2. user-story and section-count decision,
3. low-fidelity ASCII page flow,
4. nested `advise` exploration for every section,
5. generated/rendered hero video and scrub-friendly frame or keyframe plan,
6. spec-first handoff,
7. downstream implementation requirements with scroll-scrub instrumentation,
8. downstream desktop/mobile visual QA plus scroll-scrub QA.
