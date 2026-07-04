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
  kind: visual | audio | hook | storyboard | editing | copy | format | constraint
  title: string
  description: string
  anchor?: string
}
```

Store first-class frame, clip, transcript, contact-sheet, or evidence records
only when a future workflow actually needs direct media reuse or audit proof.
Do not make evidence objects, lane taxonomies, provenance enums, or
frame-accurate fields part of the default v2 capture contract.

## Retrieval Fields

Use facets only for things the operator will filter, group, or pack by:

- `outputTypes`: examples `reel`, `short-video`, `landing-page`, `thumbnail`.
- `audiences`: examples `founders`, `operators`, `students`, `creators`.
- `ageRanges`: examples `18-24`, `25-34`, `35-44`.
- `industries`: examples `ai`, `saas`, `education`, `finance`.
- `customerRoles`: examples `founder`, `marketer`, `engineer`, `buyer`.
- `tastinessScore`: optional 0-1-ish operator or agent confidence that this is
  a high-value reference.

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

Use `anchor` for lightweight grounding such as `0-3s`, `opening frame`,
`voiceover`, `caption`, `cutaway`, `end card`, or `operator note`. If the
source could not be inspected deeply, state that in analysis and keep element
anchors honest.

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

Core consumer fields are only `captures[].source`, `captures[].analysis`, and
`captures[].elements`. Retrieval notes may exist as non-core metadata, but
Farplane ingest, content-production skills, and CLI automation must not depend
on a `notes` array. `source` owns source metadata plus tags/facets such as
output types, audiences, industries, customer roles, platform, source handle,
and attribution. CLI text may render count/timeframe from `meta`; production
skills should consume captures/elements. The retrieval result should be
high-signal and production-usable, not moodboard prose and not separate
evidence objects.

## Write Sequence

1. Create or update one capture for the source.
2. Store source URL/ref, operator note/focus, analysis summary, tags/facets,
   and creative elements.
3. Add optional skill findings only when the source clearly suggests a reusable
   technique, skill update, or skill candidate.
4. Query Tasty Pack retrieval with the likely timeframe/facets to verify the
   capture returns as `{ captureId, source, analysis, elements }`, with tags and
   facets on `source`.

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
  `format`, and `constraint`;
- lightweight anchors such as `0-3s`, `opening frame`, or `caption`;
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
- tags/facets when supplied;
- no dependency on a legacy analysis-only fallback or default evidence objects.

If the backing store cannot be reached, a function is missing, upload fails, or
the query does not return the expected capture, report the exact blocker and
keep the analysis packet in chat or a ticket-scoped artifact.
