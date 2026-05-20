# Video Reconstruction Brief

## Source

- `source_id`: `SRC-0008`
- `ingest_bundle`: `media-ingest-bundle.md`
- `transcript_status`: visual-only; no full audio transcript stored
- `confidence_limits`: visible UI, prompt, timing, and final artifact evidence
  are usable; spoken narration details remain unverified.

## Storyboard

| Frame / time | Evidence | Claim or action | Confidence | Implication |
| --- | --- | --- | --- | --- |
| source setup | source and post metadata | Creator is showing a source inspiration video/post that can be reconstructed. | medium | Treat the Instagram video as evidence, not instructions. |
| image prompt | `evidence/frames/image-prompt.jpg` | The workflow starts by generating or refining a portal-style hero image asset. | high | Copied skill needs asset-generation and prompt/provenance steps. |
| event timing | `evidence/frames/event-timing.jpg` | The workflow defines animation phases such as landing and transition windows. | high | Copied skill needs explicit timeline phases, not only visual styling. |
| prompt checklist | `evidence/frames/prompt-checklist.jpg` | The creator preserves a reusable master prompt or checklist. | medium | Harness copy should extract source todos and map them into skill todos. |
| final artifact | `evidence/frames/final-artifact.jpg` | The output is a composed interactive portal page with layered imagery, text, controls, and motion affordances. | high | Target owner is `frontend-craft`; proof needs screenshots/source-frame comparison. |

## Source Todos

- [ ] Capture the inspiration/source frames and identify the desired final
  interaction.
- [ ] Generate or refine the main visual asset for the scene.
- [ ] Break the scene into reusable visual layers and UI overlays.
- [ ] Define animation phases, timing windows, and transition states.
- [ ] Compose the layers into a browser artifact.
- [ ] Iterate/debug the generated artifact rather than trusting one-shot output.
- [ ] Preserve the reusable prompt/checklist as a repeatable method.
- [ ] Verify the final artifact against the source frames.

## Skill Comparison

| Source todo | Local skill/todo match | Decision | Note |
| --- | --- | --- | --- |
| Capture inspiration/source frames | `harness-scout`, `media-ingest`, `video-understanding` | `covered` | `TASK-0158` now owns this general route. |
| Generate or refine main visual asset | `imagegen`, `image-generation`, `frontend-craft` asset routing | `augment` | `TASK-0159` should make the generated-layer plan explicit. |
| Break scene into visual layers/UI overlays | `frontend-craft`, `image-generation` background removal | `augment` | Needs a composed-scroll method checklist. |
| Define animation phases/timing | `frontend-craft` motion routing, `visual-qa` proof | `augment` | Needs scroll/timed phase contract. |
| Compose layers into browser artifact | `frontend-craft` | `augment` | This is the primary copied skill owner. |
| Iterate/debug generated artifact | `frontend-craft`, `visual-qa`, `web-design-guidelines` | `covered` | Must be pulled into the method proof checklist. |
| Preserve reusable method/todos | `skill-creator`, `frontend-craft` references | `augment` | `TASK-0159` should add final skill todos. |
| Verify against source frames | `visual-qa`, `landing-page` scroll QA | `covered` | Proof should compare source frames to implementation states. |

## Copied Skill Candidate

- `candidate`: `frontend-craft:composed-scroll-animation`
- `likely_owner`: `skills/frontend-craft`
- `supporting_skills`: `imagegen`, `image-generation`, `visual-qa`,
  `landing-page`, `web-design-guidelines`
- `acceptance_criteria`: method route exists, final skill todos exist, layer
  manifest guidance exists, and a bounded `SRC-0008` reimplementation attempt
  produces screenshots/source-frame comparison plus a gap report.
- `proof_requirements`: selected source frames, layer manifest, prototype or
  build brief, screenshots, source-frame comparison, gap report, registry
  checks.

## Gaps

- [ ] Attach a full Whisper transcript when available.
- [ ] Implement `frontend-craft:composed-scroll-animation` in `TASK-0159`.
- [ ] Run a bounded reimplementation attempt and compare output frames to this
  brief.
