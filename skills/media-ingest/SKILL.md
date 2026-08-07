---
name: media-ingest
description: "Turn URLs or local audio, video, or social media into metadata, transcript status, representative frames, retention notes, and handoff paths."
tier: 2
source: local
template_uses:
  skill-template: "0.3.7"
allowed-tools: Read, Glob, Grep, Bash
---

# Media Ingest

## Context

Use this skill when a URL or local file may contain audio or video evidence and
a downstream workflow needs more than page text. It turns media sources into a
small, auditable evidence bundle before `harness-scout`, `ingest-content`,
`video-understanding`, `content-impl-plan`, `storyboard`, or `impl-plan` makes claims
from the source.

This is a support workflow, not a scraping product. Prefer compact metadata,
transcript summaries, selected frames, contact sheets, command provenance, and
retention notes over raw media retention.

Do not use this skill for text-only articles, repos, PDFs, or transcripts that
already include the needed evidence.

## Skill Signature

```text
media_ingest(source, operator_note?, bundle_owner?)
  -> MediaIngestBundle + selected_evidence + downstream_route

state:
  reads(source URL or local media, optional operator note,
        summarize output, platform metadata, local media tools,
        references/transcription.md when transcription is needed,
        references/music-recognition.md when music is selected)
  writes(bundle manifest, transcript summary path?, contact sheet?,
         selected frames?, optional music recognition result?,
         command provenance, retention note)

gates:
  summarize_attempted_or_skipped_with_reason;
  media_fetch_only_when_text_is_thin_or_frames_audio_are_required;
  cookie_fetch_attempts_recorded_without_storing_cookie_jars;
  transcript_status_explicit;
  raw_media_kept_out_of_tracked_files_unless_approved

routes:
  summarize -> media-ingest -> video-understanding
  media-ingest -> ingest-content
  media-ingest -> audio-advisor

fails:
  claims transcript coverage from frames only;
  commits raw video, cookies, API keys, or full private transcripts;
  stops after one missing browser cookie store;
  invents spoken content, music matches, creator metadata, or permissions
```

## Phase Contract

```text
phase_contract(source, operator_note?, bundle_owner?)
  -> grounded_source_classification
   + direct_ingest_plan
   + extraction_or_fetch_commands
   + transcript_frame_music_evidence
   + retention_guard
   + bundle_manifest
   + downstream_handoff
```

## Phase Boundary

Run Tier 0 phases inline for ordinary ingests. Use `advise` only when the
source privacy, retention choice, or visual-only sufficiency is a real judgment
call. Hand video interpretation to `video-understanding`; do not make
storyboard or reimplementation claims inside media-ingest.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the source and evidence need.
  - [ ] Record URL or local path, source type, platform, visibility, privacy
    risk, downstream job, and whether authenticated access or local export may
    be required.
- [ ] 2. Run `summarize --extract-only` first, unless the caller already
  provided the needed transcript or content.
  - [ ] Treat thin page text as insufficient when the source clearly contains
    video/audio and the downstream task needs frames, audio, or timeline proof.
- [ ] 3. Fetch or locate media only when needed.
  - [ ] For blocked public social video, use local `yt-dlp` with
    `--cookies-from-browser <browser>` before degrading to metadata or
    thumbnail. Try the operator's active browser profile first, then installed
    profiles such as Brave, Chrome, Chromium, Edge, Firefox, Safari, Vivaldi,
    Opera, or Whale. Example:
    `yt-dlp --cookies-from-browser brave -o "$workdir/source.%(ext)s" "$url"`.
  - [ ] Record each attempted browser, absence, blocker, command, result, and
    destination; do not export or store cookie jars in tracked files.
- [ ] 4. Extract transcript evidence when audio or speech matters.
  - [ ] Use `summarize`, platform transcript support, or local Whisper. If
    transcription fails or is unavailable, set `transcript_status` to
    `failed`, `partial`, or `visual-only`.
- [ ] 5. Extract music evidence only when the operator selected the music,
  song, beat, or audio bed.
  - [ ] Read `references/music-recognition.md`, extract the smallest useful
    snippet, optionally run `scripts/recognize_music.py`, and record
    match/no-match/skipped/failed without blocking the ingest.
- [ ] 6. Extract visual evidence for video.
  - [ ] Produce a contact sheet and select only the frames needed to prove
    source, workflow, prompts, timeline, final state, and acceptance criteria.
- [ ] 7. Apply retention and privacy guardrails.
  - [ ] Keep raw media, cookies, API keys, secrets, and bulky raw transcripts
    out of tracked files unless the operator explicitly approved storage.
- [ ] 8. Write the `MediaIngestBundle` manifest and route the handoff.
  - [ ] Include source identity, commands, transcript status, selected frames,
    contact sheet, optional music recognition, retention note, known gaps, and
    downstream recommendation, usually `video-understanding` for video.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

`MediaIngestBundle`:

```yaml
source: canonical URL or local path plus creator/title/date when visible
visibility: public | private | customer/internal | unknown
commands:
  - exact extraction/transcription/frame command
transcript_status: available | partial | failed | visual-only | provided
transcript_summary_path: optional compact summary path
music_recognition: optional match | no-match | skipped | failed
contact_sheet_path: optional contact sheet path
selected_frames:
  - path: /path/to/frame.jpg
    label: short evidence label
retention_note: stored and intentionally omitted material
known_gaps:
  - missing transcript, blocked profile, or unverified source detail
downstream: video-understanding | ingest-content | audio-advisor | other
```

Positive command pattern:

```bash
summarize "$url" --extract-only
yt-dlp --cookies-from-browser brave -o "$workdir/source.%(ext)s" "$url"
ffmpeg -i "$workdir/source.mp4" -vf "fps=1/2,scale=270:-1,tile=4x2" "$workdir/contact_sheet.jpg"
```

## Gotchas

- Do not claim transcript coverage when only frames were inspected.
- Do not treat one missing browser cookie store as proof that browser-cookie
  fetch is unavailable.
- Do not claim a music match unless the recognition tool returned one; store
  no-match, missing dependency, or network failure as a limit.
- Do not overfit to one platform; Instagram, YouTube, TikTok, direct URLs, and
  local files are fetch routes into the same bundle contract.

## Reference Map

- [summarize](../summarize/SKILL.md) - run first for URL, local-file, and
  transcript extraction.
- [video-understanding](../video-understanding/SKILL.md) - use after ingest
  when video content needs storyboard, workflow, or source-todo reconstruction.
- [transcription notes](references/transcription.md) - read when speech or
  narration needs local/API transcription beyond `summarize`.
- [music recognition notes](references/music-recognition.md) - read only when
  the operator selected the music, song, beat, or audio bed.

## Output

- A compact `MediaIngestBundle` in the owning run folder.
- Selected evidence paths for transcript, contact sheet, frames, and optional
  music recognition.
- A clear retention note and downstream skill recommendation.
