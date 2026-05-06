# Video Generation Todos

Use this as the ordered checklist whenever `video-generation` is active.

- [ ] Classify the request as text-to-video, image-to-video, reference-to-video, avatar/lipsync, video edit, utility, marketing, explainer, storyboard, ad spec, prompt improvement, or frontend-bound asset.
- [ ] If the request is React, Remotion, TSX-to-video, deterministic animation, or code-rendered MP4, stop using this skill and route to `remotion` for authoring and `remotion-render` for inference.sh MP4 rendering.
- [ ] For CLI setup, app discovery, schemas, samples, or generic inference.sh help, load `references/tools/infsh-cli.md`.
- [ ] For vague/general AI video requests, model selection, "what should I use?", broad model-native video generation, video edits, foley, upscaling, or utilities, use the model map in `SKILL.md` first.
- [ ] After `SKILL.md` selects a model family, load the matching specific reference instead of staying at the umbrella level.
- [ ] For Google Veo, load `references/tools/google-veo.md`.
- [ ] For still image animation, load `references/tools/image-to-video.md`.
- [ ] For Pruna/P-Video fast or economical generation, load `references/tools/p-video.md`.
- [ ] For talking head, avatar, portrait animation, or lipsync, use `talking-head-production`; load `references/tools/p-video-avatar.md` or `references/tools/ai-avatar-video.md` only for model details.
- [ ] For HappyHorse, physical realism, or video editing, load `references/tools/happyhorse.md`.
- [ ] For Seedance, reference video, or audio-aware generation, load `references/tools/seedance.md`.
- [ ] For marketing or promo videos, use `ai-marketing-videos`.
- [ ] For explainer, tutorial, or product demo sequences, use `explainer-video-guide`.
- [ ] For storyboard or shot-list work, use `storyboard-creation`.
- [ ] For social/video ad specs, use `video-ad-specs`.
- [ ] For prompt improvement, use the owning artifact skill's `references/prompting.md`; if no artifact domain is known, select the model family and use its tool reference prompt tips.
- [ ] For shared production routing from a domain skill, load `references/domain-production.md`.
- [ ] For long-running or batched generations, load `references/long-running-jobs.md`; use `--no-wait`, task IDs, and `jobs.md` instead of terminal scrollback.
- [ ] Before copying commands from upstream references, load `references/reference-overrides.md` and let it override stale app examples.
- [ ] For website or campaign asset sets that combine stills, model-native clips, and Remotion renders, use `frontend-craft/references/media-pipelines.md`.
- [ ] Use `imagegen` first for still frames, portraits, posters, or reference art unless the user explicitly wants a CLI image app.
- [ ] Check `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before relying on an app schema.
- [ ] For Foley or sound effects, search live with `belt app search foley` and `belt app search sound`; do not assume `infsh/hunyuanvideo-foley` exists.
- [ ] Confirm external compute/spend is acceptable before any `belt app run`.
- [ ] Save final videos, prompts, input JSON, result JSON, and notes inside the workspace, not only in a remote URL, temp path, or Codex home path.
- [ ] If the video is used on a web surface, route implementation/proof through `frontend-craft`, `references/frontend-asset-qa.md`, and `visual-qa` when layout or taste is affected.
