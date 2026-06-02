# Video-To-Skill Route

Use this reference when a `harness-scout` source is or contains a video that may
teach a reusable skill.

## Minimal Route

1. Run `summarize --extract-only` first.
2. If the source contains video/audio, create a media ingest bundle.
3. If video evidence exists, run video understanding over transcript status,
   selected frames, and contact sheet evidence.
4. Extract the source's operational todos.
5. Compare each source todo against existing Farplane skills and skill checklists.
6. Route the copied-skill candidate to the likely owner skill, using
   `harness-advisor` only when ownership is ambiguous.

## Source Todo Statuses

Use these labels in the source-todo comparison:

- `covered`: Farplane already has the step in an existing skill/todo.
- `augment`: an existing skill is the right owner but needs a new method,
  checklist, reference, or proof requirement.
- `missing`: no good owner exists yet.
- `reject`: the source step is unsafe, too vague, not useful, or conflicts with
  Farplane doctrine.
- `defer`: useful but not needed for the current ticket or evidence is too weak.

## Output Shape

A video-to-skill scout run should leave:

- compact ingest bundle
- reconstruction brief
- source-todo comparison
- copied-skill candidate
- owner handoff
- confidence limits, especially transcript/frame gaps

## Smoke Fixture

Agents can test the route without native video support by reading:

- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/media-ingest-bundle.md`
- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-reconstruction-brief.md`
- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/handoff.md`
- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-understanding-smoke-log.md`

Expected result: the copied-skill owner is
`frontend-craft:composed-scroll-animation`, not a standalone video wrapper.
