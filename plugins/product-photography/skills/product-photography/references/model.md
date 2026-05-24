# Product Photography Model

Use this as the compact planning model for product photography and generated
commerce imagery.

## Algebra

```text
ProductPhotography := ProductFacts + Channel + ShotMatrix + MethodSet + AssetRoute + ProofPlan

Shot := Job + Channel + AspectRatio + Background + SourceAsset + GenerationRoute + Output + QA

ProductPhotoMethod := id + use_when + avoid_when + inputs + outputs + commerce_constraints + proof

MethodSelection(shot, methods, constraints) :=
  candidates = filter(methods, shot, constraints)
  chosen = advise(top3(candidates))
  shot.execution_packet = ExecutionPacket(shot, chosen)
```

## Shot Matrix

| Shot | Job | Channel | Aspect ratio | Background | Source asset | Method | Route | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Method Set

```text
product-photography:hero :=
  primary product hero, ad hero, product-page hero, or campaign key visual

product-photography:packshot :=
  clean product-only image, catalog image, SKU variant, white/background
  standard image

product-photography:lifestyle :=
  in-use, contextual, model/environment, aspirational, or scene-based shot

product-photography:detail :=
  close-up, feature detail, texture/material, scale, comparison, or callout

product-photography:marketplace :=
  Amazon, Shopify, marketplace listing set, channel-specific dimensions,
  compliance, and proof

product-photography:cutout-upscale :=
  background removal, isolation, transparent cutout, cleanup, upscale, or
  postprocess
```

## Method Selection Rule

Compare complete shot directions:

```text
Direction :=
  shot job + channel + background/style + source asset route + generation/postprocess route + proof + handoff
```

Use `advise` when shot set, style, background, realism, source asset route, or
channel handoff is a material choice.

## Execution Packet

```text
ExecutionPacket :=
  shot_id
+ chosen_method
+ required_inputs
+ prompt_or_edit_steps
+ generation_route
+ postprocess_route
+ handoff
+ qa_assertions
+ upload_boundary
```

`product-photography` owns shot selection. `imagegen`, `image-generation`, and
`frontend-craft` own production/integration routes when the packet needs them.
