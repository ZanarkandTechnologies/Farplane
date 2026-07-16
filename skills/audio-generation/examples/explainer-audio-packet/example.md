---
kind: skill-example
skill: audio-generation
status: positive-fixture
created_at: 2026-07-15
---

# Explainer Audio Generation Packet Example

This fixture demonstrates packet-only planning. It does not authorize or claim
provider execution.

```yaml
audio_generation_packets:
  - kind: voice
    provider: fish
    capability: text-to-speech
    execution_mode: dry_run
    brief_ref: audio-direction.md#voice
    prompt_or_script: "Why does a tiny delay become a giant queue?"
    profile_ref: rights-safe narrator selected at invocation
    parameters:
      model: s2-pro
      format: mp3
      sample_rate: 44100
      latency: normal
    timing:
      duration_seconds: 4.2
      cue_ref: scene-01/frames-0-126
    output:
      owner: public/audio/queue-explainer
      path: public/audio/queue-explainer/scene-01-voice.mp3
      format: mp3
    rights_and_consent:
      status: cleared
      basis: library voice approved for project use
    acceptance_checks:
      - question lands clearly before the diagram reveal
      - observed duration is within 0.25 seconds of the cue target
    secret_source: runtime_environment_only

  - kind: music
    provider: elevenlabs
    capability: music
    execution_mode: dry_run
    brief_ref: audio-direction.md#music
    prompt_or_script: "Restrained 84 BPM instrumental pulse, no vocals; build gently after the reveal and end cleanly."
    profile_ref: null
    parameters:
      model: music_v2
      duration_seconds: 28
    timing:
      duration_seconds: 28
      cue_ref: master-bed
    output:
      owner: public/audio/queue-explainer
      path: public/audio/queue-explainer/master-bed.mp3
      format: mp3
    rights_and_consent:
      status: cleared
      basis: original generated instrumental for this production
    acceptance_checks:
      - bed leaves intelligibility headroom for narration
      - ending resolves without an audible loop seam
    secret_source: runtime_environment_only

  - kind: sfx
    provider: elevenlabs
    capability: sound-effects
    execution_mode: dry_run
    brief_ref: audio-direction.md#sfx
    prompt_or_script: "Soft wooden block clicks into place; close, dry, no reverb."
    profile_ref: null
    parameters:
      model: eleven_text_to_sound_v2
      duration_seconds: 0.8
      loop: false
    timing:
      duration_seconds: 0.8
      cue_ref: scene-03/diagram-lock
    output:
      owner: public/audio/queue-explainer
      path: public/audio/queue-explainer/diagram-lock.mp3
      format: mp3
    rights_and_consent:
      status: cleared
      basis: original generated effect for this production
    acceptance_checks:
      - transient aligns with the block snap
      - tail clears before the payoff line
    secret_source: runtime_environment_only
```
