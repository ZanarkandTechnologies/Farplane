---
name: ai-video-advisor
version: 1.1.0
description: "Turn model-native video create/edit/upscale requests into provider route, prompt/input packet, spend gate, and saved video asset bundle."
tier: 3
group: content-video
source: local
methods:
  - ai-video-advisor:visual-camera-control
template_uses:
  skill-template: "0.3.7"
eval: evals/evals.json
allowed-tools: Read, Grep, Glob, Bash
---

# AI Video Advisor

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

# AI Video Advisor Todos

Use this as the ordered checklist whenever `ai-video-advisor` is active.

- [ ] Classify the request as text-to-video, image-to-video, reference-to-video, avatar/lipsync execution, video edit, upscale, utility, prompt improvement, or frontend-bound asset.
- [ ] If the request is content ticket planning, idea plus Tasty Pack planning, storyboard/action-list compilation, React, Remotion, TSX-to-video, deterministic animation, or code-rendered MP4, stop using this skill and route to `content-impl-plan`, `storyboard`, `asset-advisor`, or `remotion` as appropriate.
- [ ] For CLI setup, app discovery, schemas, samples, or generic inference.sh help, load `references/tools/infsh-cli.md`.
- [ ] For vague/general AI video requests, model selection, "what should I use?", broad model-native video generation, video edits, upscaling, or utilities, use the model map in `SKILL.md` first.
- [ ] After `SKILL.md` selects a model family, load the matching specific reference instead of staying at the umbrella level.
- [ ] For Google Veo, load `references/tools/google-veo.md`.
- [ ] For still image animation, load `references/tools/image-to-video.md`.
- [ ] For Pruna/P-Video fast or economical generation, load `references/tools/p-video.md`.
- [ ] For talking head, avatar, persistent presenter, portrait animation, or lipsync direction, route to `avatar-advisor`; load `references/tools/p-video-avatar.md` or `references/tools/ai-avatar-video.md` only for model details or execution.
- [ ] For HappyHorse, physical realism, or video editing, load `references/tools/happyhorse.md`.
- [ ] For Seedance, reference video, or audio-aware generation, load `references/tools/seedance.md`.
- [ ] For marketing/proof videos, explainers, product demos, storyboard/action-list work, or idea plus Tasty Pack planning, use `content-impl-plan` or `storyboard` before this skill.
- [ ] For social/video ad specs, use `video-production:ad-spec`.
- [ ] For prompt improvement, use the owning `video-production` method's prompting reference; if no artifact domain is known, load `references/prompting/video-prompting-guide.md`.
- [ ] For annotated routes, arrows, maps, camera paths, landmark orbits, or multi-perspective location moves, load [visual camera control](references/visual-camera-control.md) and select single-shot versus chained-maneuver topology before spend.
- [ ] For shared production routing from a domain skill, load `references/domain-production.md`.
- [ ] For long-running or batched generations, load `references/long-running-jobs.md`; use `--no-wait`, task IDs, and `jobs.md` instead of terminal scrollback.
- [ ] Before copying commands from upstream references, load `references/reference-overrides.md` and let it override stale app examples.
- [ ] For website or campaign asset sets that combine stills, model-native clips, and Remotion renders, use `frontend-craft/references/media-pipelines.md`.
- [ ] Use `imagegen` first for still frames, portraits, posters, or reference art unless the user explicitly wants a CLI image app.
- [ ] Check `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before relying on an app schema.
- [ ] For voice, music, Foley, sound effects, dubbing, or mix planning, route to `audio-advisor`; search live with `belt app search foley` and `belt app search sound` only for provider execution details.
- [ ] For narrative multi-clip video, require the caller's generation topology
  before spend. Use start/end frame chaining for `continuous_chain`, require
  transition notes for `deliberate_scene_breaks`, and block isolated I2V
  batches unless the chosen format is explicitly `montage`.
- [ ] When a selected creative element conditions a clip, require its complete
  realization packet and bind both the resolved `goldenExample` asset and
  `goldenRecipe` prompt into the actual provider input. Record the element ID
  and target output duration in the generation receipt; block title-only or
  recipe-only handoffs.
- [ ] When `asset-advisor` routes `inspired_generation`, bind its rights-safe
  reference media, transferable composition/lighting/palette/material/camera
  traits, and must-not-copy constraints into the actual provider input and
  saved prompt packet. When it routes `original_generation`, preserve the
  evidenced no-reference or explicit-generation reason, rights/likeness note,
  output path, and acceptance check. Do not copy a reference's exact
  composition, identifiable likeness, signature, logo, or protected
  expression.
- [ ] When the caller has a master audio plan, set provider audio generation
  off where the live schema supports it, derive target clip duration/handles
  from the observed master duration and cue sheet, and record any exception by
  beat.
- [ ] Confirm external compute/spend is acceptable before any `belt app run`.
- [ ] Save final videos, prompts, input JSON, result JSON, and notes inside the workspace, not only in a remote URL, temp path, or Codex home path.
- [ ] If the video is used on a web surface, route implementation/proof through `frontend-craft`, `references/frontend-asset-qa.md`, and `visual-qa` when layout or taste is affected.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Generate project-ready AI video assets with inference.sh CLI (`belt`) while keeping provider-specific details in references.

Use the `SKILL.md` Todo List at the start of the pass. It is the ordered anti-forgetting checklist for model choice, reference loading, spend gates, asset saving, and frontend proof.

Use `content-impl-plan`, `storyboard`, `asset-advisor`, `avatar-advisor`, and
`audio-advisor` for artifact/product problems. Use this skill for model/app
selection and `belt` execution once the production intent and inputs are known.

For video prompt quality when no narrower artifact prompt applies, load `references/prompting/video-prompting-guide.md` for shot type, camera movement, lighting, temporal motion, and model-specific phrasing.

Do not use this skill for parent content planning, React/Remotion code
authoring, or code-to-video. Exit and use `content-impl-plan` for the parent
plan or `remotion` for authoring and local render proof.

Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from their Related Skills sections unless the user explicitly asks to install upstream skills.

## Steps

1. Classify the job: `text-to-video`, `image-to-video`, `reference-to-video`, `avatar-lipsync-execution`, `video-edit`, `upscale`, `utility`, `prompt-improvement`, or `frontend-bound`.
2. If the request is vague, use the model tables in this file to pick the app family.
3. Load `references/reference-overrides.md` before copying commands from any upstream reference.
4. Load the specific reference file only after a family is selected.
5. Use `imagegen` first when the job needs still frames, portraits, posters, or reference art, unless the user explicitly wants an inference.sh image app.
6. Capability-gate the CLI path with `command -v belt`, `belt --help`, `belt app get <app>`, and `belt app sample <app>` before trusting any cached schema.
7. Treat `belt app run` as external compute/spend. Do not run it until that cost is acceptable for this task.
8. Save project assets, prompt/input JSON, result JSON, and notes inside the workspace.
9. For long-running or batched jobs, use the async workflow below instead of blocking the whole pass.
10. If the asset is used in a web surface, hand it to `frontend-craft` and keep browser playback/visual QA as separate proof.

## Continuity Video Gate

Before running model-native clips for a storyboarded narrative, bind:

- `generation_topology`: `continuous_chain`, `deliberate_scene_breaks`, or
  `montage`.
- `frame_handoffs`: start image and end image for each chained clip, where clip
  N+1 starts from clip N's intended end frame.
- `identity_anchors`: character, prop, location, lighting, and style details
  that must survive across clips.
- `audio_policy`: `master_audio_in_remotion`, `provider_audio_per_clip`, or
  `silent_asset`; use `generate_audio:false` when the master mix owns the reel
  and the live provider schema supports it.

Block and route back to `content-impl-plan`, `storyboard`, `asset-advisor`, or
`audio-advisor` when a narrative reel asks for isolated pretty clips, mismatched
per-clip audio, or no continuity assets. Independent async batches are only
appropriate for montage, parallel asset exploration, or non-sequential b-roll.

## Visual Camera Control Gate

When annotations or a camera trajectory condition the clip, load
[visual camera control](references/visual-camera-control.md). Compile arrows and
diagrams into explicit path, altitude, orientation, gaze, speed, timing, and
terminal-state semantics. The diagram is never sufficient by itself.

Use one generation only for a bounded compatible move. Block an overloaded
single-shot run and choose chained maneuvers when the request contains three or
more independently scored camera states, a large landmark orbit, self-crossing
or reversing geometry, both high and low perspectives plus an exact terminal
view, or a prior single-shot adherence failure. Require start/end frame
handoffs and per-maneuver acceptance checks before external spend.

Before returning even a planning-only camera-control packet, choose the bundle
slug and name the exact `trajectory.json`, prompt/input, result, clip, and
`adherence.md` paths. Mark uncreated paths `planned`. Say `worked` or `pass`
only after the claimed files exist and the adherence evidence has been checked.

For chained maneuvers, generate and judge the hardest geometric move before
spending on the remaining clips. A real orbit requires camera translation
around a gaze-locked landmark; roll, spin, pan, and fly-by are not substitutes.
Score every maneuver `clear`, `partial`, or `absent`, and preserve failed clips
plus their adherence notes as regression evidence.
Any maneuver previously scored `partial` or `absent` gets its own clip and may
not be merged with an easier adjacent move during the retry.

Every camera-control response must make the selected method and proof state
machine-glanceable:

```text
camera_control_response:
  method: ai-video-advisor:visual-camera-control
  topology: single_shot | chained_maneuvers
  bundle_paths: exact created or planned paths; expand every clip; no wildcard placeholders
  clip_plan:
    - clip_id:
      maneuver_ids: []
      start_frame:
      end_frame:
      handoff_to:
      prompt_path:
      input_path:
      result_path:
      final_clip_path:
  maneuver_evidence:
    - maneuver_id:
      acceptance: observable geometry rule, including gaze and translation when relevant
      score_scale: [clear, partial, absent]
      score: pending | clear | partial | absent
      evidence_path:
      failed_clip_retention_path: predeclared for every maneuver
```

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
- Talking head, avatar, persistent presenter, portrait animation, or lipsync direction: use `avatar-advisor`; model details live in `references/tools/p-video-avatar.md` and `references/tools/ai-avatar-video.md`
- HappyHorse or physical realism/editing: `references/tools/happyhorse.md`
- Seedance, reference video, or audio-aware generation: `references/tools/seedance.md`
- Parent content ticket or idea plus Tasty Pack/reference plan: use `content-impl-plan`
- Storyboard, script, or shot list: use `storyboard`
- Asset inventory or recreation plan: use `asset-advisor`
- Audio direction, Foley, voice, music, SFX, dubbing, or mix plan: use `audio-advisor`
- Prompt improvement: use the owning `video-production` method's prompting
  reference; if no artifact domain is known, load
  `references/prompting/video-prompting-guide.md`
- Annotated camera routes, arrows, maps, landmark orbits, or multi-perspective
  movement: [visual camera control](references/visual-camera-control.md)
- Shared artifact production workflow for domain video skills: `references/domain-production.md`
- Long-running jobs, batched tasks, timers, or delegated polling: `references/long-running-jobs.md`
- Copied-reference overrides and known stale app IDs: `references/reference-overrides.md`
- Multi-asset website/video pipelines with image, video, and Remotion: `frontend-craft/references/media-pipelines.md`
- Frontend implementation proof: `references/frontend-asset-qa.md`
- React/Remotion/code-rendered MP4: use `remotion` for code and local render proof; use `remotion-render` only for an explicit external inference.sh render path

## Examples

```bash
mkdir -p output/ai-video-advisor/flower-timelapse
belt app run google/veo-3-1-fast \
  --input '{"prompt": "A timelapse of a flower blooming in a garden"}' \
  --save output/ai-video-advisor/flower-timelapse/result.json

mkdir -p output/ai-video-advisor/jazz-band
belt app run falai/seedance-2-t2v --input '{
  "prompt": "a jazz band performing in a dimly lit club",
  "generate_audio": true,
  "duration": 10
}' --save output/ai-video-advisor/jazz-band/result.json

mkdir -p output/ai-video-advisor/snowy-edit
belt app run alibaba/happyhorse-1-0-video-edit --input '{
  "video": "https://your-video.mp4",
  "prompt": "change the background to a snowy mountain landscape"
}' --save output/ai-video-advisor/snowy-edit/result.json

mkdir -p output/ai-video-advisor/product-avatar
belt app run pruna/p-video-avatar --input '{
  "image": "https://portrait.jpg",
  "voice_script": "Welcome to the product demo."
}' --save output/ai-video-advisor/product-avatar/result.json
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
output/ai-video-advisor/<slug>/
  input.json
  result.json
  prompt.md
  final.mp4
  poster.png
  notes.md
  trajectory.json   # when visual-camera-control is active
  adherence.md      # when visual-camera-control is active
```

Use the repo's existing asset directory instead when one already exists for the target app or site.

Return the final video path or remote result plus workspace copy plan, prompt/input JSON path, result JSON path, any still/reference asset paths, and QA evidence path or skipped-QA reason.

For planning-only outputs, return the same exact bundle paths with
`status: planned`; do not imply that generation or adherence proof already
exists.
