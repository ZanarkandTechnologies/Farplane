# Media Evidence Route

Load this when text is not enough: the claim depends on frames, audio, image
detail, timing, or music, or the Resource Bank branch needs a same-source
example asset. Ordinary transcript-grounded analysis never loads it.

```text
media_evidence(source, need, workdir)
  -> MediaBundle + selected evidence paths | blocked_missing_source
```

## Rules

- **Summarize first.** `python3 skills/intelligest/scripts/extract_source.py
  "$source"` runs `summarize --extract`, treats a login wall or near-empty page
  as a failed extraction (not a source verdict), downloads with `yt-dlp`
  (browser cookies when refused), then transcribes the file with
  `summarize --extract --timestamps`. It prints the route on stderr; only its
  `blocked:` exit blocks the claim. Run it before agent-reach, Apify, a
  browser, or a blocked verdict.
- **Never store cookie jars.** Use `yt-dlp --cookies-from-browser <browser>`;
  try the operator's active browser, then other installed profiles (Brave,
  Chrome, Chromium, Edge, Firefox, Safari, Vivaldi, Opera, Whale). One missing
  cookie store is not proof the route is unavailable. Record each attempt,
  never export cookies to a file.
- **State transcript status explicitly:** `available | partial | failed |
  visual-only | provided`. Frames alone never claim transcript coverage. A
  missing summarize transcriber (Groq, ONNX, whisper.cpp model, provider key)
  is a setup blocker to name, not a source blocker.
- **Keep evidence classes apart.** Transcript facts, frame observations,
  creator claims, and inference stay separate, each anchored to a timestamp or
  frame with a confidence. A non-tutorial video yields observations, not a
  method.
- Raw media, cookies, keys, and bulky transcripts stay out of tracked files
  unless the operator approved storage; keep them in the run's workdir.

## Steps

1. Classify source, platform, visibility, privacy risk, and the exact claim
   that needs media.
2. Fetch media only when needed (`-o "$workdir/source.%(ext)s"`).
3. Transcribe with `farplane run -- summarize "$workdir/source.mp4" --extract
   --timestamps`, then platform transcripts or local Whisper; see
   [transcription](transcription.md).
4. Frames: a contact sheet, then only the frames that prove the claim:
   `ffmpeg -i "$workdir/source.mp4" -vf "fps=1/2,scale=270:-1,tile=4x2"
   "$workdir/contact_sheet.jpg"`.
5. Music only when the operator selected the song, beat, or audio bed:
   [music recognition](music-recognition.md) with
   `scripts/recognize_music.py`; record match, no-match, skipped, or failed
   without blocking.
6. Write the bundle. Missing fetchable media returns
   `blocked_missing_source` with the exact source, frame, or timestamp.

```yaml
source: canonical URL or local path, creator/title/date when visible
visibility: public | private | customer/internal | unknown
commands: [exact extraction, transcription, and frame commands]
transcript_status: available | partial | failed | visual-only | provided
transcript_summary_path: optional
music_recognition: match | no-match | skipped | failed  # optional
contact_sheet_path: optional
selected_frames: [{path, label}]
retention_note: what was stored and what was left out
known_gaps: [missing transcript, blocked profile, unverified detail]
```
