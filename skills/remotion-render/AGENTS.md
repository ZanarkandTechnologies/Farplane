# Remotion Render Skill Instructions

Keep this skill separate from `video-generation`. It turns React/Remotion component code into video, so the primary artifact is TSX and deterministic render configuration, not a model prompt.

`references/remotion-render.md` is copied from the upstream inference.sh `tools/video/remotion-render/SKILL.md`. Refresh it from upstream instead of rewriting it by hand.

Do not hide complex Remotion code inside shell one-liners. Prefer workspace files or clearly escaped JSON inputs, then render through `belt` only after capability and spend gates are clear.
