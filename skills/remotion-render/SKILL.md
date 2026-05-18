---
name: remotion-render
version: 1.0.0
description: Render React/Remotion component code into video through the inference.sh `belt` CLI when available. Use for code-to-video, TSX-to-MP4, programmatic motion graphics, data-driven videos, animated UI sequences, and deterministic React animation exports. Do not use for model-native text-to-video, image-to-video, avatar/lipsync, or video editing; use `video-generation` for those.
tier: 3
group: content-video
allowed-tools: Read, Grep, Glob, Bash
---

# Remotion Render

Render videos from React/Remotion component code.

## First Load

Trigger this skill when the user asks for Remotion, React video, TSX-to-video, code-to-video, programmatic video, data-driven video, animated UI video, or deterministic video rendering.

For authoring, debugging, or improving Remotion code, use `remotion` first. Use this skill when the task is specifically to render that code to MP4 through inference.sh.

Do not use this skill for model-native text-to-video, image-to-video, avatar/lipsync, or video editing. Use `video-generation` for those.

Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from their Related Skills sections unless the user explicitly asks to install upstream skills.

## Steps

1. Load `references/remotion-render.md`.
2. Confirm the job is code-rendered video, not model-native generation.
3. Capability-gate with `command -v belt`, `belt app get infsh/remotion-render`, and `belt app sample infsh/remotion-render --save <input.json>`.
4. Define render settings: width, height, fps, duration, codec when needed, and props.
5. Keep TSX readable in a workspace file or clearly escaped JSON input.
6. Treat `belt app run infsh/remotion-render` as external compute/spend and run it only when acceptable.
7. For long renders or multiple compositions, use `--no-wait`, record task IDs in `jobs.md`, and poll with `belt task get <task-id>`.
8. Save the MP4, input JSON, result JSON, notes, and source TSX in the workspace.
9. If used in a frontend, hand off to `frontend-craft` and `visual-qa` when layout or taste is affected.

## Default Bundle

```text
output/remotion-render/<slug>/
  Main.tsx
  input.json
  result.json
  final.mp4
  notes.md
```
