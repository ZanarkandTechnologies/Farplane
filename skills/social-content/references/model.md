# Social Content Model

Use this as the compact planning model for social content and campaign work.

## Algebra

```text
SocialContent := Brief + PlatformSet + ArtifactMatrix + MethodSet + AssetPlan + ProofPlan

Artifact := Platform + Format + Audience + MessageJob + CopyPayload + AssetCarrier + PublishBoundary + QA

SocialMethod := id + use_when + avoid_when + platform_constraints + asset_route + proof

MethodSelection(artifact, methods, constraints) :=
  candidates = filter(methods, artifact, constraints)
  chosen = advise(top3(candidates))
  artifact.execution_packet = ExecutionPacket(artifact, chosen)
```

## Artifact Matrix

| Artifact | Platform | Format | Message job | Copy payload | Asset carrier | Publish boundary | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Method Set

```text
social-content:cross-platform :=
  multi-platform campaign bundle, content calendar, captions, thumbnails,
  UGC concepts, or broad platform adaptation

social-content:carousel :=
  slide sequence, educational carousel, announcement carousel, case-study
  carousel, or multi-slide visual asset

social-content:linkedin :=
  professional/founder/B2B voice, hiring post, thought leadership,
  LinkedIn-native post, or LinkedIn carousel adaptation

social-content:x :=
  X post, thread, quote-post, or reply chain as a numbered tweet stack

social-content:newsletter :=
  recurring newsletter issue or newsletter blueprint from verified material
```

## Method Selection Rule

Compare complete artifact directions:

```text
Direction :=
  platform + format + hook/copy posture + asset carrier + CTA + proof + publish boundary
```

Compare the viable format, platform mix, hook, asset route, or CTA options
inline when the choice is real. Do not revisit isolated wording details when the direction is already
settled.

## Execution Packet

```text
ExecutionPacket :=
  artifact_id
+ chosen_method
+ platform_specs
+ copy_steps
+ asset_route
+ publish_boundary
+ qa_assertions
```

`social-content` owns the selected social artifact decision across all modes
(`x`, `linkedin`, `carousel`, `cross-platform`, `newsletter`).
[ai-image](../../ai-image/SKILL.md), [ai-video](../../ai-video/SKILL.md),
[storyboard](../../storyboard/SKILL.md), [copywriting](../../copywriting/SKILL.md)
and [impl-plan](../../impl-plan/SKILL.md) own production routes when the packet
needs them; [zernio](../../zernio/SKILL.md) owns posting and scheduling.
