# Video Production

## Purpose

Own domain-level video workflow planning through method addresses while leaving
model execution, Remotion authoring, and rendering in their specialized skills.

Use this skill for:

- marketing and promo videos
- explainers and product demos
- storyboards, shot lists, and animatics
- talking-head, avatar, and lipsync workflows
- platform-specific ad specs and paid-social creative

Use `video-generation` for model-native video execution, `remotion` for
deterministic Remotion code authoring, `remotion-render` for MP4 rendering, and
`image-generation` or `imagegen` for still assets.

## Entry Point

- `SKILL.md`: method selection, routing, references, and handoff boundaries.
- `SKILL.md` Todo List: ordered conditional checklist.
- `references/upstream-*.md`: copied upstream/domain guides by method.
- `references/prompting-*.md`: copied method-specific prompting guidance.

## Minimal Example

For a product launch ad:

1. Select `video-production:marketing`.
2. Add `video-production:ad-spec` only if paid placement constraints matter.
3. Draft the brief, shot list, prompt set, and proof plan.
4. Route clips through `video-generation`, stills through `imagegen` or
   `image-generation`, and deterministic edits through `remotion` or
   `remotion-render`.

## How To Test

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/video-production
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 bin/validators/check_skill_todo_tiers.py --allow-peer-tier3
```
