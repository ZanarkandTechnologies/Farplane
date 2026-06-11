---
name: reel-collage
description: "Turn image URLs or local files into 9:16 reel collage backgrounds for shorts, explainers, and green-screen videos."
tier: 3
group: content-social
source: local
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Reel Collage

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Confirm the output is for editing or green-screen use, not direct
      publishing.
- [ ] 2. Use exactly four source images per collage unless the user asks for a
      batch.
- [ ] 3. Prefer real-photo sources for authenticity.
- [ ] 4. Save the collage in the active workspace.
- [ ] 5. Run `scripts/make_collage.py`; do not rewrite the compositor.
- [ ] 6. Visually inspect the output when possible.
- [ ] 7. Report the output path and any source/crop caveats.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this when the user wants to turn image URLs or local image files into a
2x2 collage background for reels, shorts, TikToks, or talking-head green-screen
videos.

## Job

Create a vertical 9:16 collage image from source images, usually real photos.
Do not add a center strip by default; only use `--center-safe` when the user
explicitly wants a dark column behind a keyed speaker.

## Script

Run:

```bash
python3 /Users/kenjipcx/.codex/skills/reel-collage/scripts/make_collage.py \
  --output /path/to/collage.jpg \
  image1.jpg image2.jpg image3.jpg image4.jpg
```

Sources can be local paths or `http(s)` URLs. Defaults are `1080x1920`,
2 columns, 2 rows, cover-crop each tile, and JPEG output based on file suffix.

Useful options:

- `--width 1080 --height 1920`: output size.
- `--gutter 0`: spacing between panels.
- `--darken 0.12`: dark overlay on each tile for readable captions.
- `--fit solid`: fit the image inside its tile and fill empty space with a
  sampled edge color, useful for clean square screenshots.
- `--fit expand`: fit the image inside its tile and fill empty space with a
  blurred/dimmed copy when a softer backdrop is desired.
- `--fits cover,solid,solid`: choose fit behavior per source when one image
  should zoom/crop but another should stay fully visible.
- `--position top` or `--position top,center,bottom,left`: bias crop or
  placement globally or per source.
- `--zoom 0.85,1,1`: zoom a specific tile out or in. Values below `1` back
  off an aggressive cover crop.
- `--layout single`: expand one image to a 9:16 background.
- `--layout stack`: stack two images vertically into a 9:16 background.
- `--center-safe 260`: optional dark vertical strip behind the speaker.
- `--layout top2-bottom1`: two sources on top, third source spans the bottom.
- `--fit contain`: letterbox instead of cover-crop.
- `--notes /path/to/sources.md`: write source list.

## Decision Branches

- **User gives four URLs/paths:** run the script once.
- **User gives one square-ish image for a reel background:** use
  `--layout single --fit expand`.
- **User gives more than four sources:** either ask for the preferred grouping
  or create numbered batches of four when the grouping is obvious.
- **User wants a specific aesthetic:** select/order sources before running;
  the script only composes, crops, and tones.
- **User needs generated images first:** use `image-generation` or image search
  first, then pass the resulting files/URLs to this skill.

## Gotchas

- Do not use NDA/private screenshots unless the user explicitly confirms they
  are allowed in the video.
- Do not bake important text into the image; captions should be added in the
  video editor.
- Avoid source images with faces in the center if the speaker will be keyed
  over the middle.
- If the collage looks too AI-generated, replace sources with real photos
  rather than adding more filters.

## Judgment Questions

Use `advise` when it is unclear whether the collage should feel founder-like,
technical, documentary, cinematic, chaotic, polished, or meme-like.

## Outcome Contract

Return the generated collage path, the source paths/URLs used, and any notes
about crop issues or images that should be swapped.
