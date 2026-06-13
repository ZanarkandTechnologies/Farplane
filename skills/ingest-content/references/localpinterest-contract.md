# LocalPinterest Contract

## Source Of Truth

Use `/Users/kenjipcx/Documents/LocalPinterest` as the backing project unless the
operator supplies another vault. Read these before making storage claims:

- `AGENTS.md`
- `docs/specs/media-vault.md`
- `convex/schema.ts`
- `convex/content.ts`

## Current Tables

- `contentItems`: one logical saved reference.
- `assets`: source URLs, storage uploads, screenshots, frames, transcripts, or
  attachments linked to a content item.
- `analyses`: Codex-generated breakdowns with summary, takeaways, tags, prompt
  guess, source skill, and analysis type.
- `notes`: operator intent, Codex observations, and follow-up todos.

## Desired Storage Layer

The current tables are enough for v1 capture, but the intended Convex layer
should grow toward "source plus reusable parts." A future schema should support:

- `segments`: time ranges, frame sets, page sections, or regions of interest
  called out by the operator note.
- `elements`: reusable styles, layouts, prompts, backgrounds, captions,
  recipes, patterns, and remix constraints extracted from a source.
- `collections` or `projects`: grouping by future use, campaign, product,
  creator workflow, or user note.
- `searchMetadata`: embeddings, tag weights, recency signals, and retrieval
  reasons for future grounding.

Until those records exist, represent segments and elements through
`assets`, `analyses.takeaways`, `promptGuess`, tags, and structured notes.

## Write Sequence

1. Create an item with `content:createContentItem`.
2. Add a source URL or uploaded file with `content:addAsset`.
3. Add one or more `content:addAnalysis` rows.
4. Add user and Codex notes with `content:addNote`.
5. Query `content:getContentItem` to verify the saved record.

## Convex Function Map

```text
createContentItem({
  title,
  contentKind,
  description?,
  sourceUrl?,
  canonicalUrl?,
  platform?,
  author?,
  tags?
}) -> contentItemId

addAsset({
  contentItemId,
  assetKind,
  sourceUrl?,
  storageId?,
  mimeType?,
  name?
}) -> assetId

addAnalysis({
  contentItemId,
  analysisType,
  sourceSkill: "ingest-content",
  summary,
  takeaways,
  tags,
  promptGuess?
}) -> analysisId

addNote({
  contentItemId,
  noteKind,
  body
}) -> noteId

getContentItem({ contentItemId }) -> item + assets + analyses + notes
```

## Content Kind Mapping

- `image`: screenshot, photo, design still, visual reference.
- `video`: short-form video, motion reference, screen recording.
- `article`: article, essay, newsletter, long-form page.
- `webpage`: landing page, product page, gallery, profile, generic site.
- `audio`: podcast, voice note, music/audio reference.
- `file`: PDF, document, deck, downloaded file, unknown attachment.
- `note`: idea with no external source.

## Asset Kind Mapping

- `original`: uploaded source file or original URL.
- `thumbnail`: preview image.
- `screenshot`: screen capture.
- `frame`: selected video frame.
- `transcript`: transcript file or extracted transcript URL/storage item.
- `attachment`: supporting file.

## Segment And Element Mapping

For notes like "the first few seconds are nice" or "I like the image used at
the start," save:

- the whole source as the `contentItem`;
- the highlighted time range or region as a selected `frame`, `screenshot`, or
  structured note;
- the reusable idea as an analysis takeaway, such as "cold-open background
  image: messy academic desk, high-density paper texture";
- the generation recipe as `promptGuess` or a Codex note;
- tags that make future recall possible, such as `first-3-seconds`,
  `background-image`, `reuse-bg`, `short-form-video`, and project tags.

## Verification Standard

Storage is not done until `content:getContentItem` returns:

- the content item with expected title, kind, status, and tags;
- at least one asset or an explicit note-only reason;
- at least one analysis from `ingest-content`;
- the operator note when supplied.

If the Convex deployment cannot be found, a function is missing, upload fails,
or the query does not return the expected row, report the exact blocker and
keep the analysis packet in chat or a ticket-scoped artifact.
