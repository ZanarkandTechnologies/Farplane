# Remotion Render Todos

Use this as the ordered checklist whenever `remotion-render` is active.

- [ ] Confirm the job is code-rendered Remotion/React video, not model-native text-to-video, image-to-video, avatar/lipsync, or video editing.
- [ ] For authoring, debugging, or improving Remotion code, use [remotion](../remotion/SKILL.md) before this render skill.
- [ ] State the source component, composition id, props, width, height, fps, duration, codec needs, output path, and handoff path before rendering.
- [ ] Use [research:official-docs](../research/SKILL.md#researchofficial-docs) or [research:code-patterns](../research/SKILL.md#researchcode-patterns) when Remotion render behavior, inference.sh app behavior, local code patterns, or source assets shape the render.
- [ ] Use [plan](../plan/SKILL.md) when choosing render settings, local vs external route, codec, output package, or scope cut.
- [ ] Load `references/remotion-render.md` before relying on app-specific render behavior.
- [ ] Capability-gate with `command -v belt`, `belt app get infsh/remotion-render`, and `belt app sample infsh/remotion-render --save <input.json>` before relying on the inference.sh schema.
- [ ] Keep TSX readable in a workspace file or clearly escaped JSON input.
- [ ] Treat `belt app run infsh/remotion-render` as external compute/spend and run it only when acceptable.
- [ ] For long renders or multiple compositions, use `--no-wait`, record task IDs in `jobs.md`, and poll with `belt task get <task-id>`.
- [ ] Save the source TSX, input JSON, result JSON, logs or failure notes, final MP4, and notes inside the workspace.
- [ ] If the rendered video is used in a frontend, hand off to [frontend-craft](../frontend-craft/SKILL.md) and [visual-qa](../visual-qa/SKILL.md) when layout or taste is affected.
- [ ] Do not route model-native video requests through this skill; use [video-generation](../video-generation/SKILL.md) for those.
- [ ] Follow the [execute](../execute/SKILL.md) proof and writeback loop before claiming render, artifact, or final video quality.
