# Image Providers And Model Map

Owner: [ai-image](../SKILL.md). Load in N2 when the provider or model is not
obvious, when the operator names a model, or when an edit must fall back.

Prices and availability move. Treat every figure here as a hint and take the
live number from `treg catalog_get`, Ideogram `dry_run`, or `belt app get`
before any paid call.

## Route Order

1. **Edit of an existing image** -> Ideogram 4.5 Precise Edit (direct API).
2. **New image, paid model** -> `treg` (default route for generation).
3. **Named inference.sh app, cutout, upscale, LoRA** -> `belt`.
4. **Quick Codex-native draft, no named model, no spend** -> built-in `imagegen`.

## Editing Default: Ideogram 4.5 Precise Edit

Ideogram 4.5 Precise Edit is the default for every edit (one change, background
swap, restyle, text fix, character consistency), including edits first asked
for through `treg` or `imagegen`. It returns the source's exact size and copies
unchanged pixels from it, so repeated edits do not drift. Say in the prompt
what must stay unchanged.

| Route | Input | Credential state |
| --- | --- | --- |
| Ideogram API (default) | `farplane run -- curl -X POST "https://api.ideogram.ai/v2/image/precise-edit/ideogram-4-5?dry_run=true" -H "Api-Key: $IDEOGRAM_API_KEY" -F image=@source.png -F prompt="..." -F quality=medium` for the free quote, then the same call without `dry_run`; optional `reference_images` (max 4, 3 with a mask), `mask` (black = edit). A medium 2:3 frame quoted $0.06. | `IDEOGRAM_API_KEY` in Doppler `farplane/dev_personal`; account has credits. Not on `belt` or `treg` (checked 2026-10-12). |
| Seedream 4.5 (fallback) | `belt app run bytedance/seedream-4-5 --input input.json` with `{"prompt","image":"source.png","size":"2K"}`, or Seedream via `treg`; one source, about $0.04 | Not a precise edit: it re-dresses the whole set. Name the props that must stay and tell the operator the fallback was used. |

Without the Ideogram key, say so and use Seedream. For multi-reference
composition, use `treg` GPT Image 2 / 2.5. Name the route used in `notes.md`.

## Generation Defaults

| Use case | Default | Route | Why |
| --- | --- | --- | --- |
| Highest-quality general generation, product and marketing | GPT Image 2 / GPT Image 2.5 | `treg` (`image-gen.gpt-image-2`, `image-gen.gpt-image-2-5`) | Strong prompt adherence, references, product outputs |
| Fast Google-native generation, multi-image input | Gemini 3 Pro Image / Gemini 3.1 Flash Image | `treg` (`image-gen.gemini-3-pro-image`) or `belt google/gemini-3-1-flash-image-preview` | Cheap, multi-image, high-res |
| Text-heavy posters and banners (art text, not UI text) | `alibaba/qwen-image-2-pro` | `belt` | Text rendering is the point of the model |
| Fast or economical drafts | `pruna/p-image`, `pruna/flux-klein-4b` | `belt` | Speed and cost |
| Custom styles or LoRA | `falai/flux-dev-lora`, `falai/flux-2-klein-lora` | `belt` | FLUX style/LoRA branch |
| Background removal / transparent PNG | `infsh/birefnet` or the live app in [background-removal](tools/background-removal.md) | `belt` | Dedicated cutout branch |
| Upscaling / enhancement | `falai/topaz-image-upscaler` | `belt` | Dedicated upscaling branch |

Spend log shows these in use: "GPT Image 2 via treg", "GPT Image 2.5 via treg".
Indicative `treg` prices seen 2026-10-12: GPT Image 2 from about $0.08, GPT
Image 2.5 from about $0.16, Gemini 3 Pro Image from about $0.03 per call; the
provider choice changes the price, so read `catalog_get` each time.

## belt Model Map

Browse live apps with `belt app list --category image`.

| Model | App ID | Best for |
| --- | --- | --- |
| GPT-Image-2 | `openai/gpt-image-2` | Text-to-image, editing fallback, inpainting |
| FLUX Dev LoRA | `falai/flux-dev-lora` | High quality with custom styles |
| FLUX.2 Klein LoRA | `falai/flux-2-klein-lora` | Fast with LoRA support |
| P-Image | `pruna/p-image` | Fast, economical, multiple aspects |
| P-Image-LoRA | `pruna/p-image-lora` | Fast with preset LoRA styles |
| P-Image-Edit | `pruna/p-image-edit` | Fast drafts only; not the edit default |
| Gemini 3 Pro | `google/gemini-3-pro-image-preview` | Google high-quality generation |
| Gemini 3.1 Flash | `google/gemini-3-1-flash-image-preview` | Nano Banana 2, fast Google generation |
| Gemini 2.5 Flash | `google/gemini-2-5-flash-image` | Fast Google model |
| Grok Imagine | `xai/grok-imagine-image` | xAI generation, multiple aspects |
| Seedream 4.5 | `bytedance/seedream-4-5` | Edit fallback; 2K-4K cinematic quality |
| Seedream 3.0 | `bytedance/seedream-3-0-t2i` | Accurate text rendering |
| Reve | `falai/reve` | Natural-language editing, text rendering |
| ImagineArt 1.5 Pro | `falai/imagine-art-1-5-pro-preview` | Ultra-high-fidelity 4K |
| FLUX Klein 4B | `pruna/flux-klein-4b` | Ultra-cheap drafts |
| Topaz Upscaler | `falai/topaz-image-upscaler` | Professional upscaling |

## Tool References

Copied upstream inference.sh docs; read-only, refresh from upstream rather than
rewrite. Do not run their `npx skills add ...` lines unless asked.

- `belt` setup, commands, schemas: [infsh-cli](tools/infsh-cli.md)
- GPT-Image-2 generation, editing, inpainting: [gpt-image](tools/gpt-image.md)
- Nano Banana 2 / Gemini 3.1 Flash: [nano-banana-2](tools/nano-banana-2.md)
- Gemini 3 Pro, Gemini 2.5 Flash: [nano-banana](tools/nano-banana.md)
- Qwen general generation and editing: [qwen-image-2](tools/qwen-image-2.md)
- Qwen Pro posters and banners: [qwen-image-2-pro](tools/qwen-image-2-pro.md)
- FLUX and LoRA styles: [flux-image](tools/flux-image.md)
- Pruna P-Image fast generation: [p-image](tools/p-image.md)
- Cutouts and transparent PNGs: [background-removal](tools/background-removal.md)
- Upscaling and restoration: [image-upscaling](tools/image-upscaling.md)

## Examples

```bash
# Edit: free quote, then the paid call
farplane run -- curl -s -X POST \
  "https://api.ideogram.ai/v2/image/precise-edit/ideogram-4-5?dry_run=true" \
  -H "Api-Key: $IDEOGRAM_API_KEY" -F image=@source.png \
  -F prompt="Replace the mug with a matte black tumbler; keep the desk, light and hands unchanged" \
  -F quality=medium

# Upscale through belt
belt app get falai/topaz-image-upscaler
belt app run falai/topaz-image-upscaler --input input.json \
  --save .farplane/ai-image/2026-10-12-hero-upscale/result.json
```
