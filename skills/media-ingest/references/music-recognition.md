# Music Recognition

Use this optional path only when the operator note selects the music, song,
beat, soundtrack, or audio bed as a liked element. Normal media ingestion should
not identify every background track by default.

## Recommended Route

Prefer the local helper:

```bash
python3 skills/media-ingest/scripts/recognize_music.py /path/to/snippet.wav --json
```

The helper uses `shazamio` when installed. It performs Shazam-style recognition
against Shazam's service and returns compact JSON with:

- `status`: `matched`, `no_match`, `missing_dependency`, `error`
- `title`
- `artist`
- `album`
- `shazam_url`
- `confidence`
- `raw_track`

Install the optional dependency only when this workflow is needed. On this
machine, prefer the dedicated Codex venv so Homebrew Python 3.14 does not load
ShazamIO's native extension directly:

```bash
python3.12 -m venv ~/.codex/.venvs/shazamio
~/.codex/.venvs/shazamio/bin/python -m pip install shazamio
```

The helper re-execs into `~/.codex/.venvs/shazamio/bin/python` when it exists.

## Snippet Extraction

For video or long audio, extract the smallest useful snippet instead of saving
raw media:

```bash
ffmpeg -y -ss 00:00:00 -t 15 -i input.mp4 -vn -ac 1 -ar 44100 /tmp/farplane-music-snippet.wav
```

If the note names a segment, use that segment. Otherwise start near the audible
music hook, usually the first 0-20 seconds.

## Ingest Mapping

When recognition matches, pass the result back to `ingest-content` as an
`audio` creative element:

```text
kind: audio
title: "Music reference: <artist> - <title>"
description: "Recognized track used as the audio bed; future remixes should use
  the sonic role/energy rather than copying the source track."
anchor: "music recognition"
pinned: true only when the operator note selected the music/song/audio bed
```

Also add a `constraint` element when future creation is likely:

```text
Use the recognized track for attribution/research only. Do not reuse protected
music directly unless licensed; recreate the tempo, energy, instrument palette,
or edit function with cleared/generative/original audio.
```

If recognition fails, still store a useful `audio` element when the sound can be
described honestly, anchored to `operator note` or `audio heard`, and record the
recognition limit in the analysis.

## Alternatives

- SongRec is a mature open-source Shazam client with GUI and CLI support, but
  it is Linux-first and less convenient for this macOS repo workflow.
- RapidAPI-backed `shazam-cli` scripts exist, but they require an API key and
  add spend/account setup, so they are not the default.

## Guardrails

- Do not make track recognition a storage gate.
- Do not run recognition unless the note or downstream task asks for music
  detail.
- Do not commit raw audio snippets; keep them in `/tmp`, `.farplane/`, or a
  ticket artifact only when proof requires it.
- Do not confuse speech transcription with music recognition. Transcription
  answers "what was said"; recognition answers "what track is this?"
