# Asset Generation

Use this when a frontend needs a bitmap hero, mockup, texture, product image, illustration, generated video, poster frame, or visual direction probe.

## Default

Use the existing `imagegen` skill first for ordinary still images. It is the Codex-native path and does not require local API keys for normal generation.

Use `image-generation` when the frontend needs inference.sh image models, model selection, background removal, image upscaling, repeatable CLI image pipelines, or a named image model such as GPT-Image-2, Nano Banana, Qwen, FLUX, or P-Image.

Use `product-photography`, `ai-social-media-content`, `linkedin-content`, `social-media-carousel`, or `twitter-thread-creation` when the frontend asset is really a product-photo or social/campaign artifact rather than a generic image.

Use `video-generation` when the frontend needs model-native video, image-to-video, avatar/lipsync clips, video edits, foley, upscaling, or assembled marketing/explainer clips. Use `remotion` when the desired asset is deterministic React/Remotion code, then `remotion-render` when that code should become an MP4 through inference.sh.

## Workflow

1. Decide whether the asset is a final project asset, a visual direction probe, or a throwaway reference.
2. Use the domain skill first for product-photo or social/campaign artifacts; otherwise use `imagegen` for ordinary bitmap generation or editing, `image-generation` for inference.sh image routing, `video-generation` for model-native video, `remotion` for code-authored motion, or `remotion-render` for code-rendered MP4s.
3. Save project-bound final assets inside the workspace; never reference only `$CODEX_HOME/generated_images`, remote result URLs, or temporary output paths.
4. Record the prompt/input JSON, source references, saved path, and any post-processing.
5. For video, also record poster/fallback behavior, autoplay/loop/muted/controls policy, reduced-motion fallback, and expected QA evidence.
6. For multi-asset website or campaign work, load `media-pipelines.md` before generation so image, video, Remotion, fallback, and QA slots are planned together.
7. For batches, start independent inference.sh jobs with `--no-wait`, record task IDs in the owning skill's `jobs.md`, and continue non-dependent frontend work while polling.
8. Implement against the asset or use the probe to refine `functional-ui`, `visual-design`, or `landing-page` briefs.

## External Tool Gates

- Do not assume inference.sh, Nano Banana, Kling, Runway, Midjourney, or Replicate MCP are installed.
- If a project has a configured external tool, use it only after confirming the local command/API surface exists.
- If no configured external tool exists, keep the plan on built-in `imagegen` and code-native effects.
- Treat external image and video generation as spend-sensitive compute. Capability-gate with the owning skill before running live jobs.

## Good Uses

- Landing-page hero imagery.
- Landing-page hero video, generated scene loops, and poster frames.
- Brand/taste probes before high-fidelity UI implementation.
- Product or app mockups that need real visual material.
- Textures, backgrounds, editorial images, sprites, or cutouts.

## Bad Uses

- Icons that should be code-native SVG or from the app's icon library.
- Precise UI implementation screenshots that need semantic DOM.
- Replacing a needed UX plan with mood art.
- Using generated video to avoid browser proof for a user-visible page.
