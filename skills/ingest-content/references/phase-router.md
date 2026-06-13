# Phase Router

Use this reference when deciding which subskill or storage shape owns each
phase of `ingest_content(source, note?)`.

## Core Function

```text
ingest_content(source, note?)
  -> read_content(source, note?)
  -> breakdown_content(evidence, note?)
  -> extract_usefulness(breakdown, note?)
  -> store_content(source, evidence, usefulness, note?)
```

Each phase may choose a different specialist. The skill should behave like a
router with a shared output contract, not a single monolithic analyzer.

## Note Intent

Parse the note before extraction:

- `save_reference`: "save this", "I like this", "for future reference".
- `segment_focus`: "first few seconds", "this background", "this shot",
  "the image used here", "the caption style".
- `future_creation`: "make a video like this later", "use this for a landing
  page", "make my own version".
- `generate_now`: "make me my own", "create a similar image", "turn this into
  assets now".
- `project_memory`: a project, client, campaign, or personal context tag.

The note should influence:

- what part of the source is inspected;
- which elements are extracted;
- which tags are added;
- whether generation recipes are stored or generation skills are called now.

## Read Phase

```text
read_content(source, note?) -> evidence_bundle
```

Routes:

- URL/article/webpage/PDF/transcript: `summarize` or direct local read.
- Social/video/audio: `media-ingest` for source identity, transcript status,
  representative frames, and retention note.
- Video segment requested by note: `media-ingest` first, then
  `video-understanding` over selected frames/transcript section.
- Image/screenshot: direct visual inspection; optionally store original or
  screenshot as an asset.
- Plain idea: create note-only evidence with source kind `manual`.

Evidence must mark confidence:

- `source-backed`
- `frame-backed`
- `transcript-backed`
- `visual-only`
- `note-backed`
- `inferred`

## Breakdown Phase

```text
breakdown_content(evidence, note?) -> source_facts + taste_analysis
```

Breakdown variants:

- `summary`: what the source is and what is visible.
- `visual`: composition, typography, color, layout, asset choices, focal point.
- `video`: hook, pacing, shot structure, segment timing, editing pattern.
- `copy`: caption, headline, claim, CTA, on-screen text, meme wording.
- `style`: mood, texture, genre, cultural pattern, audience signal.
- `prompt`: likely generation/editing prompt or recreation instructions.

Do not flatten everything into one summary. If the note highlights one part,
analyze that part first, then add a one-line whole-source context summary.

## Usefulness Phase

```text
extract_usefulness(breakdown, note?) -> reusable_elements[]
```

Reusable element candidates:

- `style`: visual style, lighting, texture, design language, editing style.
- `layout`: grid, overlay, composition, hierarchy, caption placement.
- `segment`: time range, selected frame set, scene, quote, or audio moment.
- `asset`: background image, cutout, thumbnail, frame, transcript, prompt.
- `pattern`: hook, meme structure, before/after, contrast, pacing.
- `recipe`: steps to regenerate something similar.
- `constraint`: attribution, avoid-copying note, remix boundary.

Element record shape:

```text
ReusableElement = {
  kind,
  label,
  why_useful,
  evidence_anchor,
  generation_recipe?,
  tags,
  confidence,
  remix_constraints
}
```

If the operator asks to generate now, route the generation step after storage
or save the extracted recipe first so the vault remains the durable memory.

## Store Phase

```text
store_content(source, evidence, usefulness, note?) -> contentItemId + proof
```

Current LocalPinterest storage can represent elements through:

- `contentItems`: one source/reference.
- `assets`: source URL, original file, screenshot, frame, transcript, or
  attachment.
- `analyses`: summary, tags, takeaways, prompt guess, source skill.
- `notes`: user intent, Codex observations, follow-up todos.

Future richer storage should add first-class records for:

- segments: time ranges, selected frames, clip labels, transcript spans.
- reusable elements: style/layout/asset/pattern/recipe records.
- embeddings or search metadata: semantic retrieval beyond tag search.
- projects/collections: why a source was saved for a future task.

Until those tables exist, write element records into `analyses.takeaways`,
`promptGuess`, tags, and notes in a structured way.
