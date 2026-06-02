# Landing Page Maintenance

## Scope

- `SKILL.md`
- `SKILL.md` Important Checklist
- `README.md`
- `AGENTS.md`
- `references/*`
- `scripts/*`

## Boundaries

- `landing-page` owns one-page story, sections, visual scenes, media, and scrolltelling plans.
- Use the planner/executor split: no approved `LANDING_SPEC.md`, no build handoff.
- Premium/cinematic pages require generated or real asset evidence; code-native
  visuals alone are prototype support, not final media proof.
- Product/device/equipment pages require realistic product-demo media planning:
  product shots or renders, in-context use, assembly/disassembly or exploded
  views, meaningful parts/features, and scroll/video states that reveal the
  product rather than generic infographics.
- Premium landing-page visual carriers must not be custom SVG illustrations,
  SVG diagrams, or SVG overlay art. Use generated/real raster media, or real
  WebGL/Three.js scenes when procedural visuals are warranted. See `MEM-0080`.
- JSON registries under `references/` own repeatable landing recipes, taste profiles, and effect stacks.
- `visual-design` owns visual system decisions.
- `frontend-craft` owns implementation orchestration.
- Official GreenSock skills or docs own GSAP implementation details.
- [frontend-craft three-js.md](../frontend-craft/references/three-js.md) owns Three.js/WebGL/R3F implementation references for 3D landing assets.

## Checks

- Keep first-load instructions enough to produce a landing brief without references.
- Keep the `SKILL.md` Important Checklist as the ordered modern scroll-scrub recipe; avoid moving it into hidden parser state or duplicating all of it in `SKILL.md`.
- For modern Terminal/Terminus-style landing work, treat the `SKILL.md`
  Important Checklist as the mandatory pre-build recipe before implementation.
  See `MEM-0090` and `MEM-0124`.
- Keep `references/terminal-scroll-review.md` and `scripts/terminal_landing_score.py` aligned when changing Terminal/Terminus scoring dimensions.
- Keep motion guidance as routing, not stale API snippets.
- Keep section-quality and designer-judgment QA aligned with the planner gates.
- Keep asset-evidence lint aligned with the asset generation/provenance contract.
- Keep product-demo requirements strong enough that generic infographics cannot
  satisfy premium product-page claims.
- Keep SVG bans explicit enough that section visuals cannot regress into
  hand-authored SVG diagrams.
- Keep scroll-scrub QA strict enough to fail when a pinned scene scrolls out of
  view even if progress, labels, media time, or frame sources continue to
  advance. See `MEM-0083`.
- Keep generated-video evidence strict enough to reject Seedream/image stills
  assembled with local `ffmpeg` as video-generation proof. See `MEM-0084`.
