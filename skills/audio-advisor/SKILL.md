---
name: audio-advisor
description: "Turn voiceover, music, SFX, Foley, dubbing, or mix needs into an audio direction packet and production route."
tier: 3
group: content-audio
source: local
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["storyboard", "asset-advisor", "avatar-advisor", "ai-video-advisor", "remotion"]
allowed-tools: Read, Grep, Glob, Bash
---

# Audio Advisor

## Context

Use this skill when a content artifact needs voiceover, music, sound effects,
Foley, dubbing, lipsync audio, sound design, mix notes, or timing cues. It is
the audio counterpart to asset planning: the output is a production-ready audio
direction packet, not necessarily generated audio.

This skill owns voice/music/SFX direction, timing, source/generation routes,
mix notes, rights notes, and Remotion handoff cues. It does not render video,
publish audio, or run external generation unless explicitly requested.

## Skill Signature

```text
audio_advisor(script_or_storyboard, inspiration_pack?, voice?, music?, sfx?, platform?, duration?, artifact_owner?)
  -> audio_direction_packet + production_routes | blocked_report

state:
  reads(user brief, script/storyboard, Inspiration Pack captures/elements,
        source audio refs, qa_checklist.md)
  writes(audio direction artifact when durable handoff is requested)

gates:
  audio_roles_named; rights_or_usage_risk_noted; timing_cues_aligned;
  voice_music_sfx_mix_separated; motion_bindings_named; remotion_handoff_ready

routes:
  storyboard | asset-advisor | avatar-advisor | ai-video-advisor |
  audio-generation | remotion | media-ingest | review

fails:
  vibes_only_audio; copyrighted_track_without_plan; voice_without_consent_note;
  sfx_without_timing; mix_notes_missing_for_final_stitch;
  audio_bed_without_motion_bindings
```

## Phase Boundary

Use `avatar-advisor` when voice or lipsync belongs to a persistent presenter or
identity. Use `ai-video-advisor` only for provider/app details when model-native
video tools also create or transform audio. Use `audio-generation` after the
brief, rights, consent, timing, and mix direction are approved and a caller
needs a Fish or ElevenLabs generation packet or artifact. Use `remotion` for
deterministic audio placement, captions, ducking, waveform visuals, and local
render proof.

For Inspiration Pack inputs, consume `audio`, `editing`, `storyboard`, and
`hook` elements from `captures[].elements`. A generic bed is not enough for an
inspiration-led video: output time-coded cues and name the required motion/edit
binding for each important hit, transition, riser, silence, or voice/caption
beat. Return a `blocked_report` when the capture has no usable audio/editing
element and the storyboard depends on sound design that cannot be specified
honestly.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the audio job.
  - [ ] Identify script/storyboard, Inspiration Pack audio/editing elements,
    platform, duration, voice needs, music needs, SFX/Foley needs, rights
    constraints, and artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Split audio roles.
  - [ ] Separate voiceover, dialogue, lipsync, music bed, transition hits,
    Foley, ambient sound, UI sounds, silence, and mix/ducking needs.
- [ ] 3. Map timing and intent.
  - [ ] Align each audio cue to scene, beat, timestamp/frame range, emotional
    job, required motion/edit binding, and acceptance check.
  - [ ] For multi-clip narrative reels, design one master audio spine: VO or
    dialogue continuity, music bed, SFX/Foley accents, silence, ducking, and
    transitions across the full timeline.
- [ ] 4. Choose routes.
  - [ ] Route persistent presenter or lipsync identity work to
    `avatar-advisor`.
  - [ ] Route model-native audio/video generation details to
    `ai-video-advisor` when a provider owns the audio behavior.
  - [ ] When a master audio spine owns the piece, instruct model-native video
    generation to disable per-clip generated audio unless the plan explicitly
    needs diegetic source sound for a named beat.
  - [ ] Route asset inventory gaps to `asset-advisor`.
  - [ ] Route approved standalone voice, music, or SFX briefs to
    `audio-generation`; this advisor does not select runtime secrets, spend, or
    execute the provider call itself.
  - [ ] Route final placement, ducking, captions, waveform visuals, and local
    render proof to `remotion`.
- [ ] 5. Output the audio direction packet.
  - [ ] Include cue sheet, voice/music/SFX briefs, rights notes, source files or
    missing blockers, mix notes, and next production owner.
  - [ ] Apply `qa_checklist.md` again before calling the packet ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output Template

```text
## Audio Direction
- Voice:
- Music:
- SFX / Foley:
- Rights / usage:
- Mix notes:

## Cue Sheet
| Time / Frames | Scene | Audio Cue | Motion / Edit Binding | Purpose | Source / Route | Acceptance Check |
| --- | --- | --- | --- | --- | --- | --- |

## Routes
- Voice / lipsync:
- Music:
- SFX / Foley:
- Remotion:

## Done / Proof
- ready_when:
- evidence / source note:
- residual_risk:
```

## Gotchas

- Do not specify only "upbeat music" or "punchy SFX." Tie audio to beats,
  emotion, duration, motion/edit bindings, and proof checks.
- Do not assume copyrighted tracks, cloned voices, or real-person voices are
  usable without an explicit rights/consent plan.
- Do not let audio planning disappear inside video generation. Remotion needs
  timing cues and mix notes to stitch the final piece.
- Do not accept inconsistent per-clip generated audio for a coherent narrative
  reel. Use one master VO/music/SFX plan and let Remotion place the final mix.

## Reference Map

- `qa_checklist.md` - read at start and finish for audio-direction QA.
- `../storyboard/SKILL.md` - route narrative and scene planning before audio
  cue design when the script is not ready.
- `../asset-advisor/SKILL.md` - route source/missing asset inventory.
- `../avatar-advisor/SKILL.md` - route persistent voice, presenter, or lipsync
  direction.
- `../ai-video-advisor/SKILL.md` - route provider-specific model-native
  audio/video generation details.
- `../audio-generation/SKILL.md` - route approved standalone voice, music, or
  SFX briefs into provider-resolved packets or explicitly authorized artifacts.
- `../remotion/SKILL.md` - route deterministic placement, ducking, captions,
  waveforms, and local render proof.

## Output

- `audio_direction_packet`: cue sheet, voice/music/SFX briefs, rights notes,
  mix notes, and acceptance checks.
- `production_routes`: next owner for voice, music, SFX/Foley, avatar/lipsync,
  provider execution, and Remotion placement.
- `blocked_report`: missing script, unresolved rights/voice permission,
  missing timing, unavailable source audio, absent motion bindings, or unclear
  final composition route.
