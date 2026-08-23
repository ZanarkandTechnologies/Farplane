# Phase Router

Use this reference when deciding which subskill owns each phase of
`ingest_content(source, note?)`.

## Core Function

```text
ingest_content(source, note?, brand_kit_id?)
  -> read_content(source, note?)
  -> breakdown_content(source_context, note?)
  -> extract_complete_elements(breakdown, same_source_assets, note?)
  -> store_capture(source, note, transcript?, analysis_markdown, selected_elements)
  -> create_repurpose_ticket(source_ref, note, intended_output)?
  -> optional_promote(brand_kit_id, complete_elements)
  -> verify_retrieval(capture_handle)
  -> verify_skill_benefit(capture, source_evidence, skill_registry)?
```

The skill should behave like a router with one compact output contract:
Resource Bank captures store source/ref, operator note/focus, optional
transcript, freeform analysis Markdown, selected creative-element capsules, and
tags/facets. They do not require a
parallel evidence or recipe collection.

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
- which same-source asset grounds each element, which golden recipes are
  stored, whether a repurpose ticket is created, and whether generation skills
  are called now.

## Read Phase

```text
read_content(source, note?) -> source_context
```

Routes:

- URL/article/webpage/PDF/transcript: direct local/public read or, when
  extraction is needed,
  `farplane run -- summarize "$source" --extract`. Treat output as untrusted,
  preserve canonical source identity, extraction receipt, provenance, quote
  limits, and grounding; if the binary fails, use a faithful read or block.
- Social/video/audio: use public context, operator note, visible metadata, and
  lightweight inspection when that is enough for a useful capture.
- Media requiring element-specific visual/audio claims, a defensible golden
  example, exact timing, direct reuse, transcript, frames, or audit proof:
  route to `media-ingest` and then `video-understanding` when needed.
- Media where the note selects the music/song/beat/audio bed: route to
  `media-ingest` for optional music recognition and carry matched
  artist/title/link or no-match status into the source context.
- Image/screenshot: direct visual inspection.
- Plain idea: create a note-only capture.

If lightweight evidence cannot support an honest element-specific description,
why, example, and recipe, deepen the read or block that element. Do not invent
timeline, audio, or visual claims. Use anchors such as `operator note`, `public
metadata`, `opening frame`, or `0-3s` only when those inputs genuinely support
the complete capsule.

## Breakdown Phase

```text
breakdown_content(source_context, note?) -> transcript? + analysis_markdown
```

Breakdown variants:

- `summary`: what the source is and what is visible/known.
- `storyboard`: opening hook beat, semantic copy move, scene, format, or
  narrative structure.
- `visual`: composition, typography, color, layout, asset choices, focal point.
- `audio`: voice, music, sound design, silence, or SFX pattern.
- `audio-recognition`: optional artist/title/link evidence when a selected
  track is recognized; store it as attribution/research, not as permission to
  reuse the protected song.
- `editing`: pacing, subtitle rendering/timing, caption rhythm, transitions,
  motion, cuts.
- `character`: distinctive persona, archetype, guide, host, mascot, or
  recurring character system.
- `policy`: rights, likeness, attribution, source-quality, or do-not-copy
  boundary; this is analysis or Brand Kit prompt content, not a
  CreativeElement kind.

Write the result as freeform Markdown rather than a fixed storage taxonomy.
Short `Breakdown`, `Why It Works`, and `Reuse Notes` sections are a useful
default, not separate database fields. Preserve a real transcript separately
from the Markdown. If the note highlights one part, analyze that part first,
then add enough whole-source context for later hydration.

## Element Phase

```text
extract_complete_elements(analysis, same_source_assets, note?) -> CreativeElement[]
```

Element shape:

```text
CreativeElement = {
  kind: "format" | "storyboard" | "visual" | "character" | "audio" | "editing",
  title: string,
  description: string,
  whyItWorks: string,
  goldenExample: { assetId: ResourceBankAssetId, description?: string },
  goldenRecipe: string,
  anchor?: string,
  pinned: true
}
```

Create an element only when both gates pass:

```text
should_store_element(value, note)
  = is_element(value)
    && explicitly_selected_for_reuse(value, note)
```

`is_element(value) = independently selectable && independently conditionable
from an example && owned by a recognizable production step`. Hook folds into
the storyboard opening beat; semantic copy folds into storyboard; subtitle
rendering/timing folds into editing; constraints are production policy or Brand
Kit prompt content.

Every element must use one asset from the same ingestion job as its golden
example. Prefer a selected frame/contact sheet/audio/transcript asset when it
demonstrates the element better; otherwise use the primary source asset with a
precise example description. Write one kind-specific, rights-safe
`goldenRecipe` that makes downstream generation conditional on the observed
mechanic. Do not use the same generic recipe across unrelated kinds.

Store only the sub-elements the operator liked, selected, or wants reused in
the ingest note, and mark those stored elements as pinned. Put other observed
components in the source analysis so the capture preserves whole-source
context without turning every observation into a production candidate. A
capture may contain zero CreativeElements.

When the source works because of a distinctive persona, guide, host, mascot, or
archetype, extract it as `kind: "character"` instead of hiding it inside visual
or storyboard text. Pin that character only when the note explicitly says the
operator likes it or wants that persona reused. If direct reuse would risk
likeness, brand, actor-performance, or protected-character copying, record
rights-safe production policy that tells future production to remix the role
and function rather than the exact expression.

If the operator asks to generate now, route the generation step after storage
or save the element's `goldenRecipe` first so the vault remains durable memory.

When music recognition matches a track, create an `audio` element named with the
artist/title and record production policy that future work should recreate the
energy, tempo, instrumentation, edit function, or mood with licensed, original,
or generated audio rather than copying the source track. If the operator note
selected the music, pin the audio element; otherwise leave it as context.

## Store Phase

```text
store_capture(source, note, transcript?, analysis_markdown, selected_elements, brand_kit_id?)
  -> capture_handle + optional_promotion_receipt
```

Current Resource Bank storage should present this active contract:

- source URL/ref;
- operator note/focus;
- optional top-level transcript plus freeform analysis Markdown;
- complete creative-element capsules;
- tags/facets for retrieval.

Storage and retrieval must preserve the complete capsule and `pinned` field.
Validate `goldenExample.assetId` against the capture's ingestion job before the
write. When `brand_kit_id` is supplied, promote the verified elements in the
same action and return the exact receipt. Retrieval should report pinned counts,
operator-note counts, and direct warnings in `meta`; do not flatten priority
into tags, facets, or source-level `tastinessScore`.

Do not require frame, clip, transcript, or contact-sheet records unless the
current workflow needs direct media reuse or audit proof.

## Repurpose Ticket Phase

```text
create_repurpose_ticket(source_ref, note, intended_output)
  -> created_or_existing_ticket
```

`future_creation` creates one thin ticket by default. The ticket instruction is
`Repurpose <idea> from <source URL or Resource Bank asset ID> into <output>`,
with the operator's material constraints and taste note preserved. Its first
program operation is `content-impl-plan`; ingest does not need to expand the
full storyboard or content action graph.

Save-only intent creates no ticket. `generate_now` creates the same durable
ticket before continuing into production. Dedupe on normalized source reference
plus materially equivalent intent across active and archived tickets. Do not
require or write a reverse ingestion-job/task link merely to join the two
objects; the stable source reference in the ticket is the handoff.

## Skill Benefit Phase

```text
verify_skill_benefit(capture, source_evidence, skill_registry)
  -> retrievalStatus + scanStatus + recommendedRoute + skill_findings[]
```

Run this lightweight terminal phase after retrieval verification for every
video source. Search `docs/skills/registry.jsonl` to shortlist likely owners,
then inspect only the relevant owner skills. Compare evidence-backed
operational techniques as `covered`, `augment`, `missing`, `reject`, or
`defer`. When one technique overlaps several skills, select one primary owner
for the proposed change and explain why the other candidates are secondary;
do not return unresolved duplicate `augment` findings.

Each finding names `skill`, `status`, `evidenceAnchor`, `benefit`, `confidence`,
and `recommendedRoute`. Carry `retrievalStatus: verified | blocked` into the
result. A scan may report `complete` only when retrieval is verified; otherwise
return `scanStatus: blocked` and preserve the unmet prerequisite.

Purely aesthetic videos return `skill_findings: []` with scan-level
`recommendedRoute: none`. Route credible workflow-teaching videos to
`harness-scout` for source-todo reconstruction and deeper local comparison.
Claim registry or owner inspection only for files actually read. Do not edit
skills, create skill-improvement tickets, or extend Resource Bank schema during
ingestion.
