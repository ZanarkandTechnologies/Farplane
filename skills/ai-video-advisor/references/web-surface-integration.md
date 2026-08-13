# Web-Surface Media Integration

Load this when generated stills, model-native video, and Remotion output belong
to one website, landing page, campaign, or product-demo surface.

## Asset Rows

Before generation, record each slot:

| Slot | Purpose | Owner | Prompt/input | Output path | Fallback | QA |
| --- | --- | --- | --- | --- | --- | --- |
| Hero loop | first-viewport motion | `ai-video-advisor` | saved input | project video path | poster | browser playback |
| Poster | reduced-motion/mobile fallback | image owner | saved input | project image path | solid color | responsive crop |
| Explainer | deterministic data or product sequence | `remotion` | composition/input | project video path | static image | frame check |

## Flow

1. Let `impl-plan` reuse or resolve the accepted landing, visual, and asset
   context before implementation.
2. Plan slots, fallbacks, paths, and provenance before starting model jobs.
3. Generate still references or posters before dependent image-to-video work.
4. Continue layout and code only against planned paths; wire final files only
   after they exist locally.
5. Verify playback, responsive crops, autoplay/loop/muted policy,
   reduced-motion fallback, and visual proof through the ticket QA contract.

Use Remotion for deterministic timing, captions, overlays, and data callouts;
use model-native video for footage and camera motion that code cannot honestly
author.
