---
name: video-generation
version: 1.0.0
description: Generate or edit AI video assets with inference.sh `belt` video apps, using the broad AI-video model map plus Codexter's workspace, spend-gate, and frontend QA rules. Covers Google Veo, Seedance 2.0, HappyHorse, Wan, Grok, P-Video, avatar/lipsync, image-to-video, video editing, foley, upscaling, social media videos, marketing clips, explainer videos, product demos, and frontend-bound video assets. Route React/Remotion code-to-video requests to `remotion-render` instead.
allowed-tools: Read, Grep, Glob, Bash
---

# Video Generation

Generate project-ready AI video assets with inference.sh CLI (`belt`) while keeping provider-specific details in references.

Use `todos.md` at the start of the pass. It is the ordered anti-forgetting checklist for model choice, reference loading, spend gates, asset saving, and frontend proof.

Do not use this skill for React/Remotion code-to-video. Exit and use `remotion-render`.

## Steps

1. Classify the job: `text-to-video`, `image-to-video`, `reference-to-video`, `avatar-lipsync`, `video-edit`, `utility`, `marketing`, `explainer`, `storyboard`, `ad-spec`, `prompt-improvement`, or `frontend-bound`.
2. If the request is vague, use the model tables in this file to pick the app family.
3. Load the specific reference file only after a family is selected.
4. Use `imagegen` first when the job needs still frames, portraits, posters, or reference art, unless the user explicitly wants an inference.sh image app.
5. Capability-gate the CLI path with `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before trusting any cached schema.
6. Treat `belt app run` as external compute/spend. Do not run it until that cost is acceptable for this task.
7. Save project assets, prompt/input JSON, result JSON, and notes inside the workspace.
8. If the asset is used in a web surface, hand it to `frontend-craft` and keep browser playback/visual QA as separate proof.

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
| Foley/sound effects | `infsh/hunyuanvideo-foley` | Dedicated sound-effects branch |

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
| HunyuanVideo Foley | `infsh/hunyuanvideo-foley` | Add sound effects |
| Topaz Upscaler | `falai/topaz-video-upscaler` | Upscale video quality |
| Media Merger | `infsh/media-merger` | Merge clips with transitions |

## Reference Routes

- CLI setup, commands, schemas, or generic inference.sh: `references/tools/infsh-cli.md`
- Google Veo: `references/tools/google-veo.md`
- Still image animation: `references/tools/image-to-video.md`
- Pruna P-Video or WAN fast/economical generation: `references/tools/p-video.md`
- Talking head, avatar, portrait animation, or lipsync: `references/tools/p-video-avatar.md`, `references/tools/ai-avatar-video.md`, and `references/guides/talking-head-production.md`
- HappyHorse or physical realism/editing: `references/tools/happyhorse.md`
- Seedance, reference video, or audio-aware generation: `references/tools/seedance.md`
- Marketing or promo video: `references/guides/ai-marketing-videos.md`
- Explainer, tutorial, or product demo sequence: `references/guides/explainer-video-guide.md`
- Storyboard or shot list: `references/guides/storyboard-creation.md`
- Social/video ad specs: `references/guides/video-ad-specs.md`
- Prompt improvement: `references/guides/video-prompting-guide.md`
- Frontend implementation proof: `references/frontend-asset-qa.md`
- React/Remotion/code-rendered MP4: use `remotion-render`

## Examples

```bash
belt app run google/veo-3-1-fast --input '{"prompt": "A timelapse of a flower blooming in a garden"}'

belt app run falai/seedance-2-t2v --input '{
  "prompt": "a jazz band performing in a dimly lit club",
  "generate_audio": true,
  "duration": 10
}'

belt app run alibaba/happyhorse-1-0-video-edit --input '{
  "video": "https://your-video.mp4",
  "prompt": "change the background to a snowy mountain landscape"
}'

belt app run pruna/p-video-avatar --input '{
  "image": "https://portrait.jpg",
  "voice_script": "Welcome to the product demo."
}'
```

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
