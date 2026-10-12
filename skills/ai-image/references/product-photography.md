# Product Photography

Owner: [ai-image](../SKILL.md) `product` mode. Load when the request is a
product hero, packshot, lifestyle, detail, marketplace set, or product cutout.
Folded from the former product-photography skill (model, method smoke, and two
upstream guides).

## Model

```text
ProductPhotography := ProductFacts + Channel + ShotMatrix + ShotKind + AssetRoute + ProofPlan

Shot := Job + Channel + AspectRatio + Background + SourceAsset + GenerationRoute + Output + QA

ShotSelection(shot, kinds, constraints) :=
  candidates = filter(kinds, shot, constraints)
  chosen = recommend(top3(candidates))
  shot.execution_packet = ExecutionPacket(shot, chosen)
```

Build the shot matrix before any paid call:

| Shot | Job | Channel | Aspect ratio | Background | Source asset | Kind | Route | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Shot Kinds

| Kind | Use for |
| --- | --- |
| `hero` | Product-page hero, ad hero, campaign key visual |
| `packshot` | Clean product-only, catalog, SKU variant, white or plain background |
| `lifestyle` | In-use, contextual, model or environment, aspirational scene |
| `detail` | Close-up, feature, texture or material, scale, comparison, callout |
| `marketplace` | Amazon, Shopify, or listing set with channel dimensions and compliance |
| `cutout-upscale` | Background removal, isolation, transparent cutout, cleanup, upscale |

Pick one primary kind. Add supporting kinds only when the shot set really spans
jobs. When background, realism, source route, or channel is a material choice,
compare the viable directions inline and recommend one:

```text
Direction := shot job + channel + background/style + source asset route
           + generation/postprocess route + proof + handoff
```

## Execution Packet

```text
ExecutionPacket := shot_id + kind + required_inputs + prompt_or_edit_steps
                 + generation_route + postprocess_route + handoff
                 + qa_assertions + upload_boundary
```

- A real product photo plus a scene change is an **edit**: Ideogram 4.5 Precise
  Edit, never a fresh generation that redraws the product.
- A fresh generation may not reproduce the real label, logo, or packaging text.
  Composite the real packshot or label onto the generated scene, or edit the
  real photo; do not ship model-drawn product text.
- Cutouts and upscales go through `belt` (BiRefNet, Topaz); see
  [background-removal](tools/background-removal.md) and
  [image-upscaling](tools/image-upscaling.md).
- Product-page or frontend integration hands the receipt to
  [impl-plan](../../impl-plan/SKILL.md).
- No upload, publish, or store-listing change unless the operator asks for it.

## Routing Smoke Cases

| Input | Primary kind | Supporting |
| --- | --- | --- |
| "Create the main product-page hero image." | `hero` | |
| "Make clean SKU images on white for the catalog." | `packshot` | |
| "Show the bottle in a bathroom scene with natural light." | `lifestyle` | |
| "Generate closeups of the texture and cap details." | `detail` | |
| "Plan an Amazon listing image set." | `marketplace` | |
| "Remove the background and upscale this product photo." | `cutout-upscale` | |
| "Amazon listing with hero, detail, and lifestyle images." | `marketplace` | `hero`, `detail`, `lifestyle` |
| "Product-page hero from a cutout source image." | `hero` | `cutout-upscale` |

Negative controls:

- Do not choose `marketplace` for a generic hero unless a listing channel is required.
- Do not claim commercial or marketplace compliance without visual and channel proof.

## Upstream Guides

Read-only copies of the inference.sh guides; load only when shot conventions,
marketplace constraints, or prompt patterns matter.

- [Commerce conventions](product-photography-upstream-commerce.md): shot types,
  angles, backgrounds, shadows, lighting, e-commerce and Amazon requirements.
- [AI product photography](product-photography-upstream-ai.md): model examples,
  commercial styles, and generation workflows.

Their `belt` commands are examples; the default paid route is still `treg` for
generation and Ideogram for edits.
