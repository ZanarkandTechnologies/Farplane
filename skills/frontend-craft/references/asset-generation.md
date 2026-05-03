# Asset Generation

Use this when a frontend needs a bitmap hero, mockup, texture, product image, illustration, or visual direction probe.

## Default

Use the existing `imagegen` skill first. It is the Codex-native path and does not require local API keys for normal generation.

## Workflow

1. Decide whether the asset is a final project asset, a visual direction probe, or a throwaway reference.
2. Use `imagegen` for bitmap generation or editing.
3. Save project-bound final assets inside the workspace; never reference only `$CODEX_HOME/generated_images`.
4. Record the prompt, source references, saved path, and any post-processing.
5. Implement against the asset or use the probe to refine `functional-ui`, `visual-design`, or `landing-page` briefs.

## External Tool Gates

- Do not assume inference.sh, Nano Banana, Kling, Runway, Midjourney, or Replicate MCP are installed.
- If a project has a configured external tool, use it only after confirming the local command/API surface exists.
- If no configured external tool exists, keep the plan on built-in `imagegen` and code-native effects.

## Good Uses

- Landing-page hero imagery.
- Brand/taste probes before high-fidelity UI implementation.
- Product or app mockups that need real visual material.
- Textures, backgrounds, editorial images, sprites, or cutouts.

## Bad Uses

- Icons that should be code-native SVG or from the app's icon library.
- Precise UI implementation screenshots that need semantic DOM.
- Replacing a needed UX plan with mood art.
