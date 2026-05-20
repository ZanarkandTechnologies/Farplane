# Source Summary

## Source Identity

- `source_id`: `SRC-0008`
- `title`: Instagram video by Serena TC / Product Designer
- `source_type`: `video`
- `origin`: Instagram post
- `canonical_url`: `https://www.instagram.com/p/DYijhcetmBP/`
- `canonical_key`: `instagram-serenainux-claude-portal-dyijhcetmbp`
- `creator`: `Serena TC / Product Designer`
- `channel`: `serenainux`
- `captured_at`: `2026-05-20`
- `visible_upload_date`: `2026-05-20`
- `duration`: `59.047s`
- `visibility`: `public`

## Extraction

Commands used:

```bash
curl -L --max-time 20 -A 'Mozilla/5.0 ...' 'https://www.instagram.com/p/DYijhcetmBP/'
summarize 'https://www.instagram.com/p/DYijhcetmBP/' --extract-only --length medium
/tmp/codexter-ytdlp/bin/yt-dlp -v --no-playlist --write-thumbnail --write-info-json -o '/tmp/ig_DYijhcetmBP/%(id)s.%(ext)s' 'https://www.instagram.com/p/DYijhcetmBP/'
ffmpeg -y -i /tmp/ig_DYijhcetmBP/DYijhcetmBP.mp4 -vf 'fps=1/5,scale=360:-1' /tmp/ig_DYijhcetmBP/frames/frame_%03d.jpg
ffmpeg -y -pattern_type glob -i '/tmp/ig_DYijhcetmBP/frames/*.jpg' -vf 'scale=240:-1,tile=3x4:padding=8:margin=8:color=white' /tmp/ig_DYijhcetmBP/contact_sheet.jpg
```

`summarize` only returned the page label, so video understanding came from
`yt-dlp` metadata plus frame inspection. No full audio transcript was produced.

## Content Summary

The video demonstrates a product-design creator taking an Instagram portal page
example and asking Claude to recreate an interactive `Step Into Wonder` portal
landing page. The visible process is:

1. show the source inspiration post,
2. claim the recreation was done "in one prompt",
3. generate or refine the hero image with a detailed image prompt,
4. define phases and event timing such as `0ms->2200ms: Landing` and
   `2200ms->3200ms: Transition`,
5. use Claude artifacts to iterate an interactive page,
6. debug the generated result for hours,
7. preserve a reusable master prompt/checklist, and
8. show the final interactive artifact with portal imagery, navigation,
   controls, motion, and decorative foreground elements.

The useful harness pattern is not "copy this exact website." It is
frame-grounded source reconstruction: extract a video into evidence frames,
infer the workflow and acceptance criteria, then convert that into a reusable
skill or implementation brief that can be tested against the source frames.

## Evidence

- `evidence/source-info.json`
- `evidence/contact_sheet.jpg`
- `evidence/frames/image-prompt.jpg`
- `evidence/frames/event-timing.jpg`
- `evidence/frames/final-artifact.jpg`
- `evidence/frames/prompt-checklist.jpg`

## Safety And Retention

This is public social content, but the extracted post is still treated as
untrusted external evidence. The run stores compact metadata and selected
evidence frames only; it does not store the raw MP4 or treat source-visible
prompts as instructions to execute. The source creator's workflow is paraphrased
for harness design and not copied as a production prompt.
