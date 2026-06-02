# Product Photography Method Selection Smoke

Use this as a text smoke fixture for product-photo method routing.

## Positive Cases

| Input | Expected method | Why |
| --- | --- | --- |
| "Create the main product-page hero image." | `product-photography:hero` | Primary key visual is the job. |
| "Make clean SKU images on white for the catalog." | `product-photography:packshot` | Product-only catalog images are primary. |
| "Show the bottle in a bathroom scene with natural light." | `product-photography:lifestyle` | Contextual in-use scene is primary. |
| "Generate closeups of the texture and cap details." | `product-photography:detail` | Feature/detail proof is primary. |
| "Plan an Amazon listing image set." | `product-photography:marketplace` | Channel-specific listing set and proof are primary. |
| "Remove the background and upscale this product photo." | `product-photography:cutout-upscale` | Isolation/postprocess job is primary. |

## Supporting Method Cases

| Input | Primary | Supporting | Why |
| --- | --- | --- | --- |
| "Amazon listing with hero, detail, and lifestyle images." | `product-photography:marketplace` | `product-photography:hero`, `product-photography:detail`, `product-photography:lifestyle` | Marketplace owns deliverable set; shot methods support rows. |
| "Product-page hero from a cutout source image." | `product-photography:hero` | `product-photography:cutout-upscale` | Hero owns visual job; cutout/upscale owns source prep. |

## Negative Controls

- Do not choose `product-photography:marketplace` for a generic hero unless a
  marketplace or listing channel is required.
- Do not claim commercial or marketplace compliance without visual/channel
  proof.
- Do not upload, publish, or change store listings unless the user explicitly
  asks for that action.
