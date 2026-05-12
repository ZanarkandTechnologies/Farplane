# Video Generation

Category-level skill for generating, editing, assembling, and QA-ing project-bound video assets.

## Purpose

Keep video generation as the model/app execution skill with the upstream umbrella model map in `SKILL.md` and provider-specific detail in references. Domain video guides are separate public skills.

## Entry Point

- `SKILL.md`: trigger rules, upstream umbrella model map, routing, spend gates, output contract, and frontend handoff.
- `todos.md`: ordered routing checklist for choosing the right reference.
- `references/tools/`: upstream inference.sh tool `SKILL.md` files copied as reference material.
- `references/domain-production.md`: shared routing, artifact saving, async, and upstream-safety workflow for domain video skills.
- `references/long-running-jobs.md`: async `--no-wait`, task ID, polling, timer, and delegation guidance.
- `references/reference-overrides.md`: local overrides for stale upstream commands and app IDs.
- `references/prompting/video-prompting-guide.md`: copied upstream video prompting guide for shot, camera, lighting, pacing, and model-specific phrasing.
- `references/frontend-asset-qa.md`: Codexter handoff rules for web use.

Use `SKILL.md` for routing. Use `todos.md` to select only the relevant branch:

- `references/tools/infsh-cli.md`: `belt` CLI usage.
- `references/tools/*.md`: provider/app instructions.

Use separate domain skills for artifact-level work:

- `ai-marketing-videos`
- `explainer-video-guide`
- `storyboard-creation`
- `talking-head-production`
- `video-ad-specs`

Prompting guidance lives inside each artifact skill as `references/prompting.md`, with the upstream video prompting guide kept as `references/prompting/video-prompting-guide.md` for general video prompt quality. Do not create a standalone public `video-prompting-guide` skill.

Remotion code authoring lives in `skills/remotion/`. Inference.sh MP4 rendering for Remotion lives in `skills/remotion-render/`.

## Minimal Example

```bash
belt app get pruna/p-video-avatar
belt app sample pruna/p-video-avatar --save output/video-generation/avatar/input.json
```

Then edit `input.json`, run with `belt app run ... --save result.json` only when external compute/spend is acceptable, and copy the final video into the project asset path.

## How To Test

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/video-generation
belt --help
belt app list --category video
```
