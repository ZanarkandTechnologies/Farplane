# Resource Bank Contract

## Source Of Truth

Use the Farplane UI Resource Bank module as the backing store unless the
operator supplies another vault:

- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI/convex/modules/resourceBank/AGENTS.md`
- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI/convex/modules/resourceBank/schema.ts`
- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI/convex/modules/resourceBank/validators.ts`

## Active Contract

Resource Bank is a compact capture store whose creative elements are complete
production capsules, not an evidence vault or recipe database.

```text
ResourceBankCapture {
  source: string
  note?: string
  focus?: string
  transcriptText?: string
  analysisMarkdown: string
  elements: CreativeElement[]
  tags?: string[]
  facets?: {
    outputTypes?: string[]
    audiences?: string[]
    ageRanges?: string[]
    industries?: string[]
    customerRoles?: string[]
    projectId?: string
    taskId?: string
    tastinessScore?: number
  }
}

CreativeElement {
  kind: format | storyboard | visual | character | audio | editing
  title: string
  description: string
  whyItWorks: string
  goldenExample: {
    assetId: ResourceBankAssetId
    description?: string
  }
  goldenRecipe: string
  anchor?: string
  pinned: true
}
```

`whyItWorks` and `goldenRecipe` are required non-empty strings.
`goldenExample.assetId` must resolve to one asset created by the same ingestion
job as the element. Its optional description identifies the exact frame,
passage, voice, layout, caption timing, or quality worth conditioning on. The
primary source asset is valid when it is the clearest example and the
description is precise; a derived frame, contact sheet, audio, or transcript
asset is preferred when it grounds the element better.

Use `is_element(value) = independently selectable && independently
conditionable from an example && owned by a recognizable production step`.
Do not add `hook`, `copy`, `constraint`, `director`, `layout`, or `pacing`
kinds, element start/end timing, recipe collections, required-input/success-
criteria/production-hint objects, profile tables, or separate
production-pattern records. Hook folds into the storyboard opening beat;
semantic copy folds into storyboard; subtitle rendering/timing folds into
editing; constraints are production policy or Brand Kit prompt content, not
CreativeElement rows.

Storage-backed preview assets are allowed when another ingest phase produced a
real visual. They remain Resource Bank assets; a complete element may reference
one through `goldenExample.assetId`, but Tasty Pack does not add a parallel
preview/evidence collection.

## Retrieval Fields

Use facets only for things the operator will filter, group, or pack by:

- `outputTypes`: examples `reel`, `short-video`, `landing-page`, `thumbnail`.
- `audiences`: examples `founders`, `operators`, `students`, `creators`.
- `ageRanges`: examples `18-24`, `25-34`, `35-44`.
- `industries`: examples `ai`, `saas`, `education`, `finance`.
- `customerRoles`: examples `founder`, `marketer`, `engineer`, `buyer`.
- `tastinessScore`: optional 0-1-ish operator or agent confidence that this is
  a high-value reference.

`tastinessScore` is capture-level priority: "is this whole source worth
retrieving?" Every active CreativeElement is selected reuse intent and is
stored with `pinned: true`. Tasty Pack
retrieval reports pinned counts, operator-note counts, and direct warnings in
`meta`, but numeric weights are not stored on creative elements.

Keep `tags` lightweight and freeform for style, subject, project, and recall.
Do not create managed tag families for hook/open-loop/pacing/retention unless a
later UI or query path proves the need.

## Analysis Shape

Store analysis as one source-agnostic Markdown field:

```text
analysisMarkdown: """
## Breakdown
What the source is and the useful observed parts.

## Why It Works
Why it caught attention or matters.

## Reuse Notes
What to borrow at pattern level and what not to copy literally.
"""
transcriptText?: string
```

The headings are a writing default, not a database schema. This contract works
for videos, posts, websites, landing pages, screenshots, files, and notes.
Keep a real transcript in its own optional field so consumers can fetch it
without parsing prose. The analysis may preserve unselected observations and
whole-source context, but it cannot substitute for the element-level
`description`, `whyItWorks`, `goldenExample`, or `goldenRecipe` required when a
component is actually promoted into `elements[]`.

```text
should_store_element(value, note)
  = is_element(value)
    && explicitly_selected_for_reuse(value, note)
```

Create a CreativeElement only when the operator explicitly likes, selects, or
asks to reuse that component. Store other observations in analysis rather than
as unpinned context elements. A capture may contain zero elements.

## Creative Element Guidance

Use compact elements. Prefer several precise elements over one large summary.

- `format`: platform/content format or repeatable wrapper.
- `storyboard`: opening attention beat, semantic copy move, scene, narrative
  move, or structure.
- `visual`: art direction, object, setting, layout, frame idea, or asset style.
- `character`: distinctive persona, archetype, guide, host, mascot, recurring
  voice, or character system that makes the reference reusable.
- `audio`: voice, recognized music, SFX, silence, or sonic pattern.
- `editing`: pacing, transition, subtitle rendering/timing, caption rhythm,
  motion, or cut pattern.

Keep layout semantics inside `visual`, narrative pacing and semantic copy
inside `storyboard`, subtitle rendering/timing and cut rhythm inside `editing`,
and vocal pacing inside `audio`. The accepted six kinds are sufficient; do not
introduce a director-like kind.

For each element:

- `description` says what it is;
- `whyItWorks` names the mechanism and audience effect;
- `goldenExample` names one same-source asset and optionally the exact quality
  to inspect;
- `goldenRecipe` is one rights-safe prompt that recreates the function.

Recipes must be operational and kind-specific. A visual recipe should specify
composition/material/light or layout behavior; an audio recipe should specify
voice/music/SFX role and sonic behavior; storyboard recipes should specify the
opening hook, beat, narrative, or language mechanics; editing recipes should
specify subtitle, caption, transition, motion, rhythm, or cut mechanics. Do not
copy one generic recipe across unrelated kinds or merely restate the
description.

Use `anchor` for lightweight grounding such as `0-3s`, `opening frame`,
`voiceover`, `caption`, `cutaway`, `end card`, or `operator note`. If the
source could not be inspected deeply, state that in analysis and keep element
anchors honest.

Active writes create elements only for liked, selected, or operator-highlighted
sub-elements and therefore require `pinned: true`, preferably backed by the
operator note. Unpinned rows may still be read as legacy/external violations;
they are not a valid new-write context model. Do not ask for or store numeric
creative-element weights. Do not add a separate `production_pattern` object; the
reference pattern emerges from the element list. This applies across reels,
landing pages, posts, screenshots, and notes.

For `character` elements, describe the reusable role and behavior rather than
copying protected expression: e.g. "deadpan technical guide who translates
abstract infrastructure into a dry office ritual." When the source character
resembles a real person, actor performance, brand mascot, or protected
fictional character, record rights-safe remix policy in analysis or Brand Kit
prompt text: preserve archetype, function, contrast, and emotional job; avoid
copying likeness, name, exact wardrobe, voice, catchphrases, source frames,
logos, or branded presentation.

For recognized music, use the artist/title/link as attribution and research
context. The reusable element is the sonic role: tempo, energy, instrument
palette, mood, edit function, or contrast with the visuals. Pair it with a
production-policy note for future creation: do not reuse protected source
music unless licensed; recreate the function with cleared, original, or
generated audio.

## Tasty Pack Shape

Tasty Pack / Inspiration Pack retrieval should return clean captures:

```text
createTastyPack(request) -> {
  request: { idea?, timeframe, startAtMs?, endAtMs?, filters },
  captures: [
    {
      captureId,
      source,
      transcript?,
      analysis: { operatorNote?, markdown },
      elements
    }
  ],
  meta: { captureCount: number, timeframe: string }
}
```

Core consumer fields are `captures[].source`, optional `captures[].transcript`,
`captures[].analysis.markdown`, complete
`captures[].elements`, and direct `meta` counts/warnings such as
`pinnedElementCount`, `operatorNoteCount`, and `warnings`; elements may carry
`pinned`. Retrieval notes may exist as non-core metadata, but
Farplane ingest, content-production skills, and CLI automation must not depend
on a `notes` array. `source` owns source metadata plus tags/facets such as
output types, audiences, industries, customer roles, platform, source handle,
and attribution. CLI text may render count/timeframe from `meta`; production
skills should consume captures/elements and focus more on pinned elements when
composing a new artifact. The retrieval result should be
high-signal and production-usable. Retrieval must preserve each element's
`description`, `whyItWorks`, `goldenExample`, and `goldenRecipe` without
joining source-level analysis at consumption time. It is not moodboard prose,
a duplicated production-pattern object, or a separate evidence collection. Do
not add thumbnails, contact sheets, frame records,
storage IDs, or preview URLs beside the element capsules.

## Derived Preview Asset Upload

When `media-ingest` or `video-understanding` produces a representative
thumbnail, contact sheet, or selected frame image, upload it after the primary
Resource Bank asset row exists. Use the Farplane-UI helper as the write edge:

```bash
npm --prefix "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI" run resource-bank:upload-thumbnail -- \
  --job-id <resourceBankIngestionJobs id> \
  --parent-asset-id <primary resourceBankAssets id> \
  --file /path/to/contact_sheet.jpg \
  --title "Contact sheet: <source title>" \
  --source-url <original source url> \
  --canonical-url <canonical source url> \
  --tag contact-sheet \
  --tag frame-backed \
  --json
```

The script uploads the file to Convex storage, inserts a derived asset row, and
defaults to `assetRole: "thumbnail"` and `assetKind: "image"`. The resulting
derived asset should point back to the primary source asset through
`parentAssetId`. Record the returned `assetId`, `storageId`, file path, and
upload command in the ingestion proof.

Only run this step for real extracted visual assets. If the ingest pass did not
produce a thumbnail, contact sheet, or frame image, skip upload and leave the UI
source tile without a derived preview. Do not generate placeholders or evidence
objects merely to make the dashboard look complete.

## Write Sequence

1. Create or update one capture for the source.
2. Store source URL/ref, operator note/focus, optional transcript,
   `analysisMarkdown`, tags/facets, and selected creative elements.
3. Once the primary asset row exists, optionally upload a real representative
   thumbnail/contact sheet/frame image as a derived storage-backed Resource Bank
   asset with `parentAssetId` pointing to that primary asset.
4. Add optional skill findings only when the source clearly suggests a reusable
   technique, skill update, or skill candidate.
5. Validate that every golden example asset belongs to the same ingestion job.
6. Optionally promote the verified elements to the requested Brand Kit in the
   same ingest action and record the kit/revision receipt.
7. Query Tasty Pack retrieval with the likely timeframe/facets to verify the
   capture returns as `{ captureId, source, analysis, elements }`, with tags and
   facets on `source`, `analysis.operatorNote` when a note exists,
   `analysis.markdown`, optional top-level `transcript`, element
   capsule fields and `pinned` preserved, and `meta.pinnedElementCount`,
   `meta.operatorNoteCount`, and `meta.warnings` populated.
8. If a preview asset was uploaded, verify the upload returned `assetId` and
   `storageId`, and verify Resource Bank dashboard hydration can expose the
   asset as `previewAsset.storageUrl` when UI/API access is available.

## Source Kind Mapping

- `url`: generic link, webpage, profile, or social URL.
- `image`: photo, design still, visual reference.
- `video`: video file or video URL.
- `audio`: audio source.
- `file`: PDF, document, deck, downloaded file, unknown attachment.
- `note`: idea with no external source.
- `screenshot`: screenshot supplied as the source.
- `clip`: selected segment from a longer video/audio source.

## Segment And Element Mapping

For notes like "the first few seconds are nice" or "I like the image used at
the start," save:

- the whole source URL/ref as `source`;
- the operator note/focus;
- compact freeform analysis Markdown naming what is known and what is inferred;
- elements such as `format`, `storyboard`, `visual`, `character`, `audio`,
  and `editing`;
- one complete what/why/example/recipe capsule for every element;
- lightweight anchors such as `0-3s`, `opening frame`, or `caption`;
- `pinned` on the elements the operator explicitly liked, selected, or wants
  reused;
- retrieval facets for audience/output/industry/customer filters when useful.

## Snapshot And Reset

The active Resource Bank contract is the lean complete-capsule contract. When
changing a small old vault, do not preserve a long-lived legacy fallback.
Snapshot old rows to a
ticket artifact, clear active Resource Bank rows, and reingest keep-worthy
sources through the current capture contract.

## Verification Standard

Storage is not done until Resource Bank retrieval returns:

- the source URL/ref and operator note/focus;
- optional transcript plus compact freeform analysis Markdown;
- zero or more complete creative elements, with every stored element explicitly
  selected for reuse by the operator note;
- non-empty `whyItWorks` and `goldenRecipe` plus one resolvable same-ingestion-
  job `goldenExample.assetId` for every element;
- pinned creative elements preserved when the operator identified specific
  liked sub-elements;
- `meta.warnings` warns when an operator note exists but no element was pinned
  from it;
- tags/facets when supplied;
- no dependency on a legacy analysis-only fallback, source-level explanation,
  or default evidence objects to complete an element.

When a derived preview upload is attempted, preview storage is not done until
the upload command returns `assetId` and `storageId`. When dashboard/UI access is
available, also verify the source tile resolves the derived asset to
`previewAsset.storageUrl`. If no real visual was extracted, record
`derived_preview: skipped_no_visual_asset` rather than treating preview absence
as a failure.

If the backing store cannot be reached, a function is missing, upload fails, or
the query does not return the expected capture, report the exact blocker and
keep the analysis packet in chat or a ticket-scoped artifact.
