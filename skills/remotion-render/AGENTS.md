# Remotion Render Skill Instructions

Keep this skill separate from `video-generation`. It turns React/Remotion component code into video, so the primary artifact is TSX and deterministic render configuration, not a model prompt.

`references/remotion-render.md` is copied from the upstream inference.sh `tools/video/remotion-render/SKILL.md`. Refresh it from upstream instead of rewriting it by hand.

Use `remotion` for authoring and improving Remotion code. Use this skill only for inference.sh rendering and the artifact contract around MP4 output.

For long-running or batched renders, require saved `input.json`, `result.json`, task IDs, and `jobs.md` before continuing in parallel or handing polling to another lane permitted by the current harness policy.

Do not hide complex Remotion code inside shell one-liners. Prefer workspace files or clearly escaped JSON inputs, then render through `belt` only after capability and spend gates are clear.
