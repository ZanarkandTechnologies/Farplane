# Video Generation Todos

Use this as the ordered checklist whenever `video-generation` is active.

- [ ] Classify the request as text-to-video, image-to-video, reference-to-video, avatar/lipsync, video edit, utility, marketing, explainer, storyboard, ad spec, prompt improvement, or frontend-bound asset.
- [ ] If the request is React, Remotion, TSX-to-video, deterministic animation, or code-rendered MP4, stop using this skill and route to `remotion-render`.
- [ ] For CLI setup, app discovery, schemas, samples, or generic inference.sh help, load `references/tools/infsh-cli.md`.
- [ ] For vague/general AI video requests, model selection, "what should I use?", broad model-native video generation, video edits, foley, upscaling, or utilities, use the model map in `SKILL.md` first.
- [ ] After `SKILL.md` selects a model family, load the matching specific reference instead of staying at the umbrella level.
- [ ] For Google Veo, load `references/tools/google-veo.md`.
- [ ] For still image animation, load `references/tools/image-to-video.md`.
- [ ] For Pruna/P-Video fast or economical generation, load `references/tools/p-video.md`.
- [ ] For talking head, avatar, portrait animation, or lipsync, load `references/tools/p-video-avatar.md`, `references/tools/ai-avatar-video.md`, and `references/guides/talking-head-production.md`.
- [ ] For HappyHorse, physical realism, or video editing, load `references/tools/happyhorse.md`.
- [ ] For Seedance, reference video, or audio-aware generation, load `references/tools/seedance.md`.
- [ ] For marketing or promo videos, load `references/guides/ai-marketing-videos.md`.
- [ ] For explainer, tutorial, or product demo sequences, load `references/guides/explainer-video-guide.md`.
- [ ] For storyboard or shot-list work, load `references/guides/storyboard-creation.md`.
- [ ] For social/video ad specs, load `references/guides/video-ad-specs.md`.
- [ ] For prompt improvement, load `references/guides/video-prompting-guide.md`.
- [ ] Use `imagegen` first for still frames, portraits, posters, or reference art unless the user explicitly wants a CLI image app.
- [ ] Check `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before relying on an app schema.
- [ ] Confirm external compute/spend is acceptable before any `belt app run`.
- [ ] Save final videos, prompts, input JSON, result JSON, and notes inside the workspace, not only in a remote URL, temp path, or Codex home path.
- [ ] If the video is used on a web surface, route implementation/proof through `frontend-craft`, `references/frontend-asset-qa.md`, and `visual-qa` when layout or taste is affected.
