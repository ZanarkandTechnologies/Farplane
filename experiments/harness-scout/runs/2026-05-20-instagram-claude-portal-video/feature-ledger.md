# Feature Ledger

| Candidate | Source anchor | Local match | Decision |
| --- | --- | --- | --- |
| Frame-grounded source reconstruction | The video can be reduced to representative frames that show source inspiration, prompt detail, event timing, Claude artifacts, debugging, and final artifact state. | `harness-scout` ingests videos and creates scorecards, but its contract does not yet require frame selection, storyboard inference, or visual acceptance criteria. `video-production`, `remotion`, and `frontend-craft` produce media/UI but do not own external-video-to-skill reconstruction. | `adapt` |
| One-prompt interactive artifact replay | The source claims one prompt can drive a portal landing page with asset, phase, and interaction details. | `frontend-craft`, `landing-page`, `visual-design`, and `visual-qa` already handle frontend implementation and QA. The "one prompt" claim conflicts with Codexter's proof-first workflow and should not be adopted literally. | `hybrid` |
| Embedded event-timeline specification | Visible frame shows animation timing phases such as landing and transition ranges. | `remotion` and `visual-qa` already cover timing and visual proof, but `harness-scout` does not currently emit a time-coded reconstruction brief from source frames. | `adapt` |
| Source-to-skill proposal benchmark | The user is testing whether Codexter can watch a video, extract relevant frames, understand the process, and propose a reusable skill. | `harness-advisor`, `skill-creator`, and `harness-scout` exist, but there is no dedicated evaluation surface for frame-grounded skill proposal quality. | `adapt` |

## Local Baseline

- `FEAT-0011` implements manual harness source ingestion through
  `skills/harness-scout`, `docs/features/registry.jsonl`, and
  `experiments/harness-scout`.
- `FEAT-0014` already upgraded frontend skills; this source does not justify
  another broad frontend rewrite.
- `video-production`, `video-generation`, and `remotion` own video creation and
  deterministic render workflows, not source-understanding.
- `frontend-craft`, `landing-page`, and `visual-qa` can implement and verify a
  portal-style page after a reconstruction brief exists.

## Proposed Skill Shape

Name: `video-reconstruction-scout`

Purpose: turn short-form product/design/coding videos into a frame-grounded
workflow reconstruction, then propose a Codexter-native skill, method, or ticket
handoff without copying source instructions blindly.

Nested method: `video-reconstruction-scout:interactive-artifact-replay`

This method is the "skill inside the skill" for videos like this one: it
extracts frames, infers the source's build loop, converts it into a reproducible
implementation brief, and hands off to `frontend-craft` plus `visual-qa` when
the operator wants an actual remake.
