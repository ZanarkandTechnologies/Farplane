# Resource Bank Contract

## Source Of Truth

Use the Farplane UI Resource Bank module as the backing store unless the
operator supplies another vault:

- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI/convex/modules/resourceBank/AGENTS.md`
- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI/convex/modules/resourceBank/schema.ts`
- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI/convex/modules/resourceBank/validators.ts`

## Active Contract

Resource Bank v2 is a compact capture store, not an evidence vault.

```text
ResourceBankCapture {
  source: string
  note?: string
  focus?: string
  analysis: string
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
  kind: visual | audio | hook | storyboard | editing | copy | format | constraint | character
  title: string
  description: string
  anchor?: string
  pinned?: boolean
}
```

Store first-class frame, clip, transcript, contact-sheet, or evidence records
only when a future workflow actually needs direct media reuse or audit proof.
Do not make evidence objects, lane taxonomies, provenance enums, or
frame-accurate fields part of the default v2 capture contract.

Storage-backed preview assets are allowed as UI enrichment when another ingest
phase already produced a real visual. They are derived Resource Bank assets, not
Tasty Pack payload fields.

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
retrieving?" `CreativeElement.pinned` is element-level taste priority inside a
capture: "which sub-elements did the operator say they liked?" Tasty Pack
retrieval reports pinned counts, operator-note counts, and direct warnings in
`meta`, but numeric weights are not stored on creative elements.

Keep `tags` lightweight and freeform for style, subject, project, and recall.
Do not create managed tag families for hook/open-loop/pacing/retention unless a
later UI or query path proves the need.

## Analysis Shape

Keep analysis compact and source-useful:

```text
analysis:
  summary: what the source is
  why_it_works: why it caught attention or matters
  hook: what earns attention in the first 0-3 seconds when relevant
  continuation: what keeps people watching/reading when relevant
  reuse_notes: what to borrow at the pattern level
  constraints: what not to copy literally
```

The analysis explains the source; `elements[]` are the production-use pieces.
Pinned elements are the operator's taste signal. Store all useful context
elements needed to understand the reference, but mark only the specific
sub-elements the operator note liked as `pinned` so future Tasty Packs can bias
reuse without losing context.

## Creative Element Guidance

Use compact elements. Prefer several precise elements over one large summary.

- `hook`: opening attention move.
- `storyboard`: beat, scene, narrative move, or structure.
- `visual`: art direction, object, setting, layout, frame idea, or asset style.
- `audio`: voice, music, SFX, silence, or sonic pattern.
- `editing`: pacing, transition, caption rhythm, motion, or cut pattern.
- `copy`: caption, headline, phrase structure, or script move.
- `format`: platform/content format or repeatable wrapper.
- `constraint`: rights, likeness, brand, source-quality, or remix boundary.
- `character`: distinctive persona, archetype, guide, host, mascot, recurring
  voice, or character system that makes the reference reusable.

Use `anchor` for lightweight grounding such as `0-3s`, `opening frame`,
`voiceover`, `caption`, `cutaway`, `end card`, or `operator note`. If the
source could not be inspected deeply, state that in analysis and keep element
anchors honest.

Use `pinned` only for liked, selected, or operator-highlighted sub-elements,
preferably backed by `analysis.operatorNote`. Do not ask for or store numeric
creative-element weights. Do not add a separate `production_pattern` object; the
reference pattern emerges from the element list. This applies across reels,
landing pages, posts, screenshots, and notes.

For `character` elements, describe the reusable role and behavior rather than
copying protected expression: e.g. "deadpan technical guide who translates
abstract infrastructure into a dry office ritual." When the source character
resembles a real person, actor performance, brand mascot, or protected fictional
character, pair it with a `constraint` element that keeps the remix
rights-safe: preserve archetype, function, contrast, and emotional job; avoid
copying likeness, name, exact wardrobe, voice, catchphrases, source frames,
logos, or branded presentation.

## Tasty Pack Shape

Tasty Pack / Inspiration Pack retrieval should return clean captures:

```text
createTastyPack(request) -> {
  request: { idea?, timeframe, startAtMs?, endAtMs?, filters },
  captures: [
    {
      captureId,
      source,
      analysis,
      elements
    }
  ],
  meta: { captureCount: number, timeframe: string }
}
```

Core consumer fields are `captures[].source`, `captures[].analysis`,
`captures[].elements`, and direct `meta` counts/warnings such as
`pinnedElementCount`, `operatorNoteCount`, and `warnings`; elements may carry
`pinned`. Retrieval notes may exist as non-core metadata, but
Farplane ingest, content-production skills, and CLI automation must not depend
on a `notes` array. `source` owns source metadata plus tags/facets such as
output types, audiences, industries, customer roles, platform, source handle,
and attribution. CLI text may render count/timeframe from `meta`; production
skills should consume captures/elements and focus more on pinned elements when
composing a new artifact. The retrieval result should be
high-signal and production-usable, not moodboard prose, not a duplicated
production-pattern object, and not separate
evidence objects. Do not add thumbnails, contact sheets, frame records,
storage IDs, or preview URLs to the active pack contract unless a future
production workflow explicitly needs those fields.

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
2. Store source URL/ref, operator note/focus, analysis summary, tags/facets,
   and creative elements.
3. Once the primary asset row exists, optionally upload a real representative
   thumbnail/contact sheet/frame image as a derived storage-backed Resource Bank
   asset with `parentAssetId` pointing to that primary asset.
4. Add optional skill findings only when the source clearly suggests a reusable
   technique, skill update, or skill candidate.
5. Query Tasty Pack retrieval with the likely timeframe/facets to verify the
   capture returns as `{ captureId, source, analysis, elements }`, with tags and
   facets on `source`, `analysis.operatorNote` when a note exists, element
   `pinned` preserved, and `meta.pinnedElementCount`, `meta.operatorNoteCount`,
   and `meta.warnings` populated.
6. If a preview asset was uploaded, verify the upload returned `assetId` and
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
- a compact analysis naming what is known and what is inferred;
- elements such as `hook`, `visual`, `storyboard`, `editing`, `audio`, `copy`,
  `format`, `character`, and `constraint`;
- lightweight anchors such as `0-3s`, `opening frame`, or `caption`;
- `pinned` on the elements the operator explicitly liked, selected, or wants
  reused;
- retrieval facets for audience/output/industry/customer filters when useful.

## Snapshot And Reset

The active Resource Bank contract is minimal v2. When changing a small old
vault, do not preserve a long-lived legacy fallback. Snapshot old rows to a
ticket artifact, clear active Resource Bank rows, and reingest keep-worthy
sources through the current capture contract.

## Verification Standard

Storage is not done until Resource Bank retrieval returns:

- the source URL/ref and operator note/focus;
- compact analysis;
- at least one creative element for video/social inspiration sources;
- pinned creative elements preserved when the operator identified specific
  liked sub-elements;
- `meta.warnings` warns when an operator note exists but no element was pinned
  from it;
- tags/facets when supplied;
- no dependency on a legacy analysis-only fallback or default evidence objects.

When a derived preview upload is attempted, preview storage is not done until
the upload command returns `assetId` and `storageId`. When dashboard/UI access is
available, also verify the source tile resolves the derived asset to
`previewAsset.storageUrl`. If no real visual was extracted, record
`derived_preview: skipped_no_visual_asset` rather than treating preview absence
as a failure.

If the backing store cannot be reached, a function is missing, upload fails, or
the query does not return the expected capture, report the exact blocker and
keep the analysis packet in chat or a ticket-scoped artifact.
