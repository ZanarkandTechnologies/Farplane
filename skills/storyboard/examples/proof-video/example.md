---
title: Proof Video Storyboard Example
owner: storyboard
status: active
kind: skill-example
updated_at: 2026-10-12
---

# Proof Video Example

A 20-second vertical proof video, storyboarded and handed to HyperFrames
without rendering. Use it to calibrate the package shape, not as copy to reuse.

## Input

```text
idea: Farplane turns agent work into visible proof.
icp: skeptical AI operators who have been burned by vague agent claims.
platform: vertical short video, 1080x1920, 30 fps
duration: 20 seconds
style: crisp product-capture proof demo, restrained motion
cta: read the proof packet
home: active GitHub issue (plan in the body, receipts as comments)
```

## Plan (on the issue's Change Plan)

| Order | Owner | Accepted inputs | Primary output | Gate or blocker | Next handoff |
| ---: | --- | --- | --- | --- | --- |
| 1 | storyboard `script` | brief, ICP, proof packet link | hook decision, script, scene map | operator approves scenes | `assets` |
| 2 | storyboard `assets` | scene map | asset plan + accepted capture files | every layer has an accepted file | `edit` |
| 3 | `ai-video` audio mode | script | voiceover file + measured cue sheet | VO accepted | `edit` |
| 4 | storyboard `edit` | scenes, files, VO cue sheet | timed edit recipe | single timing basis, proof checks named | HyperFrames |
| 5 | HyperFrames (`/hyperframes`) | approved package | composition + render proof | stills at 2s, 9s, 19s pass | `qa` |
| 6 | `qa` / `review` | render + package | readiness verdict | independent verdict | `social-content` |

## Hook Decision (excerpt)

The full lab keeps 10+ candidates across 6+ lenses. Three finalists shown:

| Line | Immediate meaning | Curiosity | Accuracy | One breath | Drawable first frame | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Source: "Farplane turns agent work into visible proof" | medium | low | high | yes | weak | beat |
| "Done is not proof." | high | high | high | yes | green Done badge cracks | winner |
| "Your agent said done. Check." | high | medium | high | yes | chat bubble | finalist |
| "Agents can fake finished work." | high | high | overclaims | yes | weak | rejected: overstates |

First 3 seconds: on-screen "Done is not proof." / VO "Your agent says done. That is not proof." /
a real agent chat ending in "Done" freezes and a question mark lands on it /
qualifier: none needed (no factual claim yet).

## Narrative Signatures

- Hook: Done is not proof.
- Tension: completion claims are easy to fake or misunderstand.
- Turn: Farplane makes the work visible as artifacts and checks.
- Proof moment: the issue shows task, artifact path, check output, and review.
- Payoff: the viewer sees the trust loop in one glance.
- Final action: read the proof packet.

## Storyboard

| Scene | Time | Background | Main topic | Foreground | Copy/VO | Motion | Proof |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| 1 | 0-3s | shared dark desk plate | real agent chat capture ending "Done" | hand on trackpad cutout | Done is not proof. | chat freezes, question mark lands | still at 2s |
| 2 | 3-7s | same plate | real GitHub issue capture | desk edge with notebook | Farplane makes the work inspectable. | issue scrolls to artifact path | legibility still |
| 3 | 7-12s | same plate | real check output capture (validator, QA, review) | monitor bezel edge | Artifact. Check. Review. | three result lines highlight in order | still at 9s |
| 4 | 12-17s | same plate | proof comment with linked evidence | coffee cup and cable | Trust the trail, not the claim. | slow pull back to full comment | layout still |
| 5 | 17-20s | same plate | proof packet page | hand reaching to click | Read the proof packet. | settle, one restrained pulse | final still |

## Assets (route summary)

- Captures: `capture` route from the real issue, chat, and check output;
  sanitized, saved as `assets/scenes/sc0N/main-topic.png` before acceptance.
- Background plate and foreground cutouts: search first; inspired or original
  generation goes to `ai-image` only after the moodboard traits are accepted.
- No SVG or JSX drawings stand in for any scene layer; UI text cards are
  annotations, not assets.

## Done / Proof

- Hook decision, scene map, asset plan with accepted files, and a timed edit
  recipe keyed to the measured VO cue sheet exist on the issue.
- HyperFrames renders stills at 2s, 9s, and 19s before the MP4; `qa` judges them.
- Residual risk: motion taste and pacing need visual QA after the render.

## Notes

- Rejected angle: "AI agents are magic" weakens the proof-first trust claim.
- Blocker until supplied: the real issue and proof packet to capture.
