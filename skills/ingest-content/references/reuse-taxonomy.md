# Reuse Taxonomy

Use this taxonomy to make saved inspiration searchable by future creator
skills. Prefer concrete tags and reusable levers over generic taste words.

## Analysis Facets

Each saved reference should answer:

- `what_it_is`: the source format and visible subject.
- `why_it_works`: the hook, contrast, novelty, emotional promise, craft move, or
  audience fit.
- `reusable_levers`: the repeatable parts that can inspire new work.
- `reusable_elements`: first-class candidates such as style, layout, segment,
  asset, pattern, recipe, or remix constraint.
- `asset_recipe`: what assets a future agent would need to recreate the
  pattern.
- `prompt_guess`: a compact generation or editing prompt when useful.
- `remix_constraints`: what to avoid copying literally.
- `best_for`: future project, content type, campaign, product surface, or vibe.

## Tag Buckets

Use a mix of these buckets when evidence supports them:

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

## Reusable Lever Shape

Write reusable levers as action-ready phrases:

```text
- Build a 2x2 collage from four thematically related chaos/study images.
- Put a centered vertical face cutout over the grid to create a human anchor.
- Use black caption bars with white/yellow text for instant mobile legibility.
- Keep the copied idea at the composition/pacing level, not creator identity.
```

## Reusable Element Kinds

- `style`: "high-contrast lo-fi academic chaos with handheld phone energy."
- `layout`: "2x2 background grid with centered vertical talking-head overlay."
- `segment`: "first 3 seconds, before the talking-head zoom."
- `asset`: "messy desk background, black caption bar, yellow subtitle strip."
- `pattern`: "contrarian claim over visual proof collage."
- `recipe`: "generate four study-chaos panels, crop to 9:16 grid, overlay face."
- `constraint`: "do not copy the creator identity, exact caption, or source
  frames; reuse the composition pattern."

## Future Retrieval Query Shape

Future creation skills should query by:

```text
retrieve_assets(goal, tags?, recency?, project?, output_type?, count?)
  -> top_matches + why_relevant + reusable_levers + attribution
```

Example retrieval requests:

- "top 5 recent references for a 2x2 video collage background"
- "best saved caption-bar short-form video examples for AI agent content"
- "visual references tagged reusable-bg and academic-chaos"
- "inspiration for making a talking-head video feel current and punchy"
