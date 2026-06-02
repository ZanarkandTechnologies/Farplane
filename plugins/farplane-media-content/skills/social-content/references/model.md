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

social-content:twitter-thread :=
  X/Twitter hook tweet, thread, quote-post, reply chain, or media-supported
  thread
```

## Method Selection Rule

Compare complete artifact directions:

```text
Direction :=
  platform + format + hook/copy posture + asset carrier + CTA + proof + publish boundary
```

Use `advise` when the format, platform mix, hook, asset route, or CTA is a real
choice. Do not advise isolated wording details when the direction is already
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

`social-content` owns the artifact decision. `image-generation`,
`video-generation`, `remotion`, `remotion-render`, and `frontend-craft` own
production routes when the packet needs them.
