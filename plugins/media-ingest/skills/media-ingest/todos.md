# Todos

- [ ] Classify source type, platform, visibility, and whether authenticated
  access or a local export is required.
- [ ] Run `summarize --extract-only` for URL or local-file text/transcript
  extraction, unless the user already provided the needed transcript/content.
- [ ] If `summarize` returns only thin page text and the source contains media,
  fetch or locate the media through the least invasive available route.
- [ ] Record every extraction, transcription, and frame command in the ingest
  bundle.
- [ ] For audio/video, extract transcript evidence through `summarize`,
  platform transcript support, or local Whisper.
- [ ] If transcription fails or is unavailable, record `transcript_status` as
  failed, partial, or visual-only; do not infer spoken content as fact.
- [ ] For video, extract representative frames and a contact sheet.
- [ ] Select only the minimum frames needed to prove source, workflow, prompts,
  timeline, final state, and acceptance criteria.
- [ ] Keep raw media, cookies, API keys, secrets, and bulky raw transcripts out
  of tracked files unless explicitly approved.
- [ ] Write a compact manifest with source identity, command provenance,
  transcript status, selected frames, retention note, and downstream skill
  recommendation.
- [ ] For video sources that need interpretation, hand the bundle to the video
  understanding workflow.
