# Image Generation Todos

Use this as the ordered checklist whenever `image-generation` is active.

- [ ] Classify the request as text-to-image, image-edit, inpainting, multi-reference, text-rendering, style-LoRA, fast-cheap, product-mockup, product-photography, social-visual, carousel, background-removal, upscaling, or frontend-bound asset.
- [ ] For product photography, packshots, e-commerce images, or commercial product shots, use `product-photography`.
- [ ] For social media content, captions, thumbnails, UGC concepts, or cross-platform campaign assets, use `ai-social-media-content`.
- [ ] For LinkedIn posts or professional social writing, use `linkedin-content`.
- [ ] For Instagram/LinkedIn/X carousel or multi-slide post, use `social-media-carousel`.
- [ ] For Twitter/X threads or posts, use `twitter-thread-creation`.
- [ ] For shared production routing from a domain skill, load `references/domain-production.md`.
- [ ] If the user only needs normal Codex-native bitmap generation/editing and did not ask for inference.sh, `belt`, a named model, CLI repeatability, or a model comparison, use `imagegen` instead.
- [ ] For CLI setup, app discovery, schemas, samples, or generic inference.sh help, load `references/tools/infsh-cli.md`.
- [ ] For vague/general AI image requests or model selection, use the best-current defaults and model map in `SKILL.md` first.
- [ ] For GPT-Image-2, OpenAI image generation, editing, inpainting, or product/marketing outputs, load `references/tools/gpt-image.md`.
- [ ] For Nano Banana 2, Gemini 3.1 Flash Image Preview, multi-image input, high-res, or Google grounding, load `references/tools/nano-banana-2.md`.
- [ ] For Gemini native image generation, Gemini 3 Pro, or Gemini 2.5 Flash, load `references/tools/nano-banana.md`.
- [ ] For Qwen general image generation/editing, load `references/tools/qwen-image-2.md`.
- [ ] For Qwen Pro, posters, banners, or professional text rendering, load `references/tools/qwen-image-2-pro.md`.
- [ ] For FLUX, custom style, or LoRA requests, load `references/tools/flux-image.md`.
- [ ] For Pruna P-Image, fast/economical generation, fast edits, or preset LoRA styles, load `references/tools/p-image.md`.
- [ ] For transparent PNGs, cutouts, product photo cutouts, or background removal, load `references/tools/background-removal.md`.
- [ ] For upscaling, restoration, enhancement, or higher resolution, load `references/tools/image-upscaling.md`.
- [ ] For long-running or batched generations, load `references/long-running-jobs.md`; use `--no-wait`, task IDs, and `jobs.md` instead of terminal scrollback.
- [ ] Check `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before relying on an app schema.
- [ ] Confirm external compute/spend is acceptable before any `belt app run`.
- [ ] Never publish to social platforms unless the user explicitly asks to publish.
- [ ] Save final images, prompts, input JSON, result JSON, and notes inside the workspace, not only in a remote URL, temp path, or Codex home path.
- [ ] If the image is used on a web surface, route implementation/proof through `frontend-craft` and verify path loading, responsive crop, dimensions, alt text, and visual quality.
