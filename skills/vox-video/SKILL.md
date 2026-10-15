---
name: vox-video
description: "Use for \"make a Vox-style video\", \"paper collage explainer\", \"Vox ad for this product\" or \"explain X Vox style\": a narrated paper-collage reel with verified narration, exact labels and one final MP4."
source: local
department: marketing
template_uses:
  skill-template: "0.6.8"
allowed-tools: Read, Write, Bash, WebSearch, WebFetch
---

# Vox Video

## Context

Use this when the operator wants a short narrated video in the Vox explainer
look: torn paper, hand-cut shapes, two fixed colours, motion that acts out each
spoken line. It covers a product or offer ad and a pure explainer that sells
nothing, and returns one assembled MP4.

The motion comes from a video model (Veo 3.1 Fast through treg), not layered
stills: in the October 2026 bake-off, layered HyperFrames cut-outs read as
animated slides. Narration and on-screen words never come from the video
model: it misspoke the headline number and smudged its own type. Assembly is
ffmpeg through `scripts/vox_assemble.py`, not HyperFrames. The idea came from
holy-templar/vox-animated-ad-mcp (AGPL); no text was taken from it.

It does not post (`social-content`, `zernio`), make stills alone (`ai-image`),
or build reels from real archive photos and maps (`storyboard` documentary
reel).

## Skill Signature

```text
vox_video(subject, mode?: ad | explainer, materials?, product_image?, mascot_image?, aspect?: 9:16 | 16:9, length_s?)
  -> reel_bundle { final.mp4 + sheets + script + brief + prompts + jobs + receipt } | blocked
reads: the operator's materials, up to 3 web searches, live treg catalog
does: researches, writes and records the voice-over, checks it, generates silent collage clips, assembles with exact labels
writes: .farplane/vox-video/<date>-<slug>/, the spend line in ~/.farplane/USER.md
returns: final.mp4 path, transcript check, contact sheet, spend, review verdict
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Lock the brief in one pass.**
  `request + materials -> brief.md {mode, subject, faceless|mascot, aspect, length} | blocked`

  Rule: Infer the mode, aspect (default 9:16) and length (default 15-20 s) and
  ask only for what is missing; an explainer has no offer and no call to
  action unless asked. Faceless is the default. A mascot who is a real person
  needs a consent note and stays a photograph cut out with a torn paper rim,
  never redrawn. A product ad wants the product image; without one, describe
  the product from the operator's details.

  Assert:
  - brief.md names mode, faceless or mascot, aspect, length and bundle path before any spend.
- [ ] **N2 — Find the specifics the script hangs on.**
  `brief -> 3-6 sourced facts in brief.md`

  Rule: Read the operator's materials first, then at most three web searches
  (catalog lookups do not count), snippets only, plus one fetch of a URL the
  operator gave. Keep the named thing, the person and year, the surprising
  number, the buyer's own words. Thin results are a one-line note.

  Example: `"why robots can't fold laundry" -> $16,000 Laundroid, bankrupt 2019; Moravec 1988; cloth changes shape on every grab`

  Assert:
  - Every fact in the script appears in brief.md with its source.
- [ ] **N3 — Write the voice-over as one picture per sentence.**
  `facts -> script.txt + beats.md {line, verb, paper action, label, must_hear}`

  Rule: Follow [craft](references/craft.md). Size the script at about 2.8
  words a second, one idea per sentence. Each sentence gets one paper action
  from its verb and at most one 1-3 word label. List must-hear facts as
  whisper writes them: digits with sign and unit ("-38 degrees", "$16,000").

  Assert:
  - Every beat has one paper action, at most one label, and must_hear is non-empty.
- [ ] **N4 — Record the narration first and check it.**
  `script.txt -> vo.wav + transcript + sentence ends | re-record`

  Rule: One TTS voice for the whole reel via [recipes](references/recipes.md),
  plain script text with no style cue. Transcribe with whisper-cli; if a
  must-hear fact is wrong, or the take misses the target length by more than
  20%, edit and re-record before any video spend. Group whole sentences into
  windows and give each the nearest clip length (4, 6 or 8 s) that keeps its
  retime within 0.6-1.7x; e.g. a 3.8 s window takes a 6 s clip (1.6x).

  Assert:
  - The transcript holds every must-hear fact before any video call.
  - Every window holds whole sentences and fits the retime range.
- [ ] **N5 — Generate the silent collage clips.**
  `beats + windows -> c<N>.mp4 + jobs.md | regenerate`

  Rule: Topology is `deliberate_scene_breaks`: each window is its own scene
  joined by paper tears, so no scene grid or end-frame chain is needed. Write
  each prompt from the craft checklist, save it as prompts/c<N>.json, quote
  the price, submit 2 s apart, record ids in jobs.md, and download each file
  as soon as it succeeds. For a product or mascot, make the start frame with
  `ai-image` and pass it as `image`.

  Assert:
  - Every clip exists locally with its saved request body and job id.
- [ ] **N6 — Inspect the clips, then assemble.**
  `clips -> 2 fps sheets -> plan.json -> final.mp4 | regenerate`

  Rule: Make a sheet per raw clip (`vox_assemble.py --sheet c1.mp4`).
  Regenerate once for stray text or digits, a photographic person or hand
  (except the consented mascot from the start frame), a recurring prop that
  changed, or a missed beat. Write plan.json with `script` and `must_hear`,
  place each label on its word, check its whole duration on the sheet for a
  subject moving into it, and run `uv run --with pillow python
  <repo>/skills/vox-video/scripts/vox_assemble.py plan.json`.

  Assert:
  - The script exits 0: plan valid, transcript similarity at least 0.85, no missing fact.
- [ ] **N7 — Review the reel until TAS-A.**
  `final.mp4 -> review(video-quality) -> TAS-A | revise | blocked`

  Rule: Run the `review` skill with family `video-quality`, as an independent
  reviewer when one is available, on the final, its sheet and the
  transcript. On TAS-B, fix the named checks and review again; after three
  rounds, report the open checks as the blocker. Self-review never counts.

  Assert:
  - The output names the family, the number of rounds, and the final TAS.
- [ ] **N8 — Hand back the reel.**
  `reviewed reel -> receipt.md + spend line -> outbound-check before posting`

  Rule: Write receipt.md (route, prompts, job ids, rejected takes and why,
  checks, spend) and add the spend line. Anything to be posted goes through
  `outbound-check` first.

  Assert:
  - The reply names the final path, the transcript status, the TAS and the spend.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Baked model narration is not a draft to fix later: in the bake-off Veo said
  "$6,000" for $16,000 and the clip still looked finished.
- "Read this like a calm narrator: ..." in TTS text was spoken aloud and made a
  23 s take of a 14 s script.
- "No text" is not enough for props that carry markings: a thermometer came
  back with "10" on its scale until the prompt said "no scale, no digits".
- A white paper boot in one clip became a black boot in the next because the
  prompts described it differently.

## Reference Map

- [craft](references/craft.md) - N3 and N5: script shapes, verb-to-paper
  table, clip prompt checklist, label placement.
- [recipes](references/recipes.md) - N4 and N5: TTS and Veo request bodies,
  polling, rate limit, transcription commands.
- [laundry-robot example](examples/laundry-robot/example.md) - the bake-off
  trace and why the old route and the upstream method lost.

## Output

```yaml
status: worked | partial | blocked
bundle: .farplane/vox-video/<date>-<slug>/
final: final.mp4 (<duration> s, <aspect>)
transcript: pass | fail (<missing facts>)
review: video-quality TAS-<x> after <n> rounds
spend: <USD> logged
next: outbound-check before posting | none
```
