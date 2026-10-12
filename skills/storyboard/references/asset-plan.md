---
title: Asset Plan
owner: storyboard
status: active
kind: reference
updated_at: 2026-10-12
---

# Asset Plan

Load this in the `assets` mode. It turns a storyboard, reference video, Tasty
Pack, or source media into an asset inventory, discovery receipt, recreation
plan, and owner routes, and it returns accepted files with provenance. It does
not write edit direction (`edit` mode) or render (HyperFrames).

```text
asset_plan(storyboard_or_reference, element_realization_packets?, source_assets?, platform?, constraints?)
  -> asset_inventory + discovery_receipt + moodboard_decision? + generation_packets
   + accepted_asset_files + provenance | blocked_report
```

When raw media first needs metadata, transcripts, or frames, run
[intelligest](../../intelligest/references/media.md). Send a recreation plan that copies
one reference closely, or that drives a high-visibility campaign, to
[review](../../review/SKILL.md).

## Execute discovery now

When the operator approved execution and search tools exist, candidate
discovery is an action in this run, not a recommendation. Run the searches,
inspect useful candidates, and fill the receipt. If the storyboard is too vague
to search, turn each scene into a concrete need from the narration first and
block only the rows that stay unresolved. Tool unavailability is a blocker, not
`searched_no_reference`; that result needs an executed search with specific
candidate pages or asset IDs and fit decisions.

Search order: supplied and local media, Resource Bank and reference anchors,
then web, stock, archive, icon/illustration, footage, texture, or overlay
libraries suited to the asset class. Record the exact query, specific asset
page URL or ID (a search-results page is query evidence only), preview or
metadata evidence, rights status, and the fit or reject reason. Keep the
strongest fit, the strongest rejected alternative, and the reason for each
material need. "Custom is faster" is not a search result.

## Two independent axes

Classify every reference on both axes before deciding to use it:

```text
usage_role:    production_source | cinematic_reference | taste_discovery |
               archive_reference | generated
rights_status: cleared | restricted_reference_only |
               per_item_verification_required | unknown
```

- `production_source`: intended for direct use once license, provenance,
  dimensions, and transformation rights are verified.
- `cinematic_reference`: a frame studied for composition, lighting, palette,
  lens, or blocking (ShotDeck and FilmGrab are examples).
- `taste_discovery`: a broad surface for mood, material, or layout directions
  (Savee and Pinterest are examples).
- `archive_reference`: historical or documentary grounding; direct reuse still
  needs rights verification.
- `generated`: an original output whose provider terms, input rights, likeness,
  and acceptance evidence stay attached.

The same source class can give different rights results per item. Never
promote `cinematic_reference` or `taste_discovery` to `cleared` because it is
public, high quality, downloadable, or easy to screenshot. Verify current site
terms when a specific candidate matters.

## Decision ladder

Resolve every missing visual in order:
`reuse -> source -> inspired_generation -> original_generation`.
Mark each asset `reuse`, `source`, `inspired_generation`,
`original_generation`, `capture`, `compose`, or `unknown`.

- `inspired_generation` needs a rights-safe reference set, a transferable-trait
  map (composition, lighting, palette, texture/material, camera), and the
  protected expression, likeness, logos, signatures, or exact composition the
  output must not copy.
- `original_generation` is valid after `searched_no_reference` or when the
  brief explicitly requires generation, and still needs a concrete prompt,
  owner, output path, rights/likeness note, and acceptance check.
- `compose` arranges or treats accepted source media; it never draws new
  content. Custom SVG animation assets and SVG/JSX/canvas/programmatic-vector
  stand-ins for illustrations, characters, props, backgrounds, textures, or
  diagrams are banned. Existing user-supplied, brand-owned, licensed, or
  discovered SVG files stay valid as static source media with provenance.
- An inspiration-led plan made only of CSS, text, or cards is blocked unless
  the run is labelled `technical_smoke` or `text_only_format` and the content
  claim is downgraded.

## Moodboard before prompt

```text
moodboard_decision(refs)
  -> composition + lighting + palette + texture_material + camera_editorial
   + must_not_copy + accepted_at
compile_prompt(moodboard_decision) -> allowed only when accepted_at exists
```

Show the trait map as the moodboard decision and record
`moodboard_traits_accepted_at` plus the approval source (the operator or a
controlling approved spec). While pending, emit
`prompt_compilation: blocked_until_moodboard_accepted` and replace the
generation-packet table with `generation_packets: blocked_until_moodboard_accepted`.

```text
ShotDeck frame   usage_role: cinematic_reference  rights_status: restricted_reference_only
                 transfer: centered machine silhouette, hard rim light, deep negative space
Pinterest board  usage_role: taste_discovery      rights_status: per_item_verification_required
                 transfer: restrained grotesk type, brushed-metal texture, warm-gray palette
must_not_copy: exact frame composition, actor likeness, logos, source text
moodboard_traits_accepted_at: 2026-08-02T02:00:00+08:00
```

## Brand Kit, Tasty Pack, and anchors

Complete element realization packets are the source of truth. Map pinned
elements first, then the rest. Every `visual`, `storyboard`, `character`,
`audio`, or `format` element that implies a file maps to an asset decision or
appears under missing inputs, carrying its ID, provenance, description,
whyItWorks, resolved golden example, golden recipe, planned use, and
acceptance check. A title-only element is an incomplete handoff. Editing
patterns stay with the `edit` mode; map only their explicit media dependencies.

Resolve `source.assetId + anchor` (for example `contact_sheet`,
`frame_08_28.58s`, `frames 1-4`, `OG thumbnail`) into a concrete media ref. If
none resolves, emit a regeneration packet with the pinned element, anchor,
reference source, rights notes, and acceptance check. A verbal paraphrase is not
enough; only an explicit `semantic_storyboard_only` downgrade allows it.

## Continuity and overlays

- Narrative video: a character bible or no-character rationale, a recurring
  prop/object bible, location, lighting, and wardrobe anchors, and start/end
  frame assets for each model-native clip handoff.
- Layered documentary or editorial reels: load
  [documentary reel](documentary-reel.md). Inventory background, dominant
  subject, foreground, and overlay media per scene. For particles, haze, dust,
  scratches, light artifacts, mattes, and shadows, own provenance, rights,
  dimensions, alpha or black-background suitability, level/edge/loop cleanup,
  expected blend, accepted file, and acceptance check.

## Routes

| Need | Owner |
| --- | --- |
| still creation, edit, upscale, cutout | [ai-image](../../ai-image/SKILL.md) |
| model-native clip | [ai-video](../../ai-video/SKILL.md) |
| voice, music, SFX, Foley, mix | `ai-video` audio mode ([audio](../../ai-video/references/audio.md)) |
| persistent presenter, character, lipsync | `ai-video` avatar mode ([avatar](../../ai-video/references/avatar.md)) |
| raw media metadata, transcript, frames | [intelligest](../../intelligest/references/media.md) |

Every generation packet explicitly rejects SVG, JSX, canvas, and
programmatic-vector scene substitutes and asks for raster or video files. Paid
calls go through `treg` within the operator's weekly cap, with the price quoted
first. This mode never spends on its own; the realization owner does after the
gate.

## Accepted files

Every expected output is a concrete file path with a filename and extension,
never a directory, `TBD`, or "direction packet", even while prompt compilation
is blocked. Keep `accepted_file_ref` empty until the file is inspected and emit
`downstream_asset_handoff: blocked_pending_accepted_file`. A prompt or a
successful provider job is never an accepted file. Preserve supplied URLs
verbatim; when one was not supplied, write the exact missing-input blocker.

## Output template

```text
## Asset Inventory
| Asset | Role | Source | Decision | Owner | Acceptance Check |

## Asset Discovery Receipt
| Asset Need | Source Class | Usage Role | Rights Status | Queries | Candidate Links / IDs | Fit Decision | Result | Owner | Expected Output | Acceptance Check |
Result is exactly selected_source | inspiration_for_generation | searched_no_reference.
Blocked state goes in Fit Decision, never as a fourth Result value.

## Moodboard Decision
| Packet | Inspiration Refs | Transferable Traits | Must Not Copy | Status (pending|accepted) | Accepted At | Approval Source |

## Generation Packets   (only after moodboard acceptance)
| Packet | Decision | Inspiration refs | Transferable traits | Moodboard Accepted At | Must not copy | Prompt / Direction | Owner | Expected Output | Accepted File | Downstream Asset Handoff | Acceptance Check |

## Inspiration Element Map
| Element | Anchor | Asset Decision | Output / Blocker |

## Regeneration Packets
| Packet | Source Element | Anchor | Owner | Prompt / Direction | Acceptance Check |

## Overlay Media Preparation
| Scene | Overlay | File / Blocker | Alpha / Background | Cleanup | Expected Blend | Acceptance |

## Recreation Plan
- Reference pattern / preserve / change / continuity anchors / start-end frames
- Rights and likeness notes / missing inputs

## Done / Proof
- ready_when / evidence / residual_risk
```

A viral reference is not permission to clone exact visuals, likenesses, music,
or protected assets; name the risk and recreate the underlying pattern. Do not
collapse avatar, audio, stills, and clips into one generic prompt; each class
has its own continuity and proof needs.
