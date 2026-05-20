# Replay Log Fixture

This fixture lets an agent test video understanding without downloading,
playing, or natively understanding a video.

## Fixture Inputs

- `media-ingest-bundle`:
  `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/media-ingest-bundle.md`
- `selected-frame reconstruction`:
  `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-reconstruction-brief.md`
- `corrected handoff`:
  `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/handoff.md`
- `smoke log`:
  `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-understanding-smoke-log.md`

## Replay Steps

1. Read transcript status and confidence limits.
2. Read the storyboard table.
3. Extract the source todos.
4. Compare each source todo to local skills.
5. Produce a copied-skill candidate and owner handoff.

## Expected Output

- `transcript_status`: visual-only / no full transcript stored
- `source_todos`: capture source frames, generate/refine asset, isolate
  layers, define timing, compose browser artifact, debug, preserve method,
  verify against frames
- `primary_owner`: `frontend-craft`
- `method`: `frontend-craft:composed-scroll-animation`
- `supporting_skills`: `imagegen`, `image-generation`, `visual-qa`,
  `landing-page`, `web-design-guidelines`
- `confidence_limit`: spoken narration remains unverified until a transcript is
  attached

## Pass Condition

The agent passes the fixture if it routes general video handling to
`harness-scout` plus support skills, and routes the specific copied frontend
method to `frontend-craft`.
