---
name: video-generation
version: 1.0.0
description: Generate or edit AI video assets with inference.sh `belt` video apps, using the broad AI-video model map plus Codexter's workspace, spend-gate, and frontend QA rules. Covers Google Veo, Seedance 2.0, HappyHorse, Wan, Grok, P-Video, avatar/lipsync, image-to-video, video editing, foley discovery, upscaling, social media videos, marketing clips, explainer videos, product demos, and frontend-bound video assets. Route React/Remotion code authoring to `remotion` and inference.sh code-to-video renders to `remotion-render`.
tier: 3
group: content-video
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# Video Generation

Generate project-ready AI video assets with inference.sh CLI (`belt`) while keeping provider-specific details in references.

Use `todos.md` at the start of the pass. It is the ordered anti-forgetting checklist for model choice, reference loading, spend gates, asset saving, and frontend proof.

Use `video-production` method addresses for artifact/product problems:
`video-production:marketing`, `video-production:explainer`,
`video-production:storyboard`, `video-production:talking-head`, and
`video-production:ad-spec`. Prompting guidance belongs inside that domain
workflow skill. Use this skill for model/app selection and `belt` execution
once the domain intent is known.

For video prompt quality when no narrower artifact prompt applies, load `references/prompting/video-prompting-guide.md` for shot type, camera movement, lighting, temporal motion, and model-specific phrasing.

Do not use this skill for React/Remotion code authoring or code-to-video. Exit and use `remotion` for authoring, then `remotion-render` for inference.sh MP4 rendering.

Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from their Related Skills sections unless the user explicitly asks to install upstream skills.

## Steps

1. Classify the job: `text-to-video`, `image-to-video`, `reference-to-video`, `avatar-lipsync`, `video-edit`, `utility`, `marketing`, `explainer`, `storyboard`, `ad-spec`, `prompt-improvement`, or `frontend-bound`.
2. If the request is vague, use the model tables in this file to pick the app family.
3. Load `references/reference-overrides.md` before copying commands from any upstream reference.
4. Load the specific reference file only after a family is selected.
5. Use `imagegen` first when the job needs still frames, portraits, posters, or reference art, unless the user explicitly wants an inference.sh image app.
6. Capability-gate the CLI path with `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before trusting any cached schema.
7. Treat `belt app run` as external compute/spend. Do not run it until that cost is acceptable for this task.
8. Save project assets, prompt/input JSON, result JSON, and notes inside the workspace.
9. For long-running or batched jobs, use the async workflow below instead of blocking the whole pass.
10. If the asset is used in a web surface, hand it to `frontend-craft` and keep browser playback/visual QA as separate proof.

## Best Current Defaults

These defaults come from the upstream inference.sh skill snapshot at `c5ad36c`. Always verify live availability and schema with `belt app get <app>` before a run.

| Use Case | Default | Why |
| --- | --- | --- |
| Highest-quality general text-to-video | `google/veo-3-1` | Upstream names it the best-quality Veo path with frame interpolation |
| Fast text-to-video with optional audio | `google/veo-3-1-fast` | Good first choice for quick Veo generations |
| Fast/economical text-to-video or image-to-video | `pruna/p-video` | Fast, economical, audio support |
| Text/reference/image video with synchronized audio | `falai/seedance-2-t2v` / `falai/seedance-2-r2v` / `falai/seedance-2-i2v` | Seedance branch is the audio-aware option |
| Physical realism or natural-language video editing | `alibaba/happyhorse-1-0-t2v` / `alibaba/happyhorse-1-0-video-edit` | HappyHorse is the physical realism and edit branch |
| Talking head/avatar with built-in TTS | `pruna/p-video-avatar` | Fast avatar branch with voices/languages |
| Upscaling | `falai/topaz-video-upscaler` | Dedicated upscaling branch |
| Foley/sound effects | Discover live with `belt app search foley` and `belt app search sound` | No stable video Foley default is currently available; verify candidates before use |

## Model Map

Browse live apps with:

```bash
belt app list --category video
```

### Text To Video

| Model | App ID | Best For |
| --- | --- | --- |
| Veo 3.1 Fast | `google/veo-3-1-fast` | Fast, optional audio |
| Veo 3.1 | `google/veo-3-1` | Best quality, frame interpolation |
| Veo 3 | `google/veo-3` | High quality with audio |
| Veo 3 Fast | `google/veo-3-fast` | Fast with audio |
| Veo 2 | `google/veo-2` | Realistic videos |
| P-Video | `pruna/p-video` | Fast, economical, audio support |
| WAN-T2V | `pruna/wan-t2v` | Economical 480p/720p |
| Grok Video | `xai/grok-imagine-video` | xAI, configurable duration |
| Seedance 2 T2V | `falai/seedance-2-t2v` | Text-to-video with sync audio |
| Seedance 2 R2V | `falai/seedance-2-r2v` | Reference images/videos/audio to video |
| HappyHorse T2V | `alibaba/happyhorse-1-0-t2v` | Physical realism, up to 15s |

### Image To Video

| Model | App ID | Best For |
| --- | --- | --- |
| Wan 2.5 | `falai/wan-2-5` | Animate any image |
| Wan 2.5 I2V | `falai/wan-2-5-i2v` | High quality image-to-video |
| WAN-I2V | `pruna/wan-i2v` | Economical 480p/720p |
| P-Video | `pruna/p-video` | Fast image-to-video with audio |
| Seedance 2 I2V | `falai/seedance-2-i2v` | Animate images with sync audio |
| HappyHorse I2V | `alibaba/happyhorse-1-0-i2v` | Animate images, up to 1080P/15s |
| HappyHorse R2V | `alibaba/happyhorse-1-0-r2v` | Character-preserving references |

### Avatar, Editing, And Utilities

| Need | App ID | Best For |
| --- | --- | --- |
| P-Video-Avatar | `pruna/p-video-avatar` | Fast talking-head videos with built-in TTS |
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | Multi-character avatar videos |
| Fabric 1.0 | `falai/fabric-1-0` | Image talks with lipsync |
| PixVerse Lipsync | `falai/pixverse-lipsync` | Realistic lipsync |
| HappyHorse Edit | `alibaba/happyhorse-1-0-video-edit` | Natural-language video editing |
| Foley / sound effects | Discover with `belt app search foley` and `belt app search sound`; inspect candidates with `belt app get <app>` | App availability changes; do not assume a cached Foley app ID works |
| Topaz Upscaler | `falai/topaz-video-upscaler` | Upscale video quality |
| Media Merger | `infsh/media-merger` | Merge clips with transitions |

## Reference Routes

- CLI setup, commands, schemas, or generic inference.sh: `references/tools/infsh-cli.md`
- Google Veo: `references/tools/google-veo.md`
- Still image animation: `references/tools/image-to-video.md`
- Pruna P-Video or WAN fast/economical generation: `references/tools/p-video.md`
- Talking head, avatar, portrait animation, or lipsync: use `video-production:talking-head`; model details live in `references/tools/p-video-avatar.md` and `references/tools/ai-avatar-video.md`
- HappyHorse or physical realism/editing: `references/tools/happyhorse.md`
- Seedance, reference video, or audio-aware generation: `references/tools/seedance.md`
- Marketing or promo video: use `video-production:marketing`
- Explainer, tutorial, or product demo sequence: use `video-production:explainer`
- Storyboard or shot list: use `video-production:storyboard`
- Social/video ad specs: use `video-production:ad-spec`
- Prompt improvement: use the owning `video-production` method's prompting
  reference; if no artifact domain is known, load
  `references/prompting/video-prompting-guide.md`
- Shared artifact production workflow for domain video skills: `references/domain-production.md`
- Long-running jobs, batched tasks, timers, or delegated polling: `references/long-running-jobs.md`
- Copied-reference overrides and known stale app IDs: `references/reference-overrides.md`
- Multi-asset website/video pipelines with image, video, and Remotion: `frontend-craft/references/media-pipelines.md`
- Frontend implementation proof: `references/frontend-asset-qa.md`
- React/Remotion/code-rendered MP4: use `remotion` for code and `remotion-render` for inference.sh MP4 rendering

## Examples

```bash
mkdir -p output/video-generation/flower-timelapse
belt app run google/veo-3-1-fast \
  --input '{"prompt": "A timelapse of a flower blooming in a garden"}' \
  --save output/video-generation/flower-timelapse/result.json

mkdir -p output/video-generation/jazz-band
belt app run falai/seedance-2-t2v --input '{
  "prompt": "a jazz band performing in a dimly lit club",
  "generate_audio": true,
  "duration": 10
}' --save output/video-generation/jazz-band/result.json

mkdir -p output/video-generation/snowy-edit
belt app run alibaba/happyhorse-1-0-video-edit --input '{
  "video": "https://your-video.mp4",
  "prompt": "change the background to a snowy mountain landscape"
}' --save output/video-generation/snowy-edit/result.json

mkdir -p output/video-generation/product-avatar
belt app run pruna/p-video-avatar --input '{
  "image": "https://portrait.jpg",
  "voice_script": "Welcome to the product demo."
}' --save output/video-generation/product-avatar/result.json
```

## Async Workflow

Use async runs when there are multiple independent clips, expected runtime is long, or the main task can continue with layout, copy, or implementation work.

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
output/video-generation/<slug>/
  input.json
  result.json
  prompt.md
  final.mp4
  poster.png
  notes.md
```

Use the repo's existing asset directory instead when one already exists for the target app or site.

Return the final video path or remote result plus workspace copy plan, prompt/input JSON path, result JSON path, any still/reference asset paths, and QA evidence path or skipped-QA reason.
