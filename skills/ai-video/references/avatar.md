---
title: Avatar Mode
owner: ai-video
status: active
kind: mode-reference
updated_at: 2026-10-12
---

# Avatar Mode

Load this when a video needs a persistent presenter, spokesperson, character,
talking head, lipsync, or voice/persona continuity across clips. The hard part
is continuity, consent, and performance direction, not the model call.

```text
ai_video.avatar(character_or_presenter, script_or_storyboard, identity_refs?,
                voice?, timing_master?, consent?, platform?)
  -> avatar_direction_packet + generated presenter clip | blocked_report
gates: likeness_consent_recorded; persistence_rules_named;
       performance_mapped_to_beats; voice_and_lipsync_route_named;
       timing_master_bound_before_final_lipsync
fails: unsafe_likeness_use; one_prompt_identity; missing_voice_or_script;
       treating_avatar_as_generic_clip
```

## 1. Bind identity and permission

- Name the presenter or character, identity references, brand constraints,
  script or storyboard, platform, and artifact owner.
- A real person's face or voice needs a recorded consent note: who consented,
  for what use, and where the note lives. No note means `blocked_report`,
  not a softer prompt. A photo supplied by the operator is not consent from
  the person in it.
- Voice clones follow the same rule; keep private voice IDs in runtime
  context, never in packets or tracked files.

## 2. Define persistence

Specify face or character continuity, wardrobe, framing, gesture style, voice,
accent, pacing, emotional range, and the reusable reference assets (character
sheet, turnaround, voice profile). Create or edit missing reference stills
through [ai-image](../../ai-image/SKILL.md). A persistent avatar described by
one generic prompt drifts; continuity needs references, constraints, and
retake checks.

When a selected creative element (character or audio) conditions the avatar,
bind its resolved golden example and golden recipe into the provider input.
Block title-only or recipe-only handoffs.

## 3. Direct the performance

Map script beats to expression, gaze, posture, gesture, pauses, lipsync needs,
and retake criteria. For voice-led or lipsync work, generate or receive the
voice first (see [audio](audio.md)), then consume the actual audio file, its
observed duration, alignment or timestamps, and the cue sheet before the final
avatar clip. Planned seconds alone do not unlock lipsync generation.

## 4. Generate and inspect

Pick the avatar or lipsync listing through treg per [providers](providers.md);
`belt` avatar apps are the fallback. Inspect frames for identity drift, mouth
sync against the audio, hands, and wardrobe changes before acceptance.

## 5. UGC hook batch with a persistent AI actor

Adapted from treg's `make-ugc` workflow and Monid's AI-actor and Jev remake
recipes. Use when the operator wants short ad or organic hooks from one
recurring fictional presenter (not a real person's likeness).

1. Build the actor once: a portrait sheet from 3-5 image models through
   `ai-image`, pick one, keep it as the identity reference.
2. Take hook mechanisms from the storyboard's outlier research, not wording.
3. Brainstorm about 10 hooks, keep 4.
4. Render each talking-head hook with Seedance 2.5 (image + audio reference +
   script, 9:16 720p, about 6-8 s); keep the same actor reference every time.
5. Cut a short product or demo segment (screen recording plus a voice clone
   through `audio` mode); stitch and caption in HyperFrames.

Published receipts: about $0.67 a clip on treg's page; our own pilots on
2026-10-12 cost about $0.71 (6 s 480p) and $1.60 (720p) a clip. Re-quote with
`catalog_get` first: the per-call listing price has drifted from the pages.

## Packet template

```text
## Avatar Direction
- Identity:
- Consent / usage note (who, what use, where recorded):
- Continuity rules:
- Voice (profile handle, never a private ID):
- Performance:
- Platform constraints:

## Beat Map
| Beat | Script | Expression | Gesture / Framing | Lipsync / Audio | Acceptance Check |
| --- | --- | --- | --- | --- | --- |

## Routes
- Reference stills: ai-image
- Voice: ai-video audio mode
- Avatar clip: provider listing + price quote
- Composition, captions, overlays: HyperFrames (/hyperframes)

## Done / Proof
- ready_when:
- evidence (inspected frames, sync check):
- residual_risk:
```

Avatar generation does not own final editing: stitching, captions, overlays,
and render proof belong to HyperFrames.
