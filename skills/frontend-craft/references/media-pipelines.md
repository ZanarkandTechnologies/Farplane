# Media Pipelines

Use this when a website, landing page, campaign, or product demo needs multiple generated assets across still images, model-native video, and Remotion.

## Routing

| Need | Skill |
| --- | --- |
| Ordinary bitmap asset or edit | `imagegen` |
| Named inference.sh image model, batch images, upscaling, cutouts | `ai-image-advisor` |
| Product photos, packshots, e-commerce image sets | `product-photography`, then `imagegen` or `ai-image-advisor` |
| Cross-platform social campaign assets | `social-content:cross-platform`, then image/video/carousel execution |
| LinkedIn posts or professional social assets | `social-content:linkedin`, then `social-content:carousel` or image execution when visual |
| Instagram/LinkedIn/X carousel assets | `social-content:carousel`, then image/code execution |
| Twitter/X threads or media-supported posts | `social-content:twitter-thread`, then image execution when visual |
| Marketing/promo video domain plan | `video-production:marketing`, then `ai-video-advisor` for execution |
| Explainer/product demo domain plan | `video-production:explainer`, then `ai-video-advisor` or `remotion` for execution |
| Storyboard/shot list | `video-production:storyboard`, then `imagegen`, `ai-image-advisor`, or `ai-video-advisor` |
| Talking head/avatar domain plan | `video-production:talking-head`, then `ai-video-advisor` for execution |
| Platform ad specs/domain plan | `video-production:ad-spec`, then `ai-video-advisor` for execution |
| Model-native video, image-to-video, avatar/lipsync, video edit | `ai-video-advisor` |
| Remotion code authoring, timing, captions, SFX, composition rules | `remotion` |
| Render Remotion TSX/code to MP4 through inference.sh | `remotion-render` |
| Frontend implementation and proof | `frontend-craft`, then `visual-qa` when UI changed |

## Website Asset Plan

For each generated asset, write an asset row before generation:

```markdown
| Slot | Purpose | Skill | App/model | Prompt/input | Output path | Fallback | QA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hero loop | first viewport ambient product motion | ai-video-advisor | google/veo-3-1-fast | output/ai-video-advisor/hero/input.json | public/video/hero.mp4 | poster.png + CSS gradient | browser playback |
| Poster | reduced-motion/mobile fallback | ai-image-advisor | openai/gpt-image-2 | output/ai-image-advisor/poster/input.json | public/images/hero-poster.png | solid color | responsive crop |
| Data explainer | deterministic chart animation | remotion + remotion-render | infsh/remotion-render | output/remotion-render/chart/input.json | public/video/chart.mp4 | static chart PNG | frame check |
```

## Efficient Batch Flow

1. Plan all asset slots, fallbacks, and file paths first.
2. Load the relevant domain skill before choosing models when the asset is product photography, social content, a carousel, a marketing video, explainer, storyboard, talking-head video, ad, or prompt-improvement task; image/social domain skills link to [image domain-production](../../ai-image-advisor/references/domain-production.md), and video domain skills link to [video domain-production](../../ai-video-advisor/references/domain-production.md).
3. Generate still references/posters before image-to-video when they control style or identity.
4. Start independent image/video jobs with `--no-wait` and record them in each bundle's `jobs.md`.
5. Continue frontend structure, copy, layout, CSS, and Remotion authoring while jobs run.
6. Poll task IDs, copy finished media into the project, then wire real paths.
7. Verify browser loading, responsive crops, autoplay/loop/muted policy, reduced-motion fallback, and poster behavior.

## Remotion Plus AI Video

Use Remotion when timing and composition must be deterministic: data overlays, captions, product UI callouts, comparison grids, launch slates, kinetic typography, and end cards.

Use model-native video for hard-to-author footage: realistic camera motion, lifestyle clips, atmospheric backgrounds, avatar performances, or product-world scenes.

For hybrid videos, create AI clips first, then assemble with Remotion:

1. `ai-image-advisor` or `imagegen` for reference frames and poster frames.
2. `ai-video-advisor` for footage clips.
3. `remotion` for sequencing, captions, overlays, transitions, SFX timing, and brand system.
4. `remotion-render` for MP4 export when local rendering is not the chosen path.
