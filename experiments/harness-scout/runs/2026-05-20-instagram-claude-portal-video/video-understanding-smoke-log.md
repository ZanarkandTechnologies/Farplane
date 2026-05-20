# Video Understanding Smoke Log

- `source_id`: `SRC-0008`
- `mode`: text-only replay; no native video playback required
- `input_bundle`: `media-ingest-bundle.md`
- `input_brief`: `video-reconstruction-brief.md`
- `checked_at`: 2026-05-21 01:30 +0800

## Replay Input

- Transcript status is `visual-only / no full transcript stored`.
- Selected frames show image prompt, event timing, prompt checklist, and final
  artifact.
- Retention note confirms raw MP4 and bulky raw extracts are not tracked.

## Expected Source Todos

- capture source frames
- generate or refine the scene asset
- isolate layers
- define timing phases
- compose browser artifact
- debug/iterate
- preserve method
- verify against frames

## Expected Skill Comparison

| Todo group | Expected local route |
| --- | --- |
| source capture / evidence | `harness-scout`, `media-ingest`, `video-understanding` |
| asset generation / cutouts | `imagegen`, `image-generation`, `frontend-craft` |
| timing / composition | `frontend-craft`, `visual-qa` |
| source-frame proof | `visual-qa`, `landing-page` QA references |

## Expected Handoff

- `primary_owner`: `frontend-craft`
- `method`: `frontend-craft:composed-scroll-animation`
- `supporting_skills`: `imagegen`, `image-generation`, `visual-qa`,
  `landing-page`, `web-design-guidelines`
- `not_owner`: standalone video wrapper skill

## Result

Pass. The text artifacts are enough to test the route and owner decision without
native video understanding.
