# Reel Collage

Owner: [ai-image](../SKILL.md) `collage` mode. Load when the operator wants
image URLs or local files turned into a 9:16 background for reels, shorts,
TikToks, or keyed talking-head videos. Folded from the former reel-collage
skill. The compositor is [make_collage.py](../scripts/make_collage.py); run it,
do not rewrite it.

## Run

From the Farplane checkout:

```bash
uv run --with pillow python skills/ai-image/scripts/make_collage.py \
  --output .farplane/ai-image/2026-10-12-reel-bg/collage.jpg \
  --notes .farplane/ai-image/2026-10-12-reel-bg/sources.md \
  image1.jpg image2.jpg image3.jpg image4.jpg
```

Sources can be local paths or `http(s)` URLs. Defaults: `1080x1920`, 2x2 grid,
cover-crop each tile, `--darken 0.10`, JPEG when the output ends in `.jpg`.
The script needs Pillow only; the repo `.venv` does not ship it, so run it
through `uv run --with pillow` (`--help` works without Pillow).

## Options

| Option | Effect |
| --- | --- |
| `--width 1080 --height 1920` | Output size |
| `--gutter 0` | Pixels between panels |
| `--darken 0.12` | Dark overlay per tile for readable captions |
| `--fit cover\|contain\|expand\|solid` | Crop; letterbox; blurred backdrop; sampled edge colour fill |
| `--fits cover,solid,solid` | Per-source fit |
| `--position top` or `top,center,bottom,left` | Crop or placement bias, global or per source |
| `--zoom 0.85,1,1` | Per-tile zoom; below 1 backs off an aggressive cover crop |
| `--layout single\|stack\|2x2\|top2-bottom1` | 1, 2, 4, or 3 sources |
| `--center-safe 260` | Dark vertical strip behind a keyed speaker; off by default |
| `--notes sources.md` | Writes the source list |

## Decision Branches

- Four URLs or paths: run once with the 2x2 default.
- One square-ish image: `--layout single --fit expand`.
- More than four sources: ask for the grouping, or batch in fours when it is obvious.
- A specific aesthetic: choose and order sources first; the script only
  composes, crops, and tones. When the direction is unclear, compare founder,
  technical, documentary, cinematic, chaotic, polished, and meme routes inline
  and recommend one.
- Generated sources needed first: run `create` mode, then pass the saved files.
- Only use `--center-safe` when the operator wants a dark column behind the speaker.

## Gotchas

- No faces centre-frame where the speaker will be keyed over the middle; pick
  or `--position` the tiles so faces sit at the edges.
- No baked-in text: captions are added in the video edit (the external
  `hyperframes` skill).
- No NDA or private screenshots unless the operator confirms they may appear.
- If the collage looks AI-generated, swap in real photos rather than adding filters.
- The output is an editing background, not a post; nothing is published.
