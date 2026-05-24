# Long-Running Jobs

Use this when image generation, edits, background removal, upscaling, or large asset batches may take longer than a normal foreground command.

## Default Pattern

1. Create a stable bundle folder before running compute.
2. Save `input.json` and `prompt.md` first.
3. Start independent jobs with `belt app run <app> --input <input.json> --no-wait --save <result.json>` when the app and CLI support async.
4. Record each task in `jobs.md`.
5. Poll with `belt task get <task-id>`.
6. Copy or download the final image into the project asset path before wiring it into a website.

## `jobs.md` Template

```markdown
# Image Generation Jobs

| Asset | App | Task ID | Input | Result | Final path | Status | Next check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hero-poster | openai/gpt-image-2 | task_... | input.json | result.json | public/images/hero.png | running | 2026-05-07 15:30 +08 |
```

## Polling Rules

- Do not depend on terminal scrollback for task IDs or result URLs.
- If the CLI returns a task ID but not a local result, write the task ID into `jobs.md` immediately.
- Poll at practical intervals: 1-3 minutes for images, 5-10 minutes for large upscales or many variants.
- When a job finishes, update `result.json`, copy final media to the asset path, and note any failed or rejected jobs.
- If a thread wakeup/timer tool is available and the user wants the thread to continue later, create a heartbeat that includes the task IDs, result paths, and next action.

## Delegation

Use a delegated polling or QA lane only when current harness policy permits delegation, the batch is independent, and the lane can write back concrete workspace artifacts. The lane must return task IDs, result paths, final media paths, failures, and any jobs still pending.

Keep the main agent moving on non-dependent work: layout, copy, fallback placeholders, CSS, Remotion code, or QA scaffolding. Do not claim the final asset integration is complete until the media exists locally or the remote result has a recorded copy plan.
