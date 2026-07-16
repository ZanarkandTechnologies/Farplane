---
artifact_type: annotated_motion_board_index
profile_id: retro-low-poly-consequence
clean_board: ./ps1-zero-friction-storyboard-board.png
annotated_board: ./ps1-zero-friction-motion-board.png
version: "0.1.0"
---

# PS1 Zero-Friction Motion Board

The clean board owns appearance. The annotated board owns panel identity and
motion direction only. Prompts reference the short ID below; they do not copy
the annotation text into the generated frame.

| ID | Motion note | Fixed ruler | Held end state |
| --- | --- | --- | --- |
| P01 | Hold the hero rigid and almost motionless before the rule fails. | Courtyard grout grid | Balanced standing pose for 0.5 seconds |
| P02 | Both shoes translate outward in opposite directions; pelvis drops vertically. | Each shoe crosses at least two grout seams | Low uncontrolled split held for 1 second |
| P03 | The shoe translates right across the dark seam; no skating in place. | One fixed dark grout seam | Whole sole visibly beyond the seam |
| P04 | The hand and torso slide right along the rail after grip fails. | Two fixed blue rail posts | Hand beyond the second post |
| P05 | Phone falls down-right, contacts pavement, then glides right. | Pavement seam behind the phone | Phone separated from the hand and still moving |
| P06 | Wheel yaws left while the car body continues straight forward. | White stop line and curb | Car past the line without turning |
| P07 | Palms and knees slide backward while the torso advances almost nowhere. | Courtyard grout seams | Unnaturally stretched crawl pose |
| P08 | Crate translates right after release; hero remains behind reaching. | Three concrete slab seams | Clear gap between hands and crate |
| P09 | Cars, crate, and pedestrians maintain separate straight paths that converge. | Crosswalk and lane markings | Readable near-collision geometry from above |

## Provider Binding

```text
Image 1 = clean board: style, character, environment, composition authority.
Image 2 = annotated board: panel IDs and arrows are instructions only.
Active panel(s) = {panel_ids}.
Use the matching motion note above as world-relative action.
Never render the board layout, gutters, IDs, arrows, labels, or notes.
```

For a transition such as `P01 -> P02`, the first ID is the start state and the
second ID is the held end state. Seedance owns the causal motion between them;
Remotion owns only the final edit and any later captions.

## Provider Compatibility Fallback

The full board produced a false-positive real-person privacy rejection in the
live Seedance route. Disabling its optional input prefilter did not bypass the
upstream detector. For a rejected transition, derive the narrowest panel-pair
sheet with an obviously non-human faceted crash-test helmet, retain the same
world/state/arrows, independently review it, and restore the filter.

Measured P01-to-P02 fallback:
`./ps1-zero-friction-motion-board-seedance-safe.png`. It produced a clean
4.04-second Seedance proof: no annotation leakage, both shoes crossed fixed
grout seams outward, the pelvis dropped, and the final split held for the last
second.
