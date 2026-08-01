---
title: Asset Source Roles And Moodboard Gate
owner: asset-advisor
status: active
kind: reference
updated_at: 2026-08-02
---

# Asset Source Roles And Moodboard Gate

Use this branch when an asset brief mixes production libraries, film frames,
editorial galleries, social discovery, archives, or generation. Verify current
site access and terms when a specific candidate matters; the examples below
describe discovery roles, not durable licensing claims.

## Two Independent Axes

```text
classify_reference(candidate)
  -> usage_role + rights_status + evidence

usage_role:
  production_source | cinematic_reference | taste_discovery |
  archive_reference | generated

rights_status:
  cleared | restricted_reference_only | per_item_verification_required |
  unknown
```

- `production_source`: a candidate intended for direct use after its license,
  provenance, dimensions, and transformation rights are verified.
- `cinematic_reference`: a frame or shot used to study composition, lighting,
  palette, atmosphere, lens, or blocking. ShotDeck and FilmGrab are examples.
- `taste_discovery`: a broad visual surface used to find editorial, fashion,
  material, layout, or mood directions. Savee and Pinterest are examples.
- `archive_reference`: historical or documentary material used for factual or
  period grounding; direct reuse still needs rights verification.
- `generated`: an original output whose provider terms, input rights, likeness,
  and acceptance evidence remain attached to the asset.

The same source class can yield different rights results per candidate. Never
promote `cinematic_reference` or `taste_discovery` to `cleared` because it is
high quality, public, downloadable, or easy to screenshot.

## Moodboard Before Prompt

For `inspired_generation`, reduce references to transferable traits before
writing the final prompt:

```text
moodboard_decision(refs)
  -> composition + lighting + palette + texture_material + camera_editorial
   + must_not_copy + accepted_at

compile_prompt(moodboard_decision)
  -> allowed only when accepted_at exists
```

Record:

- reference URLs and observed evidence;
- the traits accepted from each reference;
- protected expression, exact composition, people/likeness, logos, text,
  signatures, or distinctive props that must not be copied;
- `moodboard_traits_accepted_at` and approval source;
- resulting prompt, owner, output path, rights note, and acceptance check.

## Example

```text
ShotDeck frame
  usage_role: cinematic_reference
  rights_status: restricted_reference_only
  transfer: centered machine silhouette, hard rim light, deep negative space

Pinterest board
  usage_role: taste_discovery
  rights_status: per_item_verification_required
  transfer: restrained grotesk type, brushed-metal texture, warm-gray palette

must_not_copy: exact frame composition, actor likeness, logos, source text
moodboard_traits_accepted_at: 2026-08-02T02:00:00+08:00
```
