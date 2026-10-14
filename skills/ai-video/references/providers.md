---
title: AI Video Provider Routes
owner: ai-video
status: active
kind: provider-reference
updated_at: 2026-10-12
---

# AI Video Provider Routes

Load this in N3 when choosing a model, quoting a price, or falling back from
the default route. Live catalog checks win over this table: model names and
prices move faster than this file.

## Default route: treg

Paid video, avatar, and image-to-video models run through the treg MCP. treg
lists video and image generation (Seedance, Veo, Wan, Gemini Image, GPT Image,
Seedream) and voice.

```text
treg_route(job) -> catalog_search(<what you want to do, not a vendor>)
               -> catalog_get(<listing>)   # parameters, price, measured reliability
               -> price quote to the operator's spend log terms
               -> call(...) | call_media(...)
               -> review(call_id, usefulness) when the result invites it
```

- Search by job ("image to video with end frame", "talking head lipsync",
  "video upscale"), then let `catalog_get` rank providers by measured success,
  speed, and price.
- Quote the price before the call. Spend stays inside the operator's weekly
  cap and is logged with the model and route, for example
  `Seedance 2.5 6 s 480p clip via treg`.
- A treg call or job ID is a receipt, not an accepted file. Download the media
  into the bundle and inspect it before acceptance.

## Model map (verify live)

| Job | Default family via treg | When to pick another |
| --- | --- | --- |
| Text-to-video, image-to-video, start/end-frame chains | Seedance 2.5 | Veo when the shot needs top realism or native dialogue audio; Wan for cheap drafts and many takes |
| Reference-to-video (several identity or spatial refs) | Seedance reference mode | Veo or Wan reference modes when Seedance rejects the reference set |
| Copy a reference clip's camera move or effect (e.g. a 3D black-bar pop-out hook) | Seedance 2.5 reference mode: the rights-safe effect clip as `@Video1` (motion and effect only), the subject still as `@Image1`, prompt `recreate @Video1's move and effect with @Image1; keep everything else` | After two failed adherence checks, generate a plate and composite the effect in HyperFrames |
| Avatar, talking head, lipsync | The listing `catalog_search("talking head lipsync")` ranks first | Fallback `pruna/p-video-avatar`, `bytedance/omnihuman-1-5`, `falai/fabric-1-0`, `falai/pixverse-lipsync` via `belt` |
| Natural-language video edit | The listing `catalog_search("edit video with a text instruction")` ranks first | Fallback `alibaba/happyhorse-1-0-video-edit` via `belt` |
| Video upscale | The listing `catalog_search("upscale video")` ranks first | Fallback `falai/topaz-video-upscaler` via `belt` |
| Start/end frames, posters, character sheets | Route to [ai-image](../../ai-image/SKILL.md) (GPT Image 2/2.5, Gemini Image, Seedream via treg) | none here |
| Voice | Fish Audio through `scripts/execute_fish_audio.py` | ElevenLabs voice; treg voice listings only when both are blocked |
| Music | ElevenLabs through `scripts/execute_elevenlabs.py` | none without operator acceptance |
| Common SFX | SoundButtonsWorld candidate search first ([audio](audio.md)) | ElevenLabs SFX generation after the operator decides |

Observed reference price: a 6 s Seedance 2.5 clip at 480p cost about USD 0.71
via treg on 2026-10-12. Use it only to sanity-check a live `catalog_get`
quote, never instead of one.

Not on treg (searched 2026-10-14): Google Flow's Omni Flash is a credit-billed
web UI, so Flow stays an operator-run manual route and agent runs use the treg
Veo 3.1 or Seedance 2.5 listing. Higgsfield (MCP or app) bills its own credits;
use it only as a fallback with a recorded reason.

## Fallback route: inference.sh (`belt`)

Use `belt` only when treg has no listing for the needed model or the listing
fails, and record the reason in the receipt. Before any `belt app run`:

1. Load [reference overrides](reference-overrides.md).
2. Check `command -v belt`, `belt app get <app>`, and `belt app sample <app>`;
   never trust a cached schema.
3. Treat `belt app run` as spend under the same cap and log.

Upstream app docs for this route live in `tools/`:
[CLI](tools/infsh-cli.md), [Veo](tools/google-veo.md),
[image-to-video](tools/image-to-video.md), [P-Video](tools/p-video.md),
[P-Video-Avatar](tools/p-video-avatar.md),
[avatar models](tools/ai-avatar-video.md), [HappyHorse](tools/happyhorse.md),
[Seedance 2.0](tools/seedance.md).

Copied upstream references are read-only usage docs. Do not run their
`npx skills add ...` commands unless the operator asks.

## Capability checks before spend

For every provider call, confirm from the live schema: first frame, end frame,
reference count, duration, aspect ratio, resolution, seed, audio switch
(`generate_audio`), and watermark. When the schema lacks an end-frame field,
record that clip N+1 will start from clip N's extracted last frame instead.
