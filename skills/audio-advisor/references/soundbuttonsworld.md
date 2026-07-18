---
title: SoundButtonsWorld SFX Candidate Discovery
owner: audio-advisor
status: active
kind: source-reference
created_at: 2026-07-18
updated_at: 2026-07-18
source_url: https://soundbuttonsworld.com/
terms_url: https://soundbuttonsworld.com/terms-of-use
dmca_url: https://soundbuttonsworld.com/dmca-copyright-policy
---

# SoundButtonsWorld SFX Candidate Discovery

Load this before looking for SoundButtonsWorld candidates. This route discovers
item-page links for the operator; it never downloads or approves audio.

## Boundary

The site's terms currently describe personal, noncommercial access, restrict
automated agents/scripts and automated searches or queries, reserve content
rights, and provide a DMCA process for user uploads. Therefore:

```text
soundbuttonsworld_candidates(cues)
  -> candidate_shortlist_for_operator | searched_no_fit
side_effects: no site search automation; no download; no approval
```

Use public search-engine indexing with queries such as
`site:soundbuttonsworld.com/sound-button <effect>` rather than automating the
site search or download controls. Do not crawl or bulk-query item pages.

Candidate availability is not permission. Flag meme, movie, television, game,
song, brand, celebrity, and recognizable voice clips as high risk. The operator
owns download, rights review, and final approval.

## Discovery Workflow

1. Convert each distinctive or commonly available cue into one literal search
   phrase: event/object first, then texture, duration, or emotional qualifier.
2. Search the public web index for SoundButtonsWorld item-page results. Do not
   automate the site's own search, play, or download controls.
3. Return at most three plausible pages per cue. Prefer ordinary effects over
   protected dialogue, music, brands, characters, or recognizable voices.
4. Put the shortlist in the final content implementation plan. If results are
   weak or absent, record `searched_no_fit` and retain the generation fallback.
5. Stop. Do not fetch the MP3, claim rights, or mark the cue production-ready.

## Content-Plan Handoff

```yaml
sfx_candidate_shortlist:
  - cue_ref: scene/time/frame
    search_phrase: literal query
    item_title: result title
    item_page_url: https://soundbuttonsworld.com/sound-button/...
    why_it_might_fit: timing/texture/motion rationale
    rights_risk: low | medium | high with reason
    status: awaiting_operator_download_and_approval
    fallback: approved local file | audio-advisor:sfx generation
searched_no_fit:
  - cue_ref: scene/time/frame
    search_phrase: literal query
    fallback: audio-advisor:sfx generation after operator decision
```

When the operator returns an approved file, treat it as an input asset: probe
format/duration, bind it to the cue, record the supplied rights basis, and hand
placement/mix proof to Remotion. Any source receipt must record
`retrieved_by: operator` and pass `scripts/validate_audio_packet.py`.

## Grounding

- Terms: https://soundbuttonsworld.com/terms-of-use
- DMCA policy: https://soundbuttonsworld.com/dmca-copyright-policy
