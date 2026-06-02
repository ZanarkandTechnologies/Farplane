# Long-Running Jobs

Use this when video generation, image-to-video, avatar rendering, upscaling, or multi-clip production may take longer than a normal foreground command.

## Default Pattern

1. Create a stable bundle folder before running compute.
2. Save `input.json` and `prompt.md` first.
3. Start independent jobs with `belt app run <app> --input <input.json> --no-wait --save <result.json>` when the app and CLI support async.
4. Record each task in `jobs.md`.
5. Poll with `belt task get <task-id>`.
6. Copy or download the final media into the project asset path before wiring it into a website.

## `jobs.md` Template

```markdown
# Video Generation Jobs

| Asset | App | Task ID | Input | Result | Final path | Status | Next check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hero-loop | google/veo-3-1-fast | task_... | input.json | result.json | public/video/hero.mp4 | running | 2026-05-07 15:30 +08 |
```

## Polling Rules

- Do not depend on terminal scrollback for task IDs or result URLs.
- If the CLI returns a task ID but not a local result, write the task ID into `jobs.md` immediately.
- Use adaptive backoff from `docs/specs/adaptive-backoff.md`: start around
  `30s` for images and short clips, around `2m` for longer videos or upscales,
  widen unchanged pending checks up to a practical cap, and reset or shorten
  the delay when a job shows progress.
- Honor service-provided timing such as ETA, queue position, or next-check
  hints before applying local defaults.
- When a job finishes, update `result.json`, copy final media to the asset path, and note any failed or rejected jobs.
- If a thread wakeup/timer tool is available and the user wants the thread to continue later, create a heartbeat that includes the task IDs, result paths, and next action.

## Delegation

Use a delegated polling or QA lane only when current harness policy permits delegation, the batch is independent, and the lane can write back concrete workspace artifacts. The lane must return task IDs, result paths, final media paths, failures, and any jobs still pending.

Keep the main agent moving on non-dependent work: layout, copy, fallback posters, CSS, Remotion code, or QA scaffolding. Do not claim the final asset integration is complete until the media exists locally or the remote result has a recorded copy plan.
