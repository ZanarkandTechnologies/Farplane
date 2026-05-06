---
name: image-generation
version: 1.0.0
description: Generate, edit, upscale, or process images with inference.sh `belt` image apps, using a broad AI-image model map plus Codexter's workspace, spend-gate, and frontend asset rules. Covers GPT-Image-2, Gemini/Nano Banana, Qwen Image, FLUX, Pruna P-Image, background removal, image upscaling, text-to-image, image editing, inpainting, LoRA styles, product mockups, social graphics, marketing visuals, illustrations, and frontend-bound image assets. Prefer built-in `imagegen` for normal Codex-native bitmap generation unless the user asks for inference.sh, belt, a named model, or CLI-based image pipelines.
allowed-tools: Read, Grep, Glob, Bash
---

# Image Generation

Generate project-ready AI image assets with inference.sh CLI (`belt`) while keeping provider-specific details in references.

Use `todos.md` at the start of the pass. It is the ordered anti-forgetting checklist for model choice, reference loading, spend gates, asset saving, and frontend proof.

Use the built-in `imagegen` skill for normal Codex-native still image generation/editing. Use this skill when the user asks for inference.sh, `belt`, a named image model, CLI repeatability, upscaling, background removal, or a multi-step image pipeline.

## Steps

1. Classify the job: `text-to-image`, `image-edit`, `inpainting`, `multi-reference`, `text-rendering`, `style-lora`, `fast-cheap`, `product-mockup`, `background-removal`, `upscaling`, or `frontend-bound`.
2. If the request is vague, use the best-current defaults below to pick the app family.
3. Load the specific reference file only after a family is selected.
4. Capability-gate the CLI path with `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before trusting any cached schema.
5. Treat `belt app run` as external compute/spend. Do not run it until that cost is acceptable for this task.
6. Save project assets, prompt/input JSON, result JSON, and notes inside the workspace.
7. If the asset is used in a web surface, hand it to `frontend-craft` and verify loading, dimensions, alt text, responsive crops, and visual quality.

## Best Current Defaults

These defaults come from the upstream inference.sh skill snapshot at `c5ad36c`. Always verify live availability and schema with `belt app get <app>` before a run.

| Use Case | Default | Why |
| --- | --- | --- |
| Highest-quality general generation/editing | `openai/gpt-image-2` | Strong text-to-image, editing, inpainting, references, and product/marketing outputs |
| Fast Google-native image generation/editing | `google/gemini-3-1-flash-image-preview` | Current Nano Banana 2 path, multi-image input, high-res, Google grounding |
| Professional text-heavy posters/banners | `alibaba/qwen-image-2-pro` | Text rendering and semantic adherence are the point of the model |
| Fast/economical generation or edits | `pruna/p-image` / `pruna/p-image-edit` | Optimized for speed/cost and common aspect ratios |
| Custom styles or LoRA | `falai/flux-dev-lora` / `falai/flux-2-klein-lora` | FLUX family is the style/LoRA branch |
| 2K-4K cinematic quality | `bytedance/seedream-4-5` | Upstream umbrella names it for 2K-4K cinematic quality |
| Background removal / transparent PNG | `infsh/birefnet` or live app from `background-removal.md` | Dedicated cutout branch |
| Upscaling/enhancement | `falai/topaz-image-upscaler` | Dedicated professional upscaling branch |

## Model Map

Browse live apps with:

```bash
belt app list --category image
```

| Model | App ID | Best For |
| --- | --- | --- |
| GPT-Image-2 | `openai/gpt-image-2` | Text-to-image, editing, inpainting |
| FLUX Dev LoRA | `falai/flux-dev-lora` | High quality with custom styles |
| FLUX.2 Klein LoRA | `falai/flux-2-klein-lora` | Fast with LoRA support |
| P-Image | `pruna/p-image` | Fast, economical, multiple aspects |
| P-Image-LoRA | `pruna/p-image-lora` | Fast with preset LoRA styles |
| P-Image-Edit | `pruna/p-image-edit` | Fast image editing |
| Gemini 3 Pro | `google/gemini-3-pro-image-preview` | Google high-quality image generation |
| Gemini 3.1 Flash | `google/gemini-3-1-flash-image-preview` | Nano Banana 2, fast Google image generation |
| Gemini 2.5 Flash | `google/gemini-2-5-flash-image` | Fast Google model |
| Grok Imagine | `xai/grok-imagine-image` | xAI image generation, multiple aspects |
| Seedream 4.5 | `bytedance/seedream-4-5` | 2K-4K cinematic quality |
| Seedream 4.0 | `bytedance/seedream-4-0` | High quality 2K-4K |
| Seedream 3.0 | `bytedance/seedream-3-0-t2i` | Accurate text rendering |
| Reve | `falai/reve` | Natural language editing, text rendering |
| ImagineArt 1.5 Pro | `falai/imagine-art-1-5-pro-preview` | Ultra-high-fidelity 4K |
| FLUX Klein 4B | `pruna/flux-klein-4b` | Ultra-cheap drafts |
| Topaz Upscaler | `falai/topaz-image-upscaler` | Professional upscaling |

## Reference Routes

- CLI setup, commands, schemas, or generic inference.sh: `references/tools/infsh-cli.md`
- GPT-Image-2, OpenAI image generation, editing, inpainting: `references/tools/gpt-image.md`
- Gemini/Nano Banana 2: `references/tools/nano-banana-2.md`
- Gemini/Nano Banana, Gemini 3 Pro, Gemini 2.5 Flash: `references/tools/nano-banana.md`
- Qwen Image 2 general generation/editing: `references/tools/qwen-image-2.md`
- Qwen Image 2 Pro, professional text rendering, posters, banners: `references/tools/qwen-image-2-pro.md`
- FLUX or LoRA style generation: `references/tools/flux-image.md`
- Pruna P-Image fast/economical generation/editing: `references/tools/p-image.md`
- Background removal, transparent PNG, cutouts: `references/tools/background-removal.md`
- Image upscaling or enhancement: `references/tools/image-upscaling.md`

## Examples

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "professional product photo of sneakers, studio lighting",
  "quality": "high"
}'

belt app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "photorealistic editorial image of a modular synthesizer on a desk"
}'

belt app run alibaba/qwen-image-2-pro --input '{
  "prompt": "A clean launch poster that says SIGNAL LAB in bold type"
}'

belt app run falai/topaz-image-upscaler --input '{"image_url": "https://..."}'
```

## Output Contract

For project assets, create a small artifact bundle:

```text
output/image-generation/<slug>/
  input.json
  result.json
  prompt.md
  final.png
  source.png
  notes.md
```

Use the repo's existing asset directory instead when one already exists for the target app or site.

Return the final image path or remote result plus workspace copy plan, prompt/input JSON path, result JSON path, source/reference asset paths, and frontend QA evidence path or skipped-QA reason.
