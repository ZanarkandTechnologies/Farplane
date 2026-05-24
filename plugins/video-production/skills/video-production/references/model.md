# Video Production Model

Use this as the compact planning model for video production work.

## Algebra

```text
VideoProduction := Brief + Audience + ChannelPlan + SceneMatrix + MethodSet + AssetPlan + DeliveryPlan + ProofPlan

Deliverable := Job + Channel + Duration + Format + SourceAssets + ScriptOrPanel + AssetRoutes + DeliverySpecs + QA

VideoMethod := id + use_when + avoid_when + inputs + outputs + routing + risk + proof

MethodSelection(deliverable, methods, constraints) :=
  candidates = filter(methods, deliverable, constraints)
  chosen = advise(top3(candidates))
  deliverable.execution_packet = ExecutionPacket(deliverable, chosen)
```

## Scene / Deliverable Matrix

| Deliverable | Job | Channel | Duration | Format | Source assets | Method | Asset route | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Method Set

```text
video-production:marketing :=
  launch, promo, testimonial, UGC ad, product demo, brand story, or campaign
  creative

video-production:explainer :=
  how-it-works, onboarding, tutorial, feature spotlight, walkthrough, or
  narrated product explanation

video-production:storyboard :=
  shot list, visual script, panel board, animatic plan, continuity plan, or
  image-to-video motion test

video-production:talking-head :=
  avatar presenter, lipsync, AI spokesperson, portrait animation, course,
  testimonial, or social presenter clip

video-production:ad-spec :=
  platform-specific paid/social placement, safe zones, duration, captions,
  hook, CTA, and deliverable specs
```

## Method Selection Rule

Compare complete deliverable directions:

```text
Direction :=
  story job + channel + format + visual carrier + sound/voice + edit/pacing + CTA + proof
```

Use `advise` for material creative/production axes. Do not independently pick
the "best" hook, asset, music, edit, and CTA if they do not cohere as one
direction.

## Execution Packet

```text
ExecutionPacket :=
  deliverable_id
+ chosen_method
+ script_or_panel_steps
+ asset_routes
+ generation_route
+ delivery_specs
+ qa_assertions
+ publish_or_likeness_boundary
```

`video-production` owns story, deliverable, and method decisions.
`video-generation`, `remotion`, `remotion-render`, `image-generation`, and
`frontend-craft` own production routes when the packet needs them.
