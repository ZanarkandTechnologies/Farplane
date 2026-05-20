# Media Ingest Bundle

## Source

- `source_id`: `SRC-0008`
- `canonical_url`: `https://www.instagram.com/p/DYijhcetmBP/`
- `source_type`: `video`
- `platform`: Instagram
- `visibility`: public
- `duration`: `59.047s`

## Commands

```bash
summarize 'https://www.instagram.com/p/DYijhcetmBP/' --extract-only --length medium
/tmp/codexter-ytdlp/bin/yt-dlp -v --no-playlist --write-thumbnail --write-info-json -o '/tmp/ig_DYijhcetmBP/%(id)s.%(ext)s' 'https://www.instagram.com/p/DYijhcetmBP/'
ffmpeg -y -i /tmp/ig_DYijhcetmBP/DYijhcetmBP.mp4 -vf 'fps=1/5,scale=360:-1' /tmp/ig_DYijhcetmBP/frames/frame_%03d.jpg
ffmpeg -y -pattern_type glob -i '/tmp/ig_DYijhcetmBP/frames/*.jpg' -vf 'scale=240:-1,tile=3x4:padding=8:margin=8:color=white' /tmp/ig_DYijhcetmBP/contact_sheet.jpg
```

## Transcript Status

- `status`: visual-only / no full transcript stored
- `reason`: `summarize` returned only thin page text during the first pass.
- `confidence impact`: source todos that depend on spoken narration remain
  lower confidence until Whisper or another transcript path is attached.

## Frame Evidence

- `evidence/contact_sheet.jpg`: compact overview of sampled frames
- `evidence/frames/image-prompt.jpg`: visible image-generation prompt/process
- `evidence/frames/event-timing.jpg`: visible animation phase/timing spec
- `evidence/frames/prompt-checklist.jpg`: visible reusable checklist/master
  prompt cue
- `evidence/frames/final-artifact.jpg`: final composed portal artifact

## Retention Note

Raw MP4, intermediate sampled frames, and any bulky raw extraction outputs were
kept out of tracked docs. This run stores compact metadata, a contact sheet,
and selected frames only.

## Downstream

Use `video-understanding` to reconstruct the source todos and copied-skill
candidate, then route the target implementation to
`frontend-craft:composed-scroll-animation`.
