# Asset Generation

Use this when a frontend needs a bitmap hero, mockup, texture, product image, illustration, generated video, poster frame, or visual direction probe.

## Default

Use the existing `imagegen` skill first for still images. It is the Codex-native path and does not require local API keys for normal generation.

Use `video-generation` when the frontend needs model-native video, image-to-video, avatar/lipsync clips, video edits, foley, upscaling, or assembled marketing/explainer clips. Use `remotion-render` when the desired asset is a deterministic React/Remotion animation rendered to MP4.

## Workflow

1. Decide whether the asset is a final project asset, a visual direction probe, or a throwaway reference.
2. Use `imagegen` for bitmap generation or editing, `video-generation` for model-native video, or `remotion-render` for code-rendered MP4s.
3. Save project-bound final assets inside the workspace; never reference only `$CODEX_HOME/generated_images`, remote result URLs, or temporary output paths.
4. Record the prompt/input JSON, source references, saved path, and any post-processing.
5. For video, also record poster/fallback behavior, autoplay/loop/muted/controls policy, reduced-motion fallback, and expected QA evidence.
6. Implement against the asset or use the probe to refine `functional-ui`, `visual-design`, or `landing-page` briefs.

## External Tool Gates

- Do not assume inference.sh, Nano Banana, Kling, Runway, Midjourney, or Replicate MCP are installed.
- If a project has a configured external tool, use it only after confirming the local command/API surface exists.
- If no configured external tool exists, keep the plan on built-in `imagegen` and code-native effects.
- Treat external video generation as spend-sensitive compute. Capability-gate with the owning skill before running live jobs.

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
