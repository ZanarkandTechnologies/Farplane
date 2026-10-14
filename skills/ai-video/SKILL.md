---
name: ai-video
description: "Use for \"make a video clip\", \"animate this image\", \"make an avatar video\" or \"generate a voiceover\": provider route, prompt, spend quote and a saved, inspected clip or audio file."
source: local
department: marketing
methods:
  - {id: "ai-video:clip", class: artifact, output: video-clip-bundle}
  - {id: "ai-video:avatar", class: artifact, output: presenter-clip-bundle}
  - {id: "ai-video:audio", class: artifact, output: audio-asset-bundle}
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# AI Video

## Context

Use this when the operator wants a model-generated video clip, a persistent
presenter or lipsync clip, or an audio asset (voice, music, SFX). One pass
returns a generated, inspected file saved with its route, prompt, and spend
receipt.

It does not make stills, posters, or start/end frames
([ai-image](../ai-image/SKILL.md)), write scripts, scenes, or asset plans
([storyboard](../storyboard/SKILL.md)), or compose, caption, mix, and render
the final video (HyperFrames, `/hyperframes`). Nothing is published here.

## Skill Signature

```text
ai_video(request, mode?: clip | avatar | audio, storyboard_or_script?, refs?, timing_master?, budget?)
  -> asset_bundle { final file + prompt.md + input.json + result.json + receipt.md } | blocked_report
reads: the request, storyboard or scene packets, reference media, live provider catalog (treg)
does: picks the mode, fixes continuity topology, quotes the price, generates, inspects frames or audio
writes: the caller's asset path, else .farplane/ai-video/<date>-<slug>/; the spend line in the operator's spend log
returns: accepted file paths, spend receipt, adherence or QA notes, and the next owner
```

## Modes

| Mode | For | Detail |
| --- | --- | --- |
| `clip` | text/image/reference-to-video, video edit, upscale, camera moves | [providers](references/providers.md), [camera control](references/visual-camera-control.md) |
| `avatar` | persistent presenter, character, likeness, lipsync | [avatar](references/avatar.md) |
| `audio` | voice, music, SFX, Foley, dubbing audio | [audio](references/audio.md) |

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the job and pick the mode.**
  `request -> mode + inputs + bundle path | route out | blocked_report`

  Rule: Classify the request as `clip`, `avatar`, or `audio`. Route stills to
  ai-image, script or scene design to storyboard, and composition, captions,
  or final render to HyperFrames. In `avatar` mode, a real person's face or
  voice needs a recorded consent note (who, what use, where); without it,
  return `blocked_report`. Choose the bundle slug now.

  Example: `"make this founder photo say our launch script", no consent note -> blocked_report naming the missing consent`

  Assert:
  - A supplied photo of a real person is never treated as consent.
  - The bundle path is named before any provider call.
- [ ] **N2 — Fix the continuity topology before spend.**
  `clips + storyboard -> generation_topology + frame handoffs | back to storyboard`

  Rule: For more than one clip, set `generation_topology` to
  `continuous_chain`, `deliberate_scene_breaks`, or `montage`. In a chain,
  clip N+1 starts from clip N's end frame. Split a shot into chained shots once
  it has three or more camera states (also a large orbit, reversal, or a
  prior adherence failure) and load
  [camera control](references/visual-camera-control.md). Scene breaks need the
  approved Storyboard scene-grid packet and matching character references.
  Missing anchors go back to storyboard or ai-image, not to isolated clips.

  Example: `six keyframes for one narrated reel -> continuous_chain, 6 handoffs, not 6 independent image-to-video runs`

  Assert:
  - Independent batches are used only for montage or exploration.
  - Every chained clip names its start frame and its end frame.
- [ ] **N3 — Choose the provider and quote the price.**
  `job -> provider listing + price quote | fallback route`

  Rule: Paid video and avatar models go through treg: `catalog_search` by job,
  `catalog_get` for parameters, price, and reliability, then `call`. Default
  families are in [providers](references/providers.md) (Seedance 2.5, Veo,
  Wan). Audio defaults: Fish Audio for voice, ElevenLabs for music; for a
  common SFX, search SoundButtonsWorld first and never download from it
  (reference and listen only). Quote the price, stay within the operator's
  weekly cap, and log the spend. `belt` and direct-provider tools are
  fallbacks with a recorded reason.

  Assert:
  - The quote is stated before the call, and the call stays inside the cap.
  - No common SFX is generated before candidate discovery and an operator decision.
- [ ] **N4 — Compile and save the prompt packet.**
  `mode + topology + listing -> prompt.md + input.json`

  Rule: Write one geometric or performance job per clip using the
  [prompting guide](references/prompting/video-prompting-guide.md). Set
  `generate_audio: false` when a master mix owns the audio. Arrows, IDs, and
  panel labels are instruction-only and must not appear as pixels. Bind a
  selected creative element's golden example and recipe, or rights-safe
  reference traits, into the actual input. Save both files before calling.

  Assert:
  - The live schema was checked for end frame, references, duration, and audio switch.
  - `input.json` matches what is sent.
- [ ] **N5 — Generate, poll, and download.**
  `packet -> job id -> local file | failed attempt`

  Rule: In a chain, generate and judge the hardest move first. Record each job
  ID in `jobs.md` and poll with backoff
  ([long-running jobs](references/long-running-jobs.md)). A provider job ID is
  not an accepted file: download the media into the bundle.

  Assert:
  - Every final file exists locally, not only as a remote URL.
- [ ] **N6 — Inspect before acceptance.**
  `local file -> frames or audio checks -> accept | retry | fail`

  Rule: Extract frames (first, last, every cue) into a contact sheet and look
  at them: identity drift, annotation leakage, hands, text, and camera
  adherence scored `clear`, `partial`, or `absent`. For audio, probe duration
  and format and listen at the start, end, and cue points. Keep failed clips
  and their notes as regression evidence.

  Assert:
  - No file is called accepted without inspected frames or audio.
  - A beautiful clip that misses a required move is a failure.
- [ ] **N7 — Return the receipt and hand off.**
  `accepted files -> receipt + spend line + next owner`

  Rule: Write `receipt.md` with route, model, prompt path, job ID, price,
  observed duration, and acceptance notes; add the spend line. Hand clips and
  audio to HyperFrames for composition; for a web surface, hand the receipt to
  `impl-plan` with [frontend asset QA](references/frontend-asset-qa.md).

  Assert:
  - Planned paths stay marked `planned`; `worked` needs files that exist.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Clip N+1 starts from clip N's end frame; when the schema has no end-frame
  field, extract clip N's last frame and record that substitution.
- `generate_audio: false` whenever a master mix owns the audio; mismatched
  per-clip audio breaks a narrative reel.
- Three or more camera states in one shot means chained shots; an orbit is
  camera translation around a gaze-locked landmark, never roll, spin, or pan.
- SoundButtonsWorld is reference and listening only: link item pages, never
  download, never automate its search, never treat availability as a license.
- Real-person likeness or voice needs a recorded consent note; private voice
  IDs and credentials never go into packets, receipts, or tracked files.
- A provider job ID, remote URL, or "succeeded" status is not an accepted file.
- A break-the-frame plate (pop-out band, object over captions) is generated on
  flat chroma green `#00B140` with the object fully in frame; HyperFrames'
  remove-background is a person matte and will not cut out a ball or prop.
- Copied `tools/` docs describe the `belt` fallback; [reference
  overrides](references/reference-overrides.md) and live checks win.

## Reference Map

- [providers](references/providers.md) - N3: treg route, current model map,
  price check, `belt` fallback and `tools/` index.
- [camera control](references/visual-camera-control.md) - N2/N6: arrows, maps,
  orbits, chained maneuvers, adherence scoring;
  [worked example](examples/visual-camera-control/example.md).
- [avatar](references/avatar.md) - avatar mode: consent, persistence, beat map.
- [audio](references/audio.md) - audio mode: cue spine, SoundButtonsWorld,
  Fish/ElevenLabs packets, scripts;
  [packet example](examples/explainer-audio-packet/example.md).
- [prompting guide](references/prompting/video-prompting-guide.md) - N4.
- [long-running jobs](references/long-running-jobs.md) - N5 batches and polling.
- [domain production](references/domain-production.md) - shared save and routing rules.
- [web surface](references/web-surface-integration.md) and
  [frontend asset QA](references/frontend-asset-qa.md) - N7 web handoff.
- [reference overrides](references/reference-overrides.md) - before copying `belt` commands.
- [asset plan](../storyboard/references/asset-plan.md) - when reference
  assets or rights are missing.

## Output

```yaml
mode: clip | avatar | audio
status: accepted | partial | failed | planned | blocked
bundle: <caller asset path or .farplane/ai-video/<date>-<slug>/>
files: {final: <path>, prompt: prompt.md, input: input.json, result: result.json, receipt: receipt.md, contact_sheet: <path>}
topology: single_shot | continuous_chain | deliberate_scene_breaks | montage | chained_maneuvers
route: <treg listing or fallback + reason>
spend: <quoted USD, actual USD, spend-log line>
inspection: <frames or audio checked, adherence scores, failures kept>
consent: <note ref | not_applicable | missing>
next_owner: hyperframes | impl-plan | storyboard | ai-image | none
```
