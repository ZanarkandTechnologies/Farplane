---
name: avatar-advisor
description: "Turn persistent presenter, character, likeness, or lipsync needs into an avatar direction packet and generation route."
tier: 3
group: content-video
source: local
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["ai-video-advisor", "ai-image-advisor", "audio-advisor", "asset-advisor", "remotion"]
allowed-tools: Read, Grep, Glob, Bash
---

# Avatar Advisor

## Context

Use this skill when a video needs a persistent avatar, presenter, spokesperson,
character, talking head, lipsync, voice/persona continuity, or identity-safe
avatar direction. This is different from generic model-native video: the hard
part is continuity, consent, performance direction, and repeatable identity
control.

This skill owns avatar direction, identity constraints, performance notes,
voice/lipsync alignment, and provider route selection. It does not generate the
final video by default, render Remotion compositions, or publish content.

## Skill Signature

```text
avatar_advisor(character_or_presenter, script_or_storyboard, identity_refs?, voice?, consent?, platform?, artifact_owner?)
  -> avatar_direction_packet + generation_route | blocked_report

state:
  reads(user brief, script/storyboard, identity references, voice refs,
        qa_checklist.md)
  writes(avatar direction artifact when durable handoff is requested)

gates:
  identity_rights_checked; persistence_requirements_named; script_aligned;
  performance_direction_specific; voice_lipsync_route_named;
  asset_and_remotion_handoff_ready

routes:
  ai-video-advisor | ai-image-advisor | audio-advisor | asset-advisor |
  remotion | review

fails:
  unsafe_likeness_use; one_prompt_identity; missing_voice_or_script;
  avatar_route_without_continuity_checks; treating_avatar_as_generic_clip
```

## Phase Boundary

Use `ai-image-advisor` when source portraits, reference images, or character
sheets must be created or edited. Use `audio-advisor` when voice, music, SFX, or
dubbing needs a plan. Use `ai-video-advisor` for model/app selection and video
execution after this skill defines the avatar direction. Use `remotion` when
avatar clips need deterministic stitching, captions, overlays, or final local
render proof.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind identity and permission.
  - [ ] Identify presenter/character, identity references, consent/rights
    status, brand constraints, script/storyboard, platform, and artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Define persistence requirements.
  - [ ] Specify face/character continuity, wardrobe, framing, gesture style,
    voice, accent, pacing, emotional range, and reusable identity tokens or
    reference assets when available.
- [ ] 3. Direct the performance.
  - [ ] Map script beats to expression, gaze, posture, gestures, pauses,
    lipsync needs, and retake criteria.
- [ ] 4. Choose generation and asset routes.
  - [ ] Route portrait/reference creation to `ai-image-advisor` when needed.
  - [ ] Route voice, dubbing, music, SFX, and mix planning to `audio-advisor`.
  - [ ] Route model-native avatar generation or lipsync execution to
    `ai-video-advisor`.
  - [ ] Route final stitching, captions, overlays, and local render proof to
    `remotion`.
- [ ] 5. Output the avatar direction packet.
  - [ ] Include identity rules, performance map, prompt or provider brief,
    input assets, acceptance checks, blockers, and next owner.
  - [ ] Apply `qa_checklist.md` again before calling the packet ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output Template

```text
## Avatar Direction
- Identity:
- Permission / usage:
- Continuity rules:
- Voice:
- Performance:
- Platform constraints:

## Beat Map
| Beat | Script | Expression | Gesture / Framing | Lipsync / Audio | Acceptance Check |
| --- | --- | --- | --- | --- | --- |

## Routes
- Reference assets:
- Avatar generation:
- Audio:
- Remotion:

## Done / Proof
- ready_when:
- evidence:
- residual_risk:
```

## Gotchas

- Do not use real-person likenesses, voices, or identity references without an
  explicit rights/consent note.
- Do not describe a persistent avatar with one generic prompt. Continuity needs
  reusable references, constraints, and retake checks.
- Do not let avatar generation own final editing. Remotion owns deterministic
  stitching, captions, overlays, and local render proof.

## Reference Map

- `qa_checklist.md` - read at start and finish for avatar-direction QA.
- `../ai-video-advisor/SKILL.md` - route provider/app selection and avatar clip
  generation after direction is ready.
- `../ai-image-advisor/SKILL.md` - route source portrait, character sheet, or
  reference-image creation.
- `../audio-advisor/SKILL.md` - route voice, dubbing, music, SFX, and mix plans.
- `../asset-advisor/SKILL.md` - route broader asset inventory and recreation
  planning.
- `../remotion/SKILL.md` - route final composition and local render proof.

## Output

- `avatar_direction_packet`: identity rules, performance map, asset inputs,
  provider brief, and acceptance checks.
- `generation_route`: next owner for reference images, avatar generation, audio,
  and Remotion composition.
- `blocked_report`: missing consent, missing script, inadequate identity refs,
  unsafe likeness use, unsupported provider need, or unresolved audio route.
