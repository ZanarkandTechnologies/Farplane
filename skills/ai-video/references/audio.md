---
title: Audio Mode
owner: ai-video
status: active
kind: mode-reference
updated_at: 2026-10-12
---

# Audio Mode

Load this when a piece needs voiceover, music, sound effects, Foley, dubbing,
lipsync audio, or cue timing. Audio mode owns cue direction, SFX candidate
discovery, rights and consent gates, provider packets, generation,
verification, and receipts. Placement, ducking, captions, and the final mix
belong to HyperFrames (`/hyperframes`).

```text
ai_video.audio(script_or_storyboard, kind?, brief?, voice?, duration?,
               timing_master_role?, provider?, execution_mode?)
  -> audio_direction_packet | sfx_candidate_shortlist | generation_packet
     | execution_receipt | blocked_report
defaults: voice=fish, music=elevenlabs, sfx=soundbuttonsworld candidates
          then elevenlabs, execution_mode=dry_run
```

## 1. Split roles and keep one spine

Separate voice/dialogue, music, SFX/Foley, ambience, UI sounds, silence,
transitions, and ducking. Bind every cue to a time or frame range, scene,
intent, motion or edit event, gain/fade need, and acceptance check.

For a multi-clip narrative reel, one master audio spine owns the piece: set
`generate_audio: false` on every video clip unless a named beat needs
diegetic source sound, and record that exception per beat. For voice-led
documentary or editorial reels, measure the locked narration first and bind
cues to it per the
[documentary reel contract](../../storyboard/references/documentary-reel.md).

## 2. Per cue: reuse, discover, decide, generate

1. Reuse an approved local asset when one fits.
2. For a common or literal SFX (shutter, click, whoosh, door), search
   SoundButtonsWorld item pages through the public web index first, per
   [SoundButtonsWorld discovery](soundbuttonsworld.md). Return up to three
   item-page links per cue with fit and rights risk, status
   `awaiting_operator_download_and_approval`, or `searched_no_fit`.
   Never download from the site, automate its search, or treat availability
   as a license; the operator retrieves and approves files.
3. Generate only after discovery finds no fit or the operator rejects the
   candidates.

Meme, movie, TV, game, song, brand, celebrity, and recognizable-voice clips are
high risk; offer an original generated fallback instead.

## 3. Providers

| Kind | Default | Reference | Script |
| --- | --- | --- | --- |
| Voice | Fish Audio (`s2.1-pro-free`) | [Fish Audio](fish-audio.md) | `scripts/execute_fish_audio.py` |
| Music | ElevenLabs (`music_v2`) | [ElevenLabs](elevenlabs.md) | `scripts/execute_elevenlabs.py` |
| SFX | ElevenLabs (`eleven_text_to_sound_v2`) after discovery | [ElevenLabs](elevenlabs.md) | `scripts/execute_elevenlabs.py` |

Fish is voice only. Block an unsupported kind/provider pair rather than
silently switching providers. treg voice listings are a fallback only when
both direct routes are blocked ([providers](providers.md)).

## 4. Packet, dry run, then execution

Each packet carries provider, model, format, prompt or script, rights-safe
profile handle, duration and cue, output owner and path, rights/consent basis,
acceptance checks, and `secret_source: runtime_environment_only`. See the
[explainer packet example](../examples/explainer-audio-packet/example.md).

- Without explicit generation or spend authority, return `dry_run` and make no
  call. The operator's standing spend cap counts as authority for in-cap
  generation; quote the price first and log it.
- For authorized runs, confirm the env var (`FISH_API_KEY`,
  `ELEVENLABS_API_KEY`) is present without printing it, and run through the
  managed environment: `farplane run -- python3 scripts/execute_fish_audio.py <packet>`
  or `doppler run -- ...`. Dry-run ElevenLabs before its first paid call.
- Never write credentials, raw headers, or private voice IDs into packets,
  receipts, or tracked files. Do not inspect arbitrary credentials to make a
  route work.

## 5. Verify and hand off

- Validate packets and receipts: `python3 scripts/validate_audio_packet.py <packet.json>`.
- Open every output file and probe duration and format (`ffprobe`); listen to
  the start, the end, and every cue point before acceptance.
- When this audio is the timing master, attach observed duration, alignment or
  timestamps, and the revised cue sheet before final visual or lipsync work.
- Hand placement, ducking, and the final mix to HyperFrames.

## Templates

```text
Cue Sheet:
| Time / Frames | Scene | Cue | Motion / Edit Binding | Purpose | Source / Provider | Rights Basis | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |

SFX Candidate Shortlist:
- cue / search phrase / item title / page URL / fit / rights risk:
- status: awaiting_operator_download_and_approval | searched_no_fit

Generation:
- mode: reuse_existing | candidate_discovery | generate | blocked
- execution_mode: dry_run | authorized_execution
- output paths / sanitized receipts / observed duration:
```
