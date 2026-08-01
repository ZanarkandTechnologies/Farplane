---
name: audio-advisor
description: "Plan audio, discover SFX candidates, generate approved assets, verify files, and hand off voice, music, Foley, dubbing, and mixes."
tier: 3
group: content-audio
source: local
template_uses:
  skill-template: "0.3.8"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["storyboard", "asset-advisor", "avatar-advisor", "ai-video-advisor", "remotion"]
methods:
  - audio-advisor:plan
  - audio-advisor:source-sfx
  - audio-advisor:voice
  - audio-advisor:music
  - audio-advisor:sfx
allowed-tools: Read, Grep, Glob, Bash, web_search
---

# Audio Advisor

## Context

Use this skill when a content artifact needs voiceover, music, sound effects,
Foley, dubbing, lipsync audio, sound design, mix notes, timing cues, SFX
candidate discovery, or provider-generated audio. Methods are `audio-advisor:plan`,
`audio-advisor:source-sfx`, `audio-advisor:voice`, `audio-advisor:music`, and
`audio-advisor:sfx`.

This skill owns audio direction, cue timing, SFX candidate discovery, rights and
consent gates, provider packets/generation, verification, receipts, mix notes,
and Remotion handoff. It never downloads SoundButtonsWorld files.

## Skill Signature

```text
audio_advisor(script_or_storyboard, element_realization_packets?, timing_master_role?, kind?, brief?, voice?, music?, sfx?, platform?, duration?, source?, provider?, execution_mode?, artifact_owner?)
  -> audio_direction_packet | sfx_candidate_shortlist | generation_packet |
     execution_receipt | blocked_report

state:
  reads(user brief, script/storyboard, complete audio/editing element packets,
        source refs, config.toml when sourcing or generating,
        provider/source reference selected by route, qa_checklist.md,
        runtime secret readiness when authorized generation is requested)
  writes(audio direction artifact, SFX candidate shortlist?, optional generated
         audio, generation receipt, actual duration/alignment/cue binding)

gates:
  audio_roles_named; selected_elements_conditioned_on_example_and_recipe;
  timing_cues_aligned; motion_bindings_named;
  rights_or_usage_basis_recorded; voice_consent_resolved_when_relevant;
  candidate_search_completed_when_sfx_idea; provider_capability_matches;
  output_owner_resolved;
  explicit_external_execution_authority; receipt_contains_no_secret;
  remotion_handoff_ready

routes:
  storyboard | asset-advisor | avatar-advisor | ai-video-advisor |
  media-ingest | remotion | review

fails:
  vibes_only_audio; copyrighted_track_without_plan; voice_without_consent;
  sfx_without_timing; candidate_shortlist_missing_for_interesting_sfx;
  soundbuttonsworld_download_or_automated_site_query; implicit_spend_or_upload;
  unsupported_provider_kind_pair; receipt_leaks_credential_or_private_voice_id;
  mix_notes_missing_for_final_stitch; audio_bed_without_motion_bindings
```

Config precedence is `invocation > config.toml > explicit fallback in this
file`. A supplied Brand Kit prompt remains prose production direction in the
brief; interpret it directly rather than requiring structured advisor fields.
Credentials resolve separately from the runtime environment, normally
through `farplane run -- <command>` or `doppler run -- <command>`; never write
credential values into packets, artifacts, receipts, or tracked files.

## Phase Boundary

Use `avatar-advisor` when voice or lipsync belongs to a persistent presenter or
identity. Use `ai-video-advisor` when a model-native video provider owns the
audio behavior. Use `remotion` for deterministic placement, captions, ducking,
waveforms, final mix, and render proof.

Planning and candidate discovery are read-only. For every video plan with an
interesting or commonly available SFX idea, search public indexed
SoundButtonsWorld item pages before proposing generation and put candidates in
the final content implementation plan for operator approval/retrieval. Never
download from the site. Paid generation still requires explicit authority.

For Brand Kit or Tasty Pack inputs, consume complete `audio`, `editing`,
`storyboard`, and `hook` realization packets. Important hits, transitions,
risers, silence, and voice/caption beats require time-coded motion/edit
bindings rather than a generic bed.

When a selected element conditions audio work, require its resolved golden
example and golden recipe together. If audio is the selected timing master,
the execution receipt must include the actual asset, observed duration,
alignment/timestamps when available, and downstream cue sheet; planned seconds
alone do not unlock visual generation.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the audio job and read `qa_checklist.md` as preflight.
  - [ ] Resolve the script/storyboard, selected elements, platform,
    duration, audio roles, rights constraints, artifact owner, desired mode,
    and whether provider execution is explicitly authorized.
  - [ ] Validate complete realization packets for selected audio/story/editing
    elements and bind each golden example plus golden recipe to its cue or
    generation direction.
- [ ] 2. Split roles and map one audio spine.
  - [ ] Separate voice/dialogue/lipsync, music, SFX/Foley, ambience, UI sounds,
    silence, transitions, and mix/ducking; bind every cue to time/frames, scene,
    intent, motion/edit event, gain/pan/fade needs, and acceptance check.
  - [ ] For multi-clip narrative reels, use one master audio spine and disable
    per-clip generated audio unless a named beat needs diegetic source sound.
  - [ ] For a voice-led documentary/editorial reel, load the
    [documentary reel production contract](../remotion/references/documentary-reel.md).
    Measure the locked narration first, bind each causal clause to a half-open
    frame range, and place music, sparse synchronized SFX, ambience, silence,
    ducking, captions, and named motion/edit events on that same spine.
- [ ] 3. Choose `reuse existing -> discover candidate -> operator decision -> generate` per cue.
  - [ ] Prefer an approved local asset for a common, literal SFX; generate only
    after candidate discovery finds no fit or the operator rejects the options.
  - [ ] For SoundButtonsWorld, read
    [candidate discovery route](references/soundbuttonsworld.md) before search.
    Search the public web index for item pages; never automate the site search,
    open download controls, crawl, or represent availability as permission.
- [ ] 4. Build the direction packet and candidate shortlist.
  - [ ] Include cue sheet, briefs, provider/fallback, rights/consent, execution
    mode, output path, mix notes, acceptance checks, blockers, and next owner.
  - [ ] For each interesting SFX idea, add up to three candidates with cue,
    search phrase, title, item-page URL, why it fits, rights risk, and
    `awaiting_operator_download_and_approval`; record `searched_no_fit` when empty.
- [ ] 5. Resolve provider detail only for cues selected for generation.
  - [ ] Read `config.toml`; Fish supports voice, while ElevenLabs supports
    voice, music, and SFX. Load `references/fish-audio.md` only for Fish voice
    or `references/elevenlabs.md` only for an ElevenLabs route; block every
    unsupported pair rather than silently switching.
  - [ ] Build the validated packet with provider/model/format, prompt or script,
    rights-safe profile handle, duration/cue, output owner/path, execution mode,
    acceptance checks, and `secret_source: runtime_environment_only`.
- [ ] 6. Stop at candidates or dry run unless generation is authorized.
  - [ ] Return SoundButtonsWorld page refs only, never files. Without explicit
    provider upload/spend/generation authority, return `dry_run` and make no call.
  - [ ] For authorized generation, confirm the required environment variable is
    present without printing it; otherwise return the exact blocker.
- [ ] 7. Execute, verify, and hand off when authorized.
  - [ ] Run Fish/ElevenLabs through the managed environment using package
    scripts; never store raw headers, credentials, or private voice IDs.
  - [ ] Validate provider JSON with `scripts/validate_audio_packet.py`; confirm
    every audio file opens and probe duration/format; record a sanitized receipt
    and route final placement/mix/render proof to `remotion`.
  - [ ] When this asset is timing master, attach observed duration,
    alignment/timestamps, and the revised cue sheet before final visual work.
  - [ ] Reapply `qa_checklist.md` and use independent review for material
    production runs.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
Audio Direction:
- Voice / music / SFX-Foley / silence / mix:

Cue Sheet:
| Time / Frames | Scene | Cue | Motion / Edit Binding | Purpose | Source / Provider | Rights Basis | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |

SFX Candidate Shortlist:
- cue / search phrase / item title / page URL / fit / rights risk:
- status: awaiting_operator_download_and_approval | searched_no_fit

Generation:
- mode: reuse_existing | candidate_discovery | generate | blocked
- execution_mode: dry_run | authorized_execution
- output_owner / paths / provider_receipts:

Done / Proof:
- ready_when:
- evidence:
- residual_risk:
```

Provider generation packets and blockers retain the schema validated by
`scripts/validate_audio_packet.py`. Load
`examples/explainer-audio-packet/example.md` only when shaping or reviewing a
combined voice, music, and SFX packet.

## Gotchas

- Keep private or rights-sensitive voice IDs in invocation/runtime context.
- Do not generate a common effect before the candidate search and operator decision.
- Do not accept inconsistent per-clip audio for a coherent narrative reel.

## Reference Map

- `qa_checklist.md` - read at start and finish for direction, sourcing,
  generation, and handoff QA.
- `config.toml` - read before source/provider/default selection.
- [SoundButtonsWorld discovery](references/soundbuttonsworld.md) - load before
  candidate search; returns links only.
- [Fish Audio route](references/fish-audio.md) - load only for Fish voice.
- [ElevenLabs routes](references/elevenlabs.md) - load only for ElevenLabs
  voice, music, or SFX.
- [Audio packet example](examples/explainer-audio-packet/example.md) - load only
  for combined packet shaping or review.
- [Documentary reel contract](../remotion/references/documentary-reel.md) -
  load for voice-led documentary/editorial reel timing and cue binding.
- `scripts/validate_audio_packet.py` - validate provider packets and blockers.
- `scripts/execute_fish_audio.py` - authorized Fish voice execution.
- `scripts/execute_elevenlabs.py` - authorized ElevenLabs voice, music, or SFX
  execution; dry-run before the first paid call.
- [Avatar Advisor](../avatar-advisor/SKILL.md) - persistent voice or lipsync.
- [Remotion](../remotion/SKILL.md) - placement, captions, ducking, mix, and
  render proof.
