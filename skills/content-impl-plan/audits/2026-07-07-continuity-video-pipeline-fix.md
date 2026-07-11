---
title: Continuity Video Pipeline Skill Fix
date: 2026-07-07
owner: content-impl-plan
status: implemented
---

# Continuity Video Pipeline Skill Fix

## Failure

The founder launch reel pipeline treated a Tasty Pack as visual inspiration,
then generated isolated model-native clips and stitched them. The result lost
the reference's story engine, recurring character, audio spine, and clip-to-clip
continuity. Remotion also assumed clip timing instead of proving frame counts,
which caused visible boundary stutter.

## Skill Ownership

| Failure mode | Owning skill | Required fix |
| --- | --- | --- |
| Tasty Pack used as vibes instead of structure | `content-impl-plan` | Require reference classification, rejected nearby formats, and `reference_leverage_map` tied to shots/assets/audio/motion/story beats. |
| No coherent story or standout recurring character | `storyboard` | Require viewer question -> answer, continuity spine, recurring character/object or explicit rationale, and connected beats. |
| Concept frames were not production-continuity assets | `asset-advisor` | Require character/object bibles, location/lighting anchors, and start/end frame assets for model-native clip handoffs. |
| Audio varied per generated clip | `audio-advisor` | Require one master VO/music/SFX spine for multi-clip narrative reels and disable provider audio unless justified by beat. |
| Seedance jobs were isolated | `ai-video-advisor` | Require `generation_topology` before spend; use start/end frame chaining for `continuous_chain`; block isolated I2V unless montage. |
| Stitched output stuttered | `remotion` | Probe clip fps/duration/frame count, use observed frame counts for `Sequence`, prefer `OffthreadVideo`, and verify final audio placement. |

## Eval Coverage Added

- `content_impl_plan_continuity_video_gate_01`
- `storyboard_connected_frames_for_ai_video_01`
- `asset_advisor_continuity_asset_graph_01`
- `audio_advisor_master_spine_for_multiclip_reel_01`
- `ai_video_advisor_blocks_isolated_i2v_for_narrative_01`
- `remotion_stitched_clips_frame_audio_qa_01`

## Expected Pipeline

```text
content_impl_plan(idea, tasty_pack)
  -> reference_classification
  -> story + continuity + generation_topology
  -> storyboard connected frame pairs
  -> asset continuity graph
  -> master audio spine
  -> ai-video start/end chained clips
  -> remotion exact-frame stitch + final mix
  -> review/qa evidence
```

The blocked path is:

```text
tasty_pack -> isolated keyframes -> isolated AI video clips -> concat -> done
```
