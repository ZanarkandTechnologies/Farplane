# Resource Bank Branch

Load this only when the operator explicitly likes, saves, or wants to reuse
part of a source ("save the opening", "I like this style", "make my own version
later"). Analysis alone never saves anything here, and "save to Wiki" is not
reuse intent. The backing store is the bunker's Resource Bank module at
`/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI-v2/convex/modules/resourceBank`.

```text
resource_bank_save(source, note, brand_kit_id?, context?)
  -> capture_handle + selected_creative_elements + tickets[] + retrieval_proof
     + optional_promotion_receipt | pending_capture_payload + blocker
```

Phase detail lives in [phase router](phase-router.md); storage fields in
[Resource Bank contract](resource-bank-contract.md); tags and facets in
[reuse taxonomy](reuse-taxonomy.md); saved-capture-to-profile work in
[compile style profile](compile-style-profile.md).

## Rules that never bend

- **Promote only what the note selects.** Whole-source understanding stays in
  `analysisMarkdown`. A CreativeElement exists only when it passes
  `is_element` (independently selectable, conditionable from an example, owned
  by a recognizable production step) and the note explicitly likes, selects,
  or asks to reuse it. A capture may hold zero elements. "Only the caption
  entrance" creates one editing element and nothing else.
- **Golden example from the same source.** Every element points to exactly one
  asset created by the same ingestion job (a frame, contact sheet, audio or
  transcript asset, else the primary source asset with a precise description).
  Never borrow an asset from another job; never reuse one generic example or
  recipe across unrelated kinds.
- **Never auto-save.** No Resource Bank write without explicit reuse intent;
  no placeholder preview when no real frame or contact sheet was extracted.
- Every element carries `kind` (format | storyboard | visual | character |
  audio | editing), `title`, `description`, non-empty `whyItWorks`, one
  `goldenExample { assetId, description? }`, one kind-specific rights-safe
  `goldenRecipe`, optional `anchor`, and `pinned: true`.

## Steps

1. Bind `source`, `note`, optional `brand_kit_id`, context, and note intent:
   save-only, segment focus, music identification, future creation, or
   generate now. With no external source, save a note-only capture only when
   the operator clearly wants the idea itself kept.
2. Resolve discovery surfaces (Pinterest pins, curated galleries) to the
   canonical original with the in-app Browser; record method, candidate URLs,
   evidence, and access limit. Unresolved items are saved as inspiration-only
   with `rights_status: unknown`; never infer a licence from visibility.
3. Read through intelligest's extraction step; use the [media evidence
   route](../media.md) when element-specific claims need frames, timing,
   audio, or music recognition. If evidence cannot support an honest
   why/example/recipe, deepen the read or block that element.
4. Write `analysisMarkdown` (Breakdown, Why It Works, Reuse Notes when useful),
   keep a real transcript in top-level `transcriptText`, and keep source
   facts, interpretation, and the operator's note apart. For video, say what
   earns the first three seconds and what keeps each later beat watched.
5. Extract only the selected elements. A persona the operator likes is
   `kind: character` with rights-safe remix policy; a recognized track is an
   `audio` element used for attribution, never permission to copy the song.
6. Store the capture with source ref, note, analysis, transcript, tags and
   facets, and complete capsules. After the primary asset row exists, upload a
   real thumbnail, contact sheet, or frame with the bunker's
   `resource-bank:upload-thumbnail` script (`assetRole: "thumbnail"`,
   `parentAssetId` = primary asset). Promote to `brand_kit_id` in the same
   action when supplied.
7. Tickets: save-only creates none. `future_creation` creates one thin
   source-addressable ticket, "Repurpose <idea> from <source URL or asset ID>
   into <output>", whose first operation is `storyboard`; dedupe on
   source plus equivalent intent first. `generate_now` creates the ticket, then
   continues into `ai-image` or `ai-video`.
8. Verify retrieval through Tasty Pack: the capture returns with source,
   analysis, note, transcript, complete elements, `pinned`, and `meta` counts
   and warnings; every example asset belongs to the capture's job. If Convex is
   unavailable, return the analysis packet, a ready-to-write
   `pending_capture_payload`, and the exact write blocker; never claim a save.

## Gotchas

- Do not collapse "I like this" into adjectives; record the concrete element a
  future creator skill can fetch and apply.
- Do not copy protected expression: store patterns, attribution, and remix
  constraints. Likeness, voice, catchphrases, and branded costume stay out.
- Do not over-tag hook or retention mechanics; they belong in analysis prose.
- Do not keep old analysis-only rows as active data after a contract reset:
  snapshot, clear, and reingest keep-worthy sources.

## Output

Return the capture handle, source and `source_resolution` (discovery URL,
canonical URL, status, method, rights status), facets and tags, selected
elements, storage and retrieval proof, optional promotion receipt, and
`tickets[]` (each with ID, source ref, intended output, status). Map the
outcome into the Intelligence Receipt as `resourceBank: saved | blocked`.
