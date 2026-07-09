# Phase Router

Use this reference when deciding which subskill owns each phase of
`ingest_content(source, note?)`.

## Core Function

```text
ingest_content(source, note?)
  -> read_content(source, note?)
  -> breakdown_content(source_context, note?)
  -> extract_elements(breakdown, note?)
  -> store_capture(source, note, analysis, elements)
```

The skill should behave like a router with one compact output contract:
Resource Bank captures store source/ref, operator note/focus, analysis summary,
creative elements, and tags/facets. They do not require separate evidence
objects by default.

## Note Intent

Parse the note before extraction:

- `save_reference`: "save this", "I like this", "for future reference".
- `segment_focus`: "first few seconds", "this background", "this shot",
  "the image used here", "the caption style".
- `music_identification`: "the music is nice", "what song is this", "I like
  the beat", "save this soundtrack", "find out more about the audio".
- `future_creation`: "make a video like this later", "use this for a landing
  page", "make my own version".
- `generate_now`: "make me my own", "create a similar image", "turn this into
  assets now".
- `project_memory`: a project, client, campaign, or personal context tag.

The note should influence:

- what part of the source is inspected;
- which creative elements are extracted;
- which retrieval facets and tags are added;
- whether generation recipes are stored or generation skills are called now.

## Read Phase

```text
read_content(source, note?) -> source_context
```

Routes:

- URL/article/webpage/PDF/transcript: `summarize` or direct local read.
- Social/video/audio: use public context, operator note, visible metadata, and
  lightweight inspection when that is enough for a useful capture.
- Media requiring exact timing, direct reuse, transcript, frames, or audit
  proof: route to `media-ingest` and then `video-understanding` when needed.
- Media where the note selects the music/song/beat/audio bed: route to
  `media-ingest` for optional music recognition and carry matched
  artist/title/link or no-match status into the source context.
- Image/screenshot: direct visual inspection.
- Plain idea: create a note-only capture.

If a source cannot be inspected deeply, say so in the analysis. Do not invent
timeline, audio, or visual claims. Use creative element anchors such as
`operator note`, `public metadata`, `opening frame`, or `0-3s` to show what the
element is grounded in.

## Breakdown Phase

```text
breakdown_content(source_context, note?) -> analysis
```

Breakdown variants:

- `summary`: what the source is and what is visible/known.
- `hook`: what earns attention first.
- `storyboard`: beat, scene, format, or narrative structure.
- `visual`: composition, typography, color, layout, asset choices, focal point.
- `audio`: voice, music, sound design, silence, or SFX pattern.
- `audio-recognition`: optional artist/title/link evidence when a selected
  track is recognized; store it as attribution/research, not as permission to
  reuse the protected song.
- `editing`: pacing, caption rhythm, transitions, motion, cuts.
- `copy`: caption, headline, claim, CTA, on-screen text, meme wording.
- `character`: distinctive persona, archetype, guide, host, mascot, or
  recurring character system.
- `constraint`: rights, likeness, attribution, source-quality, or do-not-copy
  boundary.

Do not flatten everything into one adjective-heavy summary. If the note
highlights one part, analyze that part first, then add a one-line whole-source
context summary.

## Element Phase

```text
extract_elements(analysis, note?) -> CreativeElement[]
```

Element shape:

```text
CreativeElement = {
  kind: "visual" | "audio" | "hook" | "storyboard" | "editing" | "copy" | "format" | "constraint" | "character",
  title: string,
  description: string,
  anchor?: string,
  pinned?: boolean
}
```

Extract all useful creative elements needed to understand the source, but pin
only the sub-elements the operator liked, selected, or wants reused in the
ingest note. Retrieval derives planning priority from pins instead of storing
numeric weights or creating a separate production-pattern object.

When the source works because of a distinctive persona, guide, host, mascot, or
archetype, extract it as `kind: "character"` instead of hiding it inside visual
or storyboard text. Pin that character only when the note explicitly says the
operator likes it or wants that persona reused. If direct reuse would risk
likeness, brand, actor-performance, or protected-character copying, add a
rights-safe `constraint` element that tells future production to remix the role
and function rather than the exact expression.

If the operator asks to generate now, route the generation step after storage
or save the extracted recipe first so the vault remains the durable memory.

When music recognition matches a track, create an `audio` element named with the
artist/title and add a `constraint` element that future work should recreate the
energy, tempo, instrumentation, edit function, or mood with licensed,
original, or generated audio rather than copying the source track. If the
operator note selected the music, pin the audio element; otherwise leave it as
context.

## Store Phase

```text
store_capture(source, note, analysis, elements) -> capture_handle + retrieval_proof
```

Current Resource Bank storage should present this active contract:

- source URL/ref;
- operator note/focus;
- compact analysis summary;
- creative elements;
- tags/facets for retrieval;
- optional skill findings when the source suggests a reusable technique or
  skill update.

Storage and retrieval must preserve `CreativeElement.pinned` as an element
field. Retrieval should report pinned counts, operator-note counts, and direct
warnings in `meta`; do not flatten priority into tags, facets, or source-level
`tastinessScore`.

Do not require frame, clip, transcript, or contact-sheet records unless the
current workflow needs direct media reuse or audit proof.
