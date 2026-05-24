---
name: image-generation
version: 1.0.0
description: Generate, edit, upscale, or process images with inference.sh `belt` image apps, using a broad AI-image model map plus Codexter's workspace, spend-gate, and frontend asset rules. Covers GPT-Image-2, Gemini/Nano Banana, Qwen Image, FLUX, Pruna P-Image, background removal, image upscaling, text-to-image, image editing, inpainting, LoRA styles, product mockups, social graphics, marketing visuals, illustrations, and frontend-bound image assets. Prefer built-in `imagegen` for normal Codex-native bitmap generation unless the user asks for inference.sh, belt, a named model, or CLI-based image pipelines.
tier: 3
group: content-image
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# Image Generation

Generate project-ready AI image assets with inference.sh CLI (`belt`) while keeping provider-specific details in references.

Use `todos.md` at the start of the pass. It is the ordered anti-forgetting checklist for model choice, reference loading, spend gates, asset saving, and frontend proof.

Use the built-in `imagegen` skill for normal Codex-native still image generation/editing. Use this skill when the user asks for inference.sh, `belt`, a named image model, CLI repeatability, upscaling, background removal, or a multi-step image pipeline.

Use domain image/social guide skills for artifact problems: `product-photography`
and `social-content` methods such as `social-content:cross-platform`,
`social-content:linkedin`, `social-content:carousel`, and
`social-content:twitter-thread`. Use this skill for model/app selection and
`belt` execution once the domain intent is known.

Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from their Related Skills sections unless the user explicitly asks to install upstream skills.

## Steps

1. Classify the job: `text-to-image`, `image-edit`, `inpainting`, `multi-reference`, `text-rendering`, `style-lora`, `fast-cheap`, `product-mockup`, `product-photography`, `social-visual`, `carousel`, `background-removal`, `upscaling`, or `frontend-bound`.
2. If the request is vague, use the best-current defaults below to pick the app family.
3. Load the specific reference file only after a family is selected.
4. Capability-gate the CLI path with `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before trusting any cached schema.
5. Treat `belt app run` as external compute/spend. Do not run it until that cost is acceptable for this task.
6. Save project assets, prompt/input JSON, result JSON, and notes inside the workspace.
7. For long-running or batched jobs, use the async workflow below instead of blocking the whole pass.
8. If the asset is used in a web surface, hand it to `frontend-craft` and verify loading, dimensions, alt text, responsive crops, and visual quality.

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
- Long-running jobs, batched tasks, timers, or delegated polling: `references/long-running-jobs.md`
- Product photography, packshots, e-commerce images, or commercial product shots: use `product-photography`
- Social media content, captions, thumbnails, UGC concepts, or cross-platform campaign assets: use `social-content:cross-platform`
- LinkedIn posts or professional social writing: use `social-content:linkedin`
- Instagram/LinkedIn/X carousel or multi-slide post: use `social-content:carousel`
- Twitter/X threads or posts: use `social-content:twitter-thread`
- Shared image/social artifact production workflow: `references/domain-production.md`

## Examples

```bash
mkdir -p output/image-generation/sneaker-product
belt app run openai/gpt-image-2 --input '{
  "prompt": "professional product photo of sneakers, studio lighting",
  "quality": "high"
}' --save output/image-generation/sneaker-product/result.json

mkdir -p output/image-generation/synth-editorial
belt app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "photorealistic editorial image of a modular synthesizer on a desk"
}' --save output/image-generation/synth-editorial/result.json

mkdir -p output/image-generation/signal-lab-poster
belt app run alibaba/qwen-image-2-pro --input '{
  "prompt": "A clean launch poster that says SIGNAL LAB in bold type"
}' --save output/image-generation/signal-lab-poster/result.json

mkdir -p output/image-generation/upscale
belt app run falai/topaz-image-upscaler \
  --input '{"image_url": "https://..."}' \
  --save output/image-generation/upscale/result.json
```

## Async Workflow

Use async runs when there are many independent images, slow upscales, or a frontend task can continue while assets render.

1. Create one bundle folder per asset and save `input.json` before starting the run.
2. Start independent jobs with `belt app run <app> --input <input.json> --no-wait --save <result.json>` when the CLI supports it.
3. Record every task ID in `jobs.md` with the app ID, input path, result path, intended final filename, and next poll time.
4. Poll with `belt task get <task-id>` and update `jobs.md`; do not rely on terminal scrollback as state.
5. If the current thread should wake later, use a thread heartbeat/timer when available and include the task IDs and result paths in the prompt.
6. Use a delegated QA or polling lane only when the current harness policy permits delegation and the batch is bounded/independent; make that lane write paths and task IDs back into the workspace before reporting done.
7. Continue non-dependent work while jobs run, but do not wire final assets into a frontend until the files exist locally or the remote URL has been copied into the project asset plan.

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
