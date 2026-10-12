---
title: Storyboard Package Template
owner: storyboard
status: active
kind: template
updated_at: 2026-10-12
---

# Storyboard Package Template

Render the sections the selected modes produce. The `plan` block goes in the
GitHub issue body under `Change Plan`; long sections may live in a linked file
under `.farplane/storyboard/<date>-<slug>/` with the link in the issue.

```text
## Content Production            (plan mode; issue body, Change Plan)
- Target / audience / platform:
- Creative hypothesis / accepted references:
- Constraints / timing assumption:

| Order | Owner | Accepted inputs | Primary output | Gate or blocker | Next handoff |
| ---: | --- | --- | --- | --- | --- |

## Hook Decision                 (short-form, latest-news, title-led work)
- Source title:
- Candidates (10+, 6+ lenses, at most 2 per lens):
  | Lens | Hook | keep / reject + reason |
- Rejected lines (blocked terms, synonym swaps, weakened evidence) + reasons:
- Finalists (3+):
- Source-title contest:
  | Line | Immediate meaning | Curiosity | Accuracy | One breath | Drawable first frame | Verdict |
  | Source title | | | | | | |
  | Finalist A..C | | | | | | |
- Winner + why it beats the source title:
- Rejected finalists + reasons:
- First 3 seconds: on-screen copy / voiceover / visual action / evidence qualifier

## Narrative Signatures
- Hook / Tension / Turn / Proof moment / Payoff / Final action

## Beat Sheet and Script        (two columns: narration | visual direction)
| Beat | Narration or copy | Visual direction | Function (evidence/explanation/soul) | Viewer state before -> after |

## Storyboard
| Scene | Time | Background | Main topic | Foreground | Copy/VO | Motion | Audio | Proof |

## Continuity Handoff
- Viewer question -> answer:
- Recurring character / no-character rationale:
- Recurring object or motif:
- Generation topology: continuous_chain | deliberate_scene_breaks | montage
- Frame pairs (continuous_chain): clip N start frame -> end frame
- Scene breaks / transitions:

## Scene Grid Packets            (deliberate_scene_breaks)
| Scene | Target s | Clean grid | Annotated grid | Panel IDs | Action / camera / end state | Provider strategy | Transition / audio | Reuse |

## Asset Plan                    (assets mode; see references/asset-plan.md)
## Edit Direction                (edit mode; see references/edit-direction.md)

## HyperFrames Handoff
- Dimensions / fps / duration / timing master:
- Accepted files (paths) or exact blockers:
- Edit recipe ref:
- Proof frames and ranges:
- Approval: operator approved at / approval source

## Notes
- Rejected angles / taste notes / blockers / next owner
```
