---
title: Vox video craft
status: active
owner: skills/vox-video
kind: reference
---

# Vox Video Craft

Load at N3 (script and beat sheet) and N5 (clip prompts). Everything here comes
from Farplane's own reels: the laundry-robot bake-off and the ice run.

## Script shape by register

- **Explainer.** Line 1 is a fact that sounds wrong ("You don't slip on ice.").
  Line 2 flips it. The middle names the mechanism with one number or name.
  The last line restates the opening in one plain sentence, now true. No
  pitch.
- **Ad.** Line 1 is the buyer's problem as they would say it. The middle shows
  life with the product: one concrete change per line. The last line is the
  offer and one action. Product facts appear only where they cause a change.

Script lines that survived the bake-off held a proper noun or a figure
(Laundroid, $16,000, minus 38 degrees). Lines with neither were cut first.

## Beat sheet

One row per sentence:

```text
line | verb in the line | what the paper does | label (0-1, max 3 words) | must_hear?
```

Most rows have no label. Give a label only to a figure, a name, or the one word
the viewer should remember.

## From the line's verb to the paper

Start from the verb the narrator says, not from a mood.

| The line says something… | The paper does this |
| --- | --- |
| fails, breaks, goes bust | cracks along a seam; the cut-out tips over; red shards burst out |
| beats, wins, outperforms | the loser piece falls flat; a small arrow points at it |
| changes, won't hold, shifts | the outline re-cuts itself every half second |
| is grabbed, pulled, handled | a cut-out gripper or hand pinches; the piece crumples on lift |
| is easy vs hard | a vertical tear splits the frame; neat fold on one side, heap on the other |
| rolls, slides, flows | a row of paper beads or a strip slides under the subject |
| costs, saves | a tag swings on a string; coins fall away or stack |
| is unknown, puzzling | a crumpled ball drops in; a cut-out question mark wobbles beside it |

Colour: give each reel one colour for the problem side and one for the
subject or fix, and keep both fixed across every clip (bake-off: deep red and
steel blue; ice run: teal and red). Never orange.

## Clip prompt checklist

The model starts every clip blank, so each prompt repeats all of this:

1. Header: `CLIP n of N (d s). Self-contained scene.`
2. Medium: Vox-style paper collage shot top-down on a desk; torn edges, cut
   card, soft shadows, visible paper grain, warm off-white ground.
3. Palette: the two reel colours and black ink, named the same way every time.
4. Recurring props: the same words for the same object in every clip ("a white
   paper boot with black laces"); otherwise the object changes between clips.
5. Text ban: no letters, digits, words, captions or scale marks anywhere, and
   name the empty zone that must stay blank for labels.
6. People: hands and bodies are flat cut card with no skin texture.
7. No stamp, sign or tag shape where a `stamp` label will land.
8. Cuts: paper tears, peels or slam-ins, no dissolves. Silent.
9. Beats: 2-3 lines timed from `00:00` inside the clip, each acting out one row
   of the beat sheet.
10. Start image (product or mascot only): open exactly on the attached frame and
   keep that object unchanged.

## Labels

`scripts/vox_assemble.py` sets labels in real type: always spelled right, one
font. Time each on the word it names, place it in the zone the prompt kept
blank, and end it before the next clip's subject arrives. `stamp` style for a
verdict word, `paper` for figures and names.
