---
name: media-ingest
version: 0.1.0
description: Use when a workflow needs to turn a URL, social post, audio file, video file, or local media path into a compact evidence bundle with source metadata, extraction commands, transcript status, representative frames, retention notes, and downstream handoff paths.
tier: 2
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# Media Ingest

Turn media inputs into a small, auditable evidence bundle before another skill
tries to understand or rebuild what the media shows.

This is a support workflow, not a scraping product. It should prefer compact
metadata, transcript summaries, selected frames, and command provenance over raw
media retention.

## Trigger Conditions

Use this skill when:

- a source URL may contain video or audio
- a user provides a local MP4, MOV, MP3, WAV, screen recording, or social link
- `harness-scout`, `video-understanding`, `video-production`, or
  `frontend-craft` needs transcript-plus-frame evidence before making claims
- `summarize` alone returns only a page label or thin extraction

Do not use this skill for text-only articles, repos, PDFs, or transcripts that
already include the needed evidence.

## Workflow

1. **Classify the source:** record URL or local path, source type, platform,
   visibility, privacy risk, and whether authenticated access is required.
2. **Run summarize first:** for URL and local-file inputs, run
   `summarize <source> --extract-only` or document why `summarize` is not
   available or insufficient.
3. **Fetch media only when needed:** if text extraction is too thin and the
   source is public or locally provided, use the least invasive available
   fetcher. Record the exact command and destination outside tracked docs.
4. **Extract transcript evidence:** use `summarize`, platform transcript
   support, or local Whisper. If transcription is missing or low quality,
   record that as a confidence limit rather than inventing content.
5. **Extract frame evidence for video:** produce a contact sheet and select the
   smallest set of frames that proves the workflow, UI states, prompts,
   timeline, final artifact, and visible acceptance criteria.
6. **Apply retention guard:** keep raw MP4/audio, cookies, API keys, and full
   raw transcripts out of tracked files unless the operator explicitly approved
   storage. Prefer compact summaries and selected frames.
7. **Write the bundle manifest:** leave downstream skills a manifest with
   source identity, commands, transcript status, selected frames, retention
   note, and known gaps.

## Output Contract

A completed ingest pass leaves a `MediaIngestBundle`-style artifact in the
owning run folder:

- `source`: canonical URL or local path plus creator/title/date when visible
- `visibility`: public, private, customer/internal, or unknown
- `commands`: exact extraction/transcription/frame commands that were run
- `transcript_status`: available, partial, failed, visual-only, or provided
- `transcript_summary_path`: compact summary path when available
- `contact_sheet_path`: contact sheet path for video
- `selected_frames`: frame paths with short labels
- `retention_note`: what was stored, what was intentionally omitted, and why
- `downstream`: recommended next skill, usually
  [video-understanding](../video-understanding/SKILL.md) for video

## Core Decision Branches

- **Text extraction is enough:** do not download media; hand the compact extract
  to the caller.
- **Public video/audio needs more evidence:** fetch media to temporary or
  experiment-local storage, then extract transcript and frames.
- **Authenticated/private source:** ask for a local export or approved
  authenticated path; do not invent credential handling.
- **Transcription fails:** continue with visual-only confidence labels only if
  frames are enough for the downstream task.
- **Raw media is required for proof:** keep it outside tracked docs and record a
  retention note.

## Judgement Questions

Use [advise](../advise/SKILL.md) when the answer is not mechanical:

- Is this source public enough to fetch, or should the user provide a local
  export?
- Is visual-only evidence enough for the downstream task?
- Should bulky media be retained temporarily, redacted, or discarded?

## Top Gotchas

1. Do not claim transcript coverage when only frames were inspected.
2. Do not commit raw videos, cookies, secrets, API keys, or full private
   transcripts.
3. Do not overfit to one platform; Instagram, YouTube, TikTok, direct URLs, and
   local files are fetch routes into the same bundle contract.

## References

- [summarize](../summarize/SKILL.md) for URL, local-file, and transcript
  extraction
- [video-understanding](../video-understanding/SKILL.md) for storyboard,
  visible workflow, and source-todo reconstruction after ingest
- `references/transcription.md` for local/API transcription setup notes
