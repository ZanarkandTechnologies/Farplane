# Reuse Taxonomy

Use this taxonomy to make saved inspiration searchable by future creator
skills. Prefer concrete tags and reusable levers over generic taste words.

## Analysis Facets

Each saved reference should answer:

- `what_it_is`: the source format and visible/known subject.
- `why_it_works`: hook, contrast, novelty, emotional promise, craft move, or
  audience fit.
- `continuation`: what makes the viewer keep watching/reading when relevant.
- `reusable_levers`: the repeatable parts that can inspire new work.
- `elements`: production-use components using the compact element kinds.
- `prompt_guess`: a compact generation or editing prompt when useful.
- `constraints`: what to avoid copying literally.
- `best_for`: future project, content type, campaign, product surface, or vibe.

## Retrieval Facets

Use fields, not tags, when the operator is likely to fetch Tasty Packs by the
facet:

- `outputTypes`: `reel`, `short-video`, `landing-page`, `thumbnail`, `ad`.
- `audiences`: `founders`, `operators`, `students`, `creators`, `buyers`.
- `ageRanges`: `18-24`, `25-34`, `35-44`.
- `industries`: `ai`, `saas`, `education`, `finance`, `creator-economy`.
- `customerRoles`: `founder`, `marketer`, `engineer`, `creator`, `buyer`.
- `tastinessScore`: optional relative value signal when the operator or agent
  can rank how useful the source is.

Use `tastinessScore` for whole-reference priority. Use `CreativeElement.pinned`
for priority among sub-elements inside that reference. Tasty Pack retrieval
reports pinned/operator-note counts and direct warnings; operators should not be
asked for numeric weights.

These fields exist to answer "what did I save recently for this audience or
idea?" quickly.

## Tag Buckets

Use tags for lightweight recall and creative language. Do not maintain a large
taxonomy for hook/open-loop/pacing/retention mechanics; those belong in
analysis and creative elements.

Use a mix of these buckets when source context supports them:

- Intent: `future-video`, `reuse-bg`, `thumbnail-idea`, `landing-page-inspo`,
  `visual-reference`, `copy-reference`, `editing-reference`.
- Format: `short-form-video`, `carousel`, `2x2-grid`, `talking-head-overlay`,
  `screen-recording`, `caption-bar`, `meme-format`, `collage`, `packshot`.
- Subject: `academic-chaos`, `startup`, `ai-agent`, `fashion`, `fitness`,
  `finance`, `design-world`, `creator-workflow`.
- Craft: `high-contrast-copy`, `dense-background`, `human-focal-point`,
  `bold-subtitle`, `lofi-texture`, `ui-screenshot`, `before-after`.
- Retrieval: project name, campaign name, client/product, output type, or
  platform.

## Creative Element Kinds

```text
CreativeElement {
  kind: visual | audio | hook | storyboard | editing | copy | format | constraint | character
  title
  description
  anchor?
  pinned?
}
```

Examples:

- `hook`: "fake AI-news headline buys attention in 0-3s."
- `storyboard`: "wellness ritual escalates into product reveal."
- `visual`: "ancient papery fresco texture with central mythic figure."
- `audio`: "guided-meditation voiceover cadence remixed with devtool terms."
- `editing`: "headline wrapper -> ritual beat -> product reveal -> end card."
- `copy`: "spiritualized coding slogan used as affirmation."
- `format`: "social-news wrapper around parody campaign clip."
- `character`: "deadpan infrastructure guide whose dry office persona makes
  the abstract product feel specific and rewatchable."
- `constraint`: "do not copy actor likeness, source frames, captions, or brand."

Use `pinned` for the exact sub-elements the operator liked or selected in the
ingest note. Do not store numeric creative-element weights or duplicate this
signal with a separate production-pattern record. A reel, post, landing page,
or screenshot becomes a list of creative elements with selected taste pins.
Use `character` when a distinctive persona, archetype, guide, host, mascot, or
recurring character system is one of the reasons the reference is useful. If
the character is based on a real person, actor performance, brand mascot, or
protected fictional character, add a `constraint` element for a rights-safe
remix: borrow the role, contrast, and narrative function, not the likeness,
name, exact styling, voice, catchphrase, or source frames.

## Future Retrieval Query Shape

Future creation skills should query by:

```text
create_tasty_pack(idea?, timeframe?, audience?, industry?, outputType?, tags?, count?)
  -> {
       request: { idea?, timeframe, startAtMs?, endAtMs?, filters },
       captures: [{ captureId, source, analysis, elements }],
       meta: { captureCount: number, timeframe: string }
     }
```

Creation skills consume `captures[].source`, `captures[].analysis`,
`captures[].elements`, and `meta` counts/warnings. They should treat pinned
elements as the primary taste signal and unpinned elements as context.
Retrieval notes are non-core metadata.

Example retrieval requests:

- "top 5 recent references for a 2x2 video collage background"
- "best saved caption-bar short-form video examples for AI agent content"
- "visual references tagged reusable-bg and academic-chaos"
- "inspiration for making a talking-head video feel current and punchy"
