---
profile_id: retro-low-poly-consequence
schema: farplane-video-audio-profile
version: "0.1.0"
source_capture_id: k975s09kwevmjdv266hby2gsnh8akkj4
---

# Retro Low-Poly Consequence Audio

## Audio Job

Build one continuous, creator-neutral audio spine for a 45–50 second causal
explainer. The voice owns pacing; music, SFX, silence, captions, and cuts serve
the physical mechanism being demonstrated. Seedance clips remain silent.

## Observed Source Evidence

- The decoded source master is 47.347 seconds, 44.1 kHz stereo.
- The local transcript contains 154 words, approximately 195 words per
  minute across the full reel.
- The master measures about `-14.1 LUFS` integrated, `1.8 LU` loudness range,
  and an ffmpeg true-peak readout of `-0.9 dBFS`; it is dense and consistently
  loud rather than highly dynamic.
- Stereo correlation is approximately `0.982`, with side energy roughly
  `20.4 dB` below mid energy. The mix therefore reads as narrow and
  center-forward.
- A mix-level autocorrelation estimate places the median estimated voiced F0
  around `143 Hz` across 369 qualified frames. Treat this as acoustic evidence
  about the source mix, not a target for cloning a specific person.
- Strong short-term energy rises appear around 0.7, 5.3, 9.2, 10.2, 13.6,
  15.2, 15.8, 19.3, 21.5, 22.2, 23.0, 24.7, 28.4, 29.3, and 46.1 seconds.
  They support frequent edit/mechanism accents, but signal analysis alone does
  not identify each sound's exact source.
- Phrase captions track the active narration rather than an independent lyric
  or dialogue layer.

Evidence comes from the locally decoded source master, transcript, loudness
analysis, stereo statistics, spectrogram, and the visual timeline. Raw audio
and source voice are not copied into this profile.

## Reusable Voice Profile

```text
role: original explainer narrator, never a source-voice clone
delivery: brisk, close, controlled, dry, and matter-of-fact
pace: 185–200 WPM
register: lower-mid adult register; compact pitch range; clear consonants
sentence_shape: short causal clauses with minimal pause between consequence and explanation
emotion_curve: amused premise -> clinical danger -> slightly incredulous workaround -> compressed catastrophic payoff
performance_rule: do not oversell jokes; let the literal visual carry the absurdity
ending: finish cleanly or cut an intentional final phrase at the largest visual reveal
avoid: creator imitation, announcer boom, podcast warmth, theatrical acting, breathy ASMR, singsong cadence
```

Use a rights-safe library or designed voice. A private voice handle belongs in
runtime configuration or invocation context, not this tracked profile.

## Music Profile

The available evidence does not isolate a confidently reusable source music
track or tempo. Do not manufacture a melody match. The safe reusable route is:

- no music, or a nearly subliminal synthetic tension bed;
- narrow tonal palette, little or no melody, and no emotional chord change;
- constant low-level pressure rather than a trailer build;
- duck the bed `8–12 dB` beneath narration and remove it entirely where a
  hard-silence mechanism is the point.

Music must never be the source of edit timing. Narration and visible mechanisms
own the cue sheet.

## SFX And Silence Grammar

Use one short, literal cue per important visible mechanism. Favor dry,
game-like, slightly synthetic sounds over cinematic impacts or realistic Foley.

| Timeline role | Reusable cue | Motion / edit binding | Acceptance check |
| --- | --- | --- | --- |
| 0–3s hook | one dry trigger click or snap, followed by two or three tiny failure accents | trigger lands on premise activation; accents land on the visceral reversals | cues remain shorter than the spoken nouns and do not mask the hook |
| body failure | short scrape, slip chirp, breath catch, or joint thud | begins exactly when contact fails; ends at the held awkward pose | the physical failure is identifiable without a generic whoosh |
| mechanism insert | thin ray tick, particle patter, filtered wave sweep, or contact buzz | cue follows the visible ray, particle, wave, or contact path | direction and duration match the on-screen mechanism |
| silence claim | sharply remove bed and ambience for a brief contrast window | cut occurs on the visual proof, not before the sentence | the absence is perceptible but the narration stays intelligible |
| failed workaround | repeat the earlier mechanism cue with a lower or heavier variation | recurrence proves the same rule defeats the workaround | cue family is recognizably related, not a new random effect |
| scale escalation | restrained digital rise or accelerating pulse, then one low dry stop | rise follows increasing scale/speed; stop lands on the largest frame | no trailer boom, braam, or oversized cinematic reverb |
| interrupted payoff | hard audio cut or sub-200 ms tail | cut binds to the incomplete final phrase and visual completion | ending feels intentional rather than missing media |

Before audio generation or assembly, instantiate every selected cue as:

```yaml
cue_id:
scene_id:
start_time_seconds:
end_time_seconds:
frame_range:
purpose:
motion_binding:
route: elevenlabs_sfx | approved_local_library | silence_automation
asset_path_or_blocker:
gain_db:
pan: -1.0..1.0
fade_in_ms:
fade_out_ms:
acceptance_check:
```

The storyboard must resolve the scene, time, and frame fields. The audio owner
must resolve route, asset or blocker, gain, pan, fades, and acceptance result.
Do not pass role-level placeholder rows directly to Remotion.

## Mix And Caption Handoff

- Keep one master narration file across the full reel; do not synthesize or
  normalize voice separately per shot.
- Aim the final social master near `-16` to `-14 LUFS` integrated and no higher
  than `-1 dBTP`; retain a narrow, center-forward presentation.
- Place narration at the center. Keep mechanism cues close to center unless
  visible directional motion justifies a small pan.
- Duck bed and ambience under every spoken clause; duck or mute them more
  aggressively around consonant-heavy captions and mechanism explanations.
- Generate captions from the final master voiceover, not the script draft.
  Show short active phrases and preserve lower-center safe-zone placement.
- Remotion owns final placement, ducking, caption timing, hard-silence windows,
  and loudness proof.

The executable Remotion handoff must contain:

```yaml
audio_handoff:
  master_voiceover_path_or_blocker:
  optional_music_bed_path_or_none:
  sfx_asset_paths_or_blockers: []
  cue_sheet_path:
  caption_word_timing_path_or_blocker:
  final_mix_output_path:
  loudness_proof_path:
  unresolved_blockers: []
```

`loudness_proof_path` must contain the observed integrated LUFS and true-peak
result for the final mix. The handoff is blocked while any required path is
missing or a cue row lacks timing, route, asset/blocker, gain, pan, fade, or an
acceptance check.

## Provider Routes

- Voice: `audio-generation:voice` through Fish or ElevenLabs after selecting a
  rights-safe library/designed voice.
- Music: `audio-generation:music` through ElevenLabs only if the minimal-bed
  route is selected.
- SFX: `audio-generation:sfx` through ElevenLabs, or approved local library
  assets, one cue at a time from the table above.
- Mix and captions: `remotion` using one cue sheet and one master VO.

## QA Assertions

- Voice remains original and non-imitative, between 185 and 200 WPM.
- Every SFX cue binds to named visible motion; no generic transition pack is
  spread across the reel.
- Music is absent or subordinate and has no unsupported “matching” claim.
- At least one contrast window uses reduced bed/ambience when silence or
  stopped propagation is the mechanism.
- Per-clip Seedance audio remains disabled.
- Final master is approximately `-16` to `-14 LUFS`, at or below `-1 dBTP`,
  with intelligible narration and caption timing derived from the final VO.
